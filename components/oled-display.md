# OLED Display (SSD1306) — 128×64 / 128×32 I²C Display

## What It Is

A small monochrome OLED screen (typically 128×64 or 128×32 pixels) that connects via I²C. It's the most common display for hobby projects — showing sensor readings, status, or simple graphics.

> **Analogy:** Think of it as a tiny digital sticky note. You tell it what to display pixel by pixel (or character by character, if you use the graphics library).

## Two Common Sizes

| Size | Resolution | Pixels | Typical use |
|------|-----------|--------|-------------|
| **0.96"** | 128×64 | 8192 | Most common — good for text + small graphs |
| **0.91"** | 128×32 | 4096 | Smaller, good for 1–2 lines of text |

Both use the same **SSD1306 driver chip** and the same I²C wiring.

## Pinout

The 4-pin I²C version is the most common:

```
  Pin   Label   Connect to
  ─────────────────────────────────
  1     GND     GND
  2     VCC     3.3V or 5V (check module — most work on both)
  3     SCL     ESP32 GPIO 22 (SCL)
  4     SDA     ESP32 GPIO 21 (SDA)
```

### Alternative: SPI Version

Some OLED modules use **SPI** instead of I²C. They have more pins (usually 7) but can update faster.

| Protocol | Pins needed | Speed | Wiring complexity |
|----------|-------------|-------|-------------------|
| **I²C** | **4 (VCC, GND, SDA, SCL)** | Good for text/static | Very simple |
| SPI | 7 (VCC, GND, CS, DC, RES, SDA, SCL) | Faster for animations | More wiring |

**For beginners:** Get the **I²C version** (4 pins). The SPI version is overkill for 99% of hobby projects.

## I²C Address

The SSD1306 defaults to I²C address **0x3C**. Some modules use **0x3D**. If your display doesn't respond, try the other address.

```
0x3C → most common (Adafruit default)
0x3D → some modules (try this if 0x3C fails)
```

## Wiring

```
OLED:                     ESP32:
  VCC ──────────────────── 3.3V (or VIN = 5V, check module)
  GND ──────────────────── GND
  SCL ──────────────────── GPIO 22
  SDA ──────────────────── GPIO 21
```

**I²C pull-up resistors:** The ESP32 dev board usually has 4.7kΩ pull-ups built in on GPIO 21/22. If using long wires (>30cm), add external 4.7kΩ from SDA to 3.3V and SCL to 3.3V.

## Code (Using Adafruit SSD1306 Library)

### Install Libraries
In Arduino IDE Library Manager, install:
- **Adafruit SSD1306**
- **Adafruit GFX**

### Basic Example — Text Display

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1  // No reset pin (I²C)

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(115200);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("SSD1306 allocation failed");
    for (;;);
  }

  display.clearDisplay();
  display.setTextSize(2);       // Size 2 = ~16px tall
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 10);
  display.println("Hello!");
  display.display();            // Actually show it (required!)
}

void loop() {
  // Nothing — static display
}
```

### Show Sensor Reading (Loops)

```cpp
void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  display.clearDisplay();

  display.setTextSize(2);
  display.setCursor(0, 0);
  display.print(t, 1);
  display.println(" C");

  display.setCursor(0, 20);
  display.print(h, 1);
  display.println(" %");

  display.display();  // Refresh the screen
  delay(2000);
}
```

## Common Graphics Functions

| Function | What it does |
|----------|-------------|
| `display.clearDisplay()` | Clears the buffer (doesn't show until display()) |
| `display.display()` | Sends buffer to screen — **must call this to see changes** |
| `display.setCursor(x, y)` | Sets text position (pixels from top-left) |
| `display.setTextSize(n)` | Text scale: 1 = 5×8px, 2 = 10×16px, 3 = 15×24px |
| `display.setTextColor(color)` | `SSD1306_WHITE` or `SSD1306_BLACK` (for erasing) |
| `display.println(text)` | Text with newline |
| `display.print(text)` | Text without newline |
| `display.drawPixel(x, y, color)` | Draw a single pixel |
| `display.drawLine(x1, y1, x2, y2, color)` | Draw a line |
| `display.drawRect(x, y, w, h, color)` | Draw rectangle outline |
| `display.fillRect(x, y, w, h, color)` | Draw filled rectangle |
| `display.drawCircle(x, y, r, color)` | Draw circle outline |
| `display.drawBitmap(x, y, array, w, h, color)` | Draw a monochrome bitmap |
| `display.setRotation(n)` | 0/1/2/3 — rotate screen 0°, 90°, 180°, 270° |
| `display.ssd1306_command(cmd)` | Send raw command to SSD1306 chip |

### Drawing Shapes

```cpp
display.clearDisplay();
display.drawRect(10, 10, 50, 30, SSD1306_WHITE);
display.fillRect(70, 10, 30, 30, SSD1306_WHITE);
display.drawCircle(64, 40, 20, SSD1306_WHITE);
display.display();
```

## Power Considerations

| Situation | Current draw |
|-----------|-------------|
| Display off (sleep) | ~10µA |
| Display on, all pixels off | ~6mA |
| Display on, ~50% pixels on | ~15–20mA |
| Display on, all pixels on (white) | ~20–30mA |

The OLED doesn't need a backlight (each pixel generates its own light), so it draws **much less** than an LCD (which needs 100–200mA for the backlight).

> **For battery projects:** You can call `display.ssd1306_command(SSD1306_DISPLAYOFF)` to put the display in sleep mode. Wake it with `display.ssd1306_command(SSD1306_DISPLAYON)`.

## What Happens If Something Goes Wrong

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Screen stays blank | Wrong I²C address | Try `0x3D` instead of `0x3C` |
| Screen stays blank | No power | Check VCC and GND with multimeter |
| Screen stays blank | I²C conflict | Try disconnecting other I²C devices |
| Garbage / random pixels | Bad connection / noisy I²C | Shorten wires, add 4.7kΩ pull-ups |
| Dim display | Wrong VCC voltage | Check if module needs 5V or 3.3V |
| Display flickers on update | Normal — no framebuffer separate from display | Add `delay(100)` between updates or use double buffering |
| Library says "Allocation failed" | Display not detected on I²C bus | Check wiring, address, pull-ups |

## Quick Reference

```
Common display: 0.96" 128×64 I²C (4 pins)
  VCC  → 3.3V (or 5V — check module)
  GND  → GND
  SCL  → GPIO 22 (ESP32 I²C clock)
  SDA  → GPIO 21 (ESP32 I²C data)

I²C address: 0x3C (default), try 0x3D if it doesn't work

Libraries: Adafruit SSD1306 + Adafruit GFX

Essential functions:
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C)
  display.clearDisplay()
  display.display()          // MUST call this to update
  display.setCursor(x, y)
  display.setTextSize(n)
  display.setTextColor(SSD1306_WHITE)
  display.println("text")

Power:
  On: ~20mA
  Sleep: ~10µA (send SSD1306_DISPLAYOFF)
```
