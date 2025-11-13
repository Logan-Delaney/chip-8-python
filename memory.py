from constants import FONTSET

def initialize_memory():
    memory = [0x00] * 4096
    write_fontset(memory, FONTSET)
    return memory

def write_fontset(memory, fontset):
    for i in range (0, 80):
        memory[i] = fontset[i]

def load_rom(memory, rom):
    memory_location = 0x200
    for i in range(len(rom)):
        memory[memory_location] = rom[i]
        memory_location += 1