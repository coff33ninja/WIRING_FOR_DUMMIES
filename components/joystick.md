# Joystick Module — Component Reference

## What It Is

A joystick module (like the KY-023 or generic PS2-style) contains **two potentiometers** (X and Y axis) and a **push button** (Z axis). It's the same mechanism inside PlayStation and Xbox controllers — just broken out for breadboard use.

```
          /\
         /  \
        /    \
       /      \
      /   ●    \  ← Stick (moves X and Y)
     /          \
    /    ┌──┐    \
   /     │  │     \
  /      │  │      \
 /       │  │       \
/        └──┘        \
└─────────────────────┘
  GND +5V VRx VRy SW   ← Pins
```

## Pinout

```
Standard joystick module:
  GND ── Ground
  +5V ── VCC (3.3V also works on most modules)
  VRx ── Analog X output
  VRy ── Analog Y output
  SW  ── Digital switch (active LOW, pressed = LOW)
```

## Wiring

```
Joystick             Microcontroller
  GND ──────────────── GND
  +5V ──────────────── 3.3V or 5V
  VRx ──────────────── ADC pin (analog input)
  VRy ──────────────── ADC pin (analog input)
  SW  ──────────────── GPIO (digital input with pull-up)
```

**VRx/VRy:** Connect to analog input pins (ADC). On ESP32, these are GPIO 32–39 (ADC1).
**SW:** Connect to a digital input with pull-up enabled. The module's internal switch pulls LOW when pressed.

## How It Works

### Potentiometers (X and Y)

Each axis is a **10kΩ potentiometer** connected between VCC and GND. The wiper voltage changes as you move the stick:

```
Position       VRx voltage    X-axis value (10-bit)
Center         2.5V (at 5V)   ~512
Full left      0V             0
Full right     5V             1023
Full up        0V (Ry high)   0
Full down      5V (Ry low)    1023
```

**The center position** never reads exactly 512 (midpoint). There's a tolerance zone of ~100 counts around center where the value fluctuates. Add a deadzone in software:

```cpp
int x = analogRead(VRX_PIN);
if (abs(x - 512) < 50) x = 512;  // ignore noise near center
```

### Switch (Z Axis)

The switch is a **momentary push button** that connects SW to GND when pressed. It's active LOW — reads LOW when pressed, HIGH when not.

Don't forget to enable the internal pull-up:

```cpp
pinMode(SW_PIN, INPUT_PULLUP);
```

## Reading the Joystick

```cpp
const int VRX = 34;
const int VRY = 35;
const int SW = 32;

void setup() {
  Serial.begin(115200);
  pinMode(SW, INPUT_PULLUP);
}

void loop() {
  int x = analogRead(VRX);
  int y = analogRead(VRY);
  bool pressed = !digitalRead(SW);  // invert: true when pressed

  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.println(pressed);

  delay(50);
}
```

## Thumbstick vs Full-Size Joystick

| Type | X/Y range | Spring return | Best for |
|------|-----------|---------------|----------|
| Thumbstick (KY-023) | ~10mm travel | Self-centers | Game controllers, menu navigation |
| Full-size joystick | ~30mm travel | Self-centers (some) | Robot control, CNC jogging |
| Slide potentiometer | Linear | Usually no spring | Mixers, faders, position sensors |

Both use the same wiring. The difference is physical size and feel.

## Adding a Deadzone

Analog joysticks don't return to exactly center. Add a deadzone to prevent drift:

```cpp
int applyDeadzone(int value, int center, int deadzone) {
  if (abs(value - center) < deadzone) return center;
  return value;
}

void loop() {
  int x = applyDeadzone(analogRead(VRX), 512, 60);
  int y = applyDeadzone(analogRead(VRY), 512, 60);
  // use x, y with deadzone applied
}
```

## Using with Digital Movement (D-Pad Emulation)

Convert the analog range to 4-directional digital:

```cpp
int x = analogRead(VRX);
int y = analogRead(VRY);

if (x < 300)      direction = "LEFT";
else if (x > 700) direction = "RIGHT";
else if (y < 300) direction = "UP";
else if (y > 700) direction = "DOWN";
else              direction = "CENTER";
```

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Readings jump around | Noisy power supply or no capacitor | Add 100nF cap between VCC and GND on module |
| Won't reach 0 or 1023 | Mechanical limit, or ADC range | It's normal — use software mapping |
| Center value drifts | Temperature change, or wear | Increase deadzone, or auto-calibrate at startup |
| Button not detected | Missing pull-up | Enable INPUT_PULLUP on the SW pin |
| Same reading on X and Y | VRx and VRy swapped | Swap the pins in code |
| No change in readings | Module not getting power | Check VCC and GND connections |

## Quick Reference

- **X axis:** VRx (analog, 0–VCC)
- **Y axis:** VRy (analog, 0–VCC)
- **Z axis:** SW (digital, active LOW)
- **Center voltage:** ~VCC/2 (but not exact — add deadzone of ±50 counts)
- **Power:** 3.3V or 5V (works with both)
- **Self-centering:** Springs return to center when released
- **Calibration:** Read center at startup and use it as the reference
- **Deadzone:** Ignore values within ~50 counts of center to prevent drift
- **Pull-up needed:** Enable INPUT_PULLUP for the switch pin
