# Comparator (LM393) — Component Reference

> **See also:** [Op-Amp](op-amp.md) — same pinout, different function. Don't confuse them.

## What It Is

A comparator compares two voltages and outputs a digital HIGH or LOW depending on which is larger. It's like a 1-bit ADC — you set a reference voltage and it tells you whether the input is above or below that threshold.

```
Input A ──┤\
           │  >── Output (HIGH if A > B, LOW if A < B)
Input B ──┤/
```

The LM393 is the most common hobbyist comparator. It has **two comparators in one 8-pin DIP package**, open-collector outputs, and works from 2V to 36V.

## Pinout (LM393)

```
    ┌──────────┐
OutA ┤1       8├── VCC
  -A ┤2       7├── OutB
  +A ┤3       6├── -B
 GND ┤4       5├── +B
    └──────────┘
```

Each comparator has:
- **+ (non-inverting input)** — pin 3 (A), pin 5 (B)
- **- (inverting input)** — pin 2 (A), pin 6 (B)
- **Output** — pin 1 (A), pin 7 (B)
- **Open-collector** — output sinks current to GND when active, floats when inactive. You need a pull-up resistor (typically 10kΩ) to VCC on each output.

## Open-Collector Output — Why It Matters

The LM393 output is not a push-pull like a logic gate. It can only pull LOW (to GND). When it wants to output HIGH, it disconnects (high impedance). This means:

- **You MUST have a pull-up resistor** (1k–10kΩ) from the output pin to your logic voltage (3.3V or 5V).
- You can connect multiple comparator outputs to the same wire (wired-AND) — if any pulls low, the line goes low.
- You can pull up to a DIFFERENT voltage than the comparator's VCC — useful for level shifting (e.g., 5V comparator feeding a 3.3V microcontroller).

## Basic Circuits

### Light/Dark Detector (Light Threshold)

```
VCC ──┬── LDR (10k–100k)
      │
      ├───────────────────────┐
      │                       │
      │                  ┌────┤+
      │                  │    │  LM393
      │                  │    ├── OUT ──┬── 10kΩ ── VCC
      └── 10kΩ ── GND   │    │         │
                         │    └────     └── to GPIO
                         │  GND
                         │
                     10kΩ pot ── VCC
                       (set threshold)
```

When light level crosses the pot threshold, output flips. The pot adjusts sensitivity.

### Temperature Switch (with NTC)

Replace the LDR with an NTC thermistor + fixed resistor voltage divider. Same circuit — comparator flips when temperature crosses the pot threshold.

### Zero-Crossing Detector (AC)

```
AC (step-down to ~6V) ──┤+
                         │  LM393 ── to microcontroller (detect AC zero cross)
                    GND ─┤-
```

Used for dimmers, phase control, and timing AC cycles.

## Hysteresis — The Hidden Gotcha

Without hysteresis, a comparator oscillates wildly when the input voltage is near the threshold. Even tiny noise makes it flip on and off thousands of times per second.

Add positive feedback (a resistor from output to the + input) to create hysteresis — a dead zone where the output doesn't change:

```
Vref ──┬── 10kΩ ──┤+
                  │  LM393 ── output
Input ── 10kΩ ──┤-
                 │
                 └── 100kΩ ── output (feedback resistor)
```

The 100kΩ feedback resistor creates a ~50mV hysteresis band. The output won't flip until the input crosses Vref + 25mV going up or Vref - 25mV going down. Adjust the resistor to widen or narrow the band.

## LM393 vs LM311 vs LM339

| Part | Package | Channels | Notes |
|------|---------|----------|-------|
| LM393 | 8-pin DIP | **2** | Most common for hobbyists |
| LM311 | 8-pin DIP | **1** | Higher speed, can drive loads up to 50V |
| LM339 | 14-pin DIP | **4** | Quad comparator, same pinout as LM324 op-amp |
| LM393N | 8-pin DIP | **2** | Same part, N suffix = standard |

## When to Use a Comparator vs Op-Amp

| | Comparator | Op-Amp |
|--|-----------|--------|
| Output | Digital (HIGH/LOW) | Analog (continuous) |
| Speed | Fast (typically 1µs) | Slower (compensated for stability) |
| Hysteresis | External (optional) | Don't typically use it |
| Feedback | For hysteresis only | For gain control |
| Open-loop | **Designed for it** | Unstable (oscillates) |
| Saturation | Output hits rails hard | Gradual |

**DO NOT use an op-amp as a comparator** unless the datasheet explicitly says it's OK. Many op-amps oscillate or latch up when run open-loop. Use a comparator chip instead.

## Wiring Summary

| Pin | Connect to |
|-----|-----------|
| VCC (8) | 5V (or 2–36V supply) |
| GND (4) | Common ground |
| + input | Your signal (or reference) |
| - input | Your reference (or signal) |
| Output | 10kΩ pull-up to logic voltage → GPIO |

## Quick Reference

- **LM393** = dual comparator, open-collector output
- **Always use a pull-up** on the output (10kΩ is safe)
- **Add hysteresis** (100kΩ feedback) when comparing a noisy signal
- **Supply voltage** 2–36V, but output pull-up sets your logic level
- **Output sinks** current when active (LOW), floats when inactive (HIGH via pull-up)
- **Max sink current** ~20mA (enough for an LED directly from output)
