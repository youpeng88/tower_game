# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:39:30 2016

Tower Game for 6.177 MIT Final Project
Alexander Andriatis aandriat@mit.edu
You Peng youpeng@mit.edu
Zachary Buras zjburas@mit.edu

"""
import os
import pygame
import random
import math

# allows for user input
import inputask

# creates pressable button object
import PygButton

# creates main menu
from example_menu import main as menu

# creates difficulty level menu
from difficulty_menu import main as level_menu

# creates platform choice menu
from platform_menu import main as pl_menu


### Global Variables

# RGB color definition 
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)


# screen size
SCREEN_SIZE = (1366, 768)

# margin
MARGIN = SCREEN_SIZE[0]/20

# bar size
BAR_SIZE = (SCREEN_SIZE[0]/5, SCREEN_SIZE[1])

# map size
MAP_SIZE = (SCREEN_SIZE[0] - 2*MARGIN - BAR_SIZE[0], SCREEN_SIZE[1] - 2*MARGIN)  # (width in pixels, height in pixels)

# define start screen
pygame.init()

# stores all the image used by the game for both PC and MAC options
def image_dictionary(extension):
    if extension == ".png":
    #PC Dictionary relating object type to the image files it uses and its dimensions
        IMAGE_DICT = {}
        IMAGE_DICT["base_tower"] = ("transparent_base_tower.png", (20, 40))
        IMAGE_DICT["defense_tower"] = ("transparent_defense_tower.png", (20, 20))
        IMAGE_DICT["enemy"] = ("transparent_enemy.png", (20, 20))
        IMAGE_DICT["knight"] = ("transparent_knight.png", (20, 20))
        IMAGE_DICT["background"] = ("grass_background.png", MAP_SIZE)
        IMAGE_DICT["gold_icon"] = ("gold_coins.png", (15,15))
        IMAGE_DICT["tower_icon"] = ("defense_tower_icon.png", (15,15))
        IMAGE_DICT["enemy_icon"] = ("enemy_icon.png", (15,15))
        IMAGE_DICT["level"] = ("level.png", (15,15))
        IMAGE_DICT["score"] = ("score_icon.png", (15,15))
        IMAGE_DICT["knight_click"] = ("knight_click.png", (15,15))
        IMAGE_DICT["tower"] = ("tower_icon.png", (15,15))
        IMAGE_DICT["tower_click"] = ("tower_click.png", (15,15))
        IMAGE_DICT["cannonball"] = ("cannonball.png", (10,10))
        IMAGE_DICT["dragon"] = ("dragon.png", (40,40))

    else:
        #MAC Dictionary relating object type to the image files it uses and its dimensions
        IMAGE_DICT = {}
        IMAGE_DICT["base_tower"] = ("base_tower.bmp", (20, 40))
        IMAGE_DICT["defense_tower"] = ("defense_tower.bmp", (20, 20))
        IMAGE_DICT["enemy"] = ("enemy.bmp", (20, 20))
        IMAGE_DICT["knight"] = ("knight.bmp", (20, 20))
        IMAGE_DICT["background"] = ("grass_background.bmp", MAP_SIZE)
        IMAGE_DICT["gold_icon"] = ("gold_coins.bmp", (15,15))
        IMAGE_DICT["tower_icon"] = ("defense_tower_icon.bmp", (15,15))
        IMAGE_DICT["enemy_icon"] = ("enemy_icon.bmp", (15,15))
        IMAGE_DICT["level"] = ("level.bmp", (15,15))
        IMAGE_DICT["score"] = ("score_icon.bmp", (15,15))
        IMAGE_DICT["knight_click"] = ("knight_click.bmp", (15,15))
        IMAGE_DICT["tower"] = ("tower_icon.bmp", (15,15))
        IMAGE_DICT["tower_click"] = ("tower_click.bmp", (15,15))
        IMAGE_DICT["cannonball"] = ("cannonball.bmp", (10,10))
        IMAGE_DICT["dragon"] = ("dragon.bmp", (40,40))

        
    return IMAGE_DICT
 
# stores all the border pixel locations
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

# a fuction used to calculate the distance between any 2 pixel locations
def calc_distance (obj1, obj2):
    distance = math.sqrt(float((obj2[0]-obj1[0])**2 + (obj2[1]-obj1[1])**2))
    return distance

# a fuction used to calculate the angle between any 2 vectors
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

# used to access the score of a user
def getKey(user_score):
    return user_score.score

# prompts the starting menu
def start_menu(results):
    pygame.init()
    # sets up the menu screen
    Start_screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    pygame.display.set_caption("Menu") # caption sets title of Window
    Start_screen.fill(black) 
    pygame.display.flip()
    if results is 1:
        results = menu(Start_screen) # start = None, load = 2

    # initialize files if they don't exist
    open('highscores.txt','a+').close()
    open('platform.txt','a+').close()
    open('saved_state.txt','a+').close()


    #load high scores
    f = open('highscores.txt','r')
    highscore_archive = f.readlines()
    highscore_archive_list = convert_score_list(highscore_archive)
    
    # load platform option
    g = open('platform.txt','r')
    os_type = g.readlines()
    # check if platform option has been defined, if not, asks to define platform first
    try:
        extension = os_type[0]
        print extension
    except IndexError:
        results = 3 # if no platform option, prompts to the platform choice menu

    if results == 1: # This means user selected start game
        Start_screen.fill(black)
        pygame.display.set_caption("Difficulty Level")
        level = level_menu(Start_screen)
        return level      
    elif results == 2: # user selected LOAD game
        with open('saved_state.txt','r') as f:
            saved_state = f.readlines() # need to pass this into the game to update the state
            while True:
                # checks if there is a saved state, if yes, calls for game start
                try:
                    test = saved_state[5]
                    new_game(saved_state,highscore_archive_list, extension, level=1)
                    return None
                except IndexError:
                    break
        # returns to menu if no saved game
        return 4
    
    elif results == 3: # user selected to specify operating system to select proper image type (.bmp only works on mac, .png only o PC)
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
        # click or press anywhere on the screen to go back to main menu
        while pygame.MOUSEBUTTONDOWN not in event_types and pygame.KEYDOWN not in event_types:
            display_high_score(Start_screen, highscore_archive_list)
            events = pygame.event.get()
            event_types = [event.type for event in events]
        return 4
        
    elif results == 5: # user select to see instructions
        Start_screen.fill(black)
        pygame.display.set_caption("Game Instruction")  
        events = pygame.event.get()
        event_types = [event.type for event in events]
        # click or press anywhere on the screen to go back to main menu
        while pygame.MOUSEBUTTONDOWN not in event_types and pygame.KEYDOWN not in event_types:
            display_instructions(Start_screen)
            events = pygame.event.get()
            event_types = [event.type for event in events]
        return 4

# function to generate a new game start with menu
def start_game():
    # call start menu 
    level = start_menu(1)
    while level != None: # back is selected on the menu
        if level == 4:
            level = start_menu(1) # go back to main menu page
        else: # start new game selected with a difficulty level
            #load high score
            f = open('highscores.txt','r')
            highscore_archive = f.readlines()
            highscore_archive_list = convert_score_list(highscore_archive)
            # load platform option
            g = open('platform.txt','r')
            os_type = g.readlines()
            while True:
                # checks if platform has been defined, if not, asks to select platform
                try:
                    extension = os_type[0]
                    print extension
                    # starts a new game
                    new_game(saved_stats = None, highscore_archive = highscore_archive_list, level = level, extension = extension)
                    break
                except IndexError:
                    # goes to the menu for platform selection
                    level = start_menu(3)
                    break

# function used to display game instruction
def display_instructions(screen):
    location = -3
    fontsize = 20
    Tower_Placement = "How to play: Click anywhere on the map area to place defenses"
    Knight_Placement = "How to play: To choose defense type, select tower or knight in side menu"
    Enemy_waves = "How enemies move: Enemies come out in batches randomly from the border of the map"
    Enemy_kill = "How enemies kill: Enemies only kill when they are next to the tower"
    Game_money = "How to earn gold: Kill enemies to earn gold and spend gold to build defenses"
    Game_win = "How to win: Kill as many enemies as possible to achieve higher score"
    Enemy_grow = "Watch out! Enemies come out later with more HP and more killing power"

    inputask.update_text(screen, "Instructions" , location,30)
    inputask.update_text(screen,  Tower_Placement, location+2, fontsize)
    inputask.update_text(screen, Knight_Placement, location+4, fontsize)
    inputask.update_text(screen,  Enemy_waves, location+6, fontsize)
    inputask.update_text(screen,  Enemy_kill, location+8, fontsize)
    inputask.update_text(screen,  Game_money, location+10, fontsize)
    inputask.update_text(screen,  Game_win, location+12, fontsize)
    inputask.update_text(screen,  "Have Fun!!!!! But....", location+14, fontsize)
    inputask.update_text(screen,  Enemy_grow, location+16, fontsize)

# function used to display game highscore
def display_high_score(screen, highscore_list):
    location = 2
    inputask.update_text(screen, "High Scores", location-1, 30)
    for user in highscore_list:
        location +=1
        inputask.update_text(screen, "Top " + str(location-2) +" : "+user.name + ",  "+ str(user.score) , location,20)
        if location > 11:
            break
 
# function used to generate high score list using user_score objects       
def convert_score_list(highscore_archive):
    highscores = []
    if highscore_archive != []:
         for i in range(len(highscore_archive)):
             for j in range(len(highscore_archive[i])):
                 # Reads highscore list as a name and a score
                 if highscore_archive[i][j] == "+":
                    archive_name = highscore_archive[i][0:j]
                    archive_score = int(highscore_archive[i][j+1:len(highscore_archive[i])-1])
                    highscores.append(User_Score(archive_name, archive_score))
                    highscores = sorted(highscores, key=getKey, reverse=True)
    else:
        # Defines an empty highscore section if no previous highscores
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

# function initilize a new game         
def new_game(saved_stats, highscore_archive, extension, level):
    """
    Sets up all necessary components to start a new game
    of power tower.
    """
    # make the game full screen
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    pygame.display.set_caption("Tower Power") # caption sets title of Window
    screen.fill(black) # (0,0,0) represents RGB for black
    
    # load the image dictionary
    global IMAGE_DICT
    IMAGE_DICT = image_dictionary(extension)
    
    # Starting money list corresponds to different difficulty level
    money_v = [5000, 4500, 4000]
    
    # checks if previous game stats are saved properly
    if saved_stats is not None:
        while True:
            try:
                test = int(saved_stats[0])
                break
            except IndexError:
                saved_stats = None
                break
    
    # load previous game stats if available
    if saved_stats != None:
        tower_number = int(saved_stats[0])
        knight_number = int(saved_stats[1])
        money = int(saved_stats[2])
        wavecount = int(saved_stats[3])
        score = int(saved_stats[4])
        difficulty = int(saved_stats[5])
        tower_list = []
        enemy_list = []
        knight_list = []
        dragon_list = []
        username = saved_stats[6][1:len(saved_stats[6])-1]
        # Picks whether the lines refer to towers, enemies, kights, or dragons and saves them in separate lists
        for i in range(len(saved_stats)):
             if saved_stats[i][0] == "t":
                 for j in range(len(saved_stats[i])):
                    if saved_stats[i][j] == ",":
                        for k in range(len(saved_stats[i])):
                            if saved_stats[i][k] == "+":
                                x = int(saved_stats[i][2:j])
                                y = int(saved_stats[i][j+2:k-1])
                                time = int(saved_stats[i][k+1:len(saved_stats[i])-1])
                                if time != 0:
                                    tower_list.append([time, (x,y)])
             elif saved_stats[i][0] == "e":
                 for j in range(len(saved_stats[i])):
                    if saved_stats[i][j] == ",":
                        for k in range(len(saved_stats[i])):
                            if saved_stats[i][k] == "+":
                                x = int(saved_stats[i][2:j])
                                y = int(saved_stats[i][j+2:k-1])
                                time = int(saved_stats[i][k+1:len(saved_stats[i])-1])
                                if time != 0:
                                    enemy_list.append([time, (x,y)])
             elif saved_stats[i][0] == "k":
                 for j in range(len(saved_stats[i])):
                    if saved_stats[i][j] == ",":
                        for k in range(len(saved_stats[i])):
                            if saved_stats[i][k] == "+":
                                x = int(saved_stats[i][2:j])
                                y = int(saved_stats[i][j+2:k-1])
                                time = int(saved_stats[i][k+1:len(saved_stats[i])-1])
                                if time != 0:
                                    knight_list.append([time, (x,y)])
             elif saved_stats[i][0] == "d":
                 for j in range(len(saved_stats[i])):
                    if saved_stats[i][j] == ",":
                        for k in range(len(saved_stats[i])):
                            if saved_stats[i][k] == "+":
                                x = int(saved_stats[i][2:j])
                                y = int(saved_stats[i][j+2:k-1])
                                time = int(saved_stats[i][k+1:len(saved_stats[i])-1])
                                if time != 0:
                                    dragon_list.append([time, (x,y)])
                                    
    # if not loading an old game, starts a new game based on difficulty level
    else:
        tower_number = 1
        knight_number = 0
        wavecount = 0
        tower_list = None
        enemy_list = None
        knight_list = None
        dragon_list = None
        difficulty = 1
        score = 0
        username = None
        if level!= 1:
            difficulty = level
        money = money_v[level-1]
        
    highscores = highscore_archive;

    # other starting variables, modified by the setting chosen in the opening menu    
    # list corresponds to difficulty level
    HP_enemy = [100, 150, 200]
    HP_tower = [500, 500, 600]
    HP_base = [1000, 1200, 1200]
    HP_knight = [200,300,400]
    HP_dragon = [200,300,400]
    speed_level = [1,2,3]
    defense_range = [200, 150, 100]
    attack_power_tower = [50, 75, 100]
    attack_power_enemy = [5,5,5]
    attack_power_knight = [10,10,10]
    attack_power_dragon = [10,10,10]
    tower_cost = [500,500,500]
    knight_cost = [100,100,100]
    money_earned_per_enemy = 50
    tower_reload_time = 1000

    defense_range_base = [15,20,25]
    attack_power_base = [5,8,10]
    
    # stores all game parameters
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
                          money_earned_per_enemy,
                          knight_cost[difficulty-1],
                          attack_power_knight[difficulty-1],
                          knight_number,
                          tower_reload_time,
                          enemy_list,
                          knight_list,
                          HP_knight[difficulty-1],
                          HP_dragon[difficulty-1],
                          attack_power_dragon[difficulty-1],
                          dragon_list]
    
    # initialize the board with base tower
    board = Board(HP_base[difficulty-1],screen,defense_range_base[difficulty-1], attack_power_base[difficulty-1])

    # initialize the game clock
    clock = pygame.time.Clock()
    
    # initialize the side bar for the game
    sidebar = siderbar(screen)
    sidebar.add_button("tower","tower_click", (0,1))
    sidebar.add_button("knight","knight_click", (1,1))
    
    # calls main_loop to run the game
    main_loop(screen, board, starting_varaibles, clock, sidebar)

# defines all game actions
def main_loop(screen, board, starting_varaibles, clock, sidebar):
    # retrieve game parameters/settings
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
    knight_cost = starting_varaibles[16]
    attack_power_knight = starting_varaibles[17]
    knight_number = starting_varaibles[18]
    tower_reload_time = starting_varaibles[19]
    enemy_list = starting_varaibles[20]
    knight_list = starting_varaibles[21]
    HP_knight = starting_varaibles[22]
    HP_dragon = starting_varaibles[23]
    attack_power_dragon = starting_varaibles[24]
    dragon_list = starting_varaibles[25]

    # setup background
    BackGround = Background("background", [MARGIN, MARGIN])
    screen.blit(BackGround.image, BackGround.rect)
    
    # load tower, enemy and knights location if old game is loaded
    if tower_list is not None:
        for i in range(len(tower_list)):
            time = tower_list[i][0]
            position = tower_list[i][1]
            if board.add_tower_to_board(time, position, HP_tower, defense_range, attack_power_tower, tower_reload_time):
                board.towers.draw(screen)
    if enemy_list is not None:
        for i in range(len(enemy_list)):
            time = enemy_list[i][0]
            position = enemy_list[i][1]
            if board.add_enemy_to_board(time, position, speed_level, HP_enemy, attack_power_knight, money_earned_per_enemy):
                board.enemies.draw(screen)
    if knight_list is not None:
        for i in range(len(knight_list)):
            time = knight_list[i][0]
            position = knight_list[i][1]
            if board.add_knight_to_board(time, position, HP_knight, attack_power_knight):
                board.knights.draw(screen)
                
    if dragon_list is not None:
        for i in range(len(dragon_list)):
            time = dragon_list[i][0]
            position = dragon_list[i][1]
            if board.add_dragon_to_board(time, position, speed_level, HP_dragon, attack_power_dragon, money_earned_per_enemy):
                board.dragons.draw(screen)
    pygame.display.flip()

    # set default button click to tower
    sidebar.button_list["tower"].buttonDown = True
    sidebar.button_list["knight"].buttonDown = False
    sidebar.display_text(tower_number,knight_number, money, wavecount,difficulty,score)
    sidebar.display_button()
    defense_mode = "tower"
    pygame.display.flip()

    board.towers.draw(screen) # draw tower Sprite
    pygame.display.flip()
    
    # generate the border pixel location lists
    border = map_border()
    
    # sets up game loop initial parameters
    events = pygame.event.get()
    event_types = [event.type for event in events]
    gameover = False
    mainloop = True
    loop_number = 0
    loop_created = 0
    money_earned = 0

    while mainloop == True: # when game is not over and highscore is not checked
        while pygame.QUIT not in event_types and gameover is not True: # when use didn't click exit on the window

            # check if defense_mode has changed and display in button
             for event in events:
                 if 'click' in sidebar.button_list["tower"].handleEvent(event):
                     sidebar.display_button()
                     defense_mode = "tower"
                 if 'click' in sidebar.button_list["knight"].handleEvent(event):
                     sidebar.display_button()
                     defense_mode = "knight"

            # sets the button display mode based on defense_mode correctly
             if defense_mode == "tower":
                 sidebar.button_list["tower"].buttonDown = True
                 sidebar.button_list["knight"].buttonDown = False
             else:
                 sidebar.button_list["tower"].buttonDown = False
                 sidebar.button_list["knight"].buttonDown = True

             # action 1: add tower when defese mode is tower
             if defense_mode == "tower" and pygame.MOUSEBUTTONDOWN in event_types:
                 if money >= tower_cost:
                     x,y = pygame.mouse.get_pos()
                 # add a defense tower at the location clicked (in the map area)
                     time = pygame.time.get_ticks()
                     if board.add_tower_to_board(time, (x,y), HP_tower, defense_range, attack_power_tower, tower_reload_time):
                         board.towers.draw(screen)
                         money -= tower_cost
                         tower_number +=1

             # action 1: add kight when defense mode is knight
             if defense_mode == "knight" and pygame.MOUSEBUTTONDOWN in event_types:
                 if money >= knight_cost:
                     x,y = pygame.mouse.get_pos()
                 # add a knight at the location clicked (in the map area)
                     time = pygame.time.get_ticks()
                     if board.add_knight_to_board(time, (x,y), HP_knight, attack_power_knight):
                         board.towers.draw(screen)
                         money -= knight_cost
                         knight_number +=1

             # action 2: add enemies to board
             num_border_locs = len(border)
             # defines number of demons that appear at a time
             num_enemies = random.randint(0,5)
             # enemy appears every 10 loop cycles
             if loop_number - loop_created > 10:
                 enemies_count = 0
                 while enemies_count < num_enemies:
                     # makes enemies appear randomly from a position on the map border
                     index = random.randint(0,num_border_locs-1)
                     x,y = border[index]
                     time = pygame.time.get_ticks()

                     #Add a dragon to the board every 5 waves
                     if wavecount % 5 == 0 and wavecount > 5:
                         board.add_dragon_to_board(time, (x,y),speed_level, HP_dragon, attack_power_dragon,money_earned_per_enemy)
                     else:
                         board.add_enemy_to_board(time, (x,y),speed_level, HP_enemy, attack_power_enemy,money_earned_per_enemy)

                     enemies_count +=1
                 loop_created = loop_number
                 wavecount +=1
            # Increase enemy HP by 10 and amount of money earned by 5 every 10 waves
                 if wavecount % 10 == 0:
                     HP_enemy += 10
                     HP_dragon += 10

             # action 3: defense tower attacks enemy (shoot)
             for tower in board.towers:
                 tower.attack()
             # action 3: knight attacks demon (contact)
             for knight in board.knights:
                 collision = knight.touching_enemy(board)
                 if collision is not None:
                     money_earned = knight.attack(collision, board)
                 else:
                     collision_with_another_enemy = knight.touching_another_knight_or_tower(board)

                     if collision_with_another_enemy is None:
                         knight.point_at_enemy(board)
                 if money_earned != None:
                     money += money_earned
                     score += money_earned*difficulty

             # action 4: demon attacks defense and base tower
             for enemy in board.enemies:
                 collision = enemy.touching_defense_or_base_tower_or_knight(board)
                 if collision is not None:
                     enemy.attack(collision, board)
                     if board.tower_dict[0] is None:
                         gameover = True
                         print "Your Tower is Destroyed!"
                         print "Your Score is ", score
                         break
                 else:
                     collision_with_another_enemy = enemy.touching_another_enemy(board)

                     if collision_with_another_enemy is None:
                         enemy.point_at_base(board)

            # action 4: dragon attacks defense and base tower
             for dragon in board.dragons:
                 collision = dragon.touching_defense_or_base_tower(board)
                 if collision is not None:
                     dragon.attack(collision, board)
                     if board.tower_dict[0] is None:
                         gameover = True
                         print "Your Tower is Destroyed!"
                         print "Your Score is ", score
                         break
                 else:
                     collision_with_another_dragon = dragon.touching_another_dragon(board)

                     if collision_with_another_dragon is None:
                         dragon.point_at_tower(board)

            # action 5: shoot cannonballs at enemies
             for cannonball in board.cannonballs:
                money_earned = cannonball.attack(board)
                if money_earned:
                    score += money_earned*difficulty
                    money += money_earned

            # update sidebar, towers, enemies, knights, dragons and all other sprite objects
             sidebar.display_text(tower_number,knight_number, money, wavecount,difficulty,score)
             sidebar.display_button()

             screen.blit(BackGround.image, BackGround.rect)

             board.towers.update()
             board.enemies.update()
             board.lifebars.update()
             board.knights.update()
             board.cannonballs.update()
             board.dragons.update()

             board.cannonballs.draw(screen)
             board.towers.draw(screen)
             board.enemies.draw(screen)
             board.knights.draw(screen)
             board.dragons.draw(screen)

             # redraw display
             pygame.display.flip()

             # update event list
             events = pygame.event.get()
             event_types = [event.type for event in events] # update event list

             # provide game pause choice and goes back to main menu
             for event in events:
                 if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                         gameover = True
                         print "Paused Game"

             loop_number += 1
        
        # prepare to display high score
        Highscore_screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
        pygame.display.set_caption("HighScore Leaderboard") # caption sets title of Window
        Highscore_screen.fill(black) # (0,0,0) 
        
        # if there is high score saved
        for user in range(len(highscores)):
            if score > highscores[user].score: # check if made it to highscore leader board
                inputask.display(Highscore_screen, "You Made It To The Top 10 Highscores!")
                pygame.time.wait(2000)
                Highscore_screen.fill(black)
                pygame.display.flip()
                if username == None:# if current user is not in databse ask for name input
                    while True:     # Only allows for integer input, refuses any others
                        try:
                            username = inputask.ask(Highscore_screen,"Please Enter Your Name ")
                            break
                        except ValueError:
                            inputask.display_box(Highscore_screen, "Please enter a string")
                            
                # add highscore to highscore list
                highscores.insert(user, User_Score(username, score))
                Highscore_screen.fill(black)
                # display the leaderboard for about 3 seconds and then go back to main menu
                pygame.display.set_caption("HighScore Leaderboard")  
                display_high_score(Highscore_screen, highscores)
                pygame.time.wait(2000)
                break
        
        # only saves the top 10 high scores
        highscores = highscores[0:10]
        
        # when there isn't any highsore saved
        if highscores == []:
            if username == None:
                while True:     # Only allows for integer input, refuses any others
                    try:
                        username = inputask.ask(Highscore_screen,"Please Enter Your Name: ")
                        break
                    except ValueError:
                        inputask.display_box(Highscore_screen, "Please enter a string")
            highscores.insert(user, User_Score(username, score))
            break
        mainloop = False
        
        # save current game data
        with open('saved_state.txt','w') as f:
            f.write(str(tower_number)+"\n")
            f.write(str(knight_number)+"\n")
            f.write(str(money)+"\n")
            f.write(str(wavecount)+"\n")
            f.write(str(score)+"\n")
            f.write(str(difficulty)+"\n")
            f.write("u"+str(username)+"\n")
            for tower in board.towers:
                f.write("t"+str(tower.position)+"+"+str(tower.time) + "\n")
            for enemy in board.enemies:
                f.write("e"+str(enemy.position)+"+"+str(enemy.time) + "\n")
            for knight in board.knights:
                f.write("k"+str(knight.position)+"+"+str(knight.time) + "\n")
            for dragon in board.dragons:
                f.write("d"+str(dragon.position)+"+"+str(dragon.time) + "\n")

        # save highscores
        with open('highscores.txt','w') as f:
            for user in range(len(highscores)):
                f.write(str(highscores[user].name)+"+"+str(highscores[user].score) + "\n")

    # goes back to main menu when mainloop = False
    start_game()
    
class Background(pygame.sprite.Sprite): # defines the map background
    def __init__(self, obj_type, position):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(IMAGE_DICT[obj_type][0])
        self.image = pygame.transform.scale(self.image, IMAGE_DICT[obj_type][1])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        
class siderbar(): # makes a sidebar which chooses defense types, displays game info
    def __init__(self,screen):
        self.screen = screen
        self.button_list = {}
    
    def update_text(self, message, location,obj_type): # defines info position with appropriate icon
        textSize = 20
        font = pygame.font.Font("freesansbold.ttf", 20)
        texty = 0 + textSize*6
        text = font.render(message, True, white, black)
        textRect = text.get_rect()
        textRect.centery = MARGIN + texty*(location-1)
        textRect.centerx = SCREEN_SIZE[0] - BAR_SIZE[0]/2
        self.screen.blit(text, textRect)
        icon = Background(obj_type, [textRect.x - 20, textRect.y])
        self.screen.blit(icon.image, icon.rect) 
    
    def add_button(self, obj_type1, obj_type2, location): # creates selection button for defense types
        button_rect = pygame.Rect(SCREEN_SIZE[0]-BAR_SIZE[0]*3/4+70*location[0],MARGIN + 30*location[1], BAR_SIZE[0]/5, 40)
        my_Button = PygButton.PygButton(button_rect,'',bgcolor=white,fgcolor=red)
        my_Button.setSurfaces(IMAGE_DICT[obj_type1][0],IMAGE_DICT[obj_type2][0],IMAGE_DICT[obj_type1][0]) # set tower picture as button        
        self.button_list[obj_type1] = my_Button
        
    def update_button(self,event): # changes button status depending on defense selection
        for my_Button in self.button_list.values():
            my_Button.handleEvent(event)
    
    def display_button(self): # redraws the button when status changes
        for my_Button in self.button_list.values():
            my_Button._visible = True
            my_Button.draw(self.screen)
    
    def display_text(self, tower_number,knight_number, money, wavecount,level,score): # defines and draws game info
        self.screen.fill(black)
        self.update_text("Tower #: " + str(tower_number) + "  Knight #: " + str(knight_number), 1, "tower_icon")
        self.update_text("Money: " + str(money), 2, "gold_icon")
        self.update_text("Wave #: " + str(wavecount), 3, "enemy_icon") 
        self.update_text("Score #: " + str(score), 4, "score")
        if level == 1:
            if os.path.isfile('saved_state.txt'):
                self.update_text("Difficulty Level: Easy", 5, "level")
        elif level == 2:
            self.update_text("Difficulty Level: Medium", 5, "level") 
        else:
            self.update_text("Difficulty Level: Hard", 5, "level") 


class Board: # class to track of all the game objects. ues dictionaries and sprite groups.
    def __init__(self, HP_base,screen,defense_range, attack_power):

        self.screen = screen
        
        # Initialize the base Tower
        init_x = MARGIN+MAP_SIZE[0]/2
        init_y = MARGIN+MAP_SIZE[1]/2
        time = 0
        self.base_tower = Tower(self, time, (init_x, init_y), "base_tower", HP_base, defense_range, attack_power, 0)
        self.base_tower_lifebar = Lifebar(self, time, self.base_tower,screen, HP_base)

        # Initialize the tower dictionary
        self.tower_dict = {}
        self.tower_dict[0] = self.base_tower

        # Create life bar dictionary and Sprite group
        self.lifebar_dict = {}
        self.lifebars = pygame.sprite.Group()

        # Add base tower lifebar to lifebar dictionary and Sprite group
        self.lifebar_dict[0] = self.base_tower_lifebar
        self.lifebars.add(self.base_tower_lifebar)
        
        # Adds Tower to the "towers" Sprite List
        self.towers = pygame.sprite.Group()
        self.towers.add(self.base_tower)

        # Create enemy dictionary and Sprite group
        self.enemy_dict = {}
        self.enemies = pygame.sprite.Group()

        # Create knight dictionary and Sprite group
        self.knight_dict = {}
        self.knights = pygame.sprite.Group()

        # Create cannonball dictionary and Sprite group
        self.cannonball_dict = {}
        self.cannonballs = pygame.sprite.Group()

        # Create dragon dictionary and Sprite group
        self.dragon_dict = {}
        self.dragons = pygame.sprite.Group()
        
    def add_tower_to_board(self, time, position, HP_tower,defense_range, attack_power, tower_reload_time):
        defense_tower = Tower(self, time, position, "defense_tower", HP_tower, defense_range, attack_power, tower_reload_time)
        # checks if tower placement is inside the map boundary
        if defense_tower.rect.x < MARGIN or defense_tower.rect.topright[0] > MARGIN + MAP_SIZE[0] or defense_tower.rect.y < MARGIN or defense_tower.rect.bottomleft[1] > MARGIN + MAP_SIZE[1]:
            return False
        else:
            # checks if tower placement interferes with position of other game objects
            collision_tower = pygame.sprite.spritecollideany(defense_tower, self.towers, None)
            collision_enemy = pygame.sprite.spritecollideany(defense_tower, self.enemies, None)
            collision_knight = pygame.sprite.spritecollideany(defense_tower, self.knights, None)
            collision_dragon = pygame.sprite.spritecollideany(defense_tower, self.dragons, None)
            if collision_tower is None and collision_enemy is None and collision_knight is None and collision_dragon is None:
                self.tower_dict[time] = defense_tower
                self.towers.add(defense_tower)
                defense_tower_lifebar = Lifebar(self, time, defense_tower, self.screen, HP_tower)

            # Add defense tower lifebar to lifebar dict and Sprite group
                self.lifebar_dict[time] = defense_tower_lifebar
                self.lifebars.add(defense_tower_lifebar)
                return True

    def add_enemy_to_board(self, time, position, speed_level, HP_enemy, attack_power, money_earned_per_enemy):
        enemy = Enemies(self, time, position, "enemy", HP_enemy, speed_level, attack_power, money_earned_per_enemy)
        # checks that enemy appearance does not interfere with existing game objects
        collision_tower = pygame.sprite.spritecollideany(enemy, self.towers, None)
        collision_enemy = pygame.sprite.spritecollideany(enemy, self.enemies, None)
        collision_knight = pygame.sprite.spritecollideany(enemy, self.knights, None)
        if collision_tower is None and collision_enemy is None and collision_knight is None:
            self.enemy_dict[time] = enemy
            self.enemies.add(enemy)
            enemy_lifebar = Lifebar(self, time, enemy, self.screen, HP_enemy)

            # Add enemy lifebar to lifebar dict and Sprite group
            self.lifebar_dict[time] = enemy_lifebar
            self.lifebars.add(enemy_lifebar)

    def add_knight_to_board(self, time, position, HP_knight, attack_power):
        knight = Knight(self, time, position, "knight", HP_knight, attack_power)
        # checks that knight is placed inside board
        if knight.rect.x < MARGIN or knight.rect.topright[0] > MARGIN + MAP_SIZE[0] or knight.rect.y < MARGIN or knight.rect.bottomleft[1] > MARGIN + MAP_SIZE[1]:
            return False
        else:
            # checks that knight placement does not interfere with existing game objects
            collision_tower = pygame.sprite.spritecollideany(knight, self.towers, None)
            collision_enemy = pygame.sprite.spritecollideany(knight, self.enemies, None)
            collision_knight = pygame.sprite.spritecollideany(knight, self.knights, None)
            if collision_tower is None and collision_enemy is None and collision_knight is None:
                self.knight_dict[time] = knight
                self.knights.add(knight)
                knight_lifebar = Lifebar(self, time, knight, self.screen, HP_knight)
    
                # Add knight lifebar to lifebar dict and Sprite group
                self.lifebar_dict[time] = knight_lifebar
                self.lifebars.add(knight_lifebar)
                return True
                
    def add_dragon_to_board(self, time, position, speed_level, HP_dragon, attack_power, money_earned_per_enemy):
        dragon = Dragons(self, time, position, "dragon", HP_dragon, speed_level, attack_power, money_earned_per_enemy)
        # checks that dragon placement does not interfere with tower or another dragon, ignores enemies and knights
        collision_tower = pygame.sprite.spritecollideany(dragon, self.towers, None)
        collision_dragon = pygame.sprite.spritecollideany(dragon, self.dragons, None)
        if collision_tower is None and collision_dragon is None:
            self.dragon_dict[time] = dragon
            self.dragons.add(dragon)
            dragon_lifebar = Lifebar(self, time, dragon, self.screen, HP_dragon)

            # Add dragon lifebar to lifebar dict and Sprite group
            self.lifebar_dict[time] = dragon_lifebar
            self.lifebars.add(dragon_lifebar)
    
    def add_cannonball_to_board(self, time, position, HP_cannonball, attack_power, tower):
        cannonball = Cannonball(self, time, position, "cannonball", HP_cannonball, attack_power, tower)
        self.cannonball_dict[time] = cannonball
        self.cannonballs.add(cannonball)
       
class Game_obj(pygame.sprite.Sprite):
    # a general class for objects on board with shared properties
    # superclass for enemies, towers, knights, dragons, cannonballs
    def __init__(self, board, time, position, obj_type, init_HP, attack_power):
        pygame.sprite.Sprite.__init__(self)
        self.time = time
        self.board = board
        self.position = position
        self.dimensions = IMAGE_DICT[obj_type][1]
        self.HP = init_HP
        self.attack_power = attack_power

        # chooses appropriate image from image dictionary based on object type
        self.image = pygame.image.load(IMAGE_DICT[obj_type][0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, IMAGE_DICT[obj_type][1])
        self.rect = self.image.get_rect()
        self.rect.center = position

class Lifebar(pygame.sprite.Sprite): # class for lifebar for all game objects with variable HP
    def __init__(self, time, board, boss, screen, full_HP):
        pygame.sprite.Sprite.__init__(self)
        self.time = time
        self.boss = boss # defines the object to which the lifebar belongs
        self.screen = screen
        # position lifebar above boss
        self.position = (self.boss.position[0] - self.boss.dimensions[0]/2, self.boss.position[1] - 7 - self.boss.dimensions[1]/2) # lifebar is positioned directly above its boss (game object)
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

    def update_Lifebar_text(self): # displays remaining HP over initial HP above each lifebar
        textSize = 15
        font = pygame.font.Font("freesansbold.ttf", 12)
        textx = 0 + textSize
        text = font.render(str(self.boss.HP) + "/" + str(self.full_HP), True, white)
        textRect = text.get_rect()
        textRect.y = self.position[1] - textSize
        textRect.centerx = self.boss.rect.center[0]
        self.screen.blit(text, textRect)
   
    def update(self):  # update position and amount of lifebar filled based on HP remaining
        self.position = (self.boss.rect.center[0] - self.boss.dimensions[0]/2, self.boss.rect.center[1] - 7 - self.boss.dimensions[1]/2)
        self.frac = float(self.boss.HP) / float(self.full_HP)
        pygame.draw.rect(self.screen, (0,0,0), (self.position,self.dimensions)) # fill black
        pygame.draw.rect(self.screen, (0,255,0), (self.position,(int(self.boss.dimensions[0] * self.frac),self.dimensions[1])),0) # fill green

        self.update_Lifebar_text()
            
class Tower(Game_obj): # class for towers, an immobile defense type
    def __init__(self, board, time, position, obj_type, init_HP, defense_range, attack_power, reload_time):
        super(Tower, self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.defense_range = defense_range # how far the tower can shoot
        self.previous_time = 0
        self.reload_time = reload_time # time between shots
    
    def attack(self): # attacks enemies in the vicinity of tower
        attack_enemy = self.closest_enemy() # finds closest enemy
        time = pygame.time.get_ticks()
        passed_time = time - self.previous_time
        if passed_time > self.reload_time:
            if attack_enemy != None: # if an enemy within range can be attacked
                self.board.add_cannonball_to_board(time, self.position, 10, self.attack_power, self)
                self.previous_time = time

    def death(self, board): # in event that tower is killed by enemies removes tower from the dictionary and spritegroup
        # used to associate tower with corresponding lifebar
        time = self.time
        lifebar = board.lifebar_dict[time]
        # removes the tower and lifebar from dictionaries
        board.tower_dict[time] = None
        board.lifebar_dict[time] = None
        # removes tower and lifebar from sprite groups they are in
        lifebar.kill()
        self.kill()

    def closest_enemy(self): # finds closest enemy
        e_position = None
        final_enemy = None
        closest_distance = self.defense_range
        for enemy in self.board.enemies:
            distance = calc_distance(self.position, enemy.position)
            if distance < closest_distance:
                closest_distance = distance
                e_position = enemy.position
                final_enemy = enemy
        for dragon in self.board.dragons:
            distance = calc_distance(self.position, dragon.position)
            if distance < closest_distance:
                closest_distance = distance
                e_position = dragon.position
                final_enemy = dragon
        if e_position != None:
            return final_enemy


class Cannonball(Game_obj): # class for projectiles shot by towers
    def __init__(self, board, time, position, obj_type, init_HP, attack_power, tower):
        super(Cannonball,self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.tower = tower # defines tower associated with cannonball
        self.closest_enemy = tower.closest_enemy()
        self.speed_level = 10 # speed of cannonball travel
        self.dx = 0
        self.dy = 0
        self.point_at_enemy(board)

    def attack(self, board): # attacks enemies along direction of travel, defined by the tower's attack
        collision = self.touching_enemy(board) # finds if cannonball is hitting an enemy

        # checks to see if cannonball is on the map, removes it if not
        if self.rect.x < MARGIN or self.rect.topright[0] > MARGIN + MAP_SIZE[0] or self.rect.y < MARGIN or self.rect.bottomleft[1] > MARGIN + MAP_SIZE[1]:
                self.death(board)
        # if cannonball hits an enemy, reduces enemy HP and destroys itself
        elif collision is not None:
            collision.HP -= self.attack_power
            self.death(board)
            # enemy dies if its HP falls to 0
            if collision.HP <= 0:
                return collision.death(board)
        # if cannonball is stuck delete it
        elif self.dx == 0 and self.dy == 0:
            self.death(board)
        # if cannonball is outside defense range, delete it
        elif calc_distance(self.position, self.tower.position) > self.tower.defense_range:
            self.death(board)
        # if none apply, cannonball keeps flying
        else:
            pass
        return False

    def point_at_enemy(self, board): # calculates direction in which to move to reach enemy at its location at time of fire
        enemy = self.closest_enemy
        if enemy is not None:
            direction = (float(enemy.position[0] - self.position[0]), float(enemy.position[1] - self.position[1]))
            distance = calc_distance(self.position, enemy.position)
            if distance != 0:
                new_orientation = (direction[0]/distance, direction[1]/distance)
                self.dx = int(self.speed_level*(new_orientation[0]))
                self.dy = int(self.speed_level*(new_orientation[1]))
            else:
                self.dx = 0
                self.dy = 0

    def touching_enemy(self, board): # finds enemies that the cannonball is touching
        collision_enemy = pygame.sprite.spritecollideany(self, board.enemies, collided=None)
        collision_dragon = pygame.sprite.spritecollideany(self, board.dragons, collided=None)
        if collision_dragon is not None:
            return collision_dragon
        elif collision_enemy is not None:
            return collision_enemy
        else:
            return None

    def death(self, board): # removes the cannonball
        time = self.time
        board.cannonball_dict[time] = None
        self.kill()

    def update(self): # moves the cannonball
        self.rect = self.rect.move(self.dx,self.dy)
        self.position = self.rect.center

class Knight(Game_obj): # class for knights, a mobile defense type
    def __init__(self, board, time, position, obj_type, init_HP, attack_power):
        super(Knight,self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.speed_level = 2
        self.dx = 0
        self.dy = 0
        self.point_at_enemy(board)

    def point_at_enemy(self, board): # finds closest enemy and moves towards it
        enemy = self.closest_enemy()
        if enemy is not None:
            direction = (float(enemy.position[0] - self.position[0]), float(enemy.position[1] - self.position[1]))
            distance = calc_distance(self.position, enemy.position)
            new_orientation = (direction[0]/distance, direction[1]/distance)
            self.dx = int(self.speed_level*(new_orientation[0]))
            self.dy = int(self.speed_level*(new_orientation[1]))

    def closest_enemy(self): # defines how to find the closest enemy
        final_enemy = None
        closest_distance = MAP_SIZE[1]
        for enemy in self.board.enemies:
            distance = calc_distance(self.position, enemy.position)
            if distance < closest_distance:
                closest_distance = distance
                final_enemy = enemy
        return final_enemy

    def attack(self, collision, board): # if knight contacts enemy, decreases the enemy HP
        collision.HP -= self.attack_power
        if collision.HP <= 0: # if enemy HP is zero, enemy dies
            return collision.death(board)
        return None

    def death(self, board): # if knight HP is zero, knight dies
        # used to associate knight with corresponding lifebar
        time = self.time
        lifebar = board.lifebar_dict[time]
        # removes the knight and lifebar from dictionaries
        board.knight_dict[time] = None
        board.lifebar_dict[time] = None
        # removes knight and lifebar from sprite groups they are in
        lifebar.kill()
        self.kill()

    def touching_enemy(self, board): # determines if knight touches enemy, and stops knight if it is
        collision = pygame.sprite.spritecollideany(self, board.enemies, collided=None)
        if collision is not None:
            self.dx = 0
            self.dy = 0
        return collision


    def touching_another_knight_or_tower(self, board): # if knight collides with another knight or tower, tries moving in a different direction to avoid contact
        sprite_group_without_self = board.knights.copy() # duplicates its group, excluding itself
        sprite_group_without_self.remove(self)

        collision = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None) # checks if it collides with other knights
        if collision is not None or (self.dx,self.dy) == (0,0):
            collision = True
            # picks from 8 different directions in a certain range to find the closest possible movement that lets it escape collision
            for escape_speed_multiplier in range(1,20):
                directions = [(0,escape_speed_multiplier*int(self.speed_level*-0.5)),(escape_speed_multiplier*int(self.speed_level*0.5),0),
                              (0,escape_speed_multiplier*int(self.speed_level*0.5)),(escape_speed_multiplier*int(self.speed_level*-0.5),0),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*-0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*-0.5))]
                random.shuffle(directions) # randomises the directions that are attempted for escape

                for (dx,dy) in directions: # tests moving in the direction chosen
                    self.rect = self.rect.move(dx,dy)
                    collision_in_new_path = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None)
                    if collision_in_new_path is None: # if there is no collision in the direction chosen
                        self.rect = self.rect.move(-dx,-dy) # move back to original position, to be moved later on
                        (self.dx,self.dy) = (dx,dy) # define new direction which will avoid collision
                        break

                    self.rect = self.rect.move(-dx,-dy) # if the direction chosen also has a collision, move back to original position

                if collision_in_new_path is None: # breaks out of the outer loop if a suitable direction is found
                    break

            if collision_in_new_path is not None: # if there is no movement within 20 pixels that produces no collision, stays at rest
                (self.dx,self.dy) = (0,0)

        return collision

    def update(self): # moves the knight
        self.rect = self.rect.move(self.dx,self.dy)
        # if knight is outside of the board, it is removed
        if self.rect.x < MARGIN or self.rect.topright[0] > MARGIN + MAP_SIZE[0] or self.rect.y < MARGIN or self.rect.bottomleft[1] > MARGIN + MAP_SIZE[1]:
            self.death(self.board)
        self.position = self.rect.center

class Enemies(Game_obj):
    def __init__(self, board, time, position, obj_type, init_HP, level, attack_power, money_earned_per_enemy):
        super(Enemies,self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.orientation = (0.0, 1.0) #points down initially
        self.speed_level = 2*level
        self.dx = 0
        self.dy = 0
        self.point_at_base(board)
        self.money_earned_per_enemy = money_earned_per_enemy
        self.living = True

    def point_at_base(self, board): # points at base tower and finds the direction to move towards it
        direction = (float(board.base_tower.position[0] - self.position[0]), float(board.base_tower.position[1] - self.position[1]))
        distance = calc_distance(self.position, board.base_tower.position)
        new_orientation = (direction[0]/distance, direction[1]/distance)
        # rotates the enemy to point towards the central tower
        rotate_angle = angle(new_orientation, self.orientation)
        if rotate_angle > 5: # prevents excessive rotation which can cause glitches
            self.image = pygame.transform.rotate(self.image, rotate_angle)
        # sets movement amount
        self.dx = int(self.speed_level*(new_orientation[0]))
        self.dy = int(self.speed_level*(new_orientation[1]))
        self.orientation = new_orientation

    def attack(self, collision, board): # if enemy collides with a tower or knight, decrease the defense HP
        collision.HP -= self.attack_power
        if collision.HP <= 0: # if defense HP reduced to zero, removes defense
            collision.death(board)

    def death(self, board): # removes the enemy if it dies
        # used to associate enemy with corresponding lifebar
        time = self.time
        self.living = False
        lifebar = board.lifebar_dict[time]
        # removes the enemy and lifebar from dictionaries
        board.enemy_dict[time] = None
        board.lifebar_dict[time] = None
        # removes enemy and lifebar from sprite groups they are in
        lifebar.kill()
        self.kill()
        return self.money_earned_per_enemy
        
    def touching_defense_or_base_tower_or_knight(self, board): # finds if the enemy has hit a defense unit, stops if true
        collision_tower = pygame.sprite.spritecollideany(self, board.towers, collided=None)
        if collision_tower is not None:
            self.dx = 0
            self.dy = 0
            return collision_tower
        collision_knight = pygame.sprite.spritecollideany(self, board.knights, collided=None)
        if collision_knight is not None:
            self.dx = 0
            self.dy = 0
            return collision_knight
        return None

    def touching_another_enemy(self, board): # finds if the enemy is hitting another enemy, tries to escape
        sprite_group_without_self = board.enemies.copy()
        sprite_group_without_self.remove(self)

        collision = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None) # checks if it collides with other knights
        if collision is not None or (self.dx,self.dy) == (0,0):
            collision = True
            # picks from 8 different directions in a certain range to find the closest possible movement that lets it escape collision
            for escape_speed_multiplier in range(1,20):
                directions = [(0,escape_speed_multiplier*int(self.speed_level*-0.5)),(escape_speed_multiplier*int(self.speed_level*0.5),0),
                              (0,escape_speed_multiplier*int(self.speed_level*0.5)),(escape_speed_multiplier*int(self.speed_level*-0.5),0),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*-0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*-0.5))]
                random.shuffle(directions) # randomises the directions that are attempted for escape

                for (dx,dy) in directions: # tests moving in the direction chosen
                    self.rect = self.rect.move(dx,dy)
                    collision_in_new_path = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None)
                    if collision_in_new_path is None: # if there is no collision in the direction chosen
                        self.rect = self.rect.move(-dx,-dy) # move back to original position, to be moved later on
                        (self.dx,self.dy) = (dx,dy) # define new direction which will avoid collision
                        break

                    self.rect = self.rect.move(-dx,-dy) # if the direction chosen also has a collision, move back to original position

                if collision_in_new_path is None: # breaks out of the outer loop if a suitable direction is found
                    break

            if collision_in_new_path is not None: # if there is no movement within 20 pixels that produces no collision, stays at rest
                (self.dx,self.dy) = (0,0)

        return collision

    def update(self): # moves the enemy
        self.rect = self.rect.move(self.dx,self.dy)
        self.position = self.rect.center

class Dragons(Game_obj): # enemy type which can fly over knights and ground enemies and only attacks towers
    def __init__(self, board, time, position, obj_type, init_HP, level, attack_power, money_earned_per_enemy):
        super(Dragons,self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.orientation = (0.0, 1.0) #points down initially
        self.speed_level = 2*2*level #Dragons are twice as fast as other enemies
        self.dx = 0
        self.dy = 0
        self.point_at_tower(board)
        self.money_earned_per_enemy = money_earned_per_enemy
        self.living = True

    def point_at_tower(self, board): # finds the closest defense tower and moves to it
        tower = self.closest_tower() # finds closest defese tower
        if tower is not None:
            direction = (float(tower.position[0] - self.position[0]), float(tower.position[1] - self.position[1]))
            distance = calc_distance(self.position, tower.position)
            new_orientation = (direction[0]/distance, direction[1]/distance)
            # rotates dragon based on direction of motion
            rotate_angle = angle(new_orientation, self.orientation)
            if rotate_angle > 3:
                if rotate_angle >=90 and rotate_angle <180:
                    if new_orientation[0] <0 :
                        self.image = pygame.transform.rotate(self.image,180-rotate_angle)
                    else:
                        self.image = pygame.transform.rotate(self.image,-180+rotate_angle)
                elif rotate_angle >=0 and rotate_angle < 90:
                    if new_orientation[0] <0 :
                        self.image = pygame.transform.rotate(self.image,180-rotate_angle)
                    else:
                        self.image = pygame.transform.rotate(self.image,-180+rotate_angle)
            self.dx = int(self.speed_level*(new_orientation[0]))
            self.dy = int(self.speed_level*(new_orientation[1]))
            self.orientation = new_orientation

    def closest_tower(self): # finds closest defense tower, if none exists, attacks main tower
        final_tower = None
        closest_distance = MAP_SIZE[1]
        for tower in self.board.towers:
            if tower == self.board.base_tower:
                continue
            distance = calc_distance(self.position, tower.position)
            if distance < closest_distance:
                closest_distance = distance
                final_tower = tower
        if final_tower != None:
            return final_tower
        else:
            return self.board.base_tower

    def attack(self, collision, board): # attacks tower with which it is colliding
        collision.HP -= self.attack_power
        if collision.HP <= 0: # if tower HP = 0 kills tower
            collision.death(board)

    def death(self, board): # removes the dragon if it dies
        # used to associate dragon with corresponding lifebar
        time = self.time
        self.living = False
        lifebar = board.lifebar_dict[time]
        # removes the dragon and lifebar from dictionaries
        board.dragon_dict[time] = None
        board.lifebar_dict[time] = None
        # removes dragon and lifebar from sprite groups they are in
        lifebar.kill()
        self.kill()
        return self.money_earned_per_enemy
        
    def touching_defense_or_base_tower(self, board): # checks if dragon has collided with tower
        collision_tower = pygame.sprite.spritecollideany(self, board.towers, collided=None)
        if collision_tower is not None:
            self.dx = 0
            self.dy = 0
            return collision_tower
        return None

    def touching_another_dragon(self, board): # finds if dragon is hitting another dragon, tries to escape if true
        sprite_group_without_self = board.dragons.copy()
        sprite_group_without_self.remove(self)

        collision = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None) # checks if it collides with other knights
        if collision is not None or (self.dx,self.dy) == (0,0):
            collision = True
            # picks from 8 different directions in a certain range to find the closest possible movement that lets it escape collision
            for escape_speed_multiplier in range(1,20):
                directions = [(0,escape_speed_multiplier*int(self.speed_level*-0.5)),(escape_speed_multiplier*int(self.speed_level*0.5),0),
                              (0,escape_speed_multiplier*int(self.speed_level*0.5)),(escape_speed_multiplier*int(self.speed_level*-0.5),0),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*-0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*-0.5))]
                random.shuffle(directions) # randomises the directions that are attempted for escape

                for (dx,dy) in directions: # tests moving in the direction chosen
                    self.rect = self.rect.move(dx,dy)
                    collision_in_new_path = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None)
                    if collision_in_new_path is None: # if there is no collision in the direction chosen
                        self.rect = self.rect.move(-dx,-dy) # move back to original position, to be moved later on
                        (self.dx,self.dy) = (dx,dy) # define new direction which will avoid collision
                        break

                    self.rect = self.rect.move(-dx,-dy) # if the direction chosen also has a collision, move back to original position

                if collision_in_new_path is None: # breaks out of the outer loop if a suitable direction is found
                    break

            if collision_in_new_path is not None: # if there is no movement within 20 pixels that produces no collision, stays at rest
                (self.dx,self.dy) = (0,0)

        return collision

    def update(self): # moves dragon
        self.rect = self.rect.move(self.dx,self.dy)
        self.position = self.rect.center
        
class User_Score(object): # creates an object to efficiently keep track of username and score
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return '{}: {}'.format(self.name, self.score)
        
start_game() # starts the game!
