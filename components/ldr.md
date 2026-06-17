# LDR / Photoresistor — Component Reference

## What It Is

An LDR (Light Dependent Resistor) is a resistor whose **resistance changes with light**. More light = less resistance. No light = high resistance.

> **Analogy:** Think of an LDR as a lazy sunbather. In bright sunlight, they offer almost no resistance (→ lie down). In total darkness, they're stiff and resistant (→ stand rigid). The resistance tells you how bright it is.

## How It Works

```
Resistance vs Light:
      
  1MΩ ┤                    ● Dark (no light)
      │                    
      │                    
100kΩ ┤
      │                    
  10kΩ ┤        ● Dim room
      │                    
   1kΩ ┤     ● Bright office
      │
  100Ω ┤  ● Direct sunlight
      └─────────────────────
         Dark           Bright
```

| Condition | Typical resistance |
|-----------|------------------|
| Dark (closed box) | ~1MΩ (1,000,000Ω) |
| Dim room (night light) | ~100kΩ |
| Bright office | ~10kΩ |
| Direct sunlight | ~500Ω–2kΩ |

**If you connect it directly to a voltage:** The resistance varies hugely and non-linearly. You don't read the resistance directly — you use it in a **voltage divider** to get a measurable voltage.

## Wiring (Voltage Divider with Fixed Resistor)

The LDR alone can't give you a voltage reading. You pair it with a fixed resistor to make a voltage divider:

```
     3.3V
       │
      ┌┴┐
      │ │ LDR (changes with light)
      │ │
      └┬┘
       │
       ├──── ADC pin (ESP32 GPIO)
       │
      ┌┴┐
      │ │ 10kΩ fixed resistor
      │ │
      └┬┘
       │
      GND
```

**How it reads:**
- **Bright:** LDR resistance low (~1kΩ) → more voltage at ADC pin → high reading
- **Dark:** LDR resistance high (~1MΩ) → less voltage at ADC pin → low reading

**Code:**
```cpp
const int ldrPin = 34;
int raw = analogRead(ldrPin);  // 0 (dark) → 4095 (bright)
float voltage = raw * (3.3 / 4095);
```

> **The 10kΩ is a starting point.** For very dim environments, use 100kΩ. For bright-only, use 1kΩ. The fixed resistor should be near the LDR's resistance in the range you care about.

## Alternative Wiring (LDR on Top)

```
     3.3V
       │
      ┌┴┐
      │ │ 10kΩ fixed resistor
      │ │
      └┬┘
       │
       ├──── ADC pin
       │
      ┌┴┐
      │ │ LDR
      │ │
      └┬┘
       │
      GND
```

**This inverts the reading:** High voltage = dark, low voltage = bright. Use this if your logic expects the opposite behavior.

## ESP32 ADC Note

The ESP32's ADC is **not perfectly linear**, especially near 0V and 3.3V. For an LDR voltage divider, you don't need high precision — the reading just needs to tell light from dark. But if you want a more linear response, stay in the middle 10–90% of the ADC range.

> **Fix:** Adjust your fixed resistor value until the ADC reads ~2000 (middle-ish) in your target lighting condition.

## Using an LDR to Trigger a Light (Night Lamp)

```
ESP32                LDR Circuit              Relay Module
─────                ───────────              ────────────
GPIO 34 (ADC) ──────────┐
                         │
                    ┌────┴────┐
                    │ 10kΩ    │
                    └────┬────┘
                         │
3.3V ── LDR ────────────┘
GND  ────────────────────
                         
GPIO 15 ─────────────────────────────────────── IN
5V  ─────────────────────────────────────────── VCC
GND ─────────────────────────────────────────── GND
```

**Code:**
```cpp
const int ldrPin = 34;
const int relayPin = 15;

void setup() {
  pinMode(relayPin, OUTPUT);
}

void loop() {
  int light = analogRead(ldrPin);
  if (light < 500) {        // dark
    digitalWrite(relayPin, HIGH); // turn on light
  } else {
    digitalWrite(relayPin, LOW);  // turn off
  }
  delay(100);
}
```

## LDR vs Photodiode vs Phototransistor

| | LDR | Photodiode | Phototransistor |
|--|-----|------------|-----------------|
| Output | Resistance change | Current flow | Current flow |
| Speed | Slow (10–200ms) | Very fast (ns) | Fast (µs) |
| Sensitivity | Good for ambient light | Needs amplifier | Moderate |
| Complexity | Just a resistor pair | Op-amp needed | Transistor circuit |
| Best for | Day/night detection | Fiber optic, fast pulses | Object detection |

> **Use an LDR for:** "Is it dark yet?", ambient light sensing, night lights.
> **Don't use an LDR for:** Reading data through light, color sensing, high-speed detection.

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Fixed resistor (using LDR alone) | Reads as either 0V or 3.3V — no middle values |
| Wrong fixed resistor value | Narrow usable range — reads mostly max or min |
| No ADC pin (using digital GPIO) | Can only detect fully light vs fully dark, no nuance |
| Ignoring LDR response time | Fast light changes (flashlight) don't register |
| Using LDR in direct sunlight without divider | Very low resistance may exceed component limits |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| GL5528 LDR (5mm) | 5 | Standard CdS photoresistor |
| 10kΩ resistor | 5 | For voltage divider (start here) |
| 100kΩ resistor | 2 | For dimmer environments |
| 1kΩ resistor | 2 | For bright-only sensing |

> **Pro tip:** Most LDRs contain cadmium (CdS). They're legal in most places but avoid putting them in recycling. Treat as e-waste.
