# Vibration Motor (ERM / LRA) — Component Reference

## What It Is

A vibration motor creates **physical vibration** — the buzzing feeling in your phone, game controller, or smartwatch. There are two types: **ERM** (Eccentric Rotating Mass) and **LRA** (Linear Resonant Actuator).

## ERM vs LRA

| Feature | ERM | LRA |
|---------|-----|-----|
| Mechanism | Weight on a DC motor shaft | Spring + magnet + coil |
| Vibration type | Wideband (any frequency) | Narrowband (resonant frequency) |
| Start time | ~50ms | ~5ms |
| Stop time | ~100ms (coasts) | ~5ms (brakes) |
| Control | Voltage/PWM | AC signal at resonant frequency |
| Haptic feedback | Blunt, buzzy | Crisp, precise |
| Price | Cheap ($0.50–$2) | More expensive ($2–$10) |
| Lifetime | ~100–500 hours (brushes wear) | ~1000+ hours (no brushes) |

**ERM** is a standard DC motor with an off-center weight. Apply voltage, it vibrates. Simple.

**LRA** is like a linear speaker without a cone. It needs an AC drive signal at its resonant frequency (typically 150–250 Hz). Off-resonance, it barely vibrates.

## ERM (Eccentric Rotating Mass)

### How It Works

A DC motor shaft has an **off-center weight** (like a washing machine with an unbalanced load). The spinning weight creates centrifugal force that shakes the motor:

```
          ┌───┐
          │   │  ← Weight (offset from shaft)
          └───┘
           │
     ─────┴──────  ← Motor shaft
    │   MOTOR    │
    └────────────┘
```

### Wiring (Same as a DC Motor)

```
GPIO (PWM) ──── 1kΩ ──── NPN base (2N2222)
                         │
VCC ────────── ERM(+) ───┤ Collector
ERM(-) ────────┬───────── Emitter ── GND
               │
              Diode (flyback, cathode to VCC)
```

ERM motors don't need a flyback diode in theory (they're just motors), but adding one protects the transistor.

### PWM Control

ERM vibration intensity is controlled by PWM:

```cpp
analogWrite(MOTOR_PIN, 0);     // off
analogWrite(MOTOR_PIN, 128);   // half vibration
analogWrite(MOTOR_PIN, 255);   // full vibration
```

**PWM frequency:** Use > 20 kHz to avoid audible whine from the motor.

### Voltage vs Vibration

| Voltage | Vibration intensity |
|---------|-------------------|
| Below startup voltage (typically 0.8–1.5V) | None |
| Rated voltage (typically 3V) | Full |
| 50% PWM at rated voltage | ~50% intensity |

ERM motors have a **dead zone** below the startup voltage — they won't vibrate at all below ~1V regardless of PWM duty cycle.

### Coin (Flat) ERM Motors

Common in phones and small wearables. A flat motor with a round, coin-like shape:

```
  ┌──────────┐
  │  O   O   │  ← Solder pads (+, -)
  │   ───    │
  │  ╱     ╲  │  ← Rotating mass inside
  └──────────┘
```

Same wiring as a regular ERM but smaller and lower current (~60mA at 3V).

## LRA (Linear Resonant Actuator)

### How It Works

A spring + magnet assembly moves up and down when driven with an AC signal at its resonant frequency:

```
  ╔══╗
  ║  ║  ← Spring
  ║  ║
  ║MM║  ← Magnet
  ║  ║
  ║CC║  ← Coil
  ╚══╝
```

### Wiring

LRAs are **not polarity sensitive** — they're AC devices:

```
GPIO (PWM) ──── Capacitor (4.7µF) ──── LRA +
  GND ───────────────────────────────── LRA -
```

The capacitor blocks DC and converts the PWM to an AC-like waveform. The LRA needs a specific drive frequency (typically 150–250 Hz for standard LRAs, 50–100 Hz for large ones).

### Driving at Resonant Frequency

```cpp
const int LRA_PIN = 9;
const int RESONANT_FREQ = 175; // Hz — check your LRA's datasheet

void setup() {
  analogWriteFrequency(LRA_PIN, RESONANT_FREQ);
  analogWriteResolution(10); // 0–1023 on some MCUs
}

void vibrate(int intensity) {
  analogWrite(LRA_PIN, intensity);
}
```

**Without the correct resonant frequency**, the LRA barely vibrates and draws more current wastefully.

### LRA Driver ICs

For precise control (especially in battery devices), use a dedicated LRA driver:

| Driver | Features |
|--------|----------|
| DRV2605 | I2C, haptic waveforms, auto overdrive/brake, ERM + LRA |
| DRV2603 | PWM input, auto resonant tracking |
| DRV2625 | I2C, LRA only, ultra-low power |

The **DRV2605** is the easiest to use — it handles resonant drive, braking, and has pre-programmed haptic effects (buzz, click, double-click, etc.).

## Haptic Patterns

### With ERM (Simple PWM)

```cpp
void buzz(int ms) {
  analogWrite(MOTOR_PIN, 255);
  delay(ms);
  analogWrite(MOTOR_PIN, 0);
}

void doubleBuzz() {
  buzz(100);
  delay(50);
  buzz(100);
}
```

### With DRV2605 (Pre-Programmed Effects)

```cpp
#include <Adafruit_DRV2605.h>
Adafruit_DRV2605 drv;

void setup() {
  drv.begin();
}

void loop() {
  drv.setWaveform(0, 1);     // strong click
  drv.setWaveform(1, 0);     // end sequence
  drv.go();

  delay(1000);
}
```

## Applications

| Device | Motor type | Typical drive |
|--------|-----------|---------------|
| Phone | LRA | DRV2605 I2C |
| Game controller | ERM | PWM + transistor |
| Smartwatch | Coin ERM | Direct PWM (low current) |
| Adult toys | ERM | PWM + transistor |
| Haptic feedback button | LRA | DRV2605, tuned to resonant freq |
| VR controller | LRA | Audio-like amplifier |

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| No vibration (ERM) | Below startup voltage | Increase PWM duty cycle or supply voltage |
| No vibration (ERM) | Motor stalled or dead | Check with direct VCC/GND |
| Weak vibration (ERM) | Low voltage or weight misaligned | Check power, replace motor |
| Audible buzz (ERM) | PWM frequency in audible range | Increase PWM frequency above 20 kHz |
| No vibration (LRA) | Wrong drive frequency | Find resonant frequency from datasheet |
| Weak vibration (LRA) | Off-resonance or low amplitude | Tune frequency, increase AC voltage |
| LRA draws too much current | Driven at DC instead of AC | Add capacitor in series, check waveform |
| Vibration stops under load | Power supply can't handle current spike | Add capacitor near motor |

## Quick Reference

- **ERM:** DC motor with off-center weight. Simple, cheap, PWM control.
- **LRA:** Linear actuator, needs AC at resonant frequency. Crisp haptics.
- **ERM drive:** NPN transistor + flyback diode + PWM
- **LRA drive:** AC signal at 150–250 Hz + capacitor in series
- **LRA driver IC:** DRV2605 (I2C) — handles everything automatically
- **Coin ERM:** Flat, low current, direct GPIO drive with resistor
- **Startup voltage (ERM):** Typically ~1V — below that, no vibration at all
- **Rated voltage:** Usually 3V for small ERMs, check datasheet
- **Audible noise:** Use PWM > 20 kHz for ERM, or use LRA (quieter)
