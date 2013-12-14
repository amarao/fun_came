#!/usr/bin/python
import pygame,sys

FPS=500

pygame.init()
clock=pygame.time.Clock()
disp=pygame.display.set_mode((800,600),pygame.DOUBLEBUF)
while True:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    clock.tick(FPS)

