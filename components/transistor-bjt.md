# Bipolar Junction Transistor (BJT) — Component Reference

## What It Is

A BJT is a **current-controlled switch**. Unlike a MOSFET (which is voltage-controlled), a BJT turns on when you feed a small current into the base pin. That small current controls a much larger current between collector and emitter.

> **Analogy:** Think of a BJT as a lever. You push gently on the handle (small current into Base), and the lever moves a heavy rock (big current flows Collector→Emitter).

## NPN vs PNP

| Type | How it switches | Load connection | Use |
|------|-----------------|-----------------|-----|
| **NPN** | HIGH on Base → current flows Collector→Emitter | Load between VCC and Collector | **Most common — use this** |
| PNP | LOW on Base → current flows Emitter→Collector | Load between Emitter and GND | High-side switching (less common) |

**For almost everything, use NPN.** 2N2222, BC547, BC548, and S8050 are all NPN.

> **See also:** [MOSFET](mosfet.md) — voltage-controlled alternative for higher current. [Transistor Array](transistor-array.md) — ready-made Darlington arrays with flyback diodes built-in.

## The 3 Pins

Looking at the flat face:

```
       ┌───────┐
       │ 2N2222│
       │       │
       └───────┘
         │ │ │
         │ │ └── Emitter (E)
         │ └──── Base (B)
         └────── Collector (C)
```

But the order depends on the part! Different transistor types have different pinouts.

### Common NPN Pinouts

| Part | Pin 1 | Pin 2 | Pin 3 |
|------|-------|-------|-------|
| 2N2222 (TO-92, flat face) | Emitter | Base | Collector |
| BC547/BC548 (TO-92, flat face) | Collector | Base | Emitter |
| S8050 (TO-92, flat face) | Emitter | Base | Collector |

> **ALWAYS check the datasheet.** The pinout isn't standardized. If you wire it wrong, it either doesn't work or gets hot.

### What Each Pin Does

| Pin | Name | Think of it as... |
|-----|------|-------------------|
| **B** | Base | The **tap handle** — small current here controls the big flow |
| **C** | Collector | **Input side** — connects to the load (relay, motor, etc.) |
| **E** | Emitter | **Output side** — connects to ground |

## How It Works (NPN)

```
                       +12V
                        │
                    ┌───┴───┐
                    │ Relay │  ← the load
                    └───┬───┘
                        │
                   ┌────┴────┐
    3.3V ──[1kΩ]──┤ Base    │
                   │  NPN    │
                   │  2N2222 │
                   └────┬────┘
                        │
                       GND
```

- Put **3.3V on Base** (through a resistor) → a small current flows into Base → the transistor opens → current flows through the relay coil → Collector→Emitter → ground → **Relay ON**
- Put **0V on Base** → no base current → transistor is off → no current through relay → **Relay OFF**

## The Base Resistor — CRITICAL

A BJT base is basically a diode connected to ground. Without a base resistor, it would short your GPIO pin to ground and kill it.

**Required:** A 1kΩ resistor between the GPIO pin and the Base.

```
GPIO ──── 1kΩ ──── Base
```

## Why Use a BJT Instead of a MOSFET?

| Use BJT when... | Use MOSFET when... |
|-----------------|-------------------|
| Switching relays under 500mA | Switching motors, fans, LED strips |
| Driving a small buzzer | Driving anything over 1A |
| You have 5V and don't want to buy MOSFETs | You need efficient switching |
| Cost matters (BJTs are cheaper) | Heat matters (MOSFETs run cooler) |

BJT advantage: Very cheap ($0.05), widely available, easy to find.
MOSFET advantage: Handles more current, more efficient (less heat), voltage-controlled.

## The Base Resistor Value

To calculate the base resistor:

```
R = (Vgpio - 0.7V) / (Iload / hFE)

For a relay coil drawing 100mA, with a 2N2222 (hFE ≈ 100):
  Base current needed = 100mA / 100 = 1mA
  R = (3.3 - 0.7) / 0.001 = 2600Ω → use 1kΩ (safe)
```

**Rule of thumb:** 1kΩ for 3.3V logic, 2.2kΩ for 5V logic. This provides enough base current for most small loads.

## Why You Need a Flyback Diode (with relays)

If you're driving a relay coil or solenoid with a BJT, you STILL need a flyback diode. The voltage spike from the coil turning off can destroy the transistor just as easily as a MOSFET.

(See [Diode Reference](diode.md) for details on flyback.)

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Base resistor | GPIO pin is shorted to ground → GPIO pin dies |
| Flyback diode (relay/coil load) | Transistor dies from voltage spikes after a few cycles |
| Correct pinout check | Either nothing happens, or transistor gets hot and dies |

## BJT Sub-Types — Which Transistor for Which Job

### Small Signal (General Purpose)

The most common transistors. Low current (<500mA), low power, cheap.

| Part | Max Current | Max VCE | hFE (gain) | Package | Best For |
|------|------------|---------|------------|---------|----------|
| 2N2222 | 800mA | 40V | 100–300 | TO-92 | **General purpose — the default** |
| BC547 | 100mA | 45V | 110–800 | TO-92 | Small signals, sensor buffering |
| BC548 | 100mA | 30V | 110–800 | TO-92 | Same as 547, lower voltage |
| S8050 | 700mA | 25V | 100–400 | TO-92 | Common in Chinese modules |
| 2N3904 | 200mA | 40V | 100–300 | TO-92 | Industry standard, widely available |
| BC337 | 500mA | 45V | 100–600 | TO-92 | Higher current small signal |

Use these for: relay drivers (small relays), LED drivers, buzzer drivers, logic level conversion.

### Power Transistors

For currents above 500mA. Usually in TO-220 package with a metal tab for heatsink.

| Part | Max Current | Max VCE | Power | Package | Best For |
|------|------------|---------|-------|---------|----------|
| TIP31 | 3A | 40V | 40W | TO-220 | Medium power switching |
| TIP41 | 6A | 40V | 65W | TO-220 | Power switching, audio amps |
| TIP3055 | 15A | 60V | 90W | TO-247 | High current, old but reliable |
| 2N3055 | 15A | 60V | 115W | TO-3 | Classic power transistor (huge) |
| MJE3055 | 10A | 60V | 75W | TO-220 | Modern replacement for 2N3055 |

**Power transistors need heatsinks** above ~1W dissipation. The metal tab is usually connected to the collector — don't let it touch other metal.

### Darlington Transistors

Two transistors inside — enormous gain (hFE ~1000+) but higher voltage drop (~1.4V).

| Part | Max Current | Max VCE | Gain | Package | Best For |
|------|------------|---------|------|---------|----------|
| TIP120 | 5A | 60V | 1000+ | TO-220 | **Most common Darlington** |
| TIP121 | 5A | 80V | 1000+ | TO-220 | Higher voltage |
| TIP122 | 5A | 100V | 1000+ | TO-220 | Highest voltage in series |
| TIP127 | 5A | 100V | 1000+ | TO-220 | **PNP** version (TIP120 series is NPN) |
| ULN2003 | 500mA/ch | 50V | 1000+ | DIP-16 | **7 Darlingtons in one chip** — see transistor-array.md |

**Use Darlington when:** You need high gain from a low-current source (3.3V GPIO into a 5A load without extra driver stage). The voltage drop means more heat.

**Better alternative:** Use a logic-level MOSFET — no base current needed, lower voltage drop, less heat.

### RF Transistors

Designed for radio frequencies. Not for general switching.

| Part | Frequency | Power | Use |
|------|-----------|-------|-----|
| 2N3904 | 250 MHz | 200mW | Not really RF (good up to ~100 MHz) |
| BF199 | 600 MHz | 500mW | RF amplifier, oscillators |
| 2N2222A | 250 MHz | 500mW | VHF, not for UHF |
| BFR96 | 5 GHz | 500mW | UHF, cellular, GPS front-end |

For most hobby RF work, use integrated modules (nRF24L01, LoRa, WiFi) rather than discrete RF transistors.

### Phototransistors

A phototransistor is a BJT that's triggered by light instead of base current. The base pin may not exist (2-pin package) or can be used to bias the sensitivity.

| Part | Package | Peak Wavelength | Use |
|------|---------|-----------------|-----|
| L-51ROPT1D1 | 5mm clear | 940nm (IR) | IR detection, optocouplers |
| PT333-3C | 3mm clear | 940nm | IR receiver, light barrier |
| TEPT5700 | Through-hole | 570nm (green) | Ambient light sensing |

See the optocoupler guide for the most common use — phototransistor inside a chip detecting an internal LED.

## Transistor as Amplifier (Common Emitter)

BJTs aren't just switches — they amplify. A small change in base current creates a large change in collector current:

```
VCC
  │
  Rc (collector resistor)
  │
  ├─── Output (amplified signal)
  │
  └─── Collector
       │
       NPN transistor
       │
  Input ── Rb (base resistor) ── Base
       │
      Emitter ── GND
```

- **Voltage gain** ≈ Rc / Re (if emitter has a resistor to GND)
- **Input impedance:** ~1–10kΩ (low — loads the signal source)
- **Phase:** Output is inverted (180° out of phase)

For audio amplification, use an op-amp or a dedicated audio amplifier IC. The BJT common-emitter stage is useful as a simple pre-amp for piezo sensors, electret microphones, and IR receivers.

## SMD BJT Packages — What You'll See

| SMD Package | Size (mm) | Through-hole equivalent | Power |
|-------------|-----------|------------------------|-------|
| SOT-23 | 2.9 × 1.3 | BC847 (same as BC547) | 250mW |
| SOT-223 | 6.5 × 3.5 | Medium power | 1–2W |
| DPAK (TO-252) | 6.5 × 6.1 | Power (~TIP31 level) | ~10W |
| D2PAK (TO-263) | 10 × 9 | High power (~TIP41 level) | ~50W |
| SOT-89 | 4.5 × 2.5 | Medium power | ~1W |

**Popular SMD BJTs:** BC847 (NPN, like BC547), BC857 (PNP, like BC557), MMBT3904 (NPN, like 2N3904), MMBT2222A (NPN, like 2N2222).

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Base resistor | GPIO pin is shorted to ground → GPIO pin dies |
| Flyback diode (relay/coil load) | Transistor dies from voltage spikes after a few cycles |
| Correct pinout check | Either nothing happens, or transistor gets hot and dies |
| Heatsink (power transistor) | Transistor overheats, thermal runaway → dead |
| Base current calculation | Transistor doesn't saturate → runs hot even with low load |

## Quick Reference

```
Common NPN transistors:
  2N2222  → 800mA max, general purpose
  BC547   → 100mA max, small signal
  BC548   → 100mA max, similar to 547
  S8050   → 700mA max, common in modules
  2N3904  → 200mA max, industry standard
  BC337   → 500mA max, higher current small signal
  TIP120  → 5A Darlington, high gain
  TIP41   → 6A, power switching (with heatsink)

Always use a base resistor: 1kΩ for 3.3V, 2.2kΩ for 5V
Always add a flyback diode for relay/coil loads

For higher current or simpler drive: use a logic-level MOSFET
For multi-channel: use a ULN2003 transistor array
```
