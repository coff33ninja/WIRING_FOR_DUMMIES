# Potentiometer — Component Reference

## What It Is

A potentiometer (or "pot") is a **variable resistor** — a three-legged component whose resistance changes when you turn a knob or slide a lever. Think of it as a voltage divider you can adjust with your fingers.

> **Analogy:** Imagine a water pipe with a valve you can turn. Fully open = minimum resistance (all water flows). Fully closed = maximum resistance (nothing flows). A potentiometer does the same for electricity, but it also gives you a **tap** in the middle so you can steal some of the flow.

## The 3 Pins

```
        ┌──────┐
   (1)──┤      ├──(2)  ← Outer pins = fixed resistance across the element
        │  POT │
   (3)──┤      │      ← Wiper = movable tap
        └──────┘
```

| Pin | Name | Think of it as... |
|-----|------|-------------------|
| **1** | Terminal 1 | One end of the resistive track |
| **2** | Terminal 2 | The other end of the resistive track |
| **3** | Wiper | The **movable tap** — slides along the track as you turn the knob |

## How It Works Internally

```
   Terminal 1 ───────╔═══════════╗────── Terminal 2
                      ║ resistor  ║
                      ║  track    ║
                      ╚═══════════╝
                           │
                       ┌───┴───┐
                       │  Wiper│──→ Output voltage
                       └───────┘
                     (moves as knob turns)
```

When you turn the knob, the wiper moves along a resistive element. The resistance between the wiper and each end terminal changes:

- **Fully clockwise:** Wiper near terminal 2. R(1→wiper) = max, R(wiper→2) = ~0Ω
- **Center:** Wiper in the middle. R(1→wiper) = R(wiper→2) = half the total resistance
- **Fully counter-clockwise:** Wiper near terminal 1. R(1→wiper) = ~0Ω, R(wiper→2) = max

## Potentiometer as a Voltage Divider

This is the most common use. Wire the outer pins across a voltage (e.g., 3.3V and GND), and the wiper gives you any voltage in between:

```
     3.3V
       │
      ┌┴┐
      │ │ ← Fixed resistor element
      │ │
      └┬┘
       ├──── Vout (0V to 3.3V — you choose with the knob)
      ┌┴┐
      │ │
      │ │
      └┴┘
       │
      GND
```

**Formula:** Vout = Vin × (Rwiper-to-GND) / (Rtotal)

**Why this matters:** You can read the wiper voltage with an ADC (analog-to-digital converter) pin on your ESP32 to get a value from 0 to 4095 (12-bit). This is how knobs, sliders, joysticks, and volume controls work.

## Potentiometer as a Variable Resistor (2-wire mode)

If you only connect the wiper + one outer terminal, it works as a simple variable resistor:

```
     3.3V ──┬── Pot (wiper + one end) ──┬── load
            │                            │
           GND
```

**Use case:** Adjusting brightness of an LED, setting a reference voltage, tuning a circuit.

> **Downside:** The resistance vs. rotation curve depends on the pot's "taper" (see below). Use this mode with care.

## Taper (Log vs Linear)

Not all pots are the same. The "taper" describes how resistance changes with knob position:

| Taper | Symbol | Resistance change | Used for |
|-------|--------|-------------------|----------|
| **Linear (B)** | B10K | Even — each degree of turn changes resistance by the same amount | Voltage dividers, sensor inputs, calibration knobs |
| **Logarithmic (A)** | A10K | Fast at one end, slow at the other (follows human hearing) | **Audio volume controls** — our ears hear logarithmically |

> **How to tell:** Look at the letter. "B10K" = 10kΩ linear. "A10K" = 10kΩ logarithmic. If there's no letter, it's probably linear.

## Common Values

| Value | Label | Use case |
|-------|-------|----------|
| 1kΩ | B1K | Current limiting, fine voltage adjustment |
| 10kΩ | B10K | **The standard** — voltage dividers, ADC input, most projects |
| 50kΩ | B50K | High-impedance circuits |
| 100kΩ | B100K | Very high-impedance, audio tone controls |
| 1MΩ | B1M | Specialized: electret microphones, high-Z sensors |

**For ESP32/Arduino projects, start with a 10kΩ linear pot (B10K).** It gives a clean voltage range without drawing too much current.

## Wiring to an ESP32 (ADC Read)

```
ESP32                Potentiometer (B10K)
─────                ─────────────────
3.3V ───────────────── Terminal 1
                      │
GPIO 34 (ADC) ───────── Wiper
                      │
GND  ───────────────── Terminal 2
```

**Code:**
```cpp
const int potPin = 34;
int raw = analogRead(potPin);       // 0–4095 (12-bit)
float voltage = raw * (3.3 / 4095); // 0V – 3.3V
```

> **Note:** ESP32 ADC is not perfectly linear, especially near 0V and 3.3V. For precise measurements, use the middle 10%–90% range or calibrate against a known reference.

## Physical Form Factors

| Type | Looks like | Used for |
|------|-----------|----------|
| **Rotary (knob)** | Round with 3 legs and a shaft | Knobs on a panel, volume controls |
| **Slider (fader)** | Rectangular with a sliding tab | Audio mixers, equalizers |
| **Trimmer (trimpot)** | Tiny square with a screw head | "Set and forget" calibration, internal adjustments |
| **Thumbwheel** | Small gear you roll with your thumb | Compact volume controls |

### Trimpot Wiring

Trimpots are adjusted with a screwdriver. They're meant to be set once and left alone:

```
      ┌──────┐
      │      │
      │  ☝   │ ← Screw head
      │      │
      └──────┘
        │││
        ││└── Terminal 1
        │└─── Wiper
        └──── Terminal 2
```

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| ADC reads jump wildly | Wires too long, no filtering | Add a 100nF cap from wiper to GND |
| Value changes when touched | You're touching the wiper — your body acts as an antenna | Add a 10kΩ series resistor on wiper output |
| Knob feels rough/gritty | Dirt in the track | Replace it — they're cheap |
| Readings drop at extremes | ADC nonlinearity at voltage rails | Stay in 10%–90% range |
| Wrong resistance curve | You used an audio (A) pot for a linear application | Check the letter: use B for linear |

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Using an audio pot for voltage divider | ADC readings are non-linear — 50% rotation ≠ 50% voltage |
| No decoupling cap on wiper | Noisy ADC readings that jump randomly |
| Wiring only two pins (as variable resistor) without understanding taper | Resistance curve may not match expectations |
| Forgetting voltage divider current draw | B10K draws 0.33mA from 3.3V — fine, but B1K draws 3.3mA — significant in battery projects |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| 10kΩ linear potentiometer (B10K) | 1+ | The standard for most projects |
| 10kΩ log (audio) potentiometer (A10K) | 1 | If building audio controls |
| 100nF ceramic capacitor | 1 | Decoupling the wiper to GND |
| Knob cap | 1 | Optional but makes it feel professional |
| Trimpot 10kΩ (3296W) | 1 | For calibration/set-and-forget adjustments |

> **Pro tip:** If you need precise, repeatable resistance, use a digital potentiometer (like the MCP41xx or AD5206) controlled over SPI. No moving parts, no wear, no dirt.
