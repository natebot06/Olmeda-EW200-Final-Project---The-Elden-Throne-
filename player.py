import pygame
from spear import Spear
from healthbar import Healthbar 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, spear_group, walls):
        super().__init__()
        self.ts = 16
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.ss = pygame.image.load("character.png")
        self.image.blit(self.ss, (0,0), (0,0,32,32))
        self.rect = self.image.get_rect(center=(x, y))
        self.walls = walls
        #self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.x = float(x)
        self.y = float(y)
        self.speed = 5
        self.spear_group = spear_group
        #set player stats 
        self.maxhealth = 100
        self.health = 100
        self.maxstamina = 100
        self.stamina = 100
        self.regenerate = 0.5
        #make stamina and healthbar from healthbar class 
        self.health_bar = Healthbar(20, 20, 250, 25, self.maxhealth, (0, 255, 0), (100, 0, 0))
        self.stamina_bar = Healthbar(20, 50, 200, 15, self.maxstamina, (0, 200, 255), (50, 50, 50))
    def update(self):
        keys = pygame.key.get_pressed()
        # WASD movement with keys list for smoothness
        
        directionx = 0 
        directiony = 0
        
        if keys[pygame.K_w]:
            directiony -= self.speed
        if keys[pygame.K_s]:
            directiony += self.speed
        if keys[pygame.K_a]:
            directionx -= self.speed
        if keys[pygame.K_d]:
            directionx += self.speed
        #make sure the player is moving and recognize the x and y directions so the collision mechanics work properly    
        self.x += directionx
        self.rect.centerx = self.x
        for wall in self.walls:
            if self.rect.colliderect(wall):
                if directionx>0:
                    self.rect.right = wall.left
                if directionx<0:
                    self.rect.left = wall.right
                self.x = self.rect.centerx
        
        self.y += directiony
        self.rect.centery = self.y
        for wall in self.walls:
            if self.rect.colliderect(wall):
                if directiony>0:
                    self.rect.bottom = wall.top
                if directiony<0:
                    self.rect.top = wall.bottom
                self.y = self.rect.centery
        # stamina function and regeneration 
        if self.stamina < self.maxstamina:
            self.stamina += self.regenerate
            
            if self.stamina > self.maxstamina:
                self.stamina = self.maxstamina 


    def throw_spear(self, mouse_pos):
        # new spear towards mouse
        staminacost = 20 
        if self.stamina >= staminacost:
            #spear instance and makiong the stamina function work 
            new_spear = Spear(self.rect.centerx, self.rect.centery, mouse_pos[0], mouse_pos[1])
            self.spear_group.add(new_spear)
            self.stamina -= staminacost 
    
    def drawbars(self, surface):
        self.health_bar.draw(surface, self.health)
        self.stamina_bar.draw(surface, self.stamina)
