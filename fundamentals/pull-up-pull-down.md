# Pull-Up & Pull-Down Resistors — Deep Dive

## What They Do

A pull-up or pull-down resistor **keeps a digital input pin at a known voltage** when nothing else is driving it. Without one, a floating input pin picks up random electrical noise and reads random HIGH/LOW values.

> **Analogy:** A pull-up is like a spring that holds a button in the OUT position. You push the button IN (connect to ground), and when you let go, the spring (resistor) pulls it back OUT.

## Pull-Up vs Pull-Down

```
Pull-Up:                          Pull-Down:
  VCC (3.3V)                        GPIO pin
    │                                  │
   [10kΩ]                             [10kΩ]
    │                                  │
GPIO ────[Button]──── GND          GND ────[Button]──── VCC

Button released → GPIO = HIGH      Button released → GPIO = LOW
Button pressed  → GPIO = LOW       Button pressed  → GPIO = HIGH
```

| | Pull-up | Pull-down |
|--|---------|-----------|
| Default state (no press) | **HIGH** (VCC) | **LOW** (GND) |
| Active state (button pressed) | **LOW** (GND) | **HIGH** (VCC) |
| Resistor connects between | GPIO and VCC | GPIO and GND |

## Why 10kΩ Is the Default

10kΩ is the standard pull-up/down value for almost every digital input. Here's why:

| Value | Effect | Problem |
|-------|--------|---------|
| **100Ω** | Very strong pull | Wastes current (33mA at 3.3V). Can damage pin. |
| **1kΩ** | Strong pull | 3.3mA current — fine for I2C, but excessive for buttons |
| **4.7kΩ** | Moderate | Common for I2C. OK for buttons. |
| **10kΩ** | **Weak pull — standard** | **0.33mA. Low enough to save power, strong enough to fight noise.** |
| **47kΩ** | Very weak | May not overcome noise in electrically noisy environments |
| **100kΩ** | Extremely weak | Picks up noise like an antenna. Unreliable for most digital inputs. |

**Rule:** 10kΩ for general digital inputs (buttons, switches, sensor digital outputs). 4.7kΩ for I2C. 1kΩ–10kΩ for reset pins.

## Internal Pull-Up Resistors

Most microcontrollers have **internal pull-up resistors** you can enable in software. They're typically ~20kΩ–100kΩ (varies by chip).

```
ESP32:  pinMode(pin, INPUT_PULLUP);     // ~45kΩ internal pull-up
Arduino: pinMode(pin, INPUT_PULLUP);    // ~20k–50kΩ internal pull-up
```

### When to Use Internal vs External

| | Internal pull-up | External resistor |
|--|----------------|------------------|
| Strength | Weak (~20k–100kΩ) | Choose any value |
| Extra parts | None | Need resistor + wiring |
| Current limit | Very low | Higher (for stronger pull) |
| Reliability | OK for quiet signals | Better for noisy environments |
| I2C bus | **Not suitable** — needs external 4.7kΩ | Required |

**Rule:** Internal pull-up is fine for buttons and switches on a breadboard. Use external 10kΩ when reliability matters or in noisy environments.

## Pull-Up Value for Different Scenarios

### Digital Input (Button / Switch)

```
  VCC
   │
  [10kΩ]  ← Pull-up to keep GPIO HIGH when button is open
   │
GPIO ──── Button ──── GND
```

**Value:** 10kΩ. Low enough to keep the line stable. High enough to waste negligible power.

### I2C Bus (SDA / SCL)

I2C requires pull-up resistors on both SDA and SCL lines. The value depends on the bus capacitance and speed:

| Speed | Typical pull-up | Max bus length |
|-------|----------------|----------------|
| 100kHz (Standard) | 4.7kΩ | ~50cm |
| 400kHz (Fast) | 2.2kΩ–4.7kΩ | ~30cm |
| 1MHz (Fast+) | 1kΩ–2.2kΩ | ~10cm |
| Multiple devices on bus | Lower value (more capacitance) | — |

> **Rule:** Start with 4.7kΩ for I2C at 100kHz/400kHz. If the waveform looks rounded on an oscilloscope, use a lower value (2.2kΩ). 10kΩ works for short buses with 1–2 devices.

### Reset Pin

MCU reset pins usually have an **internal pull-up** (~10k–100kΩ). If you add a button to manually reset:

```
  VCC
   │
  [10kΩ]  ← External pull-up (or rely on internal)
   │
RESET ──── Button ──── GND
```

### Open-Collector / Open-Drain Output

Devices like I2C devices, comparators, and some sensors have **open-drain** outputs — they can only pull LOW, not drive HIGH. They **require** a pull-up resistor to VCC.

```
Sensor (open-drain) ────┬──── GPIO
                        │
                       [4.7kΩ]  ← Pull-up to VCC on THAT side's voltage
                        │
                       VCC
```

## What Happens With Wrong Values

| Mistake | Result |
|---------|--------|
| No pull-up/pull-down at all | GPIO reads random values — button press seems unreliable |
| Pull-up too weak (>100kΩ) | Noise couples in — false triggers |
| Pull-up too strong (<1kΩ) | Wastes current, may exceed GPIO current rating |
| Pull-up when you needed pull-down | Logic is inverted — button reads HIGH when pressed |
| Using internal pull-up on I2C | Internal values are wrong (~50kΩ) — I2C bus fails at any distance |
| Two pull-ups on same line | Parallel resistance — lower than expected (OK for I2C, actually) |

## Quick Reference

```
Pull-up (default HIGH):
  VCC ──[10kΩ]── GPIO ──[Button]── GND
  Button open  → GPIO = HIGH (1)
  Button closed → GPIO = LOW (0)

Pull-down (default LOW):
  GPIO ──[10kΩ]── GND
  VCC ──[Button]── GPIO
  Button open  → GPIO = LOW (0)
  Button closed → GPIO = HIGH (1)

Default values:
  Buttons/switches:     10kΩ
  I2C bus (SDA/SCL):    4.7kΩ (start here)
  Reset pins:           10kΩ (or use internal)
  Internal (ESP32):     ~45kΩ INPUT_PULLUP — fine for buttons

I2C speed vs pull-up:
  100kHz  → 4.7kΩ
  400kHz  → 2.2–4.7kΩ
  1MHz    → 1–2.2kΩ

Rule: When in doubt, use 10kΩ.
```

## See Also

- [ds18b20-onewire](/projects/ds18b20-onewire)
- [i2c-devices](/projects/i2c-devices)
