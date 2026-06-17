# Optocoupler / Optoisolator — Component Reference

## What It Is

An optocoupler (also called optoisolator) is a chip that transfers electrical signals using **light** instead of direct electrical connection. It's an LED and a light-sensitive component inside a single package, with a gap between them.

> **Analogy:** Two people in soundproof rooms. One flashes a flashlight (LED) at a window. The other sees the flashes and writes them down (phototransistor). No sound passes through — only light. The two rooms are electrically isolated.

## Why Use One

| Problem | How optocoupler fixes it |
|---------|------------------------|
| Microcontroller at 3.3V, device at 12V/120V/240V | The gap means high voltage CANNOT reach your MCU |
| Relay coil creates voltage spikes | Isolates the spike from your GPIO |
| Ground loops between two circuits | No shared electrical path — grounds can be at different voltages |
| Device fails and shorts to mains | The gap means 240V never reaches your ESP32 |

## The 4 Optocoupler Types — Which Output You Need

### 1. Phototransistor Output — Standard (PC817, 4N35, TLP521)

Most common. Output is a phototransistor — current flows when LED is on. Acts like a **switch** to ground (open-collector).

| Pros | Cons |
|------|------|
| Cheap, widely available | Slower (~1–10µs switching) |
| Good for DC signals up to ~50kHz | Gain varies between units |
| Easy to wire — simple on/off | |

**Use for:** GPIO isolation, relay driver isolation, digital signal crossing, voltage translation (3.3V ↔ 5V/12V/24V).

**Common parts:** PC817 (4-pin), 4N35 (6-pin with base pin), TLP521 (4-pin).

**The base pin (4N35):** Six-pin optocouplers expose the phototransistor's base pin. You can leave it unconnected for standard operation, or pull it to ground with a resistor to speed up turn-off.

### 2. Photo-Darlington Output — High Gain (4N32, TLP127)

Output is a Darlington pair (two transistors) — very high current gain.

| Pros | Cons |
|------|------|
| Very high gain — can drive loads directly | Slower than single phototransistor |
| Can switch higher current | Higher saturation voltage (1V+ instead of 0.3V) |

**Use for:** Driving relays directly without an external transistor, when input current is very limited.

**Downside:** The Darlington configuration slows switching speed significantly — don't use for anything above ~1kHz.

### 3. Photodiode + Logic Output — Fast Digital (6N137, HCPL2601)

Output is a photodiode driving a logic gate (Schmitt trigger). Gives a clean digital signal.

| Pros | Cons |
|------|------|
| Very fast — 10Mbit/s+ | More expensive |
| Clean digital output (no analog mess) | Needs more pins |
| Schmitt trigger — noise immune | |

**Use for:** Digital communication crossing isolation barriers (SPI, I2C, UART), high-speed signals, industrial fieldbus.

### 4. TRIAC / SCR Output — AC Loads (MOC3063, MOC3021)

Output is a TRIAC or SCR — designed for switching **AC** loads directly.

| Pros | Cons |
|------|------|
| Switches AC directly (lights, motors, heaters) | DC only (TRIAC latches on DC) |
| Zero-crossing versions (MOC3063) switch at voltage zero — less noise | Needs external TRIAC for high current |
| Can control mains voltage with 3.3V logic | |

**Use for:** Dimming AC lights with PWM, switching AC fans, controlling 120V/240V loads from a microcontroller.

**Zero-crossing vs random-phase:**
- **MOC3063 (zero-crossing):** TRIAC only turns on when AC voltage crosses zero. Use for simple on/off — no radio noise.
- **MOC3021 (random-phase):** TRIAC turns on at any point in the AC cycle. Use for phase-control dimming (light dimmers).

## Anatomy — What's Inside

```
Phototransistor type (4N35 / PC817):

      Pin 1 ──┬── LED + ──┐         ┌── Collector ── Pin 6 (or 3)
              │           │         │
              │           │  LIGHT  │
      Pin 2 ──┴── LED − ──┘         │
                                    └── Emitter ──── Pin 4 (or 4)
                                        Base ────── Pin 5 (4N35 only)
```

| Pin | PC817 (4-pin) | 4N35 (6-pin) |
|-----|---------------|-------------|
| 1 | Anode (+) | Anode (+) |
| 2 | Cathode (−) | Cathode (−) |
| 3 | Emitter | Emitter |
| 4 | Collector | N/C (no connection) |
| 5 | — | Base |
| 6 | — | Collector |

> **Always check the datasheet** — pinouts vary between manufacturers and packages. DIP-4 and DIP-6 are common, but SOP-4 and SOP-5 SMD packages exist too.

## Common Optocouplers

| Part | Pins | Output type | Speed | Use |
|------|------|-----------|-------|-----|
| **PC817** | 4 | Phototransistor | ~50kHz | General GPIO isolation, relay modules |
| **4N35** | 6 | Phototransistor | ~10kHz | General purpose, has base pin for speed tuning |
| **4N32** | 6 | Photo-Darlington | ~1kHz | High gain, drive relay directly |
| **TLP127** | 4 | Photo-Darlington | ~1kHz | High gain, SMD available |
| **6N137** | 8 | Logic (Schmitt) | 10Mbit/s | Fast digital isolation |
| **HCPL2601** | 8 | Logic (Schmitt) | 10Mbit/s | Industrial digital isolation |
| **MOC3063** | 6 | TRIAC (zero-cross) | AC line | Mains on/off switching, dimmers |
| **MOC3021** | 6 | TRIAC (random-phase) | AC line | Phase-control dimming |
| **IL300** | 8 | Photodiode (linear) | DC to ~200kHz | Analog isolation (audio, ADC) |

## How to Wire It

### Standard Digital Isolation (Phototransistor)

```
GPIO side                      Load side
─────────                      ─────────
3.3V                           VCC_load (could be 5V, 12V, or 24V)
  │                              │
220Ω                             │
  │                              │
GPIO ────┬─── Anode (PC817/1)    │ 10kΩ pull-up
         │                       │   │
GND  ────┴─── Cathode (2)        │   │
                            Emitter(4)──┴──── GPIO_read (or relay transistor base)
                            Collector(3) ──── GND_load
```

The phototransistor is **open-collector** — it can only pull to ground. You must add a pull-up resistor to the load-side VCC.

### Driving a Relay Directly (Photo-Darlington, 4N32)

```
GPIO side                      12V side
─────────                      ────────
3.3V                           12V
  │                              │
1kΩ                              │
  │                              │
GPIO ────┬─── Anode (1)          │
         │               Coil(4)─┴──── Relay coil (12V, ~100mA)
GND  ────┴─── Cathode (2)        │
                            Emitter(5)──── GND_load
                                   1N4007 flyback diode across coil
```

The Darlington's high gain means the optocoupler's output current is enough to energize the relay directly — no external transistor needed.

### Switching AC (MOC3063 + External TRIAC)

```
GPIO side                      Mains side (~120/240V AC)
─────────                      ────────────────────────
3.3V                           AC Live
  │                              │
180Ω                             │
  │                              │          ┌───── AC Load
GPIO ────┬─── Anode (1)    MT2(6)┼──────────┤ (light, motor)
         │                      │          │
GND  ────┴─── Cathode (2)   MT1(4)┼──────┐  └─────────────┘
                              Gate(5)┼──┐  │
                                 BTA16 │  │
                                 TRIAC │  │
                                   │   │  │
                                  GND AC Neutral
```

The MOC3063 drives the gate of a high-power TRIAC. The MOC's internal LED is controlled by the GPIO. The zero-crossing feature means the TRIAC only turns on at AC zero-crossing — minimal electrical noise.

### Analog Isolation (IL300 — Linear Optocoupler)

For audio or sensor signals that must stay accurate across the isolation barrier. The IL300 contains a photodiode on both input and output sides + a feedback photodiode to linearize the response — it's a whole different class from simple on/off optocouplers.

**Use for:** Medical isolation amplifiers, audio equipment with ground elimination, precision analog sensor isolation.

## Input Resistor

The optocoupler's internal LED needs a current-limiting resistor, like any LED.

| Optocoupler | LED forward voltage (Vf) | Typical input current |
|-------------|-------------------------|----------------------|
| PC817 | ~1.2V | 5–10mA |
| 4N35 | ~1.2V | 10mA |
| 6N137 | ~1.4V | 6.5mA (higher speeds need more current) |
| MOC3063 | ~1.2V | 10–15mA |

```
R = (Vgpio - Vf) / I

At 3.3V with PC817 (Vf=1.2V, I=10mA):
  R = (3.3 - 1.2) / 0.01 = 210Ω → use 220Ω

At 5V with PC817:
  R = (5 - 1.2) / 0.01 = 380Ω → use 390Ω
```

**Relay modules already have this resistor built in.** If wiring a bare optocoupler, add 180–470Ω in series with the input pin.

## Which Type to Use

| Need | Output type | Part |
|------|------------|------|
| Isolate a GPIO signal (basic) | Phototransistor | PC817 or 4N35 |
| Isolate a relay driver | Phototransistor | PC817 (already on relay modules) |
| Drive a relay without external transistor | Photo-Darlington | 4N32 or TLP127 |
| Fast digital (UART, SPI across barrier) | Logic (Schmitt) | 6N137 or HCPL2601 |
| Switch AC light/motor on/off | TRIAC zero-cross | MOC3063 |
| Dim an AC light (PWM) | TRIAC random-phase | MOC3021 |
| Isolate an analog signal precisely | Linear photodiode | IL300 |
| Basic 3.3V ↔ 5V level shifting | Phototransistor | PC817 (cheap but slow) |

## What Happens If You Choose Wrong

| Mistake | Result |
|---------|--------|
| Phototransistor for 1Mbit/s UART | Data corrupted — too slow |
| Photo-Darlington for fast signal | Output lags — never reaches high state in time |
| MOC3021 for AC on/off (no dimming) | Works, but causes RF noise at every switch |
| MOC3063 for phase-control dimming | Won't dim — zero-crossing prevents it |
| 4N35 without pull-up resistor | Output never goes high — stuck at 0V |
| Standard optocoupler for analog signal | Horrible distortion — non-linear LED-to-output |

## Quick Reference

```
Input side (always):
  Anode → current-limiting resistor (220Ω for 3.3V) → GPIO
  Cathode → GND

Output side depends on type:
  Phototransistor:    open-collector → pull-up to load-side VCC
  Photo-Darlington:   open-collector → higher current drive
  Logic (Schmitt):    digital output → direct to MCU input
  TRIAC:              drives TRIAC gate for AC loads

Phototransistor speed:  ~1–10µs (not for fast digital)
6N137 speed:            ~10Mbit/s (good for UART/SPI)

Common parts by job:
  Basic isolation:   PC817 (DIP-4, cheapest)
  Fast digital:      6N137 (DIP-8)
  AC switching:      MOC3063 (zero-cross) or MOC3021 (random-phase)
  High gain:         4N32 (Darlington)
```
