# Hall Effect Sensor — Component Reference

> **See also:** [Current Sensor](current-sensor.md) — the ACS712 uses the Hall effect to measure current.

## What It Is

A Hall effect sensor detects magnetic fields. When a magnet comes near, the sensor outputs a signal — either a digital HIGH/LOW (for simple presence detection) or an analog voltage proportional to field strength.

Named after Edwin Hall who discovered in 1879 that a magnetic field perpendicular to current flow creates a voltage across a conductor.

```
    Magnet (S pole)
       │
       ▼
┌──────────────┐
│   Hall       │
│   Sensor     │──→ Output
└──────────────┘
```

## Digital vs Analog — Which to Use

| Type | Output | Detects | Use For |
|------|--------|---------|---------|
| **Digital** (unipolar) | HIGH/LOW | One pole (usually South) | Proximity switch, end-stop, RPM sensing |
| **Digital** (bipolar) | HIGH/LOW | Both poles | Rotary encoder, direction detection |
| **Digital** (latching) | HIGH/LOW, latches | One pole turns on, opposite turns off | Brushless motor commutation, RPM |
| **Analog** (linear) | Voltage proportional to field | Field strength (any pole) | Position sensing, current sensing, magnet strength |

## Digital Hall Effect Sensors

### Unipolar (e.g., A3144, SS441)

- **Only responds to one magnetic pole** (usually South).
- Output goes LOW when South pole is near, HIGH when magnet is removed.
- Simple on/off magnetic switch.

```
VCC ──┬── 10kΩ ──┬── OUT ── GPIO
      │           │
      ├── VCC     │
      │   A3144   │
      ├── OUT ────┘
      ├── GND
      │
     GND
```

**Wiring:** Standard 3-pin package (VCC, GND, OUT). VCC is 3.3–24V depending on part. OUT is open-collector with internal pull-up (or add external 10kΩ).

### Bipolar / Latching (e.g., AH180, SS41)

- **Responds to both poles.** South pole turns output ON. North pole turns output OFF.
- Output stays in the last state until the opposite pole is applied (latching).
- Used for RPM sensing — one magnet per revolution gives one pulse.

```
On a wheel:
    Magnet passes sensor → output goes LOW (South detected)
    Magnet passes again → output goes HIGH (North detected)
    ... or the opposite magnet polarity triggers the return
```

**Latching sensors** require both poles — the output doesn't change when the magnet is removed, only when the opposite pole appears. This makes them ideal for counting rotations:

```
    South ──→ output LOW (latched)
    [magnet moves away] → output stays LOW
    North ──→ output HIGH (unlatched)
    [magnet moves away] → output stays HIGH
```

## Analog Hall Effect Sensors (e.g., SS49E, A1302, AH49E)

Outputs a voltage proportional to the magnetic field strength:

- **No magnet:** Output = VCC/2 (~2.5V at 5V supply)
- **South pole approaching:** Output rises toward VCC
- **North pole approaching:** Output drops toward GND
- **Field strength vs output:** Linear within the sensor's range

### Wiring (SS49E / A1302)

```
SS49E:
    VCC ── 5V
    GND ── GND
    OUT ── ADC pin
```

Read the analog value, convert to gauss (magnetic field unit) if you know the sensitivity. For most hobby projects, you just use the relative change.

### Reading Analog Hall Sensor (Arduino)

```c
void loop() {
  int raw = analogRead(A0);
  float voltage = (raw / 1023.0) * 5.0;
  // Center is 2.5V (no field)
  float field = (voltage - 2.5) / 0.0025; // ~2.5 mV/G for SS49E
  Serial.printf("Field: %.0f gauss\n", field);
  delay(100);
}
```

## Common Applications

### RPM / Speed Sensing

Mount a small magnet on a rotating shaft or wheel. Point the hall sensor at it. Every time the magnet passes, you get a pulse. Count pulses per minute = RPM.

```
    ┌──── Wheel ────┐
    │      │        │
    │   [magnet]    │
    │      │        │
    └──────┼────────┘
           │
      Hall sensor ──→ microcontroller interrupt pin
```

Code (Arduino):

```c
volatile int pulseCount = 0;
unsigned long lastTime = 0;

void setup() {
  attachInterrupt(digitalPinToInterrupt(2), countPulse, FALLING);
}

void loop() {
  if (millis() - lastTime > 1000) {
    int rpm = pulseCount * 60; // pulses per second → RPM
    pulseCount = 0;
    lastTime = millis();
    Serial.printf("RPM: %d\n", rpm);
  }
}

void countPulse() {
  pulseCount++;
}
```

For one magnet per revolution, RPM = pulses per second × 60. For multiple magnets, divide by the number of magnets.

### End-Stop / Proximity

Mount a digital hall sensor at the end of a linear rail. Attach a magnet to the moving part. When it reaches the end, the sensor triggers.

Better than a mechanical limit switch because:
- **No contact** — no wear, no bouncing
- **Sealed** — works in dust, water, vibration
- **Infinite lifetime** — nothing to break

### Linear Position Sensing

Use an analog hall sensor and a magnet on a sliding mechanism. The voltage changes smoothly as the magnet moves closer or further. Calibrate min/max positions.

Accuracy is ~0.1mm with careful calibration, but hall sensors have significant temperature drift — don't rely on absolute readings for precision applications.

### Brushless DC Motor Commutation

This is what hall sensors are most commonly used for in industry. Three hall sensors inside a BLDC motor tell the controller exactly when to switch the next coil. Not something you typically wire as a hobbyist — the motor controller handles it.

## Hall Sensor vs Reed Switch vs IR Proximity

| | Hall Sensor | Reed Switch | IR Proximity |
|--|------------|-------------|--------------|
| Actuation | Magnetic field | Magnetic field | Light (IR) reflection |
| Mechanical contact | No | **Yes** (contacts inside) | No |
| Lifetime | Infinite | ~10 million cycles | Long |
| Switching speed | Very fast (µs) | Slow (ms — contact bounce) | Fast |
| Sensitivity | Adjustable (distance) | Fixed | Adjustable (pot) |
| Dust/water | Excellent | Good (sealed glass) | Poor (lens gets dirty) |
| Power | ~5–10 mA | 0 mA (passive switch) | ~10–20 mA (LED + receiver) |

**Hall sensors win** for speed sensing, position sensing, and harsh environments. **Reed switches** are cheaper and use zero power — good for battery-powered magnetic detection. **IR** works for short-range proximity where the environment is clean.

## Quick Reference

- **Digital hall sensors** (A3144) — on/off magnetic switch, 3.3–24V, open-collector output
- **Latching hall sensors** (SS41) — North pole on, South pole off (or vice versa), used for RPM
- **Analog hall sensors** (SS49E, A1302) — voltage proportional to field strength, use with ADC
- **Output is open-collector** for most digital types — add a pull-up resistor (10kΩ) if not built-in
- **Reverse polarity protection** — most modules have it, bare sensors don't — don't wire backwards
- **Hysteresis** — digital hall sensors have built-in hysteresis (Schmitt trigger) to avoid oscillation at the switching point
- **Temperature drift** — analog sensors drift ~0.1%/°C. Calibrate at your operating temperature.
