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
ADDSHOOT = pygame.USEREVENT + 4
pygame.time.set_timer(ADDSHOOT, 500)


player = Player(CANVAS_SIZE, 15)
meteor = Meteor(CANVAS_SIZE)
star = Star(CANVAS_SIZE)
enemy = Enemy(CANVAS_SIZE, 3, (0,0))
lazer = Lazer(CANVAS_SIZE, (0,0), 'blue', 1, 5)

#Creating Sprite groups for all the objects
meteors = pygame.sprite.Group()
stars = pygame.sprite.Group()
enemies = pygame.sprite.Group()
players = pygame.sprite.Group()
player_lazers = pygame.sprite.Group()
enemy_lazer = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

num_enemies = 5

tiny_explosion = pygame.transform.scale(pygame.image.load("Assets/explosion.png"), (50, 50)).convert_alpha()
explosion = pygame.image.load("Assets/explosion.png").convert_alpha()


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

        elif event.type == ADDENEMY:
            if len(enemies) < 2:
                start_x = WIDTH + 20 
                start_y = HEIGHT/(num_enemies + 1)
                for i in range(1, num_enemies + 1):
                    enemy = Enemy(CANVAS_SIZE, 3, (start_x, start_y*i))
                    enemies.add(enemy)
                    all_sprites.add(enemy)
        elif event.type == ADDSHOOT:
            for enemy in enemies:
                if random.choice([True, False]):
                    lazer = enemy.shoot()
                    enemy_lazer.add(lazer)
                    all_sprites.add(lazer)

    screen.fill((0,0,0))

    key_pressed = pygame.key.get_pressed()
    player.update(key_pressed)
    meteors.update()
    stars.update()
    '''    
    for i in enemies:
        i.update_x()
        i.update_y()
    '''
    for enemy in enemies:
        if not enemy.on_screen:
            enemy.get_on_screen()
        #else:
        #    enemy.update()
    
    player_lazers.update()
    enemy_lazer.update()

    players.add(player)
    all_sprites.add(player)

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)
    
    #collission detection
    player_collission_meteor = pygame.sprite.groupcollide(players, meteors, False, False)
    player_collission_lazer = pygame.sprite.groupcollide(players, enemy_lazer, False, False)
    enemy_collission_lazer = pygame.sprite.groupcollide(enemies, player_lazers, False, False)
    meteor_collission_lazer = pygame.sprite.groupcollide(meteors, player_lazers, False, False)

    if player_collission_meteor:
        for player in player_collission_meteor:
            alive = player.damage(1)
            for meteor in player_collission_meteor[player]:
                meteor.kill()
            screen.blit(tiny_explosion, (player.rect.centerx - player.rect.width/2, player.rect.centery- player.rect.height/2)  )
            if not alive:
                screen.blit(explosion, (player.rect.x - player.rect.width/2, player.rect.y - player.rect.height/2))
                running = False

    if player_collission_lazer:
        for player in player_collission_lazer:
            alive = player.damage(2)
            for lazer in player_collission_lazer[player]:
                lazer.kill()
            screen.blit(tiny_explosion, (player.rect.centerx - player.rect.width/2, player.rect.centery- player.rect.height/2)  )
            if not alive:
                screen.blit(explosion, (player.rect.x - player.rect.width/2, player.rect.y - player.rect.height/2))
                running = False

    if enemy_collission_lazer:
        for enemy in enemy_collission_lazer.keys():
            enemy.damage(2)
            for lazer in enemy_collission_lazer[enemy]:
                lazer.kill()
            screen.blit(tiny_explosion, enemy.rect)
    if meteor_collission_lazer:
        for meteor in meteor_collission_lazer.keys():
            meteor.damage(2)
            screen.blit(tiny_explosion, meteor.rect)
            for lazer in meteor_collission_lazer[meteor]:
                lazer.kill()

    pygame.display.flip()