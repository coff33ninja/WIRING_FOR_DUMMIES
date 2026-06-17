# Diode — Component Reference

## What It Is

A diode is a **one-way valve for electricity**. Current flows in one direction but not the other.

```
Current flows:   ----→|---→----
No flow:         ----←|---←----
```

## Anode vs Cathode

| Term | Meaning | Where to find it |
|------|---------|-----------------|
| **Anode** | Where current enters | Plain end (no marking) |
| **Cathode** | Where current exits | End with the **stripe** |

```
      ┌──┐                   ┌──────────────────────┐
───→──│▲ │──→───             │                      │
      └──┘                   │                      │────── Cathode
   Anode  Cathode            │                      │        (silver or black stripe)
          (stripe)            └──────────────────────┘
                              ^
                              Anode (plain side)
```

**The rule:** Stripe = cathode. Current flows FROM plain side (anode) TO stripe side (cathode).

## The 6 Diode Types — Which One to Use

### 1. Standard Rectifier (1N400x Series) — Your Daily Driver

| Part | Reverse voltage | Current | Use for |
|------|----------------|---------|---------|
| 1N4001 | 50V | 1A | Low-voltage flyback |
| 1N4004 | 400V | 1A | General purpose |
| **1N4007** | **1000V** | **1A** | **Default choice — flyback, power protection** |
| 1N5408 | 1000V | 3A | Higher-current flyback, power input |

**Best for:** Flyback diodes across motors/fans/relays, reverse polarity protection, general rectification.

**Forward voltage drop:** ~0.7V. At 1A, that's 0.7W of heat — gets warm but survives.

### 2. Schottky Diode (1N581x, SSxx) — Low Drop, Fast

| Part | Reverse voltage | Current | Forward drop |
|------|----------------|---------|-------------|
| 1N5817 | 20V | 1A | 0.32V |
| **1N5819** | **40V** | **1A** | **0.4V** |
| SS34 | 40V | 3A | 0.45V |
| SS54 | 40V | 5A | 0.5V |

**Best for:** Battery-powered circuits (every 0.1V matters), switching power supplies, high-frequency flyback.

**Why use it:** Forward voltage drop is ~0.2–0.4V instead of 0.7V. That's 0.3–0.5V saved — huge for 3.3V circuits.

**Downside:** Higher leakage current than standard diodes, lower reverse voltage (typically ≤100V), more fragile.

### 3. Fast Recovery Diode (FR10x, UF400x) — For Switching

| Part | Reverse voltage | Reverse recovery time |
|------|----------------|---------------------|
| FR107 | 1000V | 500ns |
| **UF4007** | **1000V** | **75ns** |
| HER108 | 1000V | 75ns |

**Best for:** High-frequency rectification (switching power supplies above 50kHz), where standard diodes would overheat.

**Why:** Standard rectifiers are slow — they take microseconds to "turn off." At high frequencies, they can overheat from the switching losses. Fast recovery diodes solve this.

**For hobby projects:** You probably don't need these unless you're building a high-frequency SMPS. Use standard 1N4007 for 99% of hobby work.

### 4. Zener Diode — Voltage Clamp / Reference

Designed to conduct **backward** once voltage hits a specific level. A pressure relief valve.

```
Normal operation (forward):  —→|—  (acts like normal diode)
Breakdown operation (reverse):
  Voltage < Vz:  —←|—  (blocks, tiny leakage)
  Voltage = Vz:  —←|→  (conducts, clamps voltage)
```

| Part | Zener voltage | Use for |
|------|--------------|---------|
| 3.3V zener (1N4728) | 3.3V | Clamping 5V to 3.3V, ESP32 input protection |
| 5.1V zener (1N4733) | 5.1V | Making a 5V reference rail |
| 12V zener (1N4742) | 12V | Overvoltage protection for 12V inputs |

**Best for:** Overvoltage protection (clamp a signal before it reaches your GPIO), creating a simple voltage reference, input protection on power lines.

**Wiring for GPIO protection:**
```
5V signal ──┬── 1kΩ ──┬── ESP32 GPIO
            │         │
           3.3V       │
           zener      │
            │         │
           GND       GND
```
If the signal goes above 3.3V, the zener conducts and shunts it to ground.

### 5. Signal Diode (1N4148, 1N914) — Small Signals

| Part | Current | Voltage | Speed |
|------|---------|---------|-------|
| **1N4148** | 200mA | 100V | 4ns (very fast) |
| 1N914 | 200mA | 100V | 4ns |

**Best for:** Low-current flyback (small relays <200mA), logic-level protection, signal clamping.

**Don't use for:** High-current flyback (motors, fans), power rectification, reverse polarity protection.

### 6. TVS Diode (Transient Voltage Suppression) — Surge Protection

A beefed-up zener designed to absorb large energy spikes (lightning, inductive kickback):

| Part | Standoff voltage | Peak power | Use for |
|------|-----------------|------------|---------|
| P6KE6.8A | 5.8V | 600W | 3.3V/5V power input protection |
| P6KE12A | 10.2V | 600W | 12V power input protection |
| 1.5KE24A | 20.5V | 1500W | 24V industrial protection |
| SMAJ5.0A | 5V | 400W | SMD, USB power protection |

**Best for:** Power input protection (the first thing after the power jack), ESD protection, lightning surge protection.

**Where it goes:**
```
Power In ───── [fuse] ──── TVS ──── GND
                                  │
                               [circuit]
```
The TVS sits across the power rail. If a spike exceeds its threshold, it short-circuits the spike to ground.

## Quick Selection Guide

| Job | Part | Why |
|-----|------|-----|
| Flyback diode on fan/motor | **1N4007** | Cheap, handles the spike, 1A is enough |
| Flyback on small relay (<200mA) | **1N4148** | Smaller, faster, good enough |
| Reverse polarity protection | **1N4007 or SS34** | 1N4007 is cheap; SS34 wastes less voltage |
| Battery-powered protection | **1N5819 Schottky** | 0.4V drop instead of 0.7V — saves battery |
| GPIO overvoltage clamp | **3.3V zener** | Hard-clamps input to safe voltage |
| Power supply input surge | **P6KE series TVS** | Absorbs lightning/load-dump spikes |
| High-frequency rectifier | **UF4007** | Fast recovery, doesn't overheat |
| Signal/logic protection | **1N4148** | Fast, small signal |

## Forward Voltage by Type

| Diode type | Forward drop (Vf) | At current |
|-----------|-------------------|------------|
| Schottky (1N5819) | 0.25–0.4V | 100mA–1A |
| Standard rectifier (1N4007) | 0.7–1.0V | 100mA–1A |
| Fast recovery (UF4007) | 1.0–1.4V | 100mA–1A |
| Signal (1N4148) | ~0.7V | 10mA |
| Zener (in forward) | ~0.7V | Same as standard |

> **The 0.7V rule:** Most silicon diodes drop ~0.7V when conducting. Schottky drops ~0.3V. This matters for battery projects — two Schottkys in series lose 0.6V, two standard lose 1.4V.

## What Happens If You Use the Wrong Type

| Mistake | Result |
|---------|--------|
| 1N4148 for motor flyback | Diode dies from overcurrent — then MOSFET dies from spike |
| 1N4007 in high-frequency (>50kHz) supply | Diode overheats — switching losses too high |
| Standard diode where Schottky was needed | Wastes 0.3V — battery dies faster, circuit may not work at low voltage |
| Zener instead of TVS for surge | Zener dies — it's not designed for high-energy pulses |
| TVS instead of Zener for reference | Poor regulation — TVS is not precise enough for voltage reference |
| Reversed diode in circuit | Dead short (if power path) or no current flow (if signal path) |

## Quick Reference

```
Polarity:  Stripe = cathode (exit). Plain side = anode (entry).

Flyback (motor/fan/relay):   1N4007 (default) or 1N5819 (battery)
Signal / relay <200mA:       1N4148
Reverse polarity protection: 1N4007 or SS34 (low drop)
Overvoltage clamp:           Zener (precision) or TVS (surge)
High-frequency rectifier:    UF4007 (fast recovery)

Forward voltage rule:
  Schottky = 0.3V
  Standard = 0.7V
  Fast recovery = 1.0–1.4V

Part numbers:
  1N4007   = 1A, 1000V, standard        (flyback king)
  1N4148   = 200mA, 100V, signal        (small stuff)
  1N5819   = 1A, 40V, Schottky          (low drop)
  UF4007   = 1A, 1000V, fast recovery   (high frequency)
  1N4733   = 5.1V zener                 (voltage clamp)
  P6KE6.8A = 6.8V TVS                   (surge protection)
```
