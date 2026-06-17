# OLED Sensor Readout — DHT22 + SSD1306 Display

## What You'll Build

Connect a DHT22 temperature/humidity sensor and an OLED display to your ESP32. The OLED shows live temperature and humidity readings, updating every 2 seconds.

```
  ┌─────────────────────────────────┐
  │   ┌─────────────────────────┐   │
  │   │  22.5 °C               │   │
  │   │  45 % RH               │   │
  │   │  ──■─────────────────  │   │
  │   │  Temp                   │   │
  │   └─────────────────────────┘   │
  │          OLED (SSD1306)         │
  └─────────────────────────────────┘
```

## Parts List

| Part | Qty |
|------|-----|
| ESP32 dev board | 1 |
| DHT22 sensor (module or bare) | 1 |
| OLED 0.96" 128×64 I²C | 1 |
| 10kΩ resistor (if DHT22 module doesn't have one) | 1 |
| Breadboard + jumper wires | 1 |

## Wiring

```
                       ESP32
                       ─────
OLED:
  VCC ───────────────── 3.3V
  GND ───────────────── GND
  SCL ───────────────── GPIO 22
  SDA ───────────────── GPIO 21

DHT22:
  VCC ───────────────── 3.3V
  DATA ─────[10kΩ]──── 3.3V  (pull-up required — see note)
  DATA ───────────────── GPIO 4
  GND ───────────────── GND
```

> **DHT22 pull-up note:** Some DHT22 modules have a built-in 10kΩ pull-up on the PCB. If your module has only 3 pins, check with a multimeter between VCC and DATA — if you see ~10kΩ, you don't need the external resistor. If unsure, add it — two pull-ups in parallel (~5kΩ total) works fine.

## Code

### Required Libraries

In Arduino Library Manager, install:
- **Adafruit SSD1306**
- **Adafruit GFX**
- **DHT sensor library** (by Adafruit)

### Complete Sketch

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

unsigned long lastRead = 0;
float temperature = 0;
float humidity = 0;

void setup() {
  Serial.begin(115200);

  // Initialize DHT
  dht.begin();

  // Initialize OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED not found — check wiring and I²C address");
    while (1) delay(100);  // Halt
  }

  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 10);
  display.println("Starting...");
  display.display();
  delay(1000);
}

void loop() {
  unsigned long now = millis();

  // Read sensor every 2 seconds
  if (now - lastRead >= 2000) {
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();
    lastRead = now;

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("DHT read failed — check wiring and pull-up");
    } else {
      Serial.print("Temp: ");
      Serial.print(temperature);
      Serial.print("°C  Hum: ");
      Serial.println(humidity);
    }
  }

  // Update display (every loop iteration for responsiveness)
  display.clearDisplay();

  // Temperature
  display.setTextSize(3);
  display.setCursor(0, 0);
  if (!isnan(temperature)) {
    display.print(temperature, 1);
    display.print(" ");
    display.setTextSize(1);
    display.print("C");
  } else {
    display.print("--");
  }

  // Humidity
  display.setTextSize(2);
  display.setCursor(0, 35);
  if (!isnan(humidity)) {
    display.print(humidity, 1);
    display.print(" %");
  } else {
    display.print("-- %");
  }

  display.display();
  delay(100);
}
```

### What Each Section Does

| Section | What it does |
|---------|-------------|
| `display.begin(SSD1306_SWITCHCAPVCC, 0x3C)` | Initializes OLED at I²C address 0x3C |
| `dht.readTemperature()` | Reads temperature (blocks ~250ms) |
| `dht.readHumidity()` | Reads humidity (blocks ~250ms) |
| `isnan()` | Checks if sensor read failed (returns true if NaN) |
| `display.clearDisplay()` | Clears the frame buffer |
| `display.print()` | Writes text to frame buffer |
| `display.display()` | Sends frame buffer to OLED — **required** |

## Adding a Simple Bar Graph

To make the display look more polished, add a bar graph for temperature:

```cpp
// After display.print calls, add bar graph
if (!isnan(temperature)) {
  // Draw a bar graph at the bottom
  int barWidth = map((int)(temperature * 10), 0, 500, 0, 120);  // 0–50°C
  barWidth = constrain(barWidth, 0, 120);

  display.drawRect(4, 56, 120, 6, SSD1306_WHITE);   // Outline
  display.fillRect(4, 56, barWidth, 6, SSD1306_WHITE);  // Fill
}
```

## If the Display Doesn't Work

| Symptom | Fix |
|---------|-----|
| "OLED not found" in serial | Check I²C address (try **0x3D** instead of 0x3C) |
| "OLED not found" in serial | Check SCL→GPIO 22, SDA→GPIO 21 |
| "OLED not found" in serial | Add 4.7kΩ pull-ups on SDA/SCL to 3.3V |
| Screen is on but shows nothing | `display.display()` missing — you must call it after writing |
| Garbage / pixels everywhere | Bad I²C connection — reseat wires, shorten cables |
| Dim display | Some modules need 5V VCC — check your module specs |

## If the DHT22 Doesn't Work

| Symptom | Fix |
|---------|-----|
| Reads NaN | Add 10kΩ pull-up between DATA and VCC |
| Reads NaN | Wrong GPIO pin in code |
| Reads NaN | Reading too fast — max 2 reads/sec (500ms min between reads) |
| Temperature is 5°C too high | DHT22 too close to ESP32 (ESP32 runs warm). Extend wires. |

## Going Further

| Feature | How |
|---------|-----|
| **Show max/min** | Track `maxTemp = max(maxTemp, temperature)` and display it |
| **Fahrenheit** | `temperature * 9.0 / 5.0 + 32` |
| **Combined with web server** | Add `#include <WebServer.h>` and serve the data as a web page too |
| **Deep sleep** | Read once, display for 10s, then deep sleep for 5 min (battery project) |
| **Second sensor** | Add another DHT22 on GPIO 5; display both |
| **Graph over time** | Store last 20 readings in an array and draw a line graph |

## Quick Reference

```
Wiring:
  OLED SCL → GPIO 22
  OLED SDA → GPIO 21
  DHT22 DATA → GPIO 4 (+ 10kΩ pull-up to 3.3V)

Libraries needed (install via Library Manager):
  Adafruit SSD1306, Adafruit GFX, DHT sensor library

OLED init:  display.begin(SSD1306_SWITCHCAPVCC, 0x3C)
DHT init:   dht.begin()

Read cycle:
  dht.readTemperature()  → float (NaN on failure)
  dht.readHumidity()     → float (NaN on failure)

Display cycle:
  display.clearDisplay()
  display.setCursor(x, y)
  display.print("text")
  display.display()      // Required!

Common problems:
  OLED not found → try 0x3D address
  DHT NaN → add pull-up resistor, check wiring, slow down reads

0x3C and 0x3D are the only two I²C addresses for SSD1306.
DHT22 max read rate = 2/sec (500ms between reads).
```

## See Also

- [serial-communication](/fundamentals/serial-communication)
- [analog-vs-digital](/fundamentals/analog-vs-digital)
- [multimeter](/fundamentals/multimeter)
- [soldering](/fundamentals/soldering)
- [power-batteries](/fundamentals/power-batteries)
- [boost-converter](/fundamentals/boost-converter)
