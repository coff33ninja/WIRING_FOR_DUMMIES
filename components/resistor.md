# Resistor — Component Reference

> **See also:** [Resistor Network](../fundamentals/resistor-network.md) — multiple resistors in one package for pull-up arrays and precision matching.

## What It Is

A resistor **limits how much current can flow**. It resists the flow of electricity and converts the extra energy into heat.

> **Analogy:** A garden hose with a kink. The more you pinch (higher resistance), the less water flows. The energy goes into heating the hose at the kink.

## Resistor Types — Which Construction for Which Job

### 1. Carbon Film — The Cheap Standard

Cylindrical with colored bands, light brown/beige body. Most common through-hole resistor.

| Pros | Cons |
|------|------|
| Cheap ($0.01 each) | Tolerates only ±5% (worst precision) |
| Widely available everywhere | Higher noise than metal film |
| Good enough for LEDs, pull-ups | Temperature drift ~250–500 ppm/°C |

**Use for:** LED current limiting, pull-up/pull-down, general-purpose where ±5% is fine.

### 2. Metal Film — Precision Choice

Cylindrical with colored bands, blue body (usually 5-band).

| Pros | Cons |
|------|------|
| Tolerates ±1% (precision) | Slightly more expensive |
| Low noise — good for analog | Overkill for LEDs |
| Temperature drift ~50–100 ppm/°C (stable) | |

**Use for:** Voltage dividers, analog sensor circuits, op-amp circuits, ADC reference dividers, I2C pull-ups where accuracy matters.

> **How to tell:** Carbon film = beige/tan body, 4-band. Metal film = blue body, 5-band. Both work for most hobby projects, but use metal film when the value matters.

### 3. Metal Oxide — High Power / High Temperature

Cylindrical, usually light blue or gray, similar look to metal film.

| Pros | Cons |
|------|------|
| Handles higher temperatures (up to 200°C) | Larger for same rating |
| More robust / flameproof | Limited precision (usually ±5%) |
| Better pulse handling | |

**Use for:** Power supply inrush limiting, snubbers, circuits that get hot.

### 4. Wirewound — High Power, Low Precision

Cylindrical, usually white/green ceramic body or rectangular aluminum case.

| Pros | Cons |
|------|------|
| Can handle 5W–100W+ acts as a small heater | Large and heavy |
| Very stable for power applications | **Inductive** — bad for RF/high-frequency |
| Poor precision (usually ±5–10%) |

**Use for:** Motor braking resistors, dummy loads, high-current current sensing, power supply bleed resistors.

> **Warning:** Wirewound resistors are coils of wire — they act as inductors at high frequencies. Never use them in RF circuits, switching regulator feedback, or high-speed digital.

### 5. SMD Resistor — Surface Mount

Tiny rectangular block, no legs. Uses **numeric code** instead of color bands.

```
   ┌─────────┐
   │  472    │  ← 3-digit: 47 × 10² = 4700Ω = 4.7kΩ
   └─────────┘

   ┌─────────┐
   │ 1002    │  ← 4-digit: 100 × 10² = 10000Ω = 10kΩ (±1%)
   └─────────┘

   ┌─────────┐
   │   0     │  ← Zero-ohm jumper (basically a wire)
   └─────────┘
```

**Reading SMD codes:**
- **3-digit:** First two = value, third = multiplier. `472` = 47 × 100 = 4.7kΩ. ±5%.
- **4-digit:** First three = value, fourth = multiplier. `1002` = 100 × 100 = 10kΩ. ±1%.
- **R = decimal point:** `4R7` = 4.7Ω. `0R22` = 0.22Ω.
- **0 / 000:** Zero-ohm jumper (connects pads on PCB).

**Common sizes:**

| Size code | Dimensions | Power rating | Typical use |
|-----------|------------|-------------|-------------|
| 0201 | 0.6×0.3mm | 1/20W | Ultra-compact phones |
| 0402 | 1.0×0.5mm | 1/16W | Compact designs |
| 0603 | 1.6×0.8mm | 1/10W | Most common hobby SMD |
| 0805 | 2.0×1.2mm | 1/8W | Easy to hand-solder |
| 1206 | 3.2×1.6mm | 1/4W | Easy to see/handle |

> **For hand-soldering:** Start with 0805 or 1206. 0603 is doable with a steady hand. 0402 is for machines only.

### 6. Fusible Resistor — Sacrificial Protector

Looks like a regular resistor but designed to act as a **fuse** — it opens (goes infinite resistance) when overloaded, protecting the circuit.

**Use for:** Power input protection where space is tight and you want both resistance and fuse in one part.

### 7. Zero-Ohm Jumper (0Ω)

A resistor that reads 0Ω. It's literally a wire in a resistor package.

**Use for:** Bridging PCB traces during assembly where you might want to change the connection later, or when you need to jump a trace with a pick-and-place machine.

### 8. Resistor Array / Network

Multiple resistors in one package, usually with a common pin.

```
                   ┌────┐
   COM ────────────┤    │
              R1 ─┤   ├─ Pin 1
              R2 ─┤   ├─ Pin 2
              R3 ─┤   ├─ Pin 3
              R4 ─┤   ├─ Pin 4
                   └────┘
```

**Use for:** Pull-up groups for data buses (like I2C, SPI), where you need multiple identical resistors in a compact layout.

## Which Type Should You Use?

| Application | Best type | Why |
|-------------|-----------|-----|
| LED current limiting | **Carbon film** (±5%) | Cheap, good enough |
| Pull-up / pull-down | **Carbon film** (±5%) | Value is not critical |
| I2C pull-up | **Metal film** (±1%) | Ensure bus timing accuracy |
| Voltage divider (ADC) | **Metal film** (±1%) | Accuracy matters for readings |
| Analog sensor divider | **Metal film** (±1%) | Don't want noise/error |
| High current sense (>0.5W) | **Wirewound** or **metal oxide** | Power handling |
| High-frequency circuit | **Metal film** or **carbon film** | Never wirewound (inductive) |
| Breadboard prototyping | **Carbon film** (cheap) | Your default choice |
| PCB assembly | **SMD 0805 or 0603** | Space-saving, machine-solderable |

## Units — Ohms (Ω)

| Symbol | Name | What it means |
|--------|------|---------------|
| 0Ω | Zero ohms | Jumper (a wire) |
| 10Ω | Ten ohms | Little resistance |
| 220Ω | Two hundred twenty | LED current limiting |
| 1kΩ | One kilo-ohm = 1000Ω | Pull-up/pull-down |
| 10kΩ | Ten kilo-ohm = 10000Ω | Common pull-up, divider |
| 1MΩ | One mega-ohm = 1,000,000Ω | Very high, debouncing |

## Color Codes — Reading Through-Hole Resistors

```
           ┌──────────────────┐
           │                  │
           │ ■ ■ ■ ■ □       │
           │                  │
           └──────────────────┘
```

| Color | Digit | Value |
|-------|-------|-------|
| Black | 0 | ×1Ω |
| Brown | 1 | ×10Ω |
| Red | 2 | ×100Ω |
| Orange | 3 | ×1kΩ |
| Yellow | 4 | ×10kΩ |
| Green | 5 | ×100kΩ |
| Blue | 6 | ×1MΩ |
| Violet | 7 | ×10MΩ |
| Gray | 8 | — |
| White | 9 | — |
| Gold | ±5% | ×0.1 (for <10Ω) |
| Silver | ±10% | ×0.01 (for <1Ω) |

**4-band (carbon film, ±5%):** Brown-Black-Red-Gold = 1 0 × 100 = 1kΩ ±5%
**5-band (metal film, ±1%):** Brown-Black-Black-Brown-Brown = 1 0 0 × 10 = 1kΩ ±1%

## Common Values in Our Projects

| Value | Label | Used for |
|-------|-------|----------|
| 220Ω | Red-Red-Brown | LED current limiting |
| 330Ω | Orange-Orange-Brown | LED current limiting (brighter) |
| 470Ω | Yellow-Violet-Brown | LED current limiting (dimmer) |
| 1kΩ | Brown-Black-Red | Pull-up/down, base resistor |
| 4.7kΩ | Yellow-Violet-Red | I2C pull-up, One-Wire pull-up |
| 10kΩ | Brown-Black-Orange | Pull-up/down, voltage divider |
| 100kΩ | Brown-Black-Yellow | High-value pull-down, debouncing |

## Power Rating

Most hobby resistors are **1/4 watt (0.25W)** — enough for 99% of projects. Here's when you go bigger:

| Rating | Size (approx) | At 5V max current | At 12V max current |
|--------|---------------|-------------------|--------------------|
| 1/8W (125mW) | Tiny (SMD 0805) | 25mA | 10mA |
| **1/4W** (250mW) | Standard through-hole | 50mA | 20mA |
| 1/2W (500mW) | Slightly larger | 100mA | 42mA |
| 1W | Medium cylindrical | 200mA | 83mA |
| 5W | Large wirewound | 1A | 416mA |

**Rule:** If the resistor gets too hot to touch (<5s), you need a bigger power rating.

Every resistor value has a standard E-series (E12, E24, E48). The most common is **E12** — the values we all know: 1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2 (and ×10/×100/×1k/×10k/×100k).

## What Happens If You Choose the Wrong Type

| Mistake | Result |
|---------|--------|
| Wirewound in RF/audio circuit | Acts as inductor — distorts signal |
| Carbon film in precision voltage divider | ADC readings drift with temperature |
| SMD 0402 when you need to hand-solder | Can't solder it — drops into a black hole |
| 1/4W resistor across 12V at 100mA | Gets hot — exceeding 0.25W |
| Zero-ohm jumper used as fuse | Doesn't blow — acts as wire (not fusable) |
| Resistor array for single pull-up | Waste of money — use single resistor |

## Quick Reference

```
Type      | Body color | Tolerance | Best for
Carbon    | Beige/tan  | ±5%       | LEDs, pull-ups (cheap)
Metal     | Blue       | ±1%       | Dividers, analog (precise, low noise)
Oxide     | Light blue | ±5%       | High power, high temp
Wirewound | White/green| ±5–10%    | High current (inductive — not for HF)
SMD       | Tiny black | ±1–5%     | PCBs (numeric code)

Reading:
  4-band (carbon):   Brown-Black-Red-Gold = 1kΩ ±5%
  5-band (metal):    Brown-Black-Black-Brown-Brown = 1kΩ ±1%
  SMD 3-digit:       472 = 4.7kΩ
  SMD 4-digit:       1002 = 10kΩ

Power:
  1/4W (standard) → most projects
  Gets hot? → go bigger (1/2W, 1W, 5W)
```
