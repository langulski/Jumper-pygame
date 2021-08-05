import pygame as pg
from sys import exit

from random import randint

pg.init()

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

            if obstacle_rect.bottom == 500: screen.blit(enemy_surface,obstacle_rect)
            else:screen.blit(enemy_fly_surface,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x >-100]
        return obstacle_list
    else:return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True



screen = pg.display.set_mode((800,600))

pg.display.set_caption("The jumper")

clock = pg.time.Clock()

game_active= False
test_font = pg.font.Font('font\BeardsonsNormal-rgmY8.ttf',50)

background_surface = pg.image.load('medieval\PNG\Background\Background_01.png').convert_alpha()

background2_surface = pg.image.load('medieval\PNG\Background\Background_02.png').convert_alpha()

ground_surface= pg.image.load('medieval/PNG/Background/background_03.png').convert_alpha()


#scoreboard stuff
# score_surf = test_font.render('my game',False,'white')
# score_rect= score_surf.get_rect(center=(400,50))
start_time=0
score=0

#enemy stuff
enemy_surface = pg.image.load('enemy\PNG\lizard\Idle1.png').convert_alpha()

#enemy 2

enemy_fly_surface = pg.image.load('enemy\PNG\jinn_animation\Flight1.png').convert_alpha()


#obstacle

obstacle_rect_list=[]


#player stuff
player_surf = pg.image.load('character/Idle Blinking/0_Reaper_Man_Idle Blinking_000.png').convert_alpha()
player_surf = pg.transform.scale(player_surf,(128,128))
player_rect = player_surf.get_rect(midbottom=(40,40))
player_gravity = 0 
player_stand = pg.image.load("character/Idle Blinking/0_Reaper_Man_Idle Blinking_015.png").convert_alpha()
player_stand = pg.transform.scale(player_stand,(384,384))
player_stand_rect = player_stand.get_rect(center=(400,300))


game_name = test_font.render('Jumping',False,(111,196,200))
game_name_rect = game_name.get_rect(center=(400,80))

game_message = test_font.render('Press space to run',False,(111,196,200))
game_message_rect = game_message.get_rect(center=(400,500))

#timer
obstacle_timer = pg.USEREVENT +1
pg.time.set_timer(obstacle_timer,1450)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if game_active:
            if event.type == pg.MOUSEBUTTONDOWN and player_rect.bottom >= 525:
                if player_rect.collidepoint(event.pos):
                    player_gravity =-22

            if event.type == pg.KEYDOWN and player_rect.bottom >= 525:
                if event.key == pg.K_SPACE:
                    player_gravity =-22
        else:    
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
               game_active=True
               
               start_time= int(pg.time.get_ticks()/1000)


        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(enemy_surface.get_rect(bottomright = (randint(900,1100),500))) 
            else:
                obstacle_rect_list.append(enemy_fly_surface.get_rect(bottomright = (randint(900,1100),330))) 
   # if event.type == pg.MOUSEMOTION:
#if player_rect.collidepoint(event.pos): print('collision')
        
    if game_active:
        screen.blit(background_surface,(0,0))
        screen.blit(background2_surface,(0,-100))
        # pg.draw.rect(screen, '#333300',score_rect)
        # pg.draw.rect(screen, '#333300',score_rect,10)
        # screen.blit(score_surf,score_rect)
        screen.blit(ground_surface,(0,500))
        score = display_score()
    

        # enemy_rect.x -=4
        # if enemy_rect.right <=0: enemy_rect.left = 800
        # screen.blit(enemy_surface,enemy_rect)
        
        #player
        player_gravity+=1
        player_rect.y += player_gravity
        if player_rect.bottom >=525: player_rect.bottom = 525
        screen.blit(player_surf,player_rect)

    
    #collisions
        game_active = collisions(player_rect,obstacle_rect_list)
    
    
     #Obstacle Movement

        obstacle_movement(obstacle_rect_list)
    
    # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    else:
        screen.fill((66,66,66))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom=(80,525)
        player_gravity=0

        score_message = test_font.render(f'Your Score: {score}',False,(111,196,200))
        score_message_rect = score_message.get_rect(center=(400,500))
        screen.blit(game_name,game_name_rect)
        
        
        if score==0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
    pg.display.update()


    clock.tick(60)




