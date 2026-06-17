# Battery Charger (TP4056) — Component Reference

## What It Is

The TP4056 is a **single-cell Li-ion / LiPo battery charger IC**. It's the most common charging chip in hobby electronics — found in power banks, ESP32 breakout boards, and countless DIY projects.

The module (typically that red/purple board with micro USB) handles everything: constant-current/constant-voltage charging, charge status indication, and protection.

## The TP4056 Module

```
                    ┌─────────────────────┐
                    │   TP4056 Charger     │
   Micro USB ───────┤                     ├────── Battery +
     5V in         │  CHRG  STDBY         │
                    │                      │
   GND ─────────────┤                     ├────── Battery -
                    │                     │
                    │  OUT+  OUT-         │
                    └─────────────────────┘
                         Load output
```

### Pinout

| Connection | Purpose |
|-----------|---------|
| IN+/VCC | 5V input (micro USB or solder pads) |
| GND | Ground |
| BAT+ | Battery positive |
| BAT- | Battery negative |
| OUT+/OUT- | Protected load output (some modules) |

### Indicators

| LED behavior | Meaning |
|-------------|---------|
| Red ON | Charging |
| Blue ON | Charging complete / standby |
| Red + Blue flashing | Battery disconnected, or too cold/hot |

## Charging Process

Li-ion charging follows a specific curve:

1. **Pre-conditioning** (if battery < 2.9V): Charge at 10% current until voltage reaches 2.9V
2. **Constant current** (CC): Charge at full current (default 1A) until voltage reaches 4.2V
3. **Constant voltage** (CV): Hold at 4.2V while current drops — stops when current falls below ~10% of full rate

Total charge time for a 2000mAh cell at 1A: ~2.5–3 hours.

## Setting the Charge Current

The charge current is set by a resistor (R_PROG) on the module. Common values:

| R_PROG | Charge current |
|--------|---------------|
| 1.2kΩ | 1A (default on most modules) |
| 2kΩ | 580mA |
| 5kΩ | 250mA |
| 10kΩ | 130mA |

On bare TP4056 chips, solder the appropriate resistor between PROG pin and GND. Most pre-built modules use 1.2kΩ for 1A.

**Heat note:** At 1A, the chip can reach 100°C+ without heatsinking. For sustained 1A charging, add airflow or reduce current to 500mA.

## Protection Features

### Basic TP4056 (no protection)

Just the charger chip — no over-discharge or short-circuit protection for the battery. Use with protected batteries or add a separate protection circuit.

### TP4056 + DW01 (with protection)

Most purple/red modules include a **DW01** protection IC and **FS8205** dual MOSFET:

- Over-discharge protection: cuts off at ~2.5V
- Over-current protection: cuts off at ~3A
- Short circuit protection
- Reverse battery protection (some modules)

**If the module has a blue LED,** it likely has protection. Check the back for the DW01 chip.

## Wiring Examples

### Charging Only

```
USB 5V ──── IN+ ──── TP4056 ──── BAT+ ──── Li-ion +
  GND ───── IN- ────         ──── BAT- ──── Li-ion -
```

### Charging + Load (ESP32 project)

```
USB 5V ──── IN+ ──── TP4056 ──── BAT+ ──── Battery +
  GND ───── IN- ────         ──── BAT- ──── Battery -
                         │
                       OUT+ ──── ESP32 VIN
                       OUT- ──── ESP32 GND
```

The load draws from the battery when USB is disconnected. When USB is connected, the battery charges AND the load runs.

### With Power Path (No DW01 issue)

The DW01 protection chip can cut battery power when it trips. Some modules have a separate load output (+/-) that bypasses protection for the load while still protecting the battery.

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| LED flashing (R+BL) | Battery disconnected or bad contact | Check battery wires and connectors |
| Module gets very hot | 1A charge current without heatsink | Reduce current (higher PROG resistor) or add airflow |
| Battery not charging | Supply voltage too low | Need at least 4.5V on IN+ (5V USB is ideal) |
| Battery charges too slowly | High PROG resistor | Replace with lower value for faster charge |
| Battery doesn't stop at 4.2V | Bad battery or damaged chip | Disconnect battery immediately, replace module |
| Voltage at BAT+ but module cold | Battery already full | Check if blue LED is on |

## Safety Rules

| Rule | Why |
|------|-----|
| **Never leave Li-ion charging unattended** | Thermal runaway is real. Fires happen. |
| **Use the correct charger** | TP4056 is for single-cell Li-ion (3.7V nominal, 4.2V max) |
| **Don't charge frozen batteries** | Below 0°C, charging can damage the cell |
| **Current limit** | 1A for standard 18650 cells. High-drain cells can take more |
| **Reverse polarity** | Most modules don't survive reverse battery connection |
| **Store at 3.7–3.8V** | Full charge (4.2V) degrades battery life over time |

## Quick Reference

- **Charges 3.7V Li-ion / LiPo** single cells to 4.2V
- **Default charge current:** 1A (set by R_PROG)
- **Input:** 5V DC (micro USB)
- **Indicators:** Red = charging, Blue = done
- **With DW01 protection:** Over-discharge, over-current, short circuit protection
- **Heat is normal** at 1A — provide airflow or reduce current
- **Never leave charging unattended**
- **Output (OUT+/-)** bypasses protection for load in some modules
