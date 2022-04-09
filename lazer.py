import pygame
import random
from pygame.locals import RLEACCEL

class Lazer(pygame.sprite.Sprite):
    #direction - 1 for right, -1 for left
    def __init__(self, canvas_size, start , color, direction, speed): 
        super(Lazer, self).__init__()
        img = pygame.image.load(f"Assets/{color}.png")
        self.surf = img.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                start[0],
                start[1]
            )
        )
        self.canvas_size = canvas_size
        self.speed = speed*direction

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0 or self.rect.left  > self.canvas_size[1] :
            self.kill()