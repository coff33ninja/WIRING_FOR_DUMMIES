# DS18B20 Temperature Sensor — Wiring for Dummies

## What It Is

The DS18B20 is a **digital temperature sensor** that reads from **−55°C to +125°C** (±0.5°C accuracy) and talks over a protocol called **One-Wire** — which means it uses **only one data wire** (plus power and ground).

> **Analogy:** The One-Wire protocol is like a single-string tin-can phone. You talk, the other end listens — but it's on the same wire. You have to take turns talking. The DS18B20 knows how to do this politely.

## The 3 Pins (TO-92 package — looks like a transistor)

```
     ┌──────┐
     │ DS18 │  ← Flat face
     │B20   │
     └──────┘
       │ │ │
       │ │ └── GND (pin 3)
       │ └──── DQ  (pin 2) — Data
       └────── VDD (pin 1) — Power
```

| Pin | Name | Think of it as... | Note |
|-----|------|-------------------|------|
| **1** | VDD | Power (red wire) | Connect to 3.3V or 5V |
| **2** | DQ | Data (yellow/white wire) | The **shared conversation wire** |
| **3** | GND | Ground (black wire) | Back to the power supply |

## Parasitic Power Mode vs External Power

### External Power (Recommended — Use This)

```
ESP32           DS18B20
────            ───────
3.3V ───┬──────── VDD (pin 1)
        │
      4.7kΩ
        │
GPIO ───┴──────── DQ  (pin 2)  ← data + pull-up
        │
GND  ──────────── GND (pin 3)
```

**How it works:** Pin 1 gets its own power. The sensor is fully self-powered, reads accurately, and can work with longer wires.

### Parasitic Power (Advanced)

```
ESP32           DS18B20
────            ───────
3.3V ───┬──────── (NOT connected to VDD)
        │
      4.7kΩ
        │
GPIO ───┴──────── DQ  (pin 2)
        │
GND  ──────────── GND (pin 3)
                  VDD (pin 1) ─── GND
```

In parasitic mode, the DS18B20 "steals" power from the data line. It stores energy in an internal capacitor while the line is HIGH, and uses that stored energy to run.

> **Why you'd use it:** Saves one wire — only need 2 wires instead of 3.
> **Why you probably shouldn't:** Less reliable, can't do temperature conversions accurately at low voltage, needs very strong pull-up. Use external power unless you're in a wire-constrained situation.

## The 4.7kΩ Pull-Up Resistor — NOT Optional

The DS18B20 uses **open-drain** signaling (like I2C — see the [I2C guide](i2c-devices.md)). The sensor can only pull the data line DOWN to ground. The pull-up resistor pulls it UP to 3.3V when the sensor isn't driving it.

> **What happens if you skip it:** The One-Wire bus doesn't work. Your code will scan for sensors and find **zero devices**. No data gets through.

```
3.3V
  │
4.7kΩ  ← This resistor is required
  │
GPIO ── DQ
```

**For longer wires (>5m), use 2.2kΩ instead of 4.7kΩ.**

## Multiple DS18B20s on One Wire

The DS18B20's killer feature: **every sensor has a unique 64-bit serial number** burned in at the factory. You can put dozens of them on the same single data wire and address them individually.

```
ESP32
─────
3.3V ───┬──────── VDD (all sensors share power)
        │
      4.7kΩ
        │
GPIO ───┼──────── DQ ───┬── DS18B20 #1
        │               ├── DS18B20 #2
        │               ├── DS18B20 #3
        │               └── DS18B20 #n
        │
GND  ───────────────────── GND (all sensors)
```

> **No address conflicts** — unlike I2C, there's no address pin to worry about. Each sensor has a unique ROM ID. Your library handles the addressing automatically.

### Reading Multiple Sensors

```
DS18B20 scan results:
  ROM ID: 28FF1234567890AB  → Sensor #1 (kitchen)
  ROM ID: 28FF2345678901CD  → Sensor #2 (living room)
  ROM ID: 28FF3456789012EF  → Sensor #3 (outside)
```

In your code, you assign each ROM ID a name, then read them individually.

## Wiring Diagram (Multiple Sensors, External Power)

```
3.3V ───────┬────────────────────────────────── VDD (all sensors)
            │
           4.7kΩ
            │
GPIO ───────┴────────────────────────────────── DQ (all sensors)
            │        │           │           │
GND  ────────────────┴───────────┴───────────┴── GND (all sensors)

Individual sensors:
  ┌────────┐  ┌────────┐  ┌────────┐
  │DS18B20 │  │DS18B20 │  │DS18B20 │
  │  #1    │  │  #2    │  │  #3    │
  └────────┘  └────────┘  └────────┘
```

## Identifying Pins on Different Packages

### TO-92 (looks like a transistor — the most common)

```
     ┌──────┐
     │ 1 ○  │  ← Flat face has writing
     │      │
     └──────┘
       │ │ │
       │ │ └── 3 (GND)
       │ └──── 2 (DQ)
       └────── 1 (VDD)
```

### Waterproof / Stainless Steel Probe Version

```
    (Silicone wire)
    ┌────┬────┬────┐
    Red  │    │    │  ← VDD (3.3–5V)
    │  Black │    │  ← GND
    │    │ Yellow │  ← DQ (data)
    │    │    │    │
    └────┴────┴────┘
    
    ||||||||||||||  ← Stainless steel tube (length varies)
```

> **Note:** Some waterproof probes swap the wire colors! Always check your specific sensor's datasheet. On some: Red = VDD, Black = GND, Yellow/White = DQ. On others: Red = VDD, Black = DQ, Yellow = GND. **Test with a multimeter before connecting.**

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| 4.7kΩ pull-up resistor | Bus doesn't work — "No sensors found" |
| Common ground | No communication at all |
| External power (parasitic mode with long wires) | Garbage readings, failed conversions |
| Pull-up on longer wires (use 2.2kΩ instead) | Intermittent data, some sensors appear/disappear |
| Parasitic power without strong pull-up | Sensor browns out during conversion, reads 85°C |
| Multiple sensors without library support | Confusion — but the library handles this automatically |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| DS18B20 TO-92 | 1+ | The bare transistor-style sensor |
| OR: Waterproof DS18B20 probe | 1 | For outdoor/water use |
| 4.7kΩ resistor | 1 | One-Wire pull-up — required |
| 2.2kΩ resistor | 1 | Alternative for long wires (>5m) |
| Jumper wires | 1 set | M-F, F-F |
| Screw terminal or connector | 1 | For the probe (it's usually bare wires) |

## Common Issue: Reading 85°C

If your DS18B20 consistently reads **85°C**: it's a power problem. The sensor is in an undefined state. Fixes:

1. Use external power (connect VDD to 3.3V, not parasitic)
2. Add or reduce the pull-up resistor (try 2.2kΩ)
3. Add a 100nF capacitor across VDD and GND near the sensor
4. Wait longer between readings (the sensor needs time to charge its internal cap)

85°C is the sensor's **power-on reset value** — it means it's kind-of working but not getting enough power to actually convert.

## See Also

- [serial-communication](/fundamentals/serial-communication)
- [pull-up-pull-down](/fundamentals/pull-up-pull-down)
- [multimeter](/fundamentals/multimeter)
