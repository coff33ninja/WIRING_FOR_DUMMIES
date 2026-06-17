# Wireless Technologies — Which One When

## The Confusion

There are too many wireless technologies and they all sound similar. You know:

- WiFi gets you on the internet at home
- Bluetooth connects your phone to your car or headphones
- A SIM card lets your phone work anywhere
- Your wireless mouse uses... something with a little USB dongle

But what actually makes them different? Why can't you use your wireless mouse to get on the internet? Why does Bluetooth stop working when you walk into the next room but your WiFi still works? Why does your phone need a SIM card at all when you have WiFi at home?

The short answer: **every wireless technology is a trade-off between range, speed, power, and cost.** No single technology can do everything well. This guide explains the real-world differences so you stop wondering why your wireless keyboard doesn't show up on your phone's Bluetooth list or why your SIM-card IoT project burns through batteries in a day.

## The Big Picture — One Table

| Technology | Frequency | Max Range | Max Speed | Power Use | Needs a Tower? | Needs Dongle? | Best For |
|-----------|-----------|-----------|-----------|-----------|----------------|---------------|----------|
| WiFi (2.4GHz) | 2.4 GHz | ~70m indoors | 600 Mbps | Medium | No | No (built-in) | Internet at home, streaming video |
| WiFi (5GHz) | 5 GHz | ~35m indoors | 1.3 Gbps | Medium | No | No (built-in) | Fast local file transfer, gaming |
| WiFi (6GHz / 6E) | 6 GHz | ~20m indoors | 2.4 Gbps | Medium | No | No (built-in) | Ultra-fast, low-latency local use |
| Bluetooth Classic | 2.4 GHz | ~10m | 3 Mbps | Low | No | No (built-in) | Headphones, file transfer, car audio |
| Bluetooth Low Energy (BLE) | 2.4 GHz | ~30m | 1 Mbps | **Very Low** | No | No (built-in) | IoT sensors, beacons, wearables |
| Cellular (SIM) 4G/LTE | 700–2600 MHz | **~10km** | 150 Mbps | **High** | Yes (cell tower) | No (built-in) | Phone calls, internet anywhere |
| Cellular (SIM) 5G | 600–60 GHz | ~1km (mmWave less) | 10 Gbps | **Very High** | Yes (small cells) | No (built-in) | High-speed mobile internet |
| Wireless Mouse/Keyboard (RF) | 27 MHz or 2.4 GHz | ~10m | Very low | Very Low | No | Yes (USB dongle) | Input devices, no pairing needed |
| Zigbee / Z-Wave | 2.4 GHz / 800 MHz | ~20m indoors | 250 kbps | Very Low | No | No (hub needed) | Smart home sensors, light bulbs |
| LoRa / LoRaWAN | 868 / 915 MHz | **~10km** | 50 kbps | **Very Low** | No (gateway instead) | No (module) | Long-range sensor networks |
| NFC | 13.56 MHz | ~10cm | 424 kbps | None (passive) | No | No (built-in in phones) | Tap-to-pay, keycards, tags |
| IR (Infrared) | ~300 GHz – 400 THz | ~5m (line of sight) | Very low | Very Low | No | No (but needs line of sight) | TV remotes, old laptop data |

## Why Frequency Matters

Wireless operates on the **electromagnetic spectrum**. Lower frequencies travel further and through walls better. Higher frequencies carry more data but stop at the first obstacle.

Think of it like sound:

- **Low frequency** (bass) — travels through walls, you hear it downstairs. This is cellular (700 MHz) and LoRa (868 MHz).
- **High frequency** (treble) — blocked by a door, needs line of sight. This is mmWave 5G (60 GHz) and WiFi 5 GHz.

**The 2.4 GHz band** is the "junk drawer" of wireless. WiFi, Bluetooth, Zigbee, wireless mice, and microwave ovens all use 2.4 GHz. That's why your WiFi slows down when the microwave is running or when you're in a dense apartment building — everything is shouting over each other.

## WiFi — The Internet in Your House

### How It Works

A WiFi router creates a **local network** that devices connect to. The router is plugged into your internet modem (or has one built in). Your phone/laptop/tablet talks to the router, and the router talks to the internet.

```
internet ──→ modem ──→ router ──→ your phone
                         │
                    ──→ your laptop
                    ──→ your smart TV
```

### Key Facts for Dummies

- **No SIM card needed.** WiFi does not connect to cell towers. If the internet is down, local WiFi still works between devices on your network (e.g. printing, file sharing) but you can't get online.
- **WiFi does NOT replace a SIM card.** A WiFi-only tablet can't make phone calls or use cellular data. You need WiFi or a phone hotspot.
- **Range** is about one house. Thick walls kill it. Extenders help.
- **Speed** depends on how many devices are connected, how far you are from the router, and whether you're on 2.4 GHz or 5 GHz.
- **Power** is OK for laptops (2–5W) but terrible for battery-powered sensors. A WiFi-connected temperature sensor needs recharging every few days.

### 2.4 GHz vs 5 GHz vs 6 GHz — What to Use

| Band | Range Through Walls | Max Speed | Best Use |
|------|-------------------|-----------|----------|
| 2.4 GHz | **Good** | 150–600 Mbps | General browsing, devices far from router, walls |
| 5 GHz | Poor | 800–1300 Mbps | Gaming, video streaming, same room as router |
| 6 GHz | Very poor | 2000+ Mbps | Short-range high speed, future devices |

If your device is in the same room as the router, use 5 GHz. If it's two rooms away through brick walls, 2.4 GHz will actually be faster because 5 GHz would drop packets.

### When to Use WiFi in a Project

- You need high-speed data transfer (video streaming, file uploads)
- Your device can be plugged into power or recharged daily
- You're inside a building with existing WiFi
- You want to stream sensor data to a web page or MQTT broker

**Good for:** ESP32 projects, security cameras, smart displays, media streamers.

**Bad for:** Battery-powered sensors, outdoor projects far from the router, anything that needs to work in the middle of nowhere.

## Bluetooth — Short Range, Low Power

### How It Works

Bluetooth is a **direct device-to-device** connection. No router. No internet (unless your phone bridges it). Two devices "pair" and talk to each other.

```
phone ───→ wireless speaker
        (direct, no router)
```

There are two kinds of Bluetooth:

**Bluetooth Classic (BT 2.0–4.0):**

- Designed for continuous data streams like audio
- Uses more power
- Up to ~3 Mbps
- Used in: wireless headphones, car audio, file transfer between phones

**Bluetooth Low Energy (BLE / BT 4.0+)**

- Designed for small bursts of data
- **Very low power** — a coin-cell battery can run a BLE sensor for years
- Up to ~1 Mbps
- Used in: fitness trackers, temperature sensors, beacons, smart locks

### Key Facts for Dummies

- **Bluetooth is NOT WiFi.** You can't browse the internet over Bluetooth (unless your phone shares its data connection via tethering, and even then your phone acts as a bridge).
- **Range is about 10m (30ft) for Classic, up to 100m for BLE** in open air. Walls kill it fast.
- **Pairing** is required first time. Devices need to discover each other and exchange keys.
- **Bluetooth can't connect many devices** — typically 7 at a time for Classic. BLE can do more.
- **The 2.4 GHz jam** — Bluetooth and WiFi share the same frequency. They interfere. That's why your Bluetooth headphones crackle when you're on a WiFi call.

### BLE — The IoT Superstar

BLE is the most important wireless technology for electronics hobbyists. It's cheap (ESP32 has it built-in, modules cost $2), sips power, and works with any smartphone.

| Feature | BLE vs Bluetooth Classic |
|---------|-------------------------|
| Range | Better (up to 100m in open air) |
| Speed | Worse (1 Mbps vs 3 Mbps) |
| Power | **Dramatically better** (0.01W vs 0.1W) |
| Pairing | Simpler (advertising + connect, no UI) |
| Device count | Higher (theoretically unlimited) |
| Audio | **No** — BLE can't stream audio reliably |

### When to Use Bluetooth

- You need to connect a smartphone to your project
- Short range is acceptable
- Low power is important
- You don't need internet (or your phone provides it through tethering)

**Good for:** Fitness trackers, temperature/humidity sensors, smart locks, wireless game controllers, beacons, Arduino/ESP32 phone control.

**Bad for:** Streaming video, long-range outdoor projects, connecting 50+ devices, audio streaming (use Classic for audio).

## Cellular / SIM Card — The Internet Everywhere

### How It Works

A cellular module (with a SIM card) connects to **cell towers** just like your phone. The SIM card identifies you to the network and tells the carrier who you are and what plan you have.

```
sensor_with_4G ───→ cell tower ──→ internet ──→ your server
     │
  (SIM card inside)
```

### Key Facts for Dummies

- **A SIM card is an identity, not internet.** The SIM says "I am subscriber XYZ on carrier ABC." The modem does the actual connecting.
- **You need a data plan.** Unlike WiFi (free after you pay your ISP) or Bluetooth (free), cellular requires a monthly subscription. Typically $2–$15/month for IoT plans.
- **Range is measured in kilometers.** That's the killer feature — your device works anywhere there's cell coverage.
- **Power is terrible.** A 4G modem draws ~2W when transmitting. That's ~100x more than BLE. You need a big battery or solar panel.
- **Latency is higher.** It takes 50–100ms just to set up a connection. For real-time control, this matters.

### 4G/LTE vs 5G vs NB-IoT / LTE-M

| Technology | Speed | Power | Range | Cost | Best For |
|-----------|-------|-------|-------|------|----------|
| 4G/LTE (Cat 1) | 10 Mbps down | ~2W | ~10km | $10–20/yr | General IoT, moderate data |
| 4G/LTE (Cat M1) | 1 Mbps down | ~0.5W | ~10km | $2–5/yr | Low-power IoT, sensors |
| NB-IoT | 200 kbps | ~0.1W | ~15km | $1–3/yr | Ultra-low power, tiny data |
| 5G (sub-6) | 1 Gbps down | ~3W | ~1km | ~$20/yr | High-bandwidth mobile |
| 5G (mmWave) | 10 Gbps down | ~5W | ~200m | Expensive | Stadiums, dense urban |

**Cat M1 (LTE-M) and NB-IoT** are the most important for hobbyists making real products. They're designed for IoT — lower speed but dramatically lower power and cost. A temperature sensor sending one reading per hour can run for years on two AA batteries.

### When to Use Cellular / SIM

- Your device needs to work **anywhere** (farm, highway, forest, ocean buoy)
- You already have a data plan or your client pays for connectivity
- You're building a commercial product that needs guaranteed connectivity
- WiFi isn't available (outdoor/long-range/mobile projects)

**Good for:** GPS trackers, agricultural sensors, remote weather stations, fleet tracking, alarm systems.

**Bad for:** Battery-powered frequent transmissions, indoor-only projects (WiFi is cheaper and simpler), anything where you don't want a monthly bill.

## Wireless Mouse/Keyboard — RF Dongle Life

### How It Works

Your wireless mouse or keyboard uses a **simple radio link** on 27 MHz or 2.4 GHz. The USB dongle that comes with it is actually a tiny radio receiver. When you plug it in, the mouse and dongle are already "paired" from the factory.

```
mouse ───→ USB dongle ──→ computer
(via radio)     │
            (already paired, no setup)
```

### Key Facts for Dummies

- **This is NOT Bluetooth.** Even though both use 2.4 GHz, they work completely differently. Bluetooth is a standard. Wireless mice use proprietary protocols that only work with their specific dongle.
- **No pairing needed.** It just works when you plug in the dongle. That's the whole point.
- **Much lower latency** than Bluetooth. For gaming mice, the difference matters (1ms vs 8ms+).
- **Dongle stays in the computer.** Lose it, and the mouse is useless unless you buy a replacement.
- **Battery lasts months or years.** They're extremely simple.
- **Some newer mice do use Bluetooth** (especially ones that also work with tablets/phones). These usually still come with a dongle as an option.

### Dongle vs Bluetooth — Which Input Device Protocol

| Feature | RF Dongle (Mouse/Keyboard) | Bluetooth HID |
|---------|---------------------------|---------------|
| Latency | 1–4 ms | 8–20 ms |
| Battery life | Months–years | Weeks–months |
| Pairing | None (pre-paired) | Required |
| Works with | **Only with that dongle** | Any Bluetooth device |
| Multi-device | One mouse, one dongle | Can pair with phone + tablet + laptop |
| Interference | Minimal (narrow band) | WiFi/microwave interference possible |

### When to Use RF Dongle vs Bluetooth for Input

- **Desktop computer with the dongle always plugged in:** RF dongle is better — lower latency, no pairing, longer battery.
- **Laptop user who moves around:** Bluetooth is better — no dongle to lose, works with multiple devices.
- **Gaming:** RF dongle, every time.
- **HTPC / TV computer:** Bluetooth — the dongle would be in the back of the TV where range is bad.

## Other Wireless Technologies You'll Encounter

### Zigbee (and Z-Wave)

Used in **smart home** devices. Unlike WiFi where every device connects directly to your router, Zigbee devices form a **mesh network** — each device can talk to its neighbors, and they relay data to the hub.

```
sensor ───→ light bulb ───→ smart plug ──→ hub ──→ internet
    (each device can relay)
```

- Range: ~20m per device, but mesh extends it
- Speed: 250 kbps (enough for on/off, temperature, dimming)
- Power: Very low (coin-cell battery for years for sensors)
- Needs a hub (Philips Hue, SmartThings, Home Assistant with dongle)
- **Not compatible with WiFi or Bluetooth** — needs its own hardware

**Best for:** Smart lights, motion sensors, door sensors, thermostats.

### LoRa / LoRaWAN

The long-range champion. A single LoRa gateway can cover several kilometers. Used for IoT sensors that send tiny amounts of data.

- Range: 2–15km depending on terrain
- Speed: 0.3–50 kbps (very slow — you're not sending photos)
- Power: Extremely low (a sensor can run for years on a battery)
- Needs a gateway (or use a public LoRaWAN network like The Things Network)

**Best for:** Soil moisture sensors, water meters, cattle tracking, parking sensors, any "send a few bytes once an hour from the middle of nowhere" project.

### NFC (Near Field Communication)

Used for **tap-to-pay**, keycards, and data transfer when devices are touching (or nearly touching).

- Range: ~4cm (2 inches max). Intentionally short for security.
- Power: A passive NFC tag gets power from the reader's radio field — no battery needed.
- Speed: 106–424 kbps
- Not useful for any data-intensive project.

### Infrared (IR)

The old TV remote control. Uses an LED that emits invisible light.

- Needs **line of sight** — you must point the remote at the device
- Range: ~5m
- Cheap, simple, no pairing
- Still common for: TV remotes, AC remotes, some distance sensors

**Best for:** Simple remote controls, line-of-sight data transfer.

## Which One Should You Use? Decision Flow

```
Do you need internet everywhere?
│
├─ Yes → Does your client pay a monthly fee?
│   │
│   ├─ Yes → Cellular / 4G / LTE-M
│   │
│   └─ No → Can you exist without real-time data?
│       │
│       ├─ Yes → LoRaWAN (long range, own gateway)
│       │
│       └─ No → WiFi (need nearby router)
│
└─ No → What's the range?
    │
    ├─ <10m → What are you connecting?
    │   │
    │   ├─ Mouse/keyboard → RF dongle or Bluetooth
    │   ├─ Audio → Bluetooth Classic
    │   ├─ Smart home sensor → Zigbee or BLE
    │   ├─ Control from phone → BLE
    │   └─ Tap to pay / keycard → NFC
    │
    ├─ 10–100m → WiFi or BLE
    │
    └─ 100m+ → LoRa or Cellular
```

## The Big Gotchas

### 1. Power Will Surprise You

This is the #1 thing dummies get wrong. You can't just slap a cellular modem on a project and expect batteries to last.

| Device | Current while transmitting | AA batteries would last |
|--------|--------------------------|------------------------|
| BLE sensor (1 reading/min) | 5 mA | **2+ years** |
| WiFi (ESP32, 1 send/min) | 80 mA | **~2 weeks** |
| 4G modem (1 send/min) | 500 mA | **~2 days** |
| LoRa (1 send/hour) | 20 mA | **~5 years** |

The numbers above assume the device sleeps between transmissions. A simple rule: **the further it talks, the more power it needs.**

### 2. License vs License-Free

- **WiFi, Bluetooth, Zigbee, LoRa** — license-free ISM bands. Anyone can use them. You don't need permission.
- **Cellular** — licensed bands. The carrier paid billions for spectrum rights. You pay them to use it.
- **2.4 GHz** is free but crowded. **868/915 MHz** (LoRa, Z-Wave) is free and much less crowded.
- **GPS** is free (satellites are US government, one-way receive only).

### 3. Interference Is Real

- 2.4 GHz is a disaster zone. WiFi + Bluetooth + Zigbee + microwaves all compete.
- If you deploy 100+ overlapping BLE/WiFi devices, expect reliability problems.
- 5 GHz WiFi is cleaner but has less range.
- Wired is always more reliable. When in doubt, use a cable.

### 4. Vendor Lock-In

- RF dongle mice only work with that dongle. Lose it? New mouse.
- Zigbee products from different brands mostly work together (if certified).
- LoRa modules speak standard LoRaWAN but network servers differ.
- WiFi and Bluetooth are standardized — any device can talk to any other.

## Quick Reference Cards

### For Hobbyist Projects

| Need | Use | Why |
|------|-----|-----|
| Phone controls LED from next room | BLE | Cheap, low power, works with any phone |
| Weather sensor in the garden sends data to web | WiFi (ESP32) | Free, easy, you probably have WiFi in the house |
| GPS tracker on a bike that reports location | 4G LTE-M | Must work anywhere. Pay $3/month. |
| Soil moisture in a field | LoRaWAN | 5km range, 5 years on batteries |
| Smart light bulbs in your house | Zigbee | Mesh network, works without internet |
| Wireless keyboard for gaming | RF dongle | Lowest latency, no pairing fuss |
| Temp/humidity on a plant pot | BLE | Just works, coin cell battery lasts a year |
| Doorbell camera | WiFi | Needs high bandwidth, has power nearby |

### For Commercial Products

| Requirement | Best Fit |
|------------|----------|
| Must work everywhere (global product) | LTE-M + WiFi fallback |
| Lowest possible power | BLE or LoRa (depending on range) |
| Highest reliability | Cellular (licensed band, no interference) |
| Cheapest per device | WiFi (router already there) or BLE (phone already has it) |
| Longest range with no infrastructure | LoRaWAN (public gateways exist) |
| Must pass certification easily | WiFi (FCC/CE certified modules easy to buy) |
| Smart home integration | Zigbee (works with all major hubs) |

## See Also

- [esp32-web-server](/projects/esp32-web-server)
- [esp32-fan-controller](/projects/esp32-fan-controller)
