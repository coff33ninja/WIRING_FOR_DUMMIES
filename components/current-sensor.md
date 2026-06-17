# Current Sensor (ACS712 / INA219) — Component Reference

> **See also:** [Hall Effect Sensor](hall-effect-sensor.md) — the underlying physics behind the ACS712.

## What It Is

A current sensor measures how much current is flowing through a wire. You use it to monitor power consumption, detect when a motor is stalled, measure battery charge/discharge, or build a power meter.

There are two common types:

| Sensor | Output | Measures | Max Current | Pros | Cons |
|--------|--------|----------|-------------|------|------|
| ACS712 | **Analog voltage** | AC and DC | 5A, 20A, or 30A | Simple, works with AC | Noisy, low resolution, needs ADC |
| INA219 | **I2C digital** | DC only | ±3.2A (built-in shunt) | High accuracy, 0.1mA resolution | DC only, limited range |
| INA226 | **I2C digital** | DC only | External shunt (any) | High voltage, configurable | Needs external resistor |
| CT Clamp | **Analog AC** | AC only | 100A+ | Non-contact, high current | AC only, bulky |

## ACS712 — Analog Current Sensing

### How It Works

The ACS712 uses the Hall effect — current flowing through the chip creates a magnetic field, and a sensor inside measures that field and outputs a proportional voltage.

- **No contact with the high-current path** — the main current flows through the chip internally and the measurement circuit is isolated.
- **Output voltage** is centered at VCC/2. With 0A flowing, output = 2.5V (for 5V supply). Each amp of current changes the output by 66–185 mV depending on the variant.
- **Works with AC and DC** — for AC, the output swings above and below 2.5V.

### ACS712 Variants

| Part | Range | Sensitivity | Resolution |
|------|-------|-------------|-----------|
| ACS712-05B | ±5A | 185 mV/A | ~25 mA |
| ACS712-20A | ±20A | 100 mV/A | ~50 mA |
| ACS712-30A | ±30A | 66 mV/A | ~75 mA |
| ACS723 (newer) | ±5A to ±50A | Various | Lower noise than ACS712 |

The newer **ACS723** and **ACS724** are preferred over the ACS712 — they have better accuracy, lower noise, and smaller packages. If you're buying new, get these instead.

### Wiring

```
ACS712 Module:
    VCC ── 5V
    GND ── GND
    OUT ── ADC pin of microcontroller
    IP+ ── power source (+) side
    IP- ── load (+) side
```

The current flows **through** IP+ to IP- — these are the thick screw terminals. The load is powered through the sensor.

### Reading in Code (Arduino)

```c
float readCurrent() {
  int raw = analogRead(A0);
  float voltage = (raw / 1023.0) * 5.0;
  float current = (voltage - 2.5) / 0.100; // 100 mV/A for 20A version
  return current;
}
```

### AC Current Measurement

For AC, you need to sample many readings over a full AC cycle and calculate RMS:

```c
float readAC_Current() {
  float sum = 0;
  for (int i = 0; i < 100; i++) {
    float val = (analogRead(A0) - 512) * (5.0 / 1023.0);
    sum += val * val;
    delayMicroseconds(200); // 100 samples over ~20ms (50Hz AC)
  }
  float rms = sqrt(sum / 100);
  return rms / 0.100; // Convert to amps
}
```

## INA219 — Precision DC Current Sensing

### How It Works

The INA219 measures the voltage drop across a very small resistor (shunt resistor) in series with the load. It uses a high-precision ADC to convert that tiny voltage to a current reading, which it reports over I2C.

- **Much more accurate** than the ACS712 — 0.1mA resolution at low currents.
- **DC only** — the internal ADC is designed for steady or slowly changing DC.
- **Also measures voltage** — the INA219 reads bus voltage too, so you get power (V × I).
- **I2C address** — default 0x40, can be changed to 0x41–0x4F with address pins.

### Wiring

```
INA219 Module (like Adafruit / generic):
    VCC ── 3.3V or 5V
    GND ── GND
    SDA ── SDA (GPIO 21 on ESP32, A4 on Arduino Uno)
    SCL ── SCL (GPIO 22 on ESP32, A5 on Arduino Uno)
    VIN+ ── power source (+)
    VIN- ── load (+)
```

### Reading in Code (Arduino, with Adafruit_INA219 library)

```c
#include <Adafruit_INA219.h>
Adafruit_INA219 ina219;

void setup() {
  Serial.begin(115200);
  ina219.begin();
}

void loop() {
  float voltage = ina219.getBusVoltage_V();
  float current = ina219.getCurrent_mA(); // in milliamps
  float power = voltage * (current / 1000.0); // in watts
  Serial.printf("%.2f V, %.2f mA, %.2f W\n", voltage, current, power);
  delay(1000);
}
```

## Choosing Between ACS712 and INA219

| | ACS712 | INA219 |
|--|--------|--------|
| Current type | AC or DC | **DC only** |
| Max current | 5A–30A (module choice) | ±3.2A (built-in), or custom shunt |
| Resolution | ~25–75 mA | ~0.1 mA |
| Accuracy | ±5% typical | ±0.5% typical |
| Output | Analog (needs ADC) | I2C (digital) |
| Isolation | **Galvanic isolation** | No isolation (shunt is in-circuit) |
| Price | $2–3 | $3–5 |
| Ease of use | Simple ADC read | Library needed, but more features |

**Use ACS712 when:**
- You need to measure AC current (mains-powered device)
- You need isolated measurement (high voltage side)
- You need high current (>3A)
- Accuracy doesn't matter much

**Use INA219 when:**
- You measure DC only
- You want good accuracy and resolution
- You want voltage AND current in one sensor
- Your current is under 3A (or you can add an external shunt)

**Use a CT clamp when:**
- You need to measure 50A+ AC
- You want non-contact (clamp around a wire without cutting it)
- You're building an energy monitor for your house

## Common Mistakes

- **ACS712 noisy output** — add a 100nF capacitor from OUT to GND and take multiple ADC readings and average them.
- **INA219 voltage too high** — the INA219 max bus voltage is 26V. Going higher destroys it.
- **ACS712 running at 3.3V** — the output scales with VCC. At 3.3V, VCC/2 = 1.65V, sensitivity stays the same (mV/A) but 3.3V is less noisy than 5V.
- **Using ACS712 for low currents** — below ~100mA, the ACS712 is inaccurate. Use INA219 for low-power measurements.
- **Reversing IP+ and IP-** — the ACS712 works either way (measures reverse current as negative voltage), but you must have the current flowing through the device.
