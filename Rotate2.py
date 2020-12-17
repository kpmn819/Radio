#!/usr/bin/python3

import pygame
import pygame.font
# Version 2 replaces 'screen' with 'display' to be compatable with Simple_Sprite
pygame.init()
size = (400,400)
display = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def blitRotate(surf, image, pos, originPos, angle):

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

font = pygame.font.SysFont('Times New Roman', 50)
text = font.render('image', False, (255, 255, 0))
image = pygame.Surface((text.get_width()+1, text.get_height()+1))
pygame.draw.rect(image, (0, 0, 255), (1, 1, *text.get_size()))
image.blit(text, (1, 1))
w, h = image.get_size()

angle = 45
done = False
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                done = True

    pos = (display.get_width()/2, display.get_height()/2)
    pos = (200, 100)

    display.fill(0)
    # this places the pivot point at the bottom - center
    # and to call the whole shebang this is all you need
    blitRotate(display, image, pos, (w/2, h), angle)
    #angle += 1

    #pygame.draw.line(display, (0, 255, 0), (pos[0]-20, pos[1]), (pos[0]+20, pos[1]), 3)
    #pygame.draw.line(display, (0, 255, 0), (pos[0], pos[1]-20), (pos[0], pos[1]+20), 3)
    #pygame.draw.circle(display, (0, 255, 0), pos, 7, 0)

    pygame.display.flip()

pygame.quit()