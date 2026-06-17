# Load Cell + HX711 — Component Reference

## What It Is

A **load cell** is a sensor that converts force (weight) into an electrical signal. The **HX711** is a 24-bit ADC specifically designed to read load cells. Together they're the standard way to add weight measurement to any project.

## How a Load Cell Works

Inside a load cell, there are **strain gauges** arranged in a **Wheatstone bridge**:

```
    VCC (excitation)
       │
    ┌──┴──┐
    │ R1  │ R2
    │     │
    └──┬──┘
       │
    ┌───┴───┐
    │ Signal│ ← Differential output (mV)
    └───┬───┘
       │
    ┌──┴──┐
    │ R3  │ R4
    │     │
    └──┬──┘
       │
      GND
```

When force is applied, the strain gauges change resistance (R1/R4 increase, R2/R3 decrease), unbalancing the bridge. The output is a tiny differential voltage — typically **1–2 mV per volt of excitation** at full load.

A 5kg load cell with 5V excitation produces ~5–10mV at 5kg. That's too small for a microcontroller ADC — you need the HX711 amplifier.

## Load Cell Types

| Type | Shape | Wiring | Best for |
|------|-------|--------|----------|
| Straight bar (parallel beam) | Rectangular bar | 4-wire | Kitchen scales, general purpose |
| Single point | Flat disc with hole | 4-wire | Platform scales, luggage scales |
| S-type | S-shaped | 4-wire | Hanging scales, tension measurement |
| Compression (pancake) | Flat cylinder | 4-wire | High-force, industrial |
| Bending beam | Long bar, bolted one end | 4-wire | Tank/hopper weighing |

### Color Codes (Wiring)

| Wire | Typical color | Purpose |
|------|--------------|---------|
| Red | Red | Excitation+ (E+) |
| Black | Black | Excitation- (E-) |
| White | White | Signal+ (S+, A+) |
| Green or Blue | Green | Signal- (S-, A-) |

Colors vary by manufacturer. Check the datasheet or use a multimeter to identify pairs.

## HX711 Module

The HX711 is a **24-bit differential ADC** with a programmable gain amplifier. It communicates via a simple 2-wire interface (clock + data).

### Pinout

```
HX711 module       Microcontroller
  VCC ────────────── 3.3V or 5V
  GND ────────────── GND
  SCK ────────────── GPIO (clock)
  DT ─────────────── GPIO (data)
```

### Wiring to Load Cell

```
Load cell           HX711 module
  Red (E+) ────────── E+
  Black (E-) ──────── E-
  White (S+) ──────── A+ (or S+)
  Green (S-) ──────── A- (or S-)
```

## Wiring Diagram

```
Load Cell
  Red ──── E+ ──┐
  Black ─── E- ──┤
  White ─── A+ ──┤  HX711
  Green ─── A- ──┤          SCK ──── GPIO
                 │          DT  ──── GPIO
                 │          VCC ──── 3.3V/5V
                 │          GND ──── GND
                 └──────────
```

## HX711 Gain Settings

| Gain | Use | Input range |
|------|-----|-------------|
| 128 (default) | Standard load cell, ±20mV | ±20mV differential |
| 64 | Weaker signals | ±40mV differential |
| 32 (Channel B) | Second input | ±80mV differential |

Channel A (pins A+ and A-) is typically used. Channel B is a separate input at 32x gain.

## Library

Use the **HX711 Arduino Library** (bogde):

```cpp
#include "HX711.h"
HX711 scale;

void setup() {
  scale.begin(DOUT_PIN, SCK_PIN);
  scale.set_scale();       // set calibration factor
  scale.tare();            // zero the scale
}

void loop() {
  float weight = scale.get_units(10); // average 10 reads
  Serial.println(weight);
}
```

## Calibration

Without calibration, the readings are meaningless raw counts. Calibration maps counts to real-world weight:

1. **Tare:** Put nothing on the scale, call `scale.tare()`
2. **Reference:** Place a known weight (e.g., 1kg) on the scale
3. **Calculate factor:** `scale.get_units(10)` without a scale set → get raw counts, divide by known weight
4. **Set factor:** `scale.set_scale(calculated_factor)`

Store the calibration factor in EEPROM so you don't have to recalibrate every power-up.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Reading stuck at -1 or max | HX711 not communicating | Check SCK and DT wiring, power |
| Reading doesn't change with weight | Load cell not wired correctly | Check color code, swap A+ and A- |
| Reading drifts over time | Temperature change, or air currents | Add enclosure, average more readings |
| Reading noisy | Power supply noise | Add 100µF cap across HX711 VCC/GND |
| Negative values after tare | Load cell compressed when tared | Don't press on sensor during tare |
| Non-linear readings | Load applied off-center | Use proper mounting hardware |

## Mechanical Mounting

A load cell must be mounted correctly:

```
    ││  ← Force
    ││
  ┌─┴──────┴─┐
  │  Load    │  ← Platform (attached to free end)
  │  Cell    │
  │          │
  ├──────────┤
  │          │  ← Base (attached to fixed surface)
  └──────────┘
```

- One end must be fixed, the other free to bend
- Don't bolt both ends down — the sensor won't flex and reads nothing
- Use the mounting holes provided (don't drill new ones through the strain gauge area)

## Quick Reference

- **Load cell:** 4-wire Wheatstone bridge, outputs ~1–2 mV/V
- **HX711:** 24-bit ADC + amplifier, reads load cell directly
- **Wiring:** Red=E+, Black=E-, White=A+, Green=A- (verify colors)
- **Interface:** 2-wire (SCK, DT) — any GPIO pins
- **Gain:** 128 (default), use 64 for weaker signals
- **Calibration:** Tare → known weight → calculate factor
- **Mounting:** One end fixed, one end free
- **Filter:** Average multiple readings + add capacitor for noise
