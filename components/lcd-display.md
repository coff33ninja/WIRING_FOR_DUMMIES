# LCD Display (1602 / I2C) — Component Reference

## What It Is

A character LCD display shows text on a grid using a **reflective or backlit panel** controlled by a Hitachi **HD44780** (or compatible) driver chip. The most common sizes are **16 characters × 2 rows** (1602) and **20 × 4** (2004). They can work in parallel mode (needing many GPIO pins) or with an **I2C backpack** (needing only 2 wires).

> **Analogy:** A digital name tag — you tell it which pre-built characters go where, and it lights up the right segments.

## Common Sizes

| Size | Characters | Rows | Typical uses |
|------|-----------|------|-------------|
| 1602 | 16 | 2 | Most common — menus, sensor readouts |
| 1604 | 16 | 4 | Compact but more lines |
| 2004 | 20 | 4 | More info — status screens, settings |
| 2002 | 20 | 2 | Rare, but exists |

All use the HD44780 controller (or clone) internally.

## HD44780 Controller

The HD44780 is the standard driver for character LCDs. Key facts:

- **RAM:** 80 bytes of DDRAM (display data). 1602 uses 16×2 = 32, 2004 uses 20×4 = 80.
- **Character ROM:** Pre-defined 5×8 pixel character set (ASCII + Japanese + custom characters).
- **Custom characters:** Up to 8 user-defined characters (8 bytes each).
- **Command set:** Clear, home, entry mode, cursor on/off, blink, shift, etc.

**Pinout (16-pin standard):**

| Pin | Name | Function |
|-----|------|----------|
| 1 | VSS | Ground |
| 2 | VDD | +5V power |
| 3 | V0 | Contrast adjust (analog voltage) |
| 4 | RS | Register Select (0=command, 1=data) |
| 5 | RW | Read/Write (0=write, 1=read — usually GND) |
| 6 | E | Enable (pulse high to latch) |
| 7–14 | D0–D7 | Data bus (8-bit or 4-bit mode) |
| 15 | A | Backlight anode (+5V via resistor) |
| 16 | K | Backlight cathode (GND) |

## 8-Bit vs 4-Bit Parallel Mode

You can talk to the LCD using either 8 or 4 data lines. **4-bit mode** is standard for hobby projects because it saves GPIO pins.

| Mode | Pins needed (excluding power) | Speed | When to use |
|------|-------------------------------|-------|-------------|
| **8-bit** | RS + E + D0–D7 = 10 pins | Faster (1 byte per cycle) | When you have pins to spare |
| **4-bit** | RS + E + D4–D7 = 6 pins | Slower (2 nibbles per byte) | Default for Arduino projects |
| **I2C backpack** | SDA + SCL = 2 pins | Slowest (serial) | When pins are tight |

**Wiring for 4-bit mode (6 pins):**

```
LCD Pin   → MCU GPIO
RS        → Pin 12
E         → Pin 11
D4        → Pin 5
D5        → Pin 4
D6        → Pin 3
D7        → Pin 2
RW        → GND (always write)
```

## Contrast Adjust (Potentiometer)

Pin 3 (V0) controls **contrast** — the voltage that biases the LCD glass.

- Too high: characters are invisible (all segments dark)
- Too low: characters are invisible (no segments show)
- Just right: dark characters on clear background

**Always use a 10kΩ potentiometer:**

```
    +5V
     │
     ├── Pot wiper ─── LCD pin 3 (V0)
     │
    GND
```

Turn the pot until characters are clearly visible. This adjustment is temperature-sensitive — you might need to re-tweak in a hot or cold room.

> **If you skip the contrast pot:** Tie V0 to GND through a 1–2kΩ resistor. This works for many displays but the contrast may be poor. Always use a pot for first bring-up.

## Backlight (LED with Resistor)

The backlight is an LED (or LED string) inside the LCD module. It needs a current-limiting resistor.

| Backlight config | Typical forward voltage | Typical current |
|-----------------|------------------------|-----------------|
| Standard LED backlight | ~3.0–3.4V | ~20–100mA |
| RGB backlight (rare) | ~3.0V per color | ~20mA each |

**Resistor calculation:**

For 5V supply, 3.2V Vf, 50mA desired:

R = (5V – 3.2V) / 0.05A = 36Ω → use 33Ω or 47Ω

```
LCD pin 15 (A) ───── Resistor ───── +5V
LCD pin 16 (K) ──────────────────── GND
```

**PWM dimming:** Put the resistor on the anode side, and drive the cathode (pin 16) with a **N-channel MOSFET** or NPN transistor controlled by a PWM GPIO pin. This lets software dim the backlight.

> **Warning:** Do not connect LCD pin 15 directly to 5V without a resistor. The backlight will draw more current than rated and burn out or damage the LCD.

## I2C Backpack (PCF8574)

An **I2C backpack** is a small board that sits on the back of the LCD and converts I2C serial to parallel signals. It's built around the **PCF8574** I/O expander chip.

**What the backpack does:**

```
I2C (SDA/SCL) ──→ PCF8574 ──→ 8 parallel outputs
                                │
                              RS, RW, E, D4, D5, D6, D7, Backlight
```

**I2C address:**

| Chip | Typical address | Address range |
|------|----------------|---------------|
| PCF8574 | **0x27** | 0x20–0x27 |
| PCF8574A | **0x3F** | 0x38–0x3F |

**If your LCD doesn't show anything:**
- Run an I2C scanner sketch — it will report the address
- Try 0x27 first, then 0x3F
- Some cheap backpacks have solder pads (A0, A1, A2) to change the address

**Common library:** `LiquidCrystal_I2C` (by Frank de Brabander or Marco Schwartz). For the `hd44780` library family, use `hd44780_I2Cexp`.

**Wiring (I2C backpack):**

```
Backpack VCC ─── +5V
Backpack GND ─── GND
Backpack SDA ─── MCU SDA (A4 on Uno, 21 on Mega, GPIO 21 on ESP32)
Backpack SCL ─── MCU SCL (A5 on Uno, 22 on Mega, GPIO 22 on ESP32)
```

### I2C Address Conflicts

Common I2C devices may fight with your LCD:

| Device | Address | Conflict? |
|--------|---------|-----------|
| BMP280/BME280 | 0x76/0x77 | No |
| MPU6050 | 0x68 | No |
| DS3231 RTC | 0x68 | **Yes — change RTC or LCD address** |
| OLED SSD1306 | 0x3C | No (0x3D also possible) |
| PCF8574A backpack | 0x3F | Possibly — check scanner |

**Fix a conflict:** Change the backpack's address by soldering A0/A1/A2 pads, or choose a device with a different address range.

## Limitations

Character LCDs are simple and reliable but have real limits:

| Limitation | Why it matters |
|------------|----------------|
| **Slow refresh** | Internal controller takes ~1–40ms per command. 1602 full refresh ~100ms. No video or fast animation. |
| **No graphics** | Only pre-defined 5×8 characters. No pixel-level control. Use an OLED or TFT for graphics. |
| **5V only** | Most HD44780 displays don't work at 3.3V. I2C backpack might need 5V too. |
| **Temperature sensitivity** | Contrast drifts with temperature. Outdoor projects need auto-contrast or temp compensation. |
| **Limited custom characters** | Only 8 user-defined characters. For custom icons you must reuse or swap them mid-frame. |
| **Viewing angle** | TN-style LCD has a best viewing angle — you must mount it correctly or it washes out. |

**When NOT to use a character LCD:**
- You need to display images, graphs, or animations → use OLED or TFT
- You need a fast-updating display (FPS > 10) → use OLED
- You need 3.3V operation → use OLED SSD1306
- Space is very tight → use OLED (smaller, no backpack)

## Quick Reference

```
Sizes:       1602 (16×2), 2004 (20×4)
Controller:  HD44780 (or clone)

Parallel:    8-bit (10 pins) or 4-bit (6 pins)
I2C:         PCF8574 backpack → 2 pins (SDA/SCL)
             Addresses: 0x27 (PCF8574) or 0x3F (PCF8574A)

Contrast:    10kΩ pot on V0 pin — always include it
Backlight:   Resistor on pin 15 (e.g. 47Ω for 5V)
             PWM on cathode side for dimming

Limits:
  - Text only (5×8 character grid)
  - Slow (~100ms full refresh)
  - 5V only
  - 8 custom characters max

First bring-up:
  1. Power LCD, adjust contrast pot
  2. If blank, check pot and I2C address
  3. Run I2C scanner to find address
```
