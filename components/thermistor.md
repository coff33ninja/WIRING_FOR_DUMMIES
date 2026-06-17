# Thermistor (NTC) — Temperature Sensing

## What It Is

A thermistor is a **temperature-dependent resistor**. Its resistance changes with temperature. The most common type is **NTC (Negative Temperature Coefficient)** — resistance goes **down** as temperature goes **up**.

> **Analogy:** An NTC thermistor is like a stretchy rubber band that relaxes when heated. At room temperature, it resists stretching (high resistance). When hot, it stretches easily (low resistance).

## NTC vs PTC Thermistor

| | NTC (Negative TC) | PTC (Positive TC) |
|--|-------------------|-------------------|
| Behavior | Resistance ↓ as temperature ↑ | Resistance ↑ as temperature ↑ |
| Common use | **Temperature sensing** (this guide) | Overcurrent protection (PTC fuse), self-regulating heaters |
| Typical part | 10kΩ NTC (most common) | PTC fuse, thermistor in 3D printer hotends |

**Rule:** For temperature sensing, always use **NTC**. PTC thermistors exist but are harder to work with as sensors.

## How It Works

An NTC thermistor changes resistance dramatically with temperature:

| Temperature | Resistance (typical 10kΩ NTC) |
|-------------|------------------------------|
| 0°C (32°F) | ~32kΩ |
| 25°C (77°F) | ~10kΩ (room temp) |
| 50°C (122°F) | ~3.6kΩ |
| 100°C (212°F) | ~680Ω |

The relationship is **non-linear** (exponential). You can't just measure resistance and divide by a constant — you need the **Steinhart-Hart equation** (or a simplified approximation) to convert resistance to temperature.

## Common Types

| NTC type | Resistance at 25°C | Use for |
|----------|-------------------|---------|
| **10kΩ** (most common) | 10kΩ | Room temp, object temp, ambient sensing |
| 100kΩ | 100kΩ | Higher temp ranges, 3D printer hotends |
| 1kΩ | 1kΩ | Lower resistance, specific industrial |
| 2.2kΩ | 2.2kΩ | Some specific applications |

Most hobby tutorials and libraries assume a **10kΩ NTC** with a **10kΩ fixed resistor** in the voltage divider.

## Wiring (Voltage Divider)

A thermistor alone doesn't produce a voltage an ADC can read. You need a **voltage divider** — the thermistor and a fixed resistor in series.

```
Pull-down configuration (thermistor on top):
  3.3V
    │
  [NTC]  ← Thermistor (10kΩ at 25°C)
    │
  ADC ───┬── Reads voltage at midpoint
    │
  [10kΩ]  ← Fixed resistor
    │
   GND

  At 25°C: NTC = 10kΩ → divider = 1.65V → ADC = ~2048
  At 50°C: NTC = 3.6kΩ → divider = ~0.92V → ADC = ~1142
```

```
Pull-up configuration (fixed resistor on top):
  3.3V
    │
  [10kΩ]  ← Fixed resistor
    │
  ADC ───┬── Reads voltage at midpoint
    │
  [NTC]  ← Thermistor
    │
   GND

  At 25°C: NTC = 10kΩ → divider = 1.65V → ADC = ~2048
  At 50°C: NTC = 3.6kΩ → divider = ~2.33V → ADC = ~2890
```

Both configurations work. Pick one and use a matching library or calculation.

## Converting ADC Reading to Temperature

### Step 1: ADC reading → Voltage

```cpp
// ESP32 (12-bit ADC, 0–3.3V)
float voltage = (analogRead(ADC_PIN) / 4095.0) * 3.3;
```

### Step 2: Voltage → Resistance of thermistor

For the **pull-down configuration** (thermistor on top):

```cpp
float rFixed = 10000.0;  // 10kΩ fixed resistor
float rThermistor = rFixed * (3.3 / voltage - 1);
```

### Step 3: Resistance → Temperature (Steinhart-Hart)

The simplified equation (B parameter approximation):

```cpp
#include <math.h>

float steinhart(float rThermistor) {
  float steinhart;
  steinhart = log(rThermistor / 10000.0);   // Divide by R0 (10k)
  steinhart /= 3950.0;                      // Divide by B coefficient
  steinhart += 1.0 / (25.0 + 273.15);       // Add inverse of 25°C in Kelvin
  steinhart = 1.0 / steinhart;              // Invert
  steinhart -= 273.15;                      // Convert to Celsius
  return steinhart;
}
```

**The B coefficient** (3950 in the example) is in the thermistor datasheet. Common values: 3435, 3950, 4100. If you don't know it, use 3950 — it's close enough for most cheap thermistors.

### Full Example

```cpp
#define THERMISTOR_PIN 34

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);           // ESP32: 12-bit
  analogSetAttenuation(ADC_11db);     // 0–3.3V range
}

void loop() {
  int adc = analogRead(THERMISTOR_PIN);
  float voltage = (adc / 4095.0) * 3.3;

  // Pull-down config: thermistor to 3.3V, fixed 10kΩ to GND
  float rFixed = 10000.0;
  float rThermistor = rFixed * (3.3 / voltage - 1);

  // Steinhart-Hart approximation
  float steinhart = log(rThermistor / 10000.0);
  steinhart /= 3950.0;
  steinhart += 1.0 / 298.15;
  steinhart = 1.0 / steinhart;
  float tempC = steinhart - 273.15;

  Serial.print("ADC: "); Serial.print(adc);
  Serial.print("  Ω: "); Serial.print(rThermistor);
  Serial.print("  °C: "); Serial.println(tempC);

  delay(1000);
}
```

## Self-Heating

When current flows through a thermistor, it heats itself up slightly — this is called **self-heating**. If you use too low a fixed resistor (like 1kΩ), more current flows and the thermistor reads warmer than it should.

```
10kΩ fixed resistor → ~0.33mA through thermistor at 25°C → low self-heating
1kΩ fixed resistor  → ~3mA through thermistor → measurable self-heating
```

**Rule:** Use the same value fixed resistor as your thermistor's nominal resistance (10kΩ NTC → 10kΩ fixed resistor). The self-heating error is negligible (<0.1°C).

## Thermistor vs Other Temperature Sensors

| Sensor | Pros | Cons |
|--------|------|------|
| **NTC thermistor** | Cheap, simple, fast response | Non-linear, needs calculation, not waterproof |
| **DS18B20** | Digital, accurate, waterproof | Slower (one at a time), more complex wiring |
| **DHT22** | Measures humidity too | Bigger, slower, less accurate on temp |
| **BME280** | Pressure + humidity + temp | More expensive, I²C |
| **Type K thermocouple** | Very high temp (1000°C+) | Needs amplifier, expensive |

> **Use a thermistor when:** You need fast response, low cost, and simplicity (one ADC pin). **Use DS18B20 when:** You need waterproof sensing, multiple sensors on one wire, or don't want to do math.

## What Happens If Something Goes Wrong

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Reads −273.15°C (absolute zero) | Thermistor not connected (open circuit) | Check wiring — broken wire or loose connection |
| Reads very high temperature (100°C+ at room temp) | Fixed resistor wrong value or missing | Check you have the right resistor |
| Reads room temperature correctly but doesn't change | Sensor stuck to something with thermal mass | Touch the sensor — does it respond? |
| Readings jump around | ADC noise | Add a 100nF cap from ADC pin to GND |
| Reads ~25°C constantly | Fixed resistor value equals thermistor at all temps | Your resistor is also temperature-sensitive (unlikely) — check circuit |
| Reads temperature 2–3°C off | Wrong B coefficient | Look up the correct value in your thermistor's datasheet |

## Quick Reference

```
NTC thermistor (10kΩ at 25°C most common):
  Resistance decreases as temperature increases
  Needs a fixed 10kΩ resistor in voltage divider

Wiring (voltage divider):
  3.3V ──[NTC]──┬── ADC ──[10kΩ]── GND  (pull-down)
  or
  3.3V ──[10kΩ]──┬── ADC ──[NTC]── GND  (pull-up)

Math:
  ADC → voltage → thermistor resistance → Steinhart-Hart → °C
  B coefficient: use 3950 if unknown

  float rThermistor = 10000.0 * (3.3 / voltage - 1);  // pull-down
  float tempC = 1.0 / (log(rThermistor/10000.0)/3950 + 1/298.15) - 273.15;

Fixed resistor = same value as thermistor (10kΩ for 10kΩ NTC)
Self-heating is negligible with 10kΩ fixed resistor.

Better for waterproof / multi-sensor: DS18B20 (digital, OneWire)
Better for humidity too: DHT22
Better for high temp: Type K thermocouple
```
