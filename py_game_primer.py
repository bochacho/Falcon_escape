# Simple pygame program

# Import and initialize the pygame library
import time
import pygame
import random


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


WIDTH = 800
HEIGHT = 600

#creating a player object by extending Sprite class - helps with collission detection?
class player(pygame.sprite.Sprite):
    def __init__(self):
        super(player, self).__init__()
        self.surf = pygame.image.load("Assets/falcon.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)

        #Creating a boundary
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def add_score(self, value):
        pass

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super(Meteor, self).__init__()
        rand_size = random.randint(20, 50)
        rand_rotate = random.randint(0,12)*30
        img = pygame.image.load("Assets/meteor.png")
        scaled_img = pygame.transform.scale(img, (rand_size, rand_size))
        rotated_img = pygame.transform.rotate(scaled_img, rand_rotate)

        self.surf = rotated_img.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(WIDTH +20 , WIDTH+100),
                random.randint(0, HEIGHT)
            )
        )
        self.speed = random.randint(5,15)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    move_list = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def __init__(self):
        super(Enemy, self).__init__()
        img = pygame.image.load("Assets/Tie.png")
        self.surf = img.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(WIDTH +20 , WIDTH+100),
                random.randint(0, HEIGHT)
            )
        )
        self.speed = random.randint(5,10)
        self.curr_move = 'LEFT'

    '''
    def update(self): 
        while self.rect.right > WIDTH:
            self.rect.move_ip(-self.speed, 0)
    '''    
    '''
    def update(self):
        if self.curr_move == 'RIGHT':
            self.rect.move_ip(self.speed, 0)
        elif self.curr_move == 'UP':
            self.rect.move_ip(0,-self.speed)
        elif self.curr_move == 'DOWN':
            self.rect.move_ip(0, self.speed)
        elif self.curr_move == 'LEFT':
            self.rect.move_ip(-self.speed, 0)

        if self.rect.left < WIDTH/2 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.curr_move = self.move_list[random.randint(0,3)]
    '''

    #let's just make it move up and down and then make it move left and right randomly 
    # Create 2 fns - updateX, updateY
    
    def update(self):
        if self.rect.right > WIDTH - 20:
            self.rect.move_ip(-self.speed, 0)
        else:
            if self.rect.left < WIDTH/2 or self.rect.right > WIDTH - 30 or self.rect.top < 0 or self.rect.bottom > HEIGHT:
                self.curr_move = random.choice(self.move_list)

            if self.curr_move == 'RIGHT':
                self.rect.move_ip(self.speed, 0)
            elif self.curr_move == 'UP':
                self.rect.move_ip(0,-self.speed)
            elif self.curr_move == 'DOWN':
                self.rect.move_ip(0, self.speed)
            elif self.curr_move == 'LEFT':
                self.rect.move_ip(-self.speed, 0)
    

    '''
    def update(self):
        if self.rect.left > WIDTH-20:
            self.rect.move_ip(-self.speed,0)
        else:
            border_hit = False
            if border_hit:
                curr_move = self.move_list[random.randint(0,3)]
                border_hit = False
            else:
                if curr_move == 'RIGHT':
                    self.rect.move_ip(self.speed, 0)
                elif curr_move == 'UP':
                    self.rect.move_ip(0,-self.speed)
                elif curr_move == 'DOWN':
                    self.rect.move_ip(0, self.speed)
                elif curr_move == 'LEFT':
                    self.rect.move_ip(-self.speed, 0)

                if self.rect.left < WIDTH/2 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
                    border_hit = True
    '''



class Star(pygame.sprite.Sprite):
    def __init__(self):
        super(Star,self).__init__()
        rand_size = random.randint(2, 10)
        img = pygame.image.load("Assets/star.png")
        scaled_img = pygame.transform.scale(img, (rand_size, rand_size*1.3))

        self.surf = scaled_img.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(WIDTH +20 , WIDTH+100),
                random.randint(0, HEIGHT)
            )
        )
        self.speed = 1

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
    
    def set_cent(self,x,y):
        self.rect.center = (x,y)

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((WIDTH,HEIGHT))

ADDMeteor = pygame.USEREVENT + 1
pygame.time.set_timer(ADDMeteor, 500)
ADDStar = pygame.USEREVENT + 2
pygame.time.set_timer(ADDStar, 100)
ADDTie = pygame.USEREVENT + 3
pygame.time.set_timer(ADDTie, 1000)

collission_count = 0

player = player()
meteor = Meteor()
star = Star()
tie = Enemy()

#Storing the explosion
explosion = pygame.image.load("Assets/explosion.png").convert_alpha()

meteors = pygame.sprite.Group()
stars = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

#Creating stars for the starting screen
for _ in range(random.randint(40, 70)):
    star = Star()
    star.set_cent(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    stars.add(star)
    all_sprites.add(star)


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDMeteor:
            meteor = Meteor()
            meteors.add(meteor)
            all_sprites.add(meteor)

        elif event.type == ADDStar:
            star = Star()
            stars.add(star)
            all_sprites.add(star)

        elif event.type == ADDTie:
            tie = Enemy()
            enemies.add(tie)
            all_sprites.add(tie)


    screen.fill((0,0,0))
    #returns a dict of all the keys pressed
    key_pressed = pygame.key.get_pressed()
    player.update(key_pressed)
    meteors.update()
    stars.update()
    enemies.update()

    for element in all_sprites:
        screen.blit(element.surf, element.rect)
    
    if pygame.sprite.spritecollideany(player, meteors):
        collission_count += 1
        if collission_count > 5:
            player.kill()
            screen.blit(explosion, (player.rect.x - player.rect.width/2, player.rect.y - player.rect.height/2)  )
            running = False
    pygame.display.flip()