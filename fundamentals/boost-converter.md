# Boost Converter (Step-Up) — Fundamental Reference

## What It Is

A boost converter takes a **lower DC voltage and steps it up to a higher DC voltage**. It does this by storing energy in an inductor and releasing it at a higher voltage. Like a buck converter, it's a switching regulator — efficient, but with some important quirks.

> **Analogy:** A boost converter is like a playground pump that slowly builds up pressure in a tank, then releases it in a burst to launch water higher than the source.

## How Boost Conversion Works

A boost converter uses: a **MOSFET switch**, an **inductor**, a **diode**, and an **output capacitor**.

```
           L1
Vin ──────mmm────┬──── Diode ────┬──── Vout
          │      │              │
          │   [MOSFET]        Cout ──── GND
          │      │              │
         GND    GND            GND
```

**The cycle:**

1. **MOSFET turns ON** — Current flows from Vin through the inductor straight to ground. The inductor stores energy in its magnetic field. The diode is reverse-biased (blocked), so the output capacitor supplies the load.
2. **MOSFET turns OFF** — The inductor's magnetic field collapses. The inductor voltage **reverses** and adds to Vin (this is the "boost"). The combined voltage forces current through the diode to the output capacitor and load.

The output voltage is set by the duty cycle:

```
Vout = Vin / (1 − Duty Cycle)
```

This means a 90% duty cycle gives 10× the input voltage — but real-world losses and component limits cap this.

> **Key difference from buck:** In a buck converter, current flows continuously through the inductor to the output. In a boost, current only flows to the output during the OFF time — meaning the inductor and switch must handle the full input current PLUS the output current.

## Common Modules

### MT3608 — The Tiny Powerhouse

- Input: 2–24V
- Output: up to 28V (adjustable, Vout = Vin × ~2.5 max practical)
- Max current: 2A (realistic: 1A continuous at moderate boost)
- Frequency: 1.2MHz
- Efficiency: ~80–90%

Tiny module with a small inductor and a trim pot. Potentiometer adjusts the feedback voltage (Vref ≈ 0.6V). Popular for boosting 3.7V Li-ion to 5V or 12V.

**Best for:** Battery-powered projects, moderate current, portable devices.

### XL6009 — The High-Power Beast

- Input: 5–32V
- Output: up to 35V (adjustable)
- Max current: 4A (realistic: 2–3A continuous with heatsinking)
- Frequency: 400kHz
- Efficiency: ~85–92%

Bigger module with a larger inductor and a heatsink. Better thermal performance at high current.

**Best for:** 12V→24V, higher current boost, LED drivers.

### Which Module for Which Job?

| Job | Module | Why |
|---|---|---|
| 3.7V Li-ion → 5V @ 1A | MT3608 | Small, efficient at moderate boost |
| 3.7V Li-ion → 12V @ 200mA | MT3608 | High boost ratio, but low current OK |
| 5V USB → 12V @ 1A | XL6009 | Higher current at high boost |
| 12V → 24V @ 2A | XL6009 | Big inductor, heatsink, low ripple |
| 2xAA (3V) → 5V | MT3608 | Only if you keep current under 500mA |

## Input Current vs Output Current — Conservation of Power

This is the **most important concept in boost converters**. Power in = Power out (minus losses).

```
Vin × Iin × Efficiency = Vout × Iout
```

**Example:** 3.7V Li-ion → 5V @ 1A output, 85% efficiency

```
Iin = (5V × 1A) / (3.7V × 0.85) = 5 / 3.145 ≈ 1.59A
```

Your 3.7V battery must supply **1.59A** to get 1A at 5V. If the battery can't deliver that, the module will either:
- Drop the output voltage (it falls out of regulation)
- Shut down
- Overheat and fail

**Higher boost ratio = higher input current.** To get 24V from 3.7V at 1A output:

```
Iin = (24V × 1A) / (3.7V × 0.80) = 24 / 2.96 ≈ 8.1A
```

That's 8 amps from a tiny Li-ion — not realistic. The module would fail or shut down.

## Minimum Input Current Requirement

Every boost module needs a minimum input current to start up and maintain regulation:

| Module | Min Iin (typical) | Notes |
|---|---|---|
| MT3608 | ~500mA | At startup, draws a spike. Battery must handle it. |
| XL6009 | ~1A | Larger module, needs more startup current. |

**If your power source can't supply the startup current:**
- The module may "chirp" (start, stop, start again)
- Output voltage never reaches the target
- The module oscillates and produces weird noises

**Fix:** Use a larger input cap (100–220µF) to absorb the startup surge. Or use a power source with higher current capability.

## No Output When Input Is Too Low

Boost converters have an **undervoltage lockout (UVLO)** — typically around 2V for most modules. Below this, the chip shuts down to protect itself.

| Module | Typical UVLO | Behavior below UVLO |
|---|---|---|
| MT3608 | ~2V | Chip off, no output |
| XL6009 | ~4.5V (varies) | Chip off, no output |

**For Li-ion batteries:** A 3.7V cell drains to ~3.0V before protection kicks in. The MT3608 will work down to ~2.5V, but at those voltages, you're deep-discharging the battery. Use a protection circuit on the battery.

> **Warning:** Some boost modules pass the input voltage to the output through the inductor and diode even when the chip isn't switching. This means you might see ~Vin - 0.3V on the output — not enough to power your load, but enough to be confusing.

## Output Capacitor Selection for Low Ripple

Boost converters have **higher ripple than buck converters** because the output only gets energy during the OFF time.

| Module | Typical ripple | Output cap on module |
|---|---|---|
| MT3608 | 20–100mV p-p | 10–22µF ceramic |
| XL6009 | 30–150mV p-p | 100µF electrolytic + ceramic |

**Reducing ripple:**
- Add a **220µF low-ESR cap** in parallel with the output
- Add a small **10µH inductor + 100µF cap** (LC filter) after the output
- Keep load wires short (<10cm)
- Avoid high ripple for sensitive loads like audio or ADC references

## Safety — Output Can Be Present on Input When Enabled

This is a **dangerous and often overlooked** property of boost converters:

**When a boost converter is running, the output voltage is also present at the input (minus the diode drop) if the inductor and diode conduct backwards.**

More practically: **If you turn off the input power while the boost is running, the output caps discharge into the input** through the inductor and diode. This can:
- Power the input line unexpectedly
- Keep microcontrollers running when you think they're off
- Damage the input source

**With MT3608 specifically:** The chip uses a **synchronous rectifier** (a second FET instead of a diode). When enabled, the output is effectively connected to the input. **Never disconnect the input while the boost is running** — you'll get voltage on the input from the output caps.

> **Warning:** If your circuit has a boost converter and a separate power path, make sure the boost can't back-feed into the input line. Use a Schottky diode on the input (Vin → diode → boost module) to prevent back-feed if needed.

## Common Uses

### Powering 5V from a 3.7V Li-ion Battery

The classic use case. A single 18650 cell → MT3608 → 5V for an ESP32 or Arduino.

**Design considerations:**
- 18650 capacity: 2000–3500mAh
- At 5V/200mA output, input current ≈ 390mA
- Run time: 2000mAh / 390mA ≈ 5 hours (before conversion losses)
- Use a protected 18650 or add a TP4056 charge board + DW01 protection

### Generating 12V from 5V USB

USB provides 5V at up to 2.4A (typical). A boost converter can give you 12V:

- 5V → 12V @ 500mA requires: Iin = (12 × 0.5) / (5 × 0.85) = 1.41A
- USB can supply this (2A port)
- Use XL6009 for reliable 12V/500mA

**Common loads:** Relay coils (12V), small pumps, LCD backlights (12V LED strips), fans.

### Other Use Cases

| Source | Target | Module | Notes |
|---|---|---|---|
| 1.5V (AA) | 3.3V | MT3608 | Low current only (50–100mA) |
| 3.7V Li-ion | 9V | MT3608 | For multimeters, guitar pedals |
| 5V USB | 24V | XL6009 | For LED strips, solenoid valves |
| 12V battery | 24V | XL6009 | For automotive accessories |

## Heat Dissipation

| Module | Heat source | Mitigation |
|---|---|---|
| MT3608 | Inductor (saturation) + IC | Limit to 1A output, add thermal pad |
| XL6009 | IC (under load) + inductor | Heatsink included, add airflow |

**If the module gets hot (>80°C):**
- Reduce the load current
- Increase input voltage (lower boost ratio = higher efficiency)
- Add a heatsink (small copper heatsinks with thermal tape work)
- Consider a module with a larger inductor (less core loss)

## Quick Reference

```
Boost converter: Vin < Vout, steps up voltage, ~80–92% efficient

Formula:  Vout = Vin / (1 − Duty Cycle)
Power:    Iin = (Vout × Iout) / (Vin × Efficiency)

Module     │ Vin       │ Iout(max) │ Freq    │ Best use
MT3608     │ 2–24V     │ 2A (1A)   │ 1.2MHz  │ 3.7V→5V, portable
XL6009     │ 5–32V     │ 4A (2–3A) │ 400kHz  │ 5V→12V, high current

Important:
  Higher boost ratio = higher input current
  Input current is ALWAYS higher than output current
  Mount output caps near the load for low ripple
  Boost can back-feed when enabled — isolate input if needed

Typical ripple: 20–150mV p-p
UVLO: ~2V (MT3608), ~4.5V (XL6009)
Startup current: 500mA–1A minimum

Safety:
  - Output voltage may appear on input when switching
  - Never disconnect input while running
  - Protect Li-ion cells from deep discharge
  - Add Schottky on input if back-feed is a problem
```

## See Also

- [oled-sensor-readout](/projects/oled-sensor-readout)
