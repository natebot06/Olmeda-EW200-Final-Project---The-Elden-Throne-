import pygame

class Healthbar():
    def __init__(self, x, y, width, height, max_value, b_color, a_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.a_color = a_color  
        self.b_color = b_color  #

    def draw(self, surface, current_value):
        
        current_value = max(0, min(current_value, self.max_value))
        ratio = current_value / self.max_value
        #base bar 
        a_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #adjustable bar 
        b_rect = pygame.Rect(self.x, self.y, self.width * ratio, self.height)
        pygame.draw.rect(surface, self.a_color, a_rect)
        pygame.draw.rect(surface, self.b_color, b_rect)
        