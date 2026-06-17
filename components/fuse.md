# Fuse — Component Reference

## What It Is

A fuse is a **sacrificial weak link** in your power path. When too much current flows, the fuse blows (opens) — stopping the current before wires melt, batteries vent, or chips explode. You replace the fuse instead of replacing everything else.

> **Analogy:** A fuse is like a **cheap, replaceable straw** in a water pipe. If the water pressure gets dangerously high, the straw bursts first — at a predictable, safe spot — instead of the expensive pipe bursting somewhere you can't reach.

## The 4 Fuse Types — Which One for Which Job

### 1. Glass / Ceramic Tube Fuse — The Classic

Small glass or ceramic cylinder with metal end caps. You can see the wire inside.

```
      ╔══════════╗
      ║    ψ     ║        Glass — see the wire inside
      ╚══════════╝
      ─┘        └─
```

| Pros | Cons |
|------|------|
| Cheap, standard, easy to find | Must be replaced after blowing |
| Available in many ratings | Glass can shatter on severe faults |
| Fast or slow-blow options | Needs a holder (doesn't solder directly) |

**Common sizes:**

| Size | Dimensions | Typical use |
|------|-----------|-------------|
| **5×20mm** | 5mm × 20mm | Bench power supplies, general electronics |
| **3AG / 1.25"×0.25"** | 32mm × 6.3mm | Automotive (old style), larger equipment |
| **2AG** | 15mm × 5mm | Smaller equipment, compact designs |

**Fast-blow vs Slow-blow (Time-Lag):**

| Type | Marking | Behavior | Use for |
|------|---------|----------|---------|
| **Fast (F)** | F, or no marking | Blows instantly at ~1.3× rated current | Sensitive electronics, signal processing |
| **Slow-blow (T)** | T (time-lag) | Tolerates brief inrush, blows on sustained overcurrent | Motors, fans, power supplies, anything with startup surge |
| **Very fast (FF)** | FF | Blows almost instantly | Precision instruments, delicate circuits |

> **Rule:** Use slow-blow for anything with a motor, fan, transformer, or big capacitors. Use fast-blow for sensitive electronics.

**How to read the element shape (glass fuse):**
- **Straight wire** = Fast blow
- **Spring-like / coiled wire** = Slow-blow
- **Thick element** = Higher current

### 2. Blade Fuse — Automotive Standard (ATO, Mini, Micro)

Flat plastic body with two metal prongs. Color-coded by amperage.

```
         ┌──────┐
         │  10  │  ← Amperage stamped on top
         └──────┘
         │      │
         │      │  ← Two metal prongs plug into holder
         └──────┘
    ATO / ATC (standard car fuse)
```

| Size | Current range | Found in |
|------|-------------|----------|
| **ATO / ATC** (standard) | 1–40A | Cars, trucks, RVs, 12V battery projects |
| **Mini** | 2–30A | Modern cars, compact 12V projects |
| **Micro** | 5–30A | Very compact fuse boxes |
| **MAXI** | 20–100A | High-current circuits, alternators |

**Color code (standard ATO/Mini):**

| Amps | Color | Amps | Color |
|------|-------|------|-------|
| 1A | Black | 15A | Blue |
| 2A | Gray | 20A | Yellow |
| 3A | Violet | 25A | Clear/White |
| 4A | Pink | 30A | Green |
| 5A | Tan | 35A | Violet |
| 7.5A | Brown | 40A | Orange |
| 10A | Red | | |

| Pros | Cons |
|------|------|
| Color-coded — identify at a glance | Must be replaced after blowing |
| Standard across all vehicles | Voltage rating limited to 32–58V DC |
| Easy to pull and inspect | Plastic may melt on very high faults |

> **Critical:** Blade fuses are **32V DC** (standard) or **58V DC** (mini). **Never use them on mains/AC voltage** — a 32V fuse on 120V will arc continuously when it blows and may not stop the current.

### 3. PTC Resettable Fuse (Polyfuse) — Self-Healing

A polymer disc that heats up and **increases resistance** when overcurrent flows. When the fault clears and it cools, it resets. No replacement needed. Looks like a ceramic disc capacitor with two leads.

```
Through-hole PTC:

      ╔═════╗
      ║ 1.1A║  ← Hold current rating
      ╚═════╝
        │ │        No polarity
```

| Pros | Cons |
|------|------|
| Self-resets — no replacement needed | Slow to trip (seconds, not milliseconds) |
| No polarity | Has internal resistance when "on" (0.1–5Ω) |
| Works repeatedly | Won't protect against fast transients |
| Good for hard-to-reach places | Limited voltage rating (30–60V) |

**Selection:**
```
PTC hold current = Normal load current × 1.5

Example: Fan draws 500mA → 500mA × 1.5 = 750mA → use 1.1A PTC
```

**Trip time (approximate):**

| Overcurrent | Trip time |
|-------------|-----------|
| 2× hold current | ~1–5 seconds |
| 5× hold current | ~0.1–1 second |
| 10× hold current | ~0.02–0.1 second |

**After a trip:**
1. Remove power (or fix the fault — current drops automatically)
2. Wait 10–30 seconds for cooling
3. Power back on — PTC resets automatically
4. If it trips again immediately, find the short

### 4. Fusible Resistor — Resistor + Fuse in One

A resistor designed to act as both a resistance **and** a fuse. When overloaded, it opens (goes infinite resistance) — like a resistor that sacrifices itself.

**Use for:** Power supply input where you need both current limiting and fuse protection in one part. Common in cheap power supplies and appliances.

## Fuse Ratings

| Rating | What it means | Example |
|--------|---------------|---------|
| **Current rating** | Max continuous current without blowing | 1A, 3A, 5A |
| **Voltage rating** | Max voltage the fuse can safely interrupt after blowing | 250V, 32V |
| **Speed** | How fast it blows at overcurrent | Fast, Slow-Blow |
| **Breaking capacity** | Max fault current the fuse can safely interrupt | 100A, 1500A |

> **Rule:** **Never exceed the fuse's voltage rating.** A blown fuse still has voltage across it — if rated too low, it arcs and keeps conducting. Glass = 250V (AC/DC OK). Blade = 32V or 58V (DC only — no mains). PTC = usually 30–60V.

## Quick Selection Guide

| Job | Fuse type | Typical rating |
|-----|-----------|---------------|
| Bench power supply output | Glass 5×20mm slow-blow | 1–5A |
| 12V fan or motor | Blade ATO slow-blow | 3–10A |
| Breadboard project protection | PTC resettable | Use 1.1A (most common) |
| USB port protection | PTC resettable | 500mA |
| Car accessory (12V) | Blade ATO (color-coded) | 5–30A |
| 120V/240V mains appliance | Glass 5×20mm fast | Match device rating |
| Battery pack protection | PTC resettable | 1.5× expected load |
| LED strip (12V, 2A) | Blade ATO slow-blow | 3A or PTC 2.6A |

**Choosing a value:**

```
Fuse rating = Normal load current × 1.2 to 1.5

Example: ESP32 draws 300mA → 300mA × 1.5 = 450mA → use 500mA fast
Example: Fan draws 500mA with 3A startup surge → use 3A slow-blow
```

## What Happens If You Choose Wrong

| Mistake | Result |
|---------|--------|
| Fast-blow on a motor circuit | Fuse blows every time the motor starts (inrush) |
| Slow-blow on sensitive electronics | Circuit may be damaged before fuse responds |
| Blade fuse on 48V+ circuit | Arc won't extinguish — fire risk |
| PTC for lightning surge | Too slow — electronics die before PTC reacts |
| Glass fuse rated 250V AC on 250V DC | DC arc is harder to extinguish — possible arcing |
| Fuse too large (e.g., 10A on a 1A circuit) | Circuit burns up before fuse cares |
| Replacing with wire / foil | **You disabled your only protection** |

## Quick Reference

```
Type        | Reusable? | Speed        | Voltage | Best for
Glass/Fast  | No        | Instant      | 250V    | Sensitive electronics
Glass/Slow  | No        | Tolerates inrush | 250V | Motors, fans, PSUs
Blade (ATO) | No        | Fast or slow | 32/58V DC | Automotive, 12V projects
PTC         | Yes       | Slow         | 30–60V  | Breadboards, battery packs
Fusible R   | No        | Medium       | Depends | Cheap PSUs, appliances

Selection: Fuse rating = Load current × 1.5
Slow-blow (T) = motors, fans, caps — startup surge
Fast-blow (F) = sensitive electronics — every ms counts

Never exceed voltage rating!
Glass = 250V (AC/DC OK)
Blade = 32V/58V DC only
PTC   = check the part

Golden rule: Never replace a blown fuse without finding out WHY it blew.
```
