# HC-SR04 Ultrasonic Sensor — Wiring for Dummies

## What It Is

The HC-SR04 is a **sonar range finder**. It sends out a high-frequency sound (too high for humans to hear), waits for the echo to bounce back, and measures how long it took. Sound travels at about 343m/s in air, so:

```
Distance = Time × Speed of Sound / 2

Example: Sound takes 2ms to return
Distance = 0.002 × 343 / 2 = 0.343m = 34.3 cm
```

> **Analogy:** Think of shouting in a canyon. You shout ("ping!"), wait, and hear the echo. The time between shout and echo tells you how far the canyon wall is. The HC-SR04 does the same thing, 40,000 times per second, with sound you can't hear.

## The 4 Pins

```
HC-SR04 (looking from front — two "eyes" facing you)
 ┌─────────────────────────────┐
 │     ○ ○         ○ ○        │
 │   Transmit    Receive      │
 │     ○ ○         ○ ○        │
 │                             │
 └─────────────────────────────┘
      │     │     │     │
      VCC  Trig  Echo  GND
```

| Pin | Name | Think of it as... | Voltage |
|-----|------|-------------------|---------|
| **VCC** | Power | Feeds the sensor brains | **5V** (not 3.3V!) |
| **Trig** | Trigger | The **"shout" button** — pulse HIGH for 10µs to send a ping | 5V input (5V tolerant) |
| **Echo** | Echo | The **"listen" wire** — goes HIGH for the duration of the echo | 5V output (5V) |
| **GND** | Ground | Completes the circuit | − |

## The 5V Problem

**CRITICAL:** The HC-SR04 runs on **5V**. The Echo pin outputs **5V logic**. An ESP32's GPIO pins are **3.3V** and can be damaged by 5V.

You have two options:

### Option 1: Voltage Divider on Echo (Recommended)

Use two resistors to divide the 5V Echo signal down to 3.3V:

```
HC-SR04 Echo ──┬── 10kΩ (R1)
                │
                ├──── ESP32 GPIO (3.3V safe!)
                │
                └── 20kΩ (R2) ──── GND
```

The math: Vout = 5V × 20kΩ / (10kΩ + 20kΩ) = 3.33V. Perfect.

**Alternative resistor pairs:**
- 1kΩ + 2kΩ (lower impedance, better noise immunity)
- 4.7kΩ + 10kΩ (close enough: 3.2V)
- 10kΩ + 10kΩ (gives 2.5V — still reads as HIGH)

### Option 2: Bi-Directional Level Shifter Module

> **Full component reference:** See [Level Shifter](../components/level-shifter.md) for voltage dividers vs dedicated level shifter modules, and which to choose.

Use a 3.3V/5V level shifter board. Connect the Echo pin to the HV side and the ESP32 GPIO to the LV side.

### Option 3: 3.3V Direct (Works for some boards)

Some HC-SR04 clones work at 3.3V on VCC (they have onboard regulators). If you're lucky:
- Power from ESP32 3.3V
- Trig from GPIO (3.3V)
- Echo will output ~3.3V

> **Test this cautiously.** First power from 3.3V and measure Echo voltage with a multimeter. If it's above 3.6V, use the voltage divider.

## How the Signaling Works — Timing Diagram

```
Trig (from ESP32):
     ┌────────────────────────────── Normal LOW
     │
     │   ┌───┐
     │   │   │  ← 10µs pulse
     └───┘   └────────────────────── Back to LOW

                     Sound waves travel out, hit object, bounce back
                     ═══════╗ ═══════╗ ═══════╗
                            ║        ║        ║
                            ╚════════╝════════╝═══

Echo (from sensor):
          ┌────────────────────────────────────────── HIGH
          │  ← Width = time for sound to travel × 2
     ─────┘                                          Back to LOW

     ↑                                    ↑
   Start pulse                     Echo ends = object found
   (Trig sent)                      OR 38ms timeout = no object
```

**Reading it in code:**

```
1. Set Trig HIGH for 10 microseconds
2. Wait for Echo to go HIGH
3. Measure how long Echo stays HIGH (pulseIn())
4. Calculate distance: cm = microseconds / 58
```

The timeout is about **38ms** (no object within ~6.5 meters). If Echo never goes LOW, there's nothing in range.

## Complete Wiring Diagram (ESP32)

```
ESP32                      HC-SR04
─────                      ───────
GPIO ─────────────────────── Trig (any GPIO)
                             │
GPIO ───── 10kΩ ──┬──────── Echo  (must use voltage divider!)
                   │
                  20kΩ
                   │
GND  ──────────────┴────────── GND  (shared!)
                             │
5V  ───────────────────────── VCC  (NOT 3.3V!)

5V supply:
  ┌── USB power (if ESP32 has 5V output pin)
  └── External 5V supply (tie GNDs together)
```

## Power Options

**The HC-SR04 draws about 15mA when active.** That's fine from most sources.

| Power source | Works? | Notes |
|-------------|--------|-------|
| ESP32 5V pin (from USB) | Yes | Good — that's 5V from USB passthrough |
| ESP32 3.3V pin | Maybe | Only if your specific HC-SR04 clone works at 3.3V |
| External 5V supply | Yes | Must share GND with ESP32 |
| Battery (5V rail) | Yes | Fine |

## Accuracy and Gotchas

| Factor | Effect |
|--------|--------|
| Temperature | Sound speed changes ~0.6m/s per °C. Compensate if precision matters |
| Soft surfaces (fabric, carpet) | Absorb sound — may not return echo (reads as no object) |
| Angled surfaces | Sound bounces away — no echo returns |
| Minimum range | ~2cm (anything closer reads as 2cm) |
| Maximum range | ~4m (rated), ~6m (practical in good conditions) |
| Multiple HC-SR04s | They interfere with each other if triggered at the same time |
| Voltage drop | If 5V drops below ~4.5V, readings become garbage |

## Using in Pairs (Multiple Sensors)

If you need multiple sensors, trigger them **sequentially** (one at a time), not simultaneously. Two sensors firing at once interfere with each other's echoes.

```
Trigger sensor 1 → read → wait → trigger sensor 2 → read → wait → repeat
```

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Voltage divider on Echo | ESP32 GPIO receives 5V → **GPIO pin dies** |
| Shared ground between ESP32 and sensor | No signal — Echo never goes HIGH |
| 10µs trigger pulse (too short/long) | Sensor ignores the pulse — no reading |
| Common ground with measurement reference | Distance readings are random or always max |
| 38ms timeout handling | Your code hangs forever if nothing is in range |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| HC-SR04 ultrasonic module | 1 | $2–3 on Amazon/AliExpress |
| 10kΩ resistor | 1 | For Echo voltage divider |
| 20kΩ resistor | 1 | For Echo voltage divider |
| OR: 1kΩ + 2kΩ resistors | 2 | Alternative divider pair |
| OR: Level shifter module | 1 | Bi-directional, for cleaner setup |
| Jumper wires (M-F) | 4 | For connecting sensor |
| Mounting bracket | 1 | Optional but helps aim the sensor |

## Quick Code Reference (Arduino/ESP32)

```cpp
const int trigPin = 5;
const int echoPin = 18;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  // Send 10µs trigger pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure echo pulse width
  long duration = pulseIn(echoPin, HIGH, 38000); // 38ms timeout

  // Calculate distance
  float distance = duration / 58.0; // cm
  // or: distance = duration / 148.0; // inches

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  delay(500);
}
```

## See Also

- [voltage-divider](/fundamentals/voltage-divider)
- [level-shifter](/fundamentals/level-shifter)
- [analog-vs-digital](/fundamentals/analog-vs-digital)
- [multimeter](/fundamentals/multimeter)
