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

import os
import pygame
import random
import math
import inputask
from example_menu import main as menu
from difficulty_menu import main as level_menu
from platform_menu import main as pl_menu

# from dashedline import draw_dashed_line as draw_dash
# from dashedline2 import draw_dashed_line as draw_dash2

### Global Variables

# RGB color definition 
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

# map size
MAP_SIZE = (700, 600)  # (width in pixels, height in pixels)

# margins (same for all sides)
MARGIN = 10

# screen size
SCREEN_SIZE = (MAP_SIZE[0]+2*MARGIN,680)  # (width in pixels, height in pixels)

# bar_size
BAR_SIZE = (MAP_SIZE[0],SCREEN_SIZE[1]-3*MARGIN-MAP_SIZE[1])

# default dimensions
DIMENSIONS = (20,20)

# define start screen
pygame.init()

def image_dictionary(extension):
    if extension[0] == ".png":
    #PC Dictionary relating object type to the image files it uses and its dimensions
        IMAGE_DICT = {}
        IMAGE_DICT["base_tower"] = ("transparent_base_tower.png", (20, 40))
        IMAGE_DICT["defense_tower"] = ("transparent_defense_tower.png", (20, 20))
        IMAGE_DICT["enemy"] = ("transparent_enemy.png", (20, 20))
        IMAGE_DICT["background"] = ("grass_background.png", MAP_SIZE)
        IMAGE_DICT["gold_icon"] = ("gold_coins.png", (15,15))
        IMAGE_DICT["tower_icon"] = ("defense_tower_icon.png", (15,15))
        IMAGE_DICT["enemy_icon"] = ("enemy_icon.png", (15,15))
        IMAGE_DICT["level"] = ("level.png", (15,15))
        IMAGE_DICT["score"] = ("score.png", (15,15))
    else:
        #MAC Dictionary relating object type to the image files it uses and its dimensions
        IMAGE_DICT = {}
        IMAGE_DICT["base_tower"] = ("base_tower.bmp", (20, 40))
        IMAGE_DICT["defense_tower"] = ("defense_tower.bmp", (20, 20))
        IMAGE_DICT["enemy"] = ("enemy.bmp", (20, 20))
        IMAGE_DICT["background"] = ("grass_background.bmp", MAP_SIZE)
        IMAGE_DICT["gold_icon"] = ("gold_coins.bmp", (15,15))
        IMAGE_DICT["tower_icon"] = ("defense_tower_icon.bmp", (15,15))
        IMAGE_DICT["enemy_icon"] = ("enemy_icon.bmp", (15,15))
        IMAGE_DICT["level"] = ("level.bmp", (15,15))
        IMAGE_DICT["score"] = ("score_icon.bmp", (15,15))
        
    return IMAGE_DICT
    
def map_border():
    xr = range(MARGIN+10,MAP_SIZE[0]+MARGIN-10)
    yr = range(MARGIN+10,MAP_SIZE[1]+MARGIN-10)
    n1 = len(xr)
    n2 = len(yr)
    x0 = [MARGIN+10] * n1
    y0 = [MARGIN+10] * n2
    xn = [MARGIN+MAP_SIZE[0]-10] * n1
    yn = [MARGIN+MAP_SIZE[1]-10] * n2
   
    b1 = zip(x0,yr)
    b2 = zip(xn,yr)
    b3 = zip(xr,y0)
    b4 = zip(xr,yn)
    
    border = b1 + b2 + b3 + b4
    return border

def calc_distance (obj1, obj2):
    distance = math.sqrt(float((obj2[0]-obj1[0])**2 + (obj2[1]-obj1[1])**2))
    return distance

def angle(v1, v2):
    dotproduct = sum((a*b) for a,b in zip(v1, v2))
    lengthv1 = math.sqrt(sum(a**2 for a in v1))
    lengthv2 = math.sqrt(sum(a**2 for a in v2))
    if lengthv1 == 0 or lengthv2 == 0:
        return 0
    while True:
        try:
            angle = math.acos(dotproduct/ (lengthv1 * lengthv2))
            angle = math.degrees(angle)
            return angle
        except ValueError:
            return 0

def getKey(user_score):
    return user_score.score

def update_text(screen, message, location,obj_type):
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
    textRect.x = MARGIN+50+textx*(location-1)*6
    screen.blit(text, textRect)
    icon = Background(obj_type, [textRect.x - 20, textRect.y])
    screen.blit(icon.image, icon.rect)

def sidebar(screen, tower_number, money, wavecount, level, score):
    screen.fill(black)
    update_text(screen, "Tower #: " + str(tower_number), 1, "tower_icon")
    update_text(screen, "Money: " + str(money), 2, "gold_icon")
    update_text(screen, "Wave #: " + str(wavecount), 3, "enemy_icon") 
    update_text(screen, "Score #: " + str(score), 4, "score")
    if level == 1:
        if os.path.isfile('saved_state.txt'):
            update_text(screen, "Difficulty Level: Easy", 5, "level")
    elif level == 2:
        update_text(screen, "Difficulty Level: Medium", 5, "level") 
    else:
        update_text(screen, "Difficulty Level: Hard", 5, "level") 
     
        
def new_game(saved_stats = None, highscore_archive = None, level = 1, extension = ".bmp"):
    """
    Sets up all necessary components to start a new game
    of power tower.
    """
    #pygame.init() # initialize all imported pygame modules
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tower Power") # caption sets title of Window
    screen.fill(black) # (0,0,0) represents RGB for black
    
    # load the image dictionary
    global IMAGE_DICT
    IMAGE_DICT = image_dictionary(extension)
    money_v = [5000, 4000, 2500]
    
    if saved_stats != None:
        tower_number = int(saved_stats[0])
        money = int(saved_stats[1])
        wavecount = int(saved_stats[2])
        score = int(saved_stats[3])
        difficulty = int(saved_stats[4])
        tower_list = []
        username = saved_stats[5]
        if len(saved_stats) > 6:
            for i in range(5, len(saved_stats)):
                 for j in range(len(saved_stats[i])):
                    if saved_stats[i][j] == ",":
                        for k in range(len(saved_stats[i])):
                            if saved_stats[i][k] == "+":
                                x = int(saved_stats[i][1:j])
                                y = int(saved_stats[i][j+2:k-1])
                                time = int(saved_stats[i][k+1:len(saved_stats[i])-1])
                                if time != 0:
                                    tower_list.append([time, (x,y)])
    else:
        tower_number = 1
        wavecount = 0
        tower_list = None
        difficulty = 1
        score = 0
        username = "guest"
        if level!= 1:
            difficulty = level
        money = money_v[level-1]
        
    highscores = highscore_archive;

    # other starting variables, modified by the setting chosen in the opening menu    
    HP_enemy = [100, 150, 200]
    HP_tower = [500, 500, 600]
    HP_base = [1000, 1200, 1200]
    speed_level = [2,4,6]
    defense_range = [200, 150, 100]
    attack_power_tower = [2,3,4]
    attack_power_enemy = [5,5,5]
    tower_cost = [500,500,500]
    money_earned_per_enemy = 50
    
    defense_range_base = [15,20,25]
    attack_power_base = [5,8,10]

    starting_varaibles = [HP_enemy[difficulty-1],
                          HP_tower[difficulty-1],
                          speed_level[difficulty-1],
                          tower_number,
                          wavecount,money,
                          defense_range[difficulty-1],
                          tower_cost[difficulty-1],
                          attack_power_tower[difficulty-1],
                          attack_power_enemy[difficulty-1],
                          tower_list, score,
                          difficulty,
                          highscores,
                          username,
                          money_earned_per_enemy]
    
    board = Board(HP_base[difficulty-1],screen,defense_range_base[difficulty-1], attack_power_base[difficulty-1])

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
    tower_list = starting_varaibles[10]
    score = starting_varaibles[11]
    difficulty = starting_varaibles[12]
    highscores = starting_varaibles[13]
    username = starting_varaibles[14]
    money_earned_per_enemy = starting_varaibles[15]

    time_created = 0

    # setup background
    BackGround = Background("background", [MARGIN, MARGIN])
    screen.blit(BackGround.image, BackGround.rect)
    pygame.display.flip()

    if tower_list is not None:
        for i in range(len(tower_list)):
            time = tower_list[i][0]
            position = tower_list[i][1]
            if board.add_tower_to_board(time, position, HP_tower, defense_range, attack_power_tower):
                board.towers.draw(screen)
                pygame.display.flip()


    board.towers.draw(screen) # draw tower Sprite
    pygame.display.flip()
    
    border = map_border()
    events = pygame.event.get()
    event_types = [event.type for event in events]
    gameover = False
    mainloop = True
    loop_number = 0
    loop_created = 0
    
    while mainloop == True:
        while pygame.QUIT not in event_types and gameover is not True: # when use didn't click exit on the window    
             #pygame.display.flip()
    
             # action 1: add tower
             if pygame.mouse.get_pressed()[0]:
                 if money >= tower_cost:
                     x,y = pygame.mouse.get_pos()
                 # add a defense tower at the location clicked
                     time = pygame.time.get_ticks()
                     if board.add_tower_to_board(time, (x,y), HP_tower, defense_range, attack_power_tower):
                         board.towers.draw(screen)
                         pygame.display.flip()
                         money -= tower_cost
                         tower_number +=1
    
             #Updated Action 2 and 5 (move)
             num_border_locs = len(border)
             num_enemies = 2
             time_period = 1000
             elapsed_time = pygame.time.get_ticks() - time_created
    
             if loop_number - loop_created > 10:
                 enemies_count = 0
                 while enemies_count < num_enemies:
                     index = random.randint(0,num_border_locs-1)
                     x,y = border[index]
                     time = pygame.time.get_ticks()
                     board.add_enemy_to_board(time, (x,y),speed_level, HP_enemy, attack_power_enemy,money_earned_per_enemy)
                     enemies_count +=1
                 loop_created = loop_number
                 time_created = pygame.time.get_ticks()
                 wavecount +=1
            # Increase enemy HP by 10 and amount of money earned by 5 every 10 waves 
             if wavecount % 10 == 0:
                 HP_enemy += 10
                 money_earned_per_enemy += 5                 
             
             # action 3: defense attacks enemy (shoot)
             for tower in board.towers:
                 money_earned = tower.attack()
                 score += money_earned*difficulty
                 pygame.display.flip()
                 clock.tick(100)
                 if money_earned != None:
                     money += money_earned
                                     
             # action 4: enemy attack defense and base tower
             for enemy in board.enemies:
                 collision = enemy.touching_defense_or_base_tower(board)
                 if collision is not None:
                     enemy.attack(collision, board)
                     if board.tower_dict[0] is None:
                         gameover = True
                         print "Your Tower is Destroyed!"
                         print "Your Score is ", score
                         break
                 else:
                    enemy.point_at_base(board)
                 enemy.update()
    
            # call sidebar        
             sidebar(screen, tower_number, money, wavecount,difficulty,score)
    #        screen.fill(black) # (0,0,0) represents RGB for black
             screen.blit(BackGround.image, BackGround.rect)
             board.towers.draw(screen)
    
             board.enemies.draw(screen)
             # update life bar
             board.lifebars.update()
             # board.lifebars.draw(screen)
        
             events = pygame.event.get()
             event_types = [event.type for event in events] # update event list

             loop_number += 1
    
        pygame.display.quit()
        pygame.init()
        Start_screen = pygame.display.set_mode([SCREEN_SIZE[0],300])
        pygame.display.set_caption("HighScore Leaderboard") # caption sets title of Window
        Start_screen.fill(black) # (0,0,0) represents RGB for black
        for user in range(len(highscores)):
            if score > highscores[user].score:
                inputask.display(Start_screen, "You Made It To The Top 10 Highscores!")
                pygame.time.wait(2000)
                Start_screen.fill(black)
                pygame.display.flip()
                while True:     # Only allows for integer input, refuses any others
                    try:
                        username = inputask.ask(Start_screen,"Please Enter Your Name ")
                        break
                    except ValueError:
                        inputask.display_box(Start_screen, "Please enter a string")
                highscores.insert(user, User_Score(username, score))
                Start_screen.fill(black)
                pygame.display.set_caption("HighScore Leaderboard")  
                display_high_score(Start_screen, highscores)
                pygame.time.wait(4000) 
                break
            
        highscores = highscores[0:10]
        
        if highscores == []:
            while True:     # Only allows for integer input, refuses any others
                try:
                    username = inputask.ask(Start_screen,"Please Enter Your Name: ")
                    break
                except ValueError:
                    inputask.display_box(Start_screen, "Please enter a string")
            highscores.insert(user, User_Score(username, score))
            break
 
        pygame.display.quit()
        mainloop = False
        
        # save current game data
        with open('saved_state.txt','w') as f:
            f.write(str(tower_number)+"\n")
            f.write(str(money)+"\n")
            f.write(str(wavecount)+"\n")
            f.write(str(score)+"\n")
            f.write(str(difficulty)+"\n")
            f.write(str(username)+"\n")
            for tower in board.towers:
                f.write(str(tower.position)+"+"+str(tower.time) + "\n")
            f.close()
    
        with open('highscores.txt','w') as f:
            for user in range(len(highscores)):
                f.write(str(highscores[user].name)+"+"+str(highscores[user].score) + "\n")
            f.close()

    start_game()
    
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
        time = 0
        
        self.base_tower = Tower(self, time, (init_x, init_y), "base_tower", HP_base, defense_range, attack_power)
        self.base_tower_lifebar = Lifebar(self, time, self.base_tower,screen, HP_base)

        # Initialize the tower dic
        self.tower_dict = {}
        self.tower_dict[0] = self.base_tower

        # Create life bar dict and Sprite group
        self.lifebar_dict = {}
        self.lifebars = pygame.sprite.Group()

        # Add base tower lifebar to lifebar dict and Sprite group
        self.lifebar_dict[0] = self.base_tower_lifebar
        self.lifebars.add(self.base_tower_lifebar)
        
        # Adds Tower to the "towers" Sprite List
        self.towers = pygame.sprite.Group()
        self.towers.add(self.base_tower)

        # Create enemy dict and Sprite group
        self.enemy_dict = {}
        self.enemies = pygame.sprite.Group()

    def add_tower_to_board(self, time, position, HP_tower,defense_range, attack_power):
        defense_tower = Defense_tower(self, time, position, "defense_tower", HP_tower, defense_range, attack_power)
        if defense_tower.rect.x < MARGIN or defense_tower.rect.topright[0] > MARGIN + MAP_SIZE[0] or defense_tower.rect.y < MARGIN or defense_tower.rect.bottomleft[1] > MARGIN + MAP_SIZE[1]:
            return False
        else:
            collision_tower = pygame.sprite.spritecollideany(defense_tower, self.towers, None)
            collision_enemy = pygame.sprite.spritecollideany(defense_tower, self.enemies, None)
            if collision_tower == None and collision_enemy == None:
                self.tower_dict[time] = defense_tower
                self.towers.add(defense_tower)
                defense_tower_lifebar = Lifebar(self, time, defense_tower, self.screen, HP_tower)

            # Add defense tower lifebar to lifebar dict and Sprite group
                self.lifebar_dict[time] = defense_tower_lifebar
                self.lifebars.add(defense_tower_lifebar)
                return True

    def add_enemy_to_board(self, time, position, speed_level, HP_enemy, attack_power, money_earned_per_enemy):
        enemy = Enemies(self, time, position, "enemy", HP_enemy, speed_level, attack_power, money_earned_per_enemy)
        collision_tower = pygame.sprite.spritecollideany(enemy, self.towers, None)
        collision_enemy = pygame.sprite.spritecollideany(enemy, self.enemies, None)
        if collision_tower is None and collision_enemy is None:
            self.enemy_dict[time] = enemy
            self.enemies.add(enemy)
            enemy_lifebar = Lifebar(self, time, enemy, self.screen, HP_enemy)

            # Add defense tower lifebar to lifebar dict and Sprite group
            self.lifebar_dict[time] = enemy_lifebar
            self.lifebars.add(enemy_lifebar)

    def draw_laser_line(self, enemy_position, tower_position):
        # draws normal solid line
        pygame.draw.line(self.screen, black, tower_position, enemy_position, 2)
        
        # if we want to draw dashed line
        #draw_dash(self.screen, black, tower_position, enemy_position, dash_length = 5)
        # draw_dash2(self.screen, red, tower_position, enemy_position, width = 2, dash_length = 5)
       
class Game_obj(pygame.sprite.Sprite):
    def __init__(self, board, time, position, obj_type, init_HP, attack_power):
        pygame.sprite.Sprite.__init__(self)
        self.time = time
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
    def __init__(self, time, board, boss, screen, full_HP):
        pygame.sprite.Sprite.__init__(self)
        self.time = time
        self.boss = boss
        self.screen = screen
        self.position = (self.boss.position[0] - self.boss.dimensions[0]/2, self.boss.position[1] - 7 - self.boss.dimensions[1]/2) # lifebar is positioned directly below its boss (game object)
        self.dimensions = (self.boss.dimensions[0],5) #lifebar is same width as its boss and 10 pixels high
        self.HP = self.boss.HP
        self.board = board
        self.set_pic()
        pygame.draw.rect(self.screen, (0,255,0), (self.position,self.dimensions))
        self.full_HP = full_HP
        self.update_Lifebar_text()

    def set_pic(self):
        self.image = pygame.Surface(self.dimensions)
        self.image.set_colorkey((0,0,0)) # black transparent

    def update_Lifebar_text(self):
        textSize = 10
        font = pygame.font.Font(None, 12)
        textx = 0 + textSize
        text = font.render(str(self.boss.HP) + "/" + str(self.full_HP), True, white)
        textRect = text.get_rect()
        textRect.y = self.position[1] - 8
        textRect.centerx = self.boss.rect.center[0]
        self.screen.blit(text, textRect)
   
    def update(self):

        self.position = (self.boss.rect.center[0] - self.boss.dimensions[0]/2, self.boss.rect.center[1] - 7 - self.boss.dimensions[1]/2)
        self.frac = float(self.boss.HP) / float(self.full_HP)
        pygame.draw.rect(self.screen, (0,0,0), (self.position,self.dimensions)) # fill black
        pygame.draw.rect(self.screen, (0,255,0), (self.position,(int(self.boss.dimensions[0] * self.frac),self.dimensions[1])),0) # fill green

        self.update_Lifebar_text()
            
class Tower(Game_obj):
    def __init__(self, board, time, position, obj_type, init_HP, defense_range, attack_power):
        super(Tower, self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.defense_range = defense_range
    
    def attack(self):
        money = 0
        attack_enemy = self.closest_enemy()
        if attack_enemy != None:
            enemy_position =  attack_enemy.position                  
            self.board.draw_laser_line(enemy_position, self.position)
            attack_enemy.HP -= self.attack_power                 
            if attack_enemy.HP <= 0:
                money = attack_enemy.enemy_death(self.board)
        return money

    def tower_death(self, board):
        # need to remove the object from the board
        # from dic list
        time = self.time
        board.tower_dict[time] = None
        lifebar = board.lifebar_dict[time]
        lifebar.kill()
        board.lifebar_dict[time] = None

        self.kill()
        self.update()
        lifebar.update()

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
    def __init__(self, board, time, position, obj_type, init_HP, defense_range, attack_power):
        super(Defense_tower,self).__init__(board, time, position, obj_type, init_HP, defense_range, attack_power)


class Enemies(Game_obj):
    def __init__(self, board, time, position, obj_type, init_HP, level, attack_power, money_earned_per_enemy):
        super(Enemies,self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.position = position
        self.orientation = (0.0, 1.0) #points up initially
        self.speed_level = 2*level
        self.dx = 0
        self.dy = 0
        self.point_at_base(board)
        self.money_earned_per_enemy = money_earned_per_enemy

    def point_at_base(self, board): # moving direction
#        direction = (board.base_tower.position[0] - self.position[0], board.base_tower.position[1] - self.position[1])
#        new_orientation = [0, 0]
#
#        if direction[0] < 0:
#            new_orientation[0] = -1
#        elif direction[0] == 0:
#            new_orientation[0] = 0
#        elif direction[0] > 0:
#            new_orientation[0] = 1
#        if direction[1] < 0:
#            new_orientation[1] = -1
#        elif direction[1] == 0:
#            new_orientation[1] = 0
#        elif direction[1] > 0:
#            new_orientation[1] = 1
#        self.dx = self.speed_level*new_orientation[0]
#        self.dy = self.speed_level*new_orientation[1]

        direction = (float(board.base_tower.position[0] - self.position[0]), float(board.base_tower.position[1] - self.position[1]))
        distance = calc_distance(self.position, board.base_tower.position)
        new_orientation = (direction[0]/distance, direction[1]/distance)
        rotate_angle = angle(new_orientation, self.orientation)
#        print "angle: ", rotate_angle
        if rotate_angle > 1:
            self.image = pygame.transform.rotate(self.image, rotate_angle)
        self.dx = int(self.speed_level*(new_orientation[0]))
        self.dy = int(self.speed_level*(new_orientation[1]))
        self.orientation = new_orientation
        
    def set_new_speed(self,new_level):
        self.speed_level = 1*new_level

    def attack(self, collision, board):
        collision.HP -= self.attack_power
        if collision.HP <= 0:
            collision.tower_death(board)

    def enemy_death(self, board):
        # need to remove the object from the board
        # from dic list
        time = self.time
        board.enemy_dict[time] = None
        lifebar = board.lifebar_dict[time]
        lifebar.kill()
        board.lifebar_dict[time] = None
        self.kill()
        self.update()
        lifebar.update()
        return self.money_earned_per_enemy
        
    def touching_defense_or_base_tower(self, board):
        collision = pygame.sprite.spritecollideany(self, board.towers, collided=None)
        if collision is not None:
            self.dx = 0
            self.dy = 0
        return collision

    def update(self):
        # add in angles from find direction to base tower
#        self.rect.x += self.dx
#        self.rect.y += self.dy
        self.rect = self.rect.move(self.dx,self.dy)
        self.position = self.rect.center

class User_Score(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return '{}: {}'.format(self.name, self.score)
        
def start_menu():
    pygame.init()
    Start_screen = pygame.display.set_mode([SCREEN_SIZE[0],300])
    pygame.display.set_caption("Menu") # caption sets title of Window
    Start_screen.fill(black) # (0,0,0) represents RGB for black
    results = menu(Start_screen) # start = None, load = 2
    
    #load high score
    f = open('highscores.txt','r')
    highscore_archive = f.readlines()
    highscore_archive_list = convert_score_list(highscore_archive)
    
    # load platform option
    g = open('platform.txt','r')
    extension = g.readlines()

    if results is None: # This means user selected start game
        Start_screen.fill(black)
        pygame.display.set_caption("Difficulty Level")
        level = level_menu(Start_screen)
        return level      
    elif results == 2: # user selected LOAD game
        with open('saved_state.txt','r') as f:
            saved_state = f.readlines() # need to pass this into the game to update the state
        new_game(saved_state,highscore_archive_list,extension = extension)
        return None
    # use options to specify operating system
    elif results == 3:
        Start_screen.fill(black)
        pygame.display.set_caption("Platform") 
        platform = pl_menu(Start_screen)
        if platform != 4: # 4 refers to back
            with open('platform.txt','w') as f:
                if platform == 1:
                    f.write(".png")
                else:
                    f.write(".bmp")
        return 4
        
    elif results == 4: # user selected high score
        Start_screen.fill(black)
        pygame.display.set_caption("HighScore Leaderboard")  
        events = pygame.event.get()
        event_types = [event.type for event in events]
        while pygame.MOUSEBUTTONDOWN not in event_types:
            display_high_score(Start_screen, highscore_archive_list)
            events = pygame.event.get()
            event_types = [event.type for event in events]
        return 4

def start_game():
    # call start menu
    level = start_menu()
    while level != None:
        if level == 4:
            level = start_menu()
        else: 
            #load high score
            f = open('highscores.txt','r')
            highscore_archive = f.readlines()
            highscore_archive_list = convert_score_list(highscore_archive)
            # load platform option
            g = open('platform.txt','r')
            extension = g.readlines()
            new_game(highscore_archive = highscore_archive_list, level = level, extension = extension)
            break

def display_high_score(screen, highscore_list):
    location = 1
    inputask.update_text(screen, "High Scores", location, 24)
    for user in highscore_list:
        location +=1
        #message = user[]
        inputask.update_text(screen, user.name + ": "+ str(user.score) , location,20)  
        
def convert_score_list(highscore_archive):
    highscores = []
    if highscore_archive != []:
         for i in range(len(highscore_archive)):
             for j in range(len(highscore_archive[i])):
                 if highscore_archive[i][j] == "+":
                    archive_name = highscore_archive[i][0:j]
                    archive_score = int(highscore_archive[i][j+1:len(highscore_archive[i])-1])
                    highscores.append(User_Score(archive_name, archive_score))
                    highscores = sorted(highscores, key=getKey, reverse=True)
    else:
        highscores = [User_Score("--empty--", 0),
                      User_Score("--empty--", 0),
                      User_Score("--empty--", 0),
                      User_Score("--empty--", 0),
                      User_Score("--empty--", 0),
                      User_Score("--empty--", 0),
                      User_Score("--empty--", 0),
                      User_Score("--empty--", 0),
                      User_Score("--empty--", 0),
                      User_Score("--empty--", 0)]
    return highscores
    
start_game()