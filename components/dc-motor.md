# DC Motor (Brushed) — Speed & Direction Control

## What It Is

A brushed DC motor spins when you apply voltage. Reverse the voltage and it spins the other way. More voltage = faster. More current = more torque.

> **Analogy:** A DC motor is like a water wheel. Give it water flowing one way (voltage), and it spins. Give it water flowing the other way, and it spins in reverse. More water pressure (voltage) → faster. More water volume (current) → more force.

## Motor Anatomy

```
  ┌─────────────────────┐
  │   ┌───────────┐    │
  │   │  ═══ ═══  │    │  ← Magnets (stator)
  │   │ ═══════   │    │
  │   │  ═══ ═══  │    │
  │   └───────────┘    │
  │    ↑              │
  │  Brushes (contact)│
  └─────────────────────┘
       │          │
     Terminal+  Terminal−
```

Inside: A rotor (armature) with wire coils spins between magnets. Brushes (carbon blocks) press against the commutator to deliver power to the spinning coils.

## Key Specs

| Spec | What it means | Example (small hobby motor) |
|------|---------------|----------------------------|
| **Rated voltage** | Normal operating voltage | 3V, 6V, 12V |
| **No-load current** | Current with nothing attached | ~70mA |
| **Stall current** | Current when shaft is held still (max) | ~1.5A — this is the peak your driver must handle |
| **No-load speed** | RPM with no load | 5000–12000 RPM |
| **Stall torque** | Maximum torque (at 0 RPM) | Expressed in g·cm or N·m |
| **Starting voltage** | Minimum voltage to start moving | ~0.5–1V |

> **The stall current is what matters for your motor driver.** The motor draws stall current on startup and when stalled. If your driver can't handle stall current, it will overheat or the motor will stop.

## Brushed vs Brushless

| | Brushed (this guide) | Brushless (BLDC) |
|--|---------------------|------------------|
| Cost | Cheap | More expensive |
| Control | Simple — just apply voltage | Needs ESC (Electronic Speed Controller) |
| Efficiency | Lower (brushes waste power) | Higher |
| Lifespan | Limited (brushes wear out) | Longer (no brushes) |
| Noise | Electrical noise (sparks at brushes) | Quieter |
| Hobby use | Small robots, fans, toys | Drones, RC cars, e-bikes |

**For most beginner projects:** Use brushed DC motors. They're cheap, simple to control, and easy to replace.

## Controlling a DC Motor

### 1. On/Off Control (with a MOSFET)

A motor needs more current than a GPIO pin can provide. Use a **MOSFET** as a switch:

```
For a small 3–6V motor (<500mA stall):

  12V (or motor voltage)
    │
  Motor
    │
  Drain ── IRF520 / IRLZ44N (N-channel MOSFET)
  Gate ─── GPIO (through 10kΩ pull-down)
  Source ── GND

  Flyback diode (1N4007) across motor:
    Stripe (cathode) → + side of motor
    Plain (anode)    → drain of MOSFET
```

> **The flyback diode is NOT optional.** When you turn off the MOSFET, the motor's inductance generates a voltage spike that WILL kill the MOSFET. The 1N4007 gives the spike a safe path.

### 2. Speed Control (PWM + MOSFET)

Same circuit as above, but drive the gate with **PWM** instead of a steady HIGH/LOW:

```cpp
ledcAttachPin(GATE_PIN, 0);     // MOSFET gate on this pin
ledcSetup(0, 5000, 8);          // 5kHz PWM, 8-bit
ledcWrite(0, 128);              // 50% duty = half speed
```

**PWM frequency for motors:**
| Frequency | Effect |
|-----------|--------|
| <1kHz | Audible whine — annoying |
| **5–10kHz** | **Good balance — quiet enough, efficient** |
| 20–40kHz | Silent (above hearing range) — less efficient |
| >40kHz | Driver losses increase — not worth it |

### 3. Direction + Speed (H-Bridge — L298N / L293D)

To control **both direction and speed**, you need an H-bridge — an IC with 4 switches arranged in an H shape:

```
  Motor + ───┬─── Switch1 ──── VCC
             │
             └─── Switch3 ──── GND

  Motor − ───┬─── Switch2 ──── VCC
             │
             └─── Switch4 ──── GND

  Forward: Switch1 + Switch4 ON
  Reverse: Switch2 + Switch3 ON
  Brake:   Switch1 + Switch2 ON (or Switch3 + Switch4)
  Coast:   All OFF
```

Common H-bridge ICs:

| IC | Voltage | Max current per channel | Use |
|----|---------|------------------------|-----|
| **L293D** | 4.5–36V | **600mA** | Small hobby motors, individual control |
| **L298N** | 5–35V | **2A** | Medium motors, sensor modules with onboard regulator |
| **TB6612FNG** | 2.5–13.5V | **1.2A** | Compact, low voltage drop, efficient |
| **DRV8833** | 2.7–10.8V | **1.5A** | Small robots, low voltage |

### Wiring L298N Module

```
L298N Module:

  +12V ──── 12V power (motor power)
  GND ───── GND (common with ESP32 GND)
  +5V ───── Output 5V (or input if jumper removed)
  
  ENA ───── GPIO (PWM-capable) — enable/analog speed control for Motor A
  IN1 ───── GPIO  — direction control for Motor A
  IN2 ───── GPIO  — direction control for Motor A
  
  ENB ───── GPIO (PWM-capable) — enable/speed control for Motor B
  IN3 ───── GPIO  — direction control for Motor B
  IN4 ───── GPIO  — direction control for Motor B
  
  OUT1/2 ── Motor A terminals
  OUT3/4 ── Motor B terminals
```

**Control truth table (Motor A):**

| ENA | IN1 | IN2 | Motor A behavior |
|-----|-----|-----|-----------------|
| LOW | X | X | OFF / coast |
| HIGH | LOW | LOW | Brake |
| HIGH | LOW | HIGH | Forward |
| HIGH | HIGH | LOW | Reverse |
| HIGH | HIGH | HIGH | Brake |

### Example (L298N + ESP32)

```cpp
#define ENA 13
#define IN1 12
#define IN2 14

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  ledcAttachPin(ENA, 0);
  ledcSetup(0, 5000, 8);
}

void forward(int speed) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  ledcWrite(0, speed);  // 0–255
}

void reverse(int speed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  ledcWrite(0, speed);
}

void brake() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, HIGH);
  ledcWrite(0, 255);
}

void coast() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  ledcWrite(0, 0);
}

void loop() {
  forward(200);   // Forward, ~78% speed
  delay(3000);
  brake();
  delay(1000);
  reverse(150);   // Reverse, ~58% speed
  delay(3000);
  coast();
  delay(2000);
}
```

## Power Supply Considerations

| Mistake | Result |
|---------|--------|
| Powering motor and ESP32 from same regulator | Voltage dips when motor starts → ESP32 resets |
| Powering motor from ESP32's 3.3V pin | Too little current — motor doesn't spin, ESP32 may brown out |
| Using thin wires for motor power | Wires heat up, voltage drops, motor runs slow |
| No capacitor on motor terminals | Electrical noise interferes with sensor readings |

**Rule: Separate power rails for motors and electronics:**

```
Battery (7.2V) ──┬── L298N motor driver ── Motor
                 │                   ┌──── ESP32 (via 5V regulator)
                 └───────────────────┘
```

The ESP32 and motor should share **only a common GND**, not the power rail.

### Decoupling Capacitors

Place a **100µF electrolytic + 100nF ceramic** capacitor across the motor terminals to suppress electrical noise. The capacitor absorbs the spikes from the brushes.

```
Motor + ──┬─────── L298N OUT
          │
        [100µF 25V]  [100nF]
          │
Motor − ──┴─────── L298N OUT
```

## What Happens If Something Goes Wrong

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Motor doesn't move | No power to motor driver | Check motor power supply |
| Motor doesn't move | ENA pin not HIGH | Set ENA HIGH or send PWM |
| Motor twitches but doesn't spin | Not enough current | Power supply too weak |
| ESP32 resets when motor starts | Voltage drop on shared supply | Use separate power supply |
| Motor only goes one direction | IN1/IN2 both LOW or both HIGH | Check truth table |
| Motor runs but no speed control | ENA not connected to PWM pin | Move ENA to a PWM-capable GPIO |
| MOSFET gets hot | Gate not fully driven (≥10V for standard MOSFET) | Use logic-level MOSFET (IRLZ44N) |
| Motor spins slowly with no load | Long thin wires causing voltage drop | Use thicker wires (18–20 AWG) |
| Sensor readings jump when motor runs | Electrical noise from motor brushes | Add decoupling caps across motor |

## Quick Reference

```
Brushed DC motor basics:
  Voltage → speed
  Current → torque
  Reverse voltage → reverse direction
  Stall current = max current = driver must handle this

Control methods:
  On/Off:       N-channel MOSFET + flyback diode
  Speed:        MOSFET + PWM (5–10kHz typical)
  Direction:    H-bridge (L298N, L293D, TB6612, DRV8833)

Power rules:
  Separate supply for motor and MCU (common GND only)
  Decoupling caps on motor: 100µF + 100nF
  Flyback diode across motor (required!)

L298N wiring:
  ENA/ENB → PWM GPIO (speed control)
  IN1/IN2 → direction (HIGH/LOW = forward, LOW/HIGH = reverse)
  OUT1/OUT2 → motor terminals
  Motor power → L298N 12V input (not ESP32 power)

If nothing moves:
  1. Check motor power supply voltage
  2. Check ENA is HIGH (or receiving PWM)
  3. Check IN1/IN2 are correct (not both LOW or both HIGH)
  4. Check common GND between ESP32 and motor driver
```
