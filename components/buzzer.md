# Buzzer — Component Reference

> **See also:** [Piezo Element](piezo-element.md) — bare piezo discs, useful as knock sensors or ultrasonic transceivers.

## What It Is

A buzzer is an **electromechanical or piezoelectric component that makes noise**. Feed it power and it beeps — no DAC, no audio amplifier, no programming library required.

> **Analogy:** A buzzer is the digital equivalent of shouting. It has one volume (loud) and one message ("I am here"). It's not a speaker — it's an attention-seeking device.

## Active vs Passive Buzzers

This is the most common point of confusion:

| Type | Active | Passive |
|------|--------|---------|
| Has internal oscillator | Yes | No |
| Makes sound with | DC power (just apply voltage) | PWM signal (square wave) |
| Tone control | Single fixed tone (annoying) | Any frequency you program |
| Pins | 2 (VCC, GND) | 2 (signal, GND) |
| Looks like | Closed housing (no PCB visible) | Open housing (PCB + coil visible) |

> **Active buzzer:** Apply 3.3V/5V and it screams. You cannot change the pitch. Best for alerts, alarms, error indicators.
>
> **Passive buzzer:** Send a PWM signal at different frequencies. You can play melodies, beeps, and even crude tunes. Best for musical feedback, UI sounds.

## Pinout

```
Active Buzzer                       Passive Buzzer
┌──────────┐                       ┌──────────┐
│   _____  │                       │   ░░░░  │ ← PCB visible inside
│  (●)     │                       │  (●)     │
└────┬──┬──┘                       └────┬──┬──┘
     │  │                               │  │
     +  -                              +  -
   (longer)                         (longer)
```

| Pin | Marking | Note |
|-----|---------|------|
| **+** (longer) | VCC / Anode | 3.3V–5V (check rating) |
| **–** (shorter) | GND / Cathode | Ground |

> Many buzzers are **polarized** — the longer leg is positive. Reversing polarity won't damage it but it won't make sound.

## Wiring an Active Buzzer (Simple On/Off)

```
ESP32              Active Buzzer
─────              ─────────────
GPIO ─────────────── (+) (long leg)
GND  ─────────────── (–) (short leg)
```

**Code:**
```cpp
const int buzzerPin = 12;
void setup() {
  pinMode(buzzerPin, OUTPUT);
}
void loop() {
  digitalWrite(buzzerPin, HIGH);  // SCREEEEECH
  delay(1000);
  digitalWrite(buzzerPin, LOW);   // Silence
  delay(1000);
}
```

## Wiring a Passive Buzzer (PWM — Any Tone)

```
ESP32              Passive Buzzer
─────              ──────────────
GPIO (PWM) ───────── (+) (long leg)
GND  ─────────────── (–) (short leg)
```

**Code (Arduino tone()):**
```cpp
const int buzzerPin = 12;
void setup() {
  pinMode(buzzerPin, OUTPUT);
}
void loop() {
  tone(buzzerPin, 1000);  // 1kHz beep
  delay(500);
  noTone(buzzerPin);       // Silent
  delay(500);
}
```

**Common frequencies:**
| Note | Frequency |
|------|-----------|
| Low rumble | 100–200 Hz |
| Standard beep | 1000 Hz (1kHz) |
| High alert | 2000–4000 Hz |
| Annoying | 8000 Hz (don't) |

## Driving a Buzzer Through a Transistor

Some buzzers draw more current than a GPIO can supply (especially larger panel-mount buzzers). Use an NPN transistor:

```
ESP32              NPN (2N2222)          Buzzer
─────              ────────────          ──────
GPIO ──[1kΩ]────── Base
                   Collector ──────────── (–)
                   Emitter ─── GND
                                        (+) ──── 5V (external supply)
                                      GND ───── GND (shared)
```

## Wiring a Buzzer to a Relay Module

A buzzer can be wired to the **NC (normally closed)** contact of a relay module to sound when the relay is OFF (alarm when power fails):

```
Relay Module         Buzzer
─────────────        ──────
COM ───────────────── (+) 5V
NC  ───────────────── (–) via GND path
```

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Confusing active vs passive | Active buzzer works with DC; passive stays silent without PWM |
| No current-limiting resistor (active buzzer) | Most active buzzers have built-in drive — no resistor needed |
| Reversing polarity | No sound (not damaged, just silent) |
| Driving a high-current buzzer from GPIO | GPIO pin dies — use a transistor |
| No flyback diode (inductive buzzer) | Some buzzers have internal coils — add 1N4007 if it's a magnetic buzzer |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| Active buzzer 5V | 1 | For simple alerts — beeps with DC |
| Passive buzzer 5V | 1 | For melodies — needs PWM |
| 2N2222 NPN transistor | 1 | If driving larger buzzers |
| 1kΩ resistor | 1 | Base resistor for transistor drive |

> **Pro tip:** Put a 100µF cap across the buzzer power pins if the MCU resets when the buzzer fires. Buzzers cause voltage dips.
