# AC vs DC — Fundamental Reference

## What It Is

**AC (Alternating Current)** reverses direction periodically — voltage swings positive and negative. **DC (Direct Current)** flows in one direction only — voltage stays at a fixed polarity.

> **Not the band.** Although both can blow out your speakers if you're not careful.

```
AC:      ╔══════════════╗
         ║   ╱╲    ╱╲   ║
         ║  ╱  ╲  ╱  ╲  ║
         ║ ╱    ╲╱    ╲ ║
         ║╱              ╲║
         ╚══════════════╝
         Voltage alternates polarity

DC:      ╔══════════════╗
         ║ ──────────── ║
         ║              ║
         ║              ║
         ║──────────────║
         ╚══════════════╝
         Constant polarity (e.g., 5V)
```

## Key Differences

| Property | AC | DC |
|----------|-----|-----|
| Direction | Reverses periodically | One direction only |
| Voltage | Sinusoidal (typically) | Constant (or slowly varying) |
| Polarity | Alternating (+ / −) | Fixed (+ and − don't swap) |
| Frequency | 50Hz or 60Hz (mains) | 0 Hz (no cycling) |
| Transmission over distance | Excellent (easy to transform) | Poor (high losses at low voltage) |
| Storage | Not directly storable | Storable in batteries |
| Generation | Alternators, mains grid | Batteries, solar panels, rectified AC |
| Danger | Muscle lock (harder to let go) | Let-go possible, but burns more |
| Common use | Power grid, appliances, motors | Electronics, batteries, vehicles |

## AC (Alternating Current)

### What's AC

- Household wall power (120V / 230V)
- Large motors and industrial equipment
- Long-distance power transmission lines
- Older dimmer switches
- Transformers (only work on AC)
- Audio signals (signal AC, not power AC)

### AC Waveform — The Sine Wave

AC voltage follows a sine wave:

```
  +Peak ──╱╲──────────╱╲────
          ╱  ╲        ╱  ╲
         ╱    ╲      ╱    ╲
  0V ───╱──────╲────╱──────╲──
        ╱        ╲  ╱        ╲
       ╱          ╲╱          ╲
  −Peak ─────────────────────────
```

**Key AC terms:**

| Term | Meaning | Example |
|------|---------|---------|
| **Frequency** | Cycles per second (Hz) | 60Hz = 60 cycles/s |
| **Period** | Time for one cycle | 16.67ms (60Hz) |
| **Peak voltage (Vpk)** | Maximum voltage from 0 | 170V (for 120V RMS) |
| **Peak-to-peak (Vpp)** | +Peak to −Peak | 340V (for 120V RMS) |
| **RMS voltage** | Equivalent DC voltage that delivers same power | 120V RMS = 170V peak |

### RMS vs Peak — Why 120V AC is Not 120V

The 120V you see on a wall outlet is **RMS** (Root Mean Square), NOT the peak voltage. The actual voltage swings from +170V to −170V:

```
RMS = Peak / √2          Peak = RMS × √2

120V RMS × 1.414 = ~170V peak
120V AC swings from +170V to −170V every cycle
```

**Why use RMS?** A 120V RMS AC source delivers the same power to a resistor as 120V DC. It's the "effective" voltage.

| Mains standard | RMS voltage | Peak voltage | Peak-to-peak |
|----------------|-------------|-------------|--------------|
| US / Japan | 120V | 170V | 340V |
| Europe / Asia | 230V | 325V | 650V |
| UK | 240V | 339V | 678V |

### Mains Frequency by Region

| Region | Frequency | Why it matters |
|--------|-----------|---------------|
| North America | 60Hz | Motors run faster, transformers smaller |
| Europe / Asia | 50Hz | Slightly better for long-distance |
| Japan (east) | 50Hz | Tokyo area |
| Japan (west) | 60Hz | Osaka area |
| Aircraft | 400Hz | Smaller, lighter transformers |

### Three-Phase AC

Industrial equipment uses three phases — three AC waves offset by 120°:

```
Phase A:  ╱╲      ╱╲      ╱╲
Phase B:  ╲╱╲    ╱  ╲    ╱
Phase C:   ╲ ╲╱  ╱    ╲  ╱
```

Three-phase delivers more power, smoother, with smaller wires.

### AC Safety

**AC is more dangerous than DC at the same voltage** because:

- AC causes muscle tetanus (continuous contraction) — you can't let go
- AC crosses 0V 100–120 times per second, but the peaks are higher than RMS
- AC can skip past skin resistance more easily (capacitive coupling through the body)

## DC (Direct Current)

### What's DC

- Batteries (all types: AA, 18650, LiPo, lead-acid)
- USB power
- Solar panels
- All digital electronics (microcontrollers, sensors, logic chips)
- LED lighting
- Vehicles (cars, boats, RVs — though alternators produce AC that's rectified to DC)
- Most small motors (DC motors, servo motors)

### DC Waveform — Flat Line

Ideal DC is a constant voltage, always positive (or negative):

```
  5V ────╔══════════════╗────────
          ║              ║
          ║              ║
          ║              ║
  0V ────╚══════════════╝────────
```

**Real-world DC has ripple** — small AC fluctuations on top of the DC:

```
  5V ────╔═╱╲═╱╲═╱╲═╱╲═╗───────
          ║              ║
  0V ────╚══════════════╝────────
```

Ripple comes from imperfect rectification (converting AC to DC). A capacitor smooths it out.

### DC Voltage Levels in Hobby Electronics

| Voltage | Common use |
|---------|-----------|
| **1.5V** | AA / AAA battery |
| **3.3V** | ESP32, Raspberry Pi, modern MCUs |
| **5V** | Arduino, USB, most sensors |
| **6V** | Some servos, older cameras |
| **9V** | Old Arduino (via barrel jack), guitar pedals |
| **12V** | LED strips, relays, car systems |
| **24V** | Industrial sensors, some motors |

### Polarity Matters

DC has a defined **positive (+)** and **negative (−)**. **Reverse polarity destroys electronics:**

```
Correct:   [+]───→[circuit]───→[−]   ← Works
Reversed:  [−]───→[circuit]───→[+]   ← May release magic smoke
```

**Protection methods:**
- **Schottky diode in series:** drops ~0.2–0.4V but protects against reverse polarity
- **Reverse polarity MOSFET:** near-zero voltage drop, works like a smart switch
- **Bridge rectifier:** works regardless of polarity (but drops ~1.4V)

## AC ↔ DC Conversion

### AC to DC (Rectification)

**Half-wave rectification:** Uses one diode — only passes positive half of AC:

```
AC in:  ╱╲  ╱╲  ╱╲          DC out:  ╱╲    ╱╲    ╱╲
       ╱  ╲╱  ╲╱  ╲                 ╱  ╲   ╱  ╲  ╱  ╲
      ╱        ╲                    ╱    ╲ ╱    ╲╱    ╲
    ─╱──────────╲────────         ─╱──────────────╱───────
```

**Full-wave bridge rectification:** Uses 4 diodes — flips negative half to positive:

```
AC in:  ╱╲    ╱╲    ╱╲      DC out:  ╱╲╱╲  ╱╲╱╲  ╱╲╱╲
       ╱  ╲  ╱  ╲  ╱  ╲             ╱    ╲╱    ╲╱    ╲
      ╱    ╲╱    ╲╱    ╲          ╱              ╱      ╲
      ╱      ╲      ╲              ╱              ╱        ╲
```

**Adding a capacitor** (smoothing) turns the bumpy DC into smoother DC:

```
Before cap:  ╱╲╱╲╱╲╱╲          After cap:  ═══╱╲═══╱╲═══
            ╱    ╲    ╲                    ║      ║
```

Adding a **voltage regulator** (linear or buck) gives clean, stable DC.

### DC to AC (Inversion)

Used for: solar power systems, UPS backup, variable-frequency motor drives.

```
DC in:  ────────────          AC out:  ╱╲    ╱╲    ╱╲
                                       ╱  ╲  ╱  ╲  ╱  ╲
                                      ╱    ╲╱    ╲╱    ╲
```

A simple inverter switches DC on and off rapidly, then steps it up with a transformer.

| Inverter output | Quality | Use |
|----------------|---------|-----|
| **Square wave** | Poor — harmonics, buzz | Cheap inverters, some motors |
| **Modified sine** | OK — stepped square wave | Most consumer devices |
| **Pure sine** | Excellent — same as grid | Sensitive electronics, medical |

## Why the Grid Uses AC

AC won over DC in the "War of the Currents" (Edison vs Tesla, 1880s) because of **transformers**:

```
Generator (low voltage AC) → Step-up transformer → High voltage AC → Long-distance lines
  ↓
Step-down transformer → Low voltage AC → Your house

DC couldn't be voltage-transformed easily → required thick copper wire every few blocks
```

Today, HVDC (High Voltage DC) is used for very long undersea cables and cross-country lines — it has lower losses than AC at extreme distances. But the grid is still overwhelmingly AC.

## Quick Reference

- **AC:** Voltage alternates, easy to transform, used for power grid and motors
- **DC:** Voltage constant, storable in batteries, used for all electronics
- **Mains AC:** 120V / 230V RMS, 50/60Hz, swings to ±170V / ±325V peak
- **Rectification:** AC → DC using diodes (1 diode = half-wave, 4 diodes = full-wave)
- **Inversion:** DC → AC using switching + transformer
- **RMS voltage:** The "equivalent DC" — use this for power calculations
- **Polarity:** DC has polarity — reversing it destroys electronics. AC doesn't.
- **Safety:** Both kill at high enough current. AC locks muscles; DC causes burns. Neither is safe to touch.
- **Never assume ground is neutral** — in AC wiring, neutral and ground are different things
- **Running DC electronics on AC** (without a proper power supply) = instant destruction

## See Also

- [relay-module](/projects/relay-module)
