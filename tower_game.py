# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:39:30 2016

@author: pengyou
"""

import pygame
import os
import random

### Global Variables
WIDTH = 20 # this is the width of an individual square
HEIGHT = 20 # this is the height of an individual square


# RGB color definition 
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

# Board size
board_size = (30,30) #(rows,cols)

def get_row_top_loc(rowNum, height = HEIGHT):
    """
    Returns the location of the top pixel in a square in
    row rowNum, given the row height.
    """
    loc_top_pixel = 10 + (rowNum-1)*height
    return loc_top_pixel
    #pass

def get_col_left_loc(colNum, width = WIDTH):
    """
    Returns the location of the leftmost pixel in a square in
    column colNum, given the column width.
    """
    loc_left_pixel = 10 + (colNum-1)*width
    return loc_left_pixel    
    #pass

def get_row_column_number(x,y, width = WIDTH, height = HEIGHT):
    rowNum = (y-10)/width + 1
    colNum = (x-10)/height + 1
    
    return (rowNum, colNum)        

def update_text(screen, message, location, size = board_size):
    """
    Used to display the text on the right-hand part of the screen.
    location will be used to decide what variable to display: tower number, money, wave
    """
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 0 + textSize
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.centerx = (size[1] + 4) * WIDTH + 10
    textRect.centery = textY*location
    screen.blit(text, textRect)

def sidebar(screen, tower_number, money, wavecount,board_size):
    update_text(screen, "Tower #: " + str(tower_number), 1, board_size)
    update_text(screen, "Money: " + str(money), 2, board_size)
    update_text(screen, "Wave #: " + str(wavecount), 3, board_size)
    pass

def new_game(size = board_size):
    """
    Sets up all necessary components to start a new game
    of power tower.
    """
    pygame.init() # initialize all imported pygame modules

    window_size = [size[1] * WIDTH + 200, size[0] * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Tower Power") # caption sets title of Window 

    screen.fill(black) # (0,0,0) represents RGB for black

    pygame.display.flip()
    
    board = Board(size,screen)
    
    # starting variables
    HP_enemy = 100
    HP_tower = 500
    speed_level = 1
    tower_number = 1
    wavecount = 0
    money = 5000
    
    starting_varaibles = [HP_enemy, HP_tower, speed_level, tower_number, wavecount, money]

    clock = pygame.time.Clock()

    main_loop(screen, board, starting_varaibles, clock)

def main_loop(screen, board, starting_varaibles, clock):
#    background = pygame.Surface((screen.get_width(), screen.get_height()))
#    backgroun.fill(black)
    HP_enemy = starting_varaibles[0]
    HP_tower = starting_varaibles[1]
    speed_level = starting_varaibles[2]
    tower_number = starting_varaibles[3]
    wavecount = starting_varaibles[4]
    money = starting_varaibles[5]
    
    board.squares.draw(screen) # draw Sprites (Squares)
    board.towers.draw(screen) # draw tower Sprite
    pygame.display.flip()
    
    events = pygame.event.get()
    event_types = [event.type for event in events]
    while pygame.QUIT not in event_types: # when use didn't click exit on the window           
            milliseconds = clock.tick_busy_loop()  # milliseconds passed since last frame
            seconds = milliseconds/1000.0
            
            # call sidebar
            pygame.display.flip()
            # bring waves of enemies
            frequency = 1000 # in milliseconds
            num_enemies = 1 # number of enemies generated per wave
            pygame.time.set_timer(pygame.USEREVENT + 1, frequency)
            
            # action 1: add tower
            if pygame.mouse.get_pressed()[0]: 
                x,y = pygame.mouse.get_pos()
                #row,col = get_row_column_number(x,y, WIDTH, HEIGHT)
                # add a defense tower at the location clicked
                if board.add_tower_to_board(y,x, HP_tower):
                    board.towers.draw(screen)
                    pygame.display.flip()
                    money -= 500
                    tower_number +=1
                    
            # action 2: add enemies per wave frequecy
            if pygame.USEREVENT + 1 in event_types:
                # add enemies to board
                enemies_count = 0
                while enemies_count < num_enemies:
                    row = random.randint(11,10+(board_size[1]-1)*WIDTH) 
                    col = random.randint(11,10+(board_size[0]-1)*HEIGHT)
                    if board.add_enemy_to_board(row,col,speed_level, HP_enemy):
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
    

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.image.load('brick_wall_blank1.bmp')
        #self.image = pygame.transform.chop(self.image, (60, 0, 32, 32))
        self.image = pygame.transform.scale(self.image,(WIDTH,HEIGHT))
        self.rect = self.image.get_rect() # gets a rect object with width and height specified above
                                            # a rect is a pygame object for handling rectangles
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)   

    def get_rect_from_square(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect
        #pass
    
class Board:
    def __init__(self, size, screen):
        self.size = size
        self.screen = screen
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = {}
    
        #---Populate boardSquares with Squares---#
        for i in range(1,size[0]+1):
            for j in range(1,size[1]+1):
                s = Square(i,j) # create a square object
                self.boardSquares[(i,j)] = s # add square to the data structure
                self.squares.add(s)           
        #pass

        #---Initialize the base Tower---#
        starting_col = 10+HEIGHT*size[1]/2;
        starting_row = 10+WIDTH*size[0]/2;
        self.base_tower = Tower(self, starting_col, starting_row, HP_tower)
        
        # -- Initialize the tower dic---#
        self.tower = {}
        self.tower[(starting_col, starting_row)]=self.base_tower
        
                          
        #---Adds Tower to the "towers" Sprite List---#
        self.towers = pygame.sprite.Group()
        self.towers.add(self.base_tower)
                
        # Create life bar Sprite group
        self.lifebars = pygame.sprite.Group()
        
        # Create enemy sprite group and initialize the enemy dic
        self.enemy_group = {}
        self.enemies = pygame.sprite.LayeredUpdates() # same as group() but you can use update function
    
    def add_tower_to_board(self,row,col,HP_tower):
        defense_tower = Defense_tower(self,col,row, HP_tower)
        collison = pygame.sprite.spritecollideany(defense_tower,self.towers, None)
        if collison == None:
            self.defense_tower[(row,col)]=defense_tower
            self.towers.add(defense_tower)
            return True
        else:
            return False
    
    def add_enemy_to_board(self,row,col,speed_level,HP_enemy):
        enemy = Enemies(self,col,row,speed_level,HP_enemy)
        collison = pygame.sprite.spritecollideany(enemy,self.enemies, None)
        if collison == None:
            self.enemy_group[(row,col)]=enemy
            self.enemies.add(enemy)
            return True
        else:
            return False
    
    def draw_laser_line(self,enemy_position,tower_position):
        pass

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
    def __init__(self, board,col,row, HP):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.rect = pygame.Surface([WIDTH, HEIGHT]).get_rect()
        self.rect.x = col
        self.rect.y = row
        #self.set_orientation()
        self.board = board
        self.HP = HP
        
class Tower(Game_obj):
    def __init__(self, board,col,row,HP):
        super(Tower,self).__init__(board,col,row,HP)
        self.set_pic()
        self.rect = self.image.get_rect()
        self.rect.x = col
        self.rect.y = row        
        
    def set_pic(self):
        self.image = pygame.image.load("base_tower.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image,(WIDTH,2*HEIGHT))
        
    def decrease_HP(self,decreased_HP):
        self.HP -= decreased_HP
        if self.HP < 0:
            self.kill()
    
    def kill(self):
        # need to remove the object from the board
        # from dic list
        self.board.tower[(self.rect.x,self.rect.y)] = None
        # from sprite group
        # NOT FINISHED
        pass
       
class Defense_tower(Tower):
    def __init__(self,board,col,row, HP):
        super(Defense_tower,self).__init__(board,col,row,HP)
        self.set_pic()
        self.collison = False
                
    def set_pic(self):
        self.image = pygame.image.load("defense_tower.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image,(WIDTH,HEIGHT))
        
    def closest_enemy(self):
        pass
    
class Enemies(Game_obj):
    def __init__(self,board,col,row,level,HP):
        super(Enemies,self).__init__(board,col,row)
        # here row and col will be its starting location
        self.set_pic()
        self.speed_level = 1*level
        
        self.set_direction()
       
    def set_direction(self): # moving direction
        rand_orient_x = random.choice([-1,1]) # generate random orientation
        rand_orient_y = random.choice([-1,1])        
        self.dx = self.speed_level*rand_orient_x
        self.dy = self.speed_level*rand_orient_y
                
    def set_pic(self):
        self.image = pygame.image.load("enemy.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image,(WIDTH,HEIGHT))
    
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