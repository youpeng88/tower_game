# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:39:30 2016

@author: pengyou
"""

'''
Thoughts for additional changes:
    1. Starting variables can be improved, maybe make it a dictionary instead of a list
'''

import pygame
import os
import random
import math

### Global Variables

# RGB color definition 
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

# map size
MAP_SIZE = (600, 600)  # (width in pixels, height in pixels)

# margins (same for all sides)
MARGIN = 10

# screen size
SCREEN_SIZE = (1000, MAP_SIZE[1]+2*MARGIN)  # (width in pixels, height in pixels)

# bar_size
BAR_SIZE = (SCREEN_SIZE[0]-3*MARGIN-MAP_SIZE[0],MAP_SIZE[1])

# default dimensions
DIMENSIONS = (20,20)

def map_border():
    xr = range(MARGIN+1,MAP_SIZE[0]+MARGIN)
    yr = range(MARGIN+1,MAP_SIZE[1]+MARGIN)
    n1 = len(xr)
    n2 = len(yr)
    x0 = [MARGIN+1] * n1
    y0 = [MARGIN+1] * n2
    xn = [MARGIN+MAP_SIZE[0]] * n1
    yn = [MARGIN+MAP_SIZE[1]] * n2
   
    b1 = zip(x0,yr)
    b2 = zip(xn,yr)
    b3 = zip(xr,y0)
    b4 = zip(xr,yn)
    
    border = b1 + b2 + b3 + b4
    return border

def calc_distance (obj1, obj2):
    distance = math.sqrt((obj2[0]-obj1[0])**2 + (obj2[1]-obj1[1])**2)
    return distance

def update_text(screen, message, location):
    """
    Used to display the text on the right-hand part of the screen.
    location will be used to decide what variable to display: tower number, money, wave
    """
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 0 + textSize
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.centerx = 2*MARGIN + MAP_SIZE[0] + BAR_SIZE[0]/2
    textRect.centery = MARGIN+100+textY*location*2
    screen.blit(text, textRect)

def sidebar(screen, tower_number, money, wavecount):
    update_text(screen, "Tower #: " + str(tower_number), 1)
    update_text(screen, "Money: " + str(money), 2)
    update_text(screen, "Wave #: " + str(wavecount), 3)
        
        
def new_game():
    """
    Sets up all necessary components to start a new game
    of power tower.
    """
    pygame.init() # initialize all imported pygame modules
    
    # setup background
    BackGround = Background('brick_wall.bmp', [MARGIN,MARGIN])

    screen = pygame.display.set_mode(SCREEN_SIZE)

    pygame.display.set_caption("Tower Power") # caption sets title of Window 
    
    screen.fill(black) # (0,0,0) represents RGB for black
    screen.blit(BackGround.image, BackGround.rect)

    pygame.display.flip()

    # starting variables, modified by the setting chosen in the opening menu
    HP_enemy = 100
    HP_tower = 500
    HP_base = 1000
    speed_level = 1
    tower_number = 1
    wavecount = 0
    money = 5000
    defense_range = 20

    starting_varaibles = [HP_enemy, HP_tower, speed_level, tower_number, wavecount, money, defense_range]

    board = Board(HP_base)

    clock = pygame.time.Clock()

    main_loop(screen, board, starting_varaibles, clock)

def main_loop(screen, board, starting_varaibles, clock):
    HP_enemy = starting_varaibles[0]
    HP_tower = starting_varaibles[1]
    speed_level = starting_varaibles[2]
    tower_number = starting_varaibles[3]
    wavecount = starting_varaibles[4]
    money = starting_varaibles[5]
    defense_range = starting_varaibles[6]

    board.towers.draw(screen) # draw tower Sprite
    pygame.display.flip()
    
    border = map_border()
    events = pygame.event.get()
    event_types = [event.type for event in events]
    while pygame.QUIT not in event_types: # when use didn't click exit on the window
         milliseconds = clock.tick_busy_loop()  # milliseconds passed since last frame
         seconds = milliseconds/1000.0

         # call sidebar
         sidebar(screen, tower_number, money, wavecount)
         pygame.display.flip()
         
         # bring waves of enemies
         frequency = 100 # in milliseconds
         num_enemies = 1 # number of enemies generated per wave
         pygame.time.set_timer(pygame.USEREVENT + 1, frequency)

         # action 1: add tower
         if pygame.mouse.get_pressed()[0]:
             x,y = pygame.mouse.get_pos()
             # add a defense tower at the location clicked
             if board.add_tower_to_board((x,y), HP_tower, defense_range):
                 board.towers.draw(screen)
                 pygame.display.flip()
                 money -= 500
                 tower_number +=1

         # action 2: add enemies per wave frequecy
         if pygame.USEREVENT + 1 in event_types:
             # add enemies to board
             enemies_count = 0
             num_border_locs = len(border)
             while enemies_count < num_enemies:
                 index = random.randint(1,num_border_locs)
                 x,y = border[index]
                 if board.add_enemy_to_board((x,y),speed_level, HP_enemy):
                     enemies_count +=1
             wavecount +=1
             # action 3: defense attacks enemy (shoot)
    
             # action 4: enemy attack defense and base tower
    
             # action 5: enemies move
             board.enemies.update(seconds)
             board.enemies.draw(screen)
             pygame.display.flip()
    
         events = pygame.event.get()
         event_types = [event.type for event in events] # update event list
         pass

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(MAP_SIZE[0], MAP_SIZE[1]))
        self.rect.left, self.rect.top = location

class Board:
    def __init__(self, HP_base):

        # Initialize the base Tower
        init_x = MARGIN+MAP_SIZE[0]/2
        init_y = MARGIN+MAP_SIZE[1]/2
        self.base_tower = Tower(self,(init_x, init_y),(20,40), HP_base)

        # Initialize the tower dic
        self.tower_dict = {}
        self.tower_dict[(init_x, init_y)] = self.base_tower

        # Adds Tower to the "towers" Sprite List
        self.towers = pygame.sprite.Group()
        self.towers.add(self.base_tower)

        # Create life bar dict and Sprite group
        self.lifebar_dic = {}
        self.lifebars = pygame.sprite.Group()

        # Create enemy dict and Sprite group
        self.enemy_dict = {}
        self.enemies = pygame.sprite.Group()

    def add_tower_to_board(self, position, HP_tower,defense_range):
        defense_tower = Defense_tower(self,position,DIMENSIONS,HP_tower,defense_range)
        collision_tower = pygame.sprite.spritecollideany(defense_tower, self.towers, None)
        collision_enemy = pygame.sprite.spritecollideany(defense_tower, self.enemies, None)
        if collision_tower == None and collision_enemy == None:
            self.tower_dict[(position[0], position[1])] = defense_tower
            self.towers.add(defense_tower)
            return True
        else:
            return False

    def add_enemy_to_board(self, position, speed_level, HP_enemy):
        enemy = Enemies(self, position, DIMENSIONS, speed_level, HP_enemy)
        collision_tower = pygame.sprite.spritecollideany(enemy, self.towers, None)
        collision_enemy = pygame.sprite.spritecollideany(enemy, self.enemies, None)
        if collision_tower == None and collision_enemy == None:
            self.enemy_dict[(position[0], position[1])] = enemy
            self.enemies.add(enemy)
            return True
        else:
            return False

    def draw_laser_line(self, screen, enemy_position, tower_position):
        pygame.draw.line(screen, red, tower_position, enemy_position)

class Bloodbar():
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        # 	greenpart = HP/width
        # redpart = 1 - HP / width
	  # fill rectangle
	  # position = gameobject.position+some_distance
    pass

class Game_obj(pygame.sprite.Sprite):
    def __init__(self, board, position, dimensions, HP):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.dimensions = dimensions
        self.rect = pygame.Surface([dimensions[0],dimensions[1]]).get_rect()
        self.rect.center = position
#        self.rect.x = position[0] - dimensions[0]/2
#        self.rect.y = position[1] - dimensions[1]/2
#        self.rect.topleft = (position[0] - dimensions[0]/2, position[1] - dimensions[1]/2)
#        self.rect.bottomleft = (position[0] - dimensions[0]/2, position[1] + dimensions[1]/2)
#        self.rect.topright = (position[0] + dimensions[0]/2, position[1] - dimensions[1]/2)
#        self.rect.topleft = (position[0] + dimensions[0]/2, position[1] + dimensions[1]/2)
        self.board = board
        self.HP = HP

class Tower(Game_obj):
    def __init__(self, board, position, dimensions, HP):
        super(Tower,self).__init__(board, position, dimensions, HP)
        self.set_pic()

    def set_pic(self):
        self.image = pygame.image.load("base_tower.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.dimensions[0], self.dimensions[1]))

    def decrease_HP(self,decreased_HP):
        self.HP -= decreased_HP
        if self.HP < 0:
            self.kill_sprite()

    def kill_sprite(self):
        # need to remove the object from the board
        # from dic list
        self.board.tower[(self.position[0], self.position[1])] = None
        # from sprite group
        self.kill()

class Defense_tower(Tower):
    def __init__(self, board, position, dimensions, HP, defense_range):
        super(Defense_tower,self).__init__(board, position, dimensions, HP)
        self.set_pic()
        self.collison = False
        self.defense_range = defense_range

    def set_pic(self):
        self.image = pygame.image.load("defense_tower.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.dimensions[0], self.dimensions[1]))

    def closest_enemy(self, board):
        e_position = None
        closest_distance = self.defense_range
        for enemy in board.enemies:
            distance = calc_distance(self.position, enemy.position)
            if distance < closest_distance:
                closest_distance = distance
                e_position = enemy.position
        if e_position != None:
            return e_position

class Enemies(Game_obj):
    def __init__(self, board, position, dimensions, level, HP):
        super(Enemies,self).__init__(board, position, dimensions, HP)

        self.set_pic()
        self.speed_level = 1*level
        
        self.orientation = (0,1) #points up initially
        self.point_at_base(board)
        self.position = position


    def point_at_base(self, board): # moving direction
        direction = (board.base_tower.position[0] - self.position[0], board.base_tower.position[1] - self.position[1])
        distance = calc_distance(self.position, board.base_tower.position)
        new_orientation = (direction[0]/distance, direction[1]/distance)
        orientation_change = (new_orientation[0] - self.orientation[0], new_orientation[1]- self.orientation[1])
        #from orientation_change calculate the degree of rotation, then rotate the image accordingly
        angle = math.atan2(orientation_change[1], orientation_change[0])
        angle = math.degrees(angle)
        self.image = pygame.transform.rotate(self.image, angle)

        self.orientation = new_orientation
        self.dx = self.speed_level*(self.orientation[0])
        self.dy = self.speed_level*(self.orientation[1])

    def set_pic(self):
        self.image = pygame.image.load("enemy.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.dimensions[0], self.dimensions[1]))

    def set_new_speed(self,new_level):
        self.speed_level = 1*new_level

    def decrease_HP(self,decreased_HP):
        self.HP -= decreased_HP
        if self.HP < 0:
            self.kill()

    def kill(self):
        # need to remove the object from the board
        # from dic list
        self.board.enemy_group[(self.rect.x,self.rect.y)] = None
        # from sprite group
        # self.enemies
        # NOT FINISHED
        pass

    def touching_defense_or_base_tower(self):
        pass

    def update(self,seconds):
        # add in angles from find direction to base tower
        self.rect.x += self.dx * seconds
        self.rect.y += self.dy * seconds
        pass

new_game()