# Buck-Boost Converter — Component Reference

## What It Is

A **buck-boost converter** takes a DC voltage and can either **step it up or step it down** automatically. If the input is higher than the output, it bucks. If the input is lower than the output, it boosts. This makes it ideal for battery-powered projects where the battery voltage starts above and drops below the target.

## When You Need One

| Situation | What happens | Solution |
|-----------|-------------|----------|
| 3.7V Li-ion → 5V USB | Battery is 4.2V (full) to 3.0V (dead) | 4.2→5V = boost, 3.0→5V = boost (needs boost only) |
| 3.7V Li-ion → 3.3V MCU | 4.2V → 3.3V = buck, 3.0V → 3.3V = boost | **Buck-boost** (voltage crosses the target) |
| 12V battery → 5V MCU | 12V is always above 5V | Buck only |
| Solar panel → battery | Panel voltage varies above and below battery | Buck-boost or SEPIC |

**The key case:** A single Li-ion cell powering a 3.3V circuit. Full battery is 4.2V (> 3.3V, buck needed). Dead battery is 3.0V (< 3.3V, boost needed). A simple buck or boost converter alone won't work — you need buck-boost.

## How It Works

A buck-boost converter inverts the input voltage:

```
Buck-boost topology:
   ┌───────┐
   │ Switch│
   │       │
   +─┤├────┼── + ────┬── Capacitor ──── Vout
     Inductor        │
     Storage        Diode
       │             │
       └─────────────┴── GND
```

- **Buck mode:** Switch operates in buck configuration (input > output)
- **Boost mode:** Switch operates in boost configuration (input < output)
- **Transition:** Smooth, automatic — no glitch at the crossover point

## Common Modules

### LM2577 / LM2586 (Boost + Separate Buck)

Not true buck-boost. These need two separate stages.

### MT3608 (Boost Only)

Popular for boosting 3.7V → 5V or 12V. **Not buck-boost** — input must always be below output.

```
MT3608 Boost:
  IN ── 2–24V    OUT ── up to 28V (Vin × (1-D))
  Always Vin < Vout
```

### SX1308 (Boost Only)

Similar to MT3608, slightly higher current capability.

### TPS63000 / TPS63060 (True Buck-Boost)

| Part | Max current | Input range | Output |
|------|-------------|-------------|--------|
| TPS63000 | 1.2A (buck), 1A (boost) | 1.8–5.5V | 3.3V fixed / adjustable |
| TPS63060 | 2.3A (buck), 1.8A (boost) | 2.5–12V | 5V fixed / adjustable |

True buck-boost IC. Very common in Li-ion → 3.3V applications.

### LTC3588 / LTC3530 / TPS63020

Higher-end buck-boost controllers for specific applications (energy harvesting, high efficiency).

### Cheap "Buck-Boost" Modules (the ones labeled "Buck-Boost")

Many modules labeled "buck-boost" are actually **SEPIC** converters (similar behavior but different topology). The practical difference is minimal for hobby use.

## Wiring

```
Buck-Boost module     Battery / Input
  IN+ ─────────────────── Positive
  IN- ─────────────────── Negative (GND)

  OUT+ ────────────────── Load positive (3.3V, 5V, etc.)
  OUT- ────────────────── Load negative (GND)

  Adjust pot ──────────── Adjust output voltage (multi-turn trimmer)
```

### Potentiometer Adjustment

The output voltage is set by a trimmer potentiometer on the module:

- **Clockwise:** Increases voltage
- **Counter-clockwise:** Decreases voltage

Always measure the output **with a load** before connecting your project. Some modules output a higher voltage without load.

## Efficiency

| Condition | Typical efficiency |
|-----------|-------------------|
| Buck mode (Vin > Vout) | 85–95% |
| Boost mode (Vin < Vout) | 80–90% |
| Near crossover (Vin ≈ Vout) | 70–80% (worst case) |

True buck-boost converters are less efficient than dedicated buck or boost converters at the same voltage ratio. If your input voltage is always above the output, use a buck converter instead. Same for always-below — use a boost.

## Ripple and Noise

Switching converters produce **output ripple** — small voltage fluctuations at the switching frequency:

| Converter type | Ripple | Typical switching frequency |
|---------------|--------|---------------------------|
| Buck-boost | Higher than buck | 500 kHz – 2.4 MHz |
| Buck | 5–50 mV p-p | 100–500 kHz (higher if synchronous) |
| Boost | 20–100 mV p-p | 300 kHz – 1 MHz |

**For sensitive circuits (analog, audio):** Add a linear regulator (LDO) after the buck-boost. The LDO's PSRR (Power Supply Rejection Ratio) filters out the ripple.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Output voltage too low | Potentiometer not adjusted | Turn clockwise while monitoring output |
| Output voltage too high | Potentiometer over-adjusted | Turn counter-clockwise |
| No output | Input voltage too low | Check minimum input voltage (usually 2.5V minimum) |
| Module gets hot | Load too high, or poor heat dissipation | Add heatsink, reduce load, or use higher-rated module |
| Audible whine | Ceramic capacitors vibrating (piezoelectric effect) | Add electrolytic cap on output, or use different module |
| Output voltage unstable | Input source can't supply enough current | Check battery health, use thicker wires |
| Battery drains fast | Converter efficiency poor at light load | Use a module with power-save mode at low current |
| Module fails near crossover | Large current demand at buck-boost transition | Use higher-rated module or add bulk capacitance |

## Buck-Boost vs SEPIC

| Feature | Buck-Boost | SEPIC |
|---------|-----------|-------|
| Output polarity | Inverted (Vout negative relative to GND) | Non-inverted (Vout positive relative to GND) |
| Components | 1 inductor, 1 switch, 1 diode | 2 inductors (or 1 coupled), 1 switch, 1 diode |
| Efficiency | Similar | Similar |
| Common in modules | Marked as "buck-boost" even when SEPIC | Often labeled "buck-boost" |

Most hobby modules labeled "buck-boost" are actually SEPIC converters (they output a positive voltage). The inverted-output true buck-boost is rare in ready-made modules.

## Quick Reference

- **Buck-boost:** Output can be above, below, or equal to input voltage
- **Key use case:** Li-ion battery (4.2V→3.0V) powering 3.3V circuit
- **For always-above:** Use buck converter (more efficient)
- **For always-below:** Use boost converter (more efficient)
- **True buck-boost:** TPS63000, TPS63060, LTC3530
- **Cheap modules:** Often SEPIC topology labeled as "buck-boost"
- **Adjust output:** Trimmer pot, measure with load before connecting project
- **Ripple:** Higher than simple buck/boost. Add LDO for sensitive circuits.
- **Crossover efficiency:** Worst case (~75%). Keep Vin away from Vout if possible.
- **Efficiency:** 80–95% depending on input/output ratio.
