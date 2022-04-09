import time
from tracemalloc import start
from venv import create
from numpy import False_
import pygame
import random

from player import Player
from star import Star
from meteor import Meteor
from enemy import Enemy
from lazer import Lazer

from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

#dimensions of the display screen
CANVAS_SIZE = WIDTH, HEIGHT = 800, 600

#Initializing pygame and creating the display screen
pygame.init()
screen = pygame.display.set_mode((CANVAS_SIZE))

#Creating custom Events
ADDMETEOR = pygame.USEREVENT + 1
pygame.time.set_timer(ADDMETEOR, 500)
ADDENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, 1000)
ADDSTAR = pygame.USEREVENT + 3
pygame.time.set_timer(ADDSTAR, 100)


player = Player(CANVAS_SIZE, 10)
meteor = Meteor(CANVAS_SIZE)
star = Star(CANVAS_SIZE)
enemy = Enemy(CANVAS_SIZE, 3, (0,0))
lazer = Lazer(CANVAS_SIZE, (0,0), 'blue', 1, 5)

#Creating Sprite groups for all the objects
meteors = pygame.sprite.Group()
stars = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_lazers = pygame.sprite.Group()
enemy_lazer = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

num_enemies = 5


running = True


#Creating stars for the starting screen
for _ in range(random.randint(40, 70)):
    star = Star(CANVAS_SIZE)
    star.set_cent(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    stars.add(star)
    all_sprites.add(star)


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                lazer = player.shoot()
                player_lazers.add(lazer)
                all_sprites.add(lazer)

        elif event.type == QUIT:
            running = False

        elif event.type == ADDMETEOR:
            meteor = Meteor(CANVAS_SIZE)
            meteors.add(meteor)
            all_sprites.add(meteor)

        elif event.type == ADDSTAR:
            star = Star(CANVAS_SIZE)
            stars.add(star)
            all_sprites.add(star)

        elif event.type == ADDENEMY & len(enemies) == 0:
            start_x = WIDTH + 20 
            start_y = HEIGHT/(num_enemies + 1)
            for i in range(num_enemies):
                enemy = Enemy(CANVAS_SIZE, 3, (start_x, start_y*i))
                enemies.add(enemy)
                all_sprites.add(enemy)

    screen.fill((0,0,0))

    key_pressed = pygame.key.get_pressed()
    player.update(key_pressed)
    meteors.update()
    stars.update()
    for i in enemies:
        i.update_x(WIDTH)
        i.update_y(HEIGHT)
    player_lazers.update()
    enemy_lazer.update()

    #make enemies shoot randomly
    if random.randint(0,6) == 6:
        enemies.spritedict

    all_sprites.add(player)


    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)
    
    #collission detection
    player_collission_meteor = pygame.sprite.spritecollideany(player, meteors)
    player_collission_lazer = pygame.sprite.spritecollide(player, enemy_lazer, False)
    enemy_collission_lazer = pygame.sprite.groupcollide(enemies, player_lazers, False, False)
    meteor_collission_lazer = pygame.sprite.groupcollide(meteors, player_lazers, False, False)

    if player_collission_meteor:
        player.damage(1)
    if player_collission_lazer:
        player.damage(2)
    if enemy_collission_lazer:
        for enemy in enemy_collission_lazer.keys():
            enemy.damage(2)
    if meteor_collission_lazer:
        for meteor in meteor_collission_lazer.keys():
            meteor.damage(2)

    
    


    pygame.display.flip()