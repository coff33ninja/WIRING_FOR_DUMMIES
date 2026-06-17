# Analog vs Digital Signals — Fundamental Reference

## What It Is

**Analog signals** vary continuously — infinite possible values between min and max. **Digital signals** are either HIGH (1) or LOW (0) — two states only.

```
Analog:   ╔══════════════╗
          ║  ╱╲    ╱╲   ║
          ║ ╱  ╲  ╱  ╲  ║
          ║╱    ╲╱    ╲ ║
          ╚══════════════╝
          Continuous voltage curve

Digital:  ╔══════════════╗
          ║ ┌┐  ┌┐  ┌┐  ║
          ║ ││  ││  ││  ║
          ║─┘└──┘└──┘└──║
          ╚══════════════╝
          HIGH or LOW only
```

## Key Differences

| Property | Analog | Digital |
|----------|--------|---------|
| Values | Infinite (continuous) | Two (0 or 1) |
| Noise immunity | Low | High |
| Wire count | 1 signal wire | 1 signal wire (per bit) |
| Distance | Degrades gradually | Works until it doesn't |
| Processing | Harder (analog circuits) | Easy (microcontrollers) |
| Examples | Temperature, light, sound | Buttons, relays, logic pins |

## Analog Signals

### What's Analog

- Potentiometer position
- Temperature (thermistor / analog temp sensor)
- Light level (LDR / photodiode)
- Microphone audio
- Voltage divider output
- Battery voltage

### Reading Analog with a Microcontroller

Microcontrollers are digital chips. To read an analog voltage, they use an **ADC** (Analog-to-Digital Converter):

```
Analog voltage ──→ ADC pin ──→ digital value (0–1023 for 10-bit)
```

| ADC resolution | Steps | 0V value | 3.3V value | Step size |
|---------------|-------|----------|------------|-----------|
| 8-bit | 256 | 0 | 255 | 12.9 mV |
| 10-bit | 1024 | 0 | 1023 | 3.2 mV |
| 12-bit | 4096 | 0 | 4095 | 0.8 mV |
| 16-bit | 65536 | 0 | 65535 | 0.05 mV |

**Voltage range:** Most ADCs read 0V to VCC (usually 3.3V or 5V). Connecting a higher voltage will damage the pin — use a voltage divider.

### Analog Output (DAC)

Some microcontrollers have a **DAC** (Digital-to-Analog Converter) that outputs a true analog voltage. If not, you use **PWM** to fake it:

```
DAC: True analog voltage (e.g., 0V–3.3V)
PWM: 0V or 3.3V, rapidly switched (requires filtering to smooth)
```

## Digital Signals

### What's Digital

- Push button / switch state
- Relay control
- LED on/off
- Logic pins (HIGH/LOW)
- Digital sensor outputs (DHT22, HC-SR04)
- Communication lines (UART, I2C, SPI)

### Voltage Thresholds

A digital pin doesn't see "a little bit HIGH". It has defined thresholds:

| System | Guaranteed LOW | Guaranteed HIGH | Max input |
|--------|---------------|----------------|-----------|
| 5V logic (Arduino) | 0V–1.5V | 3.5V–5V | 5.5V |
| 3.3V logic (ESP32) | 0V–0.8V | 2.0V–3.3V | 3.6V |

**The danger zone:** If a signal is between LOW and HIGH thresholds, the pin reads random values and may oscillate. This wastes power and can damage some chips.

### Pull-up and Pull-down Resistors

A digital input that's NOT connected to anything is **floating** — it picks up electrical noise and reads random values. Fix it with pull-up or pull-down resistors:

```
Pull-up (default HIGH):
VCC ── 10kΩ ──┬── GPIO pin
               │
             Button
               │
              GND ── press → reads LOW

Pull-down (default LOW):
GPIO pin ──┬── 10kΩ ── GND
           │
         Button
           │
          VCC ── press → reads HIGH
```

## Analog to Digital Conversion: The Nyquist Rule

To digitize an analog signal and reconstruct it later, you must sample at **at least 2× the highest frequency** in the signal:

- Audio (20 kHz max) → sample at 44.1 kHz (CD quality)
- Temperature (changes slowly) → sample once per second is fine
- Light sensor (steady) → sample every 100ms

Sample too slowly and you get **aliasing** — the signal looks like a different frequency than it actually is.

## When to Use Analog vs Digital

| Situation | Use |
|-----------|-----|
| Read a knob position | Analog (potentiometer → ADC) |
| Read a button press | Digital (GPIO input) |
| Measure temperature | Either: analog (TMP36) or digital (DS18B20, DHT22) |
| Control LED brightness | Digital (PWM) |
| Control LED on/off | Digital (GPIO output) |
| Detect light level | Analog (LDR + voltage divider) |
| Detect motion | Digital (PIR sensor output) |
| Play audio | Analog (DAC or PWM + filter) |
| Talk to a sensor | Digital (I2C, SPI, UART) |

## Quick Reference

- **Analog:** Infinite values, susceptible to noise, needs ADC to read
- **Digital:** Two values (HIGH/LOW), noise-resistant, native to microcontrollers
- **ADC** converts analog to digital (voltage → number)
- **DAC** converts digital to analog (number → voltage)
- **PWM** fakes analog by switching fast (not true analog, but works for LEDs/motors)
- **Never** feed > VCC into an ADC pin or digital input
- **Floating pins** are unpredictable — always use pull-up/down

## See Also

- [hc-sr04-ultrasonic](/projects/hc-sr04-ultrasonic)
- [oled-sensor-readout](/projects/oled-sensor-readout)
- [pir-motion-sensor](/projects/pir-motion-sensor)
