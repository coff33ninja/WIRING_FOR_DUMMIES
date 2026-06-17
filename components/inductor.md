# Inductor — Component Reference

## What It Is

An inductor is a **coil of wire** that stores energy in a magnetic field. When current flows through it, it creates a magnetic field around the coil. When the current tries to change (turn on or off), the inductor **resists that change** — it tries to keep current flowing the way it was.

> **Analogy:** An inductor is like a heavy flywheel on a engine. It takes effort to get it spinning (current starts flowing), but once it's spinning, it wants to keep going. If you try to stop it suddenly (turn off the current), it pushes back and keeps turning. The bigger the flywheel, the harder it resists changes.

## Inductors vs Capacitors

People often confuse them because both store energy:

| Property | Inductor | Capacitor |
|----------|----------|-----------|
| Stores energy in | Magnetic field | Electric field |
| Resists changes in | Current (smooth out current) | Voltage (smooth out voltage) |
| DC behavior | Looks like a wire (low resistance) | Looks like an open circuit (no DC flow) |
| AC behavior | Looks like a resistor (impedance) | Looks like a short circuit (passes AC) |

> **Simple rule:** Capacitors smooth out voltage bumps. Inductors smooth out current bumps.

## Where You Find Inductors in Everyday Projects

### 1. Motors, Fans, and Relays (the most common)

Any device with a coil of wire inside is an inductor:

- **DC fans** — the motor windings are coils
- **DC motors** — same thing
- **Relay coils** — the electromagnet that moves the switch
- **Solenoids** — door locks, valves, linear actuators
- **Transformers** — two or more inductors sharing a magnetic core

When you turn OFF any of these, the collapsing magnetic field generates a **voltage spike in the opposite direction**. This is called **inductive kick**, **flyback**, or **back-EMF**.

### 2. Buck Converters (voltage regulators)

A buck converter uses an inductor as a **temporary energy storage tank**. The switching MOSFET pulses current into the inductor, which stores it magnetically, then releases it at a lower voltage.

```
Buck converter simplified:
  Input ──→ Switch ──→ Inductor ──→ Output
                         │
                       Capacitor
                         │
                        GND
  
  The inductor and capacitor together smooth the pulses into steady DC.
```

This is why buck converters are so efficient — the inductor stores and releases energy instead of burning it off as heat (like a linear regulator does).

### 3. Audio Filters

Inductors + capacitors make **crossover networks** in speakers, sending high frequencies to tweeters and low frequencies to woofers.

## The Flyback Problem (and the Diode Solution)

When current flows through an inductor and you **suddenly disconnect power**, the magnetic field collapses and creates a voltage spike that can be **hundreds of volts** — even from a 12V supply.

```
Current flowing:    +12V ──→ [Inductor] ──→ GND
                    (magnetic field builds up)

Power disconnected: +12V ──X  [Inductor] ──→ ???
                    (magnetic field collapses)
                    Voltage spike goes in the OPPOSITE direction
```

This spike WILL destroy transistors, MOSFETs, and microcontrollers connected to the coil. The fix is a **flyback diode**:

> **See [Diode Reference](diode.md)** for how flyback protection works.

The diode is placed **across the inductor** (or motor/fan/relay coil) with the stripe (cathode) toward the positive side. It gives the voltage spike a safe path to circulate until the energy dissipates.

```
      +12V
        │
    ┌───┴───┐
    │ Motor │
    └───┬───┘
        │
    ┌───┴───┐
    │ 1N4007│←-- Flyback diode
    │  │    │    Stripe → +12V
    └──┐───┘
       │
    ┌──┴───┐
    │ MOSFET │
    └───────┘
        │
       GND
```

## Inductors in Power Supply Filtering

An inductor on a power line acts as a **low-pass filter** — it lets DC pass through but resists AC noise. You'll sometimes see small inductors (called **ferrite beads**) on USB cables or power wires:

```
Power In ──╔══╗── Power Out → smooth DC
           ║  ║
           ╚══╝
          Ferrite bead
          (tiny inductor that blocks high-frequency noise)
```

These are common on:
- USB cables (the little cylinder near the connector)
- Power supply output wires
- Motor wires (to reduce noise radiated back into the circuit)

## Units and Values

Inductance is measured in **henries (H)**. Most hobby inductors are much smaller:

| Unit | Value | Used for |
|------|-------|----------|
| 1µH (microhenry) | 0.000001 H | High-frequency circuits, buck converters |
| 10–100µH | 0.00001–0.0001 H | Typical buck converter inductors |
| 1mH (millihenry) | 0.001 H | Audio filters, lower frequency |
| 1H+ | 1 H | Power supply filters, heavy transformers |

## What Happens If You Skip Understanding This

| Scenario | Without understanding | With understanding |
|----------|---------------------|-------------------|
| Connecting a motor directly to a GPIO pin | GPIO pin dies from back-EMF | You use a MOSFET + flyback diode |
| Driving a relay without a flyback diode | Transistor dies after a few cycles | You add the 1N4007 and it works forever |
| Building a buck converter without inductor | Short circuit, smoke, and fireworks | The inductor is the core component that makes it work |
| Ignoring flyback on a solenoid valve | MOSFET fails on the first use | Diode protects the MOSFET |

## Quick Reference

```
Inductors in hobby projects:
  Coils = motors, fans, relays, solenoids, transformers

Every coil needs:
  1. A transistor/MOSFET to control it (GPIO can't supply enough current)
  2. A flyback diode (1N4007) across the coil to absorb the voltage spike

Flyback diode rule:
  Stripe (cathode) → Positive supply side
  Plain (anode)    → Ground/transistor side

Buck converter inductor:
  Energy storage element — without it, it's not a buck converter
```
