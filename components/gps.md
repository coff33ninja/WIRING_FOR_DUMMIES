# GPS Module (NEO-6M / NEO-8M / NEO-9M) — Component Reference

## What It Is

A GPS module receives signals from a constellation of satellites orbiting Earth and calculates your position (latitude, longitude, altitude), speed, heading, and the current UTC time. The module does ALL the math internally — your microcontroller just reads the output over a serial connection.

```
Satellites (24+ in orbit)
    │
    │ radio signals (1.5 GHz, L1 band)
    ▼
GPS Module ──serial (UART)──→ Microcontroller
    │
    └── Position: 48.8584°N, 2.2945°E
        Altitude: 324m
        Speed: 0.2 km/h
        Time: 14:32:07 UTC
```

## How It Works (Simplified)

1. The GPS module listens for signals from visible satellites (at least 4 needed for a 3D fix).
2. Each satellite transmits its position and the exact time the signal was sent.
3. The module calculates the distance to each satellite by measuring the time delay (signal travels at the speed of light).
4. With 4+ distances, it triangulates your position — latitude, longitude, altitude.
5. It outputs the result as **NMEA sentences** over serial at 9600 baud (default).

### First Fix (Cold vs Warm vs Hot Start)

| Start | What It Means | Time |
|-------|---------------|------|
| Cold | No almanac, no last position stored | 30–60 seconds |
| Warm | Has almanac but approximate position | 15–30 seconds |
| Hot | Has almanac + last known position + time | 1–5 seconds |
| A-GPS | Uses cellular/WiFi to download orbit data | 1–5 seconds (phones only) |

The first fix is always slow because the module needs to download the almanac (the satellite orbit schedule) — this takes 12+ minutes at the 50 bps data rate from satellites. Many modules save this to battery-backed RAM, so subsequent starts are faster.

## Popular GPS Modules

### NEO-6M (UBLOX)

- **Old but cheap** — $5–8 on breakout boards
- 50 channels
- Update rate: 1 Hz (1 position per second)
- Accuracy: ~2.5m CEP
- Serial output: NMEA at 9600 baud
- **No built-in antenna** — needs external patch antenna
- Has battery backup pin for faster warm starts
- Being phased out (NEO-8M/9M replaced it)

### NEO-8M (UBLOX)

- **Current standard** — $8–12
- 72 channels, better sensitivity than NEO-6M
- Accuracy: ~2.0m CEP
- Supports GPS + GLONASS + BeiDou simultaneously
- Lower power than NEO-6M
- Better indoor/urban performance

### NEO-9M (UBLOX)

- **Latest** — $15–20
- 96 channels, concurrent GNSS (GPS + Galileo + GLONASS + BeiDou)
- Accuracy: ~1.5m CEP
- Supports dead reckoning (works in tunnels for a while)
- Lower power than NEO-8M

### Other Modules

| Module | GNSS Support | Notes |
|--------|-------------|-------|
| BN-220 / BN-880 | GPS + BeiDou | Popular for drones |
| PA1616S | GPS only | Tiny, cheap, good for low power |
| Quectel L70 | GPS only | Very low power (~20mA tracking) |
| SAM-M8Q | GPS + GLONASS | Built-in antenna, compact |
| ATGM336H | GPS + BeiDou | Cheap Chinese alternative (~$3) |

## Wiring (NEO-6M / NEO-8M Typical Breakout)

```
GPS Module            Microcontroller
┌─────────┐           ┌────────────┐
│ VCC     ├───────────┤ 3.3V or 5V │
│ GND     ├───────────┤ GND        │
│ TX      ├───────────┤ RX (UART)  │
│ RX      ├───────────┤ TX (UART)  │
│ PPS     ├───────────┤ (optional) │
└─────────┘           └────────────┘
```

**Important:** Most GPS modules are 3.3V logic but can be powered from 5V (they have an onboard regulator). Check your module's specs. If it's 3.3V logic only, use a voltage divider on the TX→RX line if your microcontroller is 5V.

### Power Consumption Matters

| Module | Tracking | Acquisition | Idle |
|--------|----------|-------------|------|
| NEO-6M | ~45 mA | ~65 mA | ~10 mA |
| NEO-8M | ~25 mA | ~35 mA | ~8 mA |
| NEO-9M | ~20 mA | ~30 mA | ~5 mA |
| PA1616S | ~15 mA | ~25 mA | ~3 mA |
| Quectel L70 | ~20 mA | ~25 mA | ~2 mA |

GPS draws significant current. For battery projects, you MUST power-cycle the module between readings (use a MOSFET to switch VCC) or use a module with a proper sleep mode.

## NMEA Sentences — What You Get

The module outputs text like this at 1-second intervals:

```
$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
$GPGSA,A,3,04,05,,09,12,,,24,,,,,2.5,1.3,2.1*39
$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
```

The most useful sentence for hobbyists is **$GPGGA** (Global Positioning System Fix Data):

| Field | Example | Meaning |
|-------|---------|---------|
| Sentence ID | $GPGGA | GPS fix data |
| Time | 123519 | 12:35:19 UTC |
| Latitude | 4807.038 | 48° 07.038' N |
| N/S | N | North |
| Longitude | 01131.000 | 11° 31.000' E |
| E/W | E | East |
| Fix quality | 1 | 0=invalid, 1=GPS fix, 2=DGPS fix |
| Satellites | 08 | 8 satellites tracked |
| HDOP | 0.9 | Horizontal dilution of precision (lower = better) |
| Altitude | 545.4 | Meters above sea level |

**$GPRMC** (Recommended Minimum) is the other essential one — it includes speed over ground and course over ground, plus the date.

### Parsing in Code (Arduino, with TinyGPS++)

```c
#include <TinyGPSPlus.h>
TinyGPSPlus gps;

void setup() {
  Serial.begin(9600);  // GPS serial
  Serial1.begin(115200); // debug serial
}

void loop() {
  while (Serial.available()) {
    gps.encode(Serial.read());
  }
  if (gps.location.isUpdated()) {
    Serial1.printf("Lat: %.6f, Lng: %.6f\n",
      gps.location.lat(), gps.location.lng());
    Serial1.printf("Alt: %.1f m, Speed: %.1f km/h\n",
      gps.altitude.meters(), gps.speed.kmph());
    Serial1.printf("Sats: %d, HDOP: %.1f\n",
      gps.satellites.value(), gps.hdop.hdop());
  }
}
```

## Antenna — Critical Detail

A GPS module is useless without the right antenna.

| Antenna Type | When to Use | Notes |
|-------------|-------------|-------|
| Patch (ceramic) | Standard outdoor use | Included on most breakout boards |
| Active (with LNA) | Long cable (>1m), indoors | Has built-in amplifier, needs 3.3V power on the antenna line |
| Helical | Indoors, tight spaces | Picks up signals from all directions |
| External puck | Vehicle, marine | Weatherproof, usually active |

**If your module has an external antenna connector (u.FL / SMA) and you're using a patch antenna on the PCB, you're fine. If you're extending it with a cable longer than ~1m, you need an active antenna** — the signal loss in the cable will kill reception otherwise.

### Antenna Placement Rules

- Must have **clear view of the sky**. Through a window works (barely). Inside a metal box = zero reception.
- Keep away from metal surfaces, motors (electrical noise), and high-speed digital lines.
- The antenna ground plane matters — a patch antenna needs a ground plane underneath it (the breakout board provides this).

## PPS (Pulse Per Second) Pin

The PPS pin outputs a precise 1-second pulse, synchronized to GPS time within nanoseconds. Use it for:

- **High-accuracy timekeeping** — discipline an RTC or synchronize multiple devices
- **Timing measurements** — know exactly when an event occurred
- **Frequency reference** — calibrate oscillators

The PPS pin is a 3.3V logic pulse, 100ms wide, once per second. Connect it to an interrupt pin.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| No fix indoors | GPS needs sky view | Move near window, try active antenna |
| Fix takes minutes | Cold start, weak signal | Add battery backup, use external antenna |
| Garbage output | Wrong baud rate | Default is 9600, check your module |
| Intermittent fix | Antenna issue, interference | Check antenna connection, move away from motors |
| High current drain | Module always tracking | Power-cycle between readings (MOSFET on VCC) |
| Position jumps | Multipath (signal bounces off buildings) | Average readings over time |
| No satellites seen | Module in configuration mode | Send factory reset command |

## Quick Reference

- **Default baud:** 9600, 8N1
- **NMEA sentences:** $GPGGA (position), $GPRMC (speed+course), $GPGSV (satellites in view)
- **Fix types:** 0=no fix, 1=GPS fix, 2=DGPS, 3=estimated
- **Minimum satellites for 3D fix:** 4
- **Max update rate:** Most modules 1–10 Hz (higher = more power)
- **Battery backup:** CR1220 coin cell keeps almanac for faster starts
- **External antenna connector:** Usually u.FL or SMA
