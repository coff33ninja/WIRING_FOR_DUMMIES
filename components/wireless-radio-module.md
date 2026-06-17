# Wireless Radio Module (nRF24L01) — Component Reference

## What It Is

The nRF24L01 is a **2.4 GHz wireless transceiver module**. It lets you send data wirelessly between two microcontrollers at ranges up to 100m (with PA+LNA version). It's cheap, low-power, and works with 3.3V logic.

## Variants

| Variant | Range | Power | Best for |
|---------|-------|-------|----------|
| nRF24L01 (basic) | ~30m indoor | 0 dBm | Simple sensor-to-display, short range |
| nRF24L01+ PA+LNA | ~1000m line-of-sight | 20 dBm (100mW) | Long range, outdoor, drone control |
| nRF24L01+ (improved) | ~50m indoor | 0 dBm | Slightly better than original |

**PA+LNA** has a larger board with a separate antenna and draws ~115mA when transmitting — too much for a coin cell.

## Wiring (SPI)

The nRF24L01 uses **SPI** plus one extra pin for CE (Chip Enable). Every module needs a 10µF capacitor across VCC and GND — it draws current in bursts and will brown-out the 3.3V regulator without one.

```
nRF24L01           Microcontroller (3.3V)
  VCC ────────────── 3.3V
  GND ────────────── GND
  CE  ────────────── GPIO (any pin)
  CSN ────────────── GPIO (any pin, acts as SS/CS)
  SCK ────────────── SCK (SPI clock)
  MOSI ───────────── MOSI (SPI data in)
  MISO ───────────── MISO (SPI data out)
  IRQ ────────────── (optional, can leave unconnected)
```

Add a **10µF electrolytic capacitor** between VCC and GND as close to the module as possible. Without it, the module may fail to transmit or reset unexpectedly.

## Power

- **Supply voltage:** 3.3V only (3.0–3.6V absolute max). **Do not use 5V**.
- **Standby:** ~20µA (ultra low power)
- **TX at 0 dBm:** ~11mA
- **TX at 20 dBm (PA+LNA):** ~115mA
- **RX:** ~13mA

If using with a 5V Arduino, power through a 3.3V regulator. The 3.3V pin on an Arduino cannot supply enough current — use a separate AMS1117-3.3.

## Addresses

Each nRF24L01 has a **pipe address** — think of it as a radio channel. Both transmitter and receiver must use the same address and channel.

Pipes can use different addresses for multi-point networks. A single receiver can listen to up to 6 different transmitters on 6 different pipe addresses.

## Communication

Basic communication: one module sends, the other receives (unidirectional) or both can send/receive.

```
Transmitter:                          Receiver:
  radio.openWritingPipe(address)        radio.openReadingPipe(1, address)
  radio.write(&data, sizeof(data))      radio.read(&data, sizeof(data))
```

Maximum payload per packet: **32 bytes**. Send multiple packets for larger data.

## Library

Use the **RF24** library (maniacbug / TMRh20):

- `RF24 radio(CE, CSN)` — create radio object
- `radio.begin()` — initialize
- `radio.openWritingPipe(address)` — set TX address
- `radio.openReadingPipe(pipe, address)` — set RX address
- `radio.write(&data, size)` — transmit
- `radio.available()` — check for received data
- `radio.read(&data, size)` — read received data

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| No communication | Different addresses | Check both modules use the same address and channel |
| No communication | 5V on VCC | Module needs 3.3V exact |
| Module resets during TX | No decoupling cap | Add 10µF cap between VCC and GND |
| Short range | Antenna damaged | Replace module, keep antenna clear of metal/ground planes |
| Intermittent connection | Loose SPI wiring | Check all SPI pins make good contact |
| PA+LNA draws too much | Power supply weak | Use separate 3.3V regulator (AMS1117) |
| Can't communicate through walls | Basic module, 2.4GHz attenuation | Use PA+LNA variant, keep modules elevated |

## Quick Reference

- **3.3V only.** Never connect to 5V. Use a regulator.
- **SPI interface:** CE + CSN + SCK + MOSI + MISO
- **Must have:** 10µF decoupling capacitor near module
- **Range:** Basic = ~30m, PA+LNA = ~1000m
- **Payload:** Max 32 bytes per packet
- **Frequency:** 2.4 GHz ISM band (choose channel to avoid WiFi interference)
- **Addresses:** 40-bit, must match on TX and RX
- **Multi-point:** 1 receiver can listen to 6 transmitters
