# 7-Segment Display — Component Reference

## What It Is

A 7-segment display shows numbers using seven individually-controlled LEDs arranged in a pattern. Add an eighth segment for the decimal point (DP).

```
   aaaa
  f    b
  f    b
   gggg
  e    c
  e    c
   dddd   dp
```

Each segment is just an LED — it needs a current-limiting resistor and lights up when forward-biased.

## Common Anode vs Common Cathode

The big split is how the LED legs are wired internally.

### Common Anode

All LED anodes tie together to VCC. You light a segment by pulling its cathode **low** (GND).

```
   VCC ─┬──[a]─── pin
        ├──[b]─── pin
        ...
   GPIO ──── each cathode
```

**Active LOW** — write `0` to turn a segment on.

### Common Cathode

All LED cathodes tie together to GND. You light a segment by pulling its anode **high** (VCC).

```
   GND ─┬──[a]─── pin
        ├──[b]─── pin
        ...
   GPIO ──── each anode
```

**Active HIGH** — write `1` to turn a segment on.

| | Common Anode | Common Cathode |
|---|---|---|
| Common pin | VCC (+) | GND (-) |
| Turn on segment | LOW (0) | HIGH (1) |
| What you buy | Usually marked "CA" or "CC" | Usually marked "CC" or "CA" |
| Arduino library | `~segments` with `COMMON_ANODE` | Default / `COMMON_CATHODE` |

> **Gotcha:** If you hook up a common-anode display to a common-cathode library your segments will be inverted. Check the datasheet or test with a battery.

## 1-Digit vs Multi-Digit

1-digit: 10 pins (8 segments + 2 common, or 8 + 1 common). Simple, direct GPIO drive.

Multi-digit (2/4/8 digits): Fewer pins by sharing segment pins across digits. Digit commons are individually controlled.

```
   4-digit multiplexed pinout:

   DIG1 DIG2 DIG3 DIG4  (digit select pins)
     │    │    │    │
     └──┬─┴────┴────┘── segment bus
        │
      a b c d e f g dp (shared across all digits)
```

**Multiplexing:** You light one digit at a time, very fast. Persistence of vision (POV) makes them all appear lit. Cycle each digit every 1–5ms — below ~50Hz the display flickers.

## Decimal Point

The DP is segment 8. It's wired like any other segment — same forward voltage, same current limit. Treat it as a regular LED.

Common uses: voltage readings (3.14), negative sign (use segment g as minus).

## Current-Limiting Resistors

Each segment is an LED. Every segment needs its own resistor — do not share one resistor across all segments. Brightness shifts as more segments turn on.

**Typical resistor values at 5V:**

| Segment color | Forward voltage | Resistor (5V, ~10mA) |
|---|---|---|
| Red | ~2.0V | 220–330Ω |
| Green | ~2.2V | 220–270Ω |
| Blue | ~3.0–3.4V | 150–220Ω |
| Yellow | ~2.1V | 220–330Ω |

**Rule:** One resistor per segment pin, not one per digit. If using a driver IC (TM1637, MAX7219), the resistors are built in or specified by the datasheet.

## Drive Methods

### Direct Drive (GPIO)

Each segment gets one GPIO pin. Feasible for 1-digit (8 pins). A single digit uses 8 GPIOs — doable on a Uno, tight on an ESP8266.

| Digits needed | GPIOs required | Works? |
|---|---|---|
| 1 digit | 8 | Yes |
| 2 digits | 16 | Only on large boards |
| 4 digits direct | 32 | Impractical |

**Not recommended** beyond 1 digit without a driver.

### Shift Register (74HC595)

One shift register drives 8 segments. Another register controls digit select. Two 74HC595s give you 16 outputs from 3 GPIO pins (data, clock, latch).

See the [Shift Register guide](shift-register.md) for wiring.

### I2C Backpack (TM1637)

The TM1637 is a dedicated LED driver that handles multiplexing and constant current. Communicates over a 2-wire interface (like I2C but proprietary — CLK and DIO).

| | Direct GPIO | 74HC595 | TM1637 |
|---|---|---|---|
| Pins used | 8 per digit | 3 (any number of digits) | 2 |
| Max digits | 1 | Unlimited (chained) | 4 or 6 |
| Current limiting | External resistors | External resistors | Built-in |
| Code effort | Easy | Moderate | Easy (library) |
| Flicker at many digits | Yes | Depends on refresh | No (handles refresh) |

**When to use TM1637:** Quick prototypes, 4-digit displays, clock projects, when you don't want to write multiplexing code.

**Buying note:** Many "TM1637" modules come as a pre-soldered board with the display + backpack. They're labeled "4-digit 7-segment display module" and take 5V + GND + CLK + DIO.

## Multiplexing Multi-Digit Displays

Multiplexing reduces pins at the cost of lower peak brightness. Each digit is on only 1/N of the time.

**Current trade-off:** If multiplexing 4 digits, each digit is on 25% of the time. To maintain perceived brightness, you drive segments at 3–4× the DC current rating. Stay within max peak current from the datasheet (usually 40–60mA per segment in short pulses).

**Refresh sequence:**
```
1. Set segment pattern for digit 1
2. Enable digit 1 common
3. Delay ~2ms
4. Disable digit 1
5. Repeat for digits 2, 3, 4
```

**Flicker threshold:** Below 60Hz refresh rate, humans see flicker. Below 100Hz, cameras see it. Aim for 200Hz+ per digit.

## Brightness vs Current

Brightness in LEDs is roughly proportional to current. More current = brighter, but also more heat and shorter lifespan.

| Current per segment | Brightness | Risk |
|---|---|---|
| 2–5mA | Dim, indoor | Safe |
| 5–15mA | Normal indoor | Safe (typical range) |
| 15–25mA | Bright | May exceed 1/4W resistor rating |
| >30mA | Very bright | Short LED life, hot resistor |

**PWM dimming:** Use PWM on the common pin (or via the driver) to control brightness without changing resistors. Works because persistence of vision blends the on/off cycles.

## Pinout Examples

### Common Cathode 1-Digit (typical)

```
       a b c d e f g dp
       │ │ │ │ │ │ │ │
   ┌───┴─┴─┴─┴─┴─┴─┴─┴───┐
   │     DISPLAY          │
   └───┬──────────────────┘
       │
      COM (cathode → GND)
```

### 4-Digit Common Cathode

```
   DIG1 DIG2 DIG3 DIG4 | a b c d e f g dp
     │    │    │    │   │ │ │ │ │ │ │ │
     └────┴────┴────┘   └─┴─┴─┴─┴─┴─┴─┴─ segment bus
```

## Common Mistakes

| Mistake | Result |
|---|---|
| No current-limiting resistor | Blown segment, blown GPIO pin |
| One resistor on common pin | Brightness changes with digit count |
| Wrong common anode/cathode polarity | Segments inverted — all segments off |
| Multiplexing too slow | Visible flicker |
| Multiplexing too fast (no off-time) | Ghosting — adjacent digits faintly lit |
| 5V GPIO to 3.3V display | Overvoltage — may damage display |
| Exceeding peak segment current | Premature LED failure |

## Quick Reference

```
Common anode: common → VCC, segments → GPIO (LOW = on)
Common cathode: common → GND, segments → GPIO (HIGH = on)

Resistor per segment: 220Ω (red) / 150Ω (blue) at 5V

Drive options:
  1 digit → direct GPIO (8 pins)
  2+ digits → 74HC595 or TM1637
  4+ digits → TM1637 or MAX7219

Multiplexing: one digit at a time, ~2ms each, >200Hz
