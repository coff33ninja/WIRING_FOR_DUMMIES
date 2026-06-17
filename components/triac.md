# Triac & Solid State Relay — Component Reference

## What It Is

A **triac** is a semiconductor switch that can control **AC power**. Unlike a mechanical relay, it has no moving parts — it switches on and off electronically. A **Solid State Relay (SSR)** is a triac with built-in isolation (optocoupler + triac in one package).

## Triac vs Mechanical Relay

| Property | Triac / SSR | Mechanical Relay |
|----------|-------------|------------------|
| Switching speed | Microseconds | Milliseconds |
| Lifespan | Millions of cycles | 10,000–100,000 cycles |
| Moving parts | None | Internal spring contacts |
| AC or DC | AC only (triac turns off at zero cross) | AC and DC |
| Heat generation | Higher (especially in high current) | Low (contacts) |
| Leakage current | Small (when OFF) | Zero (when OFF) |
| Clicking sound | Silent | Audible click |
| Cost | Higher for SSR | Lower |

## How a Triac Works

A triac is like **two thyristors back-to-back**. It conducts current in both directions when triggered.

```
MT2 ──┬──┐
      │  │
      └──┤ Gate ── Trigger signal
      │  │
MT1 ──┴──┘
```

- **MT1** and **MT2** (Main Terminals): The AC power path
- **Gate:** A small current pulse triggers the triac into conduction
- Once conducting, it stays on until the AC current drops near zero (every half-cycle)

This means you need to **re-trigger the gate every half-cycle** (every 8.3ms for 60Hz, every 10ms for 50Hz).

## AC Phase Control (Dimmer)

By triggering the triac at different points in the AC waveform, you control how much power reaches the load:

```
Full power (trigger at 0°):      Half power (trigger at 90°):
╱╲    ╱╲    ╱╲                    ╱╲    ╱╲    ╱╲
╱  ╲  ╱  ╲  ╱  ╲                ╱  ╲  ╱  ╲  ╱  ╲
╱    ╲╱    ╲╱    ╲              ╱    ╲╱    ╲╱    ╲
──────┬────────────────   ──────┬────────────┬────────
      ↑ trigger                  ↑ trigger   ↑ trigger
```

This is how incandescent lamp dimmers and AC motor speed controllers work. LED bulbs and some appliances don't dim well this way — they need trailing-edge or PWM dimmers.

## Optocoupler + Triac (Isolated Trigger)

**Never drive a triac gate directly from a GPIO.** The AC mains is dangerous and the triac gate needs isolation:

```
GPIO ──── R (220Ω) ──── MOC3021 ──── Triac gate
                          (optocoupler)
                         VCC ──── 5V
```

The **MOC3021** is an optocoupler with a triac output — it provides isolation between the 3.3V/5V logic and the AC mains. The **MOC3063** has zero-crossing detection (triggers at the AC zero crossing for lower noise).

## Solid State Relay (SSR)

An SSR is a complete package: optocoupler + triac + protection in one:

```
SSR Module:
  Control side:          Load side:
  + ──── 3-32V DC ────  ──── AC Load ──── AC Line
  - ──── GND         ║   ──── AC Neutral
                      ║  (electrically isolated)
```

### DC Control SSR

| Label | Connection |
|-------|-----------|
| + (or IN+) | 3–32V DC (GPIO + VCC) |
| - (or IN-) | GND |
| AC side | Two terminals for the AC load in series |

3–32V means the SSR triggers anywhere in that range. For a 3.3V microcontroller, connect GPIO directly to the + terminal (the SSR draws very little current from the control side).

## Wiring Examples

### Lamp Control with SSR

```
GPIO ──── SSR(+) ───── SSR          SSR ──┬── Lamp ──── AC Hot
GND ───── SSR(-)     (control)            │
                                          AC Neutral
```

### Motor Control with Triac + MOC3021

```
GPIO ──── 220Ω ──── MOC3021 pin 1
VCC ───── MOC3021 pin 2
                   MOC3021 pin 6 ──── Triac Gate
AC Hot ──┬── Triac MT2
         │   Triac MT1 ──── Motor ──── AC Neutral
         │
         └── R (330Ω) ──── MOC3021 pin 4
```

## Snubber Circuit

A triac driving an inductive load (motor, transformer, pump) needs a **snubber** — a resistor + capacitor in series across the triac. It prevents false triggering from voltage spikes:

```
Triac MT2 ──┬── R (100Ω) ── C (0.1µF) ──┬── Triac MT1
            │                            │
            └────────────────────────────┘
```

Many SSR modules include a snubber. Bare triacs usually need one added.

## Heat Management

| Load current | Heatsink needed? |
|-------------|-----------------|
| < 1A | Usually not |
| 1–5A | Small clip-on heatsink |
| 5–10A | Medium heatsink, forced air may be needed |
| 10–25A | Large finned heatsink |
| 25A+ | Heatsink + fan, or water cooling |

Triacs have a voltage drop of ~1–1.5V when conducting. At 10A, that's 10–15W of heat. That heatsink isn't optional.

## Common Triac Part Numbers

| Part | Max current | Max voltage | Use |
|------|-------------|-------------|-----|
| BT136 | 4A | 600V | Small loads (lamps, fans) |
| BT137 | 8A | 600V | Medium loads |
| BT139 | 16A | 600V | Heavy loads |
| BTA16 | 16A | 600V | Heavy loads (isolated package) |
| BTA41 | 40A | 600V | Industrial loads |

BTA prefix = insulated package (mount directly to heatsink without isolation pad). BT prefix = non-insulated (needs isolation).

## Safety

| Rule | Why |
|------|-----|
| Never touch AC circuit while powered | Lethal voltage |
| Use isolated trigger (MOC3021 or SSR) | GPIOs must not be connected to AC |
| Fuse the load | Overcurrent still applies |
| Heatsink properly | Triac failure = short circuit (load stays on) |
| Snubber for inductive loads | Prevents false triggering from voltage spikes |
| Verify isolation voltage | Optocoupler rated for your mains voltage |

## Quick Reference

- **Triac:** Electronic AC switch. Trigger gate every half-cycle.
- **SSR:** Triac + isolation in one package. Safer, easier to use.
- **Always isolate** GPIO from AC via optocoupler or SSR
- **Zero-crossing SSR** switches at AC zero-cross (less noise, for resistive loads)
- **Random-fire SSR** switches immediately (needed for phase dimming)
- **Triac stays on** until AC current drops to zero — needs trigger every half-cycle
- **Snubber** needed for inductive loads (motors, transformers)
- **Heatsink** required above 1A
- **Neutral is not ground** — AC neutral carries current, but don't mix with DC ground
