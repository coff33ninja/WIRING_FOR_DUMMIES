# PWM (Pulse Width Modulation) — Fundamental Reference

## What It Is

PWM is a way to **fake an analog voltage** using a digital pin. Instead of a steady voltage, you rapidly turn the pin ON and OFF. By controlling how long it's ON vs OFF, you control the average voltage seen by the load.

```
ON  ┌┐    ┌┐    ┌┐    ┌┐    ┌┐    ┌┐
    │ │   │ │   │ │   │ │   │ │   │ │
OFF ┘ └───┘ └───┘ └───┘ └───┘ └───┘ └──
    |<->|<->|
    Period
    |<->|  = Duty cycle (25%, 50%, 75%, etc.)
    ON time
```

**Analogy:** A flickering light that flickers so fast your eye sees it as constantly on, just dimmer.

## Key Terms

| Term | Meaning |
|------|---------|
| **Frequency** | How many ON/OFF cycles per second (Hz). High enough that the load doesn't notice |
| **Period** | Time for one complete cycle (1 / frequency) |
| **Duty cycle** | Percentage of time the signal is ON |
| **Resolution** | How many steps of duty cycle you can set (e.g., 8-bit = 0–255) |

## Common Frequencies

| Application | Frequency | Why |
|-------------|-----------|-----|
| LED dimming | 500 Hz – 1 kHz | Flicker invisible to eye, no audible noise |
| Servo motor | 50 Hz | Standard servo protocol (20ms period) |
| DC motor speed | 1–20 kHz | Below 1 kHz = audible whine, above 20 kHz = silent |
| Heater control | 1–10 Hz | Thermal mass smooths it out |
| Audio | 20–40 kHz | Class D amplifier switching frequency |

**The whine:** If you hear a high-pitched squeal from your motor or LED driver, your PWM frequency is in the audible range. Increase it above 20 kHz.

## PWM on Common Microcontrollers

| MCU | PWM pins | Resolution | Max frequency |
|-----|----------|------------|---------------|
| Arduino Uno (ATmega328P) | Pins 3, 5, 6, 9, 10, 11 | 8-bit (0–255) | ~980 Hz (pins 5, 6), ~490 Hz (others) |
| ESP32 | Any pin (16 channels) | 1–16 bit | Up to 40 MHz |
| Raspberry Pi Pico | 16 pins | 1–16 bit (16-bit with PIO) | Up to 8 MHz |
| STM32 | Most pins | Up to 16 bit | Up to system clock |

## Wiring PWM Devices

### LED Dimming

```
GPIO (PWM) ──┬── 220Ω ──┬── LED ── GND
             │          │
             └──────────┘
```

No special wiring needed. Just a current-limiting resistor. The LED sees an average current proportional to duty cycle.

**Pseudo-analog:** 0% duty = off, 50% = half brightness, 100% = full brightness. Your eye averages the pulses.

### DC Motor Speed Control

```
GPIO (PWM) ──── MOSFET gate (via 1kΩ resistor)
                   │
  Motor power ───── D (MOSFET drain)
  Motor GND ─────── S (MOSFET source) ──── GND
                   │
                Diode (flyback, cathode to motor power)
```

Never connect a motor directly to a GPIO pin. The motor draws too much current and generates voltage spikes. Use a MOSFET or transistor.

### Servo Motor

```
GPIO (PWM) ──── Signal wire (usually white/yellow)
VCC (5V) ────── Red wire
GND ─────────── Brown/black wire
```

Servos use a specific PWM protocol: 50 Hz (20ms period), 1ms pulse = 0°, 1.5ms = 90°, 2ms = 180°.

Do NOT power a servo from the microcontroller's 5V pin. Use an external 5V supply.

## Software PWM vs Hardware PWM

**Hardware PWM:** A timer peripheral in the microcontroller generates the signal without any CPU involvement. Once started, it runs in the background. Preferred for everything.

**Software PWM (bit-banging):** Your code manually toggles pins in a loop. Uses CPU cycles, less precise, can glitch if other interrupts fire. Only use on pins that don't have hardware PWM.

Always use hardware PWM pins when possible.

## Quick Reference

- **Duty cycle 0%** = always OFF (0V)
- **Duty cycle 100%** = always ON (full voltage)
- **Duty cycle 50%** at 5V = average of 2.5V
- **Increase frequency** above audible range to avoid whine
- **Filters** (capacitor + resistor) can smooth PWM into a steady DC voltage
- **MOSFET + flyback diode** required for motor control
- **Hardware PWM** is better than software PWM
- **Common servo frequency:** exactly 50 Hz

## See Also

- [esp32-fan-controller](/projects/esp32-fan-controller)
- [neopixel-ws2812b](/projects/neopixel-ws2812b)
