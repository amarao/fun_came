#!/usr/bin/python

#Targets: draw a grid, move multiple objects print inputed text on the screen and keep in _under_ moving sprite but above grid.

import random
import pygame
import time

def create_grid(orig_surface,cell_size=32,color=(127,127,127,255)):
    '''
        Return surface with drawed grid
    '''
    X,Y=orig_surface.get_size()
    grid=pygame.Surface((X,Y))
    grid.fill((240,240,240,255))
    for x in xrange(0,X,cell_size):
        pygame.draw.line(grid,color,(x,0),(x,Y))
    for y in xrange(0,Y,cell_size):
        pygame.draw.line(grid,color,(0,y), (X,y))
    return grid

class Mob:
    def __init__(self,img,position,speed):
        self.img=pygame.image.load(img).convert_alpha()
        self.y=position
        self.x=0
        self.speed=speed
        self.last_update=time.time()

    def draw(self,surface):
        distance=(time.time()-self.last_update)*self.speed
        self.last_update=time.time()
        self.x+=distance
        if self.x<0:
            self.x=0
            self.speed=-self.speed
        if self.x>surface.get_width()-self.img.get_width():
            self.x=surface.get_width()-self.img.get_width()
            self.speed=-self.speed
        surface.blit(self.img,(self.x,self.y))

if __name__ == "__main__":
    SCREEN_SIZE=(800,600)
    pygame.init()
    clock=pygame.time.Clock()
    disp=pygame.display.set_mode(SCREEN_SIZE,pygame.DOUBLEBUF)
    pygame.display.set_caption("Cats race")
    grid=create_grid(disp)
    mobs=[Mob(random.choice(('2_1.png','2_2.png')),i*32+1,random.random()*16+48) for i in xrange (int(SCREEN_SIZE[1]/32))]
    msg=""
    while True:
        events=pygame.event.get()
        if pygame.QUIT in events:
            pygame.quit()
            break
        elif [event for event in events if event.type==pygame.KEYUP]:
            pass
        disp.blit(grid,(0,0))
        for mob in mobs:
            mob.draw(disp)
        pygame.display.flip()
        clock.tick(25)
        pygame.event.pump()
        
