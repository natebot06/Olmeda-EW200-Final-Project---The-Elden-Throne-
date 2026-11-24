import pygame

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.ss = pygame.image.load("tile_0115.png")
        self.image.blit(self.ss, (0,0), (0,0,16,16))
        self.rect = self.image.get_rect(center=(x,y))
        
        self.x = x
        self.y = y