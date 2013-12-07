#!/usr/bin/python

#Targets: create screen, load image to surface, move surface on the screen until any key is pressed
import pygame
import time
pygame.init()
screen_size=(640,480)
disp=pygame.display.set_mode(screen_size)
face=pygame.image.load('1.png').convert()
default_font=pygame.font.get_default_font()
font=pygame.font.SysFont(default_font,32)
msg=font.render("Press SPACE to exit",True,(250,230,210,127))
noface=face.__copy__()
noface.fill((0,0,0,0))
disp.fill((0,0,0,0))
x=0
y=0
alpha=0
while(True):
    begin=time.time()
    #remove previous face
    disp.blit(noface,(x,y))

    #calc new position and alpha
    x=(x+(screen_size[0]/100))%screen_size[0]
    y=(y+(screen_size[1]/100))%screen_size[1]
    alpha=(alpha+1)%256
    face.set_alpha(alpha)
    disp.blit(face,(x,y))

    #message here
    disp.blit(msg,(0,0))
    pygame.display.update()
    pygame.event.pump()    
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        break
    time.sleep(max(0.001,time.time()-begin+0.02))
