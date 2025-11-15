import pygame
from cpu import CPU
from memory import initialize_memory, load_rom
from display import Display
from constants import CYCLES, WIDTH, HEIGHT
from sound import create_sound, handle_sound
from input import handle_input

# --- Declare Constants ---
running = True
sound_playing = False

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CHIP-8 Emulator')
pygameClock = pygame.time.Clock()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
beep_sound = create_sound()

# --- Initialize Emulator Components ---
memory = initialize_memory()
with open('roms/space_invaders.ch8', 'rb') as f:
    rom = f.read()
load_rom(memory, rom)
cpu = CPU()
display = Display()
keys = [False] * 16

# --- Main Loop ---
while running:
    event_list = pygame.event.get()
    running = handle_input(event_list, keys)
    for i in range(CYCLES):  # run cpu cycles per frame
        cpu.cycle(memory, display, keys)
    cpu.update_timers()     # update screen and timers
    sound_playing = handle_sound(cpu.sound_timer, sound_playing, beep_sound)
    display.render(screen)
    pygame.display.flip()
    pygameClock.tick(60)

# --- Cleanup ---
pygame.quit()