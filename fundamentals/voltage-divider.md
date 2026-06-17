# Voltage Divider — Fundamental Reference

## What It Is

A voltage divider uses **two resistors in series** to produce a fraction of the input voltage. It's the simplest way to measure a higher voltage with an ADC, shift signal levels, or create a reference voltage.

> **Analogy:** A seesaw. If you put the pivot closer to one end, the long side moves more and the short side moves less. The total length (R1+R2) determines how much "effort" the seesaw takes from the input.

## The Formula

```
Vin ──── R1 ────┬──── Vout
                │
                R2
                │
               GND

Vout = Vin × R2 / (R1 + R2)
```

**Examples:**

| Vin | R1 | R2 | Vout | Notes |
|-----|-----|-----|------|-------|
| 5V | 10kΩ | 10kΩ | 2.5V | Equal divider — half voltage |
| 5V | 10kΩ | 20kΩ | 3.33V | R2 bigger → higher output |
| 5V | 20kΩ | 10kΩ | 1.67V | R1 bigger → lower output |
| 12V | 10kΩ | 10kΩ | 6V | Works at any voltage — ratio matters |
| 12V | 1kΩ | 1kΩ | 6V | Same ratio, different resistors |

> **Only the ratio matters.** R1=10kΩ + R2=10kΩ gives the same Vout as R1=1MΩ + R2=1MΩ. What changes is the current wasted and the accuracy when a load is connected.

## Choosing Resistor Values — Accuracy vs Current Waste

Every voltage divider wastes some current:

```
I_divider = Vin / (R1 + R2)
```

| Total resistance | At 5V current waste | At 12V current waste |
|---|---|---|
| 100Ω | 50mA | 120mA — way too much |
| 1kΩ | 5mA | 12mA — high for battery |
| 10kΩ | 500µA | 1.2mA — good for most uses |
| 100kΩ | 50µA | 120µA — good for battery |
| 1MΩ | 5µA | 12µA — minimal waste, but loading matters |

**General guidelines:**

| Situation | Recommended total (R1+R2) | Why |
|---|---|---|
| Battery-powered sensor | 100kΩ–1MΩ | Low quiescent current |
| ADC input (slow) | 10kΩ–100kΩ | Balances accuracy and current |
| ADC input (fast) | 1kΩ–10kΩ | Charges ADC sample-and-hold cap faster |
| On a breadboard test | 10kΩ | Easy math, low waste |
| Power supply feedback | 1kΩ–10kΩ | Stable, less noise pickup |

**Rule of thumb for most hobby projects:** Start with 10kΩ total (e.g., two 10kΩ resistors for a 50% divider). This gives 500µA at 5V — negligible for most applications.

## The Loading Effect — When the Divider Meets a Load

The formula above assumes **no current flows out of the divider's output**. As soon as you connect a load (like an ADC input, a transistor base, or another circuit), you're putting a resistor in parallel with R2, which changes the ratio.

```
Vin ──── R1 ────┬──── Vout ──── R_load ──── GND
                │
                R2
                │
               GND
```

**Example:** A 12V battery measured through a 10kΩ+10kΩ divider gives 6V at the divider. Connect it to an ESP32 ADC (which has ~100kΩ input impedance), and the effective R2 becomes:

```
R2_effective = 10kΩ || 100kΩ = 9.09kΩ
Vout = 12V × 9.09kΩ / (10kΩ + 9.09kΩ) = 12V × 0.476 = 5.71V
```

Your 6V divider output just dropped to **5.71V** — a 5% error.

### The 10× Rule of Thumb

**The load resistance should be at least 10× the divider's R2 resistance.**

```
R_load ≥ 10 × R2
```

If R2 = 10kΩ, the load should be ≥ 100kΩ for <1% error.

| Divider resistance (R2) | Minimum load for <1% error |
|---|---|
| 1kΩ | 10kΩ |
| 10kΩ | 100kΩ |
| 100kΩ | 1MΩ |
| 1MΩ | 10MΩ |

**What to do if you can't meet 10×:**
- **Use lower divider resistors** (e.g., 1kΩ+1kΩ instead of 100kΩ+100kΩ). This wastes more current but reduces loading error.
- **Use a buffer** — an op-amp voltage follower (unity gain) between the divider and the load. The op-amp's input impedance is megaohms, so loading is negligible.
- **Measure the loaded divider** and calibrate in software (not ideal — your calibration drifts with temperature and over time).

## Using a Divider for ADC — Reading Higher Voltages

Most microcontroller ADCs read 0–3.3V or 0–5V. To measure a higher voltage (like a 12V battery), use a voltage divider to scale it down.

### For 3.3V ADC (ESP32, many ARM MCUs)

| Voltage to measure | Divider ratio | Example resistors | Scaled output |
|---|---|---|---|
| 0–5V | 2:3 (Vout = Vin × 0.66) | R1=4.7kΩ, R2=10kΩ | 5V → 3.3V |
| 0–12V | 1:3.6 (Vout = Vin × 0.275) | R1=22kΩ, R2=10kΩ | 12V → 3.3V |
| 0–25V | 1:7.6 (Vout = Vin × 0.132) | R1=68kΩ, R2=10kΩ | 25V → 3.3V |

### For 5V ADC (Arduino Uno/Nano)

| Voltage to measure | Divider ratio | Example resistors | Scaled output |
|---|---|---|---|
| 0–10V | 1:1 (Vout = Vin × 0.5) | R1=10kΩ, R2=10kΩ | 10V → 5V |
| 0–12V | 5:12 (Vout = Vin × 0.416) | R1=15kΩ, R2=10kΩ | 12V → 5V |
| 0–25V | 1:5 (Vout = Vin × 0.2) | R1=40kΩ, R2=10kΩ | 25V → 5V |

### Including the ADC's Own Input Impedance

MCU ADCs have internal resistance (typically 10kΩ–100kΩ). To avoid loading error, either:

1. **Keep divider resistance low** — total R1+R2 < 10kΩ. This wastes more current but minimizes loading.
2. **Add a capacitor** — 0.1µF from the divider output to ground. This charges up and provides the ADC's instantaneous charge during sampling.
3. **Use smaller measurement resistors** — 1kΩ+1kΩ instead of 100kΩ+100kΩ.

> **For ESP32 specifically:** The ADC input impedance is about 100kΩ. Use a divider with R1+R2 ≈ 2–10kΩ total for accurate readings. Better yet, an external ADC (like ADS1115) has a much higher input impedance and is less picky.

## 5V → 3.3V Level Shifting (One Direction)

A voltage divider can shift a 5V signal down to 3.3V for an ESP32 or similar 3.3V logic input.

```
5V signal ──── R1=10kΩ ────┬──── 3.3V logic input
                           │
                          R2=20kΩ
                           │
                          GND

Vout = 5V × 20k / (10k + 20k) = 5V × 0.667 = 3.33V
```

**Limitations:**
- This only works **one direction** (5V→3.3V, not 3.3V→5V).
- It's **slow** — the RC time constant (R1 || R2 × load capacitance) limits data rate. OK for <100kHz signals, not for I2C fast mode or SPI.
- For bidirectional or high-speed signals, use a proper level shifter (e.g., BSS138 MOSFET-based).

**Good for:** One-way 5V UART TX → 3.3V RX, push-button inputs, simple logic signals.

## Using a Potentiometer as an Adjustable Divider

A potentiometer is a voltage divider in a single package. The wiper moves between the two ends, giving an adjustable output.

```
                     ┌──────┐
Vin ────┬────────────┤  B   ├──── GND
        │            │  pot │
        └────────────┤  A   │
                     │  W   │
                     └──┬───┘
                        │
                      Vout
```

| Pot value | Current waste at 5V | Best for |
|---|---|---|
| 1kΩ | 5mA | Fine control, high current |
| 10kΩ | 500µA | General purpose |
| 100kΩ | 50µA | Low power, high impedance input |
| 1MΩ | 5µA | Very low power, slow adjustments |

**Common pot configurations:**
- **Voltage reference:** Wire as shown above — gives 0V to Vin
- **Variable resistor (rheostat):** Connect only the wiper and one end. This creates a variable resistance, not a divider.
- **Trimmer pot:** Small, screw-adjustable, intended for "set-and-forget" calibration on a PCB.

> **Caution:** Don't use a pot as a "big knob" for high-current applications like dimming an LED. The pot's power rating is tiny (typically 0.1–0.5W). Use a proper PWM + MOSFET instead.

## Quick Reference

```
Formula: Vout = Vin × R2 / (R1 + R2)
  Only the ratio matters — R1=10k+R2=10k = same as 100k+100k

Choose R values:
  Low R (100Ω–1kΩ):   Accurate under load, wastes current, gets hot
  Medium R (10kΩ):     Good balance for most hobby projects
  High R (100kΩ+):     Low current waste, loading error, noise pickup

10× rule: R_load ≥ 10 × R2 for <1% loading error

ADC scaling:
  3.3V ADC: R1=22kΩ, R2=10kΩ → 0–12V → 0–3.3V
  5V ADC:   R1=10kΩ, R2=10kΩ → 0–10V → 0–5V

Level shifting (5V→3.3V):
  R1=10kΩ, R2=20kΩ → 5V → 3.33V (one direction, <100kHz)

Pot as divider: 10kΩ pot = adjustable 0V–Vin (set-and-forget with trimmer)

Watch out:
  - Loading effects distort your reading
  - ADC input impedance acts as a load on R2
  - High resistances pick up noise (keep wires short)
  - Pots have low power ratings — don't use them for loads
```

## See Also

- [hc-sr04-ultrasonic](/projects/hc-sr04-ultrasonic)
