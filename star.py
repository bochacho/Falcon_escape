import pygame
from pygame.locals import RLEACCEL
import random

class Star(pygame.sprite.Sprite):
    def __init__(self, canvas_size):
        super(Star,self).__init__()
        rand_size = random.randint(2, 10)
        img = pygame.image.load("Assets/star.png")
        scaled_img = pygame.transform.scale(img, (rand_size, rand_size*1.3))

        self.surf = scaled_img.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(canvas_size[0] + 20 , canvas_size[0] + 100),
                random.randint(0, canvas_size[1])
            )
        )
        self.speed = 1

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
    
    def set_cent(self,x,y):
        self.rect.center = (x,y)