# NeoPixel / WS2812B LED Strip — Wiring for Dummies

## What Is a WS2812B?

A WS2812B is a **smart LED** — it's a tiny RGB LED (red, green, blue) with a **built-in controller chip** inside the same package. Each LED can display any of ~16 million colors, and you can chain hundreds of them on a **single wire** for data.

> **Analogy:** Each LED is like a post office box with its own mailbox number. The microcontroller sends a long letter addressed to everyone in order: "Box 1: set red to 50%, Box 2: set green to 100%..." Each LED reads its part of the letter and forwards the rest down the line.

**Common brands:** NeoPixel (Adafruit), WS2812B (generic), WS2811 (external driver chip), SK6812 (similar, sometimes more efficient).

## The 4 Pins

```
           ┌────────────┐
           │  WS2812B   │  ← Clear square with black dot inside
           │   ○        │
           └────────────┘
              │  │  │  │
              │  │  │  └── DOUT (Data Out) → goes to next LED
              │  │  └───── DIN (Data In) ← comes from microcontroller
              │  └──────── VCC (5V, some run at 3.3–5V)
              └─────────── GND
```

> **For LED strips** (the flexible PCB with LEDs on it), there are usually 3 wires and 3 pads:
> - **Red wire / +5V pad** = Power (VCC)
> - **White wire / GND pad** = Ground
> - **Green wire / DIN pad** = Data In
> - **DOUT** = pads at the other end to chain to next strip

### What Each Pin Does

| Pin | Name | Think of it as... |
|-----|------|-------------------|
| **VCC** | Power (usually 5V) | Feeds the LED and its tiny brain. Needs 5V for full brightness |
| **GND** | Ground | Completes the circuit |
| **DIN** | Data In | The **"mail slot"** — receives color commands from the microcontroller |
| **DOUT** | Data Out | The **"outgoing mail"** — passes remaining commands to the next LED |

## The Big Capacitor — Why You Need It

When a whole strip of LEDs changes color at once (especially all-white at full brightness), the current draw can **spike instantly** from 0 to several amps. The power supply can't react that fast. Without a capacitor:

- The voltage dips → the LEDs flicker
- The ESP32 or microcontroller resets from the brownout
- The data signal gets corrupted → LEDs show wrong colors

> **What happens if you skip it:** You'll see random flickering, glitched colors, or your microcontroller keeps restarting every time you turn the LEDs bright white.

**Add a 470–1000µF electrolytic capacitor** across the power input at the start of the strip.

## Level Shifting — The 5V Problem

WS2812B LEDs **expect a 5V data signal**. An ESP32 outputs **3.3V** on its GPIO pins. This 1.7V difference causes problems:

- The LEDs might interpret 3.3V as a "maybe" instead of a clear "HIGH"
- The data signal degrades over longer wires (more than ~20cm)
- You get random wrong colors, especially on the first few LEDs

### Option 1: Use a Level Shifter (Recommended)

> **Full component reference:** See [Level Shifter](../components/level-shifter.md) for 74AHCT125 vs BSS138 modules, unidirectional vs bidirectional, and when to use each.

```
ESP32 3.3V                   74AHCT125 level shifter         WS2812B strip
─────────────────            ───────────────────────         ────────────
GPIO ────────────────→ OE (active LOW — connect to GND)
                    ──→ 1A (input) ─→ 1Y (output) ───────── DIN
5V ────────────────── VCC
3.3V ──────────────── VCCB or VCCA (depends on chip)
GND ───────────────── GND                              ──── GND

5V supply:
+5V ───────────────────────────────────────────────────── VCC
GND ────────────────── GND                              ──── GND
```

The 74AHCT125 converts 3.3V logic to 5V logic. It's a cheap, tiny chip (usually in a 14-pin DIP package).

### Option 2: The "It Usually Works" Direct Connection

Many people run WS2812B strips directly from ESP32 GPIO with no level shifter. It works... most of the time. If you get glitchy first-LED behavior, add the level shifter. If the wire is under 10cm and works, you're fine.

### Option 3: Use a 5V Microcontroller Pin

Some ESP32 boards have a **5V-tolerant** pin or you can use an Arduino Uno's 5V GPIO. Check your board's specs first.

## Power — How Big of a Supply?

Each WS2812B LED draws:

| Color | Current per LED | For 100 LEDs |
|-------|----------------|--------------|
| Off | 0mA | 0A |
| One color (dim) | ~5mA | 0.5A |
| Full white (max brightness) | ~60mA | **6A** |

> **6 amps for 100 LEDs at full white.** That's a lot. Most USB supplies can't do that. Use a proper 5V 10A supply for big strips.

### Power Injection

For strips longer than ~50 LEDs, the voltage drops along the thin copper traces. The LEDs at the far end are dimmer and may show wrong colors.

**Solution:** Inject power at multiple points — every 50–100 LEDs.

```
         5V supply (10A)
               │
     ┌─────────┼─────────┐
     │         │         │
   [50 LEDs] [50 LEDs] [50 LEDs]
     │         │         │
     └─────────┼─────────┘
               │
              GND
```

```
── DIN: From microcontroller through all LEDs, daisy-chained
── +5V and GND: Thick wires, injected every 50 LEDs
```

## Chaining Multiple Strips

Every WS2812B LED has a **DIN** and **DOUT** pin. You connect:

```
Microcontroller → DIN of LED #1 → DOUT to DIN of LED #2 → DOUT to DIN of LED #3 ...
```

The data passes through each LED. LED #1 reads the first 24 bits (its color), then sends the rest to LED #2, and so on.

> **The order matters:** The first LED in the chain is the first LED in your code. If you wire DOUT to the wrong end, your "first" LED is at the physical end of the strip.

### Wiring a Long Chain with Power Injection

```
5V 10A Supply
 │         │         │         │
 +5V ──────┼─────────┼─────────┼─────  (+5V rail along strip)
 GND ──────┼─────────┼─────────┼─────  (GND rail)
           │         │         │
 ┌─────────┘         │         └────────┐
 │          ┌────────┘        ┌─────────┘
 │          │                 │
[1-50]    [51-100]         [101-150]
 │          │                 │
 D──────────D─────────────────D──────────→ Data continues
```

## Wiring Diagram (Simplified)

```
ESP32
─────
            Level shifter (optional but recommended)
GPIO ──────┬─ 1A ──→ 1Y ───┐
3.3V ──────┤ VCCB           │
5V   ──────┘ VCCA           │
GND  ─────── GND            │
                             │
              ┌──────────────┘
              │
         WS2812B Strip
         ─────────────
DIN ──────┘
VCC ──────┬──── [+5V from supply through capacitor]
GND ──────┴──── [GND from supply]
              │
           [470–1000µF
            electrolytic]
              │
5V Supply:
+5V ──────────┘
GND ────────── GND bus
```

## Data Timing (Why It's Tricky)

The WS2812B data protocol is **timing-sensitive**. Each bit is encoded by how long the signal stays HIGH vs LOW:

```
Bit = 1:  HIGH 0.8µs, LOW 0.45µs
Bit = 0:  HIGH 0.4µs, LOW 0.85µs
Reset:    LOW >50µs (marks the end of a frame)
```

If you use **bit-banging** (manually toggling the GPIO in code), the timing might be off if your code does anything else (WiFi, Bluetooth, delay() calls).

> **Solution:** Most WS2812B libraries use RMT (ESP32) or SPI (Arduino) hardware peripherals that handle the timing automatically. Use the Adafruit NeoPixel library, FastLED, or the ESP32's built-in RMT driver.

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| 470–1000µF capacitor | Flickering, glitches, ESP32 resets on all-white |
| Level shifter | First few LEDs glitch or show wrong colors |
| Power injection (long strips) | LEDs at end are dim, colors are wrong |
| Adequate power supply | Brownouts, flickering, ESP32 resets |
| Common ground between ESP32 and strip | LEDs don't work at all |
| Resistor on data line (optional) | Signal reflections on long wires → glitches |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| WS2812B LED strip (1m, 30/60/144 LEDs/m) | 1 | 5V, RGB |
| OR: Individual WS2812B LEDs | 10+ | For custom layouts |
| 470–1000µF 16V electrolytic cap | 1 | Power decoupling — critical |
| 5V power supply (2A for 30 LEDs, 10A for 144+) | 1 | Match your LED count × 60mA |
| 74AHCT125 level shifter | 1 | 3.3V → 5V data conversion |
| Jumper wires | 1 set | M-F, F-F |
| 18 AWG wire (for power injection) | ~5m | Thicker than jumper wire for high current |
| Screw terminals | 4+ | For power connections |

## See Also

- [pwm](/fundamentals/pwm)
- [level-shifter](/fundamentals/level-shifter)
- [multimeter](/fundamentals/multimeter)
- [soldering](/fundamentals/soldering)
- [power-batteries](/fundamentals/power-batteries)
