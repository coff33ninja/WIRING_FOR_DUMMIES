# Transistor Array (ULN2003 / ULN2803) — Component Reference

> **See also:** [BJT Transistor](transistor-bjt.md) — the underlying Darlington pair theory. [MOSFET](mosfet.md) — alternative for higher-current switching.

## What It Is

A transistor array is multiple transistors in one package with all the supporting components built-in. The **ULN2003** is the most famous — 7 Darlington transistor pairs with flyback diodes, ready to drive inductive loads like relays, motors, and solenoids.

```
          ┌─┬─┬─┬─┬─┬─┬─┬──┬─┬─┬─┬─┬─┬─┬─┬─┐
  IN1 ──┤1│ │  │  │  │  │  │  │  │  │  │  │  │  │  │16├── COM
  IN2 ──┤2│  │  │  │  │  │  │  │  │  │  │  │  │  │15├── OUT1
  IN3 ──┤3│   │  │  │  │  │  │  │  │  │  │  │  │14├── OUT2
  IN4 ──┤4│    │  │  │  │  │  │  │  │  │  │  │13├── OUT3
  IN5 ──┤5│     │  │  │  │  │  │  │  │  │  │12├── OUT4
  IN6 ──┤6│      │  │  │  │  │  │  │  │  │11├── OUT5
  IN7 ──┤7│       │  │  │  │  │  │  │  │10├── OUT6
  GND ──┤8│        │  │  │  │  │  │  │  │ 9├── OUT7
          └─────────── ULN2003 ───────────┘
```

Each channel:
```
IN ──┬── 2.7kΩ ── base (first transistor)
     │              │
     7.2kΩ ── GND   └── emitter (common GND)
     │
     └── collector (first) ── base (second) ── collector ── OUT
                                 emitter ── GND
```

The Darlington pair gives **very high gain** (~1000×) — a tiny input current switches a large output current.

## Why Use ULN2003 Instead of Individual Transistors

| | Individual BJT (2N2222) | ULN2003 |
|--|------------------------|---------|
| Channels | 1 | 7 in one chip |
| Gain | ~100–300 | ~1000 (Darlington) |
| Base resistor | Need external | **Built-in** (2.7kΩ) |
| Base pull-down | Need external | **Built-in** (7.2kΩ) |
| Flyback diode | Need external | **Built-in** (for every output) |
| Max output current | 800 mA | 500 mA per channel |
| Max output voltage | 40V | 50V |
| PCB space | Lots (7 transistors + resistors + diodes) | One 16-pin DIP |
| Cost | ~$0.10 × 7 + passives | $0.50 |

**The ULN2003 is a complete driver solution** — add power and signals, connect loads. No external components needed for most applications.

## Pinout

| Pin | Name | Function |
|-----|------|----------|
| 1–7 | IN1–IN7 | Inputs (from microcontroller GPIO, active HIGH) |
| 8 | GND | Common ground |
| 9 | OUT7 | Output 7 (open-collector, active LOW) |
| 10 | OUT6 | Output 6 |
| 11 | OUT5 | Output 5 |
| 12 | OUT4 | Output 4 |
| 13 | OUT3 | Output 3 |
| 14 | OUT2 | Output 2 |
| 15 | OUT1 | Output 1 |
| 16 | COM | Common flyback diode cathode (connect to load VCC) |

## How to Wire It

### Driving a Relay

```
5V ── relay coil ──┬── OUT1 (pin 15)
                    │
ULN2003              │
IN1 (pin 1) ──┬──────┘
              │
              └── GPIO from microcontroller
              │
            GND (pin 8) ── GND
            COM (pin 16) ── 5V (same as relay supply)
```

**The COM pin is critical** — connect it to the positive supply of whatever you're switching. This connects the built-in flyback diodes to the correct voltage.

### Driving a Stepper Motor (28BYJ-48)

This is the most common use — the 28BYJ-48 5V stepper motor comes with a ULN2003 driver board:

```
GPIO 1 ── IN1 ── OUT1 ── Motor coil orange
GPIO 2 ── IN2 ── OUT2 ── Motor coil yellow
GPIO 3 ── IN3 ── OUT3 ── Motor coil pink
GPIO 4 ── IN4 ── OUT4 ── Motor coil blue
                    COM ── 5V (motor supply)
                  VCC(motor) ── 5V
```

The remaining 3 channels (IN5–IN7) are unused in this application.

### Driving Multiple LEDs

```
VCC ── 5V
      │
      ├── 220Ω ── LED1 ── OUT1
      ├── 220Ω ── LED2 ── OUT2
      ├── 220Ω ── LED3 ── OUT3
      ...
GPIO ── IN1–IN7 (HIGH = LED on, LOW = LED off)
```

The ULN2003 can sink up to 500mA per channel. For LEDs at 20mA, you could drive 7 LEDs directly. But for just 7 LEDs, individual transistors are cheaper — the ULN2003 shines with inductive loads.

## ULN2003 vs ULN2803

| | ULN2003 | ULN2803 |
|--|---------|---------|
| Channels | 7 | 8 |
| Package | DIP-16, SOIC-16 | DIP-18, SOIC-18 |
| Max current | 500 mA/channel | 500 mA/channel |
| Max voltage | 50V | 50V |
| Pinout | 1–7 IN, 9–15 OUT | 1–8 IN, 11–18 OUT |
| Input logic | **5V logic** (for 5V microcontrollers) | Same |
| Suffix A (e.g., ULN2003A) | Higher current rating | Same |

**The ULN2003 is NOT 3.3V compatible** — the input threshold is ~2.4V. For 3.3V microcontrollers (ESP32, RP2040), use the **ULN2003LV** (low-voltage version) or add a transistor buffer. In practice, the standard ULN2003 often works with 3.3V logic but without full guaranteed switching.

For 3.3V systems, consider:
- **ULN2003LV** — designed for 1.8–5V logic
- **TPIC6B595** — 8-channel sink driver with shift register, 3.3V compatible
- **MOSFET arrays** (like SI4902, DMP4050) — better for 3.3V

## Internal Flyback Diodes — How They Work

Each output has a diode from the output pin to COM:

```
OUT ──┬── Load ── VCC
      │
      ├── (parasitic inductance of load creates reverse spike when turned off)
      │
      └──┬── Diode ── COM ── VCC
         │
         (when voltage on OUT rises above VCC + 0.7V, diode conducts to VCC)
```

Without this diode, turning off an inductive load (relay, motor, solenoid) creates a voltage spike of hundreds of volts — destroying the transistor. The ULN2003's built-in diodes clamp this spike to VCC + 0.7V.

**Connect COM to the load supply voltage** for this to work. If COM is floating, the flyback diodes don't protect anything.

## Common Applications

| Application | Why ULN2003 | Wiring |
|-------------|-------------|--------|
| 28BYJ-48 stepper motor | It's sold as a driver board for this | 4 inputs, 4 outputs, COM to 5V |
| Relay bank (7 relays) | Drives relays directly, flyback diodes built-in | IN→GPIO, OUT→relay, COM→relay supply |
| 7-segment display (common anode) | Sinks segments directly | IN→GPIO, OUT→segment cathodes, COM→VCC |
| Solenoid array | All protection built-in | IN→GPIO, OUT→solenoid, COM→solenoid supply |
| Lamp/LED bank | High-current sink driver | IN→GPIO, OUT→load, COM→VCC |

## ULN2003A Variant

The ULN2003A is identical to ULN2003 but with slightly higher current rating per channel — typically 500mA continuous vs 350mA for the standard version. If buying, get the "A" version.

| Part | Max Continuous per Channel | Max Peak per Channel |
|------|---------------------------|---------------------|
| ULN2003 | 350 mA | 500 mA |
| ULN2003A | 500 mA | 600 mA |
| ULN2803A | 500 mA | 600 mA |

All channels combined should not exceed the package limit — typically ~2.5A total (the DIP package can't dissipate more).

## Quick Reference

- **ULN2003** = 7 Darlington transistor pairs with built-in base resistors and flyback diodes
- **Input:** Active HIGH — GPIO pin directly drives it (no external resistor needed)
- **Output:** Open-collector, active LOW — load connects between power supply and output
- **COM pin:** MUST be connected to the load's positive supply (for flyback diode protection)
- **Max per channel:** 500 mA (continuous)
- **Max total package:** ~2.5A (check your part)
- **Max voltage:** 50V on outputs
- **Input threshold:** ~2.4V (works with 5V logic, marginal with 3.3V — use ULN2003LV for 3.3V)
- **Typical uses:** Stepper motors (28BYJ-48), relay drivers, solenoid drivers, LED drivers
