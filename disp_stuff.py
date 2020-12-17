#!/usr/bin/python3
# Version 1 adds blitRotate 
import pygame, os
from pygame.locals import *
import pygame.font


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

def blitRotate(surf, image, pos, originPos, angle):
    # and to call the whole shebang this is all you need
    # pos is a tuple (x,y)
    '''blitRotate(display, image, pos, (w/2, h), angle)'''

    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    #pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)

def blit_em():
    # throws everything on the screen
    display.blit(needle, (414,190))
    # some weirdness with rotate y is inverted and - angle is cw + angle ccw
    w, h = needle.get_size()
    blitRotate(display, needle, (430,461), (w/2, h),85)
    #display.blit(mask, (239,411))
    display.blit(eye0, (371, 26))
    pygame.display.flip()    

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
        blit_em()
        #display.blit(needle, (414,190))
        # some weirdness with rotate y is inverted and - angle is cw + angle ccw
        #w, h = needle.get_size()
        #blitRotate(display, needle, (430,461), (w/2, h),85)
        #display.blit(mask, (239,411))
        #display.blit(eye0, (371, 26))
        #pygame.display.flip()

        #Framerate of the Game
        clock.tick(60)
