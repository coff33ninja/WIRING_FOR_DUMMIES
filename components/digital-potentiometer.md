# Digital Potentiometer (X9C103 / MCP41xx) — Component Reference

## What It Is

A digital potentiometer (digipot) is an **electronically adjustable resistor**. Instead of turning a knob, you send digital signals to change the resistance. It replaces mechanical potentiometers in circuits that need remote or automated adjustment.

## Common Chips

### X9C103 (X9C Series)

| Property | Value |
|----------|-------|
| Resistance | 1kΩ (X9C102), 10kΩ (X9C103), 50kΩ (X9C503), 100kΩ (X9C104) |
| Taps | 100 (99 resistor segments) |
| Step size | Total resistance / 99 |
| Interface | 3-wire (INC, U/D, CS) |
| Supply | ±5V or 5V single |
| Wiper current | ±1mA max |
| Non-volatile | Yes (remembers position when powered off) |

### MCP41xx / MCP42xx

| Property | Value |
|----------|-------|
| Resistance | 5kΩ, 10kΩ, 50kΩ, 100kΩ |
| Taps | 256 (8-bit resolution) |
| Step size | Total resistance / 255 |
| Interface | SPI |
| Supply | 2.7–5.5V single |
| Channels | 1 (MCP41xx) or 2 (MCP42xx) |
| Wiper current | ±1mA max |

### AD5206 / AD8400 Series

| Property | Value |
|----------|-------|
| Resistance | 10kΩ, 50kΩ, 100kΩ |
| Taps | 256 |
| Interface | SPI |
| Channels | 1 (AD8400), 2 (AD8402), 4 (AD8403), 6 (AD5206) |

## X9C103 — Wiring

```
X9C103              Microcontroller
  VCC ──────────────── 5V (or ±5V for bipolar)
  VSS ──────────────── GND
  INC ──────────────── GPIO (increment/decrement clock)
  U/D ──────────────── GPIO (up/down direction)
  CS ───────────────── GPIO (chip select, active LOW)
  RH ───────────────── High terminal (like pot pin 3)
  RW ───────────────── Wiper (like pot pin 2)
  RL ───────────────── Low terminal (like pot pin 1)
```

### How the X9C Interface Works

```
1. Pull CS LOW (select chip)
2. Set U/D HIGH (increase) or LOW (decrease)
3. Pulse INC LOW → HIGH (one step per pulse)
4. Repeat for total steps
5. Pull CS HIGH to store wiper position
```

```cpp
void digipotStep(int steps, bool up) {
  digitalWrite(CS_PIN, LOW);
  digitalWrite(UD_PIN, up ? HIGH : LOW);
  for (int i = 0; i < steps; i++) {
    digitalWrite(INC_PIN, LOW);
    delayMicroseconds(1);
    digitalWrite(INC_PIN, HIGH);
    delayMicroseconds(1);
  }
  digitalWrite(CS_PIN, HIGH); // store position
}

// Set to 50% (50 steps up from minimum)
digipotStep(50, true);
```

### X9C103 Wiper Position

The wiper has 100 positions (0–99):

| Position | Resistance (RW–RL) | Resistance (RW–RH) |
|----------|-------------------|-------------------|
| 0 | 0Ω (minimum) | 10kΩ |
| 50 | ~5kΩ | ~5kΩ |
| 99 | 10kΩ | 0Ω (maximum) |

Position 0 is the minimum (not necessarily 0Ω — there's a wiper resistance of ~40Ω).

## MCP41100 — Wiring

```
MCP41100            Microcontroller
  VDD ──────────────── 3.3V or 5V
  VSS ──────────────── GND
  CS  ──────────────── GPIO (chip select, active LOW)
  SCK ──────────────── SCK (SPI clock)
  SDI ──────────────── MOSI (SPI data in)
  SDO ──────────────── (not connected for basic use — outputs daisy-chain data)
  P0A ──────────────── High terminal (like pot pin 3)
  P0W ──────────────── Wiper (like pot pin 2)
  P0B ──────────────── Low terminal (like pot pin 1)
```

### SPI Command

Send 1 byte: command (0x11 for write) + 1 byte: value (0–255):

```cpp
void digipotWrite(int value) {
  digitalWrite(CS_PIN, LOW);
  SPI.transfer(0x11);     // write command
  SPI.transfer(value);    // 0–255
  digitalWrite(CS_PIN, HIGH);
}
```

### MCP41xx Wiper Position

256 positions (0–255):

| Value | Resistance (RW–PB) | Resistance (RW–PA) |
|-------|-------------------|-------------------|
| 0 | 0Ω (minimum) | 100kΩ |
| 128 | ~50kΩ | ~50kΩ |
| 255 | 100kΩ | 0Ω (maximum) |

## Applications

### Audio Volume Control

```
Audio in ──┬── C (1µF) ──┬── Digipot RH
                          │
Audio out ──────────────── RW ── Amplifier input
                          │
                         RL ── GND
```

The digipot acts as a voltage divider. C blocks DC from the audio source. The microcontroller adjusts volume via SPI.

**Note:** Standard digipots have limited voltage swing (±5V max for X9C, 0–VDD for MCP41xx). For line-level audio (±1V), this is fine. For higher voltages, use a different approach.

### Adjustable Reference Voltage

```
VREF ── RH ── RW ──┬── ADC reference input
                    │
                   RL ── GND
```

The microcontroller adjusts the reference voltage of an ADC or comparator.

### Programmable Gain

```
Op-amp output ── RH ── RW ──┬── Op-amp inverting input (-)
                             │
                            RL ── GND
```

Changing the digipot value changes the op-amp's feedback resistance, which changes the gain.

## Limitations

| Limitation | What it means |
|------------|---------------|
| Voltage range | X9C: ±5V maximum across RH–RL. MCP41xx: 0V to VDD only. |
| Current limit | Wiper current: ±1mA max. Exceed it and the wiper may fail. |
| Frequency limit | Audio frequencies OK (up to ~20 kHz). RF frequencies will distort. |
| Resolution | 100 steps (X9C) or 256 steps (MCP41xx). Not infinite like a mechanical pot. |
| Wiper resistance | ~40–100Ω even at "0" position — can't go to true 0Ω. |

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Resistance doesn't change | Wrong control sequence (X9C) | Verify INC/U/D/CS timing |
| Resistance doesn't change | Wrong SPI command (MCP41xx) | Check command byte (0x11) |
| Wiper goes to random position on power-up | X9C should remember, but first use is undefined | Initialize to known position at startup |
| Audio distortion | Voltage swing exceeds digipot's range | Use voltage divider before digipot, or use higher-voltage rated digipot |
| Digipot gets hot | Too much current through wiper | Add series resistor to limit wiper current to ±1mA |
| Can't get 0Ω resistance | Wiper resistance is inherent | Accept ~40–100Ω minimum, or design around it |
| Value resets on power cycle (MCP41xx) | No built-in non-volatile memory | Store value in EEPROM and restore at startup |

## Quick Reference

- **X9C103:** 10kΩ, 100 steps, 3-wire interface (INC/U/D/CS), non-volatile
- **MCP41100:** 100kΩ, 256 steps, SPI, 2.7–5.5V, volatile (resets to midpoint)
- **Wiring:** Digipot replaces a mechanical potentiometer pin-for-pin
- **Current limit:** 1mA max through the wiper
- **Voltage limit:** X9C = ±5V, MCP41xx = 0V to VDD only
- **Audio use:** Works for volume control, limited to ±5V or 0–VDD swing
- **Step size:** 10kΩ / 99 ≈ 101Ω per step (X9C103), 100kΩ / 255 ≈ 392Ω per step (MCP41100)
- **Startup:** X9C remembers last position. MCP41xx resets to midpoint (128).
- **No true 0Ω:** Wiper resistance is ~40–100Ω at minimum position.
