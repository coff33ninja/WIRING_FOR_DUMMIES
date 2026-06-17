# GPIO, ADC, PWM, DAC — Microcontroller Pin Types

## What They Are

Microcontroller pins are not all the same. Each pin type does a different job. Plugging a 12V signal into a 3.3V GPIO pin — or using a PWM-only pin when you need analog input — is how you kill a chip or wonder why nothing works.

## Pin Type Summary

| Pin type | What it does | ESP32 | Arduino Uno |
|----------|-------------|-------|-------------|
| **GPIO** (Digital I/O) | Reads 0V or VCC (high/low). Writes 0V or VCC. | Most pins | Pins 0–13, A0–A5 (as digital) |
| **ADC** | Reads an **analog voltage** and converts to a number (0–4095 or 0–1023) | Pins 32–39 | Pins A0–A5 |
| **PWM** | Outputs a **fake analog voltage** by switching on/off very fast | Any GPIO (via LEDC) | Pins 3, 5, 6, 9, 10, 11 |
| **DAC** | Outputs a **true analog voltage** (rare) | Pins 25, 26 | None (Uno has no DAC) |

## 1. GPIO (Digital Input / Output)

The simplest pin. It can read **HIGH** (3.3V on ESP32, 5V on Arduino) or **LOW** (0V). It can also output HIGH or LOW to turn things on/off.

### As Output

```
GPIO ────[330Ω]──── LED(+) ──── LED(−) ──── GND
```

```
GPIO HIGH (3.3V) → LED on
GPIO LOW (0V)    → LED off
```

### As Input (with Pull-Up)

A floating input pin reads random noise. You need a **pull-up** or **pull-down** resistor to set a known state when nothing is driving it.

```
Switch wiring (pull-down):
    3.3V
      │
    [10kΩ]
      │
GPIO ──┴───[Button]──── GND

Button released → GPIO reads HIGH (3.3V via pull-up)
Button pressed  → GPIO reads LOW (0V to GND)
```

> **See [Pull-Up / Pull-Down Reference](pull-up-pull-down.md)** for detailed selection.

### Current Limits

| | ESP32 | Arduino Uno |
|--|-------|------------|
| Max per pin | 40mA (sink or source) | 40mA |
| Recommended max | 20mA | 20mA |
| Total all pins | ~200mA | ~200mA |

> **Don't drive motors, relays, or LEDs directly from GPIO pins** (except small indicator LEDs through a resistor). Use a transistor or MOSFET to switch higher loads.

## 2. ADC (Analog to Digital Converter)

Reads a voltage and returns a number:

| Board | Resolution | Range | Example |
|-------|-----------|-------|---------|
| ESP32 | 12-bit (0–4095) | 0–3.3V | 1650 = 1.65V |
| Arduino Uno | 10-bit (0–1023) | 0–5V | 512 = 2.5V |

```
Voltage / MaxVoltage = ADC_reading / MaxADC_value

ESP32:  Voltage = (ADC_reading / 4095) × 3.3V
Arduino: Voltage = (ADC_reading / 1023) × 5.0V
```

### Common ADC Uses

- Reading a **potentiometer** (volume knob, dimmer)
- Reading a **voltage divider** with an LDR (light sensor)
- Reading a **thermistor** (temperature)
- Reading a **joystick** module

### ADC Wiring

```
Sensor ──┬── GPIO (ADC pin)
         │
        [10kΩ]
         │
        GND
```

The sensor (LDR, thermistor) and a fixed resistor form a voltage divider. The ADC reads the voltage at the midpoint.

> **ESP32 ADC quirks:**
> - Not linear at the extremes (below ~0.1V and above ~3.2V)
> - Has two ADCs (ADC1 and ADC2). ADC2 is shared with WiFi — when WiFi is on, ADC2 pins return garbage. Use ADC1 pins (32–39) for analog reads with WiFi enabled.

### ESP32 ADC Attenuation

ESP32 ADC pins have configurable input range:

| Attenuation | Max measurable voltage | Use for |
|-------------|----------------------|---------|
| 0dB (default) | ~1.1V | Low-voltage signals |
| 2.5dB | ~1.5V | — |
| 6dB | ~2.2V | — |
| **11dB** | **~3.3V (or 3.9V with slight non-linearity)** | **Default for most sensors** |

```cpp
// ESP32 — always set attenuation to 11dB for 0–3.3V range:
analogReadResolution(12);   // 12-bit
analogSetAttenuation(ADC_11db);  // Full 0-3.3V range
```

## 3. PWM (Pulse Width Modulation)

A digital pin that switches on/off **very fast** (usually ~500Hz to 40kHz). By varying the duty cycle (% of time on vs off), it simulates an analog voltage.

```
PWM at 50% duty cycle:

    ┌────┐    ┌────┐    ┌────┐    ┌────┐
    │    │    │    │    │    │    │    │
───┘    └────┘    └────┘    └────┘    └────
  ON  OFF  ON  OFF  ON  OFF  ON  OFF

ON time = OFF time → Looks like half voltage (1.65V on 3.3V)
```

| Duty cycle | At 3.3V | At 5V |
|-----------|---------|-------|
| 0% | 0V | 0V |
| 25% | 0.825V | 1.25V |
| **50%** | **1.65V** | **2.5V** |
| 75% | 2.475V | 3.75V |
| 100% | 3.3V | 5V |

### What PWM Is Actually Good For

| Use | Frequency | Why |
|-----|-----------|-----|
| **LED dimming** | 500Hz–1kHz | Flicker not visible to eye |
| **Servo control** | **50Hz** (20ms period) | Standard servo protocol |
| **DC motor speed** | 1kHz–20kHz | Higher = quieter (less audible whine) |
| **Fan speed** | 25kHz+ | Above audible range for humans |

### What PWM Is NOT Good For

- **Audio output** — PWM creates a square wave with lots of harmonics. You need a DAC or external audio DAC for clean sound.
- **Precision analog reference** — the output is still 0V or VCC, just switching fast. It's not a true analog voltage.
- **Powering sensitive analog circuits** — the switching noise couples into nearby traces.

### ESP32 PWM (LEDC)

ESP32 has a dedicated PWM controller (LEDC) that can be attached to **any GPIO pin**:

```cpp
ledcAttachPin(GPIO_PIN, channel);  // channel = 0–15
ledcSetup(channel, freq, resolution);  // freq in Hz, resolution in bits
ledcWrite(channel, duty);  // 0 to (2^resolution - 1)
```

Example — dim LED on GPIO 2:
```cpp
ledcAttachPin(2, 0);     // Attach GPIO 2 to channel 0
ledcSetup(0, 5000, 8);   // Channel 0: 5kHz, 8-bit (0–255)
ledcWrite(0, 128);       // 50% duty
```

## 4. DAC (Digital to Analog Converter)

Outputs a **true analog voltage** — not a simulated square wave. ESP32 has **two** DAC channels on GPIO 25 and 26.

```cpp
dacWrite(25, 128);  // Output ~1.65V (half of 3.3V)
```

| Value | Output voltage |
|-------|---------------|
| 0 | 0V |
| 128 | ~1.65V |
| 255 | ~3.3V |

**Use for:** Audio output (simple tone generation), generating an analog control voltage.

**Limitation:** 8-bit (0–255) only. For higher resolution audio, use an external I2S DAC.

## Quick Pin Reference (ESP32)

| Pin type | Pins | Notes |
|----------|------|-------|
| GPIO | Most pins | 0–39 (some reserved) |
| ADC (ADC1) | **32–36, 39** | Safe with WiFi on |
| ADC (ADC2) | 0, 2, 4, 12–15, 25–27 | Garbage when WiFi active |
| DAC | 25, 26 | True analog output (8-bit) |
| PWM | Any GPIO | Via LEDC peripheral |
| Touch | T0–T9 | Capacitive touch sensing |
| RTC | 0–4, 12–15, 25–27, 32–39 | Wake from deep sleep |

## Quick Reference

```
GPIO:   Read HIGH (3.3V/5V) or LOW (0V). Output HIGH or LOW.
ADC:    Read a voltage (0–3.3V or 0–5V) → number (0–4095 or 0–1023)
PWM:    Fake analog by switching fast. Good for LED dimming, servo, motor speed.
DAC:    True analog voltage output. Rare. ESP32: pins 25, 26 only.

ESP32 rules:
  ADC with WiFi ON → use ADC1 pins (32–39)
  PWM on ANY pin → use ledcAttachPin + ledcSetup + ledcWrite
  DAC only on pins 25, 26 (8-bit, 0–3.3V)
  Max 40mA per pin (20mA recommended)

Never connect >3.3V to an ESP32 GPIO pin (unless 5V-tolerant — and even then, risky).
```

## See Also

- [esp32-fan-controller](/projects/esp32-fan-controller)
- [pir-motion-sensor](/projects/pir-motion-sensor)
- [hc-sr04-ultrasonic](/projects/hc-sr04-ultrasonic)
