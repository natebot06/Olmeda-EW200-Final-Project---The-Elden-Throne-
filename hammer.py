import pygame
from math import cos, sin, radians 
import pygame
import math

class Hammer(pygame.sprite.Sprite):
    def __init__(self, ix, iy, target_x, target_y):
        super().__init__()
        #convert alpha makes the image rotate and translate smoother 
        self.og_image = pygame.image.load('hammer.png').convert_alpha()
        self.og_image = pygame.transform.rotozoom(self.og_image, 0, .2)
        self.image = self.og_image
        self.rect = self.image.get_rect(center=(ix, iy))
        #make the location a float so it moves smoother 
        self.x = float(ix)
        self.y = float(iy)
        self.speed = 10
        self.spinangle = 0
        
        #angle to the player to set velocity
        angle = math.atan2(target_y - iy, target_x - ix)
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        
    def update(self):
        #move hammer
        self.x += self.vx
        self.y += self.vy
        
        #spin hammer
        self.spinangle += 15  
        #reset angle so it continuously spins 
        if self.spinangle >= 360:
            self.spinangle -= 360
            
        self.image = pygame.transform.rotate(self.og_image, self.spinangle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        #kill if goes off screen
        if self.rect.right < 0 or self.rect.left > 1120 or self.rect.bottom < 0 or self.rect.top > 640:
            self.kill()