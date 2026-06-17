# Cellular Module (SIM800 / SIM7000) — Component Reference

## What It Is

A cellular module lets your project **connect to the mobile phone network**. It can make calls, send/receive SMS, and connect to the internet (2G, 3G, NB-IoT, LTE-M, or Cat-M1 depending on the module). This gives your project connectivity anywhere there's cell service.

## Common Modules

| Module | Network | Data | Best for |
|--------|---------|------|----------|
| **SIM800L** | 2G (GSM/GPRS) | GPRS (up to 85 kbps) | SMS, small data, regions with 2G still active |
| **SIM900** | 2G (GSM/GPRS) | GPRS (up to 85 kbps) | Older projects, still widely documented |
| **SIM7000E/G** | LTE-M / NB-IoT / 2G | Up to 375 kbps | IoT, low-power, future-proof |
| **SIM7600** | 4G LTE | Up to 150 Mbps | High-speed data, voice, video |
| **A7670/A7682** | 4G LTE | Cat-1 / Cat-M1 | IoT, replacement for SIM7000 |

**SIM800L** is the most common in hobby projects — small, cheap, and well-documented. But 2G networks are being shut down worldwide.

**SIM7000** is the modern replacement — supports LTE-M and NB-IoT (low-power wide-area networks designed for IoT).

## SIM800L — Wiring

The SIM800L module draws **bursts of up to 2A** during transmission. It needs a **dedicated power supply** — do NOT power from a microcontroller's 3.3V pin.

```
SIM800L               Power supply (4V)
  VCC ─────────────────┤
                       │
  GND ─────────────────┤
                       │
  TX ────────────────── MCU RX (3.3V logic)
  RX ────────────────── MCU TX (3.3V — use voltage divider if 5V MCU)
  RST ───────────────── GPIO (optional reset)
  NET ───────────────── (for external antenna, or use PCB trace)

  ⚠ Add 100–470µF capacitor across VCC and GND (prevents brown-out)
```

### Power Supply

| Requirement | Value |
|-------------|-------|
| Supply voltage | 3.4–4.4V (4V nominal) |
| Peak current | 2A (during transmission burst) |
| Average current | ~220mA (during call/data) |
| Idle current | ~20mA |
| Sleep current | ~0.7mA (if configured) |

**Recommended supply:** A dedicated Li-ion battery (3.7V) or a 5V→4V buck converter with >= 2A rating. A 3.3V regulator won't provide enough voltage or current.

### Logic Level

SIM800L uses **3.3V logic**. If your microcontroller is 5V (Arduino Uno), use a voltage divider on the TX line:

```
MCU TX (5V) ──── 1kΩ ──┬── SIM800L RX
                        │
                        2.2kΩ
                        │
                       GND
```

Or use a level shifter module.

## SIM800L — SIM Card

The SIM800L uses a **2G SIM card** (the same as an old cell phone). You need:

1. **An active SIM** — prepaid or monthly plan with SMS/data
2. **Unlocked** — not carrier-locked to a specific network
3. **PIN disabled** — the module can't enter the SIM PIN. Disable it in a phone first
4. **Available 2G network** — check coverage in your area

## SIM7000 — Key Differences

| Feature | SIM800L | SIM7000 |
|---------|---------|---------|
| Network | 2G only | LTE-M, NB-IoT, 2G fallback |
| Supply voltage | 3.4–4.4V | 2.7–4.2V |
| Peak current | 2A | ~500mA (NB-IoT is very low power) |
| Sleep current | ~0.7mA | ~0.4mA (PSM: 3µA) |
| Data speed | 85 kbps | Up to 375 kbps |
| GNSS/GPS | No (add separate) | Built-in (GPS/GLONASS) |
| Future-proof | No (2G sunset) | Yes |

## Sending an SMS

```cpp
#include <SoftwareSerial.h>
SoftwareSerial sim(10, 11);  // RX, TX

void setup() {
  sim.begin(9600);
  delay(1000);

  sim.println("AT");  // test communication
  delay(500);

  sim.println("AT+CMGF=1");  // text mode
  delay(500);

  sim.println("AT+CMGS=\"+1234567890\"");
  delay(500);
  sim.print("Hello from Arduino!");
  sim.write(26);  // Ctrl+Z to send
}
```

## Making an HTTP Request

```cpp
sim.println("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"");
sim.println("AT+SAPBR=3,1,\"APN\",\"your-apn\"");
sim.println("AT+SAPBR=1,1");  // open bearer
sim.println("AT+HTTPINIT");
sim.println("AT+HTTPPARA=\"URL\",\"http://example.com/data\"");
sim.println("AT+HTTPACTION=0");  // GET request
```

You'll need the **APN** from your SIM provider (e.g., "internet" for many carriers).

## Antenna

| Module | Antenna | Note |
|--------|---------|------|
| SIM800L | PCB trace (onboard) | Works for good signal areas. Add external U.FL antenna for weak signal. |
| SIM800L with external antenna | U.FL connector | Solder on a U.FL to SMA pigtail |
| SIM7000 | Usually U.FL | Always use external antenna |

**Signal problems are the #1 issue.** If communication fails, check:
- Antenna is connected
- Module is in a location with cell coverage
- Not inside a metal enclosure

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| No response to AT commands | Wrong baud rate | SIM800L defaults to 9600 or 115200 — try both |
| No response to AT commands | Power supply sag | Add 470µF capacitor, ensure 4V supply |
| No response to AT commands | Bad TX/RX wiring | Cross the connections (TX→RX, RX→TX) |
| SIM card not detected | PIN enabled | Disable PIN by inserting in a phone first |
| SIM card not detected | No 2G network | Check coverage, check if 2G is shut down in your region |
| Can't register on network | Weak signal | Move antenna, use external antenna, check your provider |
| SMS not sending | Wrong number format | Use international format (+1234567890) |
| HTTP request fails | APN wrong | Get correct APN from your SIM provider |
| Module resets during transmit | Power can't supply burst current | Bigger capacitor, better power supply |
| GPRS not connecting | APN or username/password | Check with provider |

## AT Command Basics

| Command | What it does |
|---------|-------------|
| `AT` | Test — should respond "OK" |
| `AT+CSQ` | Signal quality (0–31, higher is better) |
| `AT+CREG?` | Network registration status |
| `AT+CMGF=1` | Set SMS text mode |
| `AT+CMGS="number"` | Send SMS |
| `AT+HTTPGET` | HTTP GET request |
| `AT+HTTPPOST` | HTTP POST request |
| `AT+CIPSHUT` | Close GPRS connection |
| `AT+CSCLK=1` | Enable sleep mode |

## 2G Network Shutdown

2G networks are being shut down globally. Check if 2G is available in your region:

| Region | 2G status |
|--------|-----------|
| USA | AT&T: shut down. T-Mobile: 2024. Verizon: shut down. |
| Europe | Some countries still active, others phasing out |
| Asia | Still widely available |
| Australia | Vodafone: shut down 2024 |

If 2G is unavailable in your area, use a **SIM7000** (LTE-M/NB-IoT) or **SIM7600** (4G LTE) instead.

## Quick Reference

- **SIM800L:** 2G GPRS, SMS, voice. Requires active 2G network.
- **SIM7000:** LTE-M / NB-IoT. Lower power, future-proof, has GPS.
- **Power:** 3.4–4.4V @ 2A burst. Add 470µF cap. Do NOT use MCU regulator.
- **Logic:** 3.3V. Use voltage divider if connecting to 5V MCU.
- **SIM card:** Active, unlocked, PIN disabled.
- **Antenna:** Critical for signal. External preferred.
- **AT commands:** Communicate via UART at 9600 or 115200 baud.
- **APN:** Required for data — get from your carrier.
- **Network registration:** Check with `AT+CREG?`
- **2G sunset:** Check if 2G is still active in your region before buying SIM800L.
