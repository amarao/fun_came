#!/usr/bin/python

#Target: create internal 'area map' of empty block, display it, on mouse click install/remove object. Update only changed region of the screen (no global .update or .flip)
#left click - put/remove
#middle click - clean
#shift - whole row
#crtl - whole column
import pygame
import time
import sys
SCREEN_SIZE=(800,640)
#FPS=50

class AreaMap:
    def __init__(self, size, empty_image, filled_image, message=None):
        self.empty = pygame.image.load(empty_image).convert()
        self.fill = pygame.image.load(filled_image).convert()
        if self.empty.get_size() != self.fill.get_size():
            raise Exception("Fill/empty images not the same size")
        self.cell_size = self.empty.get_size()
        self.size = size
        self.area = [[ False for y in range(self.size[1])] for x in range(self.size[0])] #init 2D array with falses
        self.queue = [(x,y) for x in range(self.size[0]) for y in range (self.size[1])]
        self.update_rects = []
        self.message=message

    def clear(self):
        for x in range(self.size[0]):
            for y in range (self.size[1]):
                self.set_cell(False,(x,y))

    def pos(self, pos):
        '''convert position to block number, take (x,y), return x,y'''
        return pos[0]/self.cell_size[0], pos[1]/self.cell_size[1]

    def get_cell_by_pos(self, pos):
        return self.get_cell(self.pos(pos))

    def get_cell(self, index):
        return self.area[index[0]][index[1]]

    def set_cell(self,value,(x,y)):
        if self.area[x][y] != value:
            self.area[x][y] = value
            self.queue.append((x, y))

    def set_cell_by_pos(self, value, pos):
        self.set_cell(value,self.pos(pos))

    def set_row_by_pos(self, value, pos):
        for x in range(self.size[0]):
            self.set_cell(value, (x, self.pos(pos)[1]))

    def set_col_by_pos(self, value, pos):
        for y in range(self.size[1]):
            self.set_cell(value, (self.pos(pos)[0], y))

    def set_with_kmod(self, value, pos, key_mod):
        '''
            select to set single cell, row or column, based on key_mod
        '''
        if key_mod & pygame.KMOD_CTRL:
            self.set_col_by_pos(value, pos)
        elif key_mod & pygame.KMOD_SHIFT:
            self.set_row_by_pos(value, pos)
        else:
            self.set_cell_by_pos(value, pos)



    def set_cells_by_strike(self,value,pos,rel, key_mod):
        '''operates on every cell under single mouse move'''
        offset=max(map(abs,rel))
        if offset<min(self.cell_size):
            self.set_with_kmod(value, pos, key_mod) #trivial - one cell changed
            return
        div_round_to_infinity = lambda a, b: a//b if a*b<0 else (a+(-a%b))//b # http://stackoverflow.com/questions/7181757/how-to-implement-division-with-round-towards-infinity-in-python
        point_calc = lambda pos,rel, step, steps, size, index: pos[index] - rel[index] + div_round_to_infinity(rel[index]*step, steps)
        steps = div_round_to_infinity(offset, min(self.cell_size))
        for step in range(0, steps):
            x = point_calc(pos, rel, step, steps, self.cell_size, 0)
            y = point_calc(pos, rel, step, steps, self.cell_size, 1)
            self.set_with_kmod(value, (x, y), key_mod)

    def update_cell(self, disp, cell):
        reg_x = cell[0]*self.cell_size[0]
        reg_y = cell[1]*self.cell_size[1]
        if self.area[cell[0]][cell[1]]:
            pattern = self.fill
        else:
            pattern = self.empty
        disp.blit(pattern,(reg_x, reg_y))
        reg=pygame.rect.Rect((reg_x, reg_y), self.cell_size)
        self.update_rects.append(reg)

    def update(self, disp):
        if not self.queue:
            return
        for item in self.queue:
            self.update_cell( disp, item)
        if self.message:
            if self.message.get_rect().collidelist(self.update_rects) != -1:
                disp.blit(self.message, (0, 0))
                self.update_rects.append(self.message.get_rect())
        pygame.display.update(self.update_rects)
        self.queue=[]
        self.update_rects=[]

if __name__ == '__main__':
    pygame.init()
    disp = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 30)
    msg = font.render("Click anywere to draw. Shift - line, ctrl - column, mid. button - clear screen", True, (230, 30, 30, 255))
    area = AreaMap((25,20), "3_empty.png", "3_fill.png", msg)
    area.update(disp)
    while True:
        pygame.event.pump()
        event=pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                state = not area.get_cell_by_pos(event.pos)
                area.set_cells_by_strike(state, event.pos,(0,0),pygame.key.get_mods())
                prev = event.pos
            if event.button == 2:
                area.clear()
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                rel=map(int.__sub__,event.pos,prev) #workaround for fast mouse movements
                area.set_cells_by_strike(state,event.pos,rel,pygame.key.get_mods())
                prev=event.pos
        area.update(disp)

