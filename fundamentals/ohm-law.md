# Ohm's Law & Basic Circuit Theory — Fundamental Reference

## What It Is

Ohm's Law is the single most important formula in electronics. It describes how **voltage, current, and resistance** relate to each other:

```
Voltage (V) = Current (I) × Resistance (R)
     V       =      I      ×      R
```

## The Three Formulas

| Want to find | Formula | Analogy |
|-------------|---------|---------|
| Voltage | V = I × R | Water pressure |
| Current | I = V / R | Water flow rate |
| Resistance | R = V / I | Pipe narrowness |

**The water analogy:** Voltage is water pressure, current is how much water flows, resistance is how much you pinch the hose. Pinch harder (more resistance) → less flow (less current). Same pressure, narrower pipe.

## Applying Ohm's Law

### Example 1: LED Resistor

You have a 5V supply and a 2V LED that needs 20mA:

```
R = (5V - 2V) / 0.02A = 150Ω
```

Use the nearest standard value: 150Ω or 220Ω.

### Example 2: Voltage Across a Resistor

A 10kΩ resistor has 2mA flowing through it:

```
V = 0.002A × 10000Ω = 20V
```

### Example 3: Current Through a Circuit

A 12V supply with a 470Ω resistor:

```
I = 12V / 470Ω = 0.0255A = 25.5mA
```

## Power (Wattage)

Power tells you how much energy a component dissipates as heat:

```
Power (P) = V × I = I² × R = V² / R
```

**Why it matters:** A resistor rated for 1/4W will burn up if you put 1W through it.

### Example

Same LED circuit from above: 3V across the resistor at 20mA:

```
P = 3V × 0.02A = 0.06W
```

A 1/4W (0.25W) resistor is fine. 0.06W < 0.25W. Always leave a 2× margin.

## Series vs Parallel

### Resistors in Series

Total resistance adds up:

```
R_total = R1 + R2 + R3 + ...
```

Used for: voltage dividers, combining values.

### Resistors in Parallel

Total resistance is LESS than the smallest resistor:

```
1/R_total = 1/R1 + 1/R2 + 1/R3 + ...
```

Two 10kΩ resistors in parallel = 5kΩ.

### Voltage in Series

Voltages across components in series add up to the supply voltage:

```
V_supply = V_R1 + V_R2 + V_R3 + ...
```

### Current in Parallel

Branch currents add up:

```
I_total = I1 + I2 + I3 + ...
```

## Kirchhoff's Laws

### Kirchhoff's Current Law (KCL)

Current entering a junction = current leaving it. What goes in must come out.

### Kirchhoff's Voltage Law (KVL)

The sum of all voltage drops around a closed loop equals the supply voltage.

These laws let you solve any resistor network. Combined with Ohm's Law, they cover 90% of circuit analysis.

## Quick Reference

| Quantity | Symbol | Unit | Symbol | Measured with |
|----------|--------|------|--------|---------------|
| Voltage | V | Volt | V | Multimeter (parallel) |
| Current | I | Ampere | A | Multimeter (series) |
| Resistance | R | Ohm | Ω | Multimeter (ohms mode) |
| Power | P | Watt | W | Calculated (V × I) |

- **Ohm's Law:** V = I × R
- **Power:** P = V × I
- **Series current:** Same everywhere
- **Parallel voltage:** Same everywhere
- **Safety:** Never short a voltage source. Current tries to be infinite, something burns.

## See Also

- [relay-module](/projects/relay-module)
- [hc-sr04-ultrasonic](/projects/hc-sr04-ultrasonic)
