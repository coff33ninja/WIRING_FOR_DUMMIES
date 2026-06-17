# Ultrasonic Sensor (HC-SR04) — Component Reference

## What It Is

The HC-SR04 measures distance by sending a 40kHz ultrasonic pulse and timing how long it takes for the echo to return. Sound travels at ~343 m/s in air at 20°C. Half the round-trip time × speed of sound = distance.

> **Analogy:** Shouting at a cliff and counting seconds until you hear the echo. The longer the delay, the farther the cliff.

## How Sonar Works — Trigger, Pulse, Echo

```
  Microcontroller        HC-SR04
       │                   │
       │──── Trig 10µs ───→│  (step 1: trigger)
       │                   │
       │                   │─── sends 8 pulses of 40kHz
       │                   │
       │←── Echo pulse ────│  (step 2: listen)
       │     (width = time │
       │      of flight)   │
```

**Step 1 — Trigger:** Set the Trig pin HIGH for 10µs. The sensor sends 8 cycles of 40kHz ultrasound.

**Step 2 — Echo:** The Echo pin goes HIGH when the pulse is sent, and goes LOW when the echo is received. The width of this HIGH pulse = time of flight.

**Distance calculation:**
```
distance (cm) = pulse_width_us / 58
distance (inches) = pulse_width_us / 148
```

**Why 58?** Speed of sound ≈ 343 m/s = 0.0343 cm/µs. Round-trip: 2 × distance = time × 0.0343. Distance = time × 0.01715. Reciprocal: 1/0.01715 ≈ 58.3.

```
   pulse width  │◄──────────────►│
                │    HIGH        │
   ─────────────┘                └────────────
           start                 echo received

   pulse width 200µs  → distance 200/58 = 3.4cm
   pulse width 2000µs → distance 2000/58 = 34.5cm
   pulse width 20000µs → distance 20000/58 = 345cm
```

## Pinout

```
   ┌─────────────┐
   │ HC-SR04     │
   │             │
   │ VCC  Trig   │
   │  │    │     │
   │  │    │     │
   │  │    │     │
   │ GND  Echo   │
   └─────────────┘
```

| Pin | Connect to |
|---|---|
| VCC | 5V (not 3.3V — see below) |
| Trig | Any GPIO (output) |
| Echo | Any GPIO (input) — MUST voltage-divide if using 3.3V MCU |
| GND | Common ground |

## 5V vs 3.3V Problem — Voltage Divider on Echo

The HC-SR04 is a **5V device**. Its Echo pin outputs 5V logic HIGH. If you connect Echo directly to a 3.3V microcontroller (ESP8266, ESP32, Raspberry Pi), you'll fry the GPIO pin.

**Solution — Voltage divider on Echo:**

```
  HC-SR04 Echo (5V) ──┬── 1kΩ ──┬── 2.2kΩ ── GND
                       │         │
                       │         └─── MCU GPIO (3.3V safe ~1.65V)
                       │
                      ┌─┐
                      │ │ 1kΩ (or use 1kΩ + 2.2kΩ = ~1.7V)
                      └─┘
```

Resistor divider ratio for 3.3V logic:
```
Vout = Vin × R2 / (R1 + R2)
3.3V = 5V × R2 / (R1 + R2)
R1 = 1kΩ, R2 = 2.2kΩ → Vout ≈ 3.4V (close enough)
```

| MCU voltage | Divider resistors |
|---|---|
| 5V (Arduino) | None — direct connect |
| 3.3V (ESP, Pi) | 1kΩ + 2.2kΩ on Echo |

> **Alternative:** Use a 3.3V-compatible module like the HC-SR04P (marked "3.3V" on the back) or the JSN-SR04T.

**Can I power the HC-SR04 from 3.3V?** It may work at short range but accuracy degrades. Range drops from 400cm to ~150cm. Best to power at 5V and only divide the Echo pin.

## Range: 2cm to 400cm

| Range | Performance |
|---|---|
| 0–2cm | **Blind zone** — sensor cannot distinguish transmit from echo. Reads 0 or random. |
| 2–50cm | Accurate to ±3mm |
| 50–200cm | Accurate to ±5mm |
| 200–400cm | Accuracy drops to ±1–3cm |
| >400cm | Signal too weak — unreliable or no reading |

**Minimum distance** is a hard limit. The transmit pulse lasts ~1ms. During that time the receiver is blanked. After it recovers, echoes from objects closer than ~2cm arrive while the receiver is still settling. You will measure 0.

**Maximum distance** depends on:
- Surface reflectivity (soft surfaces absorb ultrasound)
- Angle of incidence (perpendicular = best reflection)
- Air temperature and humidity
- Supply voltage (5V gives full power)

## Accuracy Limitations

### Soft Surfaces

Ultrasound reflects best off hard, flat surfaces perpendicular to the beam.

| Surface | Reflection | Usable range |
|---|---|---|
| Smooth wall (90°) | Excellent | Full 400cm |
| Carpet, fabric | Poor — absorbs sound | ~50cm max |
| Person (clothing) | Fair | ~150cm |
| Foam, acoustic tile | Very poor | ~30cm |
| Angled surface (>45°) | Deflects away | May get no echo |

### Angle Sensitivity

The HC-SR04 has a ~15° beam cone. If the target surface is tilted more than ~15° from perpendicular, the echo deflects away from the receiver.

```
   Sensor          Target (angled 30°)
     │                 ╲
     │  ──────────────► ╲  (pulse deflects away)
     │                   ╲
     │ ◄── no echo ────────
```

### Multiple Reflections

In a room with parallel walls, the sensor may detect the second echo (bouncing off one wall, then another, then back). This gives a reading 2× the actual distance. Called **multi-path** or **crosstalk**.

**Mitigation:** Time out after ~30ms (≈5m) if no echo is received. Ignore readings that jump >50% from the previous reading.

## Single-Pin Alternatives

### JSN-SR04T (Waterproof)

Same principle as HC-SR04 but with a waterproof transducer on a cable. Used for tank level sensing, outdoor distance measurement, liquid presence.

| | HC-SR04 | JSN-SR04T |
|---|---|---|
| Waterproof | No | Yes (IP67 transducer) |
| Max range | 400cm | 400–600cm |
| Min range | 2cm | ~20cm |
| Beam angle | ~15° | ~30° (wider) |
| Pinout | 4 pins | 4 pins (GND, VCC, Trig, Echo) or 3-pin single-wire mode |
| Price | ~$1 | ~$3–4 |

**JSN-SR04T single-wire mode:** Some modules have a single "SIG" pin instead of separate Trig/Echo. Same protocol — trigger and read on the same pin. Timing is the same.

## Temperature Effect on Speed of Sound

Speed of sound in air is not constant. It varies with temperature:

```
v = 331.3 × √(1 + T/273.15)

T = 20°C → v = 343 m/s
T = 0°C  → v = 331 m/s
T = 40°C → v = 355 m/s
```

| Temperature | Error if using 20°C formula |
|---|---|
| 0°C | Reading is ~3.5% too high |
| 10°C | Reading is ~1.7% too high |
| 20°C | Correct |
| 30°C | Reading is ~1.7% too low |
| 40°C | Reading is ~3.5% too low |

**Compensation formula:**

```
v = 331.3 + (0.606 × T°C)
distance = (pulse_width × v) / 2 / 10000  (result in cm)
```

**For outdoor or temperature-varying projects:** Add a temperature sensor (DS18B20, DHT22) and compensate in software. A 10°C error = ~2% distance error — not huge for obstacle avoidance, but critical for tank level monitoring.

## Common Mistakes

| Mistake | Result |
|---|---|
| Echo direct to 3.3V GPIO | Damaged GPIO pin |
| Powering from 3.3V | Reduced range (150cm instead of 400cm) |
| Measuring objects <2cm | Always reads 0 or garbage |
| Soft/fabric target | No echo — timeout reading |
| Angled target | No echo — timeout reading |
| Trigger < 10µs pulse | Sensor ignores trigger — no reading |
| No delay between readings | Crosstalk — sensor hears its own previous pulse |
| Long wires (>2m) | Noise on Echo line — false triggers |

## Quick Reference

```
Pinout:
  VCC  → 5V
  Trig → GPIO output
  Echo → GPIO input (volt-divide for 3.3V MCU!)
  GND  → common ground

Timing:
  Trig HIGH for 10µs
  Measure Echo HIGH pulse width
  Distance (cm) = pulse_us / 58

Range: 2cm–400cm (practical: 3cm–300cm)
Accuracy: ±3mm near, ±3cm far
Cone angle: ~15°

3.3V MCU fix:
  Echo ── 1kΩ ──┬── 2.2kΩ ── GND
                └── GPIO

Temperature:
  v = 331.3 + (0.606 × T°C)
  Add 1.7% per 10°C above 20°C (subtract below)

Can't measure: soft surfaces, angled >15°, foam
```
