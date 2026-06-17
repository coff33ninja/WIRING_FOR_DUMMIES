# IR Receiver & IR LED — Component Reference

## What It Is

An **IR (infrared) receiver** detects modulated infrared light from a remote control. An **IR LED** emits infrared light. Together they give your project remote control capability.

IR receivers are the standard 3-pin component (VS1838, TSOP382, TSOP4838) that outputs a **demodulated digital signal** — the 38kHz carrier is already filtered out, so the microcontroller sees clean HIGH/LOW pulses.

## IR Receiver Pinout

```
  ┌──┐
  │  │
OUT│  │GND
  │  │
  └──┘
  VCC

Viewed from the front (bulge facing you):
Left:   OUT (data to microcontroller)
Center: GND
Right:  VCC (3.3V or 5V)
```

Check the datasheet — pinout varies between manufacturers.

## Wiring the Receiver

```
IR Receiver          Microcontroller
  VCC ──────────────── 3.3V or 5V
  GND ──────────────── GND
  OUT ──────────────── GPIO (digital input)

Optional: 10kΩ pull-up resistor from OUT to VCC (some receivers need it)
```

Most 38kHz receivers work at both 3.3V and 5V. No level shifting needed.

## How IR Remote Control Works

### Modulation

IR remotes use a **38kHz carrier** — the IR LED blinks at 38,000 times per second. This prevents interference from sunlight and other IR sources (which are steady, not modulated).

```
Carrier (38kHz):    ╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲
Data bit "0":       ────────________
Data bit "1":       ────____
```

The receiver chip demodulates this: it filters out the 38kHz carrier and outputs the data signal as clean digital HIGH/LOW pulses.

### Protocols

| Protocol | Used by | Bit length | Features |
|----------|---------|------------|----------|
| NEC | Most Chinese remotes | 32 bits | 8-bit address + 8-bit inverted address + 8-bit command + 8-bit inverted command |
| Sony SIRC | Sony TVs | 12, 15, or 20 bits | 5-bit address + 7-bit command |
| RC-5 | Philips | 14 bits | Toggle bit + 5-bit address + 6-bit command |
| RC-6 | Philips | 20+ bits | Leader + mode + address + command |
| Samsung | Samsung TVs | 32 bits | Similar to NEC with different timing |

**NEC protocol** is the most common in hobby projects (cheap remotes).

## Library

Use the **IRremote** library (by shirriff / z3t0 / ArminJo):

```cpp
#include <IRremote.h>
const int RECV_PIN = 11;
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup() {
  irrecv.enableIRIn();  // start receiver
}

void loop() {
  if (irrecv.decode(&results)) {
    Serial.println(results.value, HEX);  // print code
    irrecv.resume(); // receive next value
  }
}
```

## IR LED (Transmitter)

An IR LED looks like a regular LED but is **transparent or slightly purple** (not clear or colored). It emits infrared light at ~940nm.

### Wiring

```
GPIO (PWM) ──── 100Ω ──┬── IR LED anode (+)
                        │
                        └── IR LED cathode (-) ── GND
```

The 100Ω resistor limits current to ~30mA at 3.3V or ~40mA at 5V. IR LEDs can handle more current than visible LEDs (up to 50–100mA pulsed).

**38kHz carrier:** The IR LED needs to be pulsed at 38kHz. Use hardware PWM or the IRremote library's `irsend.sendNEC()` which generates the carrier automatically.

### Transmitter Circuit

```
GPIO (signal) ──── 1kΩ ──┬── NPN base (2N2222)
                          │
                          ├── Collector ── IR LED anode
                          │
Emitter ── GND            ├── IR LED cathode
                           │
              VCC ──────── R (100Ω) ─────┘
```

A transistor driver is recommended for longer range or multiple IR LEDs.

## Range

| Configuration | Typical range |
|---------------|---------------|
| One IR LED, direct GPIO | 1–3m |
| One IR LED, transistor driver | 3–5m |
| Two IR LEDs in series | 5–10m |
| High-power IR LED + lens | 10–50m |

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| No signal received | Wrong wiring | Check pinout — OUT is not VCC |
| No signal received | Wrong carrier frequency | Some remotes use 36kHz or 40kHz instead of 38kHz |
| Intermittent reception | Sunlight or LED interference | Shield receiver from direct light |
| Very short range | IR LED not driven hard enough | Use transistor driver, reduce resistor value |
| Constant garbage data | Receiver picking up 60Hz from room lights | Incandescent/LED lights flicker at 60/120Hz — shield receiver |
| Works with some remotes but not others | Different protocol | Check if the remote uses NEC, Sony, RC-5, etc. |

## Quick Reference

- **Receiver:** 3 pins — VCC, GND, OUT. 38kHz carrier frequency demodulated internally.
- **OUT is digital:** HIGH when no signal, LOW when IR is detected (active LOW on most receivers)
- **Library:** IRremote — handles NEC, Sony, RC-5, RC-6, Samsung protocols
- **IR LED:** Transparent/purple LED, 940nm wavelength, 100Ω series resistor
- **38kHz carrier:** Required for all IR remotes. Hardware PWM or library generates it.
- **Range:** Usually 3–10m. Use transistor driver for longer range.
- **Line of sight:** IR is directional — the receiver needs to "see" the remote
- **Sunlight:** Bright sunlight can overwhelm the receiver. Add shielding or use modulated signals.
