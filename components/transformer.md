# Transformer — Component Reference

## What It Is

A transformer transfers electrical energy between two circuits using **magnetic induction**. It converts AC voltage from one level to another — higher or lower — with no moving parts.

```
Primary coil     Secondary coil
┌────────┐       ┌────────┐
│  N₁    │       │  N₂    │
│ turns  │───────│ turns  │
│        │   →   │        │
│  AC in │   ←   │ AC out │
└────────┘       └────────┘
   Iron core (laminated)
```

The key principle: a changing current in the primary coil creates a changing magnetic field in the core, which induces a voltage in the secondary coil.

**Transformers ONLY work with AC (alternating current).** DC produces a steady magnetic field that doesn't induce anything — and can burn out the transformer.

## How Voltage and Current Scale

The turns ratio determines everything:

```
V₂ / V₁ = N₂ / N₁    (voltage ratio = turns ratio)
I₂ / I₁ = N₁ / N₂    (current ratio = inverse turns ratio)
```

- N₁ = number of turns on primary coil
- N₂ = number of turns on secondary coil

### Examples

| Turns Ratio | Input | Output | Type |
|-------------|-------|--------|------|
| 10:1 | 120V AC | 12V AC | Step-down (wall wart) |
| 1:10 | 12V AC | 120V AC | Step-up |
| 1:1 | Any | Same voltage | Isolation transformer |
| Center-tapped | 120V AC | 12V-0-12V AC | Split supply |

**Power stays the same** (minus losses): V₁ × I₁ ≈ V₂ × I₂. If you step voltage down by 10x, current goes up by 10x.

### Real Example

A 12V, 1A transformer (12VA):
- Primary: 120V, 0.1A
- Secondary: 12V, 1A
- Turns ratio: 120/12 = 10:1

## Types of Transformers

### Power Transformer (Standard)

The classic iron-core transformer found in wall adapters and power supplies.

- **Frequency:** 50/60 Hz mains
- **Core:** Laminated silicon steel (reduces eddy current losses)
- **Power range:** 1 VA to 1000+ VA
- **Efficiency:** 85–95%
- **Regulation:** Output voltage changes with load (5–15% drop from no-load to full-load)

### Toroidal Transformer

Donut-shaped transformer — the core is a rolled steel strip.

- **Lower magnetic field leakage** — less hum, less interference
- **More efficient** than EI-core (95%+)
- **Physically smaller** for same power rating
- **More expensive** than EI-core
- **Inrush current on startup** can trip breakers

Used in: audio amplifiers, medical equipment, sensitive electronics.

### Center-Tapped Transformer

Secondary has a third wire at the exact middle of the winding — gives two equal voltages:

```
120V ─┬── Primary ──┬── 12V ──┬── 0V (center tap)
      │              │         │
      └──────────────┘  └── -12V
```

Used for: split-rail power supplies (±12V, ±5V), full-wave rectifiers (two diodes instead of four).

### Isolation Transformer

1:1 ratio — input and output are at the same voltage but **galvanically isolated**.

- **No direct electrical connection** between primary and secondary
- Used for: safety (isolating equipment from mains), breaking ground loops, oscilloscope safety
- **Does NOT protect from shock** — the secondary can still kill you at 120V

### Flyback Transformer (CRT / High Voltage)

Special transformer that stores energy in the core during the "on" pulse and releases it during the "off" pulse.

- Used in: CRT TVs (generates 15–30kV), flash chargers, boost converters
- **Not interchangeable with power transformers** — designed for high-frequency square waves

## Identifying Transformer Pins

Transformers don't follow a standard pinout. Check the datasheet or measure:

1. **Measure resistance** between pairs of pins.
2. **Primary winding** has higher resistance (more wire turns). 120V primary: ~10–100Ω.
3. **Secondary winding** has lower resistance. 12V secondary: ~0.5–5Ω.
4. **Center tap** — three-pin secondary: the center pin connects to both outer pins.
5. **Some transformers have dual primaries** (for 120V/240V switching) — two wires in series for 240V, parallel for 120V.

### Dual Primary Wiring

```
For 120V:      For 240V:
Primary A ────  Live         Primary A ────  Live
Primary B ────  Neutral      Primary B ────  Neutral
                              │
                         (jumper between the other ends of A and B)
```

Check the datasheet — some dual-primary transformers have 4 primary pins and you wire them in series or parallel.

## Wiring a Transformer

### Basic AC-to-AC

```
Mains ── fuse ── primary ── mains neutral
                 secondary ── AC load
```

### AC-to-DC (Rectified)

```
Mains ── transformer ── bridge rectifier ── filter cap ── voltage regulator ── DC out
                                    │
                                    └─── GND
```

**NEVER power a transformer primary from a DC source.** It will draw excessive current and burn out.

## Safety — VERY IMPORTANT

**Transformers connected to mains electricity can kill you.** Follow these rules:

1. **Fuse the primary** — always. A fuse on the primary protects against transformer failure and shorts. Rating: 1.5–2x the expected primary current.
2. **Use an enclosure** — never operate a mains-connected transformer in the open.
3. **Insulate all connections** — heatshrink, tape, or terminal blocks.
4. **Check isolation** — measure resistance between primary and secondary with a multimeter. It should be infinite (open circuit).
5. **Don't exceed VA rating** — the transformer will overheat and fail.
6. **Secondary can still shock you** — a 12V secondary at 10A can cause serious burns.
7. **Use a GFCI** when testing mains circuits.

## Transformer vs Switched-Mode Power Supply (SMPS)

| | Transformer (Linear) | SMPS (Switching) |
|--|--------------------|------------------|
| Size/weight | Large and heavy | Small and light |
| Efficiency | 70–85% | 80–95% |
| Output noise | Clean (no high-frequency noise) | Ripple + HF noise |
| Regulation | Poor (voltage drops with load) | Excellent (regulated output) |
| Complexity | Simple (just windings) | Complex (controller IC, MOSFETs, feedback) |
| Cost | Cheap at low power | Cheaper at high power |
| EMI | Low (50/60 Hz only) | High (switching frequency harmonics) |
| Isolation | Natural (windings separate) | Needs optocoupler or separate transformer |

**Use a transformer when:** You need clean, low-noise DC (audio, measurement), you want simplicity and reliability, or you're building a linear power supply.

**Use an SMPS when:** Size/weight matters, efficiency matters, you need regulated output over a wide input range.

## Common Transformer Ratings

| VA Rating | Typical 12V Secondary | Use For |
|-----------|----------------------|---------|
| 3 VA | 250 mA | Small loads, relays, one sensor |
| 6 VA | 500 mA | Microcontroller + a few LEDs |
| 12 VA | 1 A | Arduino + sensors + small motor |
| 24 VA | 2 A | Multiple microcontrollers |
| 50 VA | 4 A | Bench power supply |
| 100 VA | 8 A | Audio amplifier, large project |

The VA (Volt-Amp) rating is the maximum power the transformer can deliver continuously. A 12VA transformer at 12V can deliver 1A continuous.

## Quick Reference

- **AC only** — transformers do NOT work with DC
- **Turns ratio** = voltage ratio (e.g., 10:1 = 120V→12V)
- **Current inversely scales** with voltage
- **Power rating in VA** = V × I (maximum continuous)
- **No-load voltage is higher** — expect 15–20% above rated voltage with no load
- **Fuse the primary** — always, for safety
- **Bridge rectifier + capacitor** turns AC output into DC
- **Output ripple** = 100/120 Hz (2× mains frequency) after rectification
- **Use a center-tapped transformer** for split-rail supplies (±12V)
- **Use a toroidal transformer** for low magnetic interference (audio, sensitive circuits)
- **Keep away from audio circuits** — the 50/60 Hz magnetic field induces hum
