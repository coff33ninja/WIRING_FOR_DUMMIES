#!/usr/bin/env python3
"""Scans project guides for component mentions, cross-references existing
component guides, and reports gaps. Optionally creates stub files."""

import re
import sys
from pathlib import Path

DIR = Path(__file__).parent

# Known component names (lowercase) mapped to suggested slug and display name
# Each entry: (regex_pattern, suggested_slug, display_name)
COMPONENT_PATTERNS = [
    (r"\b7.segment display\b", "7-segment-display", "7-Segment Display"),
    (r"\b7.segment\b", "7-segment-display", "7-Segment Display"),
    (r"\bstepper motor\b", "stepper-motor", "Stepper Motor"),
    (r"\bultrasonic (sensor|module)\b", "ultrasonic-sensor", "Ultrasonic Sensor (HC-SR04)"),
    (r"\bHC-SR04\b", "ultrasonic-sensor", "Ultrasonic Sensor (HC-SR04)"),
    (r"\bPIR (sensor|module)\b", "pir-sensor", "PIR Motion Sensor (HC-SR501)"),
    (r"\bHC-SR501\b", "pir-sensor", "PIR Motion Sensor (HC-SR501)"),
    (r"\bmotion sensor\b", "pir-sensor", "PIR Motion Sensor (HC-SR501)"),
    (r"\bshift register\b", "shift-register", "Shift Register (74HC595)"),
    (r"\b74HC595\b", "shift-register", "Shift Register (74HC595)"),
    (r"\baddressable LED\b", "addressable-led", "Addressable LED (WS2812B/NeoPixel)"),
    (r"\bNeoPixel\b", "addressable-led", "Addressable LED (WS2812B/NeoPixel)"),
    (r"\bWS2812\b", "addressable-led", "Addressable LED (WS2812B/NeoPixel)"),
    (r"\bfan\b", "dc-fan", "DC Fan (Axial / Blower)"),
    (r"\bsolenoid\b", "solenoid", "Solenoid"),
    (r"\bpiezo\b", "piezo-buzzer", "Piezo Buzzer / Element"),
    (r"\bliquid crystal|LCD\b", "lcd-display", "LCD Display (1602 / I2C)"),
    (r"\bI2C display\b", "lcd-display", "LCD Display (1602 / I2C)"),
    (r"\btransformer\b", "transformer", "Transformer"),
    (r"\bbuck converter\b", "buck-converter", "Buck Converter (Step-Down)"),
    (r"\bboost converter\b", "boost-converter", "Boost Converter (Step-Up)"),
    (r"\bvoltage divider\b", "voltage-divider", "Voltage Divider"),
    (r"\bphotoresistor|LDR\b", "ldr", "LDR / Photoresistor"),
    (r"\bHall.effect\b", "hall-effect-sensor", "Hall Effect Sensor"),
    (r"\bcurrent sensor\b", "current-sensor", "Current Sensor (ACS712 / INA219)"),
    (r"\bRTC\b", "real-time-clock", "Real-Time Clock (DS3231 / DS1307)"),
    (r"\bDS3231\b", "real-time-clock", "Real-Time Clock (DS3231 / DS1307)"),
    (r"\bDS1307\b", "real-time-clock", "Real-Time Clock (DS3231 / DS1307)"),
    (r"\bresistor pack\b", "resistor-network", "Resistor Network / Pack"),
    (r"\btransistor array\b", "transistor-array", "Transistor Array (ULN2003)"),
    (r"\bULN2003\b", "transistor-array", "Transistor Array (ULN2003)"),
    (r"\bop.?amp\b", "op-amp", "Operational Amplifier"),
    (r"\bcomparator\b", "comparator", "Comparator (LM393)"),
    (r"\btimer|555\b", "555-timer", "555 Timer IC"),
    (r"\bmicrocontroller|ESP32|Arduino\b", "microcontroller", "Microcontroller (ESP32 / Arduino)"),
    (r"\bspeaker\b", "speaker", "Speaker / Audio Output"),
    (r"\bmicrophone\b", "microphone", "Microphone (MAX9814 / Electret)"),
    (r"\bEthernet|LAN\b", "ethernet", "Ethernet (ESP32 / W5500)"),
    (r"\bBluetooth|BLE\b", "bluetooth", "Bluetooth / BLE (HC-05 / HM-10)"),
    (r"\bWiFi\b", "wifi", "WiFi (ESP32 / ESP8266)"),
    (r"\bGPS\b", "gps", "GPS Module (NEO-6M / NEO-8M)"),
]


def existing_slugs():
    return {f.stem.lower() for f in (DIR / "components").glob("*.md")}


def scan_projects():
    mentions = {}  # slug -> list of (project_file, display_name, matched_text)
    proj_dir = DIR / "projects"
    if not proj_dir.exists():
        return mentions
    for f in sorted(proj_dir.glob("*.md")):
        text = f.read_text("utf-8", errors="replace")
        for pattern, slug, display in COMPONENT_PATTERNS:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                if slug not in mentions:
                    mentions[slug] = []
                mentions[slug].append((f.name, display, m.group()))
    return mentions


def scan_fundamentals():
    mentions = {}
    fund_dir = DIR / "fundamentals"
    if not fund_dir.exists():
        return mentions
    for f in sorted(fund_dir.glob("*.md")):
        text = f.read_text("utf-8", errors="replace")
        for pattern, slug, display in COMPONENT_PATTERNS:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                if slug not in mentions:
                    mentions[slug] = []
                mentions[slug].append((f.name, display, m.group()))
    return mentions


def stub_content(slug, display_name):
    title = display_name
    desc_map = {
        "7-segment-display": "A 7-segment display shows numbers (0-9) and some letters using individual LED segments. Common types: common anode vs common cathode, 1-digit vs multi-digit, decimal point.",
        "stepper-motor": "A stepper motor moves in precise, fixed steps rather than spinning freely. Unlike a DC motor, you can control exact position without feedback.",
        "ultrasonic-sensor": "An HC-SR04 ultrasonic sensor measures distance by sending a high-frequency sound pulse and timing the echo. Range: 2 cm to 400 cm.",
        "pir-sensor": "A PIR (Passive Infrared) sensor detects motion by sensing changes in infrared radiation from warm bodies. Common module: HC-SR501.",
        "shift-register": "The 74HC595 shift register turns 3 microcontroller pins into 8 (or more) parallel outputs. It converts serial data to parallel — expanding your outputs.",
        "addressable-led": "Addressable LEDs (WS2812B / NeoPixel) are RGB LEDs with a built-in controller chip. Each LED shows any color, and you chain them on a single data wire.",
        "dc-fan": "A DC fan is a brushed or brushless motor with attached blades. Common sizes: 40 mm to 120 mm, voltages: 5 V, 12 V, 24 V. Uses PWM for speed control.",
        "solenoid": "A solenoid is an electromechanical device — a coil of wire that creates a magnetic field when energized, pushing or pulling a metal plunger.",
        "piezo-buzzer": "A piezo buzzer uses a piezoelectric crystal that vibrates when voltage is applied. Passive buzzers need a PWM signal; active ones beep when powered.",
        "lcd-display": "An LCD display (1602 / 20x4) shows text using a grid of liquid crystal characters. Common interfaces: parallel (8/4-bit) or I2C backpack.",
        "transformer": "A transformer transfers electrical energy between circuits through electromagnetic induction. It steps voltage up or down using two coils.",
        "buck-converter": "A buck converter steps a higher input voltage down to a lower output voltage efficiently (80-95%). Used when linear regulators would waste too much power as heat.",
        "boost-converter": "A boost converter steps a lower input voltage up to a higher output voltage. Used to power 5V devices from a 3.7V Li-ion battery.",
        "voltage-divider": "A voltage divider uses two resistors to produce a fraction of the input voltage. Essential for reading higher voltages with an ADC or shifting signal levels.",
        "hall-effect-sensor": "A Hall effect sensor detects magnetic fields. It outputs a digital signal when a magnet passes nearby, or an analog signal proportional to field strength.",
        "current-sensor": "A current sensor measures how much current flows through a wire. Common modules: ACS712 (analog), INA219 (I2C, voltage + current).",
        "real-time-clock": "An RTC keeps accurate time even when the microcontroller is powered off, using a backup battery (CR2032). Common chips: DS3231 (accurate), DS1307.",
        "resistor-network": "A resistor network packs multiple resistors in a single package. Common types: isolated, bussed (pull-up), and dual-terminator for signal lines.",
        "transistor-array": "The ULN2003 is a Darlington transistor array — 7 high-current, high-voltage outputs driven by low-current logic inputs. Used for relays, motors, solenoids.",
        "op-amp": "An operational amplifier (op-amp) amplifies the voltage difference between its two inputs. Used in comparators, filters, oscillators, and sensor signal conditioning.",
        "comparator": "A comparator (LM393) compares two voltages and outputs a digital high or low — telling you which input is higher. Used for threshold detection.",
        "555-timer": "The 555 timer IC generates precise timing pulses or oscillates at a set frequency. Three modes: astable (continuous square wave), monostable (one-shot), bistable (flip-flop).",
        "microcontroller": "A microcontroller is a tiny computer on a chip — CPU, RAM, GPIO, ADC inside one package. Common hobbyist MCUs: ESP32, Arduino (ATmega328P), RP2040.",
        "speaker": "A small speaker (8Ω / 4Ω) turns an audio signal into sound. Drive it with a PWM signal through a transistor amplifier — not directly from a GPIO pin.",
        "microphone": "An electret microphone module (MAX9814 / MAX4466) converts sound to an analog voltage. Use the ADC to read amplitude, or a comparator for sound-trigger detection.",
        "ethernet": "Ethernet gives your microcontroller a wired network connection. ESP32 has built-in MAC; add a PHY module (LAN8720 / W5500) for the physical interface.",
        "bluetooth": "Bluetooth modules (HC-05 for classic, HM-10 for BLE) add wireless serial communication to any microcontroller with a UART. Pair with a phone or another MCU.",
        "wifi": "WiFi modules (ESP32 built-in, ESP8266 external) connect your project to a wireless network for IoT, web servers, MQTT, and OTA updates.",
        "gps": "A GPS module (NEO-6M / NEO-8M) receives satellite signals to report position (lat/lon), speed, altitude, and UTC time over serial (NMEA sentences).",
    }
    desc = desc_map.get(slug, f"A {display_name.lower()} — a common electronics component used in hobby projects.")
    return f"""# {title} — Component Reference

## What It Is

{desc}
"""


def main():
    args = sys.argv[1:]
    do_create = "--create" in args

    existing = existing_slugs()
    print(f"Existing component guides: {len(existing)}")
    for s in sorted(existing):
        print(f"  ✓ {s}")

    proj_mentions = scan_projects()
    fund_mentions = scan_fundamentals()

    # Merge mentions from both sources
    all_mentions = {}
    for slug, refs in proj_mentions.items():
        all_mentions.setdefault(slug, []).extend(refs)
    for slug, refs in fund_mentions.items():
        all_mentions.setdefault(slug, []).extend(refs)

    # Filter to missing
    missing = {}
    for slug, refs in sorted(all_mentions.items()):
        if slug in existing:
            continue
        missing[slug] = refs[0]  # first reference
        sources = list(set(r[0] for r in refs))
        print(f"\n  ✗ {slug} (mentioned in: {', '.join(sorted(sources))})")

    if not missing:
        print("\nNo missing component guides found.")
        return

    print(f"\n{'='*60}")
    print(f"Total missing: {len(missing)}")

    if do_create:
        comp_dir = DIR / "components"
        for slug, (src_file, display_name, matched_text) in missing.items():
            path = comp_dir / f"{slug}.md"
            if path.exists():
                print(f"  Skipping {slug}.md (already exists)")
                continue
            path.write_text(stub_content(slug, display_name), encoding="utf-8")
            print(f"  Created {slug}.md")
        print("\nStubs created. Edit each file to add full details.")
    else:
        print("\nRun with --create to generate stub files.")


if __name__ == "__main__":
    main()
