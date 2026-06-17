# MOSFET — Component Reference

> **See also:** [BJT Transistor](transistor-bjt.md) — current-controlled alternative. [Transistor Array](transistor-array.md) — multi-channel driver with built-in protection.

## What It Is

A MOSFET is a **voltage-controlled switch**. It has no moving parts — applying voltage to one pin makes a connection between the other two pins. It's the solid-state equivalent of a light switch, but controlled by electricity instead of your finger.

> **Why not just use a regular switch?** Because a microcontroller can only provide 3.3V and a few milliamps. A MOSFET lets that tiny signal control big power (12V, multiple amps) safely.

## N-Channel vs P-Channel

| Type | How it switches | Load goes on | Use |
|------|-----------------|--------------|-----|
| N-channel | HIGH on gate → connects Source to Drain | Drain side | Low-side switching (ground switching) — most common |
| P-channel | LOW on gate → connects Source to Drain | Source side | High-side switching (power switching) |

**For almost all hobby projects, you want N-channel MOSFETs.** They're cheaper, more available, and have lower resistance (Rds(on)).

## The 3 Pins

Looking at the flat face with text:

```
        IRF3205 / IRLZ44N / etc.
       ┌─────────────────────┐
       │                     │
       │    PART NUMBER      │
       │                     │
       └─────────────────────┘

           │     │     │
           G     D     S
         Gate  Drain Source
```

But be careful — **pinouts vary between parts!** Always check the datasheet. A common trap: the IRF3205 and IRLZ44N have different pin orders.

### IRF3205 / IRLZ44N (typical TO-220 package)

| Position | Pin | Think of it as... |
|----------|-----|-------------------|
| **Left** | Gate | The **light switch handle** — voltage here turns the switch on/off |
| **Middle** | Drain | **Input side** — connects to the device you're controlling (fan, motor, etc.) |
| **Right** | Source | **Output side** — connects to ground |

### Common Pinout Pitfalls

```
IRF3205 / IRLZ44N / IRLB8743:
    Left  = Gate
    Middle = Drain
    Right = Source

IRF520 module (the pre-built board):
    The screw terminals change the order — always check the silkscreen labels.
```

**ALWAYS verify with a multimeter or datasheet.** Different manufacturers sometimes swap Drain and Source on the same-looking package. If your MOSFET gets hot instantly, you probably swapped Drain and Source.

## How It Works

- Put **3.3V (or more) on Gate** → connection between Drain and Source opens → current flows
- Put **0V on Gate** → connection between Drain and Source closes → no current flows

```
N-channel MOSFET:

    12V ──── Device (fan, motor, etc.)
                  │
                  │
              ┌───┴───┐
              │ D     │
       3.3V ──┤ G     │
              │ S     │
              └───┬───┘
                  │
                 GND
```

## Why You Need a Pull-Down Resistor

A MOSFET gate is like a **tiny capacitor** — it can hold a charge. When your microcontroller boots up, the GPIO pins aren't doing anything useful for a split second. During that time, the gate can pick up random electrical noise and partially turn on the MOSFET.

> **Without a pull-down (10kΩ from Gate to GND):** The fan might spin briefly at boot, or worse, sit in a "half on" state where the MOSFET gets hot and slowly dies.

**Required:** 10kΩ resistor from Gate to GND.

## Why You Need a Gate Resistor

A MOSFET gate also acts like a **tiny capacitor** when you first apply voltage. If you connect a GPIO pin directly, the initial current surge can:
1. Damage the GPIO pin
2. Create electrical noise that resets the microcontroller

> **Required:** 220Ω resistor between the GPIO pin and the Gate.

## Why You Need a Flyback Diode

If you're controlling a **motor, fan, relay, solenoid, or any coil**, you MUST put a flyback diode across the load. When you turn off a coil, it generates a voltage spike in the opposite direction that can punch through the MOSFET and kill it.

(See [Diode Reference](diode.md) for details.)

## Logic-Level vs Standard MOSFET

| Type | Gate voltage to fully turn on | Example |
|------|-------------------------------|---------|
| Standard | 10V | IRF3205, IRF540, IRFZ44N |
| Logic-level | 3.3V or 5V **<-- USE THESE WITH ESP32** | **IRLZ44N, IRLB8743, IRL540N** |

**CRITICAL:** A standard MOSFET like the IRF3205 needs 10V on the gate to fully turn on. An ESP32 only outputs 3.3V. The MOSFET might work a little bit (gets warm) but won't fully turn on. **Logic-level MOSFETs** are designed to work at 3.3V/5V.

> **If you already bought IRF3205s:** They still work with 3.3V — just not perfectly. They'll pass a few amps but run warmer. For a small fan, it's fine. For a big motor, use logic-level.

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Pull-down resistor (10kΩ) | MOSFET may turn on randomly at boot, device may twitch |
| Gate resistor (220Ω) | ESP32 GPIO may get damaged over time, noise on power rail |
| Flyback diode | MOSFET dies from voltage spikes — often within minutes |
| Heatsink (for >1A) | MOSFET overheats, resistance increases, more heat → thermal runaway → dead |

## Quick Reference

```
For ESP32 / 3.3V microcontrollers → use IRLZ44N or IRLB8743 (logic-level)
For relays/valves < 1A            → IRF3205 works fine (gets a little warm)
For big loads > 5A                → IRLB8743 or external driver

Pin order (check datasheet!):
  Common N-channel TO-220:
    Pin 1 = Gate
    Pin 2 = Drain (also the metal tab!)
    Pin 3 = Source
```
