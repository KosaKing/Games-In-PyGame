import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0 
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0 
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300: 
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self) -> None:
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type) -> None:
        super().__init__()
        
        if type == 'fly':
            fly_move_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_move_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_move_1, fly_move_2]
            y_position = 210
        else:
            snail_move_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_move_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_move_1, snail_move_2]
            y_position = 300 

        self.animation_index = 0    
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_position))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        # self.destroy()


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surface = test_font.render(f'{current_time}', False, 'Black')
    score_rect = score_surface.get_rect(midbottom = (400, 100))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else:
        return []

def obstacle_draw(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

def colision(player, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player.colliderect(obstacle_rect): 
                return 0
            else: 
                return 1 
    else: 
        return 1

def player_animation():
    global player_surf, player_index

    if player_rec.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('My First Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False#True 
start_time = 0
score = 0


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles_group = pygame.sprite.GroupSingle()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# score_surface = test_font.render('My game', False, 'Black')
# score_rect = score_surface.get_rect(midbottom = (400, 100))

# Enemies 
snail_move_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_move_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_moves = [snail_move_1, snail_move_2]
snail_moves_index = 0
snail_surface = snail_moves[snail_moves_index]

fly_move_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_move_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_moves = [fly_move_1, fly_move_2]
fly_moves_index = 0
fly_surface = fly_moves[fly_moves_index]

obstacle_rect_list = []

# Player 

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rec = player_surf.get_rect(midbottom = (40, 300))
player_gravity = 0 

# Intro screen 
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rec = player_stand.get_rect(center = (400, 200))

game_title = test_font.render('Deadly snail', False, 'Black')
game_title_rect = game_title.get_rect(midbottom = (player_stand_rec.midtop[0], player_stand_rec.midtop[1]-20))
instruction = test_font.render('Press space to run', False, 'Black')
instruction_rect = instruction.get_rect(midtop = (player_stand_rec.midbottom[0], player_stand_rec.midbottom[1]+20))

# Timer 
obstacle_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2 
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
                    game_active = 1
                    start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                obstacles_group.add(Obstacle('fly'))

                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 200)))
            
            if event.type == snail_animation_timer:
                if snail_moves_index == 0: snail_moves_index = 1
                else: snail_moves_index = 0
                snail_surface = snail_moves[snail_moves_index]

            if event.type == fly_animation_timer:
                if fly_moves_index == 0: fly_moves_index = 1
                else: fly_moves_index = 0
                fly_surface = fly_moves[fly_moves_index]

    if game_active:        
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # pygame.draw.rect(screen, (100,20,190), score_rect)
        # screen.blit(score_surface,score_rect)
        score = display_score()

        # screen.blit(snail_surface,snail_rect)
        # snail_rect.left -= 4
        # if snail_rect.right == 0: snail_rect.left = 800

        #player
        player_gravity += 1
        player_rec.y += player_gravity
        if player_rec.bottom >= 300: player_rec.bottom=300
        player_animation()
        screen.blit(player_surf, player_rec)
        
        player.draw(screen)
        player.update()

        obstacles_group.draw(screen)
        obstacles_group.update()
        
        # Enemies movement 
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        obstacle_draw(obstacle_rect_list)
        
        #collision 
        game_active = colision(player_rec, obstacle_rect_list)
            
    else: 
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rec)
        obstacle_rect_list.clear()
        player_rec.midbottom = (40, 300)
        player_gravity = 0
        
        score_message = test_font.render(f'Your score is {score}', False, "Black")
        score_message_rect = score_message.get_rect(midtop = (player_stand_rec.midbottom[0], player_stand_rec.midbottom[1]+20))
        
        screen.blit(game_title, game_title_rect)
        if score: screen.blit(score_message, score_message_rect)
        else: screen.blit(instruction, instruction_rect)
        

    pygame.display.update()
    clock.tick(60)