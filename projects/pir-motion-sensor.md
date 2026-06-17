# PIR Motion Sensor (HC-SR501) — Wiring for Dummies

## What It Is

A PIR (Passive Infrared) motion sensor detects **heat moving in front of it** — specifically, the infrared radiation emitted by warm bodies (humans, animals, cars with hot engines). When something warm moves across its field of view, it pulls a pin HIGH.

> **Analogy:** Think of the PIR sensor as a security camera that can't see — it just feels heat. It doesn't know *what* moved past it, only that something warm moved. Like a blind person sensing you walk past them by the warmth your body leaves behind.

## The HC-SR501 PIR Module Pins

```
         HC-SR501 (front — dome facing you)
    ┌─────────────────────────────────────┐
    │      ○ ○  (sensitivity adjust)      │
    │                                     │
    │     ┌─ hemispherical lens ──┐       │
    │     │   (Fresnel lens)      │       │
    │     └───────────────────────┘       │
    │                                     │
    │      ○ ○  (time adjust)             │
    └─────────────────────────────────────┘
         │    │    │
        GND  OUT  VCC
```

| Pin | Name | Think of it as... | Voltage |
|-----|------|-------------------|---------|
| **VCC** | Power | Feeds the sensor | **5V** (not 3.3V!) |
| **OUT** | Signal | Goes HIGH when motion detected | 3.3V or 5V (see below) |
| **GND** | Ground | Completes the circuit | − |

> **3.3V compatibility:** The HC-SR501's output is **3.3V on most modules** (it uses a 3.3V regulator internally). That means it can connect directly to an ESP32 GPIO — no level shifter needed. But **always verify with a multimeter first**.

## The Two Adjustable Pots

The HC-SR501 has two tiny potentiometers (trimpots) for adjustment:

| Pot | Label | Range | What it does |
|-----|-------|-------|-------------|
| **Sensitivity** | Sx | ~3m to ~7m | How far the sensor detects. Full CCW = 3m, Full CW = 7m |
| **Time** | Tx | ~3s to ~5min | How long OUT stays HIGH after motion stops. Full CCW = 3s, Full CW = 5min |

> Adjustment tip: Use a tiny screwdriver. Turn gently. The pots are fragile and break easily.

## Retriggering Mode (L/H Jumper)

There's a jumper on the board (often labeled **L** and **H**):

| Mode | Jumper position | Behavior |
|------|----------------|----------|
| **L** (Non-retriggering) | Bridging L pins | OUT goes HIGH once, then LOW after the time delay. A second trigger during the delay is ignored. |
| **H** (Retriggering) | Bridging H pins | OUT stays HIGH as long as motion continues. Each new trigger restarts the timer. |

**Use L for:** One-shot detection (count events, toggle lights).
**Use H for:** Occupancy sensing (keep lights on while someone is in the room).

## Basic Wiring (ESP32)

```
ESP32              HC-SR501
─────              ────────
5V ───────────────── VCC (middle pin)
GPIO ──────────────── OUT
GND ───────────────── GND
```

**Code (simple):**
```cpp
const int pirPin = 14;

void setup() {
  pinMode(pirPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  int motion = digitalRead(pirPin);
  if (motion == HIGH) {
    Serial.println("MOTION DETECTED");
  } else {
    Serial.println("All clear");
  }
  delay(100);
}
```

## The Warm-Up Period

When you first power the HC-SR501, it needs **30–60 seconds to stabilize**. During this time:
- OUT may trigger randomly (false positives)
- The sensor is calibrating its baseline infrared reading

> **Your code should ignore the first 60 seconds of readings.** Either delay setup or use a flag:
> ```cpp
> unsigned long start = millis();
> bool ready = false;
>
> void loop() {
>   if (millis() > start + 60000) ready = true;
>   if (!ready) return;
>   // ... normal motion detection
> }
> ```

## Wiring with a Relay (Lights on Motion)

A classic combo — when motion detected, turn on a light for 2 minutes:

```
ESP32                  HC-SR501              Relay Module
─────                  ────────              ────────────
5V ───────────────────── VCC
GPIO 14 ──────────────── OUT
GPIO 15 ───────────────────────────────────── IN
GND  ─────────────────── GND ───────────────── GND
5V  ────────────────────────────────────────── VCC
```

**Code:**
```cpp
const int pirPin = 14;
const int relayPin = 15;
unsigned long timer = 0;
const unsigned long timeout = 120000; // 2 min

void setup() {
  pinMode(pirPin, INPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);
  delay(60000); // skip warm-up
}

void loop() {
  if (digitalRead(pirPin) == HIGH) {
    digitalWrite(relayPin, HIGH);
    timer = millis();
  }
  if (millis() - timer > timeout) {
    digitalWrite(relayPin, LOW);
  }
}
```

## PIR + Buzzer Alarm

Adding a buzzer makes a simple motion alarm:

> See [Buzzer Component Reference](../components/buzzer.md) for wiring options.

```
ESP32              PIR               Buzzer
─────              ───               ──────
GPIO 14 ─────────── OUT
GPIO 12 ────────────────────────────── (+) active buzzer
GND  ────────────── GND ────────────── (–)
5V  ─────────────── VCC
```

## Mounting Tips

| Placement | Effect |
|-----------|--------|
| Corner of room at 2m height | Best coverage — 120° cone |
| Near HVAC vent | **False triggers** — moving warm/cold air |
| Facing a window | **False triggers** — cars outside, sun heating the glass |
| Behind glass/plastic | **Doesn't work** — IR doesn't pass through glass |
| Near a router/PSU | Possible electrical noise interference |

## What Happens If You Skip Things

| Skipped | Result |
|---------|--------|
| Warm-up delay (60s) | Constant false triggers for the first minute |
| Level shifter (if OUT is 5V) | Could damage 3.3V GPIO — check with multimeter first |
| Sensitivity adjustment | Default range (~5m) might be too much or too little |
| Time adjustment | Default 3s might be too short for your use case |
| Retrigger mode jumper (H vs L) | Inconsistent behavior — lights may flicker |

## Shopping List

| Part | Qty | Notes |
|------|-----|-------|
| HC-SR501 PIR module | 1 | $2–3 on Amazon/Ali |
| Relay module (optocoupler) | 1 | For switching lights/appliances |
| Active buzzer 5V | 1 | Optional — for alarm |
| Jumper wires (M-F) | 4 | For connections |
| Tiny screwdriver | 1 | For adjusting the sensitivity/time pots |

## Quick Reference

```
Warm-up:         60s (ignore first readings)
Detection range: 3–7m (adjustable)
Detection angle: ~120° cone
Output:          3.3V logic on most modules (verify!)
Response time:   ~500ms
Power:           5V DC, ~50µA (idle), ~1mA (triggered)
```

## See Also

- [analog-vs-digital](/fundamentals/analog-vs-digital)
- [gpio-pins](/fundamentals/gpio-pins)
- [soldering](/fundamentals/soldering)
- [multimeter](/fundamentals/multimeter)
- [power-batteries](/fundamentals/power-batteries)
