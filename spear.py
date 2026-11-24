import pygame
import math

class Spear(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.original_image = pygame.Surface((30, 2), pygame.SRCALPHA)
        self.ss = pygame.image.load("spear.png")
        self.original_image.blit(self.ss, (0,0), (0,0,30,2))
        # calc angle to go towards mouse
        dx = target_x - start_x
        dy = target_y - start_y
        self.angle = math.atan2(dy, dx)
        
        # make sure spear points to mouse
        angle_degrees = math.degrees(-self.angle)
        self.image = pygame.transform.rotate(self.original_image, angle_degrees)
        
        self.rect = self.image.get_rect(center=(start_x, start_y))
        
        self.x = float(start_x)
        self.y = float(start_y)
        self.speed = 12
        
        #angle sets the velocity 
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)
        #kill if go off screen 
        if self.rect.right < 0 or self.rect.left > 1120 or self.rect.bottom < 0 or self.rect.top > 640:
            self.kill()