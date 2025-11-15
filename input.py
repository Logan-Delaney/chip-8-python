import pygame
from constants import KEY_MAPPING

def handle_input(event_list, keys):
    for event in event_list:
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key in KEY_MAPPING:
                chip8_key = KEY_MAPPING[event.key]
                keys[chip8_key] = True

        if event.type == pygame.KEYUP:
            if event.key in KEY_MAPPING:
                chip8_key = KEY_MAPPING[event.key]
                keys[chip8_key] = False

    return True