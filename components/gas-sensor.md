# Gas Sensor (MQ Series) — Component Reference

## What It Is

MQ-series gas sensors detect various gases using a **heated metal-oxide semiconductor** (MOx). The sensor's resistance changes when certain gases are present. They're cheap, sensitive, and used in air quality monitors, gas leak detectors, and breathalyzers.

## How Gas Sensors Work

Inside an MQ sensor:
- A **heater coil** warms up the sensing element (takes 30–60 seconds)
- The **sensing material** (tin dioxide, SnO₂) changes resistance when exposed to target gases
- Higher gas concentration = lower resistance (for most MQ sensors)

```
  ┌──────────────┐
  │              │
  │  SnO₂ layer  │ ← Resistance changes with gas concentration
  │              │
  │  Heater coil │ ← Heats the sensor to operating temperature (~300–400°C)
  └──────────────┘
       │    │
     VCC   GND
```

## MQ Sensor Types

| Sensor | Detects | Typical range | Use case |
|--------|---------|---------------|----------|
| **MQ-2** | Methane, butane, LPG, smoke | 200–10000 ppm | Gas leak (kitchen), smoke alarm |
| **MQ-3** | Alcohol, ethanol | 0.04–4 mg/L | Breathalyzer, alcohol detection |
| **MQ-4** | Methane, natural gas | 200–10000 ppm | Natural gas leak detection |
| **MQ-5** | LPG, natural gas, coal gas | 200–10000 ppm | Gas leak (combined) |
| **MQ-6** | LPG, butane, propane | 200–10000 ppm | LPG leak detection |
| **MQ-7** | Carbon monoxide (CO) | 20–2000 ppm | CO alarm |
| **MQ-8** | Hydrogen (H₂) | 100–10000 ppm | Hydrogen leak detection |
| **MQ-9** | CO and methane | 20–2000 / 200–10000 | Dual gas detection |
| **MQ-135** | NH₃, NOx, alcohol, benzene, smoke, CO₂ | 10–1000 ppm | Air quality (general) |
| **MQ-136** | Hydrogen sulfide (H₂S) | 5–200 ppm | Sewer gas, rotten egg detection |
| **MQ-137** | Ammonia (NH₃) | 5–500 ppm | Refrigeration leak, agriculture |

**MQ-2** and **MQ-135** are the most common for hobby projects.

## Module Types

### Analog Module (with comparator)

Most MQ modules include an **LM393 comparator** that gives both analog and digital output:

```
MQ Module:
  VCC ── 5V
  GND ── GND
  DO  ── Digital output (HIGH = clean, LOW = gas detected above threshold)
  AO  ── Analog output (0–5V, proportional to gas concentration)

  Potentiometer ── Adjusts the digital threshold
```

**AO (analog):** Connect to ADC pin for actual gas concentration readings
**DO (digital):** Connect to GPIO for simple threshold detection (HIGH = clean air)

### Bare Sensor (no module)

A bare MQ sensor needs:
- A **load resistor** (RL) between the sensor output and GND (typically 1–47kΩ)
- **Heater voltage** (5V for most, check datasheet)
- **Circuit voltage** (5V for most)

## Wiring (Module)

```
MQ module             Microcontroller
  VCC ───────────────── 5V (most MQ sensors need 5V for the heater)
  GND ───────────────── GND
  AO  ───────────────── ADC pin (analog reading)
  DO  ───────────────── GPIO (optional, if threshold detection is enough)
```

## Warm-Up Time

MQ sensors need time to stabilize:

| Time | State |
|------|-------|
| 0–10 seconds | Heater reaches temperature |
| 10–60 seconds | Sensor stabilizes, readings are noisy |
| 1–5 minutes | Usable readings, still drifting |
| 5–30 minutes | Fully stable readings |
| Always powered | Best accuracy (leaving MQ sensors always on improves consistency) |

**Don't trust readings during the first minute.** Add a startup delay.

## Reading Gas Concentration

The relationship between sensor resistance and gas concentration is not linear. Converting the ADC reading to PPM requires logarithmic math:

```cpp
float readMQ(int pin) {
  float rs = 0;
  for (int i = 0; i < 50; i++) {
    rs += analogRead(pin);
    delay(1);
  }
  rs /= 50;

  float voltage = rs / 1024.0 * 5.0;  // for 10-bit ADC, 5V reference
  // Convert voltage to resistance using voltage divider formula
  // Then use logarithmic curve from datasheet for PPM
  return voltage;
}
```

For accurate PPM readings, you need:
1. The **load resistor value** (RL — check your module)
2. The **sensor resistance in clean air** (R0 — measure at startup)
3. The **logarithmic curve** from the datasheet (ratio vs PPM graph)

Most hobby projects use the raw analog value or a simple threshold instead of calculating PPM.

## Placement Tips

- **Elevate the sensor** above other components — it needs airflow
- **Avoid enclosures** — the sensor needs exposure to ambient air
- **Keep away from direct sunlight** — UV and temperature affect readings
- **Mount vertically** — some sensors have a specific orientation for optimal airflow
- **Don't block the mesh** — the gas needs to reach the sensing element

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| AO reading stuck at 0 or 1023 | Wrong voltage or wiring | Check 5V to VCC, GND connection |
| AO reading stuck at 0 or 1023 | ADC pin not configured | Make sure pin is an analog input |
| Readings don't change | Sensor not warmed up yet | Wait 1+ minute after power-on |
| Readings slowly drift | Normal — sensor takes 30 min to stabilize | Allow warm-up, or implement auto-calibration |
| Digital output always LOW | Threshold too sensitive | Adjust potentiometer counter-clockwise |
| Digital output always HIGH | Threshold not sensitive enough | Adjust potentiometer clockwise |
| Readings affected by humidity | MOx sensors respond to humidity too | Use MQ-135 with temperature/humidity compensation |
| Sensor stopped working | Heater burned out (unlikely but possible) | Check resistance across heater pins (~30Ω when working) |

## Calibration

Basic calibration in clean air:

```cpp
int r0 = 0;
void setup() {
  delay(60000); // 1 minute warm-up
  for (int i = 0; i < 100; i++) {
    r0 += analogRead(AO_PIN);
    delay(10);
  }
  r0 /= 100;
  // r0 = baseline reading in clean air
}
```

Compare future readings to R0 to detect gas presence.

## Power Consumption

MQ sensors consume significant power for the heater:

| Sensor | Heater current | Total power |
|--------|---------------|-------------|
| MQ-2 | ~150mA | ~750mW at 5V |
| MQ-3 | ~150mA | ~750mW |
| MQ-4 | ~150mA | ~750mW |
| MQ-7 | ~50mA (pulsed) | ~250mW |
| MQ-135 | ~150mA | ~750mW |

**Don't power from a microcontroller's 5V pin.** The heater draws too much current. Use an external 5V supply. The sensor can share ground with the MCU, but power it separately.

## Quick Reference

- **Heater needs 5V** and draws ~150mA. Use external power, not MCU's 5V pin.
- **Warm-up:** 1 minute minimum. 30 minutes for stable readings.
- **Analog pin (AO):** 0–5V proportional to gas concentration
- **Digital pin (DO):** HIGH = clean, LOW = gas detected (adjustable threshold)
- **MQ-2:** Smoke + flammable gas (methane, butane, LPG)
- **MQ-135:** General air quality (NH₃, NOx, CO₂, smoke)
- **MQ-7:** Carbon monoxide (CO) specifically
- **Place:** In open air, elevated, away from sunlight
- **Conversion:** Raw ADC → voltage → sensor resistance → PPM (use datasheet log curve)
- **Power:** Don't use MCU regulator — sensor draws too much for heater
