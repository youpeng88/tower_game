# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:39:30 2016

@author: pengyou
"""

'''
Thoughts for additional changes:
    1. Starting variables can be improved, maybe make it a dictionary instead of a list
    2. merge related varaible in to one value corresponding to the variable key
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
SCREEN_SIZE = (MAP_SIZE[1]+2*MARGIN,680)  # (width in pixels, height in pixels)

# bar_size
BAR_SIZE = (MAP_SIZE[0],SCREEN_SIZE[1]-3*MARGIN-MAP_SIZE[0],)

# default dimensions
DIMENSIONS = (20,20)

#PC Dictionary relating object type to the image files it uses and its dimensions
IMAGE_DICT = {}
IMAGE_DICT["base_tower"] = ("base_tower.png", (20, 40))
IMAGE_DICT["defense_tower"] = ("defense_tower.png", (20, 20))
IMAGE_DICT["enemy"] = ("enemy.png", (20, 20))
IMAGE_DICT["background"] = ("brick_wall.png", MAP_SIZE)
#
# # MAC Dictionary relating object type to the image files it uses and its dimensions
# IMAGE_DICT = {}
# IMAGE_DICT["base_tower"] = ("base_tower.bmp", (20, 40))
# IMAGE_DICT["defense_tower"] = ("defense_tower.bmp", (20, 20))
# IMAGE_DICT["enemy"] = ("enemy.bmp", (20, 20))
# IMAGE_DICT["background"] = ("brick_wall.bmp", MAP_SIZE)
#IMAGE_DICT["gold_icon"] = 


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
    textx = 0 + textSize
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.centery = 2*MARGIN + MAP_SIZE[1] + BAR_SIZE[1]/2
    textRect.centerx = MARGIN+50+textx*(location-1)*8
    screen.blit(text, textRect)

def sidebar(screen, tower_number, money, wavecount):
    screen.fill(black)
    update_text(screen, "Tower #: " + str(tower_number), 1)
    update_text(screen, "Money: " + str(money), 2)
    update_text(screen, "Wave #: " + str(wavecount), 3)
     
        
def new_game():
    """
    Sets up all necessary components to start a new game
    of power tower.
    """
    pygame.init() # initialize all imported pygame modules
    
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tower Power") # caption sets title of Window
    screen.fill(black) # (0,0,0) represents RGB for black

    # starting variables, modified by the setting chosen in the opening menu
    HP_enemy = 100
    HP_tower = 500
    HP_base = 1000
    speed_level = 1
    tower_number = 1
    wavecount = 0
    money = 5000
    defense_range = 50
    attack_power_tower = 2
    attack_power_enemy = 5
    tower_cost = 500
    
    defense_range_base = 15
    attack_power_base = 5

    starting_varaibles = [HP_enemy, HP_tower, speed_level, tower_number, wavecount, money, defense_range, tower_cost, attack_power_tower, attack_power_enemy]

    board = Board(HP_base,screen,defense_range_base, attack_power_base)

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
    tower_cost = starting_varaibles[7]
    attack_power_tower = starting_varaibles[8]
    attack_power_enemy = starting_varaibles[9]

    time_created = 0

    # setup background
    BackGround = Background("background", [MARGIN, MARGIN])
    screen.blit(BackGround.image, BackGround.rect)
    pygame.display.flip()
    

    board.towers.draw(screen) # draw tower Sprite
    pygame.display.flip()
    
    border = map_border()
    events = pygame.event.get()
    event_types = [event.type for event in events]
    while pygame.QUIT not in event_types: # when use didn't click exit on the window

         board.add_enemy_to_board((30,30),speed_level, HP_enemy, attack_power_enemy)
         pygame.display.flip()

         # action 1: add tower
         if pygame.mouse.get_pressed()[0]:
             if money >= tower_cost:
                 x,y = pygame.mouse.get_pos()
             # add a defense tower at the location clicked
                 if board.add_tower_to_board((x,y), HP_tower, defense_range, attack_power_tower):
                     board.towers.draw(screen)
                     pygame.display.flip()
                     money -= tower_cost
                     tower_number +=1

         #Updated Action 2 and 5 (move)
         num_border_locs = len(border)
         num_enemies = 2
         time_period = 3000
         elapsed_time = pygame.time.get_ticks() - time_created
         #print elapsed_time
         if elapsed_time > time_period:
             enemies_count = 0
             while enemies_count < num_enemies: 
                 index = random.randint(0,num_border_locs-1)
                 x,y = border[index]
                 board.add_enemy_to_board((x,y),speed_level, HP_enemy, attack_power_enemy)
                 enemies_count +=1
             time_created = pygame.time.get_ticks()
             wavecount +=1
        ###Test
         #
         # # action 2: add enemies per wave frequecy
         # if pygame.USEREVENT + 1 in event_types:
         #     # add enemies to board
         #     enemies_count = 0
         #     num_border_locs = len(border)
         #     while enemies_count <= num_enemies:
         #         index = random.randint(0,num_border_locs-1)
         #         x,y = border[index]
         #         if board.add_enemy_to_board((x,y),speed_level, HP_enemy, attack_power):
         #             enemies_count +=1
         #     wavecount +=1
         #     # action 3: defense attacks enemy (shoot)
         #     # increase money when enemy died
         #
         #     # action 4: enemy attack defense and base tower
         #            
             
         # action 3: defense attacks enemy (shoot)
         for tower in board.towers:
             tower.attack()
#             if tower.attack()!= None:
#                 money += tower.attack()
                                 
         # action 4: enemy attack defense and base tower
         for enemy in board.enemies:
             collision = enemy.touching_defense_or_base_tower(board)
             if collision is not None:
                 enemy.attack(collision, board)
             else:
                 enemy.point_at_base(board)
                 enemy.update()

         # action 5: enemies move    
         # test movement: board.add_enemy_to_board((11,11),speed_level, HP_enemy)
         board.enemies.update()

        # call sidebar
         sidebar(screen, tower_number, money, wavecount)
#        screen.fill(black) # (0,0,0) represents RGB for black
         screen.blit(BackGround.image, BackGround.rect)
         board.towers.draw(screen)

         board.enemies.draw(screen)
         # update life bar
         board.lifebars.update()
         # board.lifebars.draw(screen)
         pygame.display.flip()
         clock.tick(100)
    
         events = pygame.event.get()
         event_types = [event.type for event in events] # update event list

class Background(pygame.sprite.Sprite):
    def __init__(self, obj_type, position):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(IMAGE_DICT[obj_type][0])
        self.image = pygame.transform.scale(self.image, IMAGE_DICT[obj_type][1])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

class Board:
    def __init__(self, HP_base,screen,defense_range, attack_power):

        self.screen = screen
        
        # Initialize the base Tower
        init_x = MARGIN+MAP_SIZE[0]/2
        init_y = MARGIN+MAP_SIZE[1]/2

        self.base_tower = Tower(self, (init_x, init_y), "base_tower", HP_base, defense_range, attack_power)
        self.base_tower_lifebar = Lifebar(self,self.base_tower,screen, HP_base)

        # Initialize the tower dic
        self.tower_dict = {}
        self.tower_dict[(init_x, init_y)] = self.base_tower

        # Create life bar dict and Sprite group
        self.lifebar_dict = {}
        self.lifebars = pygame.sprite.Group()

        # Add base tower lifebar to lifebar dict and Sprite group
        self.lifebar_dict[(init_x, init_y)] = self.base_tower_lifebar
        self.lifebars.add(self.base_tower_lifebar)
        
        # Adds Tower to the "towers" Sprite List
        self.towers = pygame.sprite.Group()
        self.towers.add(self.base_tower)

        # Create enemy dict and Sprite group
        self.enemy_dict = {}
        self.enemies = pygame.sprite.Group()

    def add_tower_to_board(self, position, HP_tower,defense_range, attack_power):
        defense_tower = Defense_tower(self, position, "defense_tower", HP_tower, defense_range, attack_power)
        if defense_tower.rect.x < MARGIN or defense_tower.rect.topright[0] > MARGIN + MAP_SIZE[0] or defense_tower.rect.y < MARGIN or defense_tower.rect.bottomleft[1] > MARGIN + MAP_SIZE[1]:
            return False
        else:
            collision_tower = pygame.sprite.spritecollideany(defense_tower, self.towers, None)
            collision_enemy = pygame.sprite.spritecollideany(defense_tower, self.enemies, None)
            if collision_tower == None and collision_enemy == None:
                self.tower_dict[(position[0], position[1])] = defense_tower
                self.towers.add(defense_tower)
                defense_tower_lifebar = Lifebar(self, defense_tower, self.screen, HP_tower)

            # Add defense tower lifebar to lifebar dict and Sprite group
                self.lifebar_dict[(position[0], position[1])] = defense_tower_lifebar
                self.lifebars.add(defense_tower_lifebar)
                return True

    def add_enemy_to_board(self, position, speed_level, HP_enemy, attack_power):
        enemy = Enemies(self, position, "enemy", HP_enemy, speed_level, attack_power)
        collision_tower = pygame.sprite.spritecollideany(enemy, self.towers, None)
        collision_enemy = pygame.sprite.spritecollideany(enemy, self.enemies, None)
        if collision_tower is None and collision_enemy is None:
            self.enemy_dict[(position[0], position[1])] = enemy
            self.enemies.add(enemy)
            enemy_lifebar = Lifebar(self, enemy, self.screen, HP_enemy)

            # Add defense tower lifebar to lifebar dict and Sprite group
            self.lifebar_dict[(position[0], position[1])] = enemy_lifebar
            self.lifebars.add(enemy_lifebar)

    def draw_laser_line(self, screen, enemy_position, tower_position):
        pygame.draw.line(screen, black, tower_position, enemy_position, 3)

class Game_obj(pygame.sprite.Sprite):
    def __init__(self, board, position, obj_type, init_HP, attack_power):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.position = position
        self.dimensions = IMAGE_DICT[obj_type][1]
        self.HP = init_HP
        self.image = pygame.image.load(IMAGE_DICT[obj_type][0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, IMAGE_DICT[obj_type][1])
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.attack_power = attack_power
        #
        # self.rect.topleft = (position[0] - self.dimensions[0]/2, position[1] - self.dimensions[1]/2)
        # self.rect.bottomleft = (position[0] - self.dimensions[0]/2, position[1] + self.dimensions[1]/2)
        # self.rect.topright = (position[0] + self.dimensions[0]/2, position[1] - self.dimensions[1]/2)
        # self.rect.topleft = (position[0] + self.dimensions[0]/2, position[1] + self.dimensions[1]/2)

class Lifebar(pygame.sprite.Sprite):
    def __init__(self, board, boss, screen, full_HP):
        pygame.sprite.Sprite.__init__(self)
        self.boss = boss
        self.screen = screen
        self.position = (self.boss.position[0] - self.boss.dimensions[0]/2, self.boss.position[1] + self.boss.dimensions[1]/2) # lifebar is positioned directly below its boss (game object)
        self.dimensions = (self.boss.dimensions[0],10) #lifebar is same width as its boss and 10 pixels high
        self.HP = self.boss.HP
        #super(Lifebar,self).__init__(board, self.position, self.dimensions, self.HP)
        self.board = board
        self.set_pic()
        pygame.draw.rect(self.screen, (0,255,0), (self.position,self.dimensions))
        self.oldHP = 0
        self.full_HP = full_HP

    def set_pic(self):
        self.image = pygame.Surface(self.dimensions)
        self.image.set_colorkey((0,0,0)) # black transparent
#        self.rect = self.image.get_rect()
#        self.rect.topleft = self.position       
   
    def update(self):
            self.position = (self.boss.rect.center[0] - self.boss.dimensions[0]/2, self.boss.rect.center[1] + self.boss.dimensions[1]/2)
            
            self.frac = float(self.boss.HP) / float(self.full_HP)
            pygame.draw.rect(self.screen, (0,0,0), (self.position,self.dimensions)) # fill black
            pygame.draw.rect(self.screen, (0,255,0), (self.position,(int(self.boss.dimensions[0] * self.frac),10)),0) # fill green
            self.oldHP = self.boss.HP

class Tower(Game_obj):
    def __init__(self, board, position, obj_type, init_HP,defense_range, attack_power):
        super(Tower, self).__init__(board, position, obj_type, init_HP, attack_power)
        self.defense_range = defense_range
    
    def attack(self):
        money = None
        attack_enemy = self.closest_enemy()
        if attack_enemy != None:
            enemy_position =  attack_enemy.position                  
            self.board.draw_laser_line(self.board.screen, enemy_position, self.position)
            attack_enemy.HP -= self.attack_power                 
            if attack_enemy.HP < 0:
                attack_enemy.enemy_death()
                money = 50
                return money

    def tower_death(self, board):
        # need to remove the object from the board
        # from dic list
        board.tower_dict[(self.position[0], self.position[1])] = None
        self.position = (0,0)
        # lifebar.kill()
        # from sprite group
        self.kill()
        
    def closest_enemy(self):
        e_position = None
        final_enemy = None
        closest_distance = self.defense_range
        for enemy in self.board.enemies:
            distance = calc_distance(self.position, enemy.position)
            if distance < closest_distance:
                closest_distance = distance
                e_position = enemy.position
                final_enemy = enemy
        if e_position != None:
            return final_enemy


class Defense_tower(Tower):
    def __init__(self, board, position, obj_type, init_HP, defense_range, attack_power):
        super(Defense_tower,self).__init__(board, position, obj_type, init_HP, defense_range, attack_power)


class Enemies(Game_obj):
    def __init__(self, board, position, obj_type, init_HP, level, attack_power):
        super(Enemies,self).__init__(board, position, obj_type, init_HP, attack_power)
        self.position = position
        self.orientation = (0, 1) #points up initially
        self.speed_level = 1*level
        self.dx = 0
        self.dy = 0
        self.point_at_base(board)

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

    def set_new_speed(self,new_level):
        self.speed_level = 1*new_level

    def attack(self, collision, board):
        collision.HP -= self.attack_power
        if collision.HP < 0:
            collision.tower_death(board)

    def enemy_death(self):
        # need to remove the object from the board
        # from dic list
        self.board.enemy_dict[(self.position[0], self.position[1])] = None
        # from sprite group
        self.kill()
        
    def touching_defense_or_base_tower(self, board):
        collision = pygame.sprite.spritecollideany(self, board.towers, collided=None)
        if collision is not None:
            self.dx = 0
            self.dy = 0
        return collision

    def update(self):
        # add in angles from find direction to base tower
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.position = self.rect.center
new_game()
