# RFID / NFC (RC522) — Component Reference

## What It Is

The **RC522** is a 13.56 MHz RFID (Radio Frequency Identification) reader module. It reads passive RFID tags and NFC cards — the kind used in access control, payment systems, and public transit.

**Passive** means the tags have no battery. The reader generates a magnetic field that powers the tag wirelessly.

## How RFID Works

```
Reader (RC522):           Tag (MIFARE classic):
  ┌─────────────┐         ┌──────────┐
  │  Antenna    │ ←──────→ │  Coil    │
  │  generates  │ 13.56MHz │  powers  │
  │  magnetic   │  field   │  chip    │
  │  field      │ ←──────→ │  sends   │
  └─────────────┘   data   │  data    │
                           └──────────┘
```

1. Reader emits a 13.56 MHz magnetic field from its antenna coil
2. Tag's coil picks up the field and rectifies it to power the tag chip
3. Tag modulates the field to send data back (load modulation)
4. Reader demodulates the signal and sends the tag data over SPI

## RC522 Module

### Pinout

```
RC522 module        Microcontroller
  SDA (CS) ────────── GPIO (chip select)
  SCK ─────────────── SCK (SPI clock)
  MOSI ────────────── MOSI (SPI data in)
  MISO ────────────── MISO (SPI data out)
  IRQ ─────────────── (optional, unused in most projects)
  GND ─────────────── GND
  RST ─────────────── GPIO (reset)
  VCC ─────────────── 3.3V (DO NOT use 5V)
```

### I2C Mode (Alternative)

The RC522 supports I2C mode by setting address pins. Most modules default to SPI.

### Power

- **VCC:** 3.3V only (3.0–3.6V). **5V will destroy the module.**
- **Current:** ~13mA standby, ~26mA reading
- **Antenna current:** Determines read range (larger antenna = more range)

## Wiring (SPI — Most Common)

```
RC522                ESP32 / Arduino
  SDA ──────────────── GPIO 10 (or any CS pin)
  SCK ──────────────── SCK (GPIO 18 on ESP32)
  MOSI ─────────────── MOSI (GPIO 23 on ESP32)
  MISO ─────────────── MISO (GPIO 19 on ESP32)
  RST ──────────────── GPIO 9 (or any pin)
  GND ──────────────── GND
  3.3V ─────────────── 3.3V
```

## Library

Use the **MFRC522** library (miguelbalboa):

```cpp
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;

  // Print UID
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println();

  mfrc522.PICC_HaltA(); // stop reading
}
```

## Tag Types

| Tag | Memory | Features |
|-----|--------|----------|
| MIFARE Classic 1K | 1KB (16 sectors × 4 blocks) | Most common, ~$0.50 per tag |
| MIFARE Classic 4K | 4KB (40 sectors) | More storage, same tech |
| MIFARE Ultralight | 512 bytes | Simpler, cheaper, less secure |
| NTAG213/215/216 | 144–888 bytes | NFC Forum Type 2, phone compatible |
| FM11RF08 | 1KB | Chinese clone of MIFARE |

**MIFARE Classic 1K** is the most common — blue plastic card or key fob. The RC522 reads all of these.

## Read Range

| Antenna | Range |
|---------|-------|
| Module's onboard antenna | 2–5cm |
| External larger antenna | 5–10cm |
| High-power reader | Up to 20cm |

The short range (< 5cm) is intentional — it prevents accidentally reading the wrong tag. Tap the card directly on the module.

## Writing Data

You can write data to MIFARE tags:

```cpp
MFRC522::MIFARE_Key key;
MFRC522::StatusCode status;

byte block = 1;
byte data[16] = "Hello RFID!     ";  // 16 bytes per block

status = mfrc522.PCD_Authenticate(
  MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));
status = mfrc522.MIFARE_Write(block, data, 16);
```

**Authentication:** MIFARE Classic sectors are protected by keys (default: 0xFFFFFFFFFFFF). You need the correct key to read/write.

## NFC Phone Compatibility

The RC522 can read NFC phones that emulate a MIFARE tag (Android HCE, iPhone Core NFC). This allows:

- Phone as an access card
- Writing data from a phone to a tag
- Reading tag data with a phone (some phones)

**Note:** The RC522 is read-only for most NFC phone interactions. For two-way phone communication, use a PN532 module.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| No tags detected | Wrong wiring | Check SPI pins, especially SDA/CS |
| No tags detected | 5V on VCC | Module is dead — 3.3V only |
| No tags detected | Antenna too close to metal | Keep module away from metal surfaces |
| Reads but wrong UID | Multiple tags in range | Only present one tag at a time |
| Intermittent reads | Poor power supply | Add 100µF capacitor near module |
| Can't write to tag | Tag is locked or read-only | Some MIFARE cards have write-protected sectors |
| "Communication error" | RST pin not connected properly | Connect RST to GPIO, initialize in code |

## Quick Reference

- **3.3V only** — 5V kills it. Use 3.3V from your microcontroller or a regulator.
- **SPI interface:** SDA/CS, SCK, MOSI, MISO + RST
- **Library:** MFRC522 (miguelbalboa)
- **Tags:** MIFARE Classic 1K (most common), NTAG, Ultralight
- **Range:** 2–5cm (tap the card on the module)
- **Frequency:** 13.56 MHz (HF — High Frequency)
- **Passive tags:** No battery needed. Powered by reader's magnetic field.
- **Default key:** 0xFFFFFFFFFFFF (all F's)
- **NFC compatibility:** Limited — RC522 reads NFC tags, but PN532 is better for phone communication.
