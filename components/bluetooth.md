# Bluetooth Module (HC-05 / HM-10) — Component Reference

## What It Is

Bluetooth modules add wireless serial communication to any microcontroller with a UART. Classic Bluetooth (HC-05) pairs with phones, laptops, and other MCUs for streaming data. BLE (HM-10, CC2541) is lower power, modern, and works with iOS/Android apps without pairing overhead.

> **Analogy:** A wireless serial cable. Instead of wires between TX and RX, the data goes over radio. The microcontroller doesn't know the difference — it just sends and receives bytes.

## Classic vs BLE — Which One Do You Need?

| Feature | Classic Bluetooth (HC-05) | BLE (HM-10 / CC2541) |
|---------|--------------------------|----------------------|
| Standard | Bluetooth 2.0 + EDR | Bluetooth 4.0+ (Low Energy) |
| Data rate | ~2 Mbps (realistic ~100 KB/s) | ~1 Mbps (realistic ~50 KB/s) |
| Power | ~30–50 mA (peak) | ~5–15 mA (peak), ~0.5 mA sleep |
| Pairing | Requires PIN pairing | Advertises — app connects directly |
| Phone support | Android only (iOS blocks classic BT) | Android + iOS (most apps use BLE) |
| Multiple connections | 1 master + up to 7 slaves | 1 master + many slaves (mesh capable) |
| Profile | SPP (Serial Port Profile) | GATT (Generic Attributes) |
| Best for | Arduino-to-Arduino, laptop serial | Battery sensors, phone apps, beacons |

**Decision rule:** If your phone app uses "Bluetooth Classic" or "SPP" — use HC-05. If it uses "BLE" or "Bluetooth Low Energy" — use HM-10. When in doubt, choose BLE (HM-10) for new projects — it works with both platforms.

## Pinout

```
    ┌─────────────┐
    │             │
    │   HC-05     │
    │             │
    │ EN RX TX    │ ← header row (6 pins)
    │ VCC GND     │
    └─────────────┘

    ┌─────────────┐
    │             │
    │   HM-10     │
    │             │
    │ VCC GND TX  │ ← header row (6 pins)
    │ BRK RX WAKE │
    └─────────────┘
```

| Pin | HC-05 | HM-10 |
|-----|-------|-------|
| VCC | 5V (3.6–6V tolerant) | 3.3V only (3.0–3.6V, **not 5V tolerant**) |
| GND | Ground | Ground |
| TX | 5V output → 3.3V MCU RX (needs divider) | 3.3V output → MCU RX |
| RX | 5V tolerant input ← MCU TX | 3.3V input ← MCU TX (**5V will kill it**) |
| EN | Enable (HIGH = on, LOW = sleep) | — |
| KEY/BRK | AT command mode (HIGH at power-on) | AT command mode (HIGH at power-on) |
| STATE | Connected indicator (HIGH when paired) | Connected indicator (optional) |
| WAKE | — | Wake from sleep |

> **Critical wiring rule:** HM-10 RX is **3.3V only**. If your microcontroller outputs 5V on its TX pin, you must use a voltage divider (2kΩ + 1kΩ) or a level shifter. HC-05 is 5V-tolerant and easier to wire.

## UART Interface — The "Serial Cable"

Bluetooth modules connect via UART (Universal Asynchronous Receiver/Transmitter) — the same serial protocol used for programming Arduinos.

```
    MCU                    BT Module
   ┌─────┐                ┌─────┐
   │ TX  ──────────────── RX │
   │ RX  ──────────────── TX │
   │ GND ──────────────── GND│
   └─────┘                └─────┘
```

The module acts as a **transparent serial bridge** — bytes go in one side, come out the other over radio. The MCU doesn't know or care that the other end is wireless.

## Baud Rate — Getting the Speed Right

Both ends must use the **same baud rate** or you get garbage.

| Component | Default baud rate | Common settings |
|-----------|-------------------|-----------------|
| HC-05 | 38400 (some clones: 9600) | 9600, 19200, 38400, 115200 |
| HM-10 | 9600 | 9600, 19200, 115200 |
| Arduino SoftwareSerial | 9600–38400 (reliable) | 9600 is safest |
| ESP32 HardwareSerial | Up to 115200+ | 115200 is fine |

> **The most common newbie trap:** HC-05 comes from factory at 38400 baud. Arduino Serial Monitor defaults to 9600 baud. When you send "AT" and get gibberish back — this is why. Check the baud rate first.

**First-time connection steps:**

1. Power the module
2. Open Serial Monitor at **38400** baud (HC-05) or **9600** (HM-10)
3. Set line endings to "Both NL & CR"
4. Type `AT` and hit enter
5. If you get `OK` — you're at the right baud. If you get gibberish, try other baud rates.

## AT Commands — Configuring the Module

Both modules use AT commands over USB/UART to change settings.

### HC-05 Common AT Commands

Enter AT mode: hold the KEY/EN pin HIGH while powering on (or press the button on the board). The LED should blink slowly (~2s intervals) instead of rapidly.

| Command | What it does | Example |
|---------|-------------|---------|
| `AT` | Test connection — should reply `OK` | — |
| `AT+NAME=name` | Set the Bluetooth name | `AT+NAME=MyDevice` |
| `AT+UART=baud,stop,parity` | Set baud rate | `AT+UART=9600,0,0` |
| `AT+ROLE=0` | Set as slave (listens for connections) | — |
| `AT+ROLE=1` | Set as master (initiates connections) | — |
| `AT+CMODE=0` | Bind to specific address | — |
| `AT+CMODE=1` | Accept any connection | — |
| `AT+BIND=addr` | Bind to specific MAC address | `AT+BIND=12,34,56,78,9A,BC` |
| `AT+PSWD=1234` | Set pairing PIN | `AT+PSWD=0000` |
| `AT+ADDR?` | Read own MAC address | Returns MAC |
| `AT+VERSION?` | Read firmware version | — |
| `AT+RESET` | Soft reset after changes | — |

### HM-10 Common AT Commands

Enter AT mode: hold the BRK pin HIGH while powering on, or send BREAK signal.

| Command | What it does | Example |
|---------|-------------|---------|
| `AT` | Test — reply `OK` | — |
| `AT+NAMEname` | Set name (no `=` sign) | `AT+NAMEMyDevice` |
| `AT+BAUD0` | Set baud 9600 | n/a |
| `AT+BAUD4` | Set baud 115200 | n/a |
| `AT+TYPE0` | No PIN (just works) | — |
| `AT+TYPE2` | PIN required | — |
| `AT+PIN123456` | Set 6-digit PIN | — |
| `AT+ROLE0` | Peripheral (slave) | — |
| `AT+ROLE1` | Central (master) | — |
| `AT+ADDR?` | Read MAC | — |
| `AT+RENEW` | Factory reset | — |
| `AT+RESET` | Soft reset | — |

**HM-10 baud rate table:**

| Command | Baud rate |
|---------|-----------|
| `AT+BAUD0` | 9600 (default) |
| `AT+BAUD1` | 19200 |
| `AT+BAUD2` | 38400 |
| `AT+BAUD3` | 57600 |
| `AT+BAUD4` | 115200 |
| `AT+BAUD5` | 4800 |
| `AT+BAUD6` | 2400 |
| `AT+BAUD7` | 1200 |
| `AT+BAUD8` | 230400 |

## Master vs Slave Mode

```
    Master                    Slave

    ┌─────┐    initiates     ┌─────┐
    │     │ ────────────────  │     │
    │ HC-05│  connection      │ HC-05│
    │ Role1│                  │ Role0│
    └─────┘                  └─────┘
```

| Mode | Role | Behavior |
|------|------|----------|
| **Slave** (default) | Peripheral | Listens for incoming connections. Other devices find and connect to it. One slave per connection. |
| **Master** | Central | Scans for slaves and initiates connections. Can control up to 7 slaves in a piconet. |

**When to use each:**

- **Slave:** Sensor node that sends data to a phone or computer. Most common setup — your phone is the master.
- **Master:** Two MCUs talking to each other without a phone. The master initiates the link, the slave accepts it.
- **Master + 7 slaves:** Central hub collecting data from multiple sensor nodes (piconet).

## Pairing Process (Classic BT)

```
   Phone                    HC-05 (Slave)

     1. Scan ────────────── "HC-05" appears
     2. Tap ──────────────── HC-05 accepts
     3. Enter PIN ──────── 1234 (default)
     4. Connected! ──────── Paired
     5. Open app ────────── Data flows over serial
```

- Default PIN for HC-05 is **1234** or **0000**
- Default PIN for HM-10 (with PIN enabled): needs `AT+TYPE2` first, then `AT+PIN123456`
- Once paired, the module remembers the master — no re-pairing needed unless the bind list is cleared

**LED behavior — understanding the blink pattern:**

| Blink pattern | Meaning |
|---------------|---------|
| Fast blink (~0.5s) | Waiting for connection (discoverable) |
| Slow blink (~2s) | AT command mode (KEY pulled HIGH) |
| Solid (or 2 blinks / 2s) | Connected — ready for data |

## Voltage Levels — The Most Common Wiring Mistake

```
   HC-05 is 5V tolerant     HM-10 is 3.3V only

   5V MCU ── TX ───→ RX (safe)     5V MCU ── TX ───→ RX !!DEAD!!          
   5V MCU ←── TX ───── RX          5V MCU ←── TX ───→ 3.3V logic (OK)
   (3.3V MCU → all 3.3V, fine)     (3.3V MCU → all 3.3V, fine)
```

**Safe wiring for an HM-10 with a 5V Arduino:**

```
   Arduino TX ── 1kΩ ──┬── 2kΩ ── GND
                        │
                        └── HM-10 RX
```

This divides 5V down to ~3.3V. Without it, the HM-10's RX pin sees 5V and the module dies immediately.

**What actually works:**

| MCU | HC-05 | HM-10 |
|-----|-------|-------|
| 5V Arduino (Uno, Mega) | Direct wiring, no divider needed | Use voltage divider on MCU TX → HM-10 RX |
| 3.3V MCU (ESP32, Pi, RP2040) | Direct wiring | Direct wiring — both 3.3V |
| 5V to both VCC pins | 5V to VCC (HC-05) | 3.3V to VCC (HM-10) — separate regulator |

## Current Consumption

| State | HC-05 | HM-10 |
|-------|-------|-------|
| Idle (not connected) | ~30–40 mA | ~5–10 mA |
| Connected + idle | ~40–50 mA | ~10–15 mA |
| Transmitting | ~40–50 mA | ~15 mA |
| Sleep | ~1 mA (PIO11 sleep) | ~0.5 mA (AT+SLEEP) |

> **Wire both module and MCU to the same power supply.** A USB port can handle ~500 mA. Two modules + an ESP32 at 300 mA peak = fine. A coin cell cannot run an HC-05 — use HM-10 with a 3.3V regulator if battery-powered.

## Range

| Condition | Typical range |
|-----------|---------------|
| Line of sight, indoors | ~10m (both HC-05 and HM-10) |
| Through 1 wall | ~5–8m |
| Through 2 walls | ~3–5m |
| Outdoor, open air | ~20m (HC-05), ~30m (HM-10) |

**Range boosters:** External antenna (CC2541 has a U.FL connector version), better placement (higher up, not behind metal), or dedicated BT range extender chips.

## Common Uses

### Wireless Sensor Data

```
   Sensor ── MCU ── BT Module ── Pair ── Phone App
   (temp/humidity)         (read data on phone)
```

The MCU reads sensors and sends formatted strings over Bluetooth. A phone app (Serial Bluetooth Terminal for Android, LightBlue for iOS) displays the data.

### Phone Control

```
   Phone App ── BT ── MCU ── Relay/Motor/LED
   (send '1')         (turn on pump)
```

Phone sends single-character commands. MCU parses each byte and controls outputs. Simple, reliable, works for robot control, light switching, watering systems.

### Serial Replacement — Two MCUs

```
   Sensor MCU (slave)          Display MCU (master)
   ┌─────────┐                ┌─────────┐
   │ TX ─────┼────── BT ──────┼─── RX   │
   │ GND ────┼────────────────┼─── GND  │
   └─────────┘                └─────────┘
```

Two Arduinos talking wirelessly. The master initiates the connection, slaves accept. Used for remote sensor nodes, distributed control, multi-room systems.

## Common Mistakes

| Mistake | Result |
|---------|--------|
| HM-10 RX connected directly to 5V Arduino TX | Destroys HM-10 |
| HC-05 at 38400 baud, Serial Monitor at 9600 | Gibberish — always check baud |
| No common ground between MCU and BT module | No communication (floating signals) |
| TX connected to TX (instead of RX) | No communication |
| AT commands without NL+CR line endings | No response — module waits for line end |
| Not holding KEY/EN high when powering on HC-05 | Normal mode, not AT mode |
| Powering HC-05 from Arduino 3.3V pin | Brownouts — needs 5V |
| HC-05 and HM-10 trying to talk to each other | Classic BT and BLE are incompatible |
| Coin cell battery powering HC-05 | Drains battery in hours |
| HM-10 not awoken before sending data | No response — module is sleeping |
| Connecting before baud rate is changed | Wrong baud — both sides must match |

## Quick Reference

```
HC-05 (Classic BT):
  VCC → 5V (3.6–6V tolerant)
  RX  → MCU TX (5V tolerant — safe with 5V)
  TX  → MCU RX (5V output — use divider to 3.3V MCU)
  EN  → HIGH to enable
  KEY → HIGH for AT mode (hold at power-on)
  
  Default baud: 38400 (check your clone!)
  Default PIN: 1234 or 0000
  Default role: Slave
  Range: ~10m indoor
  Current: ~30–50 mA

HM-10 (BLE):
  VCC → 3.3V ONLY (NOT 5V)
  RX  → MCU TX via voltage divider (if 5V MCU)
  TX  → MCU RX (3.3V output, safe for 5V input)
  BRK → HIGH for AT mode
  
  Default baud: 9600
  Default role: Peripheral (slave)
  Range: ~10m indoor
  Current: ~5–15 mA

AT command recap:
  HC-05: AT+UART=9600,0,0  AT+NAME=MyDevice  AT+ROLE=0  AT+PSWD=1234
  HM-10: AT+BAUD0          AT+NAMEMyDevice   AT+ROLE0   AT+TYPE0

Connection check:
  Power → check LED blink pattern
  Match baud rate between module and MCU
  Cross TX/RX (not straight through)
  Common ground
  3.3V modules → never feed 5V into signal pins
```
