import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('My First Game')
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf',50)

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render('My game', False, 'Black')

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rec = player_surface.get_rect(midbottom = (40, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if player_rec.collidepoint(pygame.mouse.get_pos()):
        #         exit()
            
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface,(350,50))
    screen.blit(snail_surface,snail_rect)
    snail_rect.left -= 4
    if snail_rect.right == 0: snail_rect.left = 800
    screen.blit(player_surface,player_rec)
    
    # if player_rec.colliderect(snail_rect): pygame.stop
    
    # mouse_position = pygame.mouse.get_pos()
    # if player_rec.collidepoint(mouse_position):
    #     print(pygame.mouse.get_pressed())
    
    pygame.display.update()
    clock.tick(60)