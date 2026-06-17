# 555 Timer IC — Component Reference

## What It Is

The **555 timer** is an 8-pin integrated circuit that generates precise timing pulses. It can run in three modes: **astable** (continuous square wave oscillator), **monostable** (one-shot pulse), and **bistable** (flip-flop / latch). It's the most popular timer chip in hobby electronics — used for debouncing, PWM generation, tone generation, blinking LEDs, and delay circuits.

> **Analogy:** A kitchen timer you can set for "buzz forever" (astable), "buzz once when you press" (monostable), or "on/off toggle button" (bistable).

## Pinout

```
          ┌──────────┐
   GND ───┤1        8├─── VCC (4.5–16V)
  TRIG ───┤2        7├─── DISCH (Discharge)
  OUT ────┤3        6├─── THRES (Threshold)
  RESET ──┤4        5├─── CONT (Control Voltage)
          └──────────┘
```

| Pin | Name | Function |
|-----|------|----------|
| 1 | GND | Ground (0V) |
| 2 | TRIG | Trigger — when voltage drops below 1/3 VCC, output goes HIGH |
| 3 | OUT | Output — HIGH (~VCC – 1.7V) or LOW (~0V) |
| 4 | RESET | Force output LOW when tied to GND. Connect to VCC to enable. |
| 5 | CONT | Control Voltage — changes threshold/trigger levels. Bypass with 0.1µF to GND if unused. |
| 6 | THRES | Threshold — when voltage rises above 2/3 VCC, output goes LOW |
| 7 | DISCH | Discharge — open-collector that shorts to GND when output is LOW |
| 8 | VCC | Power supply (4.5–16V for NE555, 2–16V for TLC555) |

## Astable Mode (Continuous Square Wave)

In astable mode, the 555 **oscillates continuously** — a square wave generator.

**Circuit:**

```
               VCC
                │
                ├── R1 ──┬── R2 ──┬── THRES (pin 6)
                │        │        │      TRIG (pin 2)
                │        │        │
                │        │        ├── DISCH (pin 7)
                │        │        │
                │       GND       │
                │               Capacitor (C)
                │                 │
                │                GND
```

**Frequency and duty cycle formulas:**

| Parameter | Formula | Notes |
|-----------|---------|-------|
| tHIGH (charging) | t_H = 0.693 × (R1 + R2) × C | Output HIGH time |
| tLOW (discharging) | t_L = 0.693 × R2 × C | Output LOW time |
| Period | T = t_H + t_L | Total cycle time |
| Frequency | f = 1.44 / ((R1 + 2R2) × C) | In Hz |
| Duty cycle | D = (R1 + R2) / (R1 + 2R2) × 100 | Always >50% |

**Duty cycle is always >50%** in the basic astable circuit because R1 is always part of the charging path.

To get **exactly 50% duty** (or less), add a diode across R2 so the capacitor charges through R1 only and discharges through R2 only.

**Common values and resulting frequencies:**

| R1 | R2 | C | Frequency | Duty | Use |
|----|----|---|-----------|------|-----|
| 1kΩ | 10kΩ | 10µF | ~6.2 Hz | ~52% | Blinking LED |
| 1kΩ | 10kΩ | 1µF | ~62 Hz | ~52% | Audio tone (low) |
| 1kΩ | 10kΩ | 0.1µF | ~620 Hz | ~52% | Audio tone |
| 1kΩ | 10kΩ | 0.01µF | ~6.2 kHz | ~52% | PWM carrier |
| 10kΩ | 100kΩ | 10nF | ~1.3 kHz | ~52% | Tone generator |

**Resistor limits:**
- R1 minimum: ~1kΩ (keeps discharge transistor current safe)
- R2 minimum: ~1kΩ
- Total (R1 + 2R2) maximum: ~20MΩ (leakage becomes a problem above that)

## Monostable Mode (One-Shot Pulse)

In monostable mode, the 555 outputs a **single pulse** of a fixed duration when triggered. It stays low until a falling edge on TRIG starts the timer, then returns low until the next trigger.

**Circuit:**

```
              VCC
               │
               ├── R ──┬── THRES (pin 6)
               │       │      DISCH (pin 7)
               │       │
               │   Capacitor (C)
               │       │
               │      GND
               │
TRIG (pin 2) ──┼── Trigger input (normally HIGH, pulse LOW to start)
               │
VCC ─────────── R ──── TRIG (pull-up, ensures TRIG stays HIGH)
```

**Pulse width formula:**

t = 1.1 × R × C

| R | C | Pulse width |
|---|----|-------------|
| 10kΩ | 10µF | 1.1 × 10k × 10µ = 110ms |
| 100kΩ | 10µF | 1.1s |
| 1MΩ | 10µF | 11s |
| 10kΩ | 100µF | 1.1s |
| 100kΩ | 1000µF | 110s (~2 min) |

**Timing constraints:**
- Trigger pulse must be shorter than the output pulse (or it re-triggers)
- Trigger must go below 1/3 VCC to start (falling edge)
- Output pulse cannot be interrupted by a new trigger (it ignores new triggers until done)

**Use cases:**
- Button debouncing (press → one clean pulse)
- Delay before turning something on
- "Press to activate for X seconds" (doorbell, timed relay)

## Bistable Mode (Flip-Flop / Latch)

In bistable mode, the 555 acts as a **set/reset latch**. Two inputs control the output: one sets it HIGH, the other sets it LOW. No timing components needed.

**Circuit:**

```
                  VCC
                   │
  Set button ───── R ──┬── TRIG (pin 2)
  (pulse LOW)          │
                   R ──┘
                   │
  Reset button ──── R ──┬── THRES (pin 6)
  (pulse LOW)           │
                   R ──── VCC (pull-up)
```

**Simplified:**

```
TRIG (pin 2) ──── HIGH (pulled up). Pulse LOW → output goes HIGH (set)
THRES (pin 6) ─── HIGH (pulled up). Pulse LOW → output goes LOW (reset)
DISCH (pin 7) ─── Leave floating (unused)
```

| Action | TRIG | THRES | OUT |
|--------|------|-------|-----|
| Set | <1/3 VCC | — | HIGH |
| Reset | — | >2/3 VCC | LOW |

**Use cases:**
- Toggle switch replacement (one button for on, another for off)
- Simple memory element
- Latching over-temperature / over-current alarm

> **Difference from a D flip-flop:** The 555 bistable is level-sensitive, not edge-triggered. Holding TRIG low keeps output high until you release and re-trigger.

## RC Time Constant

All 555 timing comes from the **RC time constant**: τ = R × C

| Value | Time constant (1τ) | Charge to 63% | Reach 2/3 VCC (~66.7%) |
|-------|-------------------|---------------|-----------------------|
| 1kΩ + 1µF | 1ms | ~1ms | ~1.1ms |
| 10kΩ + 1µF | 10ms | ~10ms | ~11ms |
| 100kΩ + 10µF | 1s | ~1s | ~1.1s |
| 1MΩ + 100µF | 100s | ~100s | ~110s |

The 555 triggers at 1/3 VCC (discharge) and thresholds at 2/3 VCC (charge) — that's why the formulas use 0.693 (= ln 2) and 1.1 (= ln 3).

- **0.693** = ln(2) — time to charge from 1/3 to 2/3
- **1.1** = ln(3) — time to charge from 0 to 2/3

## Bypass Capacitor on Control Voltage (Pin 5)

Pin 5 (CONT) is the internal voltage divider tap. It sets the threshold at 2/3 VCC.

**If pin 5 is left floating:** Noise on the power supply couples into the voltage divider and changes the timing — the 555 fires early or late.

**Always connect a 0.1µF (100nF) ceramic capacitor** from pin 5 to GND:

```
CONT (pin 5) ───── 0.1µF ───── GND
```

This filters power supply noise so the internal reference voltage stays steady.

> You can also use pin 5 to **change the threshold manually** (e.g., apply a 0–5V control voltage for VCO (voltage-controlled oscillator) operation). But for normal timing, just bypass it.

## CMOS Version (TLC555) vs Bipolar (NE555)

There are two main families of 555 chips:

| Property | NE555 (bipolar) | TLC555 / LMC555 (CMOS) |
|----------|----------------|------------------------|
| VCC range | 4.5–16V | 2–16V |
| Typical current draw | ~6–12mA | ~0.1–0.5mA |
| Output drive | 200mA (strong) | 10–50mA |
| Max frequency | ~500kHz | ~2–3MHz |
| Input leakage | ~0.5µA | ~1–10pA (much lower) |
| Timing capacitor range | ≥100pF | ≥10pF |
| Cost | $0.10–0.30 | $0.30–0.50 |

**When to use NE555:**
- You need high output current (driving a relay, speaker)
- You have 5–12V available
- Cost is critical
- Precision timing not required

**When to use TLC555:**
- Battery-powered project (low power consumption)
- 3.3V microcontroller project (CMOS works at 3V, bipolar doesn't)
- Long timing periods (minutes) — CMOS input leakage is much lower, so large R values actually work
- Higher frequency PWM (CMOS can switch faster)

> **Gotcha:** The TLC555 output can't swing all the way to VCC under load — it loses about 0.1–0.3V. The NE555 loses about 1.7V. For 3.3V logic, the TLC555 is the better choice.

## Common Uses

| Application | Mode | Why the 555 works well |
|-------------|------|------------------------|
| **Debouncing a button** | Monostable | One clean ~10ms pulse per press |
| **PWM generation** | Astable | Fixed frequency, adjustable duty with diode mod |
| **Tone generation** | Astable | Square wave at audio frequencies — speaker output |
| **LED blinker** | Astable | Simple + LED + resistor |
| **Timed relay** | Monostable | Turn on a relay for X seconds |
| **Missing pulse detector** | Monostable | Detect if a pulse train stops (reset stays high) |
| **VCO** | Astable + pin 5 | Change frequency with voltage on control pin |
| **Frequency divider** | Monostable | Dividing a trigger signal by triggering repeatedly |

## Quick Reference

```
Modes:
  Astable    = continuous square wave. f = 1.44 / ((R1 + 2R2) × C)
  Monostable = one pulse. t = 1.1 × R × C
  Bistable   = latch. Trigger SET, Threshold RESET.

Pinout:
  1=GND, 2=TRIG, 3=OUT, 4=RESET,
  5=CONT, 6=THRES, 7=DISCH, 8=VCC

Always:
  - Bypass pin 5 (CONT) with 0.1µF to GND
  - Tie pin 4 (RESET) to VCC if not using it

CMOS vs Bipolar:
  TLC555: 2–16V, low power, 3.3V OK, MHz speeds
  NE555:  4.5–16V, strong output, cheap, <500kHz

Formulas:
  Astable:       f = 1.44 / ((R1 + 2R2) × C)
  Monostable:    t = 1.1 × R × C
  Duty (basic):  (R1 + R2) / (R1 + 2R2) — always >50%
```
