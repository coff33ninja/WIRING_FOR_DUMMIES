# DC Fan — Component Reference

## What It Is

A DC fan moves air using a spinning motor inside a housing. Most desktop computer fans are **brushless DC (BLDC)** with a built-in controller. Simpler fans use **brushed motors**. Which one you need depends on whether you want speed control, feedback, or just on/off.

> **Analogy:** A desk fan you can plug in (on/off) vs one with speed dial (PWM) vs one that reports its current speed (tachometer).

## Brushed vs Brushless DC Fans

### Brushed DC Fan

Old-school fan with carbon brushes. Two wires: positive and negative. Apply voltage, it spins.

| Pros | Cons |
|------|------|
| Simple — just power it | Brushes wear out (~1000–3000 hrs) |
| Cheap | Noisy (brush sparking) |
| Works on PWM directly | Electrically noisy (RFI) |
| Easy to reverse polarity | Less efficient |

**Use for:** Cheap cooling where noise and lifespan don't matter.

### Brushless (BLDC) Computer Fan

The standard in PCs, 3D printers, electronics enclosures. Has a built-in controller board that drives the motor coils electronically.

| Pros | Cons |
|------|------|
| Long life (30,000–100,000 hrs) | More expensive |
| Quiet | Electronics can be damaged by bad PWM |
| Built-in feedback (tach) available | Must respect control wire signals |
| Efficient | Can't reverse by swapping power (needs separate signal) |

**Use for:** Everything modern — computers, enclosures, ventilation, active cooling.

## Wiring Configurations

### 2-Wire Fan (Power + Ground)

```
Fan Red  ───── VCC (+)
Fan Black ───── GND (–)
```

**Speed control:** Change voltage (e.g. 5V = half speed on a 12V fan) — but most fans don't start below ~4–5V.

**No feedback.** No way to know if the fan is spinning.

### 3-Wire Fan (Power + Ground + Tachometer)

```
Fan Red    ───── VCC (+)
Fan Black  ───── GND (–)
Fan Yellow ───── Tachometer output (open-collector)
```

The **yellow wire** outputs **2 pulses per revolution** (some fans do 1 or 4 — check datasheet). The signal is an open-collector output: it pulls to GND briefly each revolution, and floats high otherwise.

**Reading tach on a microcontroller:**

```
Tach pin ──┬── 10kΩ pull-up ── 3.3V / 5V
           └── GPIO input (interrupt)
```

Count rising edges over 1 second, divide by 2 (or whatever pulses-per-rev your fan uses), that's RPM.

**Speed control:** Voltage control only (reduce VCC). Can't use PWM on VCC without external MOSFET (see below).

### 4-Wire Fan (Power + Ground + Tach + PWM)

```
Fan Red    ───── VCC (+) — always at full voltage (e.g. 12V)
Fan Black  ───── GND (–)
Fan Yellow ───── Tachometer
Fan Blue   ───── PWM control input
```

The **PWM pin** is a 5V logic input (3.3V works on most, but 5V is safer). The fan's internal controller uses this signal to switch the motor coils on and off — **not** the same as chopping the power wire.

**PWM signal requirements:**

- Frequency: **25kHz** (standard for 4-wire fans). Do not use 1kHz like you would for an LED — the fan will buzz or stall.
- Duty cycle: 0% = off, 100% = full speed
- Logic level: 5V typically (use level shifter if MCU is 3.3V)

> **Why 25kHz?** Above the audible range. A 1kHz PWM on a fan creates an audible whine. 25kHz is inaudible to humans.

**Speed range:**

| PWM duty | Fan speed | Typical start voltage |
|----------|-----------|---------------------|
| 0% | Stopped | — |
| 10% | ~20% speed | Min start ~4–5V |
| 50% | ~50% speed | |
| 100% | Full speed | |

Most 4-wire fans don't start reliably below 30% duty — they need a "kick" to overcome static friction. Once spinning, they'll run down to ~10%.

## Voltage vs PWM Speed Control

| Method | How it works | Good for | Bad for |
|--------|-------------|----------|---------|
| **Voltage control** | Reduce VCC to fan (e.g. 5V on a 12V fan) | Quiet analog control | Fans stall below ~4–5V; inefficient (regulator heats up) |
| **PWM on 4-wire fan** | Internal controller switches coils at kHz | Wide speed range, efficient | Requires 4-wire fan |
| **PWM on 2/3-wire fan (via MOSFET)** | Switch VCC on/off at low frequency | On/off or crude speed control | **Risky** — see below |

## Why NOT to PWM a 2-Wire Fan Directly

If you put a MOSFET on the VCC line of a 2-wire fan and PWM it at 1kHz:

| Problem | What happens |
|---------|-------------|
| **Back-EMF spikes** | The motor coils generate voltage when power cuts — can exceed MOSFET rating |
| **Stalled detection** | The fan's internal electronics see power cycling and think the fan is blocked |
| **Audible noise** | Low-frequency PWM makes the motor coil sing (whine/buzz) |
| **No start guarantee** | If the PWM duty is too low, the fan never gets enough energy to start spinning |

**If you must PWM a 2/3-wire fan:**
- Use a **MOSFET** with a **flyback diode** across the fan terminals (cathode to VCC)
- Use a **slow frequency** (~30Hz) — below audible, but still risky
- Better option: use a 4-wire fan, or buy a **voltage regulator** to lower fan voltage smoothly

## MOSFET Switching for On/Off

For turning a fan on or off (no speed control), use an N-channel MOSFET:

```
12V ─── Fan (+) ─── Fan (–) ─── Drain (MOSFET)
                                   │
GND ─────────────────────────────── Source (MOSFET)
                                   │
MCU GPIO ───── 1kΩ ─────────────── Gate (MOSFET)
```

- N-channel MOSFET on the low side (between fan GND and power supply GND)
- Gate resistor (~1kΩ) to limit MCU pin current
- Use a logic-level MOSFET (IRLZ44N, IRLB8748, etc.) for 3.3V/5V gate drive

## Flyback Diode (Inductive Load)

A fan motor is an **inductive load**. When you cut power, the magnetic field collapses and generates a **high-voltage spike** that can destroy your MOSFET or MCU.

**Always place a flyback diode** across the fan terminals (or across the motor coil):

```
         ┌──►|────┐
         │  1N4001 │
        (+)      (–)
        Fan      Fan
```

- Diode cathode to fan VCC (+), anode to fan GND (–)
- **1N4001–1N4007** for small fans (1A rating)
- **Schottky** (1N5819) for faster switching (PWM applications)
- Without it: expect MOSFET failure, MCU resets, or magic smoke

## Common Sizes and Voltages

| Size | Typical voltage | Current (no load) | Airflow | Use in |
|------|----------------|-------------------|---------|--------|
| 30mm | 5V | 0.05–0.10A | ~2 CFM | Tight enclosures, hotends |
| 40mm | 5V / 12V | 0.05–0.15A | ~5 CFM | 3D printer hotend, small cases |
| 60mm | 12V | 0.10–0.25A | ~15 CFM | PSUs, general cooling |
| 80mm | 12V | 0.10–0.30A | ~30 CFM | Standard case fan |
| 92mm | 12V | 0.15–0.40A | ~45 CFM | CPU coolers, cases |
| 120mm | 12V | 0.15–0.50A | ~60 CFM | Most common case fan |
| 140mm | 12V | 0.20–0.60A | ~80 CFM | Quiet builds, radiators |
| 200mm | 12V | 0.30–0.80A | ~120 CFM | Large silent cases |

**Common voltages:** 5V (small, USB-powered), 12V (standard PC), 24V (industrial, 3D printers), 48V (server/telecom).

> **Tip:** Running a 12V fan at 5V through a voltage regulator wastes power as heat. A 5V fan at 5V is more efficient than a 12V fan at 5V.

## Quick Reference

```
2-wire:   Power + GND only
3-wire:   Power + GND + Tach (RPM feedback, yellow)
4-wire:   Power + GND + Tach + PWM (speed control, blue)

PWM on 4-wire fan: 25kHz, 5V logic, 0-100% duty
PWM on 2/3-wire fan: risky — use MOSFET + flyback diode + ~30Hz

Flyback diode required for any inductive motor load.
N-channel MOSFET on low side for on/off or PWM.

Tach reading: 2 pulses/rev (typical), needs pull-up resistor.
```
