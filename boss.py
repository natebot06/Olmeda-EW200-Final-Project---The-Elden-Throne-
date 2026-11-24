import pygame
import math
import random
from hammer import Hammer
from healthbar import Healthbar 

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, hammer_group, spear_group, player, walls):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.hammer_group = hammer_group
        self.spear_group = spear_group
        self.player = player
        self.walls = walls
        
        self.image = pygame.image.load('image-removebg-preview.png')
        self.image = pygame.transform.rotozoom(self.image, 0, .5)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # boss stats
        self.speed = 6
        self.throw_timer = 0
        #anywhere from 1 second to 3 seconds the hammer can be thrown 
        self.throw_cooldown = random.randint(60, 180)
        self.maxhealth = 1000
        self.health = 1000
        self.name = "Sir Gideon The Gilded"
        self.font = pygame.font.Font("C:/Users/m294902/Documents/EW200/FINAL PROJECT 'The Fire Throne'/old-gangstriad-font/OldGangstriad-V48xy.otf", 28)
        self.name_surface = self.font.render(self.name, 1, (255,215,0))
        #healthbar instance 
        self.health_bar = Healthbar(260, 580, 600, 40, self.maxhealth, (255, 0, 0), (50, 0, 0))
        
    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
    def update(self):
        # throw the hammer if the timer reaches the randomized cooldown 
        self.throw_timer += 1
        if self.throw_timer >= self.throw_cooldown:
            self.throwhammer()
            self.throw_timer = 0
            #reset cooldown 
            self.throw_cooldown = random.randint(60, 180) 
            
        # move and dodge 
        self.dodge_spears()
        self.rect.center = (self.x, self.y)

    def dodge_spears(self):
        #set flags and initial conditions 
        dx, dy = 0, 0
        in_danger = 0
        
        # check spears
        for spear in self.spear_group:
            # distance between boss and spear
            dist = math.hypot(spear.x - self.x, spear.y - self.y)
            
            # if a spear is within 250 pixels, try to run away from it
            if dist < 250:
                in_danger = 1
                dx -= (spear.x - self.x)
                dy -= (spear.y - self.y)
        move_x, move_y = 0,0       
        if in_danger:
            # make it so the boss does not move faster diagnolaly 
            length = math.hypot(dx, dy)
            if length != 0:
                move_x += (dx/length) * self.speed
                move_y += (dy/length) * self.speed
        else:
            # if safe slowly move 
            if self.x < 600: move_x = 1
            if self.x > 900: move_x = -1
            if self.y < 200: move_y = 1
            if self.y > 400: move_y = -1
        
        #make sure the boss is moving and recognize the x and y directions so the collision mechanics work properly 
        self.x += move_x
        self.rect.centerx = self.x
        for wall in self.walls:
            if self.rect.colliderect(wall):
                if move_x>0: self.rect.right = wall.left
                if move_x<0: self.rect.left = wall.right
                self.x = self.rect.centerx
        self.y += move_y
        self.rect.centery = self.y
        for wall in self.walls:
            if self.rect.colliderect(wall):
                if move_y>0: self.rect.bottom = wall.top
                if move_y<0: self.rect.top = wall.bottom
                self.y = self.rect.centery
        # keep boss on screen
        self.x = max(0, min(self.x, 1070))
        self.y = max(0, min(self.y, 590))

    def throwhammer(self):
        # aim at the player
        hammerthrow = pygame.mixer.Sound("throw.mp3")
        hammerthrow.play()
        new_hammer = Hammer(self.x, self.y, self.player.x, self.player.y)
        self.hammer_group.add(new_hammer)
    def draw_bars(self, surface):
        self.health_bar.draw(surface, self.health)
        surface.blit(self.name_surface, (260, 550))