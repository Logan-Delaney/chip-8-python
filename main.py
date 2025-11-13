import pygame
from cpu import CPU
from memory import initialize_memory, load_rom
from display import Display

# --- Declare Constants ---
running = True
cycles = 12

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((640, 320))
pygame.display.set_caption('CHIP-8 Emulator')
pygameClock = pygame.time.Clock()

# --- Initialize Emulator Components ---
memory = initialize_memory()
with open('roms/ibm_logo.ch8', 'rb') as f:
    rom = f.read()
load_rom(memory, rom)
cpu = CPU()
display = Display()

# --- Main Loop ---
while running:
    event_list = pygame.event.get()  # check if pygame is closed
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    for i in range(cycles):  # run cpu cycles per frame
        cpu.cycle(memory, display)

    display.render(screen)  # update screen
    pygame.display.flip()
    pygameClock.tick(60)

# --- Cleanup ---
pygame.quit()