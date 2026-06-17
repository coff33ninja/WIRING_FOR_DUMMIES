# Capacitor — Component Reference

## What It Is

A capacitor is a **tiny rechargeable battery** that stores electrical charge and releases it almost instantly. Think of it as a **water tower** in a town's water system — when demand spikes, the tower provides water instantly without waiting for the pump to catch up.

This is called **decoupling** or **bypassing** — the #1 reason we add capacitors to circuits.

## Capacitor Types — Which One for Which Job

### 1. Multilayer Ceramic (MLCC) — The Most Common

Small, brown/orange/blue block or disc. **No polarity.**

```
     ╔═══╗
     ║   ║   No polarity — either way works
     ║   ║
     ╚═══╝
        ││
```

| Pros | Cons |
|------|------|
| Cheap, small, widely available | **Lose capacitance with DC bias** (critical!) |
| Low ESR (good for high-frequency) | Can be microphonic (vibrate with audio) |
| No polarity | Capacitance varies with temperature |

**Use for:** Decoupling (100nF next to every chip), high-frequency filtering, general-purpose.

**Temperature coefficients (read the marking):**

| Code | Tolerance | Drift | Use for |
|------|-----------|-------|---------|
| **C0G / NP0** | ±30ppm/°C | None | Precision, oscillators, filters |
| **X7R** | ±15% over −55°C to +125°C | Moderate | General decoupling, bulk (good) |
| **X5R** | ±15% over −55°C to +85°C | Moderate | Same as X7R, narrower temp range |
| **Y5V** | +22%/−82% over −30°C to +85°C | Wild | Don't use — capacitance collapses |
| **Z5U** | +22%/−56% over +10°C to +85°C | Poor | Avoid — obsolete for most uses |

> **The DC bias trap:** An X7R 10µF cap rated at 10V will only measure ~3–5µF when 5V DC is applied. This is normal. It's called DC bias derating. If you need 10µF at 5V, use a 25V-rated cap or check the datasheet's bias curve.

### 2. Aluminum Electrolytic — The Big Cans

Cylindrical, blue or black. **Polarized — reverse kills them.**

```
      ││
    ──┘│────  Long leg = Positive (+)
       │
    ──┐│────  Short leg = Negative (−)
      ││
      ││
    Stripe on side = Negative
```

| Pros | Cons |
|------|------|
| High capacitance in small package (1–4700µF) | Polarized — blows if reversed |
| High voltage ratings available | High ESR, poor at high frequencies |
| Cheap | Leakage current, dries out over years |

**Use for:** Bulk storage (100–1000µF), power supply smoothing, audio coupling.

**The X on top:** Electrolytics have a scored vent. If overvoltaged or reversed, they pop open. It's a safety feature. If you see a bulging top, replace it immediately.

### 3. Tantalum — Small but Dangerous

Small, yellow/orange/black rectangular blob. **Polarized — stripe = + (positive!).**

```
      ┌──────┐
      │      │
      │ ═══  │  Stripe = + (opposite of electrolytic!)
      │      │
      └──────┘
```

| Pros | Cons |
|------|------|
| Stable capacitance across voltage/temp | **Catastrophic failure if overvoltaged** (fire) |
| Small for the value | Expensive |
| Low ESR | Polarity is opposite from electrolytics |

**Use for:** When you need stable capacitance in a small SMD package. **Never use tantalum for power supply input** — a voltage spike will short it and it can catch fire.

> **Tantalum vs electrolytic:** Tantalum has the stripe on the POSITIVE side. Electrolytic has the stripe on the NEGATIVE side. If you confuse them, the tantalum goes "pop."

### 4. Film Capacitor — For Audio and Precision

Rectangular box, clear or colored. **No polarity.**

```
      ╔══════════╗
      ║ 104J100  ║
      ╚══════════╝
```

| Type | Material | Best for |
|------|----------|----------|
| **Polyester (Mylar)** | PET | General audio, coupling |
| **Polypropylene** | PP | High-end audio, snubbers, high frequency |
| **Polycarbonate** | PC | Precision timers (hard to find now) |

**Use for:** Audio circuits (low distortion), timing circuits (stable), snubber networks.

### 5. Supercapacitor (EDLC) — The Battery Alternative

Large cylindrical, looks like a coin cell or small AA. **Polarized.**

| Pros | Cons |
|------|------|
| Huge capacitance (1–3000F) | Low voltage (2.5–2.7V per cell) |
| Charges fast | High ESR, can't deliver high current |
| Rechargeable for 500k+ cycles | Leaks down over days/weeks |

**Use for:** Backup power for RTCs, brief hold-up during battery swaps, energy harvesting. **Not a battery replacement** for high-current applications.

## Quick Selection Guide

| Job | Best type | Typical value |
|-----|-----------|---------------|
| Decoupling a chip's power pins | MLCC X7R or C0G | 100nF (0.1µF) |
| ESP32 module bulk decoupling | MLCC X7R or tantalum | 10µF |
| Power supply input smoothing | Electrolytic | 100–470µF |
| Motor/fan/LED strip supply | Electrolytic | 100–1000µF |
| Audio signal coupling | Film (polypropylene) | 1–10µF |
| RF / oscillator tank circuit | MLCC C0G/NP0 | 10–100pF |
| RTC backup power | Supercapacitor | 0.1–1F |
| Switching regulator input | MLCC + electrolytic | 10µF + 100µF |

## ESR — What It Is and Why It Matters

ESR (Equivalent Series Resistance) is the internal resistance of a capacitor. It's not in the datasheet spec for hobby parts, but it matters:

| Cap type | ESR | Good for | Bad for |
|----------|-----|----------|---------|
| MLCC | Very low (<10mΩ) | High-frequency decoupling | — |
| Film | Low (10–100mΩ) | Audio, snubbers | — |
| Tantalum | Medium (100mΩ–2Ω) | Bulk bypass | Power input (risky) |
| Electrolytic | High (0.1–10Ω) | Power smoothing | High-frequency filtering |
| Supercapacitor | Very high (1–30Ω) | Hold-up power | Quick discharge |

> **Rule:** Lower ESR is better for decoupling. Higher ESR means the cap can't respond to sudden current demands — it "looks" like a resistor to fast signals.

## Capacitance Values

| Value | Written as | Best type | Used for |
|-------|------------|-----------|----------|
| 100pF | 100pF | MLCC C0G | RF / high-frequency filtering |
| 1nF | 1nF / 0.001µF | MLCC C0G/X7R | Noise filtering |
| 10nF | 10nF / 0.01µF | MLCC X7R | General noise filtering |
| 100nF | 100nF / 0.1µF | MLCC X7R | **Microcontroller decoupling (standard)** |
| 1µF | 1µF / 105 | MLCC X7R | Chip bulk decoupling |
| 10µF | 10µF | MLCC X7R or tantalum | ESP32 module decoupling |
| 47µF | 47µF | Electrolytic | Medium bulk |
| 100µF | 100µF | Electrolytic | Motor/fan decoupling |
| 470µF | 470µF | Electrolytic | Big motor/audio |
| 1000µF | 1000µF | Electrolytic | LED strips, servo power |
| 1F+ | 1F | Supercapacitor | RTC backup |

## Voltage Rating

**Always use a capacitor rated for more voltage than your circuit uses.** Rule: **2× the circuit voltage for electrolytics, 1.5× for ceramics.**

| Circuit voltage | Minimum cap rating |
|-----------------|-------------------|
| 3.3V | 6.3V or 10V |
| 5V | 10V or 16V |
| 12V | 25V |
| 24V | 50V |
| 48V | 100V |

> A 16V cap on a 24V circuit = the cap **explodes**. Electrolytics have a scored X on top that splits open to vent — safety feature, not a bug. MLCCs can crack and short.

## What Happens If You Choose the Wrong Type

| Scenario | Wrong choice | Result |
|----------|-------------|--------|
| 100nF decoupling — used electrolytic | Doesn't work at high frequency — chip still crashes | Use MLCC |
| Power supply smoothing — used MLCC | Electrically OK but need 10x the value and space | Use electrolytic |
| Audio coupling — used electrolytic | Signal distortion, bass roll-off | Use film |
| RTC backup — used electrolytic | Drains battery too fast (leakage) | Use supercapacitor |
| Switching regulator — used high-ESR cap | Ripple on output, regulator unstable | Use low-ESR MLCC + electrolytic |
| Hot environment — used Y5V | Capacitance drops to near zero | Use X7R or X5R |

## Quick Reference

```
MLCC (no polarity):       Decoupling, filtering, general use
  C0G/NP0 = stable        X7R/X5R = good all-round      Y5V/Z5U = avoid
  
Electrolytic (+/−):       Bulk storage, power smoothing
  Stripe = negative        Long leg = positive
  
Tantalum (+/−):           Compact bulk (dangerous if overvolted)
  Stripe = positive!       (opposite of electrolytic!)
  
Film (no polarity):       Audio, timing, precision

Supercapacitor (+/−):     RTC backup, brief hold-up

ESR rule: Lower is better for fast signals
DC bias trap: MLCCs lose capacitance under voltage — derate 2x
```
