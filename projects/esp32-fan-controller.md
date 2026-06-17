# ESP32 Fan Controller — Wiring for Dummies

This explains *why* every wire and part is there, not just where it goes.

> **New to components?** See the [Component References](../README.md) for standalone explanations of diodes, resistors, capacitors, MOSFETs, and LEDs — what they do and how to identify them physically.

---

## 1. The Fan Wires — Which is Which?

A 3-wire computer fan has three colors:

| Wire  | Purpose | Why |
|-------|---------|-----|
| Red   | +12V power | The motor needs 12V to spin |
| Black | Ground (0V) | Completes the circuit back to the power supply |
| Yellow | Tachometer (RPM signal) | Tells the ESP32 how fast the fan is spinning (optional but nice) |

The yellow wire is **optional**. If you don't need RPM readings, just leave it disconnected.

---

## 2. The MOSFET (IRF3205) — The Electronic Switch

> **Full component reference:** See [MOSFET Reference](../components/mosfet.md) for N-channel vs P-channel, logic-level differences, and pinout gotchas.

### What is it?

A MOSFET is a **transistor that acts like a light switch**, controlled by voltage instead of your finger. The ESP32 (3.3V signal) cannot directly power a 12V fan, so the MOSFET acts as a middleman.

### The 3 Pins

Looking at the flat face with text:

```
       IRF3205
    ____________
   |            |
   |  IRF3205   |
   |____________|

      |  |  |
      G  D  S
```

| Pin    | Name     | Think of it as... |
|--------|----------|-------------------|
| **G**  | Gate     | The "switch handle" — ESP32 sends voltage here to turn the fan on |
| **D**  | Drain    | Input side — connects to the fan's negative wire |
| **S**  | Source   | Output side — connects to ground |

### How it works

- ESP32 puts **3.3V on Gate** → MOSFET opens → current flows Drain→Source → **Fan ON**
- ESP32 puts **0V on Gate** → MOSFET closes → no current flows → **Fan OFF**
- The 220Ω resistor + 10kΩ pull-down on the Gate prevent noise from accidentally turning the fan on

> **Pull-down resistor (10kΩ from Gate to GND):** When the ESP32 boots up, its GPIO pins float at random voltages for a split second. The 10kΩ resistor "pulls" the gate firmly to 0V so the fan stays OFF until the ESP32 is ready.

---

## 3. The Flyback Diode (1N4007 or 1N4148) — Protecting the MOSFET

> **Full component reference:** See [Diode Reference](../components/diode.md) for anode/cathode identification, types (rectifier vs Schottky vs Zener), and reverse polarity protection.

### What is a diode?

A diode is a **one-way valve for electricity**. Current flows one way but not the other.

### Cathode vs Anode

```
     ---+---|<|---+---
         |       |
       Anode   Cathode
       (striped end)
```

| Term    | Meaning | On the part |
|---------|---------|-------------|
| **Anode**  | Where current enters | No stripe |
| **Cathode** | Where current exits | Silver/black **stripe** |

The stripe end is the **cathode**.

### Why you need it

> **Full component reference:** See [Inductor Reference](../components/inductor.md) for why coils create voltage spikes, buck converter inductors, and ferrite beads.

Fans contain coils of wire (inductors). When you turn the fan OFF, those coils create a voltage spike in the opposite direction — this is called **inductive kick** or **flyback**. Without the diode, this spike punches through and slowly destroys the MOSFET.

### Where it goes

```
    12V+ -----+---- Fan Red
              |
             [FAN]
              |
         Fan Black ----+---- Drain (MOSFET)
              |         |
              |    [1N4007]
              |    Cathode (stripe) → 12V+
              |    Anode → Fan Black
              |
            GND
```

The diode gives that voltage spike a safe path to circulate until it dies down.

Easy rule: **Stripe end goes toward +12V.**

---

## 4. The Tachometer (Yellow Wire) — Reading RPM

### Why a pull-up resistor?

The fan's yellow wire uses an **open-collector** output. This means the fan can only pull the signal **to ground**, it cannot push it **to 3.3V**. The 10kΩ resistor "pulls" the signal up to 3.3V when the fan isn't pulling it down.

Without the pull-up, the GPIO pin would float randomly and you'd get garbage RPM readings.

```
    3.3V
      |
     10kΩ
      |
GPIO27 ---- Yellow Fan Wire
```

The fan pulls GPIO27 to ground 2 times per revolution. The ESP32's interrupt counts these pulses and calculates RPM.

### RPM Formula
```
RPM = (pulse_count × 60 seconds) ÷ 2 pulses per revolution
```

Example: 100 pulses in 1 second = (100 × 60) ÷ 2 = **3000 RPM**

---

## 5. The DHT22 Pull-Up Resistor

The DHT22 uses an open-drain protocol similar to the fan tach. The data line needs a 4.7–10kΩ resistor from DATA to 3.3V to work reliably.

Many DHT22 modules (breakout boards) already have this resistor on the PCB. If you bought a bare sensor with 4 pins, you need to add one.

```
    3.3V
      |
     4.7kΩ
      |
GPIO4 ---- DHT22 DATA
             DHT22 VCC → 3.3V
             DHT22 GND → GND
```

---

## 6. Power Supply — Ground Connection

**CRITICAL:** The ESP32's ground and the 12V supply's ground **must be connected together**.

Think of voltage as height on a hill. "12V" only has meaning relative to "0V" (ground). If the two systems don't share a ground, the MOSFET Gate voltage has no reference point and won't switch properly.

```
    12V Supply         ESP32
    ──────────         ──────
    +12V ────────────── Fan Red and MOSFET Drain circuit
    GND  ─────┬──────── ESP32 GND
               │
               └──────── MOSFET Source
```

---

## 7. Hysteresis — Preventing Rapid On/Off Cycling

Without hysteresis, if the temperature sits at exactly 28°C (the turn-on point), the fan would:
1. Turn ON → temp drops slightly to 27.9°C
2. Turn OFF → temp rises back to 28°C
3. Turn ON → repeat forever (called "oscillation")

Hysteresis adds a **dead zone**. Fan turns ON at 28°C but doesn't turn OFF until 26°C. That 2°C gap prevents rapid cycling.

```
  Fan %
  100 │                                   ┌────┐
      │                                  ╱      ╲
      │                                 ╱        ╲
      │                                ╱          ╲
      │                               ╱            ╲
    0 │  ────────────────────────────┘              └────
      └─────────────────────────────────────────────────
        26  28                   36                  45  Temp °C
        ↑   ↑                   ↑                   ↑
        off on                  mid               full
```

---

## 8. PWM — Fan Speed Control

PWM stands for **Pulse Width Modulation**. Instead of varying voltage, the ESP32 turns the MOSFET on and off very fast (25,000 times per second). The fan sees the average of on/off time:

| On time | Off time | Fan sees | Speed |
|---------|----------|----------|-------|
| 100%    | 0%       | 12V      | 100%  |
| 50%     | 50%      | 6V avg   | ~50%  |
| 25%     | 75%      | 3V avg   | ~25%  |
| 0%      | 100%     | 0V       | Off   |

Modern fans are designed for PWM and respond smoothly. 25kHz is chosen because it's above the range of human hearing (no annoying whine).

---

## 9. The Resistors — Why These Values?

> **Full component reference:** See [Resistor Reference](../components/resistor.md) for color codes, pull-up vs pull-down explained, voltage dividers, and power ratings.

| Resistor | Value   | Why |
|----------|---------|-----|
| Gate series | 220Ω | Limits current from ESP32 GPIO (protects both the pin and the MOSFET gate capacitance) |
| Gate pull-down | 10kΩ | Holds gate at 0V when ESP32 isn't driving it (prevents floating turn-on) |
| Tach pull-up | 10kΩ | Standard pull-up for 3.3V logic, keeps signal clean |
| DHT22 pull-up | 4.7k–10kΩ | Required by DHT22 datasheet for communication |
| LED resistors | 220Ω | Limits LED current to ~10mA at 3.3V |

---

## 10. Decoupling Capacitors — Noise Suppression

> **Full component reference:** See [Capacitor Reference](../components/capacitor.md) for electrolytic vs ceramic, polarity identification, voltage ratings, and what happens if you skip them.

### 100–470µF electrolytic on 12V
The fan draws bursts of current each time the PWM switches. This capacitor acts as a **small reservoir** that supplies instantaneous current, preventing voltage dips on the 12V line.

**Orientation:** Electrolytic caps have polarity. The side marked with a stripe or "-" goes to ground. The longer leg is positive (+).

### 100nF ceramic on ESP32 VCC/GND
Ceramic capacitors filter out high-frequency noise. Put this as **close as possible** to the ESP32's power pins. Ceramic caps have no polarity — either way works.

---

## 11. The 1A Fuse/PTC

> **Full component reference:** See [Fuse Reference](../components/fuse.md) for how fuses work, types (glass, blade, PTC), selection, and wiring.

A resettable PTC (Positive Temperature Coefficient) fuse on the 12V line protects against:
- A jammed fan drawing too much current
- A short circuit in the wiring
- A failed MOSFET

If it trips, let it cool for a few seconds — it resets automatically.

---

## 12. Status LEDs — What Each Color Means

> **Full component reference:** See [LED Reference](../components/led.md) for leg identification, resistor selection, and forward voltage by color.

```
Green  ─── Everything is fine, fan < 50%
Yellow ─── Getting warm, fan running at 50–100%
Red    ─── PROBLEM: fan stalled or broken!
```

Each LED has its **anode (long leg, +)** connected to the GPIO pin and its **cathode (short leg, −)** connected through a 220Ω resistor to ground.

To identify polarity:
- **Long leg** = Anode (+)
- **Short leg** = Cathode (−)
- OR: Flat notch on the plastic rim = Cathode side

---

## Quick Reference: Pin Identification

### IRF3205 (looking at flat side with text)
```
  Left   = Gate
  Middle = Drain
  Right  = Source
```

### 1N4007 Diode
```
  No stripe  = Anode (current enters)
  Silver stripe = Cathode (current exits)
```

### Electrolytic Capacitor
```
  Long leg  = +
  Short leg = −
  Stripe on body = −
```

### LED
```
  Long leg  = Anode (+)
  Short leg = Cathode (−)
  Flat notch on rim = Cathode side
```

### Fan Wires
```
  Red    = +12V
  Black  = Ground
  Yellow = Tachometer signal
```

---

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| ESP32 dev board | 1 | Any 30-pin variant |
| IRF3205 | 1 | Or logic-level: IRLZ44N / IRLB8743 |
| 12V 40mm fan | 1 | 3-wire preferred (for RPM) |
| DHT22 | 1 | AM2302 equivalent |
| 1N4007 diode | 1 | Any 1A rectifier diode |
| 220Ω resistor | 3 | Gate + 2 spare for LEDs |
| 10kΩ resistor | 3 | Gate pull-down, tach pull-up, DHT22 pull-up |
| 4.7kΩ resistor | 1 | Alternative for DHT22 pull-up |
| 100µF 25V electrolytic | 1 | 12V decoupling |
| 100nF ceramic | 1 | ESP32 decoupling |
| 1A PTC resettable fuse | 1 | Optional but recommended |
| Green LED | 1 | Status OK |
| Yellow LED | 1 | Status warm |
| Red LED | 1 | Status fault |
| 12V power supply | 1 | At least 1A |
| Breadboard + jumpers | 1 set | For prototyping |

## See Also

- [pwm](/fundamentals/pwm)
- [gpio-pins](/fundamentals/gpio-pins)
- [wireless_technologies](/fundamentals/wireless_technologies)
- [soldering](/fundamentals/soldering)
- [multimeter](/fundamentals/multimeter)
- [power-batteries](/fundamentals/power-batteries)
