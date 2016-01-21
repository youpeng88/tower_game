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
import PygButton
from example_menu import main as menu
from difficulty_menu import main as level_menu
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
#   screen_resolution = pygame.display.Info()
    # sets up the menu screen
    Start_screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    pygame.display.set_caption("Menu") # caption sets title of Window
    Start_screen.fill(black) 
    pygame.display.flip()
    if results is None:
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
    try:
        extension = os_type[0]
        print extension
    except IndexError:
        results = 3 # if no platform option, prompts to the platform choice menu

    if results is None: # This means user selected start game
        Start_screen.fill(black)
        pygame.display.set_caption("Difficulty Level")
        level = level_menu(Start_screen)
        return level      
    elif results == 2: # user selected LOAD game
        with open('saved_state.txt','r') as f:
            saved_state = f.readlines() # need to pass this into the game to update the state
            while True:
                try:
                    test = saved_state[5]
                    new_game(saved_state,highscore_archive_list, extension, level=1)
                    return None
                except IndexError:
                    break
        return 4
    
    elif results == 3: # user selected to specify operating system
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
        # click anywhere on the screen to go back to main menu
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
        # click anywhere on the screen to go back to main menu
        while pygame.MOUSEBUTTONDOWN not in event_types and pygame.KEYDOWN not in event_types:
            display_instructions(Start_screen)
            events = pygame.event.get()
            event_types = [event.type for event in events]
        return 4

# function to generate a new game start with menu
def start_game():
    # call start menu 
    level = start_menu(None)
    while level != None: # back is selected on the menu
        if level == 4:
            level = start_menu(None) # go back to main menu page
        else: # start new game selected with a difficulty level
            #load high score
            f = open('highscores.txt','r')
            highscore_archive = f.readlines()
            highscore_archive_list = convert_score_list(highscore_archive)
            # load platform option
            g = open('platform.txt','r')
            os_type = g.readlines()
            while True:
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
    location = 1
    fontsize = 22
    Tower_Placement = "How to play: Click anywhere on the map area to add defense towers"
    Enemy_waves = "How enemies move: they come out in batches randomly from the border of the map"
    Enemy_kill = "How enemies kill: they only kill when they are next to the tower"   
    Game_money = "How to earn gold: kill enemies to earn gold and spend gold to build towers"
    Game_win = "How to win: kill as many enemies as possible to achieve higher score"
    
    Enemy_grow = "Watch out! Enemies come out later with more HP and more killing power"

    inputask.update_text(screen, "Instructions" , location,30)
    inputask.update_text(screen,  Tower_Placement, location+2, fontsize)
    inputask.update_text(screen,  Enemy_waves, location+4, fontsize)
    inputask.update_text(screen,  Enemy_kill, location+6, fontsize) 
    inputask.update_text(screen,  Game_money, location+8, fontsize)
    inputask.update_text(screen,  Game_win, location+10, fontsize)
    inputask.update_text(screen,  "Have Fun!!!!! But....", location+12, fontsize)
    inputask.update_text(screen,  Enemy_grow, location+14, fontsize)

    pass

# function used to display game highscore
def display_high_score(screen, highscore_list):
    location = 2
    inputask.update_text(screen, "High Scores", location-1, 30)
    for user in highscore_list:
        location +=1
        #message = user[]
        inputask.update_text(screen, "Top " + str(location-2) +" : "+user.name + ",  "+ str(user.score) , location,22)  
 
# function used to generate high score list using user_score objects       
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
    money_v = [5000, 4000, 2500]
    
    # checks if previoius game stats are saved properly(?)
    if saved_stats is not None:
        while True:
            try:
                tower_number = int(saved_stats[0])
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
        username = saved_stats[6][1:len(saved_stats[6])-1]
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
                                    
    # if not loading an old game, starts a new game based on difficulty level
    else:
        tower_number = 1
        knight_number = 0
        wavecount = 0
        tower_list = None
        enemy_list = None
        knight_list = None
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
    speed_level = [1,2,3]
    defense_range = [200, 150, 100]
    attack_power_tower = [50, 75, 100]
    attack_power_enemy = [5,5,5]
    attack_power_knight = [10,10,10]
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
                          HP_knight[difficulty-1]]
    
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
    pygame.display.flip()

    # set default button click/defense type to tower
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
    
             #Updated Action 2 and 5 (move)
             num_border_locs = len(border)
             num_enemies = 2
             if loop_number - loop_created > 10:
                 enemies_count = 0
                 while enemies_count < num_enemies:
                     index = random.randint(0,num_border_locs-1)
                     x,y = border[index]
                     time = pygame.time.get_ticks()
                     board.add_enemy_to_board(time, (x,y),speed_level, HP_enemy, attack_power_enemy,money_earned_per_enemy)
                     enemies_count +=1
                 loop_created = loop_number
                 wavecount +=1
            # Increase enemy HP by 10 and amount of money earned by 5 every 10 waves 
                 if wavecount % 10 == 0: 
                     HP_enemy += 10
                     money_earned_per_enemy += 5                 
             
             # action 3: defense attacks enemy (shoot)
             for tower in board.towers:
                 tower.attack()

             # knight attacks enemy (contact)
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

             # action 4: enemy attack defense and base tower
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

            # shoot cannonballs at enemies
             for cannonball in board.cannonballs:
                money_earned = cannonball.attack(board)
                if money_earned:
                    score += money_earned*difficulty
                    money += money_earned


            # update sidebar, towers, enemies, knights and all other sprite objects
             sidebar.display_text(tower_number,knight_number, money, wavecount,difficulty,score)
             sidebar.display_button()
             
             screen.blit(BackGround.image, BackGround.rect)

             board.towers.update()
             board.enemies.update()
             board.lifebars.update()
             board.knights.update()
             board.cannonballs.update()

             board.cannonballs.draw(screen)
             board.towers.draw(screen)
             board.enemies.draw(screen)
             board.knights.draw(screen)
             
             # display
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
                pygame.time.wait(3000)
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
    
        with open('highscores.txt','w') as f:
            for user in range(len(highscores)):
                f.write(str(highscores[user].name)+"+"+str(highscores[user].score) + "\n")
            f.close()

    # goes back to main menu when mainloop = False
    start_game()
    
class Background(pygame.sprite.Sprite):
    def __init__(self, obj_type, position):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(IMAGE_DICT[obj_type][0])
        self.image = pygame.transform.scale(self.image, IMAGE_DICT[obj_type][1])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        
class siderbar():
    def __init__(self,screen):
        self.screen = screen
        self.button_list = {}
    
    def update_text(self, message, location,obj_type):
        """
        Used to display the text on the right-hand part of the screen.
        location will be used to decide what variable to display: tower number, money, wave
        """
        textSize = 20
        font = pygame.font.Font(None, 20)
        texty = 0 + textSize*6
        text = font.render(message, True, white, black)
        textRect = text.get_rect()
        textRect.centery = MARGIN + texty*(location-1)
        textRect.centerx = SCREEN_SIZE[0] - BAR_SIZE[0]/2
        self.screen.blit(text, textRect)
        icon = Background(obj_type, [textRect.x - 20, textRect.y])
        self.screen.blit(icon.image, icon.rect) 
    
    def add_button(self, obj_type1, obj_type2, location):
        button_rect = pygame.Rect(SCREEN_SIZE[0]-BAR_SIZE[0]*3/4+70*location[0],MARGIN + 30*location[1], BAR_SIZE[0]/5, 40)
        my_Button = PygButton.PygButton(button_rect,'lala',bgcolor=white,fgcolor=red)
        my_Button.setSurfaces(IMAGE_DICT[obj_type1][0],IMAGE_DICT[obj_type2][0],IMAGE_DICT[obj_type1][0]) # set tower picture as button        
        self.button_list[obj_type1] = my_Button
        
    def update_button(self,event):
        for my_Button in self.button_list.values():
            my_Button.handleEvent(event)
    
    def display_button(self):
        for my_Button in self.button_list.values():
            my_Button._visible = True
            my_Button.draw(self.screen)
    
    def display_text(self, tower_number,knight_number, money, wavecount,level,score):
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


class Board:
    def __init__(self, HP_base,screen,defense_range, attack_power):

        self.screen = screen
        
        # Initialize the base Tower
        init_x = MARGIN+MAP_SIZE[0]/2
        init_y = MARGIN+MAP_SIZE[1]/2
        time = 0
        
        self.base_tower = Tower(self, time, (init_x, init_y), "base_tower", HP_base, defense_range, attack_power, 0)
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

        # Create knight dict and Sprite group
        self.knight_dict = {}
        self.knights = pygame.sprite.Group()

        # Create cannonball dict and Sprite group
        self.cannonball_dict = {}
        self.cannonballs = pygame.sprite.Group()

    def add_tower_to_board(self, time, position, HP_tower,defense_range, attack_power, tower_reload_time):
        defense_tower = Tower(self, time, position, "defense_tower", HP_tower, defense_range, attack_power, tower_reload_time)
        if defense_tower.rect.x < MARGIN or defense_tower.rect.topright[0] > MARGIN + MAP_SIZE[0] or defense_tower.rect.y < MARGIN or defense_tower.rect.bottomleft[1] > MARGIN + MAP_SIZE[1]:
            return False
        else:
            collision_tower = pygame.sprite.spritecollideany(defense_tower, self.towers, None)
            collision_enemy = pygame.sprite.spritecollideany(defense_tower, self.enemies, None)
            collision_knight = pygame.sprite.spritecollideany(defense_tower, self.knights, None)
            if collision_tower is None and collision_enemy is None and collision_knight is None:
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
        collision_knight = pygame.sprite.spritecollideany(enemy, self.knights, None)
        if collision_tower is None and collision_enemy is None and collision_knight is None:
            self.enemy_dict[time] = enemy
            self.enemies.add(enemy)
            enemy_lifebar = Lifebar(self, time, enemy, self.screen, HP_enemy)

            # Add defense tower lifebar to lifebar dict and Sprite group
            self.lifebar_dict[time] = enemy_lifebar
            self.lifebars.add(enemy_lifebar)

    def add_knight_to_board(self, time, position, HP_knight, attack_power):
        knight = Knight(self, time, position, "knight", HP_knight, attack_power)
        if knight.rect.x < MARGIN or knight.rect.topright[0] > MARGIN + MAP_SIZE[0] or knight.rect.y < MARGIN or knight.rect.bottomleft[1] > MARGIN + MAP_SIZE[1]:
            return False
        else:
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

    def add_cannonball_to_board(self, time, position, HP_cannonball, attack_power, tower):
        cannonball = Cannonball(self, time, position, "cannonball", HP_cannonball, attack_power, tower)
        self.cannonball_dict[time] = cannonball
        self.cannonballs.add(cannonball)


    # def draw_laser_line(self, enemy_position, tower_position):
    #     # draws normal solid line
    #     pygame.draw.line(self.screen, black, tower_position, enemy_position, 2)
    #
    #     # if we want to draw dashed line
    #     #draw_dash(self.screen, black, tower_position, enemy_position, dash_length = 5)
    #     # draw_dash2(self.screen, red, tower_position, enemy_position, width = 2, dash_length = 5)
       
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
    def __init__(self, board, time, position, obj_type, init_HP, defense_range, attack_power, reload_time):
        super(Tower, self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.defense_range = defense_range
        self.previous_time = 0
        self.reload_time = reload_time
    
    def attack(self):
        attack_enemy = self.closest_enemy()
        time = pygame.time.get_ticks()
        passed_time = time - self.previous_time
        if passed_time > self.reload_time:
            if attack_enemy != None:
                self.board.add_cannonball_to_board(time, self.position, 10, self.attack_power, self)
                self.previous_time = time

    def death(self, board):
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


class Cannonball(Game_obj):
    def __init__(self, board, time, position, obj_type, init_HP, attack_power, tower):
        super(Cannonball,self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.tower = tower
        self.closest_enemy = tower.closest_enemy()
        self.previous_enemy = self.closest_enemy
        self.speed_level = 10
        self.orientation = (0.0, 1.0) #points up initially
        self.dx = 0
        self.dy = 0
        self.point_at_enemy(board)

    def attack(self, board):
        collision = self.touching_enemy(board)
        if self.rect.x < MARGIN or self.rect.topright[0] > MARGIN + MAP_SIZE[0] or self.rect.y < MARGIN or self.rect.bottomleft[1] > MARGIN + MAP_SIZE[1]:
                self.death(board)
        elif collision is not None:
            collision.HP -= self.attack_power
            self.death(board)
            if collision.HP <= 0:
                return collision.death(board)
        elif self.dx == 0 and self.dy == 0:
            self.death(board)
        elif calc_distance(self.position, self.tower.position) > self.tower.defense_range:
            self.death(board)
        elif self.closest_enemy.living == False:
            pass
        else:
            self.point_at_enemy(board)
        return False

    def point_at_enemy(self, board): # moving direction
        enemy = self.closest_enemy
        if enemy is not None:
            direction = (float(enemy.position[0] - self.position[0]), float(enemy.position[1] - self.position[1]))
            distance = calc_distance(self.position, enemy.position)
            if distance != 0:
                new_orientation = (direction[0]/distance, direction[1]/distance)
                self.dx = int(self.speed_level*(new_orientation[0]))
                self.dy = int(self.speed_level*(new_orientation[1]))
                self.orientation = new_orientation
            else:
                self.dx = 0
                self.dy = 0

    def touching_enemy(self, board):
        collision = pygame.sprite.spritecollideany(self, board.enemies, collided=None)
        if collision is not None:
            return collision
        else:
            return None

    def death(self, board):
        time = self.time
        board.cannonball_dict[time] = None
        self.kill()
        self.update()

    def update(self):
        self.rect = self.rect.move(self.dx,self.dy)
        self.position = self.rect.center

class Knight(Game_obj):
    def __init__(self, board, time, position, obj_type, init_HP, attack_power):
        super(Knight,self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.orientation = (0.0, 1.0) #points up initially
        self.speed_level = 2
        self.dx = 0
        self.dy = 0
        self.point_at_enemy(board)

    def point_at_enemy(self, board): # moving direction
        enemy = self.closest_enemy()
        if enemy is not None:
            direction = (float(enemy.position[0] - self.position[0]), float(enemy.position[1] - self.position[1]))
            distance = calc_distance(self.position, enemy.position)
            new_orientation = (direction[0]/distance, direction[1]/distance)
            # knights have to rotate too much
            # rotate_angle = angle(new_orientation, self.orientation)
            # if rotate_angle > 1:
            #     self.image = pygame.transform.rotate(self.image, rotate_angle)
            self.dx = int(self.speed_level*(new_orientation[0]))
            self.dy = int(self.speed_level*(new_orientation[1]))
            self.orientation = new_orientation

    def closest_enemy(self):
        e_position = None
        final_enemy = None
        closest_distance = MAP_SIZE[1]
        for enemy in self.board.enemies:
            distance = calc_distance(self.position, enemy.position)
            if distance < closest_distance:
                closest_distance = distance
                e_position = enemy.position
                final_enemy = enemy
        if e_position != None:
            return final_enemy
        return False

    def attack(self, collision, board):
        collision.HP -= self.attack_power
        if collision.HP <= 0:
            return collision.death(board)
        return None

    def death(self, board):
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
        return True

    def touching_enemy(self, board):
        collision = pygame.sprite.spritecollideany(self, board.enemies, collided=None)
        if collision is not None:
            self.dx = 0
            self.dy = 0
        return collision


    def touching_another_knight_or_tower(self, board):        
        sprite_group_without_self = board.knights.copy()
        
        sprite_group_without_self.remove(self)
        collision = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None)

        if collision is not None or (self.dx,self.dy) == (0,0):

            collision = True

            for escape_speed_multiplier in range(1,20):
                
                directions = [(0,escape_speed_multiplier*int(self.speed_level*-0.5)),(escape_speed_multiplier*int(self.speed_level*0.5),0),
                              (0,escape_speed_multiplier*int(self.speed_level*0.5)),(escape_speed_multiplier*int(self.speed_level*-0.5),0),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*-0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*-0.5))]

                random.shuffle(directions)

                for (dx,dy) in directions:

                    self.rect = self.rect.move(dx,dy)

                    collision_in_new_path = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None)

                    if collision_in_new_path is None:
                        self.rect = self.rect.move(-dx,-dy)
                        (self.dx,self.dy) = (dx,dy)
                        break

                    self.rect = self.rect.move(-dx,-dy)

                if collision_in_new_path is None:
                    break

            if collision_in_new_path is not None:
                (self.dx,self.dy) = (0,0)

        return collision

    def update(self):
        # add in angles from find direction to base tower
#        self.rect.x += self.dx
#        self.rect.y += self.dy
        self.rect = self.rect.move(self.dx,self.dy)
        self.position = self.rect.center

class Enemies(Game_obj):
    def __init__(self, board, time, position, obj_type, init_HP, level, attack_power, money_earned_per_enemy):
        super(Enemies,self).__init__(board, time, position, obj_type, init_HP, attack_power)
        self.orientation = (0.0, 1.0) #points up initially
        self.speed_level = 2*level
        self.dx = 0
        self.dy = 0
        self.point_at_base(board)
        self.money_earned_per_enemy = money_earned_per_enemy
        self.living = True

    def point_at_base(self, board): # moving direction
        direction = (float(board.base_tower.position[0] - self.position[0]), float(board.base_tower.position[1] - self.position[1]))
        distance = calc_distance(self.position, board.base_tower.position)
        new_orientation = (direction[0]/distance, direction[1]/distance)
        rotate_angle = angle(new_orientation, self.orientation)
#        print "angle: ", rotate_angle
        if rotate_angle > 5:
            self.image = pygame.transform.rotate(self.image, rotate_angle)
        self.dx = int(self.speed_level*(new_orientation[0]))
        self.dy = int(self.speed_level*(new_orientation[1]))
        self.orientation = new_orientation
        
    def set_new_speed(self,new_level):
        self.speed_level = 1*new_level

    def attack(self, collision, board):
        collision.HP -= self.attack_power
        if collision.HP <= 0:
            collision.death(board)

    def death(self, board):
        # need to remove the object from the board
        # from dic list
        time = self.time
        self.living = False
        board.enemy_dict[time] = None
        lifebar = board.lifebar_dict[time]
        lifebar.kill()
        board.lifebar_dict[time] = None
        self.kill()
        self.update()
        lifebar.update()
        return self.money_earned_per_enemy
        
    def touching_defense_or_base_tower_or_knight(self, board):
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

    def touching_another_enemy(self, board):
        sprite_group_without_self = board.enemies.copy()
        
        sprite_group_without_self.remove(self)
        collision = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None)

        if collision is not None or (self.dx,self.dy) == (0,0):

            collision = True

            for escape_speed_multiplier in range(1,20):
                
                directions = [(0,escape_speed_multiplier*int(self.speed_level*-0.5)),(escape_speed_multiplier*int(self.speed_level*0.5),0),
                              (0,escape_speed_multiplier*int(self.speed_level*0.5)),(escape_speed_multiplier*int(self.speed_level*-0.5),0),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*-0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*-0.5),escape_speed_multiplier*int(self.speed_level*0.5)),
                              (escape_speed_multiplier*int(self.speed_level*0.5),escape_speed_multiplier*int(self.speed_level*-0.5))]

                random.shuffle(directions)

                for (dx,dy) in directions:

                    self.rect = self.rect.move(dx,dy)

                    collision_in_new_path = pygame.sprite.spritecollideany(self, sprite_group_without_self, collided=None)

                    if collision_in_new_path is None:
                        self.rect = self.rect.move(-dx,-dy)
                        (self.dx,self.dy) = (dx,dy)
                        break

                    self.rect = self.rect.move(-dx,-dy)

                if collision_in_new_path is None:
                    break

                if collision_in_new_path is not None:
                    (self.dx,self.dy) = (0,0)

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
        
    
start_game()
