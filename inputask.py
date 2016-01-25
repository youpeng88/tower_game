# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 10:42:07 2016
# Adapted by You Peng from 
# Timothy Downs, inputbox written for my map editor
# new function added by You Peng:
# display and update_text

"""


# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font("freesansbold.ttf",24)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 300,
                    (screen.get_height() / 2),
                    700, 44), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 302,
                    (screen.get_height() / 2) - 2,
                    700,44), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 300, (screen.get_height() / 2)))
  pygame.display.flip()
  
def display(screen, message):
  "Print a message n the middle of the screen"
  fontobject = pygame.font.Font("freesansbold.ttf",30)
  if len(message) != 0:
      screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 300, screen.get_height() / 2))
  pygame.display.flip()
  
def update_text(screen, message, location, fontsize):
    """
    Used to display the text on the right-hand part of the screen.
    location will be used to decide what variable to display: tower number, money, wave
    """
    textSize = 40
    font = pygame.font.Font("freesansbold.ttf", fontsize)
    texty = 0 + textSize
    text = font.render(message, True, (255,255,255), (0,0,0))
    textRect = text.get_rect()
    textRect.centery = screen.get_height()/5 + location*texty
    textRect.centerx = (screen.get_width() / 2)
    screen.blit(text, textRect)
    pygame.display.flip()


def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + string.join(current_string,""))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + string.join(current_string,""))
  return string.join(current_string,"")