# Ethernet Module (W5500 / ENC28J60) — Component Reference

## What It Is

An Ethernet module adds **wired network connectivity** to a microcontroller. It lets your project connect to the internet via an Ethernet cable — more reliable than WiFi, no signal dropouts, PoE capable.

## Common Modules

| Module | Interface | Speed | Buffer | Price | Best for |
|--------|-----------|-------|--------|-------|----------|
| **W5500** | SPI | 10/100 Mbps | 32KB internal | $$ | General purpose, reliable |
| **ENC28J60** | SPI | 10 Mbps | 8KB internal | $ | Budget projects, small data |
| **W5100** | SPI | 10/100 Mbps | 16KB internal | $$ | Arduino Ethernet Shield |
| **DM9000** | 16-bit parallel | 10/100 Mbps | None (needs MCU RAM) | $$$$ | High-speed, powerful MCUs |

**W5500** is the best choice for most hobby projects. It handles TCP/IP in hardware (doesn't burden the microcontroller), supports up to 8 simultaneous sockets, and works with 3.3V and 5V logic.

## W5500 vs ENC28J60

| Feature | W5500 | ENC28J60 |
|---------|-------|----------|
| Speed | 10/100 Mbps | 10 Mbps only |
| TCP offload | Full hardware TCP/IP | Software TCP (uses MCU memory) |
| Simultaneous connections | 8 sockets | 1 socket |
| SPI speed | Up to 80 MHz | Up to 20 MHz |
| Internal buffer | 32KB | 8KB |
| 3.3V tolerant | Yes | Yes |
| 5V tolerant | Yes (5V on SPI pins) | No (needs level shifting) |
| Library | Ethernet2 / Ethernet3 | UIPEthernet |
| PoE compatible | Yes (with add-on) | No |

## Wiring W5500

```
W5500 module        Microcontroller
  VCC ─────────────── 3.3V (some modules accept 5V)
  GND ─────────────── GND
  SCK ─────────────── SCK (SPI clock)
  MOSI ────────────── MOSI (data to module)
  MISO ────────────── MISO (data from module)
  CS ──────────────── GPIO (chip select, any pin)
  RST ─────────────── GPIO (reset, optional — tie to 3.3V if unused)
  INT ─────────────── GPIO (interrupt, optional)
```

## Wiring ENC28J60

```
ENC28J60 module     Microcontroller
  VCC ─────────────── 3.3V (DO NOT use 5V)
  GND ─────────────── GND
  SCK ─────────────── SCK
  MOSI ────────────── MOSI
  MISO ────────────── MISO
  CS ──────────────── GPIO (chip select)
  RST ─────────────── GPIO (reset — ENC28J60 needs a proper reset)
```

**Critical:** The ENC28J60 is **5V intolerant** on ALL pins. Use a level shifter or voltage divider on MOSI/CS/SCK if your microcontroller is 5V.

## Library

### W5500

Use the **Ethernet3** library (more modern) or **Ethernet2**:

```cpp
#include <Ethernet3.h>
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
EthernetClient client;

void setup() {
  Ethernet.init(CS_PIN);  // tell library which pin is CS
  Ethernet.begin(mac);
}
```

### ENC28J60

Use the **UIPEthernet** library:

```cpp
#include <UIPEthernet.h>
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
EthernetClient client;

void setup() {
  Ethernet.begin(mac);
}
```

## PoE (Power over Ethernet)

Some W5500 modules support PoE — receiving power through the Ethernet cable alongside data. Requires a **PoE injector** or PoE switch on the other end.

```
Ethernet cable ──┬── W5500 ── SPI ── MCU
                 │
                 └── PoE module ── 5V/3.3V out
```

**Pro:** One cable for power and data. **Con:** PoE injectors add cost, and the module draws power from the network.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| No link light | Cable bad, or no power | Check cable, check module power |
| Link light but no data | Wrong SPI pins or CS pin | Verify SPI wiring, check CS initialization |
| ENC28J60 gets hot | 5V on a 3.3V pin | Replace module (it's dead), use level shifter |
| W5500 not detected | CS pin not configured | Call `Ethernet.init(CS_PIN)` before `begin()` |
| Random disconnects | Power supply noise | Add 100µF cap near module |
| DHCP fails | Router doesn't assign IP | Use static IP: `Ethernet.begin(mac, ip)` |
| Slow data | ENC28J60 + software TCP | Switch to W5500 or reduce data rate |

## Quick Reference

- **W5500:** 10/100 Mbps, hardware TCP/IP, 8 sockets, 32KB buffer. Best choice.
- **ENC28J60:** 10 Mbps only, software TCP, 1 socket, 8KB buffer. Budget option.
- **SPI interface:** SCK, MOSI, MISO, CS. Dedicated CS pin per module.
- **3.3V logic:** ENC28J60 is 3.3V only (will die on 5V). W5500 has 5V tolerant pins.
- **MAC address:** Each module has a unique MAC, or assign one manually.
- **Link LED:** Green = connected to network. Activity LED = data flowing.
- **PoE:** Available on some W5500 modules (power from Ethernet).
- **Library:** Ethernet3 (W5500), UIPEthernet (ENC28J60).
