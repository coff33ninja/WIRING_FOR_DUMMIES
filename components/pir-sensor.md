# PIR Motion Sensor (HC-SR501) — Component Reference

## What It Is

A PIR (Passive Infrared) sensor detects motion by sensing changes in infrared radiation — basically, it notices when a warm body (human, animal, car engine) moves across its field of view. The HC-SR501 is the most common hobby module: a pyroelectric sensor with a Fresnel lens, comparator circuit, and adjustable delay on a single board.

> **Analogy:** A security camera that only cares about differences. If the heat picture changes from one moment to the next, it raises an alarm. If everything stays the same temperature, it ignores the scene.

## How Pyroelectric Sensing Works

Inside the sensor are two slots of pyroelectric material — a crystal that generates a voltage when heated or cooled.

```
            Fresnel lens
         ╱  ╲╱  ╲╱  ╲
        │   │   │   │   │
        │   │   │   │   │
        │   │   │   │   │
        └───┴───┴───┴───┘
           ╲ ╱     ╲ ╱
            ╳       ╳        ← two sensing elements
           ╱ ╲     ╱ ╲
        ──┴───┴───┴───┴──
```

**The two slots are arranged so:**

- A stationary warm body heats both slots equally → no differential signal → no detection
- A warm body moving across the field heats one slot more than the other → differential voltage → trigger

**Why two slots:** This cancels out ambient temperature changes (the whole room warming up slowly) and only responds to moving heat sources.

## Fresnel Lens

The white plastic dome on the HC-SR501 is a Fresnel lens. It focuses infrared radiation onto the sensor elements and divides the field of view into multiple detection zones.

```
   Fresnel lens focuses multiple zones:

      Top view:
      ┌─────────────────────────┐
      │ │ │ │ │ ╳ │ │ │ │ │ │   │
      └─────────────────────────┘
              sensor
              element
```

**Why it matters:**

- Without the lens, detection range is ~1m
- With the lens, range is ~5–7m
- The lens creates alternating sensitive and blind zones — a warm body passing through a blind zone might not be detected

**Detection pattern:** The lens has ~30–50 facets. Each facet creates a detection beam. The effective detection area looks like a fan of cones emanating from the sensor.

## HC-SR501 Adjustments

The board has two potentiometers (usually blue or white blocks) and a jumper:

```
   ┌────────────────────────────────────────────┐
   │                                            │
   │  [Sensitivity]  [Time Delay]   [Trigger]   │
   │      │               │            │        │
   │      │               │            │        │
   │  ┌───┴───┐      ┌───┴───┐   ┌──┴──┐     │
   │  │  Pot  │      │  Pot  │   │Jumper│     │
   │  └───────┘      └───────┘   └─────┘     │
   │                                            │
   │         [HC-SR501]                        │
   │                                            │
   │  VCC  OUT  GND                             │
   └────────────────────────────────────────────┘
```

### Sensitivity Adjust (Range)

Controls the detection range. Full range is 5–7m (indoors). Clockwise = more sensitive (longer range, more false triggers). Counter-clockwise = less sensitive (shorter range, fewer triggers).

| Setting | Range | Best for |
|---|---|---|
| Minimum (CCW) | ~3m | Narrow hallways, pet avoidance |
| Mid | ~5m | Normal room |
| Maximum (CW) | ~7m | Open areas, but many false triggers |

**Sensitivity is physical** — it adjusts the comparator's reference voltage. If you need less range, turn it down. If you still get false triggers, also reduce the time delay or switch trigger modes.

### Time Delay Adjust (Output Hold Time)

Controls how long the output stays HIGH after motion is detected. Range is roughly 0.5s to ~200s (5 seconds fully CCW to ~3 minutes fully CW).

| Setting | Output HIGH duration |
|---|---|
| Minimum (CCW) | ~0.5s |
| Mid | ~5–10s |
| Maximum (CW) | ~200s |

**Full CCW does not mean zero delay** — there is a minimum ~0.5s built in.

### Trigger Mode Jumper

Controls what happens when motion continues.

| Jumper position | Mode | Behavior |
|---|---|---|
| **H** (Repeat / Retriggerable) | Retriggerable | Timer resets on each new detection. Output stays HIGH as long as motion continues plus the delay. |
| **L** (Single / Non-retriggerable) | Non-retriggerable | Timer runs once and ignores new motion until it expires. Output goes HIGH for the delay period, then LOW regardless of continued motion. |

| Mode | Motion stops | Motion continues |
|---|---|---|
| H (retriggerable) | Output LOW after delay | Output stays HIGH (reset timer) |
| L (non-retriggerable) | Output LOW after delay | Output goes LOW after original delay, then triggers again |

**Best uses:**

- **H mode:** Occupancy sensing (lights stay on while someone is in the room)
- **L mode:** Pulse detection (alarm trigger, notification that someone walked past)

## Pinout

```
   ┌─────────────┐
   │ HC-SR501    │
   │             │
   │  VCC  OUT  GND
   │   │    │    │
   │   │    │    │
   │   │    │    │
   └─────────────┘
```

| Pin | Connect to |
|---|---|
| VCC | 5V or 12V (HC-SR501 accepts 4.5–20V) |
| OUT | GPIO input (3.3V or 5V — output matches VCC) |
| GND | Common ground |

**Output signal:** HIGH (VCC level) when motion detected. LOW otherwise. The output is digital — no analog reading needed.

**Voltage compatibility:** HC-SR501 output voltage matches its supply. Run at 5V, output is 5V. Run at 3.3V? The datasheet says minimum supply is 4.5V — do not supply 3.3V. Use a voltage divider on OUT if your MCU is 3.3V (like ESP32, Pi). Or double the supply: feed 5V to the sensor and use a voltage divider on OUT, or use a logic-level converter.

```
   HC-SR501 OUT (5V) ─── 1kΩ ──┬── 2.2kΩ ── GND
                                │
                                └── MCU GPIO (3.3V safe)
```

## Warm-Up Time (30–60 Seconds)

When the HC-SR501 powers on, it needs 30–60 seconds to stabilize. During this time the output may trigger randomly.

**Behavior:**

| Time after power-on | Output |
|---|---|
| 0–10s | May be HIGH (self-calibration) |
| 10–30s | May toggle several times |
| 30–60s | Should settle to LOW |
| >60s | Ready — stable LOW, waiting for motion |

**In your code:** Either wait 60 seconds before reading, or discard the first 60 seconds of readings. Many tutorials skip this and wonder why their sensor triggers immediately on boot.

**Why this happens:** The pyroelectric sensor needs to reach thermal equilibrium. The internal comparator adjusts its reference as the sensor warms up. Moving air, handling the board, or soldering can extend this time.

## Limitations

### Glass and Wall Blockage

Infrared radiation does not pass through solid walls, glass windows, or most building materials. The PIR sensor will not detect motion behind:

- Glass windows (IR is blocked by glass)
- Drywall / plaster walls
- Wooden doors
- Plastic enclosures (unless IR-transparent like polyethylene)

> **If the sensor is behind a window:** It sees the glass temperature, not what's outside. The glass is essentially a mirror at thermal IR wavelengths.

### Temperature Gradients (False Triggers)

The HC-SR501 detects changes in IR. A rapid change in ambient temperature looks exactly like motion:

| Cause | Effect |
|---|---|
| HVAC kicking on | Warm/cold air moves across the sensor |
| Sunlight moving across a wall | IR edge moves, triggers sensor |
| Heater / radiator turning on | Creates thermal plume |
| Opening a door | Temperature difference triggers sensor |
| Direct sunlight on sensor | Sensor saturates — false triggers or no detection |

**Mitigation:** Mount the sensor away from HVAC vents, radiators, windows, and direct sunlight. Reduce sensitivity. Add a 10–30 second cooldown in software (ignore retriggers within that window).

### Pets

A PIR sensor cannot distinguish a human from a large pet by default. A dog or cat moving within ~2m can trigger the sensor.

**Mitigation approaches:**

| Method | How it works | Effectiveness |
|---|---|---|
| Lower sensitivity | Reduces range to ~3m | Limited — pet still triggers |
| Mount higher (2m+) | Sensors points down, pet below detection zone | Works if pets stay low |
| Pet-immune lens | Special lens that creates a "dead zone" below waist height | Best, but needs specific sensor |
| Software filter | Ignore triggers that repeat at pet-like frequency | Fragile |
| Dual-element sensor | Compare two zones — small blob triggers one zone, not both | Some sensors support this |

**Practical solution:** Mount the PIR at 1.5–2m height, angled slightly downward. The detection cone starts a few meters out, creating a "pet alley" below the sensor. Or use a dedicated pet-immune PIR (different lens).

### Other Limitations

| Issue | Problem |
|---|---|
| Temperature near body heat (~35°C) | Poor detection — low thermal contrast |
| Slow movement | May not cross detection zones fast enough |
| Very fast movement | Missed — brief transient below response time |
| Multiple people | Sensor detects motion but counts no one |
| Humidity / fog | Attenuates IR slightly (minor effect) |

## Common Mistakes

| Mistake | Result |
|---|---|
| Not waiting for warm-up | False trigger on boot — reads HIGH immediately |
| Behind glass | Never detects anything |
| Pointed at window | False triggers from passing cars / clouds |
| Near HVAC vent | False triggers every time heat turns on |
| Sensitivity maxed | Triggers on every air current |
| Trigger set to L (non-retrigger) for lights | Lights turn off while room is occupied |
| 3.3V supply to HC-SR501 | Sensor may not work (min 4.5V) |
| No voltage divider on 5V OUT to 3.3V MCU | Damaged GPIO pin |

## Quick Reference

```
Pinout:
  VCC → 5–12V (min 4.5V, max 20V)
  OUT → GPIO (digital HIGH/LOW)
  GND → common ground

Warm-up: 30–60 seconds (ignore during this time)

Adjustments:
  Sensitivity: ~3m (CCW) to ~7m (CW)
  Time delay: ~0.5s (CCW) to ~200s (CW)
  Trigger mode jumper: H = retriggerable, L = non-retriggerable

Output:
  HIGH → motion detected (duration = time delay setting)
  LOW → no motion

Limitations:
  Cannot see through glass, walls, doors
  False triggers from HVAC, sunlight, heaters
  Pets can trigger within ~2m
  Needs thermal contrast (detects ΔT ~0.5–1°C)

3.3V MCU fix:
  Power PIR at 5V
  OUT ── 1kΩ ──┬── 2.2kΩ ── GND
                └── GPIO
```
