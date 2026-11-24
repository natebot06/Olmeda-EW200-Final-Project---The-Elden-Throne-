import pygame
from backgroundlevel1 import Level1
import gif_pygame
from boss import Boss
from player import Player
from heart import Heart 
import random 
pygame.init()

clock = pygame.time.Clock()

# hard code variables
TS = 16
SCALE = 2
WIDTH = (TS*35)*SCALE
HEIGHT = (TS*20)*SCALE
SIZE = (WIDTH, HEIGHT)

#make screen 
screen = pygame.display.set_mode(SIZE)

#get bg
bg = pygame.Surface(screen.get_rect().size)
pygame.transform.scale_by(bg, SCALE)
#instance of level1
level1 = Level1(TS, SIZE)

#animation_gif = gif_pygame.load("Rotating_earth_(large).gif")
youdiedgif = gif_pygame.load("youdiedgif.gif")

#initialize music 
pygame.mixer.init()
intromusic = pygame.mixer.Sound("Title Theme.mp3")
battle = pygame.mixer.Sound("Battle.mp3")
death = pygame.mixer.Sound("death.mp3")
happy = pygame.mixer.Sound("win.mp3")
#### TITLE SCREEN
intromusic.play()
running = 1
while running:
    screen.blit(bg, (0,0))
    #screen.blit(animation_gif.blit_ready(), (0,0))
    title = pygame.image.load('title.png')
    title = pygame.transform.rotozoom(title, 0, 1.08)
    screen.blit(title, (0,0))
    pygame.display.flip()
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = 0
        #go to game and stop intro music if press spacebar 
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                intromusic.stop()
                running = 0
                
                
#create all sprite groups and instances of player and boss, passing in all groups so they can interact with eachother 
hammer_group = pygame.sprite.Group()
spear_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()
player = Player(560, 480, spear_group, level1.collision_rects)               
boss = Boss(560, 240, hammer_group, spear_group, player, level1.collision_rects)
boss_group = pygame.sprite.GroupSingle(boss)

#make a new event to spawn a heart every 15 seconds
spawnheart = pygame.USEREVENT + 1
pygame.time.set_timer(spawnheart, 15000)

#####MAIN GAME LOOP
battle.play(loops = -1)
battle.set_volume(.5)
running = 1
while running:
    clock.tick(60)
    screen.blit(bg, (0, 0))
    #move the player and boss and projectiles 
    player.update()
    boss_group.update()
    spear_group.update()
    hammer_group.update()
    #when the player rect collides with the heart rect, add player health and make sure player health does not go over 100
    heart_pickup = pygame.sprite.spritecollide(player, heart_group, 1)
    for heart in heart_pickup:
        player.health += 20
        if player.health > player.maxhealth:
            player.health = player.maxhealth 
    #When a spear hits the boss the spear is killed and the boss takes 25 damage, and if the boss health is 0, end the game 
    spear_hits = pygame.sprite.spritecollide(boss, spear_group, 1)
    for spear in spear_hits:
        boss.health -= 25
        if boss.health <= 0:
            running = 0 
    #kill any spears that touch the list of tiles that are solid     
    for spear in spear_group:
        if spear.rect.collidelist(level1.collision_rects) != -1:
            spear.kill()
    
    #When a hammer hits the player, kill the hammer and the player takes 15 damage, if the player health is 0 quit the game     
    hammer_hits = pygame.sprite.spritecollide(player, hammer_group, 1)
    for hammer in hammer_hits:
        player.health -= 25
        if player.health <=0:
            running = 0 
    #kill any hammers that touch the list of tiles that are solid   
    for hammer in hammer_group:
        if hammer.rect.collidelist(level1.collision_rects) != -1:
            hammer.kill()
   
    #draw from bottom to top layer so nothing covers each other 
    heart_group.draw(screen)
    level1.draw(screen)
    boss_group.draw(screen)
    screen.blit(player.image, player.rect)
    heart_group.draw(screen)
    spear_group.draw(screen)
    hammer_group.draw(screen)
    
    #draw healthbars last so you always see them 
    player.drawbars(screen)
    boss.draw_bars(screen)
    
    pygame.display.flip()
    
    if player.health <= 0:
            battle.stop
            clock.tick(60)
            screen.fill((0,0,0))
            
            gif = pygame.transform.scale(youdiedgif.blit_ready(), SIZE)
            screen.blit(gif, (0,0))
    
    
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            battle.stop()
            running = 0
        #throw a spear towards the mouse on left click 
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player.throw_spear((mouse_x, mouse_y))
        #when the spawnheart event happens, add a heart to heart group at a random location 
        if e.type == spawnheart:
            rand_x = random.randint(200, 800)
            rand_y = random.randint(100,540)
            new_heart = Heart(rand_x, rand_y)
            heart_group.add(new_heart)
                
#if you defeat the boss you win and a victory screen comes up, you took the throne       
if boss.health <= 0:
    battle.stop()
    happy.play()
    game_over = 1
    while game_over:
        clock.tick(60)
        win = pygame.image.load('throne.jpg')
        winn= pygame.transform.scale(win, SIZE)
        screen.blit(winn, (0,0))
        font = pygame.font.Font("C:/Users/m294902/Documents/EW200/FINAL PROJECT 'The Fire Throne'/old-gangstriad-font/OldGangstriad-V48xy.otf", 28)
        surface = font.render("The generations of new tell a story of how a lone midshipman took the Elden Throne", 1,(200,0,0) )
        center = surface.get_rect(center = (WIDTH/2, 400))
        screen.blit(surface, (center))
        
        pygame.display.flip()
        
        for e in pygame.event.get():
              if e.type == pygame.QUIT:
                  game_over = 0
#if you die a death screen comes up, you lost                 
if player.health <= 0:
    battle.stop()
    death.play()
    game_over = 1
    while game_over:
        clock.tick(60)
        screen.fill((0,0,0))
        gif = pygame.transform.scale(youdiedgif.blit_ready(), SIZE)
        screen.blit(gif, (0,0))
    
        pygame.display.flip()
        
        for e in pygame.event.get():
              if e.type == pygame.QUIT:
                  game_over = 0 
pygame.quit()