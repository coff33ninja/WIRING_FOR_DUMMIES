# Microcontroller (ESP32 / Arduino / RP2040) — Component Reference

## What It Is

A microcontroller (MCU) is a tiny computer on a single chip — CPU, RAM, flash storage, and input/output peripherals all in one package. Unlike a desktop PC, it runs one program at a time with no operating system, and it responds to physical inputs (sensors, buttons) by controlling physical outputs (motors, LEDs, relays).

> **Analogy:** A tiny factory manager. It reads gauges (sensors), flips switches (outputs), follows a simple script (your code), and does nothing else until you reprogram it.

## MCU vs Raspberry Pi (Single-Board Computer)

| | Microcontroller (ESP32, Arduino, RP2040) | Raspberry Pi (SBC) |
|---|---|---|
| OS | None — bare metal (runs your code directly) | Full Linux OS (Raspberry Pi OS, Ubuntu) |
| Boot time | Instant (milliseconds) | 10–60 seconds (full OS boot) |
| Power | 10 mA–300 mA | 200 mA–2.5 A |
| Complexity | Simple — wire sensors, read/write pins | Complex — SD card, HDMI, USB stack |
| Real-time | Yes — deterministic timing | No — OS can delay IO (unless RT kernel) |
| Programming | Direct GPIO access (memory-mapped) | Via Linux sysfs, libgpiod, or libraries |
| Cost | $1–6 (chip), $3–15 (dev board) | $15–100+ |
| Storage | Flash (KB–MB), onboard | SD card (GB–TB), USB drives |
| Multitasking | Cooperative (loop) or RTOS | Full preemptive multitasking |
| Ethernet / USB | Rare (ESP32 has no USB host) | Built-in |

**Decision rule:** Use a microcontroller for anything that reads sensors and controls things. Use a Raspberry Pi when you need a screen, keyboard, internet browser, or complex software stack. Many projects use both — a Pi as the brain, an MCU as the real-time controller.

## Common Families

### ESP32 — The Swiss Army Knife

```
   ESP32 Block Diagram:
   ┌─────────────────────────────────────┐
   │  ┌─────────┐  ┌─────────┐  ┌────┐  │
   │  │ Core 0  │  │ Core 1  │  │ BT │  │
   │  │ 240 MHz │  │ 240 MHz │  │WiFi│  │
   │  └─────────┘  └─────────┘  └────┘  │
   │  ┌──────────────────────────────┐   │
   │  │  RAM: 520 KB                 │   │
   │  │  Flash: 4–16 MB              │   │
   │  │  GPIO: ~25 pins              │   │
   │  │  ADC: 2×12-bit (18 ch)       │   │
   │  └──────────────────────────────┘   │
   └─────────────────────────────────────┘
```

| Feature | Spec |
|---------|------|
| Voltage | 3.3V logic |
| CPU | Dual-core Xtensa LX6 @ 240 MHz |
| RAM | 520 KB SRAM (+ up to 8 MB PSRAM) |
| Flash | 4–16 MB (embedded, via SPI) |
| WiFi | 802.11 b/g/n (2.4 GHz) |
| Bluetooth | Classic + BLE |
| GPIO | ~25 (depending on package) |
| ADC | 2 × 12-bit SAR ADC (18 channels) |
| DAC | 2 × 8-bit |
| Peripherals | I2C, SPI, UART (3), I2S, CAN, RMT, Touch, Hall sensor |
| Deep sleep | ~10 µA |
| Price (chip) | ~$2–4 |

**What makes it special:** Built-in WiFi and Bluetooth. Dual-core. Two ADCs with 12-bit resolution. The most capable hobbyist MCU for IoT projects.

**Watch out for:** The ADC is nonlinear at the extremes (below 10% and above 90%). Some GPIOs are strapping pins that affect boot behavior (GPIO 0, 2, 12, 15).

---

### Arduino Uno (ATmega328P) — The Old Standard

```
   ATmega328P Block Diagram:
   ┌─────────────────────────────────┐
   │  ┌───────────┐                 │
   │  │ Core      │  RAM: 2 KB      │
   │  │ 16 MHz    │  Flash: 32 KB   │
   │  │(single)   │  EEPROM: 1 KB   │
   │  └───────────┘                 │
   │  GPIO: 14 digital + 6 analog   │
   │  ADC: 6×10-bit                 │
   └─────────────────────────────────┘
```

| Feature | Spec |
|---------|------|
| Voltage | 5V logic |
| CPU | ATmega328P, single-core @ 16 MHz |
| RAM | 2 KB SRAM |
| Flash | 32 KB (0.5 KB bootloader) |
| EEPROM | 1 KB |
| GPIO | 14 digital + 6 analog (Arduino pinout) |
| ADC | 6 × 10-bit |
| Peripherals | I2C, SPI, UART (1), PWM (6) |
| Power | ~5 mA idle, ~20 mA active |
| Price (chip) | ~$2 |
| Price (board) | ~$25 (genuine), ~$3 (clone) |

**What makes it special:** 5V logic — directly compatible with most sensors and modules without level shifters. Immense documentation and community. It's the "standard" that everything else is compared to.

**Watch out for:** 2 KB RAM is tiny — no strings, no large buffers, no MQTT payloads. 16 MHz is slow. No WiFi, no Bluetooth. Runs out of steam fast.

---

### RP2040 — The New Contender (Raspberry Pi Pico)

```
   RP2040 Block Diagram:
   ┌─────────────────────────────────────┐
   │  ┌─────────┐  ┌─────────┐  ┌────┐  │
   │  │ Core 0  │  │ Core 1  │  │ PIO │  │
   │  │ 133 MHz │  │ 133 MHz │  │ x2  │  │
   │  └─────────┘  └─────────┘  └────┘  │
   │  ┌──────────────────────────────┐   │
   │  │  RAM: 264 KB                 │   │
   │  │  Flash: 2 MB (on Pico board) │   │
   │  │  GPIO: 26 pins               │   │
   │  │  ADC: 4×12-bit               │   │
   │  └──────────────────────────────┘   │
   └─────────────────────────────────────┘
```

| Feature | Spec |
|---------|------|
| Voltage | 3.3V logic |
| CPU | Dual-core Cortex-M0+ @ 133 MHz |
| RAM | 264 KB SRAM |
| Flash | 2 MB (on Pico board; QSPI external) |
| GPIO | 26 |
| ADC | 4 × 12-bit |
| Peripherals | I2C (2), SPI (2), UART (2), USB 1.1, PWM (16 ch) |
| PIO | 8 state machines (programmable IO) |
| Power | ~5 mA idle, ~40 mA active |
| Price (board) | ~$4 (Pico) |

**What makes it special:** Dual-core at a $4 price. **PIO** (Programmable IO) — tiny processors that can emulate custom digital interfaces (WS2812 LEDs, DVI video, SD cards) without CPU involvement. USB 1.1 host/device onboard. Best value for raw compute.

**Watch out for:** No WiFi, no Bluetooth (add a Pico W for WiFi, but that uses the PIO for the WiFi chip). 3.3V only — needs level shifters for 5V peripherals.

## Key Specs — How to Compare MCUs

### GPIO Count — How Many Things Can You Connect?

| MCU | Total GPIO | Usable in typical project |
|-----|-----------|--------------------------|
| ATmega328P (Arduino) | 20 | 14–16 (RX/TX used for serial) |
| ESP32 | 25 | 16–18 (some reserved for strapping, flash) |
| RP2040 | 26 | 24 (one used for ADC VREF) |

**Practical rule:** Count your required pins (LEDs + sensors + UART + I2C + SPI). Double it. If you're over, get a bigger MCU or use a shift register / multiplexer.

### ADC — Reading Analog Voltages

| MCU | Channels | Resolution | Voltage range | Notes |
|-----|----------|------------|---------------|-------|
| ATmega328P | 6 | 10-bit (0–1023) | 0–5V | Simple, accurate, 5V reference |
| ESP32 | 18 | 12-bit (0–4095) | 0–3.3V | Non-linear at extremes (0–10%, 90–100%) |
| RP2040 | 4 | 12-bit (0–4095) | 0–3.3V | Noisy — averaging helps |

**Why it matters:** If you need to read a potentiometer, temperature sensor, or light sensor — ADC resolution determines how precise your reading is.

- 10-bit = 1024 steps (0–1023) → ~5 mV per step at 5V
- 12-bit = 4096 steps (0–4095) → ~0.8 mV per step at 3.3V

ESP32 ADC is notorious for non-linearity near VCC and GND. If your sensor signal is near 0V or 3.3V, the readings will be inaccurate. Use a voltage divider to center it in the linear range.

### Clock Speed — How Fast Does It Think

| MCU | Speed | Instructions per second (approx) |
|-----|-------|----------------------------------|
| ATmega328P | 16 MHz | ~16 MIPS |
| ESP32 | 240 MHz | ~600 MIPS (dual-core) |
| RP2040 | 133 MHz | ~133 MIPS (dual-core Cortex-M0+) |

**Don't obsess over clock speed.** 16 MHz is enough for reading a sensor every second. 240 MHz matters for audio processing, real-time control loops, or running TLS encryption. For blinking LEDs and reading buttons, even 16 MHz is overkill.

### Flash and RAM — How Much Code and Data

| MCU | Flash (code storage) | RAM (runtime data) | Limits |
|-----|---------------------|--------------------|--------|
| ATmega328P | 32 KB | 2 KB | No large strings, no JSON parsing |
| ESP32 | 4–16 MB | 520 KB (+PSRAM) | Can run web servers, TLS, large buffers |
| RP2040 | 2 MB | 264 KB | Medium — can run MicroPython, moderate data |

**Flash fills fast:**
- Blink without delay: ~2 KB
- WiFi + MQTT (ESP32): ~300 KB
- Full web server + SPIFFS: ~1 MB
- MicroPython firmware: ~1.5 MB

**RAM runs out faster:**
- JSON document for a few fields: ~2 KB
- JPEG buffer (320×240): ~75 KB
- Audio buffer (1 second @ 16 kHz, 16-bit): ~32 KB
- MQTT client + WiFi stack (ESP32): ~100 KB

**ATmega328P warning:** 2 KB RAM means you cannot use `String` objects, large arrays, or dynamic allocation in any meaningful way. Plan every byte.

## Voltage Level — 3.3V vs 5V (The Biggest Wiring Decision)

```
   5V MCU                        3.3V MCU
   ┌─────┐                       ┌─────┐
   │ OUT │── HIGH = 5V ──────────│ IN  │ CAN'T ACCEPT 5V
   │ OUT │── 5V ── level shifter ── IN  │ Safe
   └─────┘                       └─────┘

   3.3V MCU                      5V MCU
   ┌─────┐                       ┌─────┐
   │ OUT │── HIGH = 3.3V ────────│ IN  │ Reads as HIGH (threshold ~3V)
   └─────┘                       └─────┘
```

**Why this matters:**

| If you connect | Result |
|----------------|--------|
| 5V output to 3.3V GPIO pin | Damages the 3.3V MCU |
| 3.3V output to 5V GPIO pin | May or may not read as HIGH (5V threshold is ~3V) |

**The fix — Level Shifters:**

- **Bidirectional level shifter module** (BS170 + resistors) — best for I2C (which is bidirectional)
- **Voltage divider** — best for unidirectional signals (TX → RX)
- **74LVC245 / 74HCT245** — best for data buses (SPI, parallel)

**Common level shifting for 5V → 3.3V (unidirectional):**

```
   5V TX ── 1kΩ ──┬── 2kΩ ── GND
                  │
                  └── 3.3V RX (~3.3V)
```

**General rule for beginners:** Start with an Arduino (5V) if you want everything to "just work" with 5V sensors. Start with an ESP32 (3.3V) if you want WiFi, Bluetooth, and more capability. Buy a level shifter module ($2) to bridge the gap between 3.3V and 5V parts.

### Pin Current Limits

| MCU | Max per pin | Total VCC/GND | Practical limit per pin |
|-----|------------|----------------|------------------------|
| ATmega328P | 40 mA | 200 mA | 20 mA (LED direct) |
| ESP32 | 40 mA | 1 A (total) | 12 mA (safe for LED) |
| RP2040 | 50 mA | 500 mA | 15 mA |

**LED direct drive:** With a 220Ω resistor, a 20 mA LED draws ~15–18 mA. All three MCUs can handle this. But if you drive 10 LEDs at once on an ATmega328P, you're at 150–180 mA — close to the 200 mA total limit.

**What this means:**

- You don't need a transistor for a single LED (resistor is enough)
- You DO need a transistor or MOSFET for motors, relays, solenoids, or any load over 40 mA
- Running 20 LEDs directly = blowing the MCU's total current limit → use a shift register or ULN2003

## Special Function Pins — Not All Pins Are Equal

### Arduino Uno (ATmega328P)

| Pin | Special function | Don't use for |
|-----|-----------------|---------------|
| 0 (RX) | Serial receive | General IO if using Serial |
| 1 (TX) | Serial transmit | General IO if using Serial |
| 2–3 | External interrupts (INT0, INT1) | — |
| 3, 5, 6, 9, 10, 11 | PWM output (uses timer) | — |
| A4 (SDA), A5 (SCL) | I2C | General IO if using I2C |
| 10 (SS), 11 (MOSI), 12 (MISO), 13 (SCK) | SPI | General IO if using SPI |
| A6, A7 | Analog input only (no digital) | Digital output |
| 13 | Built-in LED (also SCK) | — |

### ESP32 Dev Board

| Pin | Special function | Don't use for |
|-----|-----------------|---------------|
| 0 | Strapping pin (boot mode) | Output (pulled LOW disables boot) |
| 2 | Strapping pin (boot mode), built-in LED | Output only (safe for LED) |
| 5 | Strapping pin (CS for flash) | Output (boot fails if pulled LOW) |
| 6–11 | Connected to internal flash | General IO (using them corrupts flash) |
| 12 | Strapping pin (voltage) | Pull-up = 1.8V flash mode (brick risk) |
| 14 | Not special | Safe |
| 15 | Strapping pin (debug logging) | Output (boot fails if pulled HIGH) |
| 34–39 | Input only (no pull-up, no output) | Output |
| TX0 (1), RX0 (3) | Serial console (USB) | — |

**ESP32 strapping pins rule:** Pins 0, 2, 5, 12, 15 control boot behavior. If you pull them HIGH or LOW on power-up, the ESP32 may fail to boot. Always check a pinout diagram for your specific board.

### RP2040 (Raspberry Pi Pico)

| Pin | Special function | Don't use for |
|-----|-----------------|---------------|
| 29 (ADC_VREF) | ADC voltage reference (3.3V) | Output |
| 23 | Runs state machine (PIO) | — (PIO isn't GPIO) |
| 24–26 | VSYS, 3V3_EN, 3V3 | Power, not GPIO |
| 1 (GP0) / 2 (GP1) | UART0 TX/RX by default | — |
| 4 (GP2) / 5 (GP3) | I2C1 SDA/SCL by default | — |
| 6 (GP4) / 7 (GP5) | I2C0 SDA/SCL by default | — |
| 24 (GP18) / 25 (GP19) | SPI0 TX/RX by default | — |
| 30 (RUN) | Reset (active low) | IO |
| All | Can be remapped — PIO is flexible | Most pins can be anything |

**RP2040 flexibility:** Most pins are interchangeable — you can assign UART, I2C, SPI, or PWM to almost any pin. This is not true for the ATmega328P or ESP32.

## Which MCU Should You Use?

| Project | Recommendation | Why |
|---------|---------------|-----|
| Learn electronics basics | Arduino Uno (clone) | 5V, simple, huge community, tutorials for everything |
| IoT sensor (battery) | ESP32 | WiFi, deep sleep, lots of RAM for TLS |
| IoT sensor (wired power) | ESP8266 (if cheap), ESP32 (if not) | Both work; ESP32 is better value now |
| Bluetooth sensor | ESP32 | Built-in BLE + Classic |
| LED strip / matrix | RP2040 (Pico) | PIO drives WS2812 without CPU load |
| Audio processing | ESP32 or RP2040 | ESP32: I2S + DSP. RP2040: PIO for custom protocols |
| Many analog sensors | ESP32 | 18 ADC channels (even if non-linear) |
| USB keyboard/mouse | RP2040 | Native USB 1.1 host/device |
| Real-time control | ATmega328P or RP2040 | Simple, deterministic, no WiFi overhead |
| Plug into a Pi | RP2040 | Same ecosystem, 3.3V, PIO for custom IO |
| Total beginner budget | Arduino Nano clone ($2) | Breadboard-friendly, 5V, same as Uno |

## Common Mistakes

| Mistake | Result |
|---------|--------|
| 5V signal into 3.3V GPIO | Damaged pin (sometimes works once, then dies) |
| Powering ESP32 from Arduino's 3.3V pin | Brownouts — insufficient current |
| Forgetting strapping pins on ESP32 | ESP32 won't boot or behaves erratically |
| Running 20 LEDs directly from ATmega328P | Exceeds total current limit → chip gets hot, resets |
| Using `String` objects on ATmega328P | Heap fragmentation → crash after minutes/hours |
| Connecting a motor directly to GPIO | Kills the pin (needs transistor/flyback diode) |
| I2C without pull-up resistors | Bus stuck LOW — no communication |
| Not connecting GND between boards | Floating signals — random readings, no communication |
| ADC on ESP32 measuring near 3.3V | Inaccurate — readings top out at ~3.0–3.1V |
| Using pin 0 on ESP32 as output | Boot fails if pulled LOW |

## Quick Reference

```
                ATmega328P        ESP32             RP2040 (Pico)
Voltage         5V                3.3V              3.3V
Cores           1                 2                 2
Speed           16 MHz            240 MHz           133 MHz
RAM             2 KB              520 KB (+PSRAM)   264 KB
Flash           32 KB             4–16 MB           2 MB
GPIO            20                25                26
ADC             6×10-bit          18×12-bit         4×12-bit
WiFi            No                Yes (built-in)    No (Pico W: external)
Bluetooth       No                Yes (dual-mode)   No
Price (board)   $3 (clone)        $3–6              $4
USB             No (via serial)   No (via serial)   Yes (USB 1.1)
Special trick   Simple, 5V, huge   WiFi+BT, dual-core,   PIO, USB, $4
                community         ADC non-linear

Level shifting needed:
  5V MCU → 3.3V module:  level shifter on module RX
  3.3V MCU → 5V module:  usually safe (threshold ~3V)
  I2C: use bidirectional level shifter module

Pin current limits:
  Per pin: 20–40 mA (safe: 15 mA)
  Total:   200 mA (ATmega), 1 A (ESP32), 500 mA (RP2040)
  Motor/relay/solenoid: use MOSFET (never direct GPIO)

Strapping hazards (ESP32):
  GPIO 0 (boot), GPIO 2, GPIO 5, GPIO 12, GPIO 15
  Do not pull these HIGH/LOW at boot unless you mean to
```
