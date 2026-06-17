# Stepper Motor — Component Reference

## What It Is

A stepper motor turns in discrete steps — each electrical pulse advances the rotor a fixed angle. No feedback needed (open-loop position control). Unlike a DC motor, you know exactly where the shaft is without an encoder.

> **Analogy:** A clock's second hand. Each tick moves exactly 1/60 of a rotation. Give it the right number of ticks and it lands precisely where you aimed.

## Motor Construction Types

### Permanent Magnet (PM)

Rotor is a permanent magnet. Stator windings are energized to attract/repel the rotor.

| Pros | Cons |
|---|---|
| Good torque at low speed | Lower top speed |
| Simple construction | Moderate holding torque |
| Low cost | |
| Low vibration (compared to VR) | |

**Use for:** Hobby projects, 3D printers (older designs), small positioning tasks.

### Variable Reluctance (VR)

Rotor is soft iron (not magnetized). Stator poles pull the rotor teeth into alignment.

| Pros | Cons |
|---|---|
| Very high step resolution | Low torque |
| Simple rotor (no magnet) | No holding torque when unpowered |
| High speed possible | Rarely seen in modern hobby kits |

**Use for:** High-speed positioning where torque is not critical.

### Hybrid (HB) — Most Common

Combines PM rotor with VR-style toothed poles. The rotor has a permanent magnet with two tooth-cups offset by half a tooth pitch.

| Pros | Cons |
|---|---|
| High torque | More expensive than PM |
| Small step angles (0.9°–1.8°) | Needs a proper driver |
| Good holding torque | |
| Smooth operation with microstepping | |

**Use for:** NEMA 17, NEMA 23 — the standard for 3D printers, CNC, robotics.

## Unipolar vs Bipolar — The Wiring Difference

This is the most important wiring decision. It determines what driver you need.

### Unipolar

Two coils, each with a center tap. 5 or 6 wires.

```


        ┌──[coil A]──┐
   A+ ──┤            ├── COM (center tap)
        └──[coil A]──┘

        ┌──[coil B]──┐
   B+ ──┤            ├── COM
        └──[coil B]──┘
```

You only energize half of each coil at a time. Easier to drive (simple transistors), but less torque per winding since only half the copper is used.

**Wire count:** 5 or 6 wires. Common center tap can be shared or separate.

| Wire colors (typical) | Function |
|---|---|
| Red / Blue | Coil A ends |
| Yellow / White (or Black) | Coil B ends |
| Black / Orange | Center taps (common) |

### Bipolar

Two coils, no center tap. 4 wires.

```


        ┌──[coil A]──┐
   A+ ──┤            ├── A-
        └────────────┘

        ┌──[coil B]──┐
   B+ ──┤            ├── B-
        └────────────┘
```

Current flows through the full coil. Requires an H-bridge driver (like A4988) to reverse polarity. Delivers more torque than unipolar for the same motor — the entire copper winding is used.

**Wire count:** 4 wires.

| Wire colors (typical) | Function |
|---|---|
| Black / Green | Coil A |
| Red / Blue | Coil B |

> **Identifying unipolar vs bipolar:** Count wires. 4 wires = bipolar. 5 or 6 = unipolar. Use a multimeter — measure resistance between wires. If two wires show continuity to multiple others, those are center taps.

### Converting Unipolar to Bipolar

Ignore the center taps (leave them unconnected). Use only the four end wires. You get a bipolar motor — slightly less inductance, same torque. Works with any bipolar driver.

## Step Angle

The angle the shaft rotates per full step.

| Step angle | Steps per revolution | Common in |
|---|---|---|
| 7.5° | 48 | Old PM motors, 28BYJ-48 |
| 1.8° | 200 | NEMA 17, most hybrid motors |
| 0.9° | 400 | High-resolution hybrid motors |

**Number of steps = 360° / step angle.**

**Accuracy:** Stepper motors are typically accurate to ±5% of a step (non-cumulative — error does not stack across steps).

## Holding Torque

Torque the motor exerts when stationary and energized (one or more coils powered).

Measured in N·cm or kg·cm.

| Motor size | Typical holding torque |
|---|---|
| 28BYJ-48 (tiny) | ~0.03 N·m |
| NEMA 14 | ~0.1–0.2 N·m |
| NEMA 17 | ~0.3–0.5 N·m |
| NEMA 23 | ~1.0–2.0 N·m |

**Holding torque ≠ running torque.** Running torque drops as speed increases (inductive reactance limits current).

## Why You Need a Driver (Not Direct GPIO)

You cannot connect a stepper motor directly to a microcontroller GPIO pin. Here's why:

| Reason | Explanation |
|---|---|
| Current | Stepper coils draw 0.3–2A+; GPIO max is ~20mA |
| Voltage | Motors run at 3–24V+; GPIO is 3.3V or 5V |
| Polarity | Bipolar needs bidirectional current — GPIO can only source/sink one direction |
| Timing | Stepping needs precise microsecond timing that software alone struggles with |

**A driver handles all of this.** Your microcontroller sends step/direction pulses (low-current logic signals). The driver handles the high-current switching.

## Common Drivers

### A4988

The hobby standard. Cheap, widely available, on breakout boards with pin headers.

| | A4988 |
|---|---|
| Max voltage | 8–35V |
| Max current per coil | ±2A (with heat sink) |
| Microstep resolution | 1/1, 1/2, 1/4, 1/8, 1/16 |
| Logic voltage | 3.3V / 5V |
| Package | Breakout with heat sink |

**Pins:** STEP, DIR, ENABLE, MS1/MS2/MS3 (microstep select), SLEEP, RESET.

**Current limit:** Adjust the tiny potentiometer on the board. Measure voltage at the REF pin — VREF = current_limit × 8 × sense_resistor. For a typical 0.1Ω sense resistor: VREF = current × 0.8.

**Typical NEMA 17 setting:** VREF ≈ 0.8–1.0V (≈1.0–1.25A).

### DRV8825

Drop-in upgrade for A4988. Higher voltage and current, better microstepping.

| | DRV8825 |
|---|---|
| Max voltage | 8.2–45V |
| Max current per coil | ±2.5A (with heat sink) |
| Microstep resolution | 1/1, 1/2, 1/4, 1/8, 1/16, 1/32 |
| Logic voltage | 3.3V / 5V |

**Pin-compatible** with A4988 boards? Mostly — check your breakout. The DRV8825 has different MS pin mapping for microstepping.

### ULN2003

Used with the tiny 28BYJ-48 5V unipolar motor. Comes as a bargain driver board with LEDs on each output (useful for debugging).

| | ULN2003 |
|---|---|
| Max voltage | 50V |
| Max current per channel | 500mA |
| Microstepping | **No** — full steps only |
| Type | Darlington transistor array (on/off, no PWM) |

| Pros | Cons |
|---|---|
| Costs pennies | No microstepping |
| Works with 28BYJ-48 | Very noisy motor |
| LEDs show step sequence | Low torque |
| 5V logic compatible | Runs hot |

**Use ULN2003 for:** The 28BYJ-48 and nothing else. For any NEMA motor, get an A4988 or DRV8825.

## Microstepping

Divides each full step into smaller fractions. The driver sends sine/cosine currents to both coils, positioning the rotor between steps.

| Setting | Steps per rev (1.8° motor) |
|---|---|
| Full step | 200 |
| 1/2 step | 400 |
| 1/4 step | 800 |
| 1/8 step | 1600 |
| 1/16 step | 3200 |
| 1/32 step (DRV8825) | 6400 |

**Trade-offs:**

| Advantage | Disadvantage |
|---|---|
| Smoother motion | Lower holding torque per microstep |
| Less vibration | More steps to move the same distance = lower max speed |
| Finer positioning | Positional accuracy is not improved (still ±5% of a full step) |
| Quieter operation | |

**Rule of thumb:** Use 1/16 microstepping for 3D printers. Use 1/4 or 1/8 for CNC where torque matters more. Use full step when speed is critical and vibration is acceptable.

## Current Limiting

The driver limits current to protect the motor. Set the current limit below the motor's rated current.

**Procedure (A4988):**

1. Power the driver with motor voltage (do not connect motor yet)
2. Measure voltage between REF pin and GND
3. VREF = current_limit × 2.5 (A4988 with 0.05Ω sense resistor)
4. Adjust potentiometer until VREF matches

**Typical values:**

| Motor | Rated current | VREF (A4988, 0.05Ω R_sense) |
|---|---|---|
| 28BYJ-48 | ~200mA | 0.5V |
| NEMA 17 (0.4A) | 0.4A | 1.0V |
| NEMA 17 (1.0A) | 1.0A | 2.5V |
| NEMA 17 (1.7A) | 1.7A | 4.25V (needs heat sink + fan) |

**If the motor gets hot (>60°C) within 30 seconds, your current limit is too high.**

## Power Supply Capacitance

Stepper drivers draw current in sharp pulses. A bulk capacitor at the driver power input is mandatory.

| Motor | Minimum capacitor |
|---|---|
| 28BYJ-48 | 47µF |
| Single NEMA 17 | 100–470µF |
| Two NEMA 17 | 470–1000µF |
| NEMA 23 | 1000–2200µF |

**Voltage rating:** At least 1.5× the supply voltage. Use 25V or 35V caps for 12V supplies, 50V for 24V.

**Place the capacitor as close to the driver's power pins as possible.** Without it, voltage dips on each step cause erratic behavior and resets.

## Quick Reference

```
Type choices:
  PM — cheap, moderate torque, loud
  VR — fast, low torque, rare
  Hybrid — best all-round (NEMA 17)

Wiring:
  Unipolar (5-6 wires) — center taps, lower torque, ULN2003 driver
  Bipolar (4 wires) — full coil, higher torque, A4988/DRV8825 driver

Driver guide:
  28BYJ-48 → ULN2003
  NEMA 17 → A4988 (1A) or DRV8825 (1.5A+)
  NEMA 23 → DRV8825 or TMC2209

Microstepping guide:
  1/1 full: fast, loud, high torque   → CNC rough moves
  1/4: smooth enough                   → most things
  1/16: very smooth, quiet             → 3D printers
  1/32: extremely smooth, less torque  → quiet printers

Power cap formula: 100–470µF per motor at 12V.
```
