# Resistor Network / Pack — Fundamental Reference

> **See also:** [Resistor](../components/resistor.md) — the underlying resistor types and color codes.

## What It Is

A resistor network is multiple resistors in a single package. Instead of placing 8 individual pull-up resistors on a breadboard (messy), you use one 8-pin SIP that has 7 resistors sharing a common pin.

```
    ┌─┬─┬─┬─┬─┬─┬─┬─┐
    │1│2│3│4│5│6│7│8│   ← Pins
    └─┴─┴─┴─┴─┴─┴─┴─┘
      │ │ │ │ │ │ │
      R R R R R R R
      │ │ │ │ │ │ │
      └─┴─┴─┴─┴─┴─┴── Common pin (pin 1)
```

## Why Use a Resistor Network

| | Individual Resistors | Resistor Network |
|--|--------------------|------------------|
| PCB space | Lots | Little |
| Assembly time | 8 pick-and-place | 1 pick-and-place |
| Cost | $0.08 × 8 = $0.64 | $0.10 |
| Matching | Unmatched (5% each) | **Matched (0.5–2%)** |
| Breadboard | 16 jumper wires | 8 jumper wires |

**Matching** is the killer feature. The resistors in a network are fabricated on the same substrate at the same time — they track temperature changes together and have very close ratios. Critical for precision voltage dividers and DAC/ADC circuits.

## Types

### Bussed (Common) — Most Common

All resistors share one common pin (usually pin 1). Used for pull-up/pull-down arrays.

```
Pin 1 ─┬── R ── Pin 2
        ├── R ── Pin 3
        ├── R ── Pin 4
        ├── R ── Pin 5
        ├── R ── Pin 6
        ├── R ── Pin 7
        └── R ── Pin 8
```

Example: 7 × 10kΩ bussed — connect pin 1 to VCC, pins 2–8 each to separate GPIO inputs.

### Isolated

Each pair of pins is its own resistor. No common pin. Used where you need independent resistors.

```
Pin 1 ─┬── R ── Pin 2
Pin 3 ─┬── R ── Pin 4
Pin 5 ─┬── R ── Pin 6
Pin 7 ─┬── R ── Pin 8
```

Example: 4 × 10kΩ isolated — 4 independent resistors in one DIP-8 package.

### Dual Terminator

Special type used for SCSI and parallel termination — typically 220Ω and 330Ω per line. Not common in hobby electronics.

## Packages

| Package | Pins | Type | Common Values |
|---------|------|------|---------------|
| SIL / SIP | 4–10 | Usually bussed | 10kΩ, 4.7kΩ, 1kΩ |
| DIL / DIP | 8, 14, 16 | Isolated or bussed | 10kΩ |
| SOIC | 8–16 | SMD isolated or bussed | Variable |
| 0402/0603 arrays | 4 | SMD isolated | Variable |

**SIP (Single In-line Package)** is the breadboard-friendly one — a flat black rectangle with legs in a row. Marked with a dot or stripe at pin 1 (common).

## Reading the Codes

SIP resistor networks often have a printed code like `A104J`:

| Code | Meaning |
|------|---------|
| A | Configuration (A = bussed, B = isolated) |
| 104 | Resistance = 10 × 10^4 = 100,000 Ω = 100kΩ |
| J | Tolerance (±5%) |

- First two digits = significant figures
- Third digit = multiplier (number of zeros)
- Examples: 471 = 470Ω, 102 = 1kΩ, 103 = 10kΩ, 104 = 100kΩ

## Common Uses

### Pull-Up Array for Buttons

```
VCC ── pin 1 (common)
      │
      ├── 10kΩ ── pin 2 ── button 1 ── GND
      ├── 10kΩ ── pin 3 ── button 2 ── GND
      ├── 10kΩ ── pin 4 ── button 3 ── GND
      ...
```

### Pull-Up Array for I2C

```
3.3V ── pin 1 (common)
       │
       ├── 4.7kΩ ── pin 2 ── SDA
       ├── 4.7kΩ ── pin 3 ── SCL
       │
       (remaining pins unused)
```

### LED Current Limiting (Isolated Type)

```
VCC ── 330Ω (between pins 1–2) ── LED 1 ── GND
VCC ── 330Ω (between pins 3–4) ── LED 2 ── GND
```

## Wiring to Breadboard

```
SIP Resistor Network:
    ┌─ ── ── ── ── ──┐
    │                  │
    │   Dot marks      │
    │   pin 1          │
    │                  │
    └─ ┬─┬─┬─┬─┬─┬─┬─┘
       │ │ │ │ │ │ │ │
       1 2 3 4 5 6 7 8
```

Insert across the breadboard center gap. Pin 1 goes into one side, pins 2–8 go into the other side. The common pin (1) connects to VCC or GND. The other pins go to your signal lines.

## Quick Reference

- **SIP 8-pin** bussed resistor network = 7 resistors with one common pin
- **Common values:** 4.7kΩ (I2C pull-up), 10kΩ (general purpose pull-up), 330Ω (LED)
- **Tolerance:** Usually ±2% (better than individual 5% resistors)
- **Power rating:** Typically 1/8W per resistor, 1/4W total
- **Marking:** Dot or stripe at pin 1; code like A104J
- **For pull-up arrays:** Use bussed type. Connect common pin to VCC.
- **For independent resistors:** Use isolated type.
- **Matching matters:** Use networks for precision voltage dividers and analog circuits.

## See Also

- [74hc595-shift-register](/projects/74hc595-shift-register)
