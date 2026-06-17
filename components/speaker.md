# Speaker / Audio Output — Component Reference

## What It Is

A speaker converts electrical signals into sound by moving a cone (or diaphragm) back and forth, pushing air. In hobby electronics, you'll deal with **small magnetic speakers** (8Ω, 4Ω), **headphone drivers** (32Ω), **piezoelectric buzzers**, and **dedicated audio amplifier modules** (like the MAX98357).

> **Analogy:** A subwoofer in a car — but tiny. Electrical signal in, physical vibration out.

## Speaker Types

### 1. Small Magnetic Speaker (4Ω / 8Ω)

The most common "speaker" in hobby kits. A coil of wire attached to a cone sits inside a magnet. Current through the coil makes it move.

| Spec | 4Ω speaker | 8Ω speaker |
|------|-----------|-----------|
| Impedance | 4Ω | 8Ω |
| Current at 5V (Ohm's law) | 5V / 4Ω = 1.25A | 5V / 8Ω = 0.625A |
| Power at 5V | 6.25W | 3.125W |
| Typical size | 2–3W rated | 0.5–1W rated |

**Why you can't drive a speaker from a GPIO pin directly:**

| GPIO spec | Value | Speaker needs |
|-----------|-------|---------------|
| Max current (Arduino) | ~20mA per pin | 100mA–1A+ |
| Max current (ESP32) | ~12mA per pin | 100mA–1A+ |
| Voltage swing | 0–3.3V or 0–5V | Needs positive AND negative swing for AC |

**Result:** Direct from GPIO = barely audible whisper, possible pin damage, distorted sound.

### 2. Headphone Driver (32Ω)

Headphones have higher impedance (16–32Ω typical). An 8Ω speaker at the same voltage draws ~4× more current than 32Ω headphones.

| Type | Impedance | Typical power | Needs |
|------|-----------|---------------|-------|
| Earbuds | 16Ω | ~10mW | Small amplifier or codec |
| Headphones | 32Ω | ~10–50mW | Headphone amp (e.g. MAX9814) |
| Professional | 250–600Ω | ~100mW | Dedicated headphone amplifier |

## Transistor / H-Bridge Drive

### Single Transistor (Speaker to GND)

For simple tones (not stereo, not high quality):

```
5V ─── Speaker (+) ─── Speaker (–) ─── Collector (NPN)
                                         │
GPIO ───── 1kΩ ────────────────────────── Base
                                         │
                                       Emitter ─── GND
```

- NPN transistor (2N2222, BC547, etc.) switches speaker to GND
- GPIO toggles at the audio frequency — speaker cone moves
- Sound quality: poor (half-wave drive, crossover distortion)
- Speaker sees ~5V peak but only on one half of the wave

### H-Bridge (Push-Pull) — Better Audio

Two transistors (or an H-bridge IC like L293D, DRV8833) let you drive the speaker with **positive AND negative voltage**:

```
         ┌─── Q1 (PNP) ──┐
         │                │
  5V ────┤              Speaker ──── GND (center-tapped)
         │                │
         └─── Q2 (NPN) ──┘
```

- Q1 on, Q2 off: speaker sees +5V
- Q2 on, Q1 off: speaker sees -5V (effectively)
- Full AC swing = louder, cleaner sound

**Simpler alternative:** Use a **DRV8833** or **TB6612** motor driver as a speaker amplifier — it's an H-bridge that can PWM at audio frequencies.

## PWM Audio — The Simple Way

Many microcontrollers have hardware PWM. You can output audio by changing the duty cycle at audio rate.

**How it works:**

- PWM frequency: 10kHz–50kHz (above audible)
- Duty cycle changes 8000–44100 times per second (sample rate)
- A **low-pass filter** (RC or LC) smooths the PWM into an analog voltage

```
MCU PWM ──── 1kΩ ──┬── 10µF ──┬── Speaker (+)
                    │          │
                   GND        GND
```

**Quality:**

| Sample rate | Bit depth | Sound quality | Use case |
|-------------|-----------|---------------|----------|
| 8kHz | 8-bit | AM radio | Voice, beeps, simple tones |
| 16kHz | 8-bit | Telephone | Voice is understandable |
| 22kHz | 10-bit | OK music | Tinny but recognizable |
| 44.1kHz | 16-bit | CD quality | Needs dedicated DAC |

**Problems with PWM audio:**
- PWM carrier frequency leaks into output (high-pitched whine)
- Microcontroller spends all its time updating PWM duty (no time for other work)
- Limited bit depth (8–10 bits on most MCUs)
- Needs external filter circuit

> **PWM audio is fine for:** Beeps, alarms, simple voice prompts (like "door open"). **Not fine for:** Music, hi-fi, or anything you want to enjoy listening to.

## Dedicated DAC + Amplifier

For actual audio quality, use a chip that handles the hard part:

| Chip | Type | Output | Interface | Quality |
|------|------|--------|-----------|---------|
| **MAX98357** | I2S Class-D amp | 3.2W @ 4Ω | I2S (digital audio) | Good — CD quality possible |
| **MAX98357A** | I2S Class-D amp | 3.2W @ 4Ω | I2S (left-channel) | Same |
| **PAM8403** | Stereo Class-D amp | 3W × 2 @ 4Ω | Analog input | Good for line-level |
| **LM386** | Class-AB amp | 0.5W @ 8Ω | Analog input | Vintage, noisy, simple |
| **MAX9814** | Electret mic amp | — | Analog output | Microphone preamp |
| **DFPlayer Mini** | MP3 decoder + amp | 3W @ 4Ω | Serial (UART) | Plays MP3 files from SD |

### MAX98357 I2S Amplifier — Recommended Module

This tiny board takes **I2S digital audio** directly from an ESP32, Teensy, or Raspberry Pi and outputs amplified audio to a speaker.

```
MAX98357 board:
  VIN  ──── 3.3–5V (module powered)
  GND  ──── GND
  BCLK ──── I2S bit clock (GPIO 26 on ESP32)
  LRC  ──── I2S left/right clock (GPIO 25)
  DIN  ──── I2S data (GPIO 27)
  GAIN ──── Gain select (leave floating for 3dB, tie to VIN for 6dB, 12dB, 15dB)
  OUT+ ──── Speaker (+)
  OUT- ──── Speaker (–)
```

**Why I2S is better than PWM:**
- Hardware handles timing — no CPU load
- 16–24 bit audio at 44.1kHz or higher
- No carrier frequency noise
- Stereo possible (two MAX98357s or a stereo chip)

**Software (ESP32 + Arduino):**
- Install the `ESP8266Audio` library or use `I2S` built-in
- Send audio data via `i2s_write()`

## Magnetic vs Piezoelectric

Both make sound but work differently:

| Property | Magnetic speaker | Piezoelectric buzzer |
|----------|-----------------|---------------------|
| **How it works** | Coil + magnet moves cone | Crystal bends when voltage applied |
| **Impedance** | Low (4–32Ω) | Very high (thousands of Ω) |
| **Current draw** | High (100mA–1A) | Very low (~5–20mA) |
| **Sound quality** | Good — full frequency range | Poor — single tone, buzzy |
| **Volume** | Quiet unless amplified | Very loud (can drive directly) |
| **Can play music?** | Yes | No — beeps only |
| **Drive circuit** | Amplifier needed | GPIO directly (or transistor to make louder) |

**When to use a buzzer:** Alert sounds, alarms, error tones, button feedback. No amplifier needed, just a GPIO pin.

**When to use a speaker:** Voice, music, any audio that needs to sound good.

> **Beware:** Active buzzers (with internal oscillator) just need DC voltage — they produce a fixed tone. Passive buzzers (piezo elements) need an AC square wave — use a PWM or toggle pin.

## GPIO Current Limits — Why You Need an Amplifier

| MCU | Max per pin | Max total | Speaker at 5V, 8Ω |
|-----|-------------|-----------|-------------------|
| Arduino Uno | 40mA | 200mA | Needs **625mA** — GPIO can't supply |
| ESP32 | 12mA | 80mA | Needs **625mA** — GPIO will brown out |
| Raspberry Pi | 16mA | 50mA | Needs **625mA** — GPIO will sag |

**Safe current calculation:**
I = V / R = 5V / 8Ω = 0.625A = 625mA

A GPIO pin supplying 625mA = magic smoke. Always use a transistor, H-bridge, or amplifier module.

## Quick Reference

```
Speaker impedance:  4Ω (louder, more current), 8Ω (common), 32Ω (headphones)

Drive methods (worst to best):
  GPIO direct    → barely audible, risks MCU damage
  NPN transistor → audible tones, poor quality
  H-bridge       → better, full AC swing
  PWM + filter   → OK for voice, carrier noise
  I2S + MAX98357 → good audio, 3.2W, recommended

Piezo buzzer:
  Active  = fixed tone (just apply DC voltage)
  Passive = needs AC square wave (PWM)

MAX98357 wiring:
  VIN, GND, BCLK, LRC, DIN, OUT+/-

Never connect a speaker directly to a GPIO pin.
```
