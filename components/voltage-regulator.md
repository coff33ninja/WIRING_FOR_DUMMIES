# Voltage Regulator — Component Reference

## What It Is

A voltage regulator takes an input voltage (which can fluctuate) and outputs a **steady, fixed voltage** regardless of what's happening on the input. Think of it like a **surge protector + filter for your power** — the input might be noisy or varying, but the output stays clean.

> **Why you need one:** A 12V supply will destroy a 3.3V ESP32. A battery might be 4.2V when full and 3.0V when empty. Sensors give different readings if voltage changes. You need a regulator.

## Linear vs Switching (Buck)

| Type | How it works | Efficiency | Heat | Noise | Use |
|------|-------------|------------|------|-------|-----|
| **Linear** (7805, AMS1117) | Burns off extra voltage as heat | ~30–60% | Hot | Very clean | Small loads, audio, sensors |
| **Switching** (buck converter module) | Turns on/off rapidly to average down voltage | 85–95% | Cool | Some ripple | Motors, LED strips, big loads |

### Linear Regulators — Simple but Wasteful

```
Input:  12V ──→ [7805] ──→ 5V output
                     │
                    GND

Power wasted = (12V - 5V) × 1A = 7 watts of heat!
That's why the 7805 needs a heatsink.
```

**Rule of thumb:** If the input voltage is more than 2× the output voltage, or the current is over 100mA, use a switching regulator instead.

### Switching (Buck) Converters — Efficient but More Parts

A buck converter uses a MOSFET to rapidly switch the input voltage on and off, then a capacitor smooths it back to a lower DC voltage. The efficiency comes from the MOSFET being either fully on or fully off — it never sits in the "waste heat" zone.

```
Input: 12V ──→ [Buck Converter Module] ──→ 3.3V output
              LM2596 / MP1584 / etc.
```

**Pre-built modules** (LM2596, Mini360, etc.) are cheap and easy. Just set the output voltage with a screwdriver and a multimeter.

## Common Regulators

| Part | Type | Output | Max Input | Max Current | Use |
|------|------|--------|-----------|-------------|-----|
| 7805 | Linear | 5V | 35V | 1A | Classic 5V regulator (needs heatsink) |
| 7812 | Linear | 12V | 35V | 1A | Regulating 12V from higher supply |
| AMS1117-3.3 | Linear | 3.3V | 15V | 1A | Common ESP32 voltage reg |
| AMS1117-5.0 | Linear | 5V | 15V | 1A | Arduino Uno's regulator |
| LM2596 | Buck | Adjustable | 40V | 3A | Pre-built modules, adjustable |
| Mini360 (MP1584) | Buck | Adjustable | 28V | 2A | Tiny, cheap buck module |

## Input and Output Capacitors — Not Optional

Linear regulators need capacitors on both input and output to **prevent oscillation**. Without them, the regulator can "hunt" (rapidly go up and down) and produce noisy voltage or even damage itself.

| Regulator | Input cap | Output cap |
|-----------|-----------|------------|
| 7805 | 330nF or 10µF | 100nF or 10µF |
| AMS1117 | 10µF (tantalum/electrolytic) | 22µF (tantalum/electrolytic) |
| LM2596 module | (usually built-in) | (usually built-in) |

> **Skipping input/output caps on a linear regulator:** The output voltage may oscillate, buzz at audible frequencies, or drift. Your microcontroller resets randomly.

## LDO (Low Drop-Out) Regulators

A standard 7805 needs about 2V more on the input than the output (the "dropout voltage"). So for 5V out, you need at least 7V in.

**LDO regulators** (like AMS1117) only need about 1V of headroom — so 4.3V input can give 3.3V output. This is crucial for battery-powered projects where the battery drops close to the output voltage.

## Heat Dissipation

Every linear regulator converts excess voltage into heat. The formula:

```
P = (Vin - Vout) × I

Example: 12V to 5V at 500mA
P = (12 - 5) × 0.5 = 3.5 watts → needs heatsink!
```

If the regulator gets too hot to touch (>60°C or so), add a heatsink or switch to a buck converter.

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| No regulator at all | Apply 12V directly to ESP32 → ESP32 dies instantly |
| No input/output caps | Regulator oscillates, output voltage wobbles → crashes |
| No heatsink (high current) | Regulator overheats → thermal shutdown → restarts → cycles forever |
| Undersized regulator | Regulator overheats, voltage drops, microcontroller browns out |

## Quick Reference

```
For 5V (Arduino, etc.):
  12V → [7805 + caps + heatsink] → 5V
  Or:  12V → [LM2596 buck (set to 5V)] → 5V (better)

For 3.3V (ESP32, etc.):
  5V  → [AMS1117-3.3 + caps] → 3.3V
  12V → [LM2596 buck (set to 3.3V)] → 3.3V (better)

Pre-built buck converter modules are cheap and easy:
  - Set output voltage with multimeter + screwdriver
  - Most handle 12V→3.3V at 1-2A without overheating
  - Already have input/output caps built in
```
