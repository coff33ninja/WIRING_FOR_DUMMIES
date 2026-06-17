# Connectors & Wire — A Practical Guide

## What This Covers

Which connector goes where. Which wire gauge for which current. Soldered vs crimped. Every hobbyist has a drawer full of connectors and no idea which is which.

## Wire Gauge (AWG) — Which Size for Which Job

Wire thickness is measured in AWG (American Wire Gauge). **Smaller number = thicker wire.**

| AWG | Diameter (mm) | Max current (chassis wiring) | Max current (power transmission) | Use for |
|-----|--------------|------------------------------|--------------------------------|---------|
| 28 | 0.32mm | 2.3A | 0.2A | Ribbon cable, fine signal wiring |
| **26** | **0.40mm** | **3.7A** | **0.4A** | Dupont jumpers, thin signal wire |
| **24** | **0.51mm** | **5.0A** | **0.6A** | Sensor wiring, data cables |
| **22** | **0.64mm** | **7.0A** | **0.9A** | **Best for breadboards** — stiff enough to push in |
| 20 | 0.81mm | 11A | 1.5A | Power wiring, LED strips |
| 18 | 1.02mm | 16A | 2.3A | Motor power, battery main leads |
| 16 | 1.29mm | 22A | 3.7A | High-current power, car wiring |

> **For breadboarding:** Use **22 AWG solid-core**. Stranded wire frays and won't push into the holes. For modules: pre-crimped Dupont jumpers (usually 26 AWG stranded).

### Solid vs Stranded

| | Solid | Stranded |
|--|-------|----------|
| Flexibility | Stiff — holds shape | Flexible — bends easily |
| Breadboard | **Excellent** — pushes right in | **Poor** — frays, won't stay |
| Solder | Good — holds in place during soldering | OK — needs tinning first |
| Vibration resistance | Poor — work-hardens and breaks | Good — withstands flexing |
| Crimp terminals | Not suitable | **Required** — strands compress |

**Rule:** Solid for breadboards and perfboard. Stranded for anything that moves (panel wiring, robot wiring, battery leads).

## Pin Headers — The Universal Connector

### 2.54mm Pitch (0.1") — Standard

The most common pin header size. Everything uses it: Arduino, ESP32, Raspberry Pi, sensor modules.

| Type | Looks like | Use |
|------|-----------|-----|
| **Male pin header** | Pins sticking up | On modules, Arduinos, ESP32s |
| **Female pin header** | Receptacles | On breadboards, as sockets |
| **Single row** | 1 row of pins | Simple connections |
| **Double row** | 2 rows (2×3, 2×4, etc.) | I2C, ICSP, JTAG |

### 2.0mm Pitch — Compact

Smaller than standard. Common on compact modules (ESP8266, some sensors). Won't fit on a standard breadboard.

### 1.27mm Pitch — Miniature

Half of 2.54mm. Used on very compact boards. **Hard to hand-solder.** Avoid if possible for hobby work.

## Dupont Connectors — The Hobby Standard

Pre-crimped jumper wires with 2.54mm housings. Come in three flavors:

| Type | Connects | Use |
|------|----------|-----|
| **Male-to-Male (M/M)** | Pin to pin | Breadboard to breadboard, module to module |
| **Male-to-Female (M/F)** | Pin to socket | Module (male) to ESP32 (female socket) |
| **Female-to-Female (F/F)** | Socket to socket | Module (male pins) to sensor (male pins) |

**Buy a kit** with 40+ wires of each type in assorted lengths and colors. **Color-code your wiring:**
- **Red** = VCC / power
- **Black** = GND
- **White / Yellow** = Data / signal
- **Blue / Green** = Secondary signals

## JST Connectors — The Standardized Ones

JST is a brand that makes many small connectors. They all look similar but are **not compatible**.

### JST-PH (2.0mm pitch)

Small, white connector. Common on **single-cell Li-ion/LiPo batteries** (1S 18650 packs). Also found on some sensors.

### JST-XH (2.54mm pitch)

Larger, usually has more pins. Common on **balance leads of LiPo batteries** (2S, 3S, 4S — you see 3-pin, 4-pin, 5-pin versions).

### JST-SM (2.5mm pitch)

Common on **LED strip connectors** — the white 2-pin or 3-pin connectors on WS2812B/NeoPixel strips.

### How to tell them apart

| Type | Pitch | Pin count | Typical use |
|------|-------|-----------|-------------|
| JST-PH | 2.0mm | 2–6 | Li-ion battery packs, small sensors |
| JST-XH | 2.54mm | 2–10 | LiPo balance leads |
| JST-SM | 2.5mm | 2–3 | LED strip connections |
| Dupont | 2.54mm | 1 (individual) | General hobby wiring |

> **They are NOT cross-compatible.** A PH housing won't fit on XH pins even though they look similar. Check the pitch before ordering.

## Screw Terminals — For Permanent Power Connections

| Type | Pitch | Use |
|------|-------|-----|
| **2-pin** | 3.5mm or 5.08mm | Power input, speaker output |
| **3-pin** | 3.5mm | Sensor terminals (VCC, GND, SIG) |
| **Pluggable** | 3.5mm | Plug-in terminal block — removable |

**Use for:** Power supply connections, high-current loads, any connection that needs to be secure and semi-permanent.

## USB Connectors

| Type | Use | Data? | Power |
|------|-----|-------|-------|
| **USB-A** | Computer port, charger port | Yes | 5V, up to 2.4A+ |
| **USB-B** | Arduino Uno, printers | Yes | 5V |
| **USB-C** | Modern phones, laptops | Yes | 5V–20V, up to 5A (with PD) |
| **Micro-B** | ESP32, phone chargers (older) | Yes | 5V, up to 2A |
| **Mini-B** | Old phones, digital cameras | Yes | 5V |

**For ESP32:** Most dev boards use **Micro-USB**. Some newer boards (ESP32-S3, C3) use **USB-C**.

## Which Connector for Which Job

| Application | Connector | Why |
|-------------|-----------|-----|
| Power from wall adapter | **Barrel jack** 5.5×2.1mm | Standard, secure, polarity-protected |
| USB from computer | **USB-A to Micro-B** or **USB-C** | Standard for ESP32 boards |
| Sensor module to breadboard | **Dupont F/F** | Module pins → breadboard |
| Breadboard to breadboard | **Dupont M/M** | Pin to pin |
| Battery pack to board | **JST-PH 2-pin** | Standard for 1S Li-ion |
| High-current power wires | **Screw terminal** or **XT60** | Secure, high current |
| LED strip connections | **JST-SM 3-pin** | Standard for WS2812B |
| Signal wiring on PCB | **Pin headers 2.54mm** | Universal |

## Quick Reference

```
Wire gauge for breadboard: 22 AWG solid-core
Wire gauge for power:      18–20 AWG stranded
Wire gauge for sensors:    24–26 AWG stranded or solid

Connectors (2.54mm pitch — most common):
  Dupont (individual)     → modules, breadboards, sensors
  Pin headers (single)    → on PCB, ESP32, Arduino
  Pin headers (double)    → ICSP, I2C, JTAG

JST family (NOT cross-compatible):
  PH (2.0mm) → Li-ion batteries, small sensors
  XH (2.54mm) → LiPo balance leads (multiple cells)
  SM (2.5mm) → LED strip connectors

Power:
  Barrel jack → wall adapters (center-positive, 5.5×2.1mm)
  USB-A/C   → 5V from computer or phone charger
  Screw terminals → secure power connections
  XT60 → high-current battery (drones, robots)

Color code your wiring:
  Red = power (VCC)
  Black = ground (GND)
  White/Yellow = signal
  Blue/Green = secondary signals
```

## See Also

- [relay-module](/projects/relay-module)
