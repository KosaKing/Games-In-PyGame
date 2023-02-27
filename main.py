import pygame
from sys import exit

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surface = test_font.render(f'{current_time}', False, 'Black')
    score_rect = score_surface.get_rect(midbottom = (400, 100))
    screen.blit(score_surface, score_rect)
    return current_time
    

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('My First Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False#True 
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# score_surface = test_font.render('My game', False, 'Black')
# score_rect = score_surface.get_rect(midbottom = (400, 100))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rec = player_surface.get_rect(midbottom = (40, 300))
player_gravity = 0 

# Intro screen 
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rec = player_stand.get_rect(center = (400, 200))

game_title = test_font.render('Deadly snail', False, 'Black')
game_title_rect = game_title.get_rect(midbottom = (player_stand_rec.midtop[0], player_stand_rec.midtop[1]-20))
instruction = test_font.render('Press space to run', False, 'Black')
instruction_rect = instruction.get_rect(midtop = (player_stand_rec.midbottom[0], player_stand_rec.midbottom[1]+20))



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rec.collidepoint(pygame.mouse.get_pos()):
                    if player_rec.bottom == 300:
                        player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rec.bottom == 300:
                        player_gravity = -20
        else: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    snail_rect = snail_surface.get_rect(midbottom = (600, 300))
                    game_active = 1
                    start_time = pygame.time.get_ticks()


    if game_active:        
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # pygame.draw.rect(screen, (100,20,190), score_rect)
        # screen.blit(score_surface,score_rect)
        score = display_score()

        screen.blit(snail_surface,snail_rect)
        snail_rect.left -= 4
        if snail_rect.right == 0: snail_rect.left = 800

        #player
        player_gravity += 1
        player_rec.y += player_gravity
        if player_rec.bottom >= 300: player_rec.bottom=300
        screen.blit(player_surface,player_rec)
        
        #collision 
        if player_rec.colliderect(snail_rect): 
            game_active = False
            
    else: 
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rec)
        
        score_message = test_font.render(f'Your score is {score}', False, "Black")
        score_message_rect = score_message.get_rect(midtop = (player_stand_rec.midbottom[0], player_stand_rec.midbottom[1]+20))
        
        screen.blit(game_title, game_title_rect)
        if score: screen.blit(score_message, score_message_rect)
        else: screen.blit(instruction, instruction_rect)
        

    pygame.display.update()
    clock.tick(60)