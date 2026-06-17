# 74HC595 Shift Register — Wiring for Dummies

## What Is a Shift Register?

A shift register is a chip that **turns serial data (one bit at a time) into parallel data (multiple bits at once)**. Think of it as expanding 3 microcontroller pins into **8 output pins** — and you can chain multiple chips for 16, 24, 32+ outputs.

> **Why you need it:** Your ESP32 has a limited number of GPIO pins. What if you need to control 16 LEDs, 8 relays, or a 7-segment display? You can't dedicate 16 pins to LEDs. The 74HC595 solves this — 3 pins control 8 outputs, and chaining more chips adds 8 more outputs each, still using only 3 pins.

> **Analogy:** Imagine a line of 8 people (the outputs). A conveyor belt brings colored balls one at a time. Each person grabs a ball when it passes, and holds it. When you shout "lock it in!" (latch), everyone holds up their ball simultaneously. The conveyor belt position is the serial data, the people are the 8 outputs, and the "lock it in" command is the latch.

## The 16 Pins

```
                74HC595 (top view)
          ┌─────────────────────────┐
    (1) Q1  ────────────────── VCC (16)
    (2) Q2  ────────────────── Q0 (15)
    (3) Q3  ────────────────── DS (14)  ← Serial data in
    (4) Q4  ────────────────── OE (13)  ← Output enable (LOW = enabled)
    (5) Q5  ────────────────── STCP (12) ← Latch (storage register clock)
    (6) Q6  ────────────────── SHCP (11) ← Shift clock
    (7) Q7  ────────────────── MR (10)  ← Master reset (HIGH = normal)
    (8) GND ────────────────── Q7S (9)  ← Serial data out (to next chip)
          └─────────────────────────┘
```

### The 3 Control Pins (from Microcontroller)

| Pin | Name | Think of it as... |
|-----|------|-------------------|
| **DS (14)** | Data / Serial Input | The **conveyor belt** — each bit goes in one at a time |
| **SHCP (11)** | Shift Clock | The **"next item" button** — each pulse moves the conveyor belt one position |
| **STCP (12)** | Latch / Storage Clock | The **"lock it in" button** — copies all positions to the outputs at once |

### Power Pins

| Pin | Connection |
|-----|-----------|
| **VCC (16)** | 3.3V or 5V (matches your microcontroller) |
| **GND (8)** | Ground |

### Control Pins

| Pin | Connection |
|-----|-----------|
| **MR (10)** | Master Reset — pull HIGH to 3.3V for normal operation. Pull LOW to clear all outputs |
| **OE (13)** | Output Enable — pull LOW to GND for normal operation. Pull HIGH to disable all outputs (tristate) |

### Data Pins

| Pin | Connection |
|-----|-----------|
| **Q0–Q7 (15, 1–7)** | The **8 output pins** — these drive LEDs, transistors, relay modules, etc. |
| **Q7S (9)** | Serial data out — connects to DS of the NEXT 74HC595 for chaining |

## How the Signaling Works

```
Data (DS):  ── 1 ── 0 ── 1 ── 0 ── 1 ── 1 ── 0 ── 1 ──
                                   ↑ Data goes in MSB first

Shift Clock (SHCP):
   ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐
   ││ ││ ││ ││ ││ ││ ││ ││
   └┘ └┘ └┘ └┘ └┘ └┘ └┘ └┘
   ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑
   Bit 0 moves in on each rising edge

Latch (STCP):
                     ┌─────
                     │
   ──────────────────┘
                     ↑ After 8 bits, pulse latch to update outputs
```

### Step by Step

1. **Set DS** (data pin) to the value of the bit you want to send (HIGH or LOW)
2. **Pulse SHCP** HIGH then LOW — this shifts the bit into the internal shift register
3. **Repeat** for all 8 bits (send MSB first or LSB first, depending on your code)
4. **Pulse STCP** HIGH then LOW — this copies the internal register to the output pins

> **Why two clocks?** The shift register can keep receiving new data while the outputs hold their current state. When you have all the new data ready, one latch pulse updates everything at once. This prevents the outputs from "scrolling" as data shifts in.

## Basic Wiring Diagram

```
ESP32                 74HC595
─────                 ───────
GPIO 18 ─────────────── DS (14)   — Serial data
GPIO 19 ─────────────── SHCP (11) — Shift clock
GPIO 23 ─────────────── STCP (12) — Latch
3.3V  ───────────────── VCC (16)
GND   ───────────────── GND (8)
3.3V  ───────────────── MR (10)   — Pull HIGH (normal operation)
GND   ───────────────── OE (13)   — Pull LOW (outputs enabled)

Outputs:
Q0 (15) ──[220Ω]── LED 1
Q1 (1)  ──[220Ω]── LED 2
Q2 (2)  ──[220Ω]── LED 3
Q3 (3)  ──[220Ω]── LED 4
Q4 (4)  ──[220Ω]── LED 5
Q5 (5)  ──[220Ω]── LED 6
Q6 (6)  ──[220Ω]── LED 7
Q7 (7)  ──[220Ω]── LED 8
```

## Chaining Multiple Chips

To control 16 outputs with only 3 ESP32 pins:

```
ESP32                       74HC595 #1                74HC595 #2
─────                       ─────────                ─────────
GPIO 18 ───────────────────── DS (14) ─────────────── DS (14)
GPIO 19 ─────┬─────────────── SHCP (11) ─┬─────────── SHCP (11)
             │                           │
GPIO 23 ─────┴─────────────── STCP (12) ──┴─────────── STCP (12)
3.3V                         VCC (16)                 VCC (16)
GND                          GND (8)                  GND (8)
3.3V                         MR (10)                  MR (10)
GND                          OE (13)                  OE (13)

                    CHAIN: Q7S (9) ───────────── DS (14) of #2
```

To send 16 bits:
1. Send bit 15 (highest bit of chip #2's output)
2. Send bit 14... down to bit 8
3. Send bit 7... down to bit 0 (chip #1's outputs)
4. Pulse latch

You send 16 bits total (2 bytes). The first 8 bits go into chip #2, the last 8 bits go into chip #1. Each additional chip adds 8 more bits.

### Data Order for Chaining

```
Chip #2 (high byte)     Chip #1 (low byte)
┌──────────────────┐   ┌──────────────────┐
│ Q0 Q1 ... Q6 Q7  │   │ Q0 Q1 ... Q6 Q7  │
│ Bit  Bit    Bit  │   │ Bit  Bit    Bit  │
│ 15   14     8    │   │  7    6      0   │
└──────────────────┘   └──────────────────┘

Data sent to DS: Bit 15 → Bit 14 → ... → Bit 0
                 ↑ First bit sent        ↑ Last bit sent
```

## Current Limits — Watch How Much You Draw

Each 74HC595 output pin can source (provide) about **6mA** at 3.3V, or sink about **20mA**. The total chip current limit is about **70mA**.

| Use case | Works? | Notes |
|----------|--------|-------|
| Driving LEDs (2mA each) | ✓ Yes | Perfect — 220Ω resistor for ~5mA per LED |
| Driving transistor/MOSFET base | ✓ Yes | Use 1kΩ base resistor |
| Driving relay module directly | ✓ Yes | Relay modules have their own drivers |
| Driving a motor directly | ✗ No | Use a MOSFET or relay — never direct from 595 |

> **If your 595 gets hot:** You're drawing too much current. Use transistors or MOSFETs as buffers for high-current loads.

## Common Uses

| Use | Wiring | Notes |
|-----|--------|-------|
| 8 LEDs | Qn → 220Ω → LED → GND | Classic blinky |
| 7-segment display | Q0–Q7 → 220Ω × 8 → display segments | Two chips for 2 digits |
| Relay control | Qn → IN of relay module | Relay module has its own driver |
| Button matrix rows | Qn → row of matrix | Scanning inputs (different wiring) |

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| MR (10) pulled HIGH | Chip is in reset — no outputs work |
| OE (13) pulled LOW | Outputs are disabled — nothing happens |
| Latch pulse (STCP) after data | Data shifts in but never appears on outputs |
| Current-limiting resistor on outputs | LEDs burn out; chip may overheat |
| VCC decoupling cap (100nF) | Noise on power, glitchy shifting, random output states |
| Shared ground | No communication — chip doesn't work |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| 74HC595 DIP-16 | 1+ | Add more if chaining |
| 220Ω resistors | 8 | For LED current limiting |
| LEDs (any color) | 8 | For testing |
| 100nF ceramic cap | 1 | Decoupling at VCC/GND |
| Jumper wires | 1 set | M-M, M-F |
| Breadboard | 1 | For prototyping |
| Optional: 7-segment display | 1 | Common cathode, for display projects |

## See Also

- [serial-communication](/fundamentals/serial-communication)
- [breadboard](/fundamentals/breadboard)
- [soldering](/fundamentals/soldering)
- [reading-schematics](/fundamentals/reading-schematics)
- [resistor-network](/fundamentals/resistor-network)
