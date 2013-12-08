#!/usr/bin/python

import pygame

pygame.init()
screen_size=(800,60)
disp=pygame.display.set_mode(screen_size, pygame.DOUBLEBUF)
msg=u""
clock=pygame.time.Clock()
default_font=pygame.font.get_default_font()
font=pygame.font.SysFont(default_font,16)

disp.fill((240,240,240,255))
pygame.display.flip()
while(not pygame.event.pump()):
    for event in pygame.event.get():
        print event
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            msg+=event.unicode
            disp.fill((240,240,240,255))
            disp.blit(font.render(msg,True,(30,30,30,255)),(0,0))
            pygame.display.flip()
    clock.tick(25)

