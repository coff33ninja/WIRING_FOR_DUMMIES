# Switch / Button — Component Reference

## What It Is

A switch is a **mechanical way to make or break a connection**. Press a button — electrons flow. Let go — they stop. Simple, but the details matter a lot in practice.

> **Analogy:** A switch is like a drawbridge. When it's down (closed), traffic (electrons) flows across. When it's up (open), nothing gets through. A momentary switch is a drawbridge that springs back up the second you stop holding it down.

## Momentary vs Latching

| Type | Stays in position? | Example | Use case |
|------|-------------------|---------|----------|
| **Momentary** (push button) | No — springs back when released | Tactile switch, doorbell | User input — "press to trigger" |
| **Latching / toggle** (switch) | Yes — stays in position | Light switch, SPDT toggle | Mode selection — "set and forget" |

## Tactile Switch (The Most Common)

The small 4-pin square buttons on breadboards:

```
Top view:                  Side view:
┌─────────┐                ┌────┐
│    ●    │                │    │
│         │           ─────┤    ├────  ← Press down
└──┬──┬──┘                │    │
   │  │                    └────┘
  ══╧══╧══  ← 4 pins     ═══╧══╧══  ← 4 pins (connected in pairs)
```

**Pinout:** The 4 pins are connected in pairs — pins on the same side are connected internally. You only need one pin from each side.

```
Internal connection:
  1 ──╮        ╭── 2
      │        │
      │  ═══   │   ← Press connects both pairs
      │        │
  3 ──╯        ╰── 4
  
  (1+3 are connected, 2+4 are connected — normally open between the pairs)
```

**Pull-up/pull-down required:** A tactile switch doesn't have a defined voltage when open. The pin "floats." You must add a pull-up or pull-down resistor.

## Wiring a Tactile Switch (Pull-Down)

```
ESP32               Tactile Switch
─────               ──────────────
3.3V ──────────────── Pin 1 (top-left)
                     Pin 2 (top-right)
GPIO ──────────────── Pin 3 (bottom-left)
                     │
GND ──[10kΩ]──────── Pin 4 (bottom-right)
```

When pressed: GPIO reads HIGH. When released: pull-down keeps it LOW.

## Wiring a Tactile Switch (Pull-Up — Preferred)

```
ESP32               Tactile Switch
─────               ──────────────
                    Pin 1 (top-left)
GPIO ───┬─────────── Pin 2 (top-right)
        │
      10kΩ
        │
3.3V ───┘
                    Pin 3 (bottom-left)
GND ──────────────── Pin 4 (bottom-right)
```

When pressed: GPIO reads LOW (active low). When released: pull-up keeps it HIGH.

> **Why pull-up is preferred:** Most microcontrollers have built-in pull-up resistors you can enable in software (`pinMode(pin, INPUT_PULLUP)`). No external resistor needed.

## Code (with Internal Pull-Up)

```cpp
const int buttonPin = 14;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  if (digitalRead(buttonPin) == LOW) {
    Serial.println("Button pressed");
    delay(200); // crude debounce
  }
}
```

## Debouncing — Why Buttons Glitch

When you press a mechanical button, the contacts **bounce** — they make and break contact 10–50 times over a few milliseconds before settling:

```
What you think happens:   ────────┐
                                 │
                            ─────┘

What actually happens:    ──┐ ┌─┐ ┌───┐ ┌─
                            │ │ │ │   │ │
                            └─┘ └─┘   └─┘
                            ↑  Bounce!  ↑
```

**Without debouncing:** A single press looks like 5–20 rapid presses to your code. Lights flicker, counters jump, modes toggle wildly.

### Debounce Method 1: Software (Delay)

```cpp
if (digitalRead(buttonPin) == LOW) {
  delay(50); // wait for bouncing to stop
  if (digitalRead(buttonPin) == LOW) {
    // confirmed press
  }
}
```

### Debounce Method 2: Software (Timestamp — Non-Blocking)

```cpp
unsigned long lastDebounce = 0;

void loop() {
  int reading = digitalRead(buttonPin);
  if (reading == LOW && millis() - lastDebounce > 50) {
    lastDebounce = millis();
    // confirmed press
  }
}
```

### Debounce Method 3: Hardware (RC Filter)

Add a capacitor across the switch. The capacitor charges/discharges slowly, smoothing out the bounce:

```
GPIO ───┬─── Switch ─── GND
        │
      10kΩ
        │
3.3V ───┘
        │
      100nF
        │
       GND
```

**The RC time constant (~1ms) filters out the bounce.**

## Toggle Switch (SPDT)

```
              ┌──────────────┐
              │              │
         ─────┤   ╱          │
              │  ╱           │
              │ ╱            │
              └──────────────┘
                │  │  │
                C  NO NC
```

| Pin | Name | What it does |
|-----|------|-------------|
| **C** (Common) | The moving contact | Connect to GPIO |
| **NO** (Normally Open) | Connected when toggled ON | Connect to 3.3V |
| **NC** (Normally Closed) | Connected when toggled OFF | Connect to GND |

**Wiring:**
```
3.3V ────── NO
GPIO ────── C  ← reads HIGH when ON, LOW when OFF
GND  ────── NC
```

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Pull-up/pull-down resistor (tactile switch) | GPIO floats — random triggering, false readings |
| Debouncing | Multiple triggers from one press |
| Input_PULLUP mode in code (thinking it's external) | Floating input — same as no resistor |
| Using NO and NC backwards | Switch reads backwards — ON = LOW, OFF = HIGH |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| Tactile switch 6×6mm | 10 | Breadboard-friendly, cheap |
| 10kΩ resistors | 10 | Pull-up/pull-down |
| 100nF ceramic caps | 5 | Hardware debouncing |
| SPDT toggle switch | 1 | Panel-mount, for mode selection |
