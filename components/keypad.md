# Keypad (Matrix 4x4) — Component Reference

## What It Is

A matrix keypad is a grid of push buttons arranged in **rows and columns**. The 4×4 keypad (16 buttons) uses only 8 microcontroller pins instead of 16. Common in security systems, door locks, and calculator-style input.

```
Row 1 ─┬──── ┬──── ┬──── ┬────
        │     │     │     │
        [1]   [2]   [3]   [A]
        │     │     │     │
Row 2 ─┼──── ┼──── ┼──── ┼────
        │     │     │     │
        [4]   [5]   [6]   [B]
        │     │     │     │
Row 3 ─┼──── ┼──── ┼──── ┼────
        │     │     │     │
        [7]   [8]   [9]   [C]
        │     │     │     │
Row 4 ─┼──── ┼──── ┼──── ┼────
        │     │     │     │
        [*]   [0]   [#]   [D]
        │     │     │     │
       Col1  Col2  Col3  Col4
```

## Pinout

Most 4×4 keypads have 8 pins (usually in a single-row header):

| Pin | Label | Purpose |
|-----|-------|---------|
| 1 | R1 | Row 1 |
| 2 | R2 | Row 2 |
| 3 | R3 | Row 3 |
| 4 | R4 | Row 4 |
| 5 | C1 | Column 1 |
| 6 | C2 | Column 2 |
| 7 | C3 | Column 3 |
| 8 | C4 | Column 4 |

**Check your specific keypad.** Pin 1 is usually marked with a square pad or arrow. The row/column order varies between manufacturers.

## Wiring

```
Keypad              Microcontroller
  R1 ──────────────── GPIO
  R2 ──────────────── GPIO
  R3 ──────────────── GPIO
  R4 ──────────────── GPIO
  C1 ──────────────── GPIO
  C2 ──────────────── GPIO
  C3 ──────────────── GPIO
  C4 ──────────────── GPIO
```

No pull-up resistors needed — the library enables the microcontroller's internal pull-ups.

## How Matrix Scanning Works

The microcontroller scans the keypad by:

1. Setting all column pins HIGH (with pull-ups)
2. Setting one row pin LOW at a time
3. Reading the column pins to see which columns are pulled LOW
4. If a column reads LOW while a row is LOW, that row+column intersection is pressed

This happens so fast (microseconds per scan) that no keypress is missed.

## Library

Use the **Keypad** library (mark-stanley / Arduino):

```cpp
#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3, 2};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();
  if (key) {
    Serial.println(key);
  }
}
```

## Debouncing

The **Keypad** library handles debouncing internally. The default debounce time is 10ms. You can change it:

```cpp
keypad.setDebounceTime(50);  // 50ms debounce
```

If you're getting multiple reads from a single press, increase the debounce time. If keypresses are being missed, decrease it.

## Multi-Key Press (2+ Keys Simultaneously)

A basic matrix keypad cannot distinguish all multi-key combinations. If you press two keys in the same row, the scan may see a third "phantom" key at the intersection:

```
Pressing 1 and 3:
  R1 LOW ──── [1]──┬───[3]── C3 LOW → detects 1 and 3 correctly
                    │
                    └─── C1 LOW → also detects phantom?

Solution: Add diodes on each button (or use a keyboard encoder)
```

For most hobby projects, single-key presses are sufficient. If you need multi-key, add an **I2C GPIO expander** (MCP23017) and read each key individually.

## Custom Keypad Layouts

You can make your own keypad with any combination of buttons:

```cpp
// 3×4 keypad (phone layout, no A/B/C/D)
const byte ROWS = 4;
const byte COLS = 3;
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};
```

Rows and columns don't have to be sequential on your PCB — assign them to any GPIOs:

```cpp
byte rowPins[ROWS] = {12, 14, 27, 26};
byte colPins[COLS] = {25, 33, 32};
```

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| No keys detected | Row/column mapping wrong | Swap row and column pin arrays |
| No keys detected | GPIOs not configured correctly | Library handles this — check pins are valid |
| Multiple keys detected from one press | Phantom key (multi-press) | Don't press two keys at the same time |
| Key repeat (same key fires multiple times) | Debounce too short | Increase debounce time or add state tracking |
| Intermittent readings | Loose wiring | Check connections, solder if on breadboard |
| Keys in wrong order | keymap array doesn't match wiring | Check which pin is row 1/col 1 on your specific keypad |

## Quick Reference

- **4×4 keypad:** 16 buttons, 8 pins (4 rows + 4 columns)
- **Library:** Keypad (mark-stanley) — handles scanning and debouncing
- **Wiring:** Any 8 GPIOs — rows and columns are interchangeable in software
- **Key mapping:** `char keys[ROWS][COLS]` — match the physical layout
- **No pull-ups needed:** Library uses internal pull-ups
- **Single-key press:** Only reliable for one key at a time
- **Multi-key:** Diodes needed per button, or use I2C expander
- **3×4 keypad:** Also common — 12 keys, 7 pins
