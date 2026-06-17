# Shift Register (74HC595) — Component Reference

## What It Is

A shift register takes serial data (one bit at a time) and turns it into parallel output (8 bits at once). The 74HC595 is the most common — it's a **serial-in, parallel-out** (SIPO) register with 8 output pins. It turns 3 microcontroller pins into 8, and you can chain multiple chips to get unlimited outputs.

> **Analogy:** A conveyor belt of buckets. You drop balls (bits) into the first bucket, then push the belt. Each push moves every ball one bucket down. After 8 pushes, all 8 buckets are filled and you dump them simultaneously onto 8 parallel tracks.

## How It Works — The Three Control Lines

The 74HC595 is controlled by three digital signals:

| Pin | Name | Function |
|---|---|---|
| 14 | DS (Data) | Serial data input. One bit per clock pulse. |
| 11 | SH_CP (Shift Clock) | On rising edge, shifts data in by one bit. |
| 12 | ST_CP (Latch Clock / Store Clock) | On rising edge, copies shift register contents to output latches. |

**Data flow:**

```
Microcontroller → DS (data pin)
                → SH_CP (shift clock pin)
                → ST_CP (latch pin)

Inside 74HC595:
  DS ──→ [Shift Register (8-bit)] ──→ [Storage Register (8-bit)] ──→ Q0–Q7 pins
           ↑                            ↑
        SH_CP                        ST_CP
```

**Sequence:**

1. Set DS to bit 7 (MSB first) or bit 0 (LSB first)
2. Pulse SH_CP high → that bit shifts in
3. Repeat for all 8 bits
4. Pulse ST_CP high → all 8 outputs update simultaneously

```



   DS      █     █     █     █     █     █     █     █
           │     │     │     │     │     │     │     │
   SH_CP  ─┘  ┌──┘  ┌──┘  ┌──┘  ┌──┘  ┌──┘  ┌──┘  ┌──
              │     │     │     │     │     │     │
   ST_CP     ────────────────────────────────────────┐
                                                    │
                                                ────┘
                                             (outputs update)
```

**Why separate shift and storage registers?** Without the storage register, outputs would glitch as each bit shifts in. The storage latch lets you shift in 8 bits silently, then update all outputs in one clean step.

## Pinout

```
            ┌──────────┐
   Q0  ────┤1        16├──── VCC (2–6V)
   Q1  ────┤2        15├──── Q7 (serial output, for chaining)
   Q2  ────┤3        14├──── DS (data in)
   Q3  ────┤4        13├──── OE (output enable, active LOW)
   Q4  ────┤5        12├──── ST_CP (latch/store clock)
   Q5  ────┤6        11├──── SH_CP (shift clock)
   Q6  ────┤7        10├──── MR (master reset, active LOW)
   GND ────┤8         9├──── Q7̅ (inverted serial output)
            └──────────┘
```

| Pin | Description |
|---|---|
| Q0–Q7 | Parallel outputs (8 bits) |
| Q7 / Q7̅ | Serial output (feed to next chip's DS or inverted) |
| DS | Serial data input |
| SH_CP | Shift clock — data shifts on rising edge |
| ST_CP | Storage/latch clock — outputs update on rising edge |
| OE | Output enable — LOW = outputs active, HIGH = outputs high-impedance |
| MR | Master reset — LOW resets all shift register bits to 0 |
| VCC | 2–6V (5V typical) |
| GND | Ground |

## Chaining Multiple Shift Registers

Connect Q7 (pin 9) of the first chip to DS (pin 14) of the next. Both chips share the same SH_CP and ST_CP lines.

```
    74HC595 #1                74HC595 #2
  DS    SH_CP  ST_CP        DS     SH_CP  ST_CP
  │      │      │           │       │      │
  └──┬───┴──────┘           └──┬────┴──────┘
     │   ┌─────────────────────┘
     │   │
     └───┘ common clock/latch from MCU

  #1 Q7 ─────────────────────── #2 DS
```

**To output 16 bits:**

1. Shift out the high byte (MSB) first
2. Shift out the low byte second
3. Pulse ST_CP — all 16 outputs update at once

```



   DS      [bit 15] [bit 14] ...[bit 8] [bit 7] ...[bit 0]
                                    │                │
                                goes to #2       stays in #1
```

**Maximum number in a chain:** Practically unlimited. The SH_CP and ST_CP lines fan out and the total capacitance limits speed. For hobby speeds (1–10 MHz), 8+ chips in a chain works fine.

## Output Enable (OE) and Master Reset (MR)

**OE (pin 13) — active LOW:**

| OE | Output pins Q0–Q7 |
|---|---|
| LOW | Driven to match storage register |
| HIGH | High-impedance (3-state, disconnected) |

**Use case:** Turn off all outputs simultaneously without clearing the data. Pull OE low permanently for normal operation. Connect to a PWM pin for global dimming of LEDs (pulse the OE line).

**MR (pin 10) — active LOW:**

| MR | Effect |
|---|---|
| LOW | Clears shift register (all 0s). Storage register and outputs unchanged until next ST_CP pulse. |
| HIGH | Normal operation |

**Use case:** Pull MR high (VCC) permanently for normal operation. Drive low to reset without power cycling. Leave floating? Never — floating MR picks up noise and causes random resets. Always tie to VCC through a 10kΩ pull-up if not driven.

## Current Per Output Pin

Each 74HC595 output can source or sink:

| Parameter | Value |
|---|---|
| Max per output pin | ±20mA |
| Max total across all pins | ±70mA |
| Max through VCC or GND | ±70mA |

**Practical limits:**

| Load per pin | Total pins driven at once | OK? |
|---|---|---|
| 20mA | 3 | Yes |
| 10mA | 7 | Yes |
| 5mA | 14 (two chips) | Yes |
| 20mA on all 8 pins | 160mA total | **No** — exceeds 70mA VCC limit |

> **Rule:** If driving 8 LEDs at 20mA each, add up: 8 × 20mA = 160mA. The chip's VCC pin cannot supply that. Either limit each output to 8mA, or use transistor arrays (ULN2803) after the shift register.

**Add a decoupling capacitor (0.1µF) between VCC and GND** close to the chip. Without it, output glitches and latch errors appear when multiple pins switch.

## 3-State Outputs

When OE is high, the 8 output pins enter high-impedance (Hi-Z) state — they act as if disconnected. This lets multiple outputs share the same bus line without fighting each other.

**Common use:** Driving a common-anode 7-segment display. One 74HC595 controls segment pins (Q0–Q7), another controls the digit common pins. When you update the segments, hold digit OE high so no digit is lit during the shift. Release OE when the storage register is stable.

## Common Uses

### 7-Segment LED Displays

Two 74HC595s per 4-digit display:

- One chip: Q0–Q7 → segment pins a–g + dp
- Second chip: Q0–Q3 → digit select (DIG1–DIG4)

Multiplexing handled in software — refresh each digit every 2ms.

### LED Arrays (8×8 Matrix)

One 74HC595 for rows, another for columns. PWM the OE pin for brightness control.

```
  74HC595 #1: row outputs (anodes or cathodes)
  74HC595 #2: column outputs (opposite polarity)

  Scan row by row:
    1. Set column pattern for row 1
    2. Enable row 1
    3. Delay
    4. Disable row 1
    5. Repeat
```

### Relay Banks

One 74HC595 drives 8 relays. Since a relay coil draws 30–100mA and the 74HC595 can only supply 20mA, use a ULN2803 (8-channel Darlington driver) between the 74HC595 and the relays.

```
  MCU → 74HC595 → ULN2803 → 8 relays
                (current booster)
```

### Button Matrix Input (74HC165 — the input cousin)

The 74HC595 is output-only. For input shifting (reading many buttons), use the **74HC165** (parallel-in, serial-out). Same idea, opposite direction.

## Common Mistakes

| Mistake | Result |
|---|---|
| OE or MR floating | Random resets, outputs stuck off |
| 20mA on all 8 outputs | Chip overheats, VCC pin exceeds 70mA |
| No decoupling capacitor | Glitches on outputs during shifts |
| Q7 not connected when chaining | Second chip gets no data — all outputs 0 |
| Wrong clock polarity | Data never shifts in — timing mismatch |
| Latch before finishing shift | Outputs update mid-stream — visible flicker |
| Driving inductive load directly | Back-EMF kills the output pin |

## Quick Reference

```
Pins:
  DS (14)    → data in
  SH_CP (11) → shift clock
  ST_CP (12) → latch clock
  OE (13)    → output enable (LOW = on)
  MR (10)    → master reset (HIGH = normal)
  Q0–Q7      → parallel outputs
  Q7         → serial out for chaining

Wiring:
  OE → GND (always active)
  MR → VCC via 10kΩ (never floating)

Current limits:
  20mA per pin max
  70mA total VCC/GND max
  8 LEDs at ~8mA each = safe

Chaining:
  #1 Q7 → #2 DS
  Same SH_CP, same ST_CP
  Shift MSB first (or LSB — pick one, stay consistent)

Library: ShiftOut (Arduino), shiftOut() built-in
```
