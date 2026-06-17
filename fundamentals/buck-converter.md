# Buck Converter (Step-Down) — Fundamental Reference

## What It Is

A buck converter takes a **higher DC voltage and steps it down to a lower DC voltage** efficiently. Unlike a linear regulator (which burns off excess voltage as heat), a buck converter uses switching to convert with 80–95% efficiency — meaning much less heat and higher available current.

> **Analogy:** A linear regulator is like a pressure valve that dumps excess water pressure into a leak. A buck converter is like a gearbox — it trades voltage for current but wastes very little energy.

## Linear vs Switching — The Big Difference

| | Linear Regulator (e.g. 7805) | Buck Converter |
|---|---|---|
| Efficiency | ~30–50% (Vin=12V, Vout=5V) | ~80–95% |
| Heat at 1A (12V→5V) | ~7W (needs a heatsink) | ~0.5W (barely warm) |
| Noise | Clean output | Some ripple (~10–50mV) |
| Circuit complexity | 3 pins, 2 caps | Inductor, caps, feedback network |
| Cost | $0.50 | $1–5 (module) |
| Best for | Low current, low dropout, noise-sensitive | High current, big voltage differences |

**Rule of thumb:** If you're dropping more than a few volts OR drawing more than 500mA, use a buck converter. Linear regulators are fine for small loads or when input and output are close.

## How Buck Conversion Works

A buck converter has four key parts: a **MOSFET switch**, an **inductor**, a **diode** (or second MOSFET for synchronous), and a **capacitor**.

```
Vin ──────┬─── [MOSFET] ────┬──── L1 ────┬──── Vout
          │                 │            │
        Cin ──── GND      Diode        Cout ──── GND
          │                 │            │
         GND               GND          GND
```

**The cycle:**

1. **MOSFET turns ON** — Current flows from Vin through the inductor to the output. The inductor stores energy in its magnetic field. Current ramps up.
2. **MOSFET turns OFF** — The inductor's magnetic field collapses, reversing its voltage. The diode (or second FET) provides a path for the current to keep flowing.
3. **The capacitor** — Smooths out the voltage, maintaining a steady output while the inductor charges and discharges.

The **duty cycle** (percentage of time the MOSFET is on) determines the output voltage:

```
Vout = Vin × Duty Cycle  (in continuous conduction mode)
```

## Common Modules

### LM2596 — The Classic Workhorse

- Input: 4.5–40V
- Output: 1.25–37V (adjustable)
- Max current: 3A (realistic: 2A continuous)
- Frequency: 150kHz (audible whine possible)
- Efficiency: ~80–88%

Clear blue PCB with a big inductor and a trim pot for adjustment. Cheap ($1–3). Bulky but reliable.

**Best for:** General purpose 12V→5V, 24V→12V, up to 2A.

### Mini-360 (MP1584-based) — Tiny & Light

- Input: 4.5–28V
- Output: 0.8–20V (adjustable)
- Max current: 2A (realistic: 1.2–1.5A continuous)
- Frequency: 1MHz (inaudible)
- Efficiency: ~85–93%

Tiny module smaller than a coin. Needs good cooling — the inductor and IC will overheat at sustained >1.5A.

**Best for:** Compact projects, battery-powered, moderate current.

### MP1584 — The Minier-360

Same chip as Mini-360 but in an even smaller package. The inductor is tiny. Watch the heat at anything above 1A.

### XL4015 — The High-Current Beast

- Input: 8–36V
- Output: 1.25–32V (adjustable)
- Max current: 5A (realistic: 4A with heatsinking)
- Frequency: 180kHz
- Efficiency: ~85–90%

Big inductor, big heatsink on the IC. The trim pot adjusts voltage, and there's usually a secondary trim for current limiting.

**Best for:** Powering 5V/3A from 12V, running multiple devices, LED strips.

### Which Module for Which Job?

| Job | Module | Why |
|---|---|---|
| 12V→5V @ 1A | LM2596 | Cheap, reliable, plenty of headroom |
| 12V→5V @ 3A | XL4015 | Needs heatsink, but handles the current |
| 24V→3.3V @ 500mA | Mini-360 | Compact, efficient at low current |
| 9V→5V @ 2A | Mini-360 | Small voltage drop, excellent efficiency |
| Battery-powered | Mini-360 / MP1584 | Higher frequency means smaller inductor, less weight |

## Input & Output Capacitors

Most modules come with caps. If you're building from scratch:

| Position | Recommendation | Why |
|---|---|---|
| Input cap | 100–470µF electrolytic + 0.1µF ceramic | Handles input ripple, keeps regulator stable |
| Output cap | 100–470µF electrolytic + 10µF ceramic | Reduces output ripple |

**Capacitor voltage rating:** Always at least 1.5× the max input voltage. A 25V cap on a 24V input will fail eventually.

Low-ESR caps (like polymer or good-quality electrolytic) improve stability and reduce ripple dramatically.

## Adjustable Output — The Feedback Resistor Divider

Most buck converter modules have an **adjustable version** (marked "ADJ"). The output voltage is set by two resistors forming a voltage divider on the feedback pin:

```
Vout ──── R1 ────┬──── FB pin
                 │
                 R2
                 │
                GND
```

The formula (for LM2596 and most modules):

```
Vout = Vref × (1 + R1/R2)
```

Where Vref is typically **1.25V** (varies by chip — check the datasheet).

**Common values for typical outputs (Vref = 1.25V):**

| Desired Vout | R1 (top) | R2 (bottom) | Actual Vout |
|---|---|---|---|
| 3.3V | 1.2kΩ | 1kΩ | 3.25V |
| 5V | 3kΩ | 1kΩ | 5.0V |
| 9V | 6.2kΩ | 1kΩ | 9.0V |
| 12V | 8.66kΩ | 1kΩ | 12.08V |

**On pre-built modules:** The trim pot is usually a 3296W-type (25-turn). Turn clockwise to raise voltage, counter-clockwise to lower. Always measure with a multimeter — the markings on the pot are not accurate.

## Efficiency vs Load

| Load | Efficiency | What happens |
|---|---|---|
| 0% (no load) | ~50–70% | Converter still draws quiescent current |
| 10–30% | ~85–92% | Sweet spot — highest efficiency |
| 50–80% | ~80–88% | Good — most modules run here |
| 100% | ~75–85% | Drop due to I²R losses in inductor and FET |

**Efficiency matters most for battery life.** If you're running from a battery, pick a module with >90% efficiency at your typical load.

## Heat Dissipation

- **LM2596:** The IC itself gets hot. Add a heatsink if >1.5A continuous.
- **Mini-360 (MP1584):** The inductor gets hot (saturation). The IC is under the PCB — thermal relief is poor.
- **XL4015:** Comes with a heatsink. Add airflow if >3A continuous.

**Signs of trouble:**
- Module reaches >80°C — reduce load or add cooling
- Inductor whistling — too much current or the inductor is saturating
- Voltage drops under load — the module is overheating or the input supply can't deliver

## Input Voltage Must Be Higher Than Output — Dropout

A buck converter **can only step down**. The input must be at least 1–2V higher than the output (the dropout voltage, which varies by chip).

| Module | Typical dropout | Notes |
|---|---|---|
| LM2596 | ~1.5V | 12V→10V OK. 12V→11.5V — might lose regulation |
| Mini-360 | ~0.8V | Better for small voltage drops |
| XL4015 | ~1.5V | Similar to LM2596 |

**Rule of thumb:** Keep Vin at least 2V above Vout for reliable regulation.

## Output Ripple

All buck converters produce some ripple at the switching frequency.

| Module | Typical ripple | Mitigation |
|---|---|---|
| LM2596 | 30–80mV p-p | Extra cap + small inductor (LC filter) |
| Mini-360 | 20–50mV p-p | Better caps help |
| XL4015 | 30–100mV p-p | Higher ripple at high current |

**How to reduce ripple:**
- Add a 10–47µF low-ESR cap at the output
- Add an LC filter (10µH + 100µF) after the output
- Keep load wires short
- Use a linear regulator after the buck for noise-sensitive loads (post-regulation)

## When to Use a Buck Converter

| Use | Why |
|---|---|
| 12V battery → 5V for ESP32/RPi | High current, big voltage drop — linear would melt |
| 24V industrial supply → 12V fans | Efficiency saves power in enclosures |
| 9V battery → 3.3V sensor | Battery lasts much longer vs linear regulator |
| Any time you want less heat | Buck converters run cool |

**When NOT to use a buck converter:**
- Input and output voltages are close (<1V difference) — use an LDO
- Load is <50mA and you want simplicity — use a linear regulator
- Noise can't be tolerated (audio, RF) — post-regulate with an LDO or add heavy filtering
- Space is extremely tight — some linear regulators are smaller

## Quick Reference

```
Buck converter: Vin > Vout, steps down voltage, ~85–95% efficient

Formula:  Vout = Vin × Duty Cycle
Feedback: Vout = Vref × (1 + R1/R2)   (Vref usually 1.25V)

Module        │ Vin       │ Iout(max) │ Freq    │ Size
LM2596        │ 4.5–40V   │ 3A (2A)   │ 150kHz  │ Large
Mini-360      │ 4.5–28V   │ 2A (1.5A) │ 1MHz    │ Tiny
XL4015        │ 8–36V     │ 5A (4A)   │ 180kHz  │ Large + heatsink

Caps:
  Input:  100–470µF electrolytic + 0.1µF ceramic
  Output: 100–470µF electrolytic + 10µF ceramic

Vin must be 1.5–2V above Vout minimum
Ripple: 20–100mV p-p (add LC filter to reduce)
Heat: if >80°C, reduce load or add cooling
```

## See Also

- [stepper-motor-a4988](/projects/stepper-motor-a4988)
