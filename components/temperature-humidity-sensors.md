# Temperature & Humidity Sensors — Which One to Use

## What They Are

Temperature and humidity sensors convert physical conditions into electrical signals your microcontroller can read. The two main approaches: **analog** (thermistor, voltage divider) and **digital** (one-wire, I²C, single-wire protocol).

## Quick Comparison

| Sensor | Output | Measures | Accuracy (temp) | Interface | Price | Best for |
|--------|--------|----------|-----------------|-----------|-------|----------|
| **DHT11** | Digital | Temp + humidity | ±2°C, ±5% RH | Single-wire | ~$2 | Cheap projects, low precision OK |
| **DHT22** (AM2302) | Digital | Temp + humidity | **±0.5°C**, ±2% RH | Single-wire | ~$5 | Hobby standard — most projects |
| **SHT30 / SHT31** | Digital | Temp + humidity | **±0.2–0.3°C** | I²C | ~$3–6 | When accuracy matters |
| **SHT40 / SHT45** | Digital | Temp + humidity | **±0.1–0.2°C** | I²C | ~$5–10 | Precision / lab-grade |
| **BME280** | Digital | Temp + humidity + **pressure** | ±0.5°C, ±3% RH | I²C / SPI | ~$5 | Weather stations, altitude |
| **BMP280** | Digital | Temp + **pressure** (no humidity) | ±0.5°C | I²C / SPI | ~$3 | Cheaper altimeter |
| **AHT10 / AHT20** | Digital | Temp + humidity | ±0.3°C, ±2% RH | I²C | ~$2 | Cheap I²C alternative to DHT22 |
| **DS18B20** | Digital | Temp only | ±0.5°C | **OneWire** | ~$3 | Waterproof, long wires, multiple sensors |
| **NTC thermistor** | **Analog** | Temp only | ±0.5–2°C (calibrated) | ADC pin | ~$1 | Simple analog, fast response |
| **LM35** | **Analog** | Temp only | ±0.5°C | ADC pin | ~$2 | Linear 10mV/°C output |

## Detailed Breakdown

### DHT11 — The Cheap One

| | Value |
|--|-------|
| Temperature range | 0–50°C |
| Temperature accuracy | **±2°C** (barely useful) |
| Humidity range | 20–80% RH |
| Humidity accuracy | **±5%** (very loose) |
| Update rate | **1 reading/sec** |
| Price | ~$2 |

**Use for:** Projects where ±2°C is acceptable and you only need a rough humidity reading. **The extra $3 for a DHT22 is almost always worth it.**

### DHT22 (AM2302) — The Hobby Standard

| | Value |
|--|-------|
| Temperature range | −40°C to 80°C |
| Temperature accuracy | **±0.5°C** |
| Humidity range | 0–100% RH |
| Humidity accuracy | **±2%** |
| Update rate | **2 readings/sec** |
| Price | ~$5 |

**Wiring:**

```
DHT22 Module:
  VCC ──── 3.3V or 5V
  DATA ─── GPIO + 10kΩ pull-up to VCC (required!)
  GND ──── GND
```

> **The 10kΩ pull-up is NOT optional.** DHT uses an open-drain protocol — it can only pull the line low. Without the pull-up, communication fails.

**Libraries:** `DHT sensor library` by Adafruit

```cpp
#include <DHT.h>
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

dht.begin();
float t = dht.readTemperature();
float h = dht.readHumidity();
// Max 2 reads/sec — add delay(500) between reads
```

### SHT30 / SHT31 — I²C, More Accurate

| | SHT30 | SHT31 |
|--|-------|-------|
| Temperature accuracy | ±0.3°C | ±0.2°C |
| Humidity accuracy | ±2% | ±1.5% |
| Interface | I²C | I²C |
| I²C address | 0x44 (or 0x45) | 0x44 (or 0x45) |
| Price | ~$3 | ~$5 |

**Wiring:**

```
SHT30 Module:
  VCC ──── 3.3V
  GND ──── GND
  SCL ──── GPIO 22
  SDA ──── GPIO 21
```

**Libraries:** `Adafruit SHT31` or `SparkFun SHT30`

```cpp
#include <Wire.h>
#include <Adafruit_SHT31.h>

Adafruit_SHT31 sht31 = Adafruit_SHT31();

void setup() {
  Wire.begin();
  sht31.begin(0x44);  // Default address
}

void loop() {
  float t = sht31.readTemperature();
  float h = sht31.readHumidity();
  delay(1000);
}
```

### BME280 — Temp + Humidity + Pressure

A single chip that measures temperature, humidity, and **barometric pressure**. You can calculate altitude from pressure.

| | Value |
|--|-------|
| Temperature | ±0.5°C |
| Humidity | ±3% |
| Pressure | ±1 hPa (≈ ±8m altitude) |
| Interface | I²C (default 0x76 or 0x77) or SPI |
| Price | ~$5 |

**Use for:** Weather stations, altimeters, outdoor sensor nodes.

**Wiring (I²C):**

```
BME280 Module:
  VCC ──── 3.3V
  GND ──── GND
  SCL ──── GPIO 22
  SDA ──── GPIO 21
```

**Libraries:** `Adafruit BME280`

```cpp
#include <Wire.h>
#include <Adafruit_BME280.h>

Adafruit_BME280 bme;
bme.begin(0x76);  // Default address (some modules use 0x77)

float t = bme.readTemperature();
float h = bme.readHumidity();
float p = bme.readPressure() / 100.0F;  // Convert Pa to hPa
float a = bme.readAltitude(1013.25);     // Altitude in meters (sea level pressure as reference)
```

### AHT10 / AHT20 — Cheap I²C Alternative

Chinese I²C temp/humidity sensors. Similar accuracy to DHT22 but uses I²C instead of the finicky single-wire protocol.

| | AHT10 | AHT20 |
|--|-------|-------|
| Temperature accuracy | ±0.3°C | ±0.3°C |
| Humidity accuracy | ±2% | ±2% |
| Interface | I²C (0x38) | I²C (0x38) |
| Price | ~$2 | ~$3 |

**Use for:** Budget I²C projects where you want more libraries and community support than SHT30 but at DHT11 pricing.

**Libraries:** `Adafruit AHTX0`

```cpp
#include <Adafruit_AHTX0.h>
Adafruit_AHTX0 aht;
aht.begin();

sensors_event_t humidity, temp;
aht.getEvent(&humidity, &temp);
// temp.temperature, humidity.relative_humidity
```

### DS18B20 — Waterproof, Long Wires

Digital temperature sensor in a **waterproof metal probe**. Multiple sensors can share one wire (OneWire protocol).

| | Value |
|--|-------|
| Temperature | −55°C to 125°C, ±0.5°C |
| Interface | OneWire (unique 64-bit address per chip) |
| Cable length | 10m+ with proper pull-up |
| Price | ~$3 |

> **Full guide:** See [DS18B20 Project Guide](../projects/ds18b20-onewire.md) for wiring and code.

### NTC Thermistor — Analog, Simple, Fast

A resistor that changes resistance with temperature. Needs an ADC pin and a voltage divider.

| | Value |
|--|-------|
| Temperature | −40°C to 125°C (typical) |
| Accuracy | ±0.5–2°C (depends on calibration) |
| Interface | **ADC pin** + fixed resistor |
| Response time | Very fast (small thermal mass) |
| Price | ~$1 |

> **Full guide:** See [Thermistor Reference](thermistor.md) for the voltage divider circuit and Steinhart-Hart equation.

## Which Interface?

| Interface | Pros | Cons | Sensors using it |
|-----------|------|------|-----------------|
| **Single-wire** (DHT) | One pin, simple library | Timing-critical, slow, pull-up required | DHT11, DHT22 |
| **I²C** | Standard bus, multiple sensors, fast | Two pins, address conflicts, pull-ups needed | SHT30, BME280, AHT10 |
| **OneWire** | Waterproof, long wires, many on one pin | Slower, more complex addressing | DS18B20 |
| **Analog ADC** | One pin, no protocol, instant read | Voltage divider needed, less precise | NTC thermistor, LM35 |

## Quick Selection Guide

| Need | Best sensor | Why |
|------|-------------|-----|
| Simple hobby temp + humidity | **DHT22** | Cheap, easy, good enough accuracy |
| I want I²C (simpler wiring) | **AHT20** or **SHT30** | I²C avoids DHT's timing quirks |
| Weather station (needs pressure) | **BME280** | Only option that does pressure too |
| Waterproof temp sensing | **DS18B20** | Stainless steel probe, long cable |
| Many temp sensors, one pin | **DS18B20** | Each has unique address, share one wire |
| Very accurate temperature | **SHT31** or **SHT45** | ±0.1–0.2°C |
| Cheap and simple | **NTC thermistor** | $1, one ADC pin, voltage divider |
| Low power / battery | **SHT30** or **BME280** | Low standby current, I²C |
| Lab / data logging grade | **SHT45** | ±0.1°C, ±1% RH |
| Bare minimum budget | **DHT11** | $2 but ±2°C accuracy — add $3 for DHT22 |

## Quick Reference

```
Temp + humidity sensors:

  DHT family (single-wire):
    DHT11: ±2°C, ±5% RH, 1/sec — barely useful
    DHT22: ±0.5°C, ±2% RH, 2/sec — hobby standard (buy this, not DHT11)
    Wiring: VCC + DATA (10kΩ pull-up!) + GND
    Library: DHT sensor library (Adafruit)

  I²C family:
    SHT30:  ±0.3°C — accurate, I²C
    SHT31:  ±0.2°C — even more accurate
    BME280: temp + humidity + pressure (weather stations)
    AHT20:  budget I²C, similar to DHT22 in accuracy
    Wiring: VCC + GND + SCL + SDA (I²C pull-ups needed)
    Addresses: 0x44, 0x76, 0x77, 0x38 — depends on sensor

  Temp only:
    DS18B20:  waterproof, OneWire, many on one pin
    NTC:      analog, fast, cheap ($1)

Pull-up rules:
  DHT11/22:   10kΩ pull-up on DATA to VCC (required!)
  I²C:        4.7kΩ on SDA and SCL to VCC (often built-in on dev boards)
  OneWire:    4.7kΩ on data line (required!)
```
