# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:39:30 2016

@author: pengyou
"""

import pygame
import os

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
    
    tower_number = 1

    wavecount = 0
    
    money = 5000

    clock = pygame.time.Clock()

    main_loop(screen, board, tower_number, wavecount, money, clock)

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

        #---Initialize the Tower---#
        starting_col = size[1]/2;
        starting_row = size[0]/2;
        self.base_tower = Base_tower(self, starting_col, starting_row, self.screen)
        self.defense_tower = {}
        
                          
        #---Adds Tower to the "game_obj" Sprite List---#
        self.game_obj = pygame.sprite.Group()
        self.game_obj.add(self.base_tower)
        
    
    def add_tower_to_board(self,row,col):
        if (row,col) in self.defense_tower:
            return False
        else:
            defense_tower = Defense_tower(self,col,row, self.screen)
            self.defense_tower[(row,col)]=defense_tower
            self.game_obj.add(defense_tower)
            return True

class Game_obj(pygame.sprite.Sprite):
    def __init__(self, board,col,row):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.rect = pygame.Surface([WIDTH, HEIGHT]).get_rect()
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        #self.set_orientation()
        self.board = board
        
class Base_tower(Game_obj):
    def __init__(self, board,col,row, screen):
        super(Base_tower,self).__init__(board,col,row)
        self.screen = screen
        self.set_pic()
        
        
    def set_pic(self):
        self.image = pygame.image.load("base_tower.bmp").convert_alpha(self.screen)
        self.image = pygame.transform.scale(self.image,(WIDTH,2*HEIGHT))
       
class Defense_tower(Game_obj):
    def __init__(self,board,col,row,screen):
        super(Defense_tower,self).__init__(board,col,row)
        self.screen = screen
        self.set_pic()
                
    def set_pic(self):
        self.image = pygame.image.load("defense_tower.bmp").convert_alpha(self.screen)
        self.image = pygame.transform.scale(self.image,(WIDTH,HEIGHT))

class Enemies(Game_obj):
    def __init__(self,board,col,row):
        super(Enemies,self).__init__(board,col,row)
        self.set_pic()

       
def main_loop(screen, board, tower_number, wavecount, money, clock):
    board.squares.draw(screen) # draw Sprites (Squares)
    board.game_obj.draw(screen) # draw tower Sprite
    pygame.display.flip()
    
    events = pygame.event.get()
    event_types = [event.type for event in events]
    while pygame.QUIT not in event_types: # when use didn't click exit on the window
            update_text(screen, "Tower #: " + str(tower_number), 1, board.size)
            update_text(screen, "Money: " + str(money), 2, board.size)
            update_text(screen, "Wave #: " + str(wavecount), 3, board.size)
            pygame.display.flip()
            if pygame.MOUSEBUTTONDOWN in event_types: 
                x,y = events[0].pos
                row,col = get_row_column_number(x,y, WIDTH, HEIGHT)
                # add a defense tower at the location clicked
                if board.add_tower_to_board(row,col):
                    board.game_obj.draw(screen)
                    pygame.display.flip()
                    money -= 500
                    tower_number +=1
            events = pygame.event.get()
            event_types = [event.type for event in events] # update event list
    pass
    
new_game()