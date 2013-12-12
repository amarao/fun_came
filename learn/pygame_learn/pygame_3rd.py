#!/usr/bin/python

#Target: create internal 'area map' of empty block, display it, on mouse click install/remove object. Update only changed region of the screen (no global .update or .flip)
#right click invert row, middle click - column
import pygame
import time

class AreaMap:
    def __init__(self, size, empty_image, filled_image ):
        self.empty = pygame.image.load(empty_image).convert()
        self.fill = pygame.image.load(filled_image).convert()
        if self.empty.get_size() != self.fill.get_size():
            raise Exception("Fill/empty images not the same size")
        self.cell_size = self.empty.get_size()
        self.size=size
        self.area = [[False]*self.size[0]]*self.size[1] #size[0] X size=[1] 2D array of 'falses'

    def invert_cell(self,x,y):
        self.area[x][y] = not self.area[x][y]
        self.update+=[(x,y)]

    def invert_column(self,y):
        for x in range(self.size[0]):
            self.invert_cell(self,x,y)

    def invert_row(self,x):
        for y in range(self,size[1]):
            self.invert_cell(self,x,y)

    def update(self,disp):
        pass

if name == '__main__':
    pygame.init()
    clock=pygame.time.Clock()
    disp=pygame.display.set_mode(SCREEN_SIZE,pygame.DOUBLEBUF)
    default_font=pygame.font.get_default_font()
    font=pygame.font.SysFont(default_font,32)
    msg=font.render("Click anywere",True,(30,30,30,255))

    
