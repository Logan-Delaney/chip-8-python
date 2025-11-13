import pygame
from cpu import CPU
from memory import initialize_memory, load_rom
from display import Display
import numpy as np

# --- Declare Constants ---
running = True
sound_playing = False
cycles = 12
key_mapping = {
    pygame.K_1: 0x1,
    pygame.K_2: 0x2,
    pygame.K_3: 0x3,
    pygame.K_4: 0xC,
    pygame.K_q: 0x4,
    pygame.K_w: 0x5,
    pygame.K_e: 0x6,
    pygame.K_r: 0xD,
    pygame.K_a: 0x7,
    pygame.K_s: 0x8,
    pygame.K_d: 0x9,
    pygame.K_f: 0xE,
    pygame.K_z: 0xA,
    pygame.K_x: 0x0,
    pygame.K_c: 0xB,
    pygame.K_v: 0xF,
}
width = 64 * 20
height = 32 * 20

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('CHIP-8 Emulator')
pygameClock = pygame.time.Clock()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

# --- Create Sound ---
sample_rate = 22050
frequency = 440  # Hz (A4 note)
duration = 0.1
num_samples = int(sample_rate * duration)
samples = np.sin(2 * np.pi * frequency * np.linspace(0, duration, num_samples))
samples = (samples * 32767).astype(np.int16)
beep_sound = pygame.mixer.Sound(samples)

# --- Initialize Emulator Components ---
memory = initialize_memory()
with open('roms/tetris.ch8', 'rb') as f:
    rom = f.read()
load_rom(memory, rom)
cpu = CPU()
display = Display()
keys = [False] * 16

# --- Main Loop ---
while running:
    event_list = pygame.event.get()  # check if pygame is closed
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in key_mapping:
                chip8_key = key_mapping[event.key]
                keys[chip8_key] = True

        if event.type == pygame.KEYUP:
            if event.key in key_mapping:
                chip8_key = key_mapping[event.key]
                keys[chip8_key] = False

    for i in range(cycles):  # run cpu cycles per frame
        cpu.cycle(memory, display, keys)

    cpu.update_timers()     # update screen and timers
    if cpu.sound_timer > 0:
        if not sound_playing:
            beep_sound.play(-1)  # Loop
            sound_playing = True
    else:
        if sound_playing:
            beep_sound.stop()
            sound_playing = False

    display.render(screen)
    pygame.display.flip()
    pygameClock.tick(60)

# --- Cleanup ---
pygame.quit()