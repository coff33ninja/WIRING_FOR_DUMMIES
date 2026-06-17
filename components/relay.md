# Relay — Component Reference

## What It Is

A relay is an **electrically operated switch**. A small current through its coil creates a magnetic field that physically moves a metal contact, switching a much larger current on the other side.

> **Analogy:** Think of a relay as a remote-controlled light switch. You press a tiny button in one room (the coil), and a big switch flips in another room (the contacts). The person pressing the button is completely isolated from the high-voltage circuit they're controlling.

## Electromechanical vs Solid State

| Type | Electromechanical (EMR) | Solid State (SSR) |
|------|------------------------|-------------------|
| Switching mechanism | Physical metal contact moves | Semiconductor (triac / MOSFET) switches |
| Audible click | Yes — you hear it | No — silent |
| Wear out | Yes — contacts degrade after 10k–100k cycles | No moving parts |
| Switching speed | Slow (~5–20ms) | Fast (~1µs) |
| Isolation | Yes — physical gap | Yes — optocoupler |
| Best for | AC/DC, any load | Frequent switching, silent operation |

> **Most hobby projects use EMRs** — they're cheap, simple, and the click is reassuring.

## The 5 Pins of a Standard Relay

```
          ┌──────────────────────────────┐
          │    ═══ COIL ═══              │
          │   ┌──┐    ┌──┐              │
    Coil+─┤   │  │    │  │   ├─ COM      │
          │   │  │    │  │   │           │
    Coil-─┤   └──┘    └──┘   ├─ NC       │
          │                  ├─ NO       │
          └──────────────────────────────┘
```

| Pin | Name | What it does |
|-----|------|-------------|
| **Coil +** | Positive (85) | Drive side — apply voltage to energize |
| **Coil −** | Negative (86) | Drive side — ground to energize |
| **COM** | Common (30) | The moving contact — connects to NC or NO |
| **NC** | Normally Closed (87a) | Connected to COM when relay is OFF |
| **NO** | Normally Open (87) | Connected to COM when relay is ON |

## NO vs NC — When to Use Which

```
Relay OFF (coil not powered):   COM ───── NC  (device connected to NC is ON)
                                COM ╳──── NO  (device connected to NO is OFF)

Relay ON (coil powered):        COM ╳──── NC  (device connected to NC is OFF)
                                COM ───── NO  (device connected to NO is ON)
```

| Use NO when | Use NC when |
|-------------|-------------|
| Turning something ON with a signal | Keeping something ON by default |
| Lamp, motor, pump (normally off) | Alarm, emergency stop (failsafe) |
| "Press to start" | "Cut to stop" |

> **Failsafe rule:** Use NC for safety-critical circuits. If the relay loses power, the NC path closes and keeps things safe (e.g., emergency brake defaults to ON).

## Coil Ratings — What Voltage to Use

| Coil rating | Typical trigger voltage | Use with |
|-------------|------------------------|----------|
| 3.3V | 2.5–3.5V | Some ESP32-compatible relays |
| 5V | 3.75–5.5V | Arduino, most relay modules |
| 12V | 9–14V | Automotive, industrial |

> **A 5V relay needs ~5V to click.** An ESP32 GPIO at 3.3V cannot drive a 5V relay coil directly. Use a transistor driver or a relay module with built-in driver.

## Driving a Relay from a Microcontroller

### Option 1: Relay Module (Recommended for beginners)

Pre-built PCB with transistor, flyback diode, and optocoupler:

```
ESP32          Relay Module
─────          ────────────
GPIO ─────────── IN
5V  ─────────── VCC
GND ─────────── GND
```

The module handles the transistor drive, flyback protection, and isolation. You just need to send a HIGH or LOW signal.

### Option 2: Transistor Driver (Bare Relay)

For driving a bare 5V relay directly:

```
ESP32              NPN (2N2222)          5V Relay
─────              ────────────          ────────
GPIO ──[1kΩ]────── Base
                   Collector ──────────── Coil −
                   Emitter ─── GND
                                        Coil + ──── 5V
                                        COM ─────── Load +
                                        NO ──────── Load ─── GND
```

**Critical:** Add a **1N4007 flyback diode** across the relay coil (stripe toward 5V) to absorb the voltage spike when the coil turns off.

## Contact Ratings

Every relay specifies its max voltage and current for the contacts:

| Marking | Meaning | Example |
|---------|---------|---------|
| 10A 250VAC | Can switch 10A at 250V AC | Household mains |
| 10A 30VDC | Can switch 10A at 30V DC | Automotive |
| 5A 250VAC | Smaller relay | Lighter loads |

> **Don't exceed both simultaneously.** If you switch high voltage, reduce the current rating. Read the datasheet.

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Flyback diode across coil | Transistor/MOSFET dies from voltage spike |
| Base resistor on transistor | GPIO pin tries to sink unlimited current → dies |
| Using NO when you need NC | Load stays off when relay is triggered — backwards behavior |
| Overloading contacts (too much current) | Contacts weld shut — relay stays ON permanently |
| No snubber across AC contacts | Arcing shortens relay life, causes interference |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| 5V relay module (optocoupler) | 1 | Easiest — just signal, VCC, GND |
| SRD-05VDC-SL-C (Songle) | 1 | Standard 5V relay, 10A contacts |
| 1N4007 flyback diode | 1 | For bare relay coils |
| 2N2222 NPN transistor | 1 | For driving bare relay |
| 1kΩ resistor | 1 | Base resistor for transistor |

> **If the relay clicks but the load doesn't turn on:** Check the COM/NO/NC wiring. COM connected? Load connected between NO/NC and GND?
