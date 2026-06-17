# Reading Schematics — Fundamental Reference

## What It Is

A schematic is a **map of your circuit**. It shows how components connect using standardized symbols. Wires are lines, components are symbols, and junctions are dots.

```
  VCC ────────┬──────── LED ──── R ──── GND
              │
          ┌───┴───┐
          │  IC   │
          │       │
          └───────┘
```

## Common Symbols

### Passive Components

| Symbol | Component | Notes |
|--------|-----------|-------|
| ──┤├── | Capacitor (non-polarized) | Two parallel lines |
| ──┤├── + | Capacitor (polarized) | Curved line = negative |
| ──/\/\/\── | Resistor | Zigzag (US) or rectangle (EU) |
| ──○○── | Inductor | Loops or a filled rectangle |
| ──( )── | Ferrite bead | One lump |

### Semiconductors

| Symbol | Component | Notes |
|--------|-----------|-------|
| ─▶|── | Diode | Arrow = direction of conventional flow |
| ─▶|── ─┤├── | Zener diode | Z-shaped bar |
| ──▶|── ── | Schottky diode | S-shaped bar |
| ───▶── | LED | Arrow = light output |
| ──▶── ←── | Photodiode | Inward arrows = light sensitive |
| ──▶── ──▶── | Diode with square = phototransistor |

### Transistors

```
NPN:         PNP:         N-MOSFET:    P-MOSFET:
  C            E            D             S
  │            │            │             │
  │\           │/           │             │
B ─┤       B ─┼─           G ─┤           G ─┤
  │/           │\           │             │
  │            │            │             │
  E            C            S             D
```

| Symbol | Type |
|--------|------|
| Arrow pointing OUT from base | NPN (Not Pointing iN) |
| Arrow pointing IN to base | PNP |
| Separate body diode | MOSFET (always shows the internal diode) |

### Logic Gates

| Symbol | Function |
|--------|----------|
| ┌──┐ | AND — output HIGH when all inputs HIGH |
| ─┤ &├─ | |
| └──┘ | |
| ┌──┐ | OR — output HIGH when any input HIGH |
| ─┤ ≥1├─ | |
| └──┘ | |
| ┌──┐ | NOT (inverter) — output opposite of input |
| ─┤ 1├─○─ | Circle = inversion |
| └──┘ | |
| Circle on output | Active LOW (e.g., ─○ means "asserted low") |

### ICs / Chips

ICs are drawn as rectangles with labeled pins:

```
┌─────────────────┐
│                 │
│   LM358         │
│                 │
│ 1 ─┤ Output 1   │
│ 2 ─┤ Input -1   │
│ 3 ─┤ Input +1   │
│ 4 ─┤ GND        │
│ 5 ─┤ Input +2   │
│ 6 ─┤ Input -2   │
│ 7 ─┤ Output 2   │
│ 8 ─┤ VCC        │
└─────────────────┘
```

Pin numbers and functions are labeled. In complex schematics, ICs may be drawn with functional groups separated.

## Reading Wires

| Drawing | Meaning |
|---------|---------|
| ────┬──── | Wire crossing, NO connection |
| ────┬──── | |
| ────┼──── (no dot) | Wires just happen to cross |
| ────●──── | Wire junction, CONNECTED |
| ────┤├──── | |
| ────┴──── | Wire connecting at a T-junction (always connected) |

**Everything connected needs a dot** at the junction. Crossed lines without dots are NOT connected.

## Power and Ground Symbols

| Symbol | Meaning |
|--------|---------|
| ── VCC | Positive supply (usually 3.3V or 5V) |
| ── +5V | Labeled supply voltage |
| ── +3.3V | Labeled supply voltage |
| ──▼ | Ground (GND, 0V) — triangle pointing down |
| ──▼| | Chassis ground (for enclosures) |
| ──|◄ | Earth ground (safety earth) |
| ── V+ | Positive supply rail |
| ── V- | Negative supply rail |

**Ground is not optional.** Every circuit must have a return path to ground, even if it's not drawn. In many schematics, ground symbols are used instead of drawing the GND wire all the way back.

## How to Read a Schematic

### Step 1: Find Power and Ground

Identify where power enters and where ground is. Usually at the top (VCC) and bottom (GND) of the page.

### Step 2: Trace Signal Flow

Signals typically flow left to right. Inputs are on the left, outputs on the right.

### Step 3: Break It Into Blocks

A complex schematic is made of simpler building blocks:
- Power supply section
- Input section (sensors, buttons)
- Processing section (microcontroller, op-amp)
- Output section (LEDs, motors, displays)

### Step 4: Read Component Labels

Each component has a reference designator:
- R1, R2, R3 = resistors
- C1, C2, C3 = capacitors
- D1, D2, D3 = diodes
- Q1, Q2, Q3 = transistors
- U1, U2, U3 = ICs
- J1, J2, J3 = connectors

### Step 5: Check Datasheet Pinouts

ICs are abstracted. Always check the datasheet to confirm which pin does what. Pin numbers on the schematic match the physical chip.

## Common Mistakes

| Mistake | What Actually Happens |
|---------|----------------------|
| Missing ground | Circuit doesn't work, no return path |
| Connecting VCC and GND directly | Short circuit → magic smoke |
| Ignoring decoupling caps | IC oscillates or glitches |
| Swapping TX and RX | UART: no data |
| No pull-up resistor on open-drain bus (I2C) | Bus doesn't work |
| Connecting 5V to 3.3V input | ESP32: dead GPIO pin |

## Quick Reference

- **Dots connect, crosses don't.** Wire junction = dot. Crossed lines without dots = not connected.
- **VCC top, GND bottom.** Power rail at the top, ground at the bottom.
- **Left to right.** Inputs on the left, outputs on the right.
- **R** = resistor, **C** = capacitor, **D** = diode, **Q** = transistor, **U** = IC.
- **Every IC needs a decoupling cap** (100nF between VCC and GND, close to the chip).
- **Datasheets are law.** Pin numbers, voltage limits, current limits — always verify.

## See Also

- [relay-module](/projects/relay-module)
- [stepper-motor-a4988](/projects/stepper-motor-a4988)
- [74hc595-shift-register](/projects/74hc595-shift-register)
