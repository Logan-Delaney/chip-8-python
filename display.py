import pygame

class Display:
    def __init__(self):
        self.width = 64
        self.height = 32
        self.display = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def clear(self):
        self.display = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def get_pixel(self, x, y):
        return self.display[y][x]

    def set_pixel(self, x, y, value):
        self.display[y][x] = value

    def draw_sprite(self, x, y, sprite_data, height):
        collision = False
        for i in range (height):
            byte = sprite_data[i]
            for j in range (8):
                newY = (y + i) % 32
                newX = (x + j) % 64
                bit = byte & (0x80 >> j)
                if bit != 0:
                    pixel = self.display[newY][newX]
                    result = pixel ^ 1
                    self.display[newY][newX] = result
                    if pixel == 1 and result == 0:
                        collision = True

        return collision


    def render(self, screen):
        black = (0, 0, 0)
        white = (255, 255, 255)
        scale_factor = 20
        screen.fill(black)
        for y in range(32):
            for x in range(64):
                xx = x * scale_factor
                yy = y * scale_factor
                if self.display[y][x]:
                    pygame.draw.rect(screen, white, (xx, yy, scale_factor, scale_factor))