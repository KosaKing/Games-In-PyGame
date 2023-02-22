import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('My First Game')
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf',50)

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

score_surface = test_font.render('My game', False, 'Black')
score_rect = score_surface.get_rect(midbottom = (400, 100))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rec = player_surface.get_rect(midbottom = (40, 300))
player_gravity = 0 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rec.collidepoint(pygame.mouse.get_pos()):
                player_gravity = -20

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_gravity = -20

            
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    pygame.draw.rect(screen, (100,20,190), score_rect)
    screen.blit(score_surface,score_rect)


    screen.blit(snail_surface,snail_rect)
    snail_rect.left -= 4
    if snail_rect.right == 0: snail_rect.left = 800

    #player
    player_gravity += 1
    screen.blit(player_surface,player_rec)
    player_rec.y += player_gravity

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print('spacja')

    # if player_rec.colliderect(snail_rect): pygame.stop
    
    # mouse_position = pygame.mouse.get_pos()
    # if player_rec.collidepoint(mouse_position):
    #     print(pygame.mouse.get_pressed())
    
    pygame.display.update()
    clock.tick(60)