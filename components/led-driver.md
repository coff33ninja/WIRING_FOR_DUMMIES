# LED Driver (MAX7219) — Component Reference

## What It Is

The MAX7219 is an **LED driver IC** that controls up to 64 individual LEDs (or 8 seven-segment digits). It communicates over SPI and handles multiplexing, current limiting, and brightness control in hardware — offloading all the work from your microcontroller.

## What It Does

- Drives **8 seven-segment digits** or **64 individual LEDs** (8×8 matrix)
- **SPI interface** — 3 pins (DIN, CS, CLK)
- **Built-in current limiting** — no series resistors needed
- **Digital brightness control** — 16 levels (via register)
- **BCD decoding** — can automatically display digits 0–9
- **Multiplexing** — handled internally, no flicker

## Common Modules

### 8-Digit 7-Segment Module

```
┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
│8.│ │8.│ │8.│ │8.│ │8.│ │8.│ │8.│ │8.│
└──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘
```

### 8×8 LED Matrix Module

```
4 in 1 module (4 × MAX7219 + 4 × 8×8 matrices):
  ╔══╗ ╔══╗ ╔══╗ ╔══╗
  ║88║ ║88║ ║88║ ║88║
  ╚══╝ ╚══╝ ╚══╝ ╚══╝
  (daisy-chained)
```

## Wiring (SPI)

```
MAX7219 module        Microcontroller
  VCC ───────────────── 5V (or 3.3V — check module, 5V is typical)
  GND ───────────────── GND
  DIN ───────────────── MOSI (SPI data out)
  CS  ───────────────── GPIO (chip select, any pin)
  CLK ───────────────── SCK (SPI clock)
```

### Daisy Chaining Multiple Modules

```
Module 1           Module 2           Module 3
  DOUT ────────────── DIN               DIN
  CS  ─────────────── CS  ───────────── CS
  CLK ─────────────── CLK ───────────── CLK
```

Connect DOUT of module 1 to DIN of module 2, etc. All modules share CS and CLK. Send 16 bits × number of modules in one go.

## Library

Use the **LedControl** library (wayoda) or **MD_MAX72XX** (for matrices):

```cpp
#include <LedControl.h>

LedControl lc = LedControl(DIN_PIN, CLK_PIN, CS_PIN, 1); // 1 module

void setup() {
  lc.shutdown(0, false);        // wake up (low-power mode is default!)
  lc.setIntensity(0, 8);        // brightness (0–15)
  lc.clearDisplay(0);
}
```

**Critical:** The MAX7219 starts in **shutdown (low-power) mode**. You must wake it with `shutdown(0, false)` before it will display anything.

## Seven-Segment Display

```cpp
// Display a number
lc.setDigit(0, digit, value, decimalPoint);
// 0 = module address, digit = position (0–7, right to left)
// value = 0–9, decimalPoint = true/false

lc.setDigit(0, 0, 1, false);  // rightmost digit shows "1"
lc.setDigit(0, 1, 2, false);  // second from right shows "2"
```

### Displaying Numbers

```cpp
int number = 1234;
for (int i = 7; i >= 0; i--) {
  lc.setDigit(0, i, number % 10, false);
  number /= 10;
  if (number == 0) break;
}
```

### BCD Mode (Automatic Digit Decoding)

By default, digits 0–7 decode BCD to 0–9 (and some letters). Disable decoding for custom segments:

```cpp
lc.setDigit(0, 0, 0, false);   // BCD decoded (shows "0")
lc.writeByte(0, 0, B01101110); // raw segments (shows "H" pattern)
```

## LED Matrix

```cpp
#include <MD_MAX72XX.h>

MD_MAX72XX mx = MD_MAX72XX(HARDWARE_TYPE, CS_PIN, 1); // 1 module

void setup() {
  mx.begin();
  mx.setIntensity(8);
}

void loop() {
  mx.clear();
  mx.setPoint(3, 4, true);  // turn on pixel at row 3, column 4
  mx.update();               // send to display
}
```

### Scrolling Text

```cpp
const char message[] = "Hello! ";
mx.clear();
mx.setTextWrap(true);

for (int i = 0; i < 100; i++) {
  mx.clear();
  mx.print(message);
  mx.transform(MD_MAX72XX::TSL); // scroll left
  mx.update();
  delay(100);
}
```

## Current Setting

The MAX7219's segment current is set by a **single resistor** (R_SET) between ISET pin and GND:

| R_SET | Segment current (typical) | 7-segment brightness |
|-------|--------------------------|----------------------|
| 9.5kΩ | 40mA | Very bright |
| 13.3kΩ | 30mA | Bright |
| 22.1kΩ | 17mA | Normal |
| 33.3kΩ | 10mA | Dim |
| 36.9kΩ | 8mA | Dim (conservative for small displays) |

Most modules use ~22kΩ (17mA per segment). Don't exceed the display's max current rating. For small 0.36" displays, 10mA is enough.

## Power Consumption

| Configuration | Current (max, all LEDs on) |
|--------------|---------------------------|
| 8 digits, all segments + decimal on | ~8 × 8 × 17mA = ~1.1A |
| 8×8 matrix, all LEDs on | 64 × 17mA = ~1.1A |
| Typical use (displaying "1234") | ~100–200mA |

**That's a lot of current.** An 8-digit display with all segments lit draws over 1A. Most modules use a 5V supply, and a microcontroller's 5V pin can't supply that. Use an external 5V supply.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Nothing displays (but all segments dimly on) | MAX7219 in shutdown mode | Call `shutdown(0, false)` |
| Nothing displays (blank) | Wrong CS pin or wiring | Check SPI wiring, especially CS pin assignment |
| Flickering | Refresh rate too low | MAX7219 handles refresh internally — flicker means bad power or wrong registers |
| Wrong characters displayed | BCD decoding on when you want raw (or vice versa) | Use `setDigit()` for BCD or write custom bytes |
| Display too dim | R_SET resistor too large | Replace R_SET with lower value (e.g., 22.1kΩ → 13.3kΩ) |
| Display too bright / hot | R_SET too small, or intensity too high | Check R_SET, reduce intensity register |
| Random segments light up | Daisy chain data misalignment | Ensure you send 16 bits per module |
| Daisy chain has wrong data on last module | CS pulse too short | Make sure CS stays LOW during entire SPI transaction |

## Quick Reference

- **SPI interface:** DIN, CS, CLK — 3 wires (no MISO)
- **Drives:** 8 seven-segment digits OR 8×8 LED matrix
- **No current-limiting resistors needed** — built-in (set by R_SET)
- **Shutdown mode:** Always wake with `shutdown(0, false)` at startup
- **Brightness:** 16 levels via `setIntensity(0, level)`
- **Daisy chaining:** DOUT → DIN, all share CS and CLK
- **Library:** LedControl (7-segment), MD_MAX72XX (matrix)
- **Power:** Can draw 1A+ with all LEDs on — use external supply
- **R_SET:** 10kΩ–37kΩ. Higher = dimmer. ~22kΩ is standard.
