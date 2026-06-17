# Breadboard & Wiring — Fundamentals

## What It Is

A breadboard is a **reusable prototyping board** — a plastic block with holes connected by metal clips underneath. You push component leads and jumper wires into the holes to build circuits without soldering.

```
Top view:

    ┌──────────────────────────────────────┐
    │  [+][+]                              │  ← Power rail (red/blue stripe)
    │  [-] [-]                             │  ← Ground rail (black/blue stripe)
    ├──────────────────────────────────────┤
    │  (a)(b)(c)(d)(e) • (f)(g)(h)(i)(j)  │
    │  (a)(b)(c)(d)(e) • (f)(g)(h)(i)(j)  │  ← Terminal strips
    │  (a)(b)(c)(d)(e) • (f)(g)(h)(i)(j)  │    (rows connected horizontally)
    │  (a)(b)(c)(d)(e) • (f)(g)(h)(i)(j)  │
    │  (a)(b)(c)(d)(e) • (f)(g)(h)(i)(j)  │
    ├──────────────────────────────────────┤
    │  [-]  [-]                            │  ← Ground rail
    │  [+]  [+]                            │  ← Power rail
    └──────────────────────────────────────┘
```

## How the Holes Are Connected

### Terminal Strips (the main area)

Each row of 5 holes (a–e or f–j) is **electrically connected** under the plastic. The center gap (the "notch" or "DIP channel") separates the left and right sides — they are **not connected**.

```
Row 1:   (a)─(b)─(c)─(d)─(e)    •    (f)─(g)─(h)─(i)─(j)
Row 2:   (a)─(b)─(c)─(d)─(e)    •    (f)─(g)─(h)─(i)─(j)

(a) through (e) are connected.
(f) through (j) are connected.
Row 1 is NOT connected to Row 2.
```

**Rule:** Every component leg in the same row-letter-group is connected. If you push a resistor leg into 1a and an LED leg into 1e, they're connected.

### Power Rails (the red/blue columns)

The two long columns on each side (usually marked with red + and blue −) run the **full length** of the board. They are connected vertically.

```
Left power rail:      [+]─[+]─[+]─[+]─[+]─[+]─[+]─[+]  (all connected)
Left ground rail:     [−]─[−]─[−]─[−]─[−]─[−]─[−]─[−]  (all connected)
```

**Important:** Many breadboards have a **gap in the middle** of the power rails. If your board has this, you must jumper across it to carry power to the top half.

## Jumper Wires — Which Type for What

| Type | Looks like | Best for |
|------|-----------|----------|
| **Solid-core 22 AWG** | Single stiff wire, no stranded visible | **Breadboarding** — stiff enough to push in, holds shape |
| **Dupont jumper** (M/M, M/F, F/F) | Pre-crimped with plastic housing | Connecting modules, sensors, Arduino/ESP32 pin headers |
| **Stranded wire** | Multiple thin strands | Permanent soldered connections — **bad for breadboards** (strands fray and don't fit) |
| **Ribbon cable** | Multiple parallel wires | Data buses (I2C, SPI), keeping wiring tidy |

> **Gold rule for breadboards:** Use **22 AWG solid-core hookup wire** cut to length. Pre-made Dupont jumpers are fine for modules. Stranded wire is a nightmare — the strands splay and won't push into the hole.

## Common Mistakes

| Mistake | What happens | Fix |
|---------|-------------|-----|
| Component legs in different rows | Circuit doesn't work — open connection | Check both legs are in the same row group |
| Stranded wire in breadboard | Strands fray, short to adjacent holes | Use solid-core 22 AWG or pre-crimped Dupont |
| IC inserted across the gap wrong way | Pins on wrong side of DIP channel, or rotated 180° | Notch on IC must point left; straddle the center gap |
| Power rails not jumpered across break | Top half of board has no power | Add a short jumper wire across the rail break |
| Loose component leg | Intermittent connection — works when pressed | Push leg all the way in; if still loose, use a shorter leg |
| Wire insulation pushed into hole | Wire doesn't make contact | Strip 6mm (1/4") of insulation; push only bare wire into hole |
| Overcrowding | Wires block each other, hard to debug | Use longer jumpers routed over components, or use a bigger board |
| Applying >30V on a breadboard | Arc between clips — breadboard may melt | Breadboards are rated ~30V max. Use terminal strips for mains/high voltage |

## Breadboard Sizes

| Type | Rows | Typical use |
|------|------|-------------|
| **Mini** (170 tie-points) | 17 rows × 2 sides | Tiny circuits, single sensor testing |
| **Half-size** (400 tie-points) | 30 rows × 2 sides | Most hobby projects — fits an ESP32 + a few modules |
| **Full-size** (830 tie-points) | 63 rows × 2 sides | Big projects with many components |
| **With binding posts** | Full-size + power terminals | Integrating external power supplies with banana plugs |

## Wiring a Chip (DIP IC)

Integrated circuits in DIP (Dual Inline Package) **straddle the center gap**:

```
Correct:              Wrong:
┌────────────────┐    ┌────────────────┐
│  ┌──────────┐  │    │  ┌──────────┐  │
│  │  NOTCH   │  │    │  │  NOTCH   │  │
│  └──────────┘  │    │  └──────────┘  │
│ 1 2 3 4 5 6 7  │    │ 1 2 3 4 5 6 7  │
│ • • • • • • •  │    │ • • • • • • •  │
│                •│    │              • │
│ • • • • • • •  │    │ • • • • • • •  │
│ 8 9 ......

The chip straddles the center gap.
Pin 1 is top-left (notch end).
One side in (a-e), other side in (f-j).
```

**Pin numbering:** With the notch at the left, pin 1 is the bottom-left pin. Pins count down the left side, then up the right side.

## Wiring a Module (like an ultrasonic or relay module)

Most modules have male pin headers (2.54mm pitch). Use **female-to-female Dupont jumpers** to connect from the module to the breadboard, or female-to-male to go from module to ESP32.

## Quick Reference

```
Breadboard connections:
  Rows (a-e) CONNECTED horizontally
  Rows (f-j) CONNECTED horizontally
  Left and right sides NOT connected (gap)
  Power rails (+) CONNECTED vertically
  Ground rails (-) CONNECTED vertically
  Watch for power rail breaks (jumper across)

Best wire: 22 AWG solid-core (stripped 6mm)
  Stranded = bad (frays)
  Dupont jumpers = good for modules

Common part placement:
  DIP chips straddle the center gap (notch left, pin 1 bottom-left)
  Resistors and LEDs span the gap too (anode to left side, current limit resistor to right)
  Modules connect via F/F or F/M Dupont jumpers

Danger:
  Max ~30V on breadboard
  No mains/high voltage on breadboard
```

## See Also

- [74hc595-shift-register](/projects/74hc595-shift-register)
- [esp32-fan-controller](/projects/esp32-fan-controller)
- [pir-motion-sensor](/projects/pir-motion-sensor)
