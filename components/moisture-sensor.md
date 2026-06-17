# Soil Moisture / Rain Sensor — Component Reference

## What It Is

A soil moisture sensor measures **how wet the ground is** by detecting the electrical conductivity between two probes. Wet soil conducts better than dry soil. A rain sensor works on the same principle — water on the sensing surface completes the circuit.

## How It Works

Two exposed traces on the PCB act as probes. The microcontroller reads the resistance between them:

- **Dry (in air):** Very high resistance → ADC reads ~1023 (5V) or 0 (some modules invert)
- **Damp soil:** Moderate resistance → ADC reads ~500–700
- **Wet soil / water:** Low resistance → ADC reads ~0–300

```
    Dry soil:   ──/\/\/\──  (high resistance, near open circuit)
    Wet soil:   ────────    (low resistance, near short circuit)
```

**The problem:** DC current through the probes causes **electrolysis** — the copper traces corrode over time. To prevent this, use the sensor intermittently (read every 5 minutes, not continuously) and turn off power between readings.

## Module Types

### LM393 Comparator Module (Most Common)

The standard module has an **LM393 comparator** that gives both analog and digital output:

```
Moisture sensor module:
  VCC ── 5V (or 3.3V)
  GND ── GND
  AO  ── Analog output (0–5V, proportional to moisture)
  DO  ── Digital output (HIGH = dry, LOW = wet; threshold set by pot)

  Potentiometer ── Adjusts the digital trigger threshold
```

### Capacitive Sensor (Better, Corrosion-Resistant)

A **capacitive moisture sensor** measures the dielectric constant of the soil (not conductivity). It doesn't have exposed metal traces, so no corrosion:

- More expensive but lasts much longer
- Sensitive to proximity of metal and large objects
- Still needs intermittent reading for best accuracy

### Rain Sensor

A rain sensor module is the same principle but with a larger exposed grid. It detects water droplets on the surface:

```
Rain sensor board                    Module
  ┌──────────────────────┐
  │  ═══ ═══ ═══ ═══ ═══ │  ──┬── VCC
  │  ═══ ═══ ═══ ═══ ═══ │    ├── GND
  │  ═══ ═══ ═══ ═══ ═══ │    ├── AO (analog)
  │  ═══ ═══ ═══ ═══ ═══ │    └── DO (digital)
  └──────────────────────┘
     Interdigitated traces
```

Mount at a slight angle so water runs off.

## Wiring

```
Moisture module       Microcontroller
  VCC ───────────────── 5V or 3.3V
  GND ───────────────── GND
  AO  ───────────────── ADC pin (analog reading)
  DO  ───────────────── GPIO (optional, threshold detection)
```

For the bare sensor (without module), connect the probes through a voltage divider:

```
VCC ──┬── Probe 1 ────┬── ADC pin
      │               │
     10kΩ            Soil
      │               │
     GND ── Probe 2 ──┘
```

## Reading with a Microcontroller

```cpp
const int MOISTURE_PIN = 34;  // ADC pin

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(MOISTURE_PIN);

  if (value > 900) {
    Serial.println("Very dry");
  } else if (value > 600) {
    Serial.println("Dry");
  } else if (value > 350) {
    Serial.println("Damp");
  } else {
    Serial.println("Wet");
  }

  delay(5000);  // read every 5 seconds (don't read constantly)
}
```

**Thresholds vary** by sensor, soil type, and temperature. Calibrate by testing in dry soil and wet soil:

```cpp
// Calibration
int dryValue = 950;   // measured in dry soil
int wetValue = 250;   // measured in water
int range = dryValue - wetValue;
int percent = map(reading, wetValue, dryValue, 100, 0);
// percent = 0 (dry) to 100 (wet)
```

## Preventing Corrosion

The biggest problem with resistive moisture sensors is **electrode corrosion**:

| Technique | How it helps |
|-----------|-------------|
| **AC drive** | Alternate polarity between readings instead of DC |
| **Pulse power** | Only power the sensor during reading, turn off between |
| **Stainless steel probes** | Replace copper traces with stainless screws/wires |
| **Capacitive sensor** | No exposed metal traces — measures dielectric constant |
| **Read less often** | Every 5–60 minutes, not continuously |

### Pulse Power Circuit

Don't leave VCC connected continuously. Use a MOSFET or transistor to switch power only during readings:

```
GPIO (control) ──── MOSFET gate
                      │
VCC ── MOSFET drain ──┴── Sensor VCC
        MOSFET source ── GND (N-channel)
```

In code:

```cpp
pinMode(POWER_PIN, OUTPUT);
digitalWrite(POWER_PIN, LOW);  // sensor off

void readMoisture() {
  digitalWrite(POWER_PIN, HIGH);  // power on
  delay(100);                      // stabilize
  int reading = analogRead(MOISTURE_PIN);
  digitalWrite(POWER_PIN, LOW);   // power off
  return reading;
}
```

## Calibration Example

```cpp
int dryValue, wetValue;
bool calibrated = false;

void calibrate() {
  Serial.println("Place sensor in DRY soil, press any key...");
  while (!Serial.available());
  dryValue = analogRead(MOISTURE_PIN);

  Serial.println("Place sensor in WET soil, press any key...");
  while (!Serial.available());
  wetValue = analogRead(MOISTURE_PIN);

  calibrated = true;
}
```

## Common Problems

| Problem | Cause | Fix |
|--------|-------|------|
| Readings always max (dry) | Sensor not in soil, or probes not touching | Push probes fully into soil |
| Readings always min (wet) | Probes shorted by water on surface | Wipe dry and re-insert |
| Readings drift over time | Corrosion building on probes | Clean probes, use pulse power, switch to capacitive |
| Readings don't change with water | Sensor not in contact with soil | Ensure good soil contact, or water the soil not the sensor |
| Digital output doesn't trigger | Threshold set wrong | Adjust potentiometer |

## Quick Reference

- **Resistive sensor:** Simple, cheap, corrodes over time
- **Capacitive sensor:** More expensive, no corrosion, lasts longer
- **Analog output:** 0–1023 (or 0–4095 for 12-bit), wet = low value, dry = high value
- **Digital output:** Adjustable threshold via potentiometer
- **Pulse power:** Turn sensor on only during readings to prevent corrosion
- **Calibrate** for your specific soil type and sensor
- **Thresholds vary** between sensor batches
- **Rain sensor:** Same technology, larger sensing area, mount at angle
