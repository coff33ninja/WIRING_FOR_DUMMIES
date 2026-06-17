# Audio Amplifier (LM386, PAM8403, MAX98357) — Component Reference

## What It Is

An audio amplifier takes a **low-power audio signal** (from a microphone, audio jack, or microcontroller DAC) and boosts it to drive a speaker. You can't drive a speaker directly from a GPIO pin — it can't supply enough current.

## Why You Need One

| Source | Output | Can drive a speaker? |
|--------|--------|---------------------|
| Microphone (electret) | ~20mV | No |
| Headphone jack (line out) | ~1V | No |
| Microcontroller DAC / PWM | ~1–3.3V | No (too little current) |
| Audio amplifier output | 0.5–50W | Yes |

## Common Amplifier Chips

### LM386 — Classic, Through-Hole

| Property | Value |
|----------|-------|
| Power output | 0.3–1W (depending on supply) |
| Supply voltage | 4–12V |
| Quiescent current | ~4mA |
| Input impedance | ~50kΩ |
| Gain | 20–200 (pin 1–8 jumper) |

**Wiring:**

```
Audio in ──┬── 10kΩ ──┬── 10µF ──┬── LM386 pin 3 (+)
           │          │          │
          GND        GND    ┌────┘
                            │
LM386 pin 7 ── 10µF ── GND    (bypass)
LM386 pin 6 ── VCC (4–12V)
LM386 pin 4 ── GND
LM386 pin 5 ──┬── 220µF ──┬── Speaker (+)
              │           │
              └── 0.1µF ──┘
LM386 pin 1 ── 10µF ── LM386 pin 8  (gain = 200)
             (omit for gain = 20)
```

**Gain control:** With nothing between pins 1 and 8, gain = 20. With a 10µF cap, gain = 200. You can also add a resistor in series (e.g., 1.2kΩ) for intermediate gain.

### PAM8403 — Class D, Efficient, Small

| Property | Value |
|----------|-------|
| Power output | 3W per channel (3W+3W) |
| Supply voltage | 2.5–5.5V |
| Quiescent current | ~5mA |
| Efficiency | ~85% |
| Channels | 2 (stereo) |

**Why Class D:** The PAM8403 switches the output transistors rapidly (instead of operating in linear mode like the LM386). This makes it much more efficient — longer battery life, less heat.

**Wiring:**

```
Module:
  VCC ── 5V
  GND ── GND
  L+  ── Left speaker (+)
  L-  ── Left speaker (-)
  R+  ── Right speaker (+)
  R-  ── Right speaker (-)
  LIN ── Audio input (left channel)
  RIN ── Audio input (right channel)
  SHUT ── HIGH = enable, LOW = mute (tie to VCC if unused)
```

**Input:** 3.5mm audio jack, or microcontroller DAC/PWM output through a 1µF capacitor.

### MAX98357 — I2S Digital Input

| Property | Value |
|----------|-------|
| Power output | 3W at 4Ω |
| Supply voltage | 2.5–5.5V |
| Input | **I2S digital** (not analog) |
| Efficiency | ~85% |
| Channels | 1 (mono) |

**Unique:** The MAX98357 takes digital audio directly from the microcontroller's I2S bus — no DAC needed. The chip decodes the I2S signal and amplifies it in one step.

**Wiring (with ESP32):**

```
MAX98357            ESP32
  VIN ─────────────── 5V
  GND ─────────────── GND
  BCLK ────────────── GPIO 26 (I2S bit clock)
  LRC ─────────────── GPIO 25 (I2S word select / left-right clock)
  DIN ─────────────── GPIO 27 (I2S data)
  SD ──────────────── GPIO (shutdown, active LOW — pull HIGH or leave floating)
  GAIN ────────────── Leave floating for 3dB, or connect through resistor divider
```

**Library:** ESP32-AudioI2S or Arduino ESP32 I2S library.

**Advantage over LM386/PAM8403:** No analog noise from PWM or DAC. The I2S signal is digital all the way to the amp. No hiss, no hum.

## Speaker Impedance

| Amplifier | Speaker impedance | Result |
|-----------|------------------|--------|
| LM386 | 4–8Ω | Works well |
| LM386 | 16Ω+ | Quieter, but okay |
| PAM8403 | 4Ω | 3W output |
| PAM8403 | 8Ω | 1.5W output |
| MAX98357 | 4Ω | 3W output |
| MAX98357 | 8Ω | 1.5W output |

**Don't use speakers with impedance lower than the amp's rating.** A 2Ω speaker on a PAM8403 rated for 4Ω will draw too much current and may destroy the chip.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Hum / buzzing | Ground loop or noisy power supply | Star ground, add 100µF + 100nF on supply |
| High-frequency whine | PWM audio signal without filtering | Add low-pass filter (RC: 100Ω + 10nF) before amp input |
| No sound, chip hot | Speaker impedance too low | Use proper impedance speaker |
| No sound, chip cold | No input signal, or muted | Check input, check SHUTDOWN/SD pin |
| Distorted sound | Amplifier clipping (overdriven) | Reduce input volume, or increase supply voltage |
| PAM8403 makes static noise | SHUTDOWN pin floating | Pull SHUTDOWN HIGH (or to VCC through 10kΩ) |

## Quick Reference

- **LM386:** Classic, through-hole, 0.3–1W, 4–12V supply. Gain set by pin 1–8.
- **PAM8403:** Class D, 3W+3W stereo, 2.5–5.5V, efficient. Good for battery projects.
- **MAX98357:** I2S digital input, 3W mono, no analog noise. Best quality.
- **Speaker impedance:** Match or exceed the amp's rating. 4Ω or 8Ω is standard.
- **Coupling capacitor:** Always put a capacitor (1–10µF) between the audio source and amp input to block DC offset.
- **Decoupling:** 100µF near the amplifier's power pins. Audio circuits are sensitive to power supply noise.
- **Volume control:** A potentiometer (10kΩ) between audio source and amplifier input.
