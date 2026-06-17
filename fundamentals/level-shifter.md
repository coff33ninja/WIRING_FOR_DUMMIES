# Level Shifter — Fundamental Reference

## What It Is

A level shifter (also called a logic level converter) is a circuit that **translates signals from one voltage to another**. It lets a 3.3V microcontroller talk safely to a 5V sensor, or vice versa, without letting the magic smoke out.

> **Why you need it:** A 5V signal on a 3.3V GPIO pin will **damage the pin** over time (or instantly). The ESP32's absolute max input is 3.6V. A level shifter is the bodyguard that stands between them.

## When You Need Level Shifting

| Scenario | Problem | Solution |
|----------|---------|----------|
| ESP32 → WS2812B LED strip | ESP32 outputs 3.3V, LEDs expect 5V data | Level shift data line to 5V |
| HC-SR04 Echo → ESP32 | Sensor outputs 5V, ESP32 can't take it | Level shift Echo to 3.3V |
| ESP32 → 5V I2C sensor | SDA/SCL are 3.3V, sensor expects 5V logic | Bidirectional level shifter on both lines |
| 5V Arduino → 3.3V sensor | Arduino outputs 5V, sensor expects 3.3V | Level shift signal lines down |

## Unidirectional vs Bidirectional

| Type | Signal flow | Used for |
|------|------------|----------|
| **Unidirectional** | One direction only | WS2812B data (ESP32 → LED), SPI (MOSI/MISO separate) |
| **Bidirectional** | Both directions on one wire | I2C (SDA and SCL both send and receive) |

## The 4 Main Ways to Level Shift

### 1. Voltage Divider (3.3V ← 5V — step DOWN only)

Two resistors to drop 5V to 3.3V. Simple, cheap, **one direction only** (cannot go 3.3V → 5V).

```
5V signal ──┬── R1 (10kΩ)
             │
             ├──── 3.3V output
             │
            R2 (20kΩ)
             │
            GND
```

**Use for:** HC-SR04 Echo pin, reading any 5V sensor with a 3.3V input.
**Don't use for:** I2C, WS2812B data, or any bidirectional communication.

### 2. 74AHCT125 / 74HCT125 (Unidirectional — 3.3V → 5V)

A dedicated logic chip that boosts 3.3V inputs to 5V outputs. It needs its own 5V supply. Four channels in one chip.

```
                 74AHCT125
            ┌─────────────────┐
     GND ───┤ OE1 (1)    VCC ├─── 5V
  3.3V in ──┤ 1A (2)    1Y  ├─── 5V out
            │    ...         │
            └─────────────────┘
```

**Use for:** WS2812B data line, SPI, any one-way 3.3V→5V conversion.
**Don't use for:** I2C (bidirectional).

### 3. BSS138 MOSFET Module (Bidirectional — works both ways)

The most common "level shifter" board on Amazon/eBay — a small PCB with 4 channels, each using a BSS138 MOSFET and two 10kΩ resistors. **Automatically works in both directions** without any direction control pin.

```
3.3V side          Module           5V side
───────           ───────           ───────
3.3V ────────────── LV ──────────── HV ─────── 5V
GND  ────────────── GND
GPIO ────────────── LV1 ─────────── HV1 ───── 5V device pin
GPIO ────────────── LV2 ─────────── HV2
                   ...
```

**Use for:** I2C, UART, any bidirectional communication.
**Works because:** When the 3.3V side pulls LOW, the MOSFET conducts and pulls the 5V side LOW too. When the 3.3V side goes HIGH, the MOSFET stops conducting and the 5V side is pulled HIGH by its own pull-up resistor.

### 4. TXS0108E / TXB0108 (Auto-Direction IC)

A more modern chip that detects direction automatically. Faster and more capable than the BSS138 module. Comes as a chip or pre-built module.

**Use for:** Higher-speed signals (SD cards, SPI at 10+ MHz).
**Downside:** More expensive, can be unstable with certain open-drain signals.

## Which One Should You Use?

| Application | Best choice |
|-------------|-------------|
| HC-SR04 Echo (5V → 3.3V) | Voltage divider (cheapest, simplest) |
| WS2812B data (3.3V → 5V) | 74AHCT125 (dedicated level shifter) |
| I2C any voltage mismatch | BSS138 MOSFET module (bidirectional) |
| General purpose, unknown | BSS138 MOSFET module |
| SD card, fast SPI | TXS0108E or TXB0108 |

## Wiring Example: BSS138 Module for I2C

```
ESP32 (3.3V)       BSS138 Module        5V I2C Device
───────────        ─────────────        ─────────────
3.3V ──────────────── LV ─────────────── HV ────────── 5V
GND  ──────────────── GND
GPIO 21 (SDA) ─────── LV1 ────────────── HV1 ──────── SDA
GPIO 22 (SCL) ─────── LV2 ────────────── HV2 ──────── SCL

Also connect:
  LV side pull-ups (4.7kΩ to 3.3V) if needed
  HV side pull-ups (4.7kΩ to 5V) if needed
```

## What Happens If You Skip It

| Scenario | Result |
|----------|--------|
| 5V signal into 3.3V GPIO (HC-SR04 Echo) | **GPIO pin dies** — can't read any input on that pin anymore |
| 3.3V data into 5V WS2812B | LEDs glitch, wrong colors, first LED behaves strangely |
| 5V I2C into 3.3V pins | Bus lockups, possible pin damage over time |
| Nothing — sometimes 5V works on 3.3V | It might work for a while, then fail unpredictably when voltage drops or rises |

> **The "it works without it" trap:** Sometimes 5V signals are close enough to 3.3V thresholds that they "work" for months. Then one day a voltage spike, a warm afternoon, or a slightly weaker power supply causes random crashes that are nearly impossible to debug. Level shifters are cheap insurance.

## Quick Reference

```
3.3V → 5V (one way)    → 74AHCT125 or TXS0108E
5V → 3.3V (one way)    → Voltage divider (2 resistors)
Both directions         → BSS138 MOSFET module (4-channel)
Cheapest                → Voltage divider (step down only)
Fastest                 → TXS0108E
Most common             → BSS138 MOSFET module
```

## See Also

- [neopixel-ws2812b](/projects/neopixel-ws2812b)
- [hc-sr04-ultrasonic](/projects/hc-sr04-ultrasonic)
- [i2c-devices](/projects/i2c-devices)
