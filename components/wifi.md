# WiFi (ESP32 / ESP8266) — Component Reference

## What It Is

WiFi modules connect your project to a wireless network for IoT, web servers, MQTT, and OTA updates. The ESP8266 was the breakout hit — a $3 WiFi chip for Arduino. The ESP32 supersedes it with built-in Bluetooth, dual cores, and more GPIO. Both can run as standalone microcontrollers or as AT-command-driven coprocessors for another MCU.

> **Analogy:** A tiny web server that fits on a breadboard. It can fetch weather data, serve a web page, or report sensor readings over your home WiFi — all for the cost of a coffee.

## ESP32 vs ESP8266 — Which One to Use

| Feature | ESP32 | ESP8266 (ESP-01) |
|---------|-------|-------------------|
| CPU | Dual-core Xtensa LX6 @ 240 MHz | Single-core Xtensa L106 @ 80 MHz |
| RAM | 520 KB SRAM + 4 MB PSRAM (some) | 160 KB (50 KB usable) |
| Flash | 4–16 MB (built-in) | 1–4 MB (external) |
| WiFi | 802.11 b/g/n, 2.4 GHz | 802.11 b/g/n, 2.4 GHz (same) |
| Bluetooth | Classic + BLE (dual mode) | None |
| GPIO count | ~25 (varies by dev board) | ~9 (ESP-01 exposes only 2) |
| ADC | 2 × 12-bit (18 channels total) | 1 × 10-bit |
| Performance | TCP throughput ~80 Mbps | TCP throughput ~10 Mbps |
| Price | ~$3–6 | ~$1–3 |
| Power (TX) | ~300–500 mA peak | ~200–300 mA peak |
| Power (sleep) | ~10 µA (deep sleep) | ~20 µA (deep sleep) |
| Ease of wiring | Built-in USB, voltage reg | Needs 3.3V regulator, USB-serial |

**Decision rule:** Use ESP8266 for simple sensor nodes (send data once/minute). Use ESP32 when you need Bluetooth, multiple analog inputs, more GPIO, or better performance. ESP32 is almost always the better choice today for new projects.

## WiFi Bands and Standards

| Standard | Frequency | Max speed | Range |
|----------|-----------|-----------|-------|
| 802.11b | 2.4 GHz | 11 Mbps | Best range |
| 802.11g | 2.4 GHz | 54 Mbps | Good range |
| 802.11n | 2.4 GHz | 150 Mbps (HT20) | Good range (MIMO) |

**Both ESP32 and ESP8266 are 2.4 GHz only.** They do not support 5 GHz bands. If your home WiFi runs 5 GHz-only (uncommon — nearly all routers broadcast both), the module won't see it.

**Why 2.4 GHz matters for wiring:**

- 2.4 GHz penetrates walls better than 5 GHz
- But it also overlaps with microwave ovens, cordless phones, and USB 3.0 noise
- The module has no antenna connector by default — the PCB trace is the antenna

## Station Mode vs Access Point Mode

### Station Mode (STA) — Connects to a Router

```
   ESP32 ── WiFi ── Router ── Internet
                         │
                     ┌───┴───┐
                     │ Phone │
                     └───────┘
```

The ESP joins your existing network, gets an IP from DHCP, and can reach the internet or be reached by other devices on the same network.

**Use for:** MQTT to a broker, HTTP requests to APIs, serving a web page accessible from any device on your WiFi.

**Code pattern:**
```cpp
WiFi.begin("SSID", "password");
while (WiFi.status() != WL_CONNECTED) delay(100);
Serial.println(WiFi.localIP());
```

### Access Point Mode (AP) — Creates Its Own Network

```
   ESP32 ── broadcasts ── "ESP32-Net"
                              │
                         ┌────┴────┐
                      Phone     Laptop
```

The ESP creates its own WiFi network. Other devices connect directly to it, no router needed. Max ~5 clients.

**Use for:** Initial configuration (captive portal to enter WiFi credentials), direct phone-to-device control without internet, demos where no WiFi infrastructure exists.

**Code pattern:**
```cpp
WiFi.softAP("ESP32-Config", "password");
Serial.println(WiFi.softAPIP()); // default 192.168.4.1
```

### Combined Mode (STA+AP)

The ESP connects to your router AND hosts its own access point simultaneously. Common for "configuration mode" — the AP hosts a setup page, and once configured, the ESP connects to the real network while the AP stays available for troubleshooting.

## ESP8266 — The AT Command Approach

The ESP8266 originally shipped with AT firmware. You talk to it over UART, just like the Bluetooth modules:

```
   Arduino                        ESP8266
   ┌──────┐                      ┌──────┐
   │ TX   ───────────────────── RX   │
   │ RX   ───────────────────── TX   │
   │ GND  ───────────────────── GND  │
   │ 5V   ── regulator ── 3.3V ── VCC│
   └──────┘                      └──────┘
```

The Arduino sends AT commands over serial, the ESP8266 handles all the WiFi/TCP work:

| AT Command | What it does |
|------------|-------------|
| `AT+CWMODE=1` | Set station mode |
| `AT+CWJAP="SSID","pass"` | Connect to WiFi |
| `AT+CIFSR` | Get IP address |
| `AT+CIPSTART="TCP","192.168.1.5",80` | Open TCP connection |
| `AT+CIPSEND=5` | Send 5 bytes of data |
| `AT+CIPCLOSE` | Close connection |

**Downsides to AT firmware:**

- Clunky — two-device debugging, shared serial port
- Limited throughput — the serial link is slower than the WiFi chip can handle
- No access to ESP8266's full potential
- Most projects today skip AT firmware and program the ESP directly

## ESP32 / ESP8266 Native SDK — Full Control

Both ESP32 and ESP8266 can be programmed directly from the Arduino IDE (install the board package) or PlatformIO. No separate Arduino needed.

```
   USB cable ──── ESP32 Dev Board ──── GPIO pins
                    │
                    ├── WiFi (built-in)
                    ├── Bluetooth (ESP32 only)
                    ├── I2C, SPI, UART, ADC, DAC
                    └── File system (SPIFFS / LittleFS)
```

**Key difference from AT approach:** The ESP is the main processor. It reads sensors, controls outputs, AND handles WiFi. One chip, one program.

**Libraries you'll use:**

| Task | ESP32 Library | ESP8266 Library |
|------|--------------|-----------------|
| WiFi connection | `WiFi.h` | `ESP8266WiFi.h` |
| HTTP server | `WebServer.h` | `ESP8266WebServer.h` |
| HTTP client | `HTTPClient.h` | `ESP8266HTTPClient.h` |
| MQTT | `PubSubClient.h` (or `esp-mqtt`) | `PubSubClient.h` |
| OTA updates | `ArduinoOTA.h` | `ArduinoOTA.h` |
| WebSockets | `WebSocketsServer.h` | `WebSocketsServer.h` |

## Power Consumption — The 300 mA Peak Problem

WiFi is power-hungry. When transmitting, the ESP can draw a spike of 300–500 mA.

```
   Idle:       ~50–80 mA
   Connected:  ~80–120 mA
   Transmit:   ~200–500 mA (peak, 10–100 ms bursts)
   Modem sleep: ~5–20 mA (WiFi connected but radio off most of time)
   Deep sleep:  ~10 µA (ESP32), ~20 µA (ESP8266)
```

**Wiring implications:**

- **DO NOT power an ESP8266 from an Arduino's 3.3V pin** — the regulator can't supply the peak current. Use a dedicated 3.3V regulator (AMS1117-3.3) rated for 800 mA+.
- **DO power an ESP32 dev board via USB** or the 5V pin (it has a regulator onboard). The 3.3V pin on a dev board is output only — supplying 3.3V there bypasses the regulator and is fine if your supply can handle the peaks.
- **Keep power wires short and thick** — voltage drop on long breadboard jumpers during transmit peaks causes brownouts.

**Capacitor rule:** Add a 100–470 µF electrolytic capacitor between VCC and GND near the module's power pins. This provides a local reservoir for transmit peaks. Without it, the voltage dips, the module browns out, and your code crashes.

## Antenna Types

```
   PCB Trace Antenna            Ceramic Antenna           External Antenna    
   ┌───────────────────┐    ┌────────────────────┐    ┌────────────────────┐
   │                   │    │                    │    │                    │
   │  ▓▓▓▓▓▓▓▓▓▓      │    │   ▒▒▒▒             │    │   ┌─┬─┬─┐         │
   │  (zigzag trace)   │    │   (ceramic chip)   │    │   │ U│ │U.FL      │
   │                   │    │                    │    │   │ .│ │connector │
   └───────────────────┘    └────────────────────┘    └───┴─┴─┴──────────┘
```

| Type | Range | Size | Cost | Found on |
|------|-------|------|------|----------|
| PCB trace | ~50–100m (line of sight) | Medium (part of PCB) | Free | Most dev boards (ESP32 DevKit, NodeMCU) |
| Ceramic chip | ~30–80m | Tiny (~3×2 mm) | ~$0.10 | ESP-12, ESP-07, compact modules |
| External (U.FL/IPEX) | ~100–300m+ (with proper antenna) | Connector + antenna | ~$1–3 | ESP-07, ESP32 with U.FL, industrial modules |

**Practical advice:** The PCB trace antenna on most dev boards is good enough for a house. Don't add an external antenna unless you need to put the board inside a metal box (the metal blocks the PCB antenna, and the external antenna goes outside the box).

## Security

| Feature | What it does |
|---------|-------------|
| WPA2-PSK | Pre-shared key (password) — standard home WiFi security. Supported. |
| WPA3 | Newer standard — **not supported** by ESP32/ESP8266 |
| WEP | Ancient, broken — supported but don't use |
| Enterprise (WPA2-802.1X) | Radius server auth — supported with extra code |
| TLS/SSL | ESP32 has hardware crypto acceleration. ESP8266 is very slow with TLS. |
| HTTPS | Works on both, but ESP8266 struggles with cert verification |

**Encrypt if sending data over the internet.** Use MQTT over TLS (port 8883) or HTTPS. Unencrypted HTTP means anyone on the same network can read your sensor data or control commands.

## Common Uses

### IoT Sensor Node

```
   Sensor ── ESP32 ── WiFi ── Internet ── MQTT Broker ── Dashboard
   (DHT22)         publishes every 60s        │
                                         (cloud or local)
```

ESP reads temperature/humidity, connects to WiFi, publishes to MQTT broker, then deep sleeps for 60 seconds. Power consumption averages ~0.5 mA (deep sleep + brief transmit).

### Web Server (On-Device Control)

```
   Phone browser ── WiFi ── ESP32
   (192.168.1.42)        serves HTML page
                           with on/off button
```

ESP hosts a web page with a simple UI. Click a button, it sends a request, ESP turns a pin HIGH. No cloud, no app, no internet required.

### OTA Updates

```
   Computer ── WiFi ── ESP32 (flash wirelessly)
   (Arduino IDE / PlatformIO upload)
```

Upload new firmware over the air. Essential for devices mounted in hard-to-reach places. First flash includes the OTA library, subsequent flashes go over WiFi.

## Common Mistakes

| Mistake | Result |
|---------|--------|
| Powering ESP8266 from Arduino 3.3V pin | Brownouts, random resets, WiFi disconnect |
| No decoupling capacitor near VCC pins | WiFi transmit crashes the chip |
| 5V directly to ESP8266 VCC | Instant death (3.3V max) |
| ESP32 3.3V pin used as power input | Works but bypasses regulator — must be stable 3.3V |
| Long thin wires from power supply | Voltage drop during TX peaks → brownout |
| Placing ESP in a metal enclosure | WiFi blocked completely |
| Using AP mode with 10+ clients | Clients can't connect (max ~5) |
| SSID with spaces or special chars | Connection fails silently |
| Forgetting to flush serial buffers during AT commands | Commands get eaten — add delays |
| ESP8266 with TLS connections | Slows to a crawl — use ESP32 for secure connections |
| No watchdog timer in production code | ESP hangs after hours/days — use `ESP.wdtEnable()` |

## Quick Reference

```
ESP32 (standalone):
  VCC → 5V (dev board USB or Vin pin)
  3.3V → output (do not use as input on dev board)
  Built-in USB → programming + serial
  WiFi + BT + dual-core CPU in one chip
  GPIO: ~25 pins, many with ADC/Touch/PWM
  Deep sleep: ~10 µA

ESP8266 (ESP-01 / NodeMCU):
  VCC → 3.3V (regulated, 500 mA+ capable)
  3.3V only — 5V destroys it
  Needs external USB-serial for programming
  GPIO: 2 (ESP-01) or ~9 (NodeMCU)
  Deep sleep: ~20 µA
  No Bluetooth

Station mode: Connects to router (standard setup)
AP mode: Creates its own network (config pages, direct control)
STA+AP: Both simultaneously (setup portal + normal operation)

Power tips:
  ESP32: 100 µF on 3.3V, 470 µF on Vin
  ESP8266: 470 µF on 3.3V, avoid Arduino 3.3V pin
  Deep sleep + periodic transmit = ~0.5 mA average

WiFi limits:
  2.4 GHz band only (no 5 GHz)
  WPA2 supported, WPA3 not supported
  Range ~50m indoor with PCB antenna
  Max ~5 AP clients
```
