# Rotary Encoder — Position / Menu Knob

## What It Is

A rotary encoder is a **knob that turns indefinitely** and tells you which direction it's turning. Unlike a potentiometer (which has a fixed range), you can spin an encoder forever — it's like a volume knob that never hits a stop.

> **Analogy:** Think of it as the scroll wheel on a mouse. You can scroll up or down forever, and the computer knows how much and which direction.

## Two Types

| Type | What it outputs | Use for |
|------|----------------|---------|
| **Incremental (quadrature)** | Two square wave signals (A and B) phase-shifted by 90° | **Most common** — menu navigation, volume, position |
| **Absolute** | Specific position value on each step | Less common — remembers position after power loss |

Incremental encoders are what you'll find in hobby kits (like the KY-040 module).

## How Quadrature Output Works

An incremental encoder has two output pins: **CLK (A)** and **DT (B)**. As the knob turns:

```
Clockwise:                       Counter-clockwise:
  CLK: ┌─┐ ┌─┐ ┌─┐ ┌─┐           CLK: ┌─┐ ┌─┐ ┌─┐ ┌─┐
       ┘ └─┘ └─┘ └─┘ └─                ┘ └─┘ └─┘ └─┘ └─
  DT:  ┌─┐   ┌─┐   ┌─┐           DT:  ┌──┐ ┌──┐ ┌──┐ ┌──
       ┘ └───┘ └───┘ └───             ┘  └──┘  └──┘  └──
  DT leads CLK                      CLK leads DT
```

When turning **clockwise**, DT goes HIGH before CLK. When turning **counter-clockwise**, CLK goes HIGH before DT. The microcontroller reads both signals and checks the order to determine direction.

## Pinout (KY-040 Module)

The common KY-040 rotary encoder module has 5 pins:

```
  ┌──────────────────────┐
  │  KY-040              │
  │                      │
  │  CLK  DT  SW  +  GND│
  └──────────────────────┘
   │     │   │   │   │
   │     │   │   │   └──── GND
   │     │   │   └──────── VCC (3.3V)
   │     │   └──────────── Button (push-to-click, switch to GND)
   │     └──────────────── DT (data pin B)
   └────────────────────── CLK (clock pin A)
```

| Pin | Label | Connect to |
|-----|-------|-----------|
| CLK | Clock / A | GPIO (with pull-up) |
| DT | Data / B | GPIO (with pull-up) |
| SW | Switch / Button | GPIO (with pull-up) — optional |
| + | VCC | 3.3V |
| GND | GND | GND |

## Wiring

The encoder has **internal mechanical switches** that connect CLK and DT to GND when the contacts close. You need **pull-up resistors** (or use internal INPUT_PULLUP).

```
Using internal pull-ups (simplest):
  CLK ──── GPIO 32  (pinMode(32, INPUT_PULLUP))
  DT  ──── GPIO 33  (pinMode(33, INPUT_PULLUP))
  SW  ──── GPIO 25  (pinMode(25, INPUT_PULLUP))
  VCC ──── 3.3V
  GND ──── GND
```

```
Using external 10kΩ pull-ups (for noisy environments):
  3.3V
    │
   [10kΩ]    [10kΩ]    [10kΩ]
    │         │         │
  CLK ────── DT ────── SW ───── GND (through encoder)
    │
  GPIO 32
```

> **KY-040 modules already have pull-up resistors on the board.** If using a bare encoder (no PCB), add 10kΩ pull-ups from CLK to VCC and DT to VCC.

## Code

### Reading Position (Polling)

```cpp
#define CLK 32
#define DT 33
#define SW 25

int lastClk = HIGH;
int counter = 0;

void setup() {
  Serial.begin(115200);
  pinMode(CLK, INPUT_PULLUP);
  pinMode(DT, INPUT_PULLUP);
  pinMode(SW, INPUT_PULLUP);
  lastClk = digitalRead(CLK);
}

void loop() {
  int clk = digitalRead(CLK);
  if (clk != lastClk) {          // State change detected
    if (digitalRead(DT) != clk) {
      counter++;                 // Clockwise
    } else {
      counter--;                 // Counter-clockwise
    }
    Serial.println(counter);
    lastClk = clk;
  }

  if (digitalRead(SW) == LOW) {  // Button pressed
    Serial.println("Button pressed!");
    delay(200);                  // Simple debounce
  }
}
```

### Reading Position (Interrupt-Based — Better)

For reliable reading without timing issues (especially with WiFi active), use interrupts:

```cpp
volatile int counter = 0;

void IRAM_ATTR readEncoder() {
  if (digitalRead(DT) != digitalRead(CLK)) {
    counter++;
  } else {
    counter--;
  }
}

void setup() {
  pinMode(CLK, INPUT_PULLUP);
  pinMode(DT, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(CLK), readEncoder, FALLING);
  Serial.begin(115200);
}

void loop() {
  Serial.println(counter);
  delay(100);
}
```

## Debouncing

Rotary encoders are mechanical switches — they **bounce**. Each detent (click) generates multiple transitions. Without debouncing, a single click might register 3–5 steps.

### Hardware Debouncing

Add a **small capacitor (100nF)** between each encoder pin and GND:

```
CLK ──┬── GPIO
      │
    100nF
      │
     GND

DT ──┬── GPIO
     │
   100nF
     │
    GND
```

### Software Debouncing

Add a minimum time between accepted state changes:

```cpp
void loop() {
  static unsigned long lastTurn = 0;
  int clk = digitalRead(CLK);

  if (clk != lastClk && millis() - lastTurn > 2) {  // 2ms debounce
    if (digitalRead(DT) != clk) {
      counter++;
    } else {
      counter--;
    }
    lastTurn = millis();
    lastClk = clk;
  }
}
```

## What Happens If Something Goes Wrong

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| One direction always counts up and down | Swap CLK and DT | They're assigned to the wrong pins |
| One click = 3–5 counts | Bouncing — no debounce | Add 100nF caps or software debounce |
| Random counts / noise | No pull-up resistors | Enable INPUT_PULLUP or add external 10kΩ |
| Button press registers as turn | Switch is bouncing into CLK/DT line | Add debounce caps |
| Encoder works then stops | Wires loose / jumping out of breadboard | Use shorter leads or secure with tape |
| Count drifts when not touching it | Electrical noise on long wires | Use shielded wire or lower pull-up value |

## Quick Reference

```
Rotary encoder (KY-040 module):
  CLK ── GPIO (with pull-up)
  DT  ── GPIO (with pull-up)
  SW  ── GPIO (with pull-up)
  VCC ── 3.3V
  GND ── GND

Code pattern (polling):
  Detect CLK state change
  Compare DT to CLK → direction
  Count up (CW) or down (CCW)

Debouncing:
  Required — mechanical contacts bounce
  Hardware: 100nF cap from CLK to GND and DT to GND
  Software: ignore transitions within 2ms of last one

KY-040 modules have built-in pull-ups on the PCB.
Bare encoders need external 10kΩ pull-ups on CLK and DT.

Always test direction by turning — swap CLK/DT in code if reversed.
```
