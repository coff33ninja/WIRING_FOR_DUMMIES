# Power & Batteries — Supply Guide

> **See also:** [Batteries & Cell Chemistries](/fundamentals/batteries) — detailed comparison of all battery types, chemistries, and charging profiles.

## What This Covers

Choosing the right power source — wall adapter, USB, battery — is the first thing you do in any project. The wrong choice means brownouts, resets, fires, or a project that's tethered to a wall when it should be portable.

## Wall Adapters (AC-DC)

### Voltage and Current Ratings

Every wall adapter (wall wart, power brick) has two numbers:

| Rating | What it means | Rule |
|--------|---------------|------|
| **Output voltage** (e.g., 5V, 9V, 12V) | What voltage it delivers | **Must match your circuit's voltage requirement** |
| **Output current** (e.g., 1A, 2A, 3A) | Maximum current it can supply | **Must be ≥ what your circuit draws** |

### A 2A Adapter Won't Overpower a 500mA Circuit

This is the most misunderstood rule: **The circuit draws what it needs, not what the supply can deliver.** A 5V 10A adapter connected to an ESP32 (which draws 300mA) is fine — the ESP32 draws 300mA and the adapter sits there with 9.7A of headroom.

The reverse — a 500mA adapter trying to power a 2A circuit — is where things fail. The adapter overheats, voltage droops, and the circuit browns out or the adapter dies.

```
Circuit draws 300mA  →  5V 1A adapter  →  OK (plenty of headroom)
Circuit draws 2A     →  5V 1A adapter  →  NOT OK (overload)
```

**Rule:** Pick an adapter rated for at least 1.5× your circuit's maximum current draw.

### Barrel Jack Polarity

Barrel jacks (the round power connectors) come in two polarities. **Using the wrong one can destroy your project.**

```
Center Positive (most common):      Center Negative (rare — older devices):
   ┌────┐                              ┌────┐
   │ ═══│                              │ ═══│
   └────┘                              └────┘
   (+) · (−)                            (−) · (+)
  Center = +                          Center = −
```

**Always check the polarity symbol on the adapter and your device.** The symbol looks like this:

```
Center-positive:      Center-negative:
   (+)  (−)              (−)  (+)
   ═══ ═══               ═══ ═══
```

> **Most hobby modules use center-positive.** But cheap devices sometimes reverse it. Verify with a multimeter before plugging in.

### Sizes

| Barrel size (OD × ID) | Common use |
|----------------------|------------|
| **5.5mm × 2.1mm** | **Most common — Arduino, Raspberry Pi, breadboards** |
| 5.5mm × 2.5mm | Larger — some laptops, audio gear |
| 3.5mm × 1.35mm | Smaller — older devices, some modules |

> **2.1mm and 2.5mm ID are visually similar.** A 2.5mm plug fits loosely in a 2.1mm jack (intermittent). A 2.1mm plug won't fit in a 2.5mm jack.

## USB Power

USB is 5V (by spec) but the available current depends on the source:

| USB type | Max current | Voltage | Notes |
|----------|-------------|---------|-------|
| USB 2.0 (computer port) | 500mA | 4.75–5.25V | May shut down if you draw more |
| USB 3.0 | 900mA | 4.75–5.25V | Same — don't exceed |
| USB-C (phone charger) | **1–3A** | 5V (or 9V/12V/20V with PD) | Most common hobby supply |
| Wall charger (phone brick) | **1–3A** | 5V nominal | Usually good for 1–2A |
| Power bank | 1–3A | 5V | Built-in battery + USB out |

### USB Voltage Drop

**USB voltage is NOT exactly 5V at your board.** Every cable and connector drops some voltage:

```
USB port (5.0V) → [cable resistance] → board input (4.6–5.0V)

Long thin cables: drop 0.2–0.5V at 1A
Short thick cables: drop ~0.05V at 1A
```

A 7805 linear regulator needs at least 7V input for 5V output. If you feed it 5V USB, it can't regulate. **Check your board's actual input voltage with a multimeter.**

## Batteries

### Common Types for Hobby Projects

| Type | Nominal voltage | Capacity (typical) | Best for |
|------|----------------|-------------------|----------|
| **18650 Li-ion** | 3.7V (4.2V full, 3.0V empty) | 2000–3500mAh | Portable IoT, high current |
| **LiPo pouch** | 3.7V per cell (1S, 2S, 3S) | 100–5000mAh | Drones, compact projects |
| **AA Alkaline** | 1.5V (drops to 1.0V) | 1500–3000mAh | Low-power, simple circuits |
| **AA NiMH** | 1.2V (flat discharge) | 1000–2500mAh | Rechargeable alternative to alkaline |
| **CR2032** (coin cell) | 3.0V | 200–240mAh | RTC backup, tiny low-power sensors |
| **9V (PP3)** | 9V (drops to 6V) | 500–600mAh | Old Arduinos, smoke detectors (avoid) |

### Li-ion / LiPo Safety

**Lithium batteries are dangerous if mishandled.** They store a lot of energy in a small space.

| What NOT to do | What happens |
|---------------|-------------|
| Overcharge past 4.2V per cell | Battery swells → fire |
| Over-discharge below 3.0V per cell | Battery damaged internally → may catch fire on next charge |
| Short-circuit the terminals | Instant high current → fire |
| Puncture or crush | Internal short → fire |
| Charge without a protection circuit | Overcharge → fire |

**Rules for lithium batteries:**

1. **Always use a protection circuit** — either a built-in protection IC (protected 18650) or a separate BMS (Battery Management System)
2. **Charge with a dedicated Li-ion/LiPo charger** (TP4056 for 18650, balance charger for LiPo packs). Never use a dumb wall adapter directly.
3. **Never leave a charging lithium battery unattended**
4. **If a battery swells or gets hot, stop using it immediately.** Dispose of it at a battery recycling center.
5. **Store at ~3.7–3.8V** (not full charge) for long-term storage

### Voltage Regulation from Batteries

Battery voltage changes as it discharges. You need a regulator to provide a steady voltage to your circuit.

```
3x AA (4.5V → 3.0V) ── [boost converter] ── 3.3V to ESP32
1x 18650 (4.2V → 3.0V) ── [boost converter] ── 3.3V to ESP32
2x AA (3.0V → 2.0V) ── [boost converter] ── 3.3V (works until batteries are flat)
```

| Battery config | Raw voltage | Needs |
|---------------|-------------|-------|
| 1× Li-ion (18650) | 3.0–4.2V | **Boost converter** to 3.3V or 5V |
| 2× AA alkaline | 2.0–3.0V | **Boost converter** to 3.3V |
| 3× AA alkaline | 3.0–4.5V | **Boost converter** (or LDO if always >3.3V) |
| 2× Li-ion in series | 6.0–8.4V | **Buck converter** to 5V or 3.3V |
| USB power bank | 5V regulated | Direct (or LDO to 3.3V) |

### CR2032 Coin Cell

Good for **very low power** projects (RTC backup, small LCD, remote sensor). **Not good for** anything that draws more than ~10mA continuously.

```
CR2032 → ESP32 → ESP32 draws 80mA → battery lasts ~3 hours (useless)
CR2032 → DS3231 RTC → draws 3µA → battery lasts ~6+ years
```

**Rule:** If your project draws >10mA, don't use a coin cell. Use a Li-ion or AA(s).

## Power Budgeting — How to Calculate

Before picking a power source, add up what your circuit draws:

| Component | Current | Notes |
|-----------|---------|-------|
| ESP32 | 80mA (WiFi on, transmitting) | 150mA+ with WiFi + BT |
| DHT22 | 1.5mA (peak) | 0.1mA average |
| 16×2 LCD + backlight | 100–200mA | Backlight dominates |
| Servo SG90 | 150mA (idle), 500mA (stall) | Peaks when moving |
| Relay module | 70–100mA | Per relay |
| NeoPixel (bright, white) | 60mA | Per pixel |

```
ESP32 + DHT22 + NeoPixel (8 pixels) = 80 + 1.5 + 480 = ~560mA max
→ Power supply needs: 560mA × 1.5 = 840mA → use a 1A+ supply
→ Battery: 2000mAh / 560mA = ~3.5 hours continuous
```

## Quick Reference

```
Wall adapter:
  Voltage: must match your circuit
  Current: must be ≥ circuit draw × 1.5
  Polarity: center-positive (most common) — always verify
  Barrel size: 5.5×2.1mm (most common)

USB:
  5V nominal, but can drop to ~4.5V over a long thin cable
  Computer port: max 500mA
  Phone charger: 1–3A

Batteries:
  18650 Li-ion: 3.7V, needs protection + boost converter for 3.3V
  AA alkaline:  1.5V, linear regulator wastes a lot
  AA NiMH:      1.2V, rechargeable, similar to alkaline
  CR2032:       tiny, low current only (µA range)

Li-ion safety:
  Protection circuit required
  Dedicated charger required (TP4056, etc.)
  Never short, puncture, or overcharge
  Swollen battery = discard immediately

Voltage regulator choice:
  Battery → boost converter (if battery voltage < needed voltage)
  Wall → buck converter (if adapter voltage > needed voltage)
  Small voltage difference → LDO (linear, wastes power as heat)
```

## See Also

- [oled-sensor-readout](/projects/oled-sensor-readout)
- [esp32-web-server](/projects/esp32-web-server)
