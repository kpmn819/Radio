#!/usr/bin/env python
# Version 2 replace names
# Version 3 get rid of move stuff
"""
This is the full and final example from the Pygame Tutorial,
"How Do I Make It Move". It creates 10 objects and animates
them on the screen.
Note it's a bit scant on error checking, but it's easy to read. :]
Fortunately, this is python, and we needn't wrestle with a pile of
error codes.
"""


#import everything
import os, pygame
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

#our game object class
class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)
    def move(self):
        self.pos = self.pos.move(self.speed, 0)
        if self.pos.right > 600:
            self.pos.left = 0
    


#quick function to load an image
def load_image(name):
    path = os.path.join(main_dir, 'Graphics', name)
    return pygame.image.load(path).convert_alpha()


#here's the full code
def main():
    pygame.init()
    screen = pygame.display.set_mode((841, 640))


    radio = load_image('Radio.png')
    needle = load_image('Needle.png')
    eyeball0 = load_image('Eyeball0.png')


    #   successfully overwrites the old sprite position.


    screen.blit(radio, (0, 0))

    objects = []
    
    o = GameObject(needle, 320, 0)
    e = GameObject(eyeball0,320,0)
    objects.append(o)
    objects.append(e)
    print([objects])

    while 1:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                return

        for o in objects:
            # for each object
            screen.blit(radio, o.pos, o.pos)
        for o in objects:
            #o.move()
            screen.blit(o.image, o.pos)

        pygame.display.update()



if __name__ == '__main__': main()
