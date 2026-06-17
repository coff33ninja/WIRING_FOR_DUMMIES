# Real-Time Clock (DS3231 / DS1307) — Component Reference

## What It Is

A Real-Time Clock (RTC) module keeps accurate time — hours, minutes, seconds, date, month, year — even when the main microcontroller is powered off. It runs on a small backup battery (usually CR2032) and communicates over I2C.

> **Analogy:** The RTC is like a digital watch with its own battery, tucked inside your project. Your microcontroller pings it when it needs to know what time it is.

## DS3231 vs DS1307 — The Two You'll Actually Use

| Feature | DS3231 | DS1307 |
|---|---|---|
| Accuracy | ±2ppm (~1 minute per year) | ±2ppm... wait. No — it's actually ±2 **seconds per day** (~12 min/year without temp comp) |
| Temp compensation | Yes — crystal ovenized | No — crystal drifts with temperature |
| Built-in crystal | Yes (inside the package) | No — external 32.768kHz crystal |
| Crystal drift | Minimal (temperature-stabilized) | Major — the external crystal can drift ±20+ seconds/day in varying temps |
| Backup battery | CR2032 | CR2032 |
| Battery life | ~2–5 years | ~5–10 years (lower power draw) |
| Power consumption | ~200µA (running) / ~3µA (battery) | ~200µA (running) / ~0.5µA (battery) |
| SQW output | Yes (1Hz, 4kHz, 8kHz, 32kHz) | Yes (1Hz only) |
| Alarm output | Yes (two alarms) | No |
| Cost | ~$2–4 (module) | ~$1–2 (module) |
| 24-hour mode | Yes | Yes |
| 12-hour mode | Yes | Yes |

**The short version:** DS1307 is older, cheaper, and less accurate. The external crystal makes it a timebomb — literally, in the sense that your timekeeping will drift. DS3231 is the modern choice. Unless you're on a strict budget or working from old stock, **just buy DS3231**.

> **Why you almost never see DS1307 in new projects:** By the time you add the external crystal, the PCB space, and the headache of drift, the DS3231 is actually easier to use and more reliable. The price difference is under $2.

## Backup Battery — CR2032

The CR2032 coin cell keeps the RTC running when main power is off.

| What | Value |
|---|---|
| Type | CR2032 (3V lithium coin cell) |
| Capacity | ~225mAh |
| DS3231 draw on battery | ~3µA |
| DS1307 draw on battery | ~0.5µA |
| Lifespan (DS3231) | ~2–5 years |
| Lifespan (DS1307) | ~5–10 years |

**Installing the battery:**
- Positive (+) side faces **up** on most modules (marked on the holder)
- The battery only powers the RTC when main power is **off**
- If main power is on, the RTC uses main power and the battery is idle

**When the battery dies:**
- The RTC resets to a default date (usually 01/01/2000 or similar)
- Your project loses track of time until you set it again
- The module still works when USB/main power is connected — it just won't remember time after power-off

> **Warning:** Some cheap modules come with a **rechargeable LIR2032** instead of a CR2032. LIR2032 is 3.6V and will be overcharged by the module's charging circuit. If your module arrived with a silver battery with no markings, check the voltage — if it reads >3.3V fresh, it's an LIR. Replace with a CR2032.

## I2C Interface

Both DS3231 and DS1307 use I2C:

| Parameter | DS3231 | DS1307 |
|---|---|---|
| I2C address | 0x68 | 0x68 |
| Bus voltage | 2.3–5.5V | 4.5–5.5V (5V only!) |

**Important:** DS1307 is **5V only**. If connecting to a 3.3V MCU (ESP32, Raspberry Pi), you need a level shifter or use the DS3231 instead. DS3231 works at both 3.3V and 5V.

**Wiring:**

```
MCU (3.3V or 5V)        RTC Module
────────────           ──────────
VCC (3.3V or 5V)  ──── VCC
GND               ──── GND
SCL (pin 22)      ──── SCL (with 4.7kΩ pull-up to VCC)
SDA (pin 21)      ──── SDA (with 4.7kΩ pull-up to VCC)
```

Most RTC modules already have 4.7kΩ pull-up resistors on the I2C lines. Don't add another set if your MCU board also has them — you'll end up with ~2.35kΩ pull-ups, which is still OK but wastes current.

## SQW Output — Square Wave / Interrupt

The SQW pin can output a square wave signal:

| Setting | Frequency | Use case |
|---|---|---|
| 0 (default) | Disabled (high-impedance) | — |
| 1 | 1Hz | Second-pulse LED blink, timer ticks |
| 2 | 4.096kHz | — |
| 3 | 8.192kHz | Microcontroller clock substitute |
| 4 | 32.768kHz | External crystal replacement |

**DS1307** only supports 1Hz on SQW. **DS3231** supports all frequencies plus alarm output.

**Practical uses for SQW:**
- **Blink an LED** — connect SQW (1Hz) to an LED + 220Ω resistor. The LED blinks once per second, no MCU needed.
- **Wake up an ESP32 from deep sleep** — connect SQW (1Hz) to a GPIO configured for wake-on-pin-change. The RTC wakes the MCU at a specific time.
- **Generate a 32kHz clock** for a low-power MCU that doesn't have its own crystal.

## 24-Hour vs 12-Hour Mode

Both chips support both modes, controlled by a bit in the hour register.

- **24-hour mode:** Hours 0–23 (set by writing 0x00–0x17)
- **12-hour mode:** Hours 1–12 with AM/PM bit (set by writing 0x01–0x12 + AM/PM flag)

**Use 24-hour mode** unless you have a specific reason for 12-hour. It's simpler in code — no AM/PM flag to check, no 12-to-0 rollover edge case.

## DS3231's Integrated Crystal — The Big Advantage

The DS3231 has the 32.768kHz crystal **inside the package**, along with a temperature sensor and compensation circuitry.

**Why this matters:**
- The crystal is **temperature-compensated** — the DS3231 measures its internal temperature every 64 seconds and adjusts for crystal drift
- No external crystal = no PCB routing, no stray capacitance, no crystal mounting issues
- No crystal aging effects from solder stress or humidity

**The DS1307, on the other hand:**
- Uses an external 32.768kHz crystal (usually a cylindrical one on the module)
- The crystal is sensitive to temperature — a 10°C change can shift it by several seconds per day
- The crystal's load capacitors (12.5pF) must match — cheap modules often use the wrong caps, making drift worse
- Vibrations, PCB flex, and humidity all affect the external crystal

**Real-world difference:** A DS3231 might lose 1–2 minutes per **year**. A DS1307 might lose 5–15 minutes per **month** depending on ambient temperature swings.

## Alarm Functionality

DS3231 has **two configurable alarms**:

| Alarm | Trigger | Typical use |
|---|---|---|
| Alarm 1 | Second, minute, hour, day-of-week, or any combination | Wake at a specific time each day |
| Alarm 2 | Same as Alarm 1 (minute granularity only) | Second alarm, different time |

**What happens when an alarm fires:**
- The SQW pin goes low (if configured for alarm output)
- The alarm flag is set in the status register
- The INT/SQW pin triggers the MCU if connected to an interrupt-capable GPIO

**Common pattern:** Set Alarm 1 for 06:00 every day. The MCU goes into deep sleep. At 6 AM, the RTC pulls SQW low, waking the MCU. The MCU reads the time, does its work, then sets the alarm for the next day and goes back to sleep. Total power consumption: ~10µA during sleep + 200µA during operation.

## Why an RTC When ESP32 Has Built-in Time?

ESP32, ESP8266, Raspberry Pi, and many other MCUs have built-in RTC peripherals and can keep time over WiFi (NTP). So why add an external RTC?

| Reason | Explanation |
|---|---|
| **Power consumption** | The ESP32's deep-sleep RTC draws ~5µA. The DS3231 draws ~3µA. Combined: ~8µA. But WiFi NTP sync once per hour draws ~180mA for 5 seconds — that's 0.25mAh per sync. In a week, NTP syncs cost more power than an RTC running continuously for 2 years. |
| **MCU is off** | If your project is powered off entirely, the RTC keeps running on its coin cell. When power returns, the MCU asks "what time is it?" and the RTC knows — no NTP sync needed. |
| **No WiFi needed** | If your project doesn't have internet, the RTC is the only way to keep accurate time. |
| **Accuracy** | ESP32's internal RTC drifts ±5–30 seconds per day depending on temperature. DS3231 drifts ±1 minute per year. |
| **Battery backup** | The RTC's CR2032 lasts years. The ESP32's backup domain is powered by the same main supply — when that's off, the ESP32 loses time. |

**When you DON'T need an RTC:**
- Your project has permanent internet access and keeps time over NTP
- You only need relative time (millis() style — "how long since boot")
- Accuracy doesn't matter (± a few seconds per day is fine)
- The device is never fully powered off

## Quick Reference

```
RTC (DS3231)         RTC (DS1307)
─────────            ─────────
±2ppm (±1 min/yr)    ±1ppm... no, actually ±2 sec/day (~12 min/yr)
Temp compensated     No temp comp
Internal crystal     External crystal (drift city)
~$2–4                ~$1–2
3.3V or 5V           **5V only**
I2C address: 0x68    I2C address: 0x68
Two alarms, SQW      Single 1Hz SQW

I2C wiring:
  VCC → 3.3V or 5V
  GND → GND
  SCL → SCL (pull-up to VCC, usually on module)
  SDA → SDA (pull-up to VCC, usually on module)

Battery:
  Type:   CR2032 (NOT LIR2032)
  Life:   ~2–5 years (DS3231) / ~5–10 years (DS1307)
  Installed: Positive up on most modules

Why use one:
  - Keeps time when MCU is off (coin cell backup)
  - Lower power than NTP sync from WiFi
  - Accurate time without internet
  - Alarm can wake MCU from deep sleep

When to skip:
  - Always-on internet for NTP
  - Only need millis() timing
  - ±seconds/day drift is fine
```
