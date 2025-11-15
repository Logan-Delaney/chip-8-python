import numpy as np
import pygame

def create_sound():
    sample_rate = 22050
    frequency = 440  # Hz (A4 note)
    duration = 0.1
    num_samples = int(sample_rate * duration)
    samples = np.sin(2 * np.pi * frequency * np.linspace(0, duration, num_samples))
    samples = (samples * 32767).astype(np.int16)
    beep_sound = pygame.mixer.Sound(samples)
    return beep_sound

def handle_sound(timer, currently_playing, sound):
    if timer > 0:
        if not currently_playing:
            sound.play(-1)
            return True
    else:
        if currently_playing:
            sound.stop()
            return False
    return currently_playing