# Relay Module — Wiring for Dummies

## What Is a Relay?

A relay is an **electrically operated mechanical switch**. When you apply power to the coil inside, it creates a magnetic field that physically moves a metal contact to make or break a connection.

> **Analogy:** It's like a light switch that you control with electricity instead of your finger. A tiny current (from the ESP32) switches a big current (120V/240V mains or 12V high-power loads).

## Relay Module vs Bare Relay

### Bare Relay (just the relay itself)

```
   ┌─────────────────────┐
   │                     │
   │   Coil pins         │
   │    │     │          │
   │   (+)   (−)         │
   │                     │
   │  COM  NO   NC       │
   │   │    │    │       │
   └─────────────────────┘

   Coil pins: Apply voltage to make the switch move
   COM:     Common terminal
   NO:      Normally Open (open when relay off, closes when on)
   NC:      Normally Closed (closed when relay off, opens when on)
```

**Needs external:** Flyback diode, transistor/MOSFET driver, base/gate resistor.

### Relay Module (pre-built board)

```
   ┌──────────────────────┐
   │                      │
   │  [LED] [LED]         │
   │                      │
   │  VCC GND IN          │
   │                      │
   │  COM  NO   NC        │  ← Screw terminals
   │                      │
   └──────────────────────┘
```

**Already has:** Flyback diode, driver transistor, base resistor, status LED. You just need VCC, GND, and a GPIO pin.

> **Recommendation:** For beginners, **use a pre-built relay module**. The bare relay needs 6 external parts; the module needs only 3 wires.

## The Three Switch Contacts

| Contact | Name | Behavior |
|---------|------|----------|
| **COM** | Common | The middle pin — connects to either NO or NC |
| **NO** | Normally Open | **Broken** when relay is OFF. **Connected** to COM when relay is ON |
| **NC** | Normally Closed | **Connected** to COM when relay is OFF. **Broken** when relay is ON |

### What to Use

```
                    Normally OFF (pump, fan, light, alarm)
                    ─────────────────────────────────────
                    Power ──── COM │
                                  │  When relay OFF: nothing
                                  │  When relay ON:  power flows to device
                    NO ───────────┴── Device

                    Normally ON (failsafe cooling fan, safety valve)
                    ───────────────────────────────────────────────
                    Power ──── COM │
                                  │  When relay OFF: device runs
                                  │  When relay ON:  device stops
                    NC ───────────┴── Device
```

**Use NO for almost everything.** You want the load to be off when the relay is off.

## Wiring a Relay Module

### 5V Relay Module with ESP32

```
ESP32              Relay Module
────               ────────────
5V (or 3.3V?) ────── VCC
GND ──────────────── GND
GPIO ─────────────── IN

                   Screw terminals:
                   COM ─────── Power (+) to load
                   NO  ─────── Load (+) input
                   (Load GND goes to power supply GND)
```

> **Important:** Most 5V relay modules **don't work reliably at 3.3V**. The coil needs 5V to close. You can:
> 1. Power the relay module with 5V, and use a 3.3V GPIO to trigger it
> 2. Check if your module has an optocoupler (most do) — the GPIO can be 3.3V
> 3. Don't power a 5V relay module from the ESP32's 3.3V pin — it won't have enough current

### Powering the Relay Module

A relay coil draws about 70–100mA when energized. If you turn on multiple relays:

- **One relay:** Powered from the ESP32's 5V pin (if using USB power) — fine
- **Multiple relays:** Use an external 5V supply. The ESP32's voltage regulator can't supply 500mA for 5 relays.

```
External 5V supply:
  5V  ────── Relay VCC
  GND ────── Relay GND ────── ESP32 GND (must share ground!)
  
ESP32:
  3.3V ────── not connected to relay VCC
  GPIO ────── Relay IN
  GND  ────── Relay GND (and external supply GND)
```

## Optoisolated vs Non-Isolated Relay Modules

> **Full component reference:** See [Optocoupler Reference](../components/optocoupler.md) for how optoisolation works, PC817 pinout, and input resistor values.

### Optoisolated (recommended)

The module has a **tiny LED + light sensor** (optocoupler) between the GPIO pin and the relay circuit. There is no electrical connection — the signal travels as light.

```
GPIO ──→ Optocoupler LED ──light──→ Phototransistor ──→ Relay coil
         └────── No electrical connection ──────┘
```

**Advantage:** If the relay arcs or the load surges, the high voltage CANNOT reach your ESP32. Your $5 microcontroller is protected.

### Non-Isolated

The GPIO pin is directly connected (through a transistor) to the relay coil.

**Disadvantage:** If the relay dies or arcs, the high voltage can travel back through the circuit and kill your ESP32.

> **Check your module:** If you see two separate IC chips (one small 4-pin = optocoupler, one 3-pin = transistor), it's optoisolated. If you see only one 3-pin transistor, it's not.

## Inductive Loads and Arcing

Relays are mechanical. When the contacts open, an **arc** can form between them — that's the tiny blue spark you sometimes see. This arc:

1. Wears out the contacts over time (rated for ~100,000 cycles)
2. Creates electrical noise
3. Can weld the contacts shut if the load is too big

### Rated for Your Load

| Relay rating | What it can switch |
|-------------|-------------------|
| 10A @ 125VAC | Standard household lamp, fan, small appliance |
| 10A @ 30VDC | Car accessories, LEDs, pumps |
| 5A @ 250VAC | Most home electronics |

**Don't exceed the rating.** A 5A relay switching a 12A load = welded contacts and a permanently ON device. Use a contactor or higher-rated relay for big loads.

## Wiring a Bare Relay (If You Must)

If you're using a bare relay instead of a module:

```
ESP32 GPIO ──[1kΩ]── Base (2N2222)
                        │
                    Collector ───┐
                        │        │
                    Emitter ── GND
                                 │
                   +12V ──────┬──┴── Relay coil (+)
                              │
                          Relay coil (−) ─── Collector
                              
                          Flyback diode
                          (stripe toward +12V)
                          ┌─────────────────┐
                          │ 1N4007           │
                          │           stripe │
                          └─────────────────┘
```

(See [BJT Reference](../components/transistor-bjt.md) and [Diode Reference](../components/diode.md) for details.)

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Flyback diode (bare relay) | Transistor/MOSFET dies from coil voltage spike |
| Base resistor (bare relay) | GPIO pin is shorted through transistor base → dead GPIO |
| Common ground | Relay won't trigger — no reference voltage |
| Adequate power supply | Relay chatters (rapid on/off), doesn't fully engage |
| External 5V for multi-relay | ESP32 resets when relay tries to engage |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| 1-channel 5V relay module | 1 | Optoisolated preferred — check for optocoupler |
| OR: Bare relay (SRD-05VDC-SL-C) | 1 | If you want to build from scratch |
| OR: 2N2222 transistor | 1 | For bare relay driver |
| OR: 1N4007 diode | 1 | Flyback for bare relay |
| OR: 1kΩ resistor | 1 | Base resistor for bare relay |
| Jumper wires | 1 set | M-F for module |
| External 5V supply | 1 | For multiple relays or high coil current |

## See Also

- [ac-vs-dc](/fundamentals/ac-vs-dc)
- [reading-schematics](/fundamentals/reading-schematics)
- [grounding-decoupling](/fundamentals/grounding-decoupling)
- [multimeter](/fundamentals/multimeter)
- [ohm-law](/fundamentals/ohm-law)
- [soldering](/fundamentals/soldering)
- [connectors-wire](/fundamentals/connectors-wire)
