import math
from turtle import speed
import pygame
from pygame.locals import RLEACCEL
import random
from lazer import Lazer
import numpy as np


move_list = ['UP', 'DOWN', 'LEFT', 'RIGHT']
padding = 10


class Enemy(pygame.sprite.Sprite):

    def __init__(self, canvas_size, health, start_place):
        super(Enemy, self).__init__()
        img = pygame.image.load("Assets/Tie.png")
        self.surf = img.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                start_place[0],
                start_place[1]
            )
        )
        self.speedX = 2
        self.speedY = 3
        self.health = health
        self.canvas_size = canvas_size
        self.on_screen = False
    '''
    def update_x(self):
        #IF AND ONLY IF the target is on the target location, keep doing loops with sin 


        pass
    '''
    '''
    def update(self):
        angle_var = self.rect.centery - self.speedY
        angle = math.radians(360*angle_var/self.canvas_size[1])
        amplitude_x = 60
        move_x = self.speedX*math.sin(angle)
        move_y = self.speedY*math.sin(angle/2)
        self.rect.move_ip(move_x, move_y)

    def update_y(self):
        if self.rect.bottom > self.canvas_size[1] - padding or self.rect.top < padding: 
            self.speedY = self.speedY*-1
        self.rect.move_ip(0, self.speedY)
    '''
    def damage(self, value):
        self.health -= value
        if self.health < 1:
            self.kill()
    
    def get_on_screen(self):
        if self.rect.right < self.canvas_size[0]*4/5:
            self.on_screen = True
        self.rect.move_ip(-self.speedX, 0)
        
    def shoot(self):
        lazer = Lazer(self.canvas_size, self.rect.center, 'red', 1, 10)
        return lazer