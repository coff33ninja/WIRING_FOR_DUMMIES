# LED — Component Reference

## What It Is

LED stands for **Light Emitting Diode**. It's a diode that happens to emit light when current flows through it. Everything in the [diode reference](diode.md) applies — it's a one-way valve, just one that glows.

## Polarity — Which Leg Is Which

```
         ┌─────┐
         │     │
    (+)  │     │  (−)
    ─────┤     ├─────
    LONG  │     │  SHORT
    LEG   │     │  LEG
         │     │
         └─────┘
         FLAT SIDE
         (notch on rim)
```

| Feature | Anode (+) | Cathode (−) |
|---------|-----------|-------------|
| Leg length | **Longer leg** | Shorter leg |
| Plastic rim | Round side | **Flat notch** |
| Inside the LED | Smaller piece | Larger piece |

> **Note:** If you've already cut the legs (common with salvage or bulk parts), the flat notch on the rim is your only clue. And if the rim is perfectly round too, check with a multimeter or just try both ways — it won't break from being backwards for a second.

## Why You Need a Current-Limiting Resistor

An LED doesn't have internal resistance — it's basically a short circuit once it turns on. If you connect it directly to 3.3V, it will try to draw as much current as the power supply can deliver. This:

1. Melts the LED (it turns blue/white briefly, then dark = dead)
2. Can also kill the GPIO pin on your microcontroller

### The Formula

```
R = (Vsupply - Vled) / Iled

For a typical LED:
  Vsupply = 3.3V (ESP32 GPIO)
  Vled    = 2.0V (red LED forward voltage)
  Iled    = 0.01A (10mA — bright enough)

  R = (3.3 - 2.0) / 0.01 = 130Ω → use 220Ω (safe standard value)
```

### Rule of Thumb

| Supply | Resistor Value |
|--------|---------------|
| 3.3V GPIO | 220Ω (standard) |
| 5V GPIO | 470Ω |
| 12V (e.g., indicator lamp) | 1kΩ |

## Color and Forward Voltage

Different colors have different voltage drops:

| Color | Forward voltage (Vf) | Typical brightness at 10mA |
|-------|---------------------|----------------------------|
| Red | ~1.8–2.0V | Medium |
| Yellow | ~1.9–2.1V | Medium |
| Green | ~2.0–2.4V | Medium |
| Blue | ~3.0–3.3V | Bright |
| White | ~3.0–3.4V | Very bright |
| RGB (common cathode) | 2.0/3.0/3.0V | Bright |

> **Fun fact:** Blue and white LEDs need so much voltage they won't fully light up from 3.3V. They still work, just dimmer. Use 5V for full brightness on blue/white.

## Wiring

```
GPIO pin ──── 220Ω ────┬── LED (+) (ANODE, long leg)
                        │
GND      ──────────────┴── LED (−) (CATHODE, short leg)
```

The resistor can go on either side of the LED — before or after. It doesn't matter. Same current flows through the whole loop.

## What Happens If You Skip the Resistor

| Scenario | Result |
|----------|--------|
| 3.3V + LED + no resistor | LED flashes bright once, then dead. GPIO pin may survive. |
| 5V + LED + no resistor | LED dead instantly. GPIO pin can also die. |
| 12V + LED + no resistor | LED explodes (seriously — it can crack open). GPIO pin very dead. |

## Common Types

| Type | Looks like | Use |
|------|------------|-----|
| Through-hole (5mm) | Standard round dome, 2 legs | Panel indicators, status LEDs |
| Through-hole (3mm) | Smaller dome | Compact builds |
| SMD 0805/0603 | Tiny rectangle, no legs | PCB designs |
| RGB LED | 4 legs (common cathode or anode) | Color-changing indicators |
| Diffused | Cloudy plastic, even light | Status lights you stare at |
| Clear | Transparent plastic, focused beam | Indicators, flashlight-like |

## Quick Reference

```
Physical identification:
  Long leg  = Anode (+) → goes toward GPIO (through resistor)
  Short leg = Cathode (−) → goes toward GND
  Flat notch = Cathode side

Standard resistor:
  3.3V → 220Ω
  5V   → 470Ω

If it doesn't light:
  1. Check orientation (try flipping)
  2. Check resistor value (not 10kΩ?)
  3. Check GPIO is actually HIGH
  4. Multimeter: measure voltage across LED legs
```
