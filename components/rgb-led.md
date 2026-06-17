# RGB LED (Common Anode / Cathode) — Component Reference

## What It Is

An RGB LED is **three LEDs in one package** — one red, one green, one blue. By mixing them at different brightnesses, you can create any color. Unlike an addressable LED (WS2812), this is a plain LED — you control each color with a separate pin and resistor.

## Types

### Common Cathode

The **negative** side of all three LEDs is connected together (to GND). You apply positive voltage to each color pin:

```
              ┌── R ── Anode R
              │
    Cathode ──┼── G ── Anode G
    (to GND)  │
              └── B ── Anode B
```

### Common Anode

The **positive** side of all three LEDs is connected together (to VCC). You pull each color pin LOW to turn it on:

```
              ┌── R ── Cathode R
              │
    Anode ────┼── G ── Cathode G
    (to VCC)  │
              └── B ── Cathode B
```

| Type | Pinout | How to turn on | How to turn off |
|------|--------|----------------|-----------------|
| Common Cathode | Longest pin = GND | GPIO HIGH | GPIO LOW |
| Common Anode | Longest pin = VCC | GPIO LOW | GPIO HIGH |

## Pinout (Typical 5mm Through-Hole)

```
Common Cathode:                Common Anode:
    ┌──┐                          ┌──┐
   R│  │B                        R│  │B
    │  │                          │  │
    └──┘                          └──┘
     │                            │
    GND                          VCC
    (longest pin)                 (longest pin)
   G                              G
```

**Pin order varies by manufacturer.** Always check the datasheet or test with a multimeter in diode mode.

## Wiring

### Common Cathode

```
Microcontroller          RGB LED
  GPIO (PWM) ──── 220Ω ── R pin
  GPIO (PWM) ──── 220Ω ── G pin
  GPIO (PWM) ──── 220Ω ── B pin
  GND ──────────────────── Common cathode (longest pin)
```

### Common Anode

```
Microcontroller          RGB LED
  GPIO (PWM) ──── 220Ω ── R pin
  GPIO (PWM) ──── 220Ω ── G pin
  GPIO (PWM) ──── 220Ω ── B pin
  VCC ──────────────────── Common anode (longest pin)
```

**Each color needs its own resistor.** Don't use one resistor on the common pin — the current would be shared unequally and colors would be wrong.

## Resistor Values

| Supply | Red (2.0V) | Green (3.0V) | Blue (3.0V) |
|--------|-------------|---------------|--------------|
| 3.3V | 68Ω | 15Ω | 15Ω |
| 5V | 150Ω | 100Ω | 100Ω |

Calculated for ~20mA per channel. Green and blue have higher forward voltage, so they need smaller resistors for the same brightness.

For equal brightness at 5V with 220Ω resistors:

| Color | Resistor | Current |
|-------|----------|---------|
| Red | 220Ω | (5V - 2V) / 220 = 13.6mA |
| Green | 220Ω | (5V - 3V) / 220 = 9.1mA |
| Blue | 220Ω | (5V - 3V) / 220 = 9.1mA |

**Result:** The red channel will be noticeably brighter. To balance them, use different resistor values or compensate in software.

## Controlling Color

Use PWM on each pin. The color is a mix of the three duty cycles:

```cpp
// Common cathode: 0–255 = off–full brightness
analogWrite(RED_PIN, 255);   // full red
analogWrite(GREEN_PIN, 0);   // no green
analogWrite(BLUE_PIN, 0);    // no blue
// → pure red

analogWrite(RED_PIN, 255);
analogWrite(GREEN_PIN, 255);
analogWrite(BLUE_PIN, 0);
// → yellow (red + green)
```

### Common Colors

| Color | R | G | B |
|-------|---|---|---|
| Red | 255 | 0 | 0 |
| Green | 0 | 255 | 0 |
| Blue | 0 | 0 | 255 |
| Yellow | 255 | 255 | 0 |
| Cyan | 0 | 255 | 255 |
| Magenta | 255 | 0 | 255 |
| White | 255 | 255 | 255 |
| Orange | 255 | 64 | 0 |
| Purple | 170 | 0 | 255 |
| Warm white | 255 | 200 | 150 |

### Common Anode (Inverted)

For common anode, the values are inverted:

```cpp
// Common anode: 0 = full brightness, 255 = off
analogWrite(RED_PIN, 0);    // full red
analogWrite(GREEN_PIN, 255); // no green
analogWrite(BLUE_PIN, 255);  // no blue

// Or use math:
int red = 255 - 255;   // = 0 (full on)
int green = 255 - 0;   // = 255 (off)
int blue = 255 - 0;    // = 255 (off)
```

## RGB LED vs Addressable LED

| Feature | RGB LED | Addressable (WS2812) |
|---------|---------|---------------------|
| Pins needed | 3 (R, G, B + common) | 1 data pin |
| Resistors | 3 (one per color) | None needed |
| PWM channels | 3 | None (built-in driver) |
| Individual control | Use PWM | Built-in per-LED |
| Daisy chain | No | Yes (hundreds in series) |
| Cost | $0.10 | $1+ |
| Color consistency | Needs calibration | Matched per-chip |

Use an RGB LED when you need one or two indicators. Use addressable LEDs for strips or multiple LEDs.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Only one color works | Other GPIOs not PWM-capable | Check which pins support PWM on your MCU |
| Colors are wrong or dim | Common cathode vs anode mismatch | Check type and adjust code |
| One color much brighter than others | Forward voltage difference | Use different resistors per color, or software balance |
| LED heats up | No current-limiting resistors | Add 220Ω resistors to each color pin |
| Color changes when you change brightness | Insufficient PWM resolution | Use 8-bit or higher resolution PWM |

## Quick Reference

- **Common cathode:** Longest pin to GND. GPIO HIGH = on.
- **Common anode:** Longest pin to VCC. GPIO LOW = on.
- **Each color needs its own resistor** — don't share a common resistor.
- **PWM required** for mixing colors. Use hardware PWM pins.
- **Red is brighter** at the same resistor value — use larger resistor for red or balance in software.
- **Typical resistor values:** 220Ω per color at 5V, 100Ω per color at 3.3V.
- **Color mixing:** RGB values 0–255 (common cathode) or 255–0 (common anode).
- **For strips or multiple LEDs:** Use addressable LED (WS2812) instead.
