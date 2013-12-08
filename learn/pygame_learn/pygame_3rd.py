#!/usr/bin/python

#Target: create internal 'area map' of empty block, display it, on mouse click install/remove object. Update only changed region of the screen (no global .update or .flip)
import pygame
import time

class AreaMap:
    def __init__(self,size,empty_image,filled_image):
        self.empty=pygame.image.load(empty_image).convert()
        self.fill=pygame.image.load(filled_image).convert()
        

if name == '__main__':
    pygame.init()
    clock=pygame.time.Clock()
    disp=pygame.display.set_mode(SCREEN_SIZE,pygame.DOUBLEBUF)
    default_font=pygame.font.get_default_font()
    font=pygame.font.SysFont(default_font,32)
    msg=font.render("Click anywere",True,(30,30,30,255))
