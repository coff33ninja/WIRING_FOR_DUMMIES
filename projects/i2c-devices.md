# I2C Devices — Wiring for Dummies

## What Is I2C?

I2C (pronounced "eye-squared-see") is a way to connect **multiple devices** to a microcontroller using only **two wires**. Think of it like a party line telephone — everyone shares the same two wires, but only the person whose name you call responds.

- **SDA** (Serial Data): The actual data wire — carries information back and forth
- **SCL** (Serial Clock): The timing wire — keeps everyone in sync

Every device on an I2C bus has a **unique address** (like a phone number). The microcontroller calls out an address, and only the device with that address responds.

```
3.3V
  │
  ├──[4.7kΩ]──┐
  │            ├── SDA ──┬── Device A (0x3C)
  │            │         ├── Device B (0x76)
  │            │         └── Device C (0x68)
  │            │
  ├──[4.7kΩ]──┐
  │            ├── SCL ──┬── Device A
  │            │         ├── Device B
  │            │         └── Device C
  │            │
 GND ──────────┴───────── All devices' GND
```

## Common I2C Devices

| Device | What it does | Address | Voltage |
|--------|-------------|---------|---------|
| SSD1306 OLED (128×64) | Small monochrome display | 0x3C (or 0x3D) | 3.3–5V |
| BMP280 / BME280 | Temperature, pressure, humidity | 0x76 (or 0x77) | 3.3V |
| MPU6050 | Accelerometer + Gyroscope | 0x68 (or 0x69) | 3.3V |
| ADS1115 | 16-bit analog-to-digital converter | 0x48–0x4B | 3.3–5V |
| MCP23017 | 16-pin GPIO expander | 0x20–0x27 | 3.3–5V |
| DS3231 | Real-time clock (RTC) | 0x68 | 3.3–5V |

## Why You Need Pull-Up Resistors

I2C uses **open-drain signaling**. Each device can only pull the SDA or SCL line **down to ground** — it cannot push the line **up to 3.3V**. That's the pull-up resistor's job.

> **Analogy:** Think of a bunch of people in a rowboat. Each person (device) can only push their oar DOWN (pull signal to ground). The pull-up resistor is a spring that pushes the oar back UP when nobody is pushing down.

Without pull-up resistors, the signal lines float — they pick up random electrical noise, and the I2C bus either doesn't work or gives corrupted data.

### Resistor Value

| I2C speed | Pull-up value | Use |
|-----------|---------------|-----|
| 100kHz (standard) | 4.7kΩ | **Default — works for everything** |
| 400kHz (fast) | 2.2kΩ–4.7kΩ | Faster data, more devices |
| 1MHz (fast+) | 1kΩ–2.2kΩ | Fastest, short wires only |

**Default: 4.7kΩ.** Works for 99% of hobby projects.

> **What happens if you skip them:** The I2C bus doesn't work at all — the microcontroller sends data but nothing responds. Serial monitor shows "I2C device not found" or the bus hangs.

## Address Conflicts

Two devices with the same address on the same bus = **no communication**. The microcontroller calls out the address and both devices try to respond, garbling the data.

### How to Fix

1. **Check the address pin.** Most I2C devices have a pin that changes the address:
   - BMP280: ADDR pin → GND = 0x76, VCC = 0x77
   - MPU6050: ADDR pin → GND = 0x68, VCC = 0x69
   - MCP23017: A0/A1/A2 pins → 8 different addresses

2. **Use a multiplexer** (TCA9548A) if you need more devices of the same type than addresses allow.

3. **Use two I2C buses** if your microcontroller has a second I2C port.

### Address Scanner Sketch

Before worrying, run an I2C scanner sketch. It will tell you every address it finds. Most problems come from guessing the wrong address.

```
I2C Scanner output:
  Found device at 0x3C  ← Your OLED
  Found device at 0x76  ← Your BMP280
```

If a device you expect isn't shown: check wiring, check voltage, check address pin.

## 3.3V vs 5V — Level Shifting

Some I2C devices run at 5V (old LCD modules, some sensors). If you connect a 5V device's SDA/SCL directly to a 3.3V ESP32, you can **damage the ESP32** because the 5V signal exceeds the GPIO's voltage limit.

### If all devices are 3.3V

Wire them directly together. No level shifting needed.

### If you have a mix of 3.3V and 5V devices

> **Full component reference:** See [Level Shifter](../components/level-shifter.md) for bidirectional vs unidirectional shifting, voltage dividers, and BSS138 MOSFET modules.

**Option 1: Use a logic level shifter module.**

```
3.3V side           5V side
ESP32          Level shifter    5V Device
GPIO (SDA) ──→ LV1 ─── HV1 ──→ SDA
GPIO (SCL) ──→ LV2 ─── HV2 ──→ SCL
3.3V ────────→ LV ─── HV ─────→ 5V
GND  ────────→ GND ── GND ────→ GND
```

**Option 2: Check if the 5V device actually accepts 3.3V logic.**

Many 5V I2C devices accept 3.3V signals just fine because they read anything above ~2.5V as HIGH. Try it directly — but **monitor for heat or smoke** on first power-up.

**Option 3: Use pull-up resistors to 3.3V only.**

Connect pull-ups to 3.3V (not 5V). This limits the "HIGH" voltage to 3.3V even on 5V devices. Many 5V devices tolerate this.

```
5V device SDA ──┬── ESP32 GPIO
                │
              4.7kΩ
                │
              3.3V   ← NOT 5V
```

## Wiring Diagrams

### SSD1306 OLED (128×64, I2C)

```
ESP32             SSD1306 OLED
────              ───────────
3.3V ────────────── VCC
GND  ────────────── GND
GPIO21 ──┬──────── SDA
        4.7kΩ
          │
         3.3V
GPIO22 ──┬──────── SCL
        4.7kΩ
          │
         3.3V
```

### Multiple Devices (OLED + BMP280)

```
ESP32             4.7kΩ × 2
────             ──────────
3.3V ───────┬──────┬───┬────┬──
           4.7kΩ   │   │    │
GND  ───────┴──────┴───┴────┴──
                 SCL  SDA
                   │    │
GPIO22 ────────────┘    │
GPIO21 ─────────────────┘
                        │
             ┌──────────┴──────────┐
             │                     │
        OLED VCC GND SCL SDA    BMP280 VCC GND SCL SDA
             │                     │
             3.3V  GND             3.3V  GND
```

## Wiring Checklist

- Pull-up resistors (4.7kΩ) on BOTH SDA and SCL
- All devices share the same ground
- All devices are powered (don't assume VCC from bus — each needs its own power)
- Unique addresses (run scanner to verify)
- Voltage compatibility (3.3V vs 5V)
- Keep wires under ~1 meter for reliable communication

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Pull-up resistors on SDA/SCL | I2C bus doesn't work — "device not found" |
| Common ground | No communication at all — voltage references are different |
| Address conflict | Bus interference, no devices respond |
| Level shifter (5V device on 3.3V MCU) | ESP32 GPIO may be damaged by 5V signal |
| Power to one device | That device is invisible on the bus |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| SSD1306 OLED 128×64 I2C | 1 | Standard 0.96" display |
| BMP280 / BME280 module | 1 | Temperature + pressure (+ humidity for BME) |
| 4.7kΩ resistors | 2 | I2C pull-ups |
| Jumper wires | 1 set | F-F and M-F |
| Optional: ADS1115 ADC | 1 | If you need more analog inputs |
| Optional: Level shifter | 1 | If mixing 3.3V and 5V I2C devices |

## See Also

- [serial-communication](/fundamentals/serial-communication)
- [level-shifter](/fundamentals/level-shifter)
- [pull-up-pull-down](/fundamentals/pull-up-pull-down)
- [multimeter](/fundamentals/multimeter)
