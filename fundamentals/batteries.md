# Batteries & Cell Chemistries — Fundamental Reference

## What This Covers

Every battery is a **chemical reaction in a box**. Understanding the chemistry tells you its voltage, how to charge it, how much current it can deliver, whether it's safe to puncture, and how long it lasts. This guide covers every common chemistry you'll encounter in hobby electronics — and a few emerging ones.

## Primary vs Secondary (Non-Rechargeable vs Rechargeable)

| | Primary | Secondary |
|---|---------|-----------|
| **Rechargeable?** | No — chemical reaction is irreversible | Yes — reaction reverses with current |
| **Energy density** | Higher (more capacity per gram) | Lower (chemistry trades density for reversibility) |
| **Self-discharge** | Very low (years) | Higher (months) |
| **Typical use** | Smoke detectors, remotes, RTC backup | Phones, IoT projects, drones, cars |
| **Examples** | Alkaline, Zinc-Carbon, CR2032 | Li-ion, NiMH, Lead-Acid, LiFePO4 |

## Chemistry Comparison

### Primary (Non-Rechargeable)

| Chemistry | Nominal V | Capacity (AA) | Self-Discharge | Cost | When to use |
|-----------|-----------|---------------|----------------|------|-------------|
| **Zinc-Carbon** | 1.5V | 400–600mAh | ~2 years | Very cheap | Low-drain devices, disposable projects |
| **Alkaline** | 1.5V | 1500–3000mAh | ~5–7 years | Cheap | Standard for most consumer devices |
| **Lithium Primary** (CR123A, AA-sized) | 1.5–3V | 3000–3500mAh | ~10–15 years | Expensive | Extreme temps, long shelf life, high current |
| **Silver Oxide** (SR series) | 1.55V | 150–200mAh (small) | ~5 years | Moderate | Watches, calculators, precision analog |
| **Zinc-Air** | 1.4V | 400–600mAh (hearing aid size) | ~1 month *once activated* | Low | Hearing aids — high density, short life after opening |

### Secondary (Rechargeable)

| Chemistry | Nominal V | Full / Cutoff | Energy Density | Cycles | Memory Effect | Best For |
|-----------|-----------|---------------|----------------|--------|---------------|----------|
| **NiCd** | 1.2V | 1.4V / 1.0V | Low | 1000+ | **Yes** — must fully discharge before recharge | Power tools (mostly obsolete), old gear |
| **NiMH** | 1.2V | 1.4V / 1.0V | Medium | 500–1000 | Minimal (LSD NiMH like Eneloop: none) | **Best rechargeable AA/AAA** |
| **Lead-Acid** (SLA) | 2V per cell (6V, 12V) | 2.1V / 1.75V | Low | 200–500 | No | UPS, solar, alarm systems, car starting |
| **Li-ion** (LiCoO₂) | 3.7V | 4.2V / 3.0V | High | 300–500 | No | **Most common hobby battery** — 18650, 14500, pouches |
| **LiPo** (Li-ion Polymer) | 3.7V | 4.2V / 3.0V | High | 200–400 | No | Drones, RC, compact high-discharge projects |
| **LiFePO₄** | 3.2V | 3.6V / 2.5V | Medium | 2000+ | No | Solar, EVs, projects needing long cycle life |
| **Sodium-Ion** (Na-ion) | 3.3V | 3.6V / 2.0V | Medium | 1000+ | No | Emerging — cheaper than Li, less fire risk |

## What Nominal Voltage Actually Means

A battery's voltage is **not constant** — it changes with state of charge and load.

```
NiMH AA discharge curve:
  ┌─── 1.4V (full)
  │    ╲
  │     ╲──── 1.2V (most of the discharge — "nominal")
  │           ╲
  └───         1.0V (cutoff — don't go lower)

Li-ion 18650 discharge curve (under light load):
  ┌─── 4.2V (full)
  │    ╲
  │     ╲──── 3.7V (most of the discharge)
  │           ╲
  └───         3.0V (cutoff — protection circuit disconnects)
```

**When a device says "3.7V" it doesn't mean the battery outputs 3.7V exactly.** It means the battery spends most of its life around 3.7V, starting at 4.2V and ending at 3.0V. You must design your circuit's voltage regulator for the **entire range**, not just the nominal voltage.

## Form Factors

### Cylindrical Cells

The most common format across chemistries. Sizes are standardized:

| Designation | Size (diameter × length) | Typical capacity (Li-ion) | Typical capacity (NiMH) |
|-------------|-------------------------|---------------------------|--------------------------|
| **AAAA** | 8.3 × 42mm | — | ~625mAh |
| **AAA** | 10.5 × 44.5mm | — | 800–1100mAh |
| **AA** | 14.5 × 50.5mm | — | 1000–2500mAh |
| **C** | 26 × 50mm | — | 2500–5000mAh |
| **D** | 34 × 61mm | — | 5000–10000mAh |
| **9V (PP3)** | 26 × 17 × 48mm (prism) | — | 200–300mAh |
| **14500** | 14 × 50mm (AA-sized) | 600–1000mAh | — |
| **18650** | 18 × 65mm | 2000–3500mAh | — |
| **21700** | 21 × 70mm | 4000–5000mAh | — |
| **26650** | 26 × 65mm | 5000–6500mAh | — |
| **32700** | 32 × 70mm | 6000–7000mAh | — |

> **14500 is the same size as AA.** They are NOT interchangeable voltage-wise. 14500 = 3.7V Li-ion, AA = 1.2–1.5V. Using a 14500 in a device designed for AA will destroy it.

### Coin / Button Cells

| Cell | Chemistry | Voltage | Capacity | Common Use |
|------|-----------|---------|----------|------------|
| **CR2032** | Lithium Primary | 3.0V | 200–240mAh | RTC backup, key fobs, small sensors |
| **CR1220** | Lithium Primary | 3.0V | 35–40mAh | Key fobs, small wearables |
| **SR626SW** | Silver Oxide | 1.55V | 25–30mAh | Watches, calculators |
| **LR44 / AG13** | Alkaline | 1.5V | 100–150mAh | Small toys, laser pointers |
| **LIR2032** | Li-ion (rechargeable) | 3.6V | 40–60mAh | Rechargeable RTC backup |

### Pouch / Prismatic

- **LiPo pouch** — soft plastic envelope, no metal can. Thin, light, can be made in any shape. Used in phones, drones, wearables. **Easily damaged by puncture.**
- **Prismatic Li-ion** — hard rectangular case, common in phones and power banks. Higher density than 18650 but bulkier.

## Lead-Acid Sub-Types

| Type | Abbreviation | Electrolyte | Best For |
|------|-------------|-------------|----------|
| **Flooded** (wet cell) | — | Liquid acid (free-flowing) | Car starting batteries — cheap, can gas, must be upright |
| **SLA** (Sealed Lead-Acid) | SLA | Liquid acid (sealed, spill-proof) | UPS, alarm systems, emergency lights |
| **AGM** (Absorbent Glass Mat) | AGM | Acid absorbed in fiberglass mat | Start-stop cars, solar, high-vibration environments |
| **Gel Cell** | GEL | Acid turned to gel with silica | Deep-cycle, marine, applications where spill is catastrophic |

Sealed lead-acid (SLA, AGM, Gel) are **not interchangeable with flooded** — they have different charge voltage limits. Gel cells in particular are **easily damaged by overvoltage**.

## Nickel-Based Detail

### NiCd (Nickel-Cadmium)

- **The old guard.** Widely used in 1990s–2000s power tools and cordless phones.
- **Memory effect is real** — if you repeatedly charge a partially-discharged NiCd, it "remembers" that reduced capacity. Requires periodic full discharge.
- **Cadmium is toxic** — banned or restricted in many countries (EU RoHS). NiCd batteries must be recycled properly.
- Very robust against overcharging (trickle charge OK) and cold temperatures.

> **Verdict:** Obsolete for almost all hobby use. Replace with NiMH or Li-ion.

### NiMH (Nickel-Metal Hydride)

- **Modern replacement for NiCd.** Higher capacity, less toxic, minimal memory effect.
- **Self-discharge** was NiMH's original weakness (20–30% per month), solved by **LSD NiMH**:
  - **LSD = Low Self-Discharge.** Branded as Eneloop, IKEA LADDA, Amazon Basics.
  - Holds 70–85% charge after 1 year.
  - **Pre-charged and ready to use** out of the package.
  - **Does NOT suffer from memory effect.** Treat them like Li-ion — charge whenever.
- **Delta-V detection** for charging — NiMH has a small voltage drop when full. Most smart chargers detect this (ΔV = −10mV per cell).
- **High self-discharge non-LSD NiMH:** Good for high-drain uses (camera flashes, RC cars) where you use and recharge the same day.

### Charging NiMH

| Parameter | Value |
|-----------|-------|
| Charge rate (fast) | 0.5C–1C (e.g., 2000mA for a 2000mAh cell) |
| Charge termination | Delta-V (−10mV/cell) or temperature |
| Trickle charge | 0.05C–0.1C (only if not LSD, LSD doesn't need it) |
| Fully charged | 1.4–1.5V resting |
| Storage | Any state of charge — NiMH has low self-discharge when LSD |

> **NiMH chargers ≠ Li-ion chargers.** If you put a NiMH cell in a Li-ion charger set to Li-ion, it will overcharge and fail. Use a **smart chemistry-detecting charger** (like an Opus BT-C3100 or ISDT).

## Lithium-Based Detail

### Li-ion (Lithium Cobalt Oxide — LiCoO₂)

- **The workhorse.** Powers phones, laptops, power tools, and most hobby electronics.
- Highest energy density of mainstream rechargeable chemistries.
- **Requires a protection circuit** to prevent overcharge (>4.2V), over-discharge (<3.0V), and short circuit.
- **Protected 18650 cells** have a tiny PCB on the bottom that does this. **Unprotected cells** need an external BMS.
- **Do NOT use unprotected 18650 in hobby projects** unless you have a proper BMS.

### LiPo (Lithium Polymer)

- **Same chemistry as Li-ion, different packaging.** The electrolyte is a gel/polymer, not a liquid, allowing soft packaging.
- **Higher discharge rates** than cylindrical Li-ion (20C, 30C, 50C+ rated).
- **Extremely sensitive to physical damage.** Puncture = fire. Don't fold, pinch, or compress.
- **No hard shell** — can swell if damaged or overcharged. A swollen LiPo is a fire risk.
- Used in drones, RC cars, and any application needing high current in a small package.

### LiFePO₄ (Lithium Iron Phosphate)

- **Safer, longer life, lower energy density.**
- Lower nominal voltage (3.2V vs 3.7V) — **not interchangeable** with standard Li-ion.
- **Very flat discharge curve:** 3.3–3.0V over most of the discharge. Hard to estimate SoC by voltage alone.
- 2000+ charge cycles (vs 300–500 for LiCoO₂).
- Does NOT burn as violently as LiCoO₂ if punctured.
- Common in solar, UPS, EV conversions, and projects that need high cycle life.
- **Charge to 3.6V max** (not 4.2V!). Charging a LiFePO₄ with a standard Li-ion charger damages it.

### Li-ion Charge Profiles

| Chemistry | Full V | Cutoff V | Charge method | Charge C-rate |
|-----------|--------|----------|--------------|---------------|
| **Li-ion (LiCoO₂)** | 4.20V ±0.05V | 3.0V | CCCV (Constant Current, Constant Voltage) | 0.5C–1C |
| **LiPo** | 4.20V ±0.05V | 3.0V | CCCV | 0.5C–1C (higher if rated) |
| **LiFePO₄** | 3.60V ±0.05V | 2.5V | CCCV | 0.5C–1C |
| **LTO** (Lithium Titanate) | 2.70V | 1.8V | CCCV | 1C–5C |

**CCCV charging means:**
1. **CC (Constant Current)** — charger delivers fixed current until cell hits target voltage
2. **CV (Constant Voltage)** — holds that voltage, current gradually drops to near zero
3. **Termination** — charger cuts off when current drops below ~0.05C

```
Li-ion CCCV curve:
Current
  ┌─── CC phase ────┐
  │                 │ CV phase
  │   1A         ───┼── target V reached
  │                 │╲
  │                 │ ╲ current drops
  └─────────────────┴── cutoff (50mA)
```

## Emerging Chemistries

| Chemistry | Nominal V | Status | What's Promising |
|-----------|-----------|--------|------------------|
| **Sodium-Ion (Na-ion)** | 3.0–3.3V | Early commercial | Sodium is abundant (cheaper than lithium). No cobalt. Less fire risk. Slightly lower energy density. |
| **Solid State** | 3.5–4.0V (varies) | Prototype / early production | No liquid electrolyte = no fire. Higher density potential. Still expensive. |
| **Lithium-Sulfur (Li-S)** | ~2.2V | Research | Very high theoretical density (5× Li-ion). Short cycle life still. |
| **Salt Water / Aqueous** | ~1.0V | Experimental | Uses salt water electrolyte. Cheap, absolutely non-flammable. Very low voltage. |

### Sodium-Ion In Practice

Sodium-ion is the most likely near-term replacement for Li-ion in stationary storage and budget applications. Key differences:
- Can be **fully discharged to 0V** for transport/storage (no copper dissolution issue like Li-ion)
- Operates well in **cold temperatures** (−20°C)
- Uses **aluminum foil** for both anode and cathode (Li-ion needs copper for anode)
- Energy density: 120–160 Wh/kg (vs 200–260 for Li-ion)
- **Available now in 18650 and 26650 formats** from some Chinese manufacturers (CATL, HiNa)

> **For now:** Stick with Li-ion or NiMH for hobby projects. Sodium-ion modules exist but ecosystem (chargers, protection circuits, balance boards) is immature.

## Self-Discharge Comparison

How much charge a battery loses per month sitting unused:

```
Lithium Primary     → 0.5–1% / year     ← best for emergency/backup
Alkaline            → 1–2% / year       ← good
LSD NiMH (Eneloop)  → 10–15% / year     ← very good — grab-and-go
Li-ion (standard)   → 1–5% / month      ← fine for daily use
NiMH (standard)     → 20–30% / month    ← bad — recharge before use
NiCd                → 10–15% / month    ← moderate
Lead-Acid (SLA)     → 3–10% / month     ← moderate, keep topped up
```

## Safety by Chemistry

| Chemistry | Fire Risk | Venting | Toxicity | Notes |
|-----------|-----------|---------|----------|-------|
| **Alkaline** | Low | Can leak KOH (corrosive) | Low | Old cells leak white crust — clean with vinegar |
| **Zinc-Carbon** | Low | Can leak | Low | Cheap, leak-prone |
| **NiMH** | Low | Safe vent | Low | Very safe chemistry |
| **NiCd** | Low | Safe vent | **High (cadmium)** | Must recycle, banned in some regions |
| **Lead-Acid** | Medium (hydrogen gas) | Vents explosive H₂ | **High (lead)** | Sparks near charging lead-acid = explosion risk |
| **Li-ion / LiPo** | **High** (thermal runaway) | Vents flammable gas | Moderate | Thermal runaway = fire. Needs protection circuit. |
| **LiFePO₄** | Low | Safe vent | Low | Safest lithium chemistry |
| **Sodium-Ion** | Low | Safe vent | Low | Non-flammable, safer than Li |

### Thermal Runaway (Li-ion)

This is the BIG danger with standard Li-ion/LiPo:

```
Overcharge or internal short → temperature rises → separator melts → internal short grows → temperature spikes → cell vents flame → adjacent cells also go
```

**Prevention:**
1. Always use a BMS or protected cells
2. Never charge unattended
3. Charge in a fireproof container (LiPo bag, ammo box with vent holes) for high-capacity packs
4. Stop using immediately if voltage is abnormal, cell is hot, or case is swollen

## Battery Math Quick Reference

```
Capacity (Wh) = Voltage (V) × Capacity (Ah)

Runtime (hours) = Capacity (Ah) / Load current (A)

C-rate = discharge current / capacity
  1C   = 2000mA for a 2000mAh cell
  0.5C = 1000mA
  2C   = 4000mA

Example:
  3000mAh 18650 powering an ESP32 drawing 80mA
  → 3.0Ah / 0.08A = 37.5 hours

Same 18650 powering a 1A motor
  → 3.0Ah / 1.0A = 3 hours
```

## See Also

- [Power & Batteries — Supply Guide](/fundamentals/power-batteries) — practical power source selection, voltage regulation, power budgeting
- [Voltage Regulators](/components/voltage-regulator) — keeping voltage steady from a dying battery
- [Boost Converter](/fundamentals/boost-converter) — stepping battery voltage up
- [Battery Charger (TP4056)](/components/battery-charger) — charging 18650 Li-ion
