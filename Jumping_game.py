import pygame as pg
from sys import exit

import random
from random import randint, choice



class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pg.image.load('character/Running/run_01.png').convert_alpha()
        player_walk2 = pg.image.load('character/Running/run_02.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pg.image.load('character/Jump Start/jump_01.png').convert_alpha()
        

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,525))
        self.gravity=0
    def player_input(self):
        keys =pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >=525:
            self.gravity = -21
    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >=525:
            self.rect.bottom = 525
    
    
    def animation_state(self):
        if self.rect.bottom <525:
            self.image = self.player_jump
        else:
            self.player_index +=0.1
            if self.player_index >=len(self.player_walk):self.player_index=0
            self.image = self.player_walk[int(self.player_index)]
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pg.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            enemy_fly_frame1 = pg.image.load('enemy/PNG/jinn_animation/Flight1.png').convert_alpha()
            enemy_fly_frame2 = pg.image.load('enemy/PNG/jinn_animation/Flight2.png').convert_alpha()
            enemy_fly_frame3 = pg.image.load('enemy/PNG/jinn_animation/Flight3.png').convert_alpha()
            self.frames = [enemy_fly_frame1,enemy_fly_frame2,enemy_fly_frame3]
            y_pos =410
        else:
            enemy_frame1 = pg.image.load('enemy\PNG\lizard\walk_01.png').convert_alpha()
            enemy_frame2 = pg.image.load('enemy\PNG\lizard\walk_02.png').convert_alpha()
            enemy_frame3= pg.image.load('enemy\PNG\lizard\walk_03.png').convert_alpha()    
            self.frames = [enemy_frame1,enemy_frame2,enemy_frame3]
            y_pos =525

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900,1100),y_pos))
        
    def animation_state(self):
        self.animation_index +=0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 7
        self.destroy()
    
    def destroy(self):
        if self.rect.x <=-10:
            self.kill()



def display_score():
    current_time = int(pg.time.get_ticks()/1000)-start_time
    score_surf = test_font.render(f'Score: {current_time}',False,"White")
    score_rect= score_surf.get_rect (center= (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -=5

            if obstacle_rect.bottom == 525: screen.blit(enemy_surf,obstacle_rect)
            else:screen.blit.flip(enemy_fly_surf,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x >-100]
        return obstacle_list
    else:return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprites():
    if pg.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True


pg.init()
screen = pg.display.set_mode((800,600))

pg.display.set_caption("The jumper")

clock = pg.time.Clock()

game_active= False
test_font = pg.font.Font('font\BeardsonsNormal-rgmY8.ttf',40)

background_surface = pg.image.load('medieval\PNG\Background\Background_01.png').convert_alpha()

background2_surface = pg.image.load('medieval\PNG\Background\Background_02.png').convert_alpha()

ground_surface= pg.image.load('medieval/PNG/Background/background_03.png').convert_alpha()


#scoreboard stuff

start_time=0
score=0


#groups
player = pg.sprite.GroupSingle()
player.add(Player())

obstacle_group = pg.sprite.Group()


# #enemy stuff
# enemy_frame1 = pg.image.load('enemy\PNG\lizard\walk_01.png').convert_alpha()
# enemy_frame2 = pg.image.load('enemy\PNG\lizard\walk_02.png').convert_alpha()
# enemy_frame3= pg.image.load('enemy\PNG\lizard\walk_03.png').convert_alpha()
# enemy_frames = [enemy_frame1,enemy_frame2,enemy_frame3]
# enemy_frame_index=0
# enemy_surf = enemy_frames[enemy_frame_index]
# #enemy 2

# enemy_fly_frame1 = pg.image.load('enemy/PNG/jinn_animation/Flight1.png').convert_alpha()
# enemy_fly_frame2 = pg.image.load('enemy/PNG/jinn_animation/Flight2.png').convert_alpha()
# enemy_fly_frame3 = pg.image.load('enemy/PNG/jinn_animation/Flight3.png').convert_alpha()
# enemy_fly_frames =[enemy_fly_frame1,enemy_fly_frame2,enemy_fly_frame3]
# enemy_fly_index = 0 
# enemy_fly_surf =enemy_fly_frames[enemy_fly_index]
# #obstacle

# obstacle_rect_list=[]


# #player stuff
# player_walk1 = pg.image.load('character/Running/run_01.png').convert_alpha()
# player_walk2 = pg.image.load('character/Running/run_02.png').convert_alpha()
# player_walk = [player_walk1,player_walk2]
# player_index = 0
# player_jump = pg.image.load('character/Jump Start/jump_01.png').convert_alpha()

# player_surf = player_walk[player_index]
# player_rect = player_surf.get_rect(midbottom=(40,40))
# player_gravity = 0 

#player in start screen
player_stand = pg.image.load("character/Idle Blinking/0_Reaper_Man_Idle Blinking_015.png").convert_alpha()
player_stand = pg.transform.scale(player_stand,(384,384))
player_stand_rect = player_stand.get_rect(center=(400,300))


game_name = test_font.render('Dead Jumping',False,(111,196,200))
game_name_rect = game_name.get_rect(center=(400,80))

game_message = test_font.render('Press space to run',False,(111,196,200))
game_message_rect = game_message.get_rect(center=(400,500))

#timer
obstacle_timer = pg.USEREVENT +1
pg.time.set_timer(obstacle_timer,1500)

#ground enemy timer
enemy_animation_timer = pg.USEREVENT +2
pg.time.set_timer(enemy_animation_timer,500)

#fly enemy timer
enemy_animation_fly_timer = pg.USEREVENT +3
pg.time.set_timer(enemy_animation_fly_timer,150)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','enemy','enemy','enemy'])))
        
        else:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                game_active = True
                start_time = int(pg.time.get_ticks() / 1000)
                
                
    if game_active:
        screen.blit(background_surface,(0,0))
        screen.blit(background2_surface,(0,-100))
        screen.blit(ground_surface,(0,500))
        score = display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprites()
		
    else:
        screen.fill((66,66,66))
        screen.blit(player_stand,player_stand_rect)

        score_message = test_font.render(f'Your score: {score}',False,('White'))
        score_message_rect = score_message.get_rect(center = (400,500))
        screen.blit(game_name,game_name_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)

    pg.display.update()
    clock.tick(60)