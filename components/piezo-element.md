# Piezo Element — Component Reference

> **See also:** [Buzzer](buzzer.md) — pre-built buzzer modules that are simpler to use for beeps. [Speaker](speaker.md) — for audio-quality sound output.

## What It Is

A piezo element (piezoelectric disc) is a thin ceramic disc sandwiched between two metal plates. When you apply voltage, the disc physically bends. When it bends (from a knock or vibration), it generates voltage.

This works **both ways**:

- **Apply voltage → it bends/moves** (use as a buzzer, speaker, or actuator)
- **Bend it → it generates voltage** (use as a knock sensor, vibration sensor, or microphone)

The name comes from Greek "piezein" — to press or squeeze.

## Piezo as Sound Maker (Buzzer)

This is the most common use. When you apply an AC voltage (square wave), the disc vibrates at that frequency and produces sound.

### Bare Piezo Disc vs Piezo Buzzer

| | Bare Piezo Disc | Piezo Buzzer Module |
|--|----------------|---------------------|
| What it is | Just the ceramic disc | Disc + oscillator circuit inside |
| Signal needed | **AC square wave** (PWM) | DC voltage (internal circuit makes the tone) |
| Microcontroller | Needs PWM pin | Works with any GPIO HIGH/LOW |
| Frequency | You control it | Fixed (usually ~2–4 kHz) |
| Volume | Depends on frequency + voltage | Fixed |
| Use for | Variable tones, music, alarms | Simple beep/alert |

**A bare piezo element is NOT a speaker.** It can't reproduce music (too high impedance, no frequency response). It's good for beeps, tones, and ultrasonic output.

### Driving a Bare Piezo Disc (PWM)

```
Microcontroller
    │
    ├── PWM pin ── piezo (+) ── piezo (-) ── GND
    │
   GND
```

Arduino code:

```c
void setup() {
  pinMode(9, OUTPUT);
}

void loop() {
  tone(9, 1000); // 1 kHz tone
  delay(1000);
  noTone(9);
  delay(500);
  tone(9, 3000);  // 3 kHz tone
  delay(1000);
  noTone(9);
  delay(500);
}
```

**Important:** The `tone()` function on Arduino uses a timer and prevents PWM on pins 3 and 11 on Uno. Use `analogWrite()` with a frequency parameter for more control.

### Louder Sound — Higher Voltage

Piezo elements are more efficient at higher voltages. A 12Vpp signal is much louder than 5V. Use a simple transistor driver:

```
5V PWM ── base resistor ──┬── 2N2222 (NPN)
                          │    │
                        GND   │
                              │
                       12V ──┬┴── piezo (+) ── piezo (-) ── collector
```

Or use the `tone()` library with a piezo-specific driver. But for most hobby projects, 5V direct drive is loud enough.

### Resonant Frequency

Every piezo disc has a **resonant frequency** (typically 3–7 kHz). At this frequency, the disc vibrates with maximum amplitude and is loudest. Driving at resonance gives the highest volume for the lowest power.

To find your piezo's resonance: sweep frequencies from 1 kHz to 10 kHz and measure volume (by ear or with a microphone). The loudest frequency is the resonant frequency.

## Piezo as Sensor (Knock / Vibration / Ultrasonic Receiver)

When the piezo disc is physically deformed (knock, vibration, pressure change), it generates a voltage spike. You can read this with an ADC or digital input.

### Knock Sensor

```
Piezo (+)
    │
    ├── 1MΩ resistor ── GND (bleed off static charge)
    │
    ├── 100kΩ resistor ── ADC pin
    │
    └── 5.1V zener diode ── GND (protect from overvoltage)
```

The 1MΩ resistor prevents the piezo from holding a charge (which would block small vibrations from being detected). The zener diode clips voltage spikes — a piezo can generate 50V+ from a hard knock.

Without the protection diode, a hard knock can destroy your ADC pin. Always add protection.

### Reading Piezo Knock (Arduino)

```c
const int piezoPin = A0;

void loop() {
  int val = analogRead(piezoPin);
  if (val > 100) { // Threshold — adjust for sensitivity
    Serial.printf("Knock detected! Value: %d\n", val);
    delay(200); // Debounce
  }
}
```

### Ultrasonic Receiver

Piezo discs can receive ultrasonic signals. A 40kHz piezo disc is the receiver in HC-SR04 ultrasonic distance sensors. The same disc used as a transmitter can receive if you switch modes fast enough.

## Piezo as Energy Harvester

This is an advanced use: a piezo disc on a vibrating surface (engine, shoe heel, bridge) generates small amounts of electricity. With a rectifier and capacitor, you can harvest micro-watts to power ultra-low-power circuits.

A typical 27mm piezo disc stomped on produces ~1–5 mJ per stomp — enough for a brief radio transmission or sensor reading.

Not practical for most hobby projects but common in research and "energy harvesting" demos.

## Piezo vs Speaker vs Buzzer

| | Piezo Disc | Magnetic Speaker | Magnetic Buzzer |
|--|-----------|-----------------|-----------------|
| Sound mechanism | Crystal bending | Coil + magnet | Coil + magnet + contact |
| Frequency range | Narrow (resonant peak) | Wide (full audio) | Narrow (fixed tone) |
| Impedance | High (1kΩ–10kΩ) | Low (4Ω–32Ω) | Low (16Ω–50Ω) |
| Power | Low (µA–mA) | Higher (10mA–1A) | Moderate (30–100mA) |
| Max volume | Loud at resonance | Increasing with power | Fixed loudness |
| Audio quality | Poor (buzzy) | Good | Poor |
| Microcontroller drive | Direct (PWM) | Needs amplifier | Direct (GPIO or transistor) |
| Part cost | $0.10–$0.50 | $0.50–$5 | $0.50–$2 |
| Ultrasonic use | Yes | No | No |

**Use a piezo** for: beeps, alarms, ultrasonic sensing, knock detection, cost-sensitive projects.

**Use a speaker** for: music, voice, quality audio output.

**Use a magnetic buzzer** for: simple beeps with DC voltage (no PWM needed).

## Quick Reference

- **Piezo works both ways** — voltage creates movement, movement creates voltage
- **Bare piezo needs PWM/tone AC signal** — DC voltage just bends it once
- **Piezo buzzer module needs DC** — internal oscillator handles the AC
- **Resonant frequency** is the loudest point — find yours by sweeping 1–10 kHz
- **Higher voltage = louder sound** — up to 24Vpp for some discs
- **Knock sensor needs protection** — 5.1V zener across the piezo or a 100kΩ series resistor
- **1MΩ bleeder resistor** across piezo when used as sensor — prevents charge buildup
- **Piezo impedance varies with frequency** — at resonance it drops significantly
- **Don't exceed the voltage rating** — small discs crack above ~30V, larger discs handle more
