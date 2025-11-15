# CHIP-8 Emulator

A fully functional CHIP-8 emulator built in Python with pygame. Supports all 35 opcodes, graphics, sound, and keyboard input.

## Features

- Complete implementation of all 35 CHIP-8 opcodes
- 64x32 monochrome display scaled by 20 with sprite rendering
- Delay and sound timers running at 60Hz
- 16-key keyboard input support
- Programmatic beep sound generation
- Configurable CPU speed

## Requirements

- Python 3.8+
- pygame
- numpy

## Installation

1. Clone the repository:

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Controls

The CHIP-8 keypad is mapped to your keyboard as follows:
```
CHIP-8 Keypad:    Keyboard Mapping:
1 2 3 C           1 2 3 4
4 5 6 D           Q W E R
7 8 9 E           A S D F
A 0 B F           Z X C V
```

## Acknowledgments

Built as a learning project to understand emulation, CPU architecture, and low-level programming concepts.