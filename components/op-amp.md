# Operational Amplifier (Op-Amp) — Component Reference

## What It Is

An operational amplifier ("op-amp") is a high-gain voltage amplifier with two inputs and one output. With external resistors and capacitors, you can make it amplify, filter, add, subtract, integrate, or buffer signals.

The "ideal" op-amp:
- **Infinite gain** — a tiny voltage difference between inputs gets amplified to the rails
- **Infinite input impedance** — no current flows into the inputs
- **Zero output impedance** — can drive any load
- **Infinite bandwidth** — amplifies all frequencies equally

Real op-amps approximate this. The TL072, LM358, LM324, and NE5532 are the most common hobbyist parts.

## The Golden Rules

1. **The output does whatever it takes to make the two inputs equal** (when negative feedback is applied).
2. **No current flows into the input pins** (for FET-input op-amps like TL072).
3. **The inputs are at the same voltage** (when the op-amp is in linear operation with negative feedback).

## Pinout (LM358 — Dual Op-Amp)

```
    ┌──────────┐
OutA ┤1       8├── VCC
  -A ┤2       7├── OutB
  +A ┤3       6├── -B
 GND ┤4       5├── +B
    └──────────┘
```

> **See also:** [Comparator](comparator.md) — same pinout but designed for open-loop voltage comparison, not amplification.

## Essential Circuits

### Voltage Follower (Buffer)

```
Input ──┤+
         │  ── Output
    ────┤-
        │
        └── (connected to output)
```

- Gain = 1
- High input impedance, low output impedance
- Use to isolate a high-impedance source (like a sensor) from a low-impedance load (like an ADC)

### Non-Inverting Amplifier

```
Input ──┤+
         │  ── Output
    ────┤-
        │
        ├── R1 ── GND
        │
        R2
        │
        └── Output (feedback)
```

- Gain = 1 + (R2 / R1)
- Input impedance = very high (the op-amp's input impedance)
- **Example:** R1 = 1kΩ, R2 = 10kΩ → Gain = 11

### Inverting Amplifier

```
Input ── R1 ──┤-
               │  ── Output
         ────┤+
              │
         ──── GND (or bias voltage)
         │
         R2 (feedback)
         │
         └── Output
```

- Gain = -R2 / R1
- Input impedance = R1 (not as high as non-inverting)
- Output is inverted — positive input gives negative output
- **Example:** R1 = 1kΩ, R2 = 10kΩ → Gain = -10 (inverts and amplifies 10x)

### Differential Amplifier

```
V1 ── R1 ──┤-
            │  ── Output
V2 ── R3 ──┤+
            │
       R4 ── GND
       │
       R2 (feedback)
       │
       └── Output
```

- Output = (V2 - V1) × (R2 / R1) (when R1/R2 = R3/R4)
- Use for: measuring the difference between two signals (like a current-sense shunt resistor)
- **Must match resistor ratios precisely** for good common-mode rejection

### Summing Amplifier

```
V1 ── R1 ──┤-
V2 ── R2 ──┤-   │
V3 ── R3 ──┤-   │  ── Output
         ────┤+
              │
         ──── GND
         │
         Rf (feedback)
         │
         └── Output
```

- Output = -(V1 × Rf/R1 + V2 × Rf/R2 + V3 × Rf/R3)
- Used in audio mixers, DAC output scaling, signal summing

## Single-Supply Operation

Many hobbyist circuits use a single supply (e.g., 5V or 3.3V) instead of dual supplies (±12V). This changes how you bias the inputs.

### Creating a Virtual Ground

With a single supply, you need to bias the non-inverting input to VCC/2 so the output can swing both above and below the bias point:

```
VCC
  │
  R1 (same value)
  │
  ├─── to op-amp + input
  │
  R2 (same value)
  │
 GND
```

Add a 10µF capacitor from the bias point to GND to keep it stable.

Now signals are AC-coupled (through a capacitor) and biased to VCC/2, and the output swings around VCC/2 instead of ground.

### Rail-to-Rail Op-Amps

Not all op-amps can output all the way to VCC or GND. A **rail-to-rail** op-amp can — useful for single-supply and low-voltage circuits.

| Op-Amp | Rail-to-Rail | Supply | Common Use |
|--------|-------------|--------|-----------|
| LM358 | **No** (output ~1.5V from rails) | 3–32V | General purpose, cheap |
| LM324 | **No** | 3–32V | Quad version of LM358 |
| TL072 | **No** | 7–36V | Audio, low noise, JFET input |
| NE5532 | **No** | 5–22V | Audio, higher current drive |
| MCP6002 | **Yes** | 1.8–6V | 3.3V/5V rail-to-rail |
| MCP6004 | **Yes** | 1.8–6V | Quad, rail-to-rail |
| OPA340 | **Yes** | 2.7–5.5V | Precision rail-to-rail |
| TLV2462 | **Yes** | 2.7–6V | Rail-to-rail, decent speed |

For 3.3V microcontroller projects, use rail-to-rail op-amps (MCP6002, OPA340). The LM358 wastes 1.5V of your output range on each side.

## Common Op-Amp Packages

| Package | Pins | Op-Amps | Typical Part |
|---------|------|---------|-------------|
| DIP-8 | 8 | 1 | TL071, NE5534 |
| DIP-8 | 8 | 2 | LM358, TL072, NE5532 |
| DIP-14 | 14 | 4 | LM324, TL074, MCP6004 |
| SOIC-8 | 8 | 1 or 2 | Surface-mount, same function |

## Op-Amp Selection Guide

| Need | Op-Amp | Why |
|------|--------|-----|
| General purpose, cheap | LM358 | $0.50, dual, 3–32V |
| Audio, low noise | NE5532 | 8 nV/√Hz noise, good for audio |
| Audio, JFET input | TL072 | High input impedance, low noise |
| 3.3V single supply | MCP6002 | Rail-to-rail, 1.8–6V |
| Precision (instrumentation) | AD620 | Single, precision, external resistor sets gain |
| Low power, battery | TLC2272 | CMOS rail-to-rail, low quiescent |
| High speed (>1 MHz) | LM6172 | 100 MHz, fast slew rate |
| High voltage (±15V or more) | OPA604 | 24V supply, audio quality |

## What Op-Amps Can't Do

- **Drive high current** — most op-amps max out at ~20mA. You need a transistor/buffer for motors, speakers, relays.
- **Work open-loop as comparators** — many op-amps oscillate or latch up without feedback. Use an actual comparator chip (LM393) instead.
- **Output rail-to-rail** — unless it's a rail-to-rail model, expect 1–2V of dead zone at each rail.
- **Work at high frequency without care** — stray capacitance on the feedback resistor creates oscillation. Keep feedback resistor below 100kΩ for high-speed circuits.

## Quick Reference

- **Op-amp golden rule:** Output adjusts to make inputs equal (with negative feedback)
- **Negative feedback:** Resistor from output to inverting input — controls gain, reduces distortion
- **No feedback** = comparator mode (unstable for most op-amps)
- **Gain = 1 + R2/R1** for non-inverting, **Gain = -R2/R1** for inverting
- **Bandwidth decreases with gain** — a 1 MHz op-amp at gain 100 only has 10 kHz bandwidth
- **Decouple power pins** — always put a 100nF capacitor from VCC to GND close to the chip
- **Don't leave inputs floating** — connect unused inputs to GND or VCC/2 to prevent oscillation
