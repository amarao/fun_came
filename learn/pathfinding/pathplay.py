#!/usr/bin/python -u
'''
    Targets:
        * Create framework for path finding: 
            * maze creation (manual) from learn_pygame/pygame_3rd.py
            * start/end points
            * creep class
            * some way to change pathfinding algorithm
        * Implement stright-to-the-target pathfinding
        * Implement A* algorithm
        * Some kind of decision visualization
        * Interface to show/change current algorithm

'''
import pygame
import time
import sys
SCREEN_SIZE=(800,640)
FPS=50

class Creep(object): #no animation yet
    def __init__(self,sprite, cell_size,initial_pos,finish):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.start=initial_pos
        self.finish=finish
        self.cell_size = cell_size
        self.pos = initial_pos
        self.speed = 25
        self.delay = self.speed
        self.path=[]

    def move(self,area):
        if self.delay:
            self.delay -= 1
            return None
        else:
            self.delay = self.speed
        print "+",
        if area.get_cell(self.pos) == "Finish":
            self.pos = area.get_start()
            self.path = None
        if self.path:
            old_pos=self.pos
            new_pos=self.path.pop()
            if self.validate(new_pos):
                self.pos=new_pos
                return old_pos
            else:
                self.path=self.pathfind(area)
        else:
            print "*",
            self.path=self.pathfind( area)

    def validate(self, pos):
        return True

    def get_pixel_position(self):
        print "position", (self.pos[0]*self.cell_size[0],self.pos[1]*self.cell_size[1])
        return (self.pos[0]*self.cell_size[0],self.pos[1]*self.cell_size[1])

    def update(self,surface):
        '''
            make a blit, return update rect
        '''
        surface.blit(self.sprite,self.get_pixel_position())
        return pygame.Rect(self.get_pixel_position(),self.cell_size)

    def pathfind(self,area):
        '''
            Implements a* pathfinding algorithm. http://en.wikipedia.org/wiki/A*_search_algorithm
        '''
        #not really, just stub to test the rest
        return [(a,a) for a in xrange(20)]

class AreaMap:
    def __init__(self, size, empty_image, filled_image, message=None):
        self.size=size
        self.empty = pygame.image.load(empty_image).convert()
        fill = pygame.image.load(filled_image).convert_alpha()
        self.fill = self.empty.copy()
        self.fill.blit(fill, (0, 0)) #create 'fill' tile over empty (fill can contain transparency)
        self.start = self.fill.copy()
        self.start.fill((30, 30, 30, 127))
        self.finish = self.fill.copy()
        self.finish.fill((230, 230, 230, 127))
        if self.empty.get_size() != self.fill.get_size():
            raise Exception("Fill/empty images not the same size")
        self.cell_size = self.empty.get_size()
        self.size = size
        self.area = [[ False for y in range(self.size[1])] for x in range(self.size[0])] #init 2D array with falses
        self.queue = set([(x, y) for x in range(self.size[0]) for y in range (self.size[1])])
        self.update_rects = []
        self.message=message
        
    def shift(self, (x,y), (shift_x, shift_y)):
        return x+shift_x, y+shift_y

    def get_edges(self, x, y):
        '''
            return accessible edges in graph for specified vertex
            finish & stop are accessible

            return value: list of edges, each edge - pair of coordinates
        '''
        accessible=[]
        for shift in ( (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1) ):
            if self.get_cell(self.shift((x,y), shift) ) == None: #Only None field is accessible
                accessible.append((self.shift((x,y),shift)))
        return accessible

    def add_start(self, x, y):
        '''
            add start point to area
        '''
        self.area[x][y] = "Start"
        self.mob=Creep("mob.png",self.cell_size,(x,y))
        self.queue.add((x, y))


    def add_finish(self, x, y):
        '''
            add finish point to area
        '''
        self.area[x][y] = "Finish"
        self.queue.add((x, y))

    def get_start(self):
        for x in self.size[0]:
            for y in self.size[y]:
                if self.area[x][y]=="Start":
                    return (x,y)

    def get_finish(self):
        for x in self.size[0]:
            for y in self.size[y]:
                if self.area[x][y]=="Finish":
                    return (x,y)

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
        if index[0] < 0 or index [1] < 0 or index [0] >= self.size[0] or index[1] >= self.size[1]:
            return "Unaccessible"
        return self.area[index[0]][index[1]]

    def set_cell(self,value,(x,y)):
        if self.area[x][y] in ("Start", "Finish"): #do not allow replace of finish or start
            return 
        if self.area[x][y] != value:
            self.area[x][y] = value
            self.queue.add((x, y))

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
        print "updating:", cell, reg_x, reg_y
        if self.area[cell[0]][cell[1]]== True:
            pattern = self.fill
        elif self.area[cell[0]][cell[1]] == False:
            pattern = self.empty
        elif self.area[cell[0]][cell[1]] == "Finish":
            pattern = self.finish
        elif self.area[cell[0]][cell[1]] == "Start":
            pattern = self.start
        else:
            print "wat?"
        disp.blit(pattern,(reg_x, reg_y))
        reg=pygame.rect.Rect((reg_x, reg_y), self.cell_size)
        self.update_rects.append(reg)
#        print "update_rects", self.update_rects

    def update(self, disp):
        mob_old_pos = self.mob.move(self)
        if mob_old_pos:
            self.queue.add(mob_old_pos)
            print "old", mob_old_pos, self.queue
        if not self.queue:
            return
        for item in self.queue:
            self.update_cell( disp, item)
        self.update_rects.append(self.mob.update(disp))
        if self.message:
            if self.message.get_rect().collidelist(self.update_rects) != -1:
                disp.blit(self.message, (0, 0))
                self.update_rects.append(self.message.get_rect())
        pygame.display.update(self.update_rects)
        self.queue=set()
        self.update_rects=[]


if __name__ == '__main__':
    pygame.init()
    disp = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 30)
    msg = font.render("Click anywere to draw. Shift - line, ctrl - column, mid. button - clear screen", True, (230, 30, 30, 255))
    area = AreaMap((25,20), "p1_empty.png", "p1_barrier.png", msg)
    area.add_start(0,5)
    area.add_finish(24,15)
    area.update(disp)
    while True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
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
        clock.tick(FPS)

