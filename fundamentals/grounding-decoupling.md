# Grounding & Decoupling — Fundamental Reference

## What It Is

**Ground (GND)** is the common reference point for all voltages in your circuit. It's the 0V baseline — everything else is measured relative to it.

**Decoupling** (also called bypassing) uses capacitors near ICs to smooth out voltage dips and filter noise. Every digital chip needs them.

## Ground — Why It Matters

### Star Ground vs Daisy Chain

```
Star Ground (GOOD):           Daisy Chain (BAD):
                              ┌───┐   ┌───┐   ┌───┐
    ┌───┐                     │   │   │   │   │   │
    │   │                     └─┬─┘   └─┬─┘   └─┬─┘
    └─┬─┘                       │       │       │
      │                         └───────┴───────┴── GND
      │
┌─────┴─────┐  ← Common point
│     │     │
│  ┌──┴──┐  │
│  │     │  │
└──┴─┐ ┌─┴──┘
   ┌─┘ └─┐
   │     │
  ┌┴┐   ┌┴┐
```

All ground wires meet at **one point** — the star. This prevents ground currents from one circuit from affecting another.

### Ground Loops

A ground loop happens when there are two or more paths to ground. Current flows through the loop, creating voltage differences and noise:

```
Sensor ──────── Signal ──── Microcontroller
    │                              │
    └────────── GND ───────────────┘
        ↑ This creates a loop
```

**Fix:** Connect all grounds at a single point (star ground). For audio circuits, this is critical — ground loops cause hum.

### Ground in Practice

- Every component needs a ground connection (even if not shown on the schematic)
- Use thick wires for ground (lower resistance)
- Keep power and ground wires close together (less inductance, less noise)
- For high-current circuits, use a ground plane or thick bus wire

## Decoupling — Why It Matters

### What Happens Without Decoupling

When a digital chip switches, it draws a sudden spike of current. If the power supply can't deliver instantly, the voltage dips:

```
VCC ──┬─────────┬── IC
      │         │
      │         └── Current spike when clock edge hits
      │
  Long wires ──→ inductance prevents instant current delivery
  ──→ VCC voltage drops
  ──→ IC misbehaves or resets
```

### The Fix: Decoupling Capacitor

A small capacitor (typically 100nF) placed right next to the IC's VCC pin acts as a **local energy reservoir**:

```
VCC ─────┬─────── IC VCC
         │
        ─┼─ 100nF
        ─┼─
         │
GND ─────┴─────── IC GND
```

When the IC needs a sudden burst of current, the cap provides it instantly (faster than the power supply can).

### Decoupling Capacitor Guidelines

| IC type | Capacitor value | Placement |
|---------|----------------|-----------|
| Digital logic (general) | 100nF ceramic | Within 5mm of each VCC pin |
| Microcontroller | 100nF + 10µF electrolytic | 100nF per VCC pin, 10µF near board power input |
| Op-amp / analog | 100nF per supply pin | Close to the chip |
| Motor driver | 100nF + 100µF | High-frequency + bulk capacitance |
| RF module | 100nF + 10pF | Multiple values for wideband decoupling |

**Two caps are better than one:** Small ceramic (100nF) handles fast transients. Larger electrolytic (10–100µF) handles slower dips. Use both.

### Why 100nF?

100nF (0.1µF) is the standard because:
- Small enough to have low self-inductance (responds fast)
- Large enough to supply a useful charge
- Cheap, tiny, and available everywhere

## Ground Planes

A **ground plane** is a large area of copper connected to ground — usually an entire layer of a PCB. Benefits:

- Very low resistance (all grounds are essentially the same point)
- Excellent noise shielding
- Lower inductance (better for high-frequency circuits)

**On a breadboard,** the ground rail serves as your ground plane. Use it liberally: connect one GND rail to the other, and run a thick wire for the main ground bus.

## Mixed Signal Grounding (Analog + Digital)

Analog signals (sensors, audio) are sensitive to noise. Digital signals (microcontroller, SPI) are noisy. Don't let digital noise corrupt analog signals.

```
    ┌───────────────┐     ┌───────────────┐
    │  Analog       │     │  Digital      │
    │  Circuit      │     │  Circuit      │
    └──────┬────────┘     └───────┬───────┘
           │                     │
           └─────────┬───────────┘
                     │
                   Star ground point
```

Separate analog and digital ground traces, joining them at **one point** near the power supply. Some ADC chips have separate AGND and DGND pins — connect both to the star ground point.

## Filtering Power Supply Noise

### RC Filter for Analog Circuits

```
VCC ──── R (10–100Ω) ────┬──── Analog circuit VCC
                          │
                        ─┼─ C (10–100µF)
                        ─┼─
                          │
                         GND
```

The resistor + capacitor form a low-pass filter that removes power supply noise. Useful for analog sensors, audio, and op-amp circuits.

### Ferrite Bead

A ferrite bead on the power line adds high-frequency resistance without DC voltage drop:

```
VCC ──── ════ ──── VCC_clean
         FB
```

Common on microcontroller boards near the USB power input. Blocks high-frequency noise from the USB cable.

## Quick Reference

- **All grounds must connect.** Floating ground = circuit doesn't work
- **Star ground** = all ground wires meet at one point
- **Avoid ground loops** — single path to ground for each circuit section
- **Every IC needs a 100nF decoupling cap** within 5mm of each VCC pin
- **Use two caps:** 100nF ceramic + 10–100µF electrolytic per board
- **Separate analog and digital ground** for mixed-signal circuits
- **Thick ground wires** = lower resistance = less noise
- **A ground plane is best** (PCB only — breadboards use thick bus wires)

## See Also

- [stepper-motor-a4988](/projects/stepper-motor-a4988)
- [relay-module](/projects/relay-module)
