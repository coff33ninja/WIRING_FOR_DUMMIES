# Wiring for Dummies

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![GitHub Repo](https://img.shields.io/badge/GitHub-WIRING__FOR__DUMMIES-181717?logo=github)

> Plain-English explanations of *why* every wire and part is there, not just where to plug it in.

A complete electronics reference library for beginners — no buzzwords, no skipped steps. Every guide explains the reasoning behind the wiring, so you actually *learn* instead of just copying diagrams.

## How to Use This

- **New to electronics?** Start with the component references first — they explain what each part does.
- **Building a specific project?** Jump to the project guide. It will tell you which component references to read first.
- **Have a specific part question?** The component references are standalone.

<!-- GUIDES:START -->
## Crash Course — Start Here

New to electronics? These explain the fundamental concepts you need before wiring anything.

| Guide | What it covers |
|-------|---------------|
| _auto-generated_ |

## Component References

These explain what each component *actually does* — read these after the Crash Course if you need a specific part explained.

| Component | What it covers |
|-----------|---------------|
| _auto-generated_ |

## Project Guides

Complete wiring guides that reference the component explanations above.

| Project | What it covers |
|---------|---------------|
| _auto-generated_ |
<!-- GUIDES:END -->

## Cross-Reference Map

```
Component Guides ←─ are used by ─→ Project Guides
───────────────                     ─────────────
[Crash Course]
Breadboard & Wiring                   ALL projects (understanding the board)
  ↑
GPIO / ADC / PWM / DAC                ALL projects (which pin to use for what)
  ↑
Pull-Up / Pull-Down                   ALL projects (button wiring, I²C, sensor data lines)
  ↑
Multimeter                            ALL projects (debugging — the #1 troubleshooting tool)
  ↑
Power & Batteries                     ALL projects (power source selection)
  ↑
Connectors & Wire                     ALL projects (which connector/wire gauge where)
  ↑
[Components]
Diode                                ESP32 Fan Controller (flyback diode)
  ↑                                  Relay Module (flyback diode across coil)
  │                                  Stepper Motor A4988 (not needed — driver handles it)
  │
Resistor                             ALL projects (pull-ups, pull-downs, current limiting)
  ↑                                  HC-SR04 (voltage divider on Echo)
  │
Capacitor                            ESP32 Fan Controller (100µF bulk, 100nF decoupling)
  ↑                                  Stepper Motor A4988 (100–470µF bulk — critical)
  │                                  NeoPixel WS2812B (470–1000µF — critical)
  │
MOSFET                               ESP32 Fan Controller (main switching element)
  ↑
LED                                  ESP32 Fan Controller (status indicators)
  ↑                                  74HC595 Shift Register (output demonstration)
  │
BJT Transistor                       Relay Module (coil driver)
  ↑
Voltage Regulator                    Any project powering 3.3V/5V from higher supply
  ↑
Level Shifter                        NeoPixel WS2812B (3.3V→5V data)
  ↑                                  HC-SR04 (5V→3.3V Echo)
  │                                  I2C Devices (mixed-voltage bus)
  │
Optocoupler                          Relay Module (input isolation)
  ↑
Fuse                                  ESP32 Fan Controller (overcurrent)
  ↑
Inductor                             ESP32 Fan Controller (fan coils — why flyback diodes exist)
                                     Voltage Regulator (buck converter core component)
                                     │
Potentiometer                        ANY project with an analog knob/slider (ADC input)
                                     Voltage dividers (built-in adjustable)
                                     │
Buzzer                               PIR Motion Sensor (alarm output)
                                     Relay Module (NC-contact alert)
  ↑
Relay                                Relay Module (the core component)
  ↑                                  ANY project switching high power
  │
Switch/Button                        ALL projects (user input)
  ↑                                  PIR Motion Sensor (override switch)
  │
Crystal Oscillator                   ESP32 (RTC sleep timer)
  ↑                                  Custom PCB builds
  │
LDR / Photoresistor                  ANY project needing light sensing
  ↑                                  (night lights, auto-dim)
  │
Servo Motor                          Robot arm / animatronic projects
                                      Camera gimbal, RC projects
  ↑
Temperature & Humidity Sensors        OLED Sensor Readout (temp/humidity data)
  ↑                                    ESP32 Web Server (sensor data endpoint)
  ↑
OLED Display (SSD1306)               OLED Sensor Readout (display output)
  ↑                                  I2C Devices (I²C display example)
  ↑
Rotary Encoder                       ANY project with menu navigation / user input
  ↑
DC Motor (Brushed)                   Robot / fan / pump projects (PWM + H-bridge)
  ↑
Thermistor (NTC)                     ANY project needing analog temperature sensing
```

## What Each File Is For

| File | What it does |
|------|-------------|
| `main.py` | Entry point — run with `python main.py` (or `start.bat`) |
| `server/` | Server package — imported by `main.py`; config, markdown, templates, page handlers |
| `projects/esp32-fan-controller.md` | The original guide — ESP32-powered temperature-controlled fan |
| `fundamentals/*.md` | Crash Course — start here if you're new to electronics |
| `projects/*.md` | Step-by-step wiring guides that reference the component files |
| `README.md` | This file — the project home page (served at `/`) |
| `start.bat` | Windows launcher for `main.py` |
| `pyproject.toml` | Project metadata and `uv` support — run with `uv run main.py` |

## Upcoming

- **Buy-links on component pages** — click a component name to search Google Shopping / AliExpress / Mouser for that part. The auto-linker in `server/markdown.py` will turn component names into search URLs.
- **Visual wiring diagrams** — SVG/Breadboard view wiring diagrams embedded in guides.

## Quick Start

| Option | Command |
|--------|---------|
| Windows | Double-click `start.bat` |
| Python | `python main.py` |
| Python (custom port) | `python main.py 8080` |
| uv | `uv run main.py` |
| npx (static only) | `npx http-server . -p 3000 -c-1` |

Open http://localhost:3000 in your browser. Press Ctrl+C to stop.

To add new content:
- **Components** → add `.md` file in `components/`
- **Fundamentals** → add `.md` file in `fundamentals/`
- **Projects** → add `.md` file in `projects/`
- The server auto-discovers new files on restart

## License

MIT — see [LICENSE](LICENSE). Free to use, share, and modify. Built for the electronics learning community.
