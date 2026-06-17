# Crystal Oscillator — Component Reference

## What It Is

A crystal oscillator (usually a **quartz crystal**) is a component that **vibrates at a very precise frequency** when you apply voltage to it. Microcontrollers use it as a heartbeat — every tick of the crystal advances the chip one step.

> **Analogy:** A crystal is like a perfectly tuned tuning fork. Tap it and it rings at exactly one pitch forever. The microcontroller counts these vibrations to know exactly when to execute each instruction.

## Why You Need One

Your ESP32 or Arduino has an **internal oscillator** (RC circuit) that can run without an external crystal. But it's inaccurate:

| Oscillator type | Accuracy | Drift with temperature |
|----------------|----------|----------------------|
| Internal RC (no crystal) | ±1–3% | Significant |
| External ceramic resonator | ±0.5% | Moderate |
| External quartz crystal | ±30–100 ppm (0.003–0.01%) | Minimal |

**Without a crystal:** Serial communication may fail at high baud rates. Timers drift. `delay(1000)` might be 970ms or 1030ms.

## How It Looks

```
       ┌──────┐
       │  ═══  │  ← Metal can (sometimes plastic)
       │  ═══  │
       └──┬┬──┘
          ││
          Pin 1    Pin 2
          (no polarity — either way)
```

**Crystals have no polarity** — you can connect them either way. But they do need **load capacitors** on each pin to ground.

## Wiring to an ESP32

```
ESP32
─────
                ┌──────┐
GPIO 12 (XTAL) ─┤  ═══  ├─ GPIO 13 (XTAL)
                │  ═══  │
                └──┬┬──┘
                   ││
                   ││
              ┌────┘└────┐
              │          │
             22pF      22pF
              │          │
             GND        GND
```

| Crystal frequency | Load capacitor value |
|------------------|---------------------|
| 32.768 kHz (RTC) | 12–15 pF |
| 4–8 MHz | 18–22 pF |
| 10–20 MHz | 15–22 pF |
| 40 MHz (ESP32 main) | 20 pF (internal) |

> **ESP32 note:** The ESP32 has an **internal 40MHz crystal oscillator driver** — you usually don't add your own. The crystal is already on the dev board. You only add external crystals for:
> - **RTC** (32.768 kHz) — for accurate deep-sleep timing
> - **Custom clock** — when building your own PCB without a module

## Common Crystal Frequencies

| Frequency | Used for |
|-----------|----------|
| 32.768 kHz | Real-time clock, low-power sleep timers |
| 4 MHz | Basic Arduino (Uno, Nano) |
| 8 MHz | 3.3V Arduino Pro Mini |
| 12 MHz | USB communication, some dev boards |
| 16 MHz | Standard Arduino clock |
| 20 MHz | Fast Arduino, some PICs |
| 25 MHz | Ethernet controllers |
| 40 MHz | ESP32 main clock (on-module) |

## Ceramic Resonator vs Quartz Crystal

| | Ceramic Resonator | Quartz Crystal |
|--|-----------------|----------------|
| Accuracy | ±0.5% | ±0.001% (30 ppm) |
| Cost | Cheaper | Slightly more |
| Drift | Moderate | Minimal |
| Load caps | Sometimes built-in | Always external |
| Looks like | Blue/orange rectangular block | Silver metal can |

> **For UART/serial that needs to work:** Use a quartz crystal. Ceramic resonators drift enough to cause baud rate errors at high speeds.

## 32.768 kHz RTC Crystal

A watch crystal for low-power timekeeping:

```
ESP32 (Deep Sleep)        32.768 kHz Crystal
──────────────────        ──────────────────
GPIO 32 (RTC_XTAL_P) ────── Pin 1
GPIO 33 (RTC_XTAL_N) ────── Pin 2

Also add:
  12pF ── GPIO 32 ── GND
  12pF ── GPIO 33 ── GND
```

This lets the ESP32's RTC keep accurate time during deep sleep, drawing only ~5µA.

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Load capacitors | Crystal may not start oscillating, or runs at wrong frequency |
| Using wrong load cap value | Frequency off by measurable amount — serial errors |
| No crystal (relying on internal RC) | Timing drifts — `delay()` is inaccurate, serial may fail at 115200 baud |
| Long wires from crystal to MCU | Signal noise, unreliable oscillation |
| Placing crystal near heat source | Frequency shifts with temperature |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| 16 MHz quartz crystal (HC-49) | 1 | For custom Arduino builds |
| 32.768 kHz watch crystal | 1 | For RTC / accurate sleep timing |
| 22 pF ceramic capacitors | 4 | Load caps for MHz crystals |
| 12 pF ceramic capacitors | 2 | Load caps for 32.768 kHz crystal |

> **Pro tip:** If your crystal circuit doesn't oscillate, try swapping the load caps for slightly different values (15–33pF range). Some crystals need different loads than the datasheet suggests.
