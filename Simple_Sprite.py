#!/usr/bin/python3

import pygame, os
from pygame.locals import *



eye0_img = 'Eyeball0.png'
needle_img = 'Needle.png'
radio = 'Radio.png'
mask_img = 'Mask_Needle.png'

pygame.init()

class Background(pygame.sprite.Sprite):
    def __init__(self,image_file,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

BackGround = Background(radio, [0,0])

class OverlaySprites(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect  = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
needle_sp = OverlaySprites('Needle.png',0,[400,200])



#============VARIABLES==============
os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
screen_width=841
screen_height=640
bgColor = (255, 255, 255)
size=(screen_width, screen_height)
display = pygame.display.set_mode(size)
progress = True
pygame.display.set_caption('Python - Pygame Simple Sprite Movement')

# for now there must be something named 'char' so the program will work
#char = pygame.image.load(radio).convert_alpha()
eye0 = pygame.image.load(eye0_img).convert_alpha()
needle = pygame.image.load(needle_img).convert_alpha()
mask = pygame.image.load(mask_img).convert_alpha()
char = pygame.image.load(mask_img).convert_alpha()

x=325
y=250
speed = 1
left = False
right = False
up = False
down = False



#============MAIN LOOP==============
while progress:
        display.fill(bgColor)
        display.blit(BackGround.image, BackGround.rect)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        progress = False
                        pygame.quit()
                        quit()
                elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                                progress = False
                                pygame.quit()
                                quit()
                #Player Input KeyDown
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                                left = True
                        elif event.key == pygame.K_RIGHT:
                                right = True
                        elif event.key == pygame.K_UP:
                                up = True
                        elif event.key == pygame.K_DOWN:
                                down = True
                        
                #Player Input KeyUP           
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                                left = False
                        elif event.key == pygame.K_RIGHT:
                                right = False
                        elif event.key == pygame.K_UP:
                                up = False
                        elif event.key == pygame.K_DOWN:
                                down = False
        #Sprite Started To Move
        if left:
                x-=speed
        elif right:
                x+=speed
        elif up:
                y-=speed
        elif down:
                y+=speed

        #Limit The Player Movement within the boundary
        if x > screen_width - char.get_width():
                x = screen_width - char.get_width()
        if x < 0:
                x = 0
        if y > screen_height - char.get_height():
                y = screen_height - char.get_height()
        if y < 0:
                y = 0
        print('x= ',x,' y= ',y)
        
        #screen.blit(BackGround.image, BackGround.rect)
        #display.blit(BackGround.image, BackGround.rect)
        #display.blit(needle.image, needle.rect)
        display.blit(char, (x,y))
        display.blit(needle, (414,190))
        display.blit(mask, (320,408))
        display.blit(eye0, (371, 26))
        pygame.display.flip()

        #Framerate of the Game
        clock.tick(60)
