# Solenoid — Component Reference

> **See also:** [Relay](relay.md) — both are inductive loads that need flyback diodes.

## What It Is

A solenoid is an electromechanical device that converts electrical current into **linear motion**. When current flows, a magnetic field pushes or pulls a metal plunger (the moving rod) inside the coil. When current stops, a spring returns the plunger to its resting position.

```
   ┌─────────────────────┐
   │  ═══════════════    │
   │  ║  Coil windings   │
──┤  ║                   ├──  ← Plunger (pulls in when energized)
   │  ║                   │
   │  ═══════════════    │
   ├─────────────────────┤
   │    ┌─────┐          │
   │    │Spring│         │  ← Return spring
   │    └─────┘          │
   └─────────────────────┘
        │        │
       VCC      GND
```

Common uses: door locks, pinball flippers, vending machine dispensers, valves (water/gas), car door latches, industrial automation.

## How It Works

1. Apply DC voltage across the coil.
2. Current flows, creating a magnetic field.
3. The magnetic field pulls the metal plunger into the coil center (solenoid "engages").
4. While energized, the plunger holds position.
5. Cut power, the spring pushes the plunger back (solenoid "releases").

### Pull vs Push Solenoids

| Type | Plunger rests | When energized |
|------|--------------|----------------|
| Pull | Extended OUT | Pulls IN |
| Push | Retracted IN | Pushes OUT |
| Pull-Push | Extended OUT | Can pull or push (two coils or mechanical linkage) |

Most solenoids are **pull-type** — they pull inward when powered.

## Key Specifications

| Spec | Typical Range | What It Means |
|------|---------------|---------------|
| Voltage | 3V, 5V, 6V, 12V, 24V | Operating voltage |
| Current | 0.3A – 3A | How much the coil draws |
| Resistance | 5Ω – 100Ω | Coil DC resistance (V = I × R) |
| Stroke | 5mm – 50mm | How far the plunger moves |
| Force | 0.5N – 50N | How hard it pulls |
| Duty cycle | 10% – 100% | Max on-time before overheating |
| Response time | 10ms – 100ms | How fast it engages |

### Understanding Duty Cycle

**This is critical.** Many solenoids are NOT designed for continuous operation.

| Duty Cycle | Max On Time | Min Off Time | Use |
|------------|-------------|--------------|-----|
| 10% | 1 second | 9 seconds | Brief pulses (door lock) |
| 25% | 2.5 seconds | 7.5 seconds | Intermittent (pinball flipper) |
| 50% | 5 seconds | 5 seconds | Moderate |
| 100% | Continuous | N/A | Continuous (latching valve) |

If you exceed the duty cycle, the coil overheats, insulation melts, and the solenoid is destroyed. **Always check the datasheet duty cycle.** If you're running a solenoid continuously, use a latching solenoid instead.

## Wiring — Driver Circuit (Required)

**NEVER connect a solenoid directly to a microcontroller pin.** Solenoids draw 0.3–3A, far beyond what a GPIO can supply. You need a driver circuit.

### Basic Driver — N-Channel MOSFET

```
12V supply ── fuse ── solenoid (+) ── solenoid (-) ──┬── D (IRLZ44N)
                                                      │
                                                      3.3V/5V PWM ── R (10kΩ) ── G
                                                      │
                                                     S ── GND
                                                    │
                                                    10kΩ ── GND (pull-down)
```

The MOSFET switches ground to the solenoid. When the gate goes HIGH, the MOSFET conducts and the solenoid energizes. The 10kΩ pull-down keeps the MOSFET off during boot.

### With Flyback Diode — ABSOLUTELY REQUIRED

A solenoid is an **inductive load**. When you turn off the MOSFET, the magnetic field collapses and generates a voltage spike in the opposite direction — hundreds of volts that will destroy your MOSFET.

```
12V ── solenoid ──┬── MOSFET drain
                   │
                   1N4007 (flyback diode)
                   cathode to 12V, anode to drain
```

**Always put a flyback diode across the solenoid** — cathode to the positive side, anode to the drain (or negative side of solenoid). This gives the inductive spike a safe path to circulate and collapse.

### Using a Relay Module as Driver

You can also drive a solenoid from a relay module (the relay contacts switch the high current):

```
Microcontroller ── relay module IN ── relay COM ── 12V supply
                                        relay NO ── solenoid (+)
                                        solenoid (-) ── GND
```

This works but is bulkier and slower than a MOSFET. Use a MOSFET for faster switching (PWM) and lower power consumption.

## Latching Solenoids

A latching solenoid uses a **permanent magnet** inside so it holds position without power. You apply a pulse to change state (extend or retract), then cut power — it stays in that position.

- **Zero power consumption** when holding
- **Needs a bipolar driver** (H-bridge) because you reverse voltage to change direction
- **Typical pulse:** 20–100ms at rated voltage
- Used in: smart locks, water valves, automotive actuators

### Latching Solenoid Driver (H-Bridge)

Use a DRV8833 or L298N module with two GPIOs:

```
GPIO 1 ── IN1 (forward: extend)
GPIO 2 ── IN2 (reverse: retract)
H-bridge output ── solenoid
```

## Solenoid vs Linear Actuator

| | Solenoid | Linear Actuator |
|--|----------|----------------|
| Motion | Binary (in or out) | Any position (controllable) |
| Stroke | Short (5–50mm) | Long (10–1000mm) |
| Force | High for size | Lower for size |
| Control | On/off only | PWM or feedback position |
| Hold | Needs power (or latching type) | Can hold position (screw drive) |
| Price | Cheap ($2–$10) | Expensive ($20–$100) |

**Use a solenoid** for: quick push/pull actions, locking, releasing, striking.

**Use a linear actuator** for: precise positioning, lifting, pushing to variable positions.

## Using Solenoids with PWM

You can PWM a solenoid to control force (but NOT position — it's either in or out). Useful for:

- **Reducing heat** — run at full voltage to engage, then reduce to 50% PWM to hold with less heating
- **Soft engagement** — ramp PWM up over 20ms to reduce mechanical shock

Code (Arduino):

```c
const int solenoidPin = 9; // PWM-capable pin
const int engageDuration = 500; // ms

void engageSolenoid() {
  // Ramp up over 50ms
  for (int i = 0; i < 255; i += 10) {
    analogWrite(solenoidPin, i);
    delay(2);
  }
  delay(engageDuration);
  analogWrite(solenoidPin, 0); // Release
}
```

**PWM only works with a MOSFET driver** (not a relay). The MOSFET switches fast enough to follow the PWM signal.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Solenoid doesn't move | Not enough current | Check supply voltage, wire gauge, MOSFET gate voltage |
| Solenoid gets hot quickly | Duty cycle too high | Reduce on-time, add heatsink, use lower duty cycle |
| MOSFET gets hot | Gate not driven to full voltage | Use logic-level MOSFET, increase gate drive voltage |
| Microcontroller resets when solenoid engages | Voltage drop on supply | Add 1000µF capacitor near solenoid driver |
| Solenoid chatters | PWM frequency too low | Increase PWM frequency above 100 Hz |
| Plunger stuck | Mechanical obstruction, rust | Lubricate, check alignment |

## Quick Reference

- **Solenoid** = linear motion from magnetic coil, binary (in/out)
- **Flyback diode** — ALWAYS required (1N4007 or similar) across the coil
- **Driver needed** — MOSFET or relay, NOT direct from GPIO
- **Duty cycle matters** — exceeding it destroys the solenoid
- **For continuous hold:** Use latching solenoid, mechanical latch, or PWM reduction
- **Typical voltage:** 12V is most common for hobby solenoids
- **Typical current:** 0.5–2A (use 20AWG or thicker wire)
- **Response time:** ~20–50ms for small solenoids
- **Push vs pull:** Check before buying — most are pull-type
