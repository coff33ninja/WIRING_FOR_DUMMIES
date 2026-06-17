# Multimeter — How to Use One

## What It Is

A multimeter (multimeter / DMM) measures voltage, current, resistance, and continuity. It's the single most important debugging tool in electronics. **90% of "why doesn't this work?" questions are answered with a multimeter.**

## The 4 Measurements You'll Actually Use

### 1. Voltage (V)

**How:** Turn dial to V (DC voltage, solid line over dashed line). Touch probes across the thing you're measuring — **in parallel**.

```
        ┌──────┐
  5V ───┤  LOAD ├─── GND
        └──────┘
        ↑  ↑
        │  │
        Red Black (probes)
```

**Common mistakes:**
- **Wrong range** — reading 3.3V when set to 200V AC gives 0. Reading 3.3V on AC setting gives 0. Always check the dial.
- **Probes in wrong jacks** — red probe in the 10A jack instead of V/Ω jack. The meter shows 0 and you wonder why.

**Pro tip:** If a circuit isn't working, **measure voltage at the chip's power pins first**. If the chip isn't getting power, nothing else matters.

### 2. Continuity (BEEP)

**How:** Turn dial to the diode/continuity symbol (→→)). With **power OFF**, touch both ends of a wire or trace.

```
Probe 1 ──────[wire]────── Probe 2
                ↓
            BEEP = connected (good)
        No beep = broken (open circuit)
```

**Use for:** Checking if a jumper wire is actually connected, if a fuse is blown, if a solder joint is good, if a PCB trace is broken.

**Common mistake:** Measuring continuity on a **live** circuit. The meter may beep, may not — and you can damage the meter. **Power off → measure continuity → power on.**

### 3. Resistance (Ω)

**How:** Turn dial to Ω. With **power OFF**, touch probes across a resistor (or component).

```
Probe 1 ────[470Ω Resistor]──── Probe 2
                ↓
           Display: ~470Ω
```

**Use for:** Checking resistor values (color codes can be wrong), checking if a switch/button closes properly, checking if a motor winding is shorted.

**Common mistakes:**
- Measuring resistance on a **live** circuit — meter shows garbage or "OL"
- **Body resistance** — touching both probe tips with your fingers shows 1–10MΩ (your skin resistance)
- Reading a resistor **in-circuit** — other components parallel to it affect the reading. Lift one leg or measure before soldering.

### 4. Current (A / mA)

**How:** Turn dial to mA or A. Move red probe to the **A or mA jack**. Break the circuit and insert the meter **in series**.

```
       ┌─[METER]─┐
       │    ↑    │
Power ─┘   Red   └─ Load ── GND
          (probes)
```

**This is the most dangerous measurement.** If you connect the meter in **parallel** across a voltage source (like measuring voltage), you short-circuit it through the meter's very low resistance shunt — blowing the meter's fuse or damaging the circuit.

**Use for:** Measuring how much current a project actually draws, checking if a motor is stalled (drawing too much), sizing a power supply.

**Common mistake:** Measuring current with probes in the **voltage jacks**. The meter reads 0 and you think the circuit isn't working. Move the red probe to the A/mA jack.

## Which Jack Does What

Most multimeters have 3–4 jacks:

```
   ┌─────────────────────────────┐
   │                             │
   │     COM     VΩmA     10A   │
   │     (COM)   (Volts,  (High  │
   │     Black   Ohms,    Amps)  │
   │     always)  mA)     Red   │
   │              Red           │
   └─────────────────────────────┘
```

| Jack | Label | Red goes here for | Max current |
|------|-------|-------------------|-------------|
| **COM** | COM | Black probe **always** | — |
| **VΩ** | VΩmA | Voltage, resistance, continuity, diode test, low current | 200–600mA (fused) |
| **mA** | VΩmA | Same as VΩ on some meters | 200–600mA (fused) |
| **10A** | 10A / 20A | High current (unfused — dangerous) | 10–20A (unfused) |

> **The 10A jack is usually unfused.** If you short 12V through the 10A jack with probes in the wrong mode, the wire inside gets red hot. Respect it.

## Auto-Ranging vs Manual

| Type | How it works | Pros | Cons |
|------|-------------|------|------|
| **Auto-ranging** | Automatically picks the right scale (V, mV, kΩ, MΩ) | Easier for beginners | Slower, sometimes jumps between ranges |
| **Manual** | You select the range (200Ω, 2kΩ, 20kΩ, etc.) | Faster once you know, more control | Shows "1" or "OL" if range is wrong |

**Manual range trick:** If you see "1" or "OL" on resistance mode, your range is too low. Turn the dial to the next higher range.

## What "OL" Means

| Mode | OL means |
|------|----------|
| Voltage | Over limit — voltage exceeds the range you selected (switch to higher range) |
| Resistance | **Open circuit** — no connection (or > range). Infinite resistance. |
| Continuity | No beep = open circuit (same as OL) |
| Diode | Open junction (or reverse-biased diode) |

## Common Debugging Flow

**"My circuit doesn't work" — what to check with the multimeter:**

1. **Power — is it actually there?**
   - Measure voltage at power supply output → should be ~5V or ~12V
   - Measure voltage at breadboard power rails → should match
   - Measure voltage at chip VCC pin → should be right voltage

2. **Ground — is it connected?**
   - Continuity test from chip GND pin to power supply GND → should beep

3. **Signal — is it changing?**
   - Button press: measure voltage at GPIO pin while pressing → should toggle HIGH/LOW
   - Sensor: measure voltage at sensor output while triggering → should change

4. **Current — is anything drawing too much?**
   - If voltage drops when you connect a load, measure current → may exceed supply rating

## Choosing a Multimeter

| Price range | What you get | Recommendation |
|------------|-------------|---------------|
| **$10–15** | Basic — V, Ω, continuity, diode, manual range | Works for 90% of hobby work |
| **$20–40** | Auto-ranging, capacitance, frequency, backlight, better safety | **Best for hobbyists** |
| **$50–100** | True RMS, temperature, data logging, CAT II/III safety | For mains/industrial work |
| **$100+** | Bench DMM, 4.5+ digits, PC connectivity | Lab use, precision |

> **Don't buy the absolute cheapest meter.** A $8 meter has unfused inputs and may be unsafe on mains voltage. A $25–30 meter (like the ANENG AN8008, UNI-T UT33, or a basic Fluke knockoff) is safe and accurate enough for hobby work.

## Quick Reference

```
Measure voltage:  Probes in COM + VΩ. Dial to V⎓. In PARALLEL with load.
Measure current:  Probes in COM + mA (or 10A). In SERIES with load. (Dangerous!).
Measure resistance: Probes in COM + VΩ. Dial to Ω. POWER OFF. Component isolated.
Continuity:       Probes in COM + VΩ. Dial to →)). POWER OFF. Beep = connected.

Jack rules:
  Black probe → COM (always)
  Red probe   → VΩ for voltage, resistance, continuity
  Red probe   → mA or 10A for current (move probe!)

Safety:
  Never measure resistance on a live circuit
  Never measure continuity on a live circuit
  Never connect current probes in parallel (short!)
  When in doubt → start with voltage measurement (safest)
  If you blow a fuse in the meter, replace it with the SAME rating
```

## See Also

- [relay-module](/projects/relay-module)
- [esp32-fan-controller](/projects/esp32-fan-controller)
- [hc-sr04-ultrasonic](/projects/hc-sr04-ultrasonic)
- [stepper-motor-a4988](/projects/stepper-motor-a4988)
