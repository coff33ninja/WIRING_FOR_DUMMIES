# H-Bridge / Motor Driver (L298N, L293D) — Component Reference

## What It Is

An H-bridge is a circuit that lets a microcontroller **control a DC motor's direction and speed**. It can drive current in either direction through the motor — forward, backward, stop, and brake.

> **Name origin:** The schematic looks like the letter H. The motor sits on the crossbar, and the four switches form the vertical legs.

```
       VCC
        │
     ┌──┴──┐
     │ S1  │ S2
     │     │
     └──┬──┘
        │
    ┌───┴───┐
    │ MOTOR │
    └───┬───┘
        │
     ┌──┴──┐
     │ S3  │ S4
     │     │
     └──┬──┘
        │
       GND
```

S1 + S4 closed = motor forward. S2 + S3 closed = motor backward. Never close S1+S2 or S3+S4 simultaneously (shoot-through = dead transistors).

## Common Driver ICs

### L298N

| Property | Value |
|----------|-------|
| Max current per channel | 2A |
| Max motor voltage | 12V (up to 46V absolute) |
| Logic voltage | 5V |
| Dropout voltage | ~2V (important — motor sees less than supply) |
| Channels | 2 (can drive 2 DC motors or 1 stepper) |

**L298N module** (the blue board with giant heatsink) includes:
- Terminal blocks for motor wires
- 5V regulator (can power Arduino from motor supply)
- Enable jumper pins (for PWM speed control)

### L293D

| Property | Value |
|----------|-------|
| Max current per channel | 600mA (1.2A peak) |
| Max motor voltage | 36V |
| Logic voltage | 5V |
| Built-in flyback diodes | Yes |
| Channels | 2 (or 1 stepper motor) |

L293D has built-in flyback diodes (the D stands for "damped"). L298N needs external diodes.

## Wiring L298N Module

```
Microcontroller              L298N Module
  GPIO (IN1) ─────────────── IN1
  GPIO (IN2) ─────────────── IN2
  GPIO (ENA/PWM) ─────────── ENA (jumper removed)

Motor power (7–12V) ──────── 12V input
  GND ─────────────────────── GND
  (5V output) ────────────── Optional: powers Arduino from motor supply)

Motor A ──────────────────── OUT1, OUT2
```

**ENA jumper:** With the jumper on, the motor runs at full speed when IN1/IN2 are set. Remove the jumper and connect ENA to a PWM pin to control speed.

## Wiring L293D

```
Microcontroller              L293D
  GPIO ───────────────────── Pin 1 (Enable 1-2)
  GPIO ───────────────────── Pin 2 (Input 1)
  GPIO ───────────────────── Pin 7 (Input 2)
  VCC (motor) ────────────── Pin 8 (VCC2)
  VCC (logic) ────────────── Pin 16 (VCC1)
  GND ────────────────────── Pin 4, 5, 12, 13
Motor A ──────────────────── Pin 3 (Output 1), Pin 6 (Output 2)
```

## Control Logic

| IN1 | IN2 | ENA | Motor behavior |
|-----|-----|-----|----------------|
| HIGH | LOW | HIGH | Forward (full speed) |
| LOW | HIGH | HIGH | Reverse (full speed) |
| HIGH | HIGH | HIGH | Brake (shorted) |
| LOW | LOW | HIGH | Coast (freewheeling) |
| X | X | LOW | Stopped (disabled) |
| PWM | LOW | HIGH | Forward at duty cycle % speed |
| LOW | PWM | HIGH | Reverse at duty cycle % speed |

## Speed Control with PWM

To control motor speed, send a PWM signal to the Enable pin (ENA or ENB):

```
IN1 = HIGH, IN2 = LOW           → direction = forward
ENA = PWM (0–255 on Arduino)    → speed = duty cycle
```

At 50% duty cycle, the motor receives half power (but NOT half voltage — motors are nonlinear).

## Flyback Diodes

When you turn off a motor, the collapsing magnetic field generates a voltage spike that can destroy the driver. Flyback diodes provide a safe path for this current.

- **L293D:** Built-in — no external diodes needed
- **L298N module:** Usually has built-in diodes. If using bare L298N chip, add 4 fast-recovery diodes (1N4007 or 1N5819) per motor

## What NOT to Do

| Don't | Why |
|-------|-----|
| Enable both IN1 and IN2 HIGH for long | Brake mode heats the driver and motor |
| Connect motor directly to GPIO | Not enough current, GPIO pin dies |
| Exceed max current | L293D = 600mA, L298N = 2A per channel |
| Forget common ground | Microcontroller and motor supply need shared GND |
| Switch direction instantly | Stop the motor first (both inputs LOW for 10ms), then reverse |
| Exceed max motor voltage | L298N: 12V nominal, 46V absolute max |

## Quick Reference

- **H-bridge** lets you control direction + speed of DC motors
- **L298N:** 2A per channel, needs external flyback diodes, ~2V dropout
- **L293D:** 600mA per channel, built-in diodes, good for small motors
- **IN1/IN2:** direction control
- **ENA/ENB:** PWM speed control
- **Never short the power supply** — don't enable both inputs HIGH on the same channel
- **Always connect GND** between microcontroller and motor driver
- **Use PWM frequency above 20 kHz** to avoid motor whine
