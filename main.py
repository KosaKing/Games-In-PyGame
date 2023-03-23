import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0 
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
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

def colision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False):
        obstacles_group.empty()
        return False
    return True

# Game start 
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('My First Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False #True 
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.05)
bg_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles_group = pygame.sprite.Group()

# Loading background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()


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

# game loop 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    game_active = 1
                    start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                obstacles_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))


    if game_active:        
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        
        score = display_score()
        
        player.draw(screen)
        player.update()

        obstacles_group.draw(screen)
        obstacles_group.update()
        
        #collision 
        game_active = colision_sprite()
       
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
