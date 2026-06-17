# SD Card Module — Component Reference

## What It Is

An SD card module lets a microcontroller **read and write files** on an SD or microSD card. It's the standard way to add data logging, configuration storage, or media playback to a project.

## The Module

Most SD card modules use **SPI** mode and include a voltage regulator and level shifter so they work with both 3.3V and 5V microcontrollers.

```
SD Card Module:
        ┌─────────────────┐
        │                 │
 VCC ───┤                 ├─── CS
 GND ───┤                 ├─── MOSI
        │                 ├─── SCK
        │                 ├─── MISO
        │                 │
        └─────────────────┘
```

## Wiring (SPI Mode)

```
SD Module            Microcontroller
  VCC ──────────────── 5V (module has onboard regulator)
  GND ──────────────── GND
  CS  ──────────────── GPIO (chip select, any pin)
  MOSI ─────────────── MOSI (SPI data out)
  SCK ──────────────── SCK (SPI clock)
  MISO ─────────────── MISO (SPI data in)
```

Most modules work with **5V VCC** (the onboard AMS1117-3.3 regulates it down). For 3.3V microcontrollers, 3.3V VCC also works (bypasses the regulator).

### ESP32 Specific

ESP32's SPI pins typically default to:
- MOSI: GPIO 23
- MISO: GPIO 19
- SCK: GPIO 18
- CS: Any GPIO (commonly GPIO 5 or 4)

For the ESP32, you can use **SDMMC mode** (4-bit parallel) for faster reads. This uses dedicated pins and is much faster than SPI:

```
SDMMC pins: CMD=GPIO15, CLK=GPIO14, D0=GPIO2, D1=GPIO4, D2=GPIO12, D3=GPIO13
```

SDMMC is significantly faster but uses specific pins only.

## Formatting the SD Card

SD cards need to be formatted as **FAT32** or **FAT16**:

| Card size | Recommended format |
|-----------|-------------------|
| ≤ 2GB | FAT16 |
| 4–32GB | FAT32 |
| > 32GB | exFAT (NOT supported by SDFat library) |

**Cards larger than 32GB** may not work — most hobby libraries don't support exFAT. A 16GB or 32GB card formatted FAT32 is the sweet spot.

**Format on Windows:** Use the SD Card Formatter tool (sdcard.org) or Windows format with "FAT32".

## Library

### SD Library (Arduino built-in)

```cpp
#include <SD.h>
File dataFile;

void setup() {
  SD.begin(CS_PIN);
  dataFile = SD.open("log.txt", FILE_WRITE);
  dataFile.println("Hello, SD card!");
  dataFile.close();
}
```

### SDfat Library (faster, more features)

The **SdFat** library is faster, supports long filenames, and has better error handling:

```cpp
#include <SdFat.h>
SdFat SD;
File dataFile;

void setup() {
  SD.begin(CS_PIN, SD_SCK_MHZ(50)); // 50 MHz SPI
}
```

## Data Logging Example

```cpp
#include <SD.h>

const int CS = 10;
File logFile;

void setup() {
  SD.begin(CS);
  logFile = SD.open("data.csv", FILE_WRITE);
  logFile.println("time_ms,temperature,humidity");
  logFile.close();
}

void loop() {
  logFile = SD.open("data.csv", FILE_WRITE);
  if (logFile) {
    logFile.print(millis());
    logFile.print(",");
    logFile.print(25.3);    // sensor reading
    logFile.print(",");
    logFile.println(60.1);  // sensor reading
    logFile.close();
  }
  delay(60000); // log every minute
}
```

## File Operations

| Operation | Code |
|-----------|------|
| Open for reading | `SD.open("file.txt")` |
| Open for writing | `SD.open("file.txt", FILE_WRITE)` |
| Check exists | `SD.exists("file.txt")` |
| Delete | `SD.remove("file.txt")` |
| Create directory | `SD.mkdir("/logs")` |
| List files | `File dir = SD.open("/")` then `dir.openNextFile()` |

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Card not initializing | Wrong CS pin | Verify CS pin matches code |
| Card not initializing | Card formatted wrong | Reformat as FAT32 |
| Card not initializing | Bad SPI wiring | Check MOSI/MISO/SCK connections |
| Can't open file | Card nearly full | Free up space or use larger card |
| Can't open file | Filename too long | Use 8.3 format (FILENAME.TXT) in SD library |
| Random data corruption | Power dropout during write | Add 100µF capacitor near module VCC |
| Very slow writes | SPI speed too low | Increase SPI speed (up to 20 MHz) |
| Card works on PC but not in module | 3.3V/5V mismatch | Check module voltage rating |

### 8.3 Filename Format

The built-in SD library uses 8.3 filenames: up to 8 characters, dot, up to 3 character extension:

```
LOGFILE.TXT  ✓  (8 + 3)
MYLOGFILE.TXT ✓  (still 8 + 3: MYLOGFIL.E.TXT is wrong)
longfilename.txt ✗ (too long)
```

The **SdFat** library supports long filenames.

## Power Consumption

| State | Current draw |
|-------|-------------|
| Idle / not selected | ~0.2mA |
| Reading | ~20mA |
| Writing | ~30–50mA (up to 100mA on some cards) |
| Peak (startup) | ~100mA |

The startup current spike can brown-out a microcontroller. Use a 100µF capacitor near the module.

## Quick Reference

- **SPI interface:** CS, MOSI, MISO, SCK
- **Power:** 5V (module regulates to 3.3V). Add 100µF capacitor.
- **Format:** FAT32 (or FAT16 for ≤ 2GB)
- **Filename limit:** 8.3 characters with built-in SD library
- **SPI speed:** Up to 20 MHz typical, 50 MHz with SdFat library
- **Library:** `SD.h` (built-in) or `SdFat` (faster, long filenames)
- **Logging:** Open → write → close. Don't keep files open long-term.
- **ESP32:** SDMMC mode is faster but uses dedicated pins. SPI works on any pins.
