# Microphone (Electret / MAX9814 / MEMS) — Component Reference

## What It Is

A microphone converts sound (air pressure waves) into an electrical signal. For microcontrollers and hobby electronics, there are two common types:

- **Electret condenser microphone** — cheap, common, needs a bias voltage
- **MEMS microphone** — tiny, modern, surface-mount only
- **MAX9814 module** — electret capsule + amplifier + AGC in one board

## Electret Microphone Capsule

The little silver can with two legs you see on Arduino microphone modules. Inside is a lightweight diaphragm and a charged electret material. Sound vibrates the diaphragm, changing capacitance, which produces a tiny voltage change.

### How to Use a Bare Electret Capsule

An electret capsule alone produces a **very weak signal** — millivolts at best. You can't read it directly with an ADC. You need:

1. **Biasing** — the capsule needs DC voltage through a resistor (typically 2.2–10kΩ)
2. **Amplification** — an op-amp to boost the signal to ADC range (0–3.3V or 0–5V)
3. **DC blocking** — a capacitor to remove the DC bias from the audio signal
4. **DC offset** — bias the amplified signal to VCC/2 so the ADC can read both positive and negative swings

### Minimum Circuit

```
VCC (5V)
  │
  10kΩ
  │
  ├─── electret capsule (+)
  │         │
  │         └─── GND
  │
  └── 100nF capacitor ──┬── 10kΩ ── VCC/2 (virtual ground)
                        │
                        10kΩ
                        │
                       GND
```

This gives you a weak audio signal centered at VCC/2. It works for clap detection and simple sound presence but won't sound good.

## MAX9814 Module — The Easy Way

The MAX9814 is a complete microphone module with:

- Electret capsule built-in
- Amplifier with 40dB, 50dB, or 60dB gain (selectable)
- **Automatic Gain Control (AGC)** — adjusts amplification so loud and quiet sounds stay in range
- Output biased to 1.25V (for 3.3V supply)
- Low noise

### Wiring

```
MAX9814 Module:
    VCC ── 3.3V or 5V
    GND ── GND
    OUT ── ADC pin
    GAIN ── GND (40dB), VCC (50dB), or float (60dB)
    AR ── Attack/Release timing (float = default)
```

| GAIN Connection | Gain | Best For |
|----------------|------|----------|
| GND | 40dB | Loud sounds, close-talk |
| Float (nothing) | 50dB | General purpose |
| VCC | 60dB | Quiet sounds, distant pickup |

### Reading Audio (Arduino)

```c
const int micPin = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int sample = analogRead(micPin);
  float voltage = (sample / 1023.0) * 3.3;
  Serial.println(voltage); // 1.25V = silence
  delay(1);
}
```

For sound level detection (amplitude):

```c
const int micPin = A0;
int minVal = 1023;
int maxVal = 0;

void loop() {
  for (int i = 0; i < 200; i++) {
    int val = analogRead(micPin);
    if (val < minVal) minVal = val;
    if (val > maxVal) maxVal = val;
    delayMicroseconds(200); // ~10ms for 200 samples
  }
  int amplitude = maxVal - minVal;
  Serial.printf("Sound level: %d\n", amplitude);
  minVal = 1023;
  maxVal = 0;
  delay(100);
}
```

## MAX4466 Module — Alternative

The MAX4466 is similar to the MAX9814 but **without AGC**. You get fixed gain. Better for audio recording where consistent amplification matters. Worse for variable-loudness environments.

| | MAX9814 | MAX4466 |
|--|---------|---------|
| AGC | Yes (auto-adjusts gain) | No |
| Max gain | 60dB | 60dB (fixed via resistor) |
| Output bias | 1.25V (at 3.3V supply) | VCC/2 |
| Clap detection | Better (AGC handles loud/quiet) | OK |
| Audio recording | Distorts with AGC (gain pumping) | Better (consistent) |

## INMP441 / MEMS Microphones (I2S)

MEMS (Micro-Electro-Mechanical System) microphones are tiny surface-mount sensors. The INMP441 and ICS-43434 are popular, communicating over **I2S** (a digital audio protocol) — they output a digital signal directly, no ADC needed.

```
INMP441:
    VCC ── 3.3V
    GND ── GND
    WS (word select) ── I2S_WS
    SCK (clock) ── I2S_SCK
    SD (data) ── I2S_SD
    L/R (channel select) ── GND or VCC
```

**Advantages over analog:**
- No noise from ADC or wiring
- No gain setting needed
- Can do 16-bit audio at 44.1kHz (CD quality)
- Tiny footprint

**Disadvantages:**
- ESP32 has I2S, Arduino Uno does NOT
- More complex to code (need I2S library)
- Surface-mount only — use a breakout board

## Which Microphone to Use

| Need | Use | Why |
|------|-----|-----|
| Clap detection, sound trigger | MAX9814 | AGC handles all volumes, simple analog out |
| Voice recording (Arduino) | MAX4466 | Consistent gain, less distortion than MAX9814 |
| Voice recording (ESP32) | INMP441 (I2S) | Digital, high quality, no noise |
| Ultra-low power wake on sound | Electret capsule + transistor | <1µA quiescent |
| Two microphones (direction detect) | Two MAX9814 or two INMP441 | Compare amplitude difference for direction |
| Frequency analysis (FFT) | INMP441 (I2S) | Clean digital signal, good sample rate |

## Clap Detection Circuit (Simple Trigger)

```
MAX9814 OUT ── ADC ── microcontroller
                    │
                    └── Read analog, detect when amplitude exceeds threshold
```

Simpler version without MAX9814: Use an electret capsule biased through a transistor. Output goes LOW when sound exceeds threshold. No ADC needed — just a digital input. Adjust sensitivity with a pot.

## Quick Reference

- **Electret capsule** needs bias (2.2–10kΩ to VCC) and amplification — not usable alone
- **MAX9814** = complete module with AGC, output at 1.25V bias (3.3V supply), 3 pins (VCC, GND, OUT)
- **MAX4466** = no AGC, output at VCC/2, better for consistent audio
- **INMP441** = digital I2S output, needs I2S peripheral, best quality
- **Output voltage range:** 0V to VCC, silence is at bias point (~1.25V or VCC/2)
- **Sound level:** Take many ADC readings, find min/max over ~20ms, amplitude = max - min
- **Noise:** Keep microphone wires short and shielded. Digital noise from nearby GPIO lines will couple into the analog signal.
