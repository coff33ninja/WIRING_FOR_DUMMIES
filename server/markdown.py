"""Markdown-to-HTML renderer with auto-linking."""

import re


def html_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")



# Auto-link database: (regex, slug, display_name, kind)  kind='comp'|'fund'
AUTO_LINKS = [
    # ── Components ──────────────────────────────────────────────
    (r"\b7.segment display\b", "7-segment-display", "7-Segment Display", "comp"),
    (r"\b7.segment\b", "7-segment-display", "7-Segment Display", "comp"),
    (r"\bstepper motor\b", "stepper-motor", "Stepper Motor", "comp"),
    (r"\bultrasonic (sensor|module)\b", "ultrasonic-sensor", "Ultrasonic Sensor (HC-SR04)", "comp"),
    (r"\bHC-SR04\b", "ultrasonic-sensor", "Ultrasonic Sensor (HC-SR04)", "comp"),
    (r"\bPIR (sensor|module)\b", "pir-sensor", "PIR Motion Sensor (HC-SR501)", "comp"),
    (r"\bHC-SR501\b", "pir-sensor", "PIR Motion Sensor (HC-SR501)", "comp"),
    (r"\bmotion sensor\b", "pir-sensor", "PIR Motion Sensor (HC-SR501)", "comp"),
    (r"\bshift register\b", "shift-register", "Shift Register (74HC595)", "comp"),
    (r"\b74HC595\b", "shift-register", "Shift Register (74HC595)", "comp"),
    (r"\baddressable LED\b", "addressable-led", "Addressable LED (WS2812B/NeoPixel)", "comp"),
    (r"\bNeoPixel\b", "addressable-led", "Addressable LED (WS2812B/NeoPixel)", "comp"),
    (r"\bWS2812\b", "addressable-led", "Addressable LED (WS2812B/NeoPixel)", "comp"),
    (r"\bfan\b", "dc-fan", "DC Fan (Axial / Blower)", "comp"),
    (r"\bsolenoid\b", "solenoid", "Solenoid", "comp"),
    (r"\bpiezo\b", "piezo-element", "Piezo Element", "comp"),
    (r"\b(liquid crystal|lcd)\b", "lcd-display", "LCD Display (1602 / I2C)", "comp"),
    (r"\btransformer\b", "transformer", "Transformer", "comp"),
    (r"\bbuck converter\b", "buck-converter", "Buck Converter (Step-Down)", "fund"),
    (r"\bboost converter\b", "boost-converter", "Boost Converter (Step-Up)", "fund"),
    (r"\bvoltage divider\b", "voltage-divider", "Voltage Divider", "fund"),
    (r"\bHall.effect\b", "hall-effect-sensor", "Hall Effect Sensor", "comp"),
    (r"\bcurrent sensor\b", "current-sensor", "Current Sensor (ACS712 / INA219)", "comp"),
    (r"\bRTC\b", "real-time-clock", "Real-Time Clock (DS3231 / DS1307)", "comp"),
    (r"\bDS3231\b", "real-time-clock", "Real-Time Clock (DS3231 / DS1307)", "comp"),
    (r"\bDS1307\b", "real-time-clock", "Real-Time Clock (DS3231 / DS1307)", "comp"),
    (r"\bresistor (pack|network)\b", "resistor-network", "Resistor Network / Pack", "fund"),
    (r"\btransistor array\b", "transistor-array", "Transistor Array (ULN2003)", "comp"),
    (r"\bULN2003\b", "transistor-array", "Transistor Array (ULN2003)", "comp"),
    (r"\bop.?amp\b", "op-amp", "Operational Amplifier", "comp"),
    (r"\bcomparator\b", "comparator", "Comparator (LM393)", "comp"),
    (r"\b(timer|555)\b", "555-timer", "555 Timer IC", "comp"),
    (r"\b(microcontroller|ESP32|Arduino)\b", "microcontroller", "Microcontroller (ESP32 / Arduino / RP2040)", "comp"),
    (r"\bRP2040\b", "microcontroller", "Microcontroller (ESP32 / Arduino / RP2040)", "comp"),
    (r"\bspeaker\b", "speaker", "Speaker / Audio Output", "comp"),
    (r"\bmicrophone\b", "microphone", "Microphone (MAX9814 / Electret)", "comp"),
    (r"\b(Bluetooth|BLE)\b", "bluetooth", "Bluetooth (HC-05 / HM-10)", "comp"),
    (r"\bHC-05\b", "bluetooth", "Bluetooth (HC-05 / HM-10)", "comp"),
    (r"\bHM-10\b", "bluetooth", "Bluetooth (HC-05 / HM-10)", "comp"),
    (r"\bWiFi\b", "wifi", "WiFi (ESP32 / ESP8266)", "comp"),
    (r"\bESP8266\b", "wifi", "WiFi (ESP32 / ESP8266)", "comp"),
    (r"\bGPS\b", "gps", "GPS Module (NEO-6M / NEO-8M)", "comp"),
    (r"\bNEO-6M\b", "gps", "GPS Module (NEO-6M / NEO-8M)", "comp"),
    (r"\bNEO-8M\b", "gps", "GPS Module (NEO-6M / NEO-8M)", "comp"),
    (r"\bnRF24L01\b", "wireless-radio-module", "Wireless Radio Module (nRF24L01)", "comp"),
    (r"\bwireless radio module\b", "wireless-radio-module", "Wireless Radio Module (nRF24L01)", "comp"),
    (r"\bH.bridge\b", "h-bridge", "H-Bridge / Motor Driver (L298N, L293D)", "comp"),
    (r"\bL298N\b", "h-bridge", "H-Bridge / Motor Driver (L298N, L293D)", "comp"),
    (r"\bL293D\b", "h-bridge", "H-Bridge / Motor Driver (L298N, L293D)", "comp"),
    (r"\bmotor driver\b", "h-bridge", "H-Bridge / Motor Driver (L298N, L293D)", "comp"),
    (r"\bTP4056\b", "battery-charger", "Battery Charger (TP4056)", "comp"),
    (r"\bbattery charger\b", "battery-charger", "Battery Charger (TP4056)", "comp"),
    (r"\bLi.?ion charger\b", "battery-charger", "Battery Charger (TP4056)", "comp"),
    (r"\bload cell\b", "load-cell", "Load Cell + HX711", "comp"),
    (r"\bHX711\b", "load-cell", "Load Cell + HX711", "comp"),
    (r"\bweight sensor\b", "load-cell", "Load Cell + HX711", "comp"),
    (r"\bW5500\b", "ethernet", "Ethernet Module (W5500 / ENC28J60)", "comp"),
    (r"\bENC28J60\b", "ethernet", "Ethernet Module (W5500 / ENC28J60)", "comp"),
    (r"\bEthernet module\b", "ethernet", "Ethernet Module (W5500 / ENC28J60)", "comp"),
    (r"\btriac\b", "triac", "Triac & Solid State Relay", "comp"),
    (r"\bsolid.?state relay\b", "triac", "Triac & Solid State Relay", "comp"),
    (r"\bSSR\b", "triac", "Triac & Solid State Relay", "comp"),
    (r"\bSD card\b", "sd-card", "SD Card Module", "comp"),
    (r"\bmicroSD\b", "sd-card", "SD Card Module", "comp"),
    (r"\bdata logging\b", "sd-card", "SD Card Module", "comp"),
    (r"\baudio amplifier\b", "audio-amplifier", "Audio Amplifier (LM386, PAM8403, MAX98357)", "comp"),
    (r"\bLM386\b", "audio-amplifier", "Audio Amplifier (LM386, PAM8403, MAX98357)", "comp"),
    (r"\bPAM8403\b", "audio-amplifier", "Audio Amplifier (LM386, PAM8403, MAX98357)", "comp"),
    (r"\bMAX98357\b", "audio-amplifier", "Audio Amplifier (LM386, PAM8403, MAX98357)", "comp"),
    (r"\bIR receiver\b", "ir-receiver", "IR Receiver & IR LED", "comp"),
    (r"\bTSOP\b", "ir-receiver", "IR Receiver & IR LED", "comp"),
    (r"\binfrared receiver\b", "ir-receiver", "IR Receiver & IR LED", "comp"),
    (r"\bRFID\b", "rfid", "RFID / NFC (RC522)", "comp"),
    (r"\bRC522\b", "rfid", "RFID / NFC (RC522)", "comp"),
    (r"\bkeypad\b", "keypad", "Keypad (Matrix 4x4)", "comp"),
    (r"\bmatrix keypad\b", "keypad", "Keypad (Matrix 4x4)", "comp"),
    (r"\bjoystick\b", "joystick", "Joystick Module", "comp"),
    (r"\bgas sensor\b", "gas-sensor", "Gas Sensor (MQ Series)", "comp"),
    (r"\bMQ.2\b", "gas-sensor", "Gas Sensor (MQ Series)", "comp"),
    (r"\bMQ.135\b", "gas-sensor", "Gas Sensor (MQ Series)", "comp"),
    (r"\bMQ.7\b", "gas-sensor", "Gas Sensor (MQ Series)", "comp"),
    (r"\bsoil moisture\b", "moisture-sensor", "Soil Moisture / Rain Sensor", "comp"),
    (r"\brain sensor\b", "moisture-sensor", "Soil Moisture / Rain Sensor", "comp"),
    (r"\bSIM800\b", "cellular", "Cellular Module (SIM800 / SIM7000)", "comp"),
    (r"\bSIM7000\b", "cellular", "Cellular Module (SIM800 / SIM7000)", "comp"),
    (r"\bcellular module\b", "cellular", "Cellular Module (SIM800 / SIM7000)", "comp"),
    (r"\bRGB LED\b", "rgb-led", "RGB LED (Common Anode / Cathode)", "comp"),
    (r"\bbuck.?boost\b", "buck-boost-converter", "Buck-Boost Converter", "comp"),
    (r"\bMAX7219\b", "led-driver", "LED Driver (MAX7219)", "comp"),
    (r"\bLED driver\b", "led-driver", "LED Driver (MAX7219)", "comp"),
    (r"\bvibration motor\b", "vibration-motor", "Vibration Motor (ERM / LRA)", "comp"),
    (r"\bERM\b", "vibration-motor", "Vibration Motor (ERM / LRA)", "comp"),
    (r"\bLRA\b", "vibration-motor", "Vibration Motor (ERM / LRA)", "comp"),
    (r"\bhaptic\b", "vibration-motor", "Vibration Motor (ERM / LRA)", "comp"),
    (r"\bdigital potentiometer\b", "digital-potentiometer", "Digital Potentiometer (X9C103 / MCP41xx)", "comp"),
    (r"\bdigipot\b", "digital-potentiometer", "Digital Potentiometer (X9C103 / MCP41xx)", "comp"),
    (r"\bX9C103\b", "digital-potentiometer", "Digital Potentiometer (X9C103 / MCP41xx)", "comp"),
    (r"\bMCP41\b", "digital-potentiometer", "Digital Potentiometer (X9C103 / MCP41xx)", "comp"),
    # Extra component patterns for existing guides
    (r"\bBJT\b", "transistor-bjt", "BJT Transistor", "comp"),
    (r"\bNPN\b", "transistor-bjt", "BJT Transistor", "comp"),
    (r"\bPNP\b", "transistor-bjt", "BJT Transistor", "comp"),
    (r"\bdiode\b", "diode", "Diode", "comp"),
    (r"\bflyback diode\b", "diode", "Diode (flyback protection)", "comp"),
    (r"\bMOSFET\b", "mosfet", "MOSFET", "comp"),
    (r"\bcapacitor\b", "capacitor", "Capacitor", "comp"),
    (r"\bdecoupling cap\b", "capacitor", "Capacitor (decoupling)", "comp"),
    (r"\binductor\b", "inductor", "Inductor", "comp"),
    (r"\bLED\b", "led", "LED (Light Emitting Diode)", "comp"),
    (r"\bLDR\b", "ldr", "Light Dependent Resistor (LDR)", "comp"),
    (r"\bphotoresistor\b", "ldr", "Light Dependent Resistor (LDR)", "comp"),
    (r"\bpotentiometer\b", "potentiometer", "Potentiometer", "comp"),
    (r"\btrimpot\b", "potentiometer", "Potentiometer (trimpot)", "comp"),
    (r"\brelay\b", "relay", "Relay Module", "comp"),
    (r"\bservo\b", "servo", "Servo Motor", "comp"),
    (r"\bbuzzer\b", "buzzer", "Buzzer", "comp"),
    (r"\bOLED\b", "oled-display", "OLED Display (SSD1306)", "comp"),
    (r"\bSSD1306\b", "oled-display", "OLED Display (SSD1306)", "comp"),
    (r"\boptocoupler\b", "optocoupler", "Optocoupler / Optoisolator", "comp"),
    (r"\boptoisolator\b", "optocoupler", "Optocoupler / Optoisolator", "comp"),
    (r"\bfuse\b", "fuse", "Fuse", "comp"),
    (r"\bcrystal oscillator\b", "crystal", "Crystal Oscillator", "comp"),
    (r"\bDC motor\b", "dc-motor", "DC Motor", "comp"),
    (r"\bvoltage regulator\b", "voltage-regulator", "Voltage Regulator", "comp"),
    (r"\bLDO\b", "voltage-regulator", "Voltage Regulator (LDO)", "comp"),
    (r"\b7805\b", "voltage-regulator", "Voltage Regulator (7805)", "comp"),
    (r"\bthermistor\b", "thermistor", "Thermistor", "comp"),
    (r"\bNTC\b", "thermistor", "Thermistor (NTC)", "comp"),
    (r"\bDHT11\b", "temperature-humidity-sensors", "Temperature & Humidity Sensors (DHT11/DHT22)", "comp"),
    (r"\bDHT22\b", "temperature-humidity-sensors", "Temperature & Humidity Sensors (DHT11/DHT22)", "comp"),
    (r"\bDHT\d{2}\b", "temperature-humidity-sensors", "Temperature & Humidity Sensors (DHT11/DHT22)", "comp"),
    (r"\btemperature.humidity\b", "temperature-humidity-sensors", "Temperature & Humidity Sensors (DHT11/DHT22)", "comp"),
    # ── Fundamentals ──────────────────────────────────────────
    (r"\bOhm.s law\b", "ohm-law", "Ohm's Law & Basic Circuit Theory", "fund"),
    (r"\bOhm\b", "ohm-law", "Ohm's Law & Basic Circuit Theory", "fund"),
    (r"\bserial communication\b", "serial-communication", "Serial Communication (UART, I2C, SPI)", "fund"),
    (r"\bUART\b", "serial-communication", "Serial Communication (UART, I2C, SPI)", "fund"),
    (r"\bI[2²]C\b", "serial-communication", "Serial Communication (UART, I2C, SPI)", "fund"),
    (r"\bSPI\b", "serial-communication", "Serial Communication (UART, I2C, SPI)", "fund"),
    (r"\bPWM\b", "pwm", "PWM (Pulse Width Modulation)", "fund"),
    (r"\bpulse width modulation\b", "pwm", "PWM (Pulse Width Modulation)", "fund"),
    (r"\banalog vs digital\b", "analog-vs-digital", "Analog vs Digital Signals", "fund"),
    (r"\bsoldering\b", "soldering", "Soldering Basics", "fund"),
    (r"\breading schematics\b", "reading-schematics", "Reading Schematics", "fund"),
    (r"\bschematic symbol\b", "reading-schematics", "Reading Schematics", "fund"),
    (r"\bAC vs DC\b", "ac-vs-dc", "AC vs DC", "fund"),
    (r"\bgrounding\b", "grounding-decoupling", "Grounding & Decoupling", "fund"),
    (r"\bdecoupling\b", "grounding-decoupling", "Grounding & Decoupling", "fund"),
    (r"\bbreadboard\b", "breadboard", "Breadboard Basics", "fund"),
    (r"\bGPIO\b", "gpio-pins", "GPIO Pins", "fund"),
    (r"\bmultimeter\b", "multimeter", "Using a Multimeter", "fund"),
    (r"\bpull.up\b", "pull-up-pull-down", "Pull-Up & Pull-Down Resistors", "fund"),
    (r"\bpull.down\b", "pull-up-pull-down", "Pull-Up & Pull-Down Resistors", "fund"),
    (r"\blevel shifter\b", "level-shifter", "Level Shifting", "fund"),
    (r"\bconnector\b", "connectors-wire", "Connectors & Wire", "fund"),
    (r"\bjumper wire\b", "connectors-wire", "Connectors & Wire", "fund"),
    (r"\bpower.batteries\b", "power-batteries", "Power & Batteries — Supply Guide", "fund"),
    (r"\bwireless technology\b", "wireless_technologies", "Wireless Technologies", "fund"),
]

# Sort by pattern length descending so longer (more specific) patterns match first
AUTO_LINKS.sort(key=lambda x: len(x[0]), reverse=True)



def auto_link(text):
    """Auto-link plain-text mentions of components/fundamentals in HTML.

    Preserves existing <a>, <code>, <img> tags so they are not double-linked.
    """
    tokens = {}
    counter = [0]

    def _save(m):
        key = f"\x00L{counter[0]}\x00"
        counter[0] += 1
        tokens[key] = m.group(0)
        return key

    # Protect already-linked content, code spans, and images
    text = re.sub(r"<a\s[^>]*>.*?</a>", _save, text, flags=re.DOTALL)
    text = re.sub(r"<code>[^<]*</code>", _save, text)
    text = re.sub(r"<img[^>]*>", _save, text)

    for pattern, slug, _, kind in AUTO_LINKS:
        prefix = "components" if kind == "comp" else "fundamentals"
        href = f"/{prefix}/{slug}"
        text = re.sub(pattern, lambda m, h=href: f'<a href="{h}">{m.group(0)}</a>', text, flags=re.IGNORECASE)

    for key, value in tokens.items():
        text = text.replace(key, value)

    return text



def inline(text):
    text = text.replace("&amp;", "\x00a").replace("&lt;", "\x00l").replace("&gt;", "\x00g")
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = text.replace("\x00a", "&amp;").replace("\x00l", "&lt;").replace("\x00g", "&gt;")
    return auto_link(text)


def md_to_html(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    lines = text.split("\n")
    out = []
    in_code = False
    code_buf = []
    in_table = False

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            if in_code:
                out.append(f"<pre><code>{''.join(code_buf)}</code></pre>\n")
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(html_escape(line) + "\n")
            i += 1
            continue

        if not line.strip():
            if in_table:
                out.append("</table>\n")
                in_table = False
            out.append("<br>\n")
            i += 1
            continue

        if line.strip().startswith("|") and line.strip().endswith("|"):
            if not in_table:
                in_table = True
                out.append("<table>\n")
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            tag = "th" if re.search(r"^[-]+$", cells[0]) else "td"
            if tag == "th" and any(re.match(r"^[-]+$", c) for c in cells):
                i += 1
                continue
            out.append(f"<tr>{''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells)}</tr>\n")
            i += 1
            continue
        if in_table:
            out.append("</table>\n")
            in_table = False

        if re.match(r"^---+$", line.strip()):
            out.append("<hr>\n")
            i += 1
            continue

        m = re.match(r"^(#{1,3})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            anchor = re.sub(r"[^a-zA-Z0-9]+", "-", m.group(2).lower()).strip("-")
            out.append(f'<h{level} id="{anchor}">{inline(m.group(2))}</h{level}>\n')
            i += 1
            continue

        if line.strip().startswith(">"):
            content = re.sub(r"^>\s?", "", line, count=1)
            out.append(f"<blockquote>{inline(content)}</blockquote>\n")
            i += 1
            continue

        if re.match(r"^[\s]*[-*+]\s+", line):
            out.append("<ul>\n")
            while i < len(lines) and re.match(r"^[\s]*[-*+]\s+", lines[i]):
                content = re.sub(r"^[\s]*[-*+]\s+", "", lines[i])
                out.append(f"<li>{inline(content)}</li>\n")
                i += 1
            out.append("</ul>\n")
            continue

        if re.match(r"^\s*\d+[.)]\s+", line):
            out.append("<ol>\n")
            while i < len(lines) and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                content = re.sub(r"^\s*\d+[.)]\s+", "", lines[i])
                out.append(f"<li>{inline(content)}</li>\n")
                i += 1
            out.append("</ol>\n")
            continue

        p = []
        while i < len(lines) and lines[i].strip():
            p.append(inline(lines[i]))
            i += 1
        if p:
            out.append(f"<p>{' '.join(p)}</p>\n")

    if in_table:
        out.append("</table>\n")
    if in_code:
        out.append(f"<pre><code>{''.join(code_buf)}</code></pre>\n")

    return "".join(out)

