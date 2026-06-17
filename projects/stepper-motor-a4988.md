# Stepper Motor + A4988 Driver — Wiring for Dummies

## What Is a Stepper Motor?

A stepper motor is a motor that moves in **precise, fixed steps** rather than spinning freely. Instead of "turn on" and "go," it moves in fractions of a rotation — think of it like the second hand on a clock, ticking from one position to the next.

> **Analogy:** A regular DC motor is like spinning a coin on a table — you know it's moving but not how far. A stepper motor is like a record player's tonearm — you can say "move 47 steps to the right" and it lands exactly there every time.

**Use for:** 3D printers, CNC machines, robot arms, camera pan/tilt, anything needing precise position control.

## A4988 Driver — What It Does

The A4988 is a **stepper motor driver** — it takes simple signals from the microcontroller and converts them into the precise sequence of coil energizations that make the stepper move.

> **Why you need a driver:** A stepper motor draws way more current than an ESP32 can provide (hundreds of mA per coil). The A4988 handles the high current and just needs the ESP32 to send "step once" pulses.

## A4988 Pinout

```
              A4988 (looking from top)
          ┌─────────────────────────┐
          │                         │
   (1) ENABLE ────────────────── VDD (16)
   (2) MS1    ────────────────── VREG (15)  (don't connect)
   (3) MS2    ────────────────── GND (14)
   (4) MS3    ────────────────── 2B  (13) → Motor coil B
   (5) RESET  ────────────────── 2A  (12) → Motor coil B
   (6) SLEEP  ────────────────── 1A  (11) → Motor coil A
   (7) STEP   ────────────────── 1B  (10) → Motor coil A
   (8) DIR    ────────────────── VDD (9)
          └─────────────────────────┘
```

### Control Pins (ESP32 side)

| Pin | Name | Think of it as... |
|-----|------|-------------------|
| STEP | Step | **"Take one step" button.** Each HIGH pulse = one step |
| DIR | Direction | **"Which way to go."** HIGH = one direction, LOW = reverse |
| ENABLE | Enable | **"Motor on/off."** LOW = motor holds position, HIGH = free spin (coils off) |
| MS1, MS2, MS3 | Microstep select | Step resolution (see below) |
| RESET | Reset | Pull HIGH for normal operation. Pull LOW to reset internal state |
| SLEEP | Sleep | Pull HIGH for normal operation. Pull LOW to save power (coils off) |

### Power Pins (Motor side)

| Pin | Name | Connects to |
|-----|------|-------------|
| VMOT | Motor power | 8–35V supply (select voltage based on motor rating) |
| GND | Ground | Power supply ground |
| 1A, 1B | Coil A | One coil of the stepper motor |
| 2A, 2B | Coil B | The other coil of the stepper motor |

### Power Pins (Logic side)

| Pin | Connects to |
|-----|-------------|
| VDD | 3.3V or 5V (matches your microcontroller logic) |
| GND | Ground (tied to ESP32 GND) |

**WARNING:** The two ground pins (GND on logic side and GND on motor side) must be connected together. They're separate on the chip but must share the same ground reference.

## Wiring Diagram

```
ESP32                 A4988
────                  ─────
3.3V ────────────────── VDD
GND  ────────────────── GND (logic)
GPIO 16 ─────────────── STEP
GPIO 17 ─────────────── DIR
GPIO 4  ─────────────── MS1
GPIO 5  ─────────────── MS2
GPIO 18 ─────────────── MS3
GPIO 15 ─────────────── ENABLE (LOW = enabled)
3.3V ────────────────── RESET (pull HIGH)
3.3V ────────────────── SLEEP (pull HIGH)

Power Supply           A4988
12V ──────────────────── VMOT
GND  ─────────────────── GND (motor side)
                         │
                     ┌───┴───┐
                     │       │
                   100µF  470µF
                  25V     25V
                   cap     cap
                     │       │
                     └───┬───┘
                         │
                        GND

Stepper Motor          A4988
Coil A+ ──────────────── 1A
Coil A− ──────────────── 1B
Coil B+ ──────────────── 2A
Coil B− ──────────────── 2B

CRITICAL: Power supply GND ───── ESP32 GND (tie them together)
```

## The Power Capacitor — NOT OPTIONAL

The A4988 datasheet is very specific: **you need a 47–100µF electrolytic capacitor** across VMOT and GND. Without it, sudden current draw from the motor causes voltage dips that can:

1. Make the A4988 miss steps (motor loses position)
2. Reset the chip mid-motion
3. Generate voltage spikes that damage the driver

> **What happens if you skip it:** The motor might work on the bench but fail under load. The A4988 gets hot, skips steps, or behaves erratically. 100µF minimum, 470µF is better.

## Microstepping — Smooth vs Strong

Stepper motors have a built-in **step angle**, usually 1.8° (200 steps per revolution) or 0.9° (400 steps per revolution).

Microstepping electronically divides each step into smaller pieces by partially energizing two coils at once.

| MS1 | MS2 | MS3 | Microsteps | Steps/rev (1.8° motor) |
|-----|-----|-----|------------|----------------------|
| LOW | LOW | LOW | Full (1) | 200 |
| HIGH | LOW | LOW | 1/2 | 400 |
| LOW | HIGH | LOW | 1/4 | 800 |
| HIGH | HIGH | LOW | 1/8 | 1600 |
| HIGH | HIGH | HIGH | 1/16 | 3200 |
| LOW | LOW | HIGH | (same as 1/16) | 3200 |
| HIGH | LOW | HIGH | (reserved) | |
| LOW | HIGH | HIGH | (reserved) | |

**For 3D printers / CNC:** Usually 1/16 (all HIGH) for smooth motion.
**For slow precise positioning:** 1/4 or 1/8.
**For maximum torque:** Full step.

> **Tradeoff:** More microsteps = smoother motion but less torque per step. 1/16 is the sweet spot for most projects.

## Current Limiting — Don't Skip This

The A4988 has a tiny trimpot (screw-adjustable potentiometer) that sets the **maximum current** sent to the motor. If you don't set it:

- Too LOW → Motor has no torque, skips steps
- Too HIGH → Motor and driver overheat, can burn out

### How to Set It

1. Power the A4988 (VDD + VMOT)
2. Place a multimeter (voltage mode) between the trimpot metal top and GND
3. Adjust until voltage reads: **Vref = Imax × 8 × Rsense**
   - For most A4988 modules, Rsense = 0.05Ω (check yours)
   - Formula simplified: **Vref = Motor current rating × 0.4**
   - For a 1.2A motor: Vref = 1.2 × 0.4 = **0.48V**

### The Easier Way

1. Start with Vref at about 0.4V (turn trimpot most of the way down)
2. Run the motor and see if it skips steps
3. Turn Vref up a tiny bit (⅛ turn)
4. Repeat until motor runs smoothly

**The motor should NOT be too hot to touch.** If it's burning your finger, turn Vref down.

```
                A4988 module (top view)
          ┌─────────────────────────┐
          │    ○                    │  ← Trimpot (tiny screw)
          │                         │
          │                         │
          │            ○            │
          └─────────────────────────┘
          ↑ Multimeter probe here (metal part)
```

## How Step/Direction Signaling Works

The ESP32 sends **pulses** to the STEP pin. Each rising edge (LOW→HIGH) tells the A4988 to advance one microstep.

```
DIR pin ─────────────────────────────────── HIGH = forward
                            ────────────── LOW = reverse

STEP pin:
   ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐
   ││ ││ ││ ││ ││ ││ ││ ││
   └┘ └┘ └┘ └┘ └┘ └┘ └┘ └┘
   ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑
   Each = 1 microstep
```

Each pulse takes a tiny amount of time. The **maximum step rate** for the A4988 is about 200kHz. For most projects, 1–5kHz (1000–5000 steps per second) is plenty.

### Speed Formula

```
Steps per second = RPM × Steps_per_rev / 60

For a 1.8° motor at 1/16 microstepping:
  Steps per rev = 200 × 16 = 3200
  At 60 RPM:  60 × 3200 / 60 = 3200 steps/sec
  Pulse frequency: 3.2kHz
```

## Common Mistakes

| Mistake | Result |
|---------|--------|
| No power cap | Driver resets mid-motion, motor skips steps |
| VDD connected to VMOT (or vice versa) | Driver instantly dies (connected wrong voltage) |
| Wires swapped on motor coils | Motor vibrates but doesn't move — swap one coil's wires |
| Current too low | Motor has no torque, skips steps. You hear clicking |
| Current too high | Driver and motor overheat — possible burn |
| No ground connection between supplies | Driver doesn't work at all (no reference) |
| RESET/SLEEP floating | Driver stays in reset or sleep — motor does nothing |

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Power supply capacitor (100–470µF) | Driver resets, skips steps, erratic behavior |
| Current adjustment | Either weak motor or overheated driver |
| RESET/SLEEP pulled HIGH | Driver stays in reset or sleep — motor dead |
| Heat sink on A4988 | Driver overheats and enters thermal shutdown → stops working |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| A4988 Stepper driver module | 1 | With heatsink included if possible |
| NEMA17 stepper motor (1.8°) | 1 | 200 steps/rev, ~1.2A typical |
| 100µF 25V electrolytic cap | 1 | Minimum for VMOT decoupling |
| 470µF 25V electrolytic cap | 1 | Better for VMOT decoupling |
| 12V power supply (2A+) | 1 | Matches motor voltage rating |
| Jumper wires | 1 set | For ESP32 → A4988 |
| Small flathead screwdriver | 1 | For trimpot adjustment |
| Optional: Heatsink for A4988 | 1 | If running over ~500mA |
| Optional: Logic-level shifter | 1 | If motor requires >3.3V logic |

## See Also

- [grounding-decoupling](/fundamentals/grounding-decoupling)
- [power-batteries](/fundamentals/power-batteries)
- [buck-converter](/fundamentals/buck-converter)
- [reading-schematics](/fundamentals/reading-schematics)
- [multimeter](/fundamentals/multimeter)
