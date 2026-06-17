# Addressable LED (WS2812B / NeoPixel) — Component Reference

## What It Is

An addressable LED is an RGB (or RGBW) LED with a **built-in driver chip** inside the same package. You control each LED individually over a single data wire — no need to dedicate a pin per LED. Popular families: WS2812B (NeoPixel), APA102 (DotStar), and SK6812.

> **Analogy:** A strand of Christmas lights where you can tell each bulb "you be red, you be green, you be blue" — all through one wire.

## Addressable LED Families

### 1. WS2812B / WS2813 / SK6812 — Single-Wire (NeoPixel-type)

These use a **single data wire** + VCC + GND. Each LED listens, grabs its color, then passes remaining data downstream.

| Spec | WS2812B | WS2813 | SK6812 RGB | SK6812 RGBW |
|------|---------|--------|------------|-------------|
| Voltage | 5V (built-in regulator) | 5V | 5V or 3.3V options | 5V |
| Data rate | 800kHz | 800kHz | 800kHz | 800kHz |
| PWM per channel | 8-bit (256 steps) | 8-bit | 8-bit | 8-bit |
| Extra channel | — | — | — | White (W) |
| Breakpoint-resume | No | Yes (dual data) | No | No |
| Cost | $$ | $$$ | $ | $$ |

**WS2812B** — The most common. Found in NeoPixel strips, rings, matrices. Adafruit NeoPixel library supports them.

**WS2813** — Same protocol but has **dual data lines**: if one LED dies, data hops past it to the next. Useful for permanent installations where repair is hard.

**SK6812** — Drop-in replacement for WS2812B, often cheaper. The **RGBW** variant adds a 4th white channel (W) for proper white light without mixing R+G+B.

> **Protocol:** Each LED receives 24 bits (GRB order, not RGB!) at 800kHz. WS2812B expects: G7–G0, R7–R0, B7–B0. RGBW expects 32 bits: G, R, B, W. Timing is tight — the data pin is bit-banged, so **disable interrupts** when sending data on microcontrollers like Arduino.

### 2. APA102 / APA102C — Dual-Wire (DotStar)

Two-wire interface: **Clock (CI) + Data (DI)** + VCC + GND.

| Spec | APA102 | APA102C |
|------|--------|---------|
| Voltage | 5V | 5V |
| Data rate | Up to 20MHz (SPI) | Up to 20MHz (SPI) |
| PWM per channel | 8-bit | 8-bit |
| Global brightness | 5-bit (32 levels) | 5-bit (32 levels) |
| Cost | $$$ | $$ |

**Why choose DotStar over NeoPixel:**

| Advantage | DotStar (APA102) | NeoPixel (WS2812B) |
|-----------|-----------------|-------------------|
| Refresh rate | Much faster (SPI clock) | Limited by bit-bang timing |
| No interrupt problems | SPI hardware handles timing | Must disable interrupts |
| Global brightness | Hardware dim all LEDs at once | Must re-send all data |
| Data rate | 2–20MHz | Fixed 800kHz |

**Use DotStar when:** You need high frame rates (wearable animations), or you're running many LEDs and can't afford interrupt jitter, or you want to use hardware SPI.

**Use NeoPixel when:** You want the cheapest per-LED cost, you only have one free pin, or you're already using SPI for something else.

### 3. WS2801 / LPD8806 — Older Protocols

| Chip | Data rate | Voltage | Notes |
|------|-----------|---------|-------|
| WS2801 | 1MHz (SPI-like) | 5V | Older, larger package, 2-wire |
| LPD8806 | 25MHz (SPI) | 5V | 7-bit per channel (less color depth) |

These are less common in new designs but still found in older strips. Both use clock + data like APA102.

## Voltage: 5V vs 3.3V Data

**Most addressable LEDs run on 5V power** but expect **5V logic on the data pin**.

- If you're using a 3.3V microcontroller (ESP32, Raspberry Pi, Teensy 3.x), the 3.3V data signal may **not reliably hit the 0.7×VCC threshold** (~3.5V) that the LED chip needs.
- **Solution:** Use a **level shifter** (3.3V → 5V) on the data line. A 74AHCT125 or similar works.
- Some SK6812 variants are specified for 3.3V data — always check the datasheet.

> **Tip:** Many people run WS2812B from a 3.3V GPIO and it *mostly* works — until a long data wire adds noise, or temperature changes, or you add a second strip. If you want reliability, level-shift.

## Chaining

Addressable LEDs chain easily:

```
DATA OUT → DATA IN → DATA OUT → DATA IN → ...
```

Each LED passes the data packet **after removing its own 24/32 bits**. A microcontroller sends color data for all LEDs in one burst. More LEDs = more time to refresh.

**Total LEDs practical limits:**

| Microcontroller | Max LEDs at 30fps | Notes |
|----------------|-------------------|-------|
| Arduino Uno (16MHz) | ~500 | Data transfer takes ~30ms per 150 LEDs |
| ESP32 (240MHz) | ~1000+ | Much faster, can use RMT peripheral |
| Raspberry Pi | ~1000+ | Can use SPI or DMA for WS2812B |

## Power Injection — Voltage Drop

**The #1 mistake with long strips:** powering 300 LEDs from one end only.

- Each LED draws **~60mA at full white** (20mA per channel × 3 RGB).
- 60 LEDs at full white = 3.6A.
- 300 LEDs at full white = 18A.
- **Thin wires have resistance.** By LED #50 the voltage may drop below 4.5V and colors shift (red looks dim).

**When to inject power:**

| Strip length | LEDs | Power entry | What to do |
|-------------|------|-------------|------------|
| ≤1m | ≤60 | One end | Fine for most projects |
| 1–2m | 60–120 | Both ends | Add power at start and end |
| 2–5m | 120–300 | Every 50–100 LEDs | Inject 5V every meter |
| >5m | >300 | Every meter | Multiple injection points |

**Signs you need power injection:**
- LEDs near the end are dimmer or a different color (especially when showing white)
- Red LEDs look fine but blue/green are weak (blue/green drop out at lower voltage)
- The strip gets warm (copper trace resistance = heat)

> **Rule of thumb:** Run 5V and GND wires (at least 18AWG) alongside the strip and tap every meter. For very long runs, use 12V addressable strips (WS2815) and buck-convert locally.

## Decoupling Capacitor

**Always add a capacitor** between VCC and GND at the strip input.

| Value | Purpose |
|-------|---------|
| **470–1000µF** electrolytic | Bulk energy storage for current spikes |
| **0.1µF ceramic** (optional) | High-frequency noise suppression |

Without it, the inrush current when LEDs switch on can brown-out the microcontroller or cause flicker on other LEDs in the strip. Place it as close to the strip's VCC/GND as possible.

**Polarity:** Electrolytic capacitors are polarized. Negative leg goes to GND. Reversing it = explosion.

## Data Timing Constraints (WS2812B / SK6812)

The single-wire protocol uses **very specific** timing:

| Signal | Duration |
|--------|----------|
| T0H (bit 0 high) | ~0.35µs |
| T0L (bit 0 low) | ~0.80µs |
| T1H (bit 1 high) | ~0.70µs |
| T1L (bit 1 low) | ~0.60µs |
| RES | ≥50µs (latch/reset) |

- Total time for one LED: 24 bits × ~1.25µs = ~30µs
- 100 LEDs: ~3ms per frame
- 300 LEDs: ~9ms per frame

**If timing is off:** LEDs show wrong colors, flicker, or the first LED works but later ones don't. This happens when:
- Interrupts fire during data transmission
- You're using a too-slow microcontroller
- You're running at a non-standard clock speed

> **Best practice on Arduino:** Use the Adafruit NeoPixel library or FastLED — both handle timing with assembly-optimized routines. On ESP32, use the **RMT** (Remote Control) peripheral which generates the timing in hardware.

## Limiting Frame Rate

More LEDs = slower max frame rate.

| LEDs | Max smooth FPS | Notes |
|------|---------------|-------|
| 50 | ~600 | Overkill — human eye sees ~30–60fps |
| 100 | ~300 | Fine for animations |
| 300 | ~100 | Still good for animations |
| 600 | ~50 | Getting choppy for fast motion |
| 1000 | ~30 | OK for ambient, bad for video-reactive |

You can reduce color depth (e.g. 7-bit instead of 8-bit on FastLED) to double the update rate, or use a global brightness setting to reduce PWM artifacts.

## Quick Reference

```
WS2812B (NeoPixel): 1-wire data, 5V, 800kHz, 24-bit GRB, cheap
APA102 (DotStar):   2-wire (clock+data), 5V, SPI up to 20MHz, global dimming, more $$$
SK6812:             Drop-in for WS2812B, RGBW variant available
WS2813:             WS2812B + dual data (breakpoint resume)

Critical:
  - Always add 470–1000µF cap at strip VCC
  - Level-shift data if using 3.3V MCU
  - Inject power every 1-2 meters for long strips
  - 18AWG or thicker for injection wires
  - Each LED ~60mA at max white
  - GRB format (not RGB)
  - Disable interrupts during data send
```
