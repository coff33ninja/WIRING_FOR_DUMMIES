# Servo Motor — Component Reference

## What It Is

A servo motor is a **motor you can tell exactly where to turn**. Give it a PWM signal and it rotates to a precise angle (usually 0°–180°) and holds that position against external force.

> **Analogy:** A regular DC motor is like a spinning wheel — it just goes round and round. A servo is like a robot arm at a factory — you say "go to position 90" and it moves there and stops. It knows exactly where it is at all times.

## What's Inside a Servo

```
                  ┌──────────────────────────────┐
                  │                              │
                  │  ┌───┐                       │
  Signal ─────────┤  │   │                       │
                  │  │Control│  ┌──────┐         │
  Power  ─────────┤  │Board  │  │Motor │         │
                  │  │       │  └──┬───┘         │
  GND   ─────────┤  └───┘       │   │           │
                  │              │   │ Potentiometer│
                  │   ┌──────────┘   │  (position   │
                  │   │  Gear train  │   feedback)  │
                  │   └──────────────┘             │
                  └──────────────────────────────┘
```

- **DC motor** — spins the output shaft
- **Gear train** — reduces speed, increases torque
- **Potentiometer** — measures the current shaft position
- **Control board** — compares target position (signal) to actual position (pot), drives motor until they match

## The 3 Wires

```
              ┌──────────────┐
              │              │
              │    SERVO     │
              │              │
              └──────┬───────┘
                  ┌──┴───┐
                  │  │   │
              Signal (+) GND
```

| Wire color (typical) | Name | Connect to |
|----------------------|------|------------|
| **Orange / Yellow / White** | Signal (PWM) | GPIO pin (PWM-capable) |
| **Red** | Power (+) | 5V (or external supply for big servos) |
| **Brown / Black** | Ground (−) | GND (shared with MCU) |

> **Power warning:** Never power a servo from the ESP32/Arduino 5V pin if it's a medium or large servo. The motor draw can exceed 500mA and brown out your microcontroller. Use a separate 5V supply.

## Servo Sizes

| Size | Typical model | Torque | Current | Use case |
|------|--------------|--------|---------|----------|
| **Micro** (9g) | SG90, MG90S | 0.18 N·m | ~200mA stall | Small robots, camera gimbals |
| **Standard** (55g) | MG996R, TowerPro | 0.5–1 N·m | ~1A stall | Robot arms, animatronics |
| **High-torque** (80g+) | DS3218, "20kg" | 0.8–2 N·m | ~2A stall | Heavy lifting, RC cars |

> **SG90 (the most common hobby servo):** Draws ~100–200mA moving, ~700mA stalled. Can run from Arduino 5V pin for a single servo. For multiple servos, use external power.

## Wiring — Single Micro Servo (SG90)

```
ESP32               SG90 Servo
─────               ──────────
GPIO 13 (PWM) ─────── Orange (signal)
5V  ───────────────── Red (power)
GND ───────────────── Brown (ground)
```

## Wiring — Multiple Servos (External Power)

```
                ┌──── SG90 #1 (signal → GPIO 13)
                │
ESP32           │                External 5V Supply
─────           │                ──────────────────
GPIO 13 ────────┤                +5V ──────┬───────
GPIO 14 ────────┼──── SG90 #2   GND ───────┴──┬────
                │                             │
               GND ───────────────────────────┤
                │                             │
VIN (or USB) ────────────────────────────────┘
```

> **Always share GND between the ESP32 and the servo power supply.**

## Controlling a Servo with ESP32

**Using the Arduino `ESP32Servo` library:**

```cpp
#include <ESP32Servo.h>

Servo myServo;
const int servoPin = 13;

void setup() {
  myServo.attach(servoPin);
}

void loop() {
  myServo.write(0);    // 0°
  delay(1000);
  myServo.write(90);   // 90°
  delay(1000);
  myServo.write(180);  // 180°
  delay(1000);
}
```

**Using PWM directly (if you want to understand it):**

```cpp
const int servoPin = 13;

void setup() {
  ledcSetup(0, 50, 16);        // 50Hz PWM, 16-bit resolution
  ledcAttachPin(servoPin, 0);
}

void setServo(int angle) {
  int duty = map(angle, 0, 180, 1638, 8192); // 0°=1ms, 180°=2ms at 50Hz
  ledcWrite(0, duty);
}

void loop() {
  setServo(90);
  delay(1000);
}
```

## The PWM Signal (for understanding)

Servos expect a **50Hz PWM signal** (period = 20ms):

```
    20ms total ──────────────────────┐
                                     │
  0°  → 1ms pulse  ┌─┐              │
                    │ │              │
                    └─┘              │
                                     │
 90°  → 1.5ms pulse ┌──┐            │
                     │  │            │
                     └──┘            │
                                     │
180°  → 2ms pulse   ┌───┐           │
                     │   │           │
                     └───┘           │
                                     │
```

| Angle | Pulse width | Duty cycle (at 50Hz) |
|-------|-------------|---------------------|
| 0° | 1.0ms | 5% |
| 90° | 1.5ms | 7.5% |
| 180° | 2.0ms | 10% |

## Continuous Rotation Servos

Some servos are modified for continuous rotation (like a regular motor but with speed control):

```
write(0)    → full speed clockwise
write(90)   → stopped
write(180)  → full speed counter-clockwise
```

> **Check your servo's type before wiring.** A continuous-rotation servo does not hold position — it just spins at a speed.

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| External power for >1 servo | ESP32 browns out / resets when servos draw current |
| Shared GND (ESP32 + servo supply) | Servo twitches randomly, doesn't respond |
| Using non-PWM GPIO pin | Servo ignores signal — won't move |
| Wrong PWM frequency (not 50Hz) | Servo buzzes, jitters, or doesn't hold position |
| Stalling servo (blocking it) | High current draw, possible ESC/transistor damage |
| Powering servo through breadboard long traces | Voltage drop causes erratic behavior — use proper wires |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| SG90 micro servo (9g) | 1 | Cheap, standard, starts here |
| MG90S metal gear servo | 1 | Metal gears — won't strip as easily |
| MG996R standard servo | 1 | Bigger, stronger, needs external power |
| 5V 2A power supply | 1 | For powering servos separately |
| Female-to-female jumper wires | 3 per servo | Servo has female pins |

> **If your servo jitters:** Add a 100–470µF capacitor across the servo power pins (close to the servo). This smooths out the current spikes.
