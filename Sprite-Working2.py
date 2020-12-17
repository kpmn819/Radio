import os,pygame
import sys
main_dir = os.path.split(os.path.abspath(__file__))[0]
# Version 2 add keyboard response
pos_x = 100
pos_y = 100
which_one = 0
GREEN = (0,255,0)

pygame.init()



def load_image(name):
    image = pygame.image.load(name).convert
    return image

eye0_img = load_image('Eyeball0.png')


class TestSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(TestSprite, self).__init__()
        self.images = []
        self.images.append(load_image('Needle.png'))
        self.images.append(load_image('Eyeball0.png'))
        # assuming both images are 64x64 pixels

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5,5, 64, 64)

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        global pos_x
        global pos_y
        global which_one
        self.index += 1
        self.rect = pygame.Rect(pos_x, pos_y, 64, 64)
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        
    def move_me(self):
        self.rect = pygame.Rect(pos_x,pos_y,64,64)
        
        
class FixedSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image = eye0_img
        self.rect = self.image.get_rect()
        self.rect.center = (371, 26)
        



def main():

    screen = pygame.display.set_mode((841,640))
    
    
    fixed_sprites = pygame.sprite.Group()
    eyeballs = pygame.sprite.Group()
    eyeball0 = FixedSprite()
    eyeballs.add(eyeball0)    
    
    radio = load_image('Radio.png')
    my_sprite = TestSprite()
    print(my_sprite)
    my_group = pygame.sprite.Group(my_sprite)
    screen.blit(radio, (0, 0))

    while True:
#        event = pygame.event.poll()
#        if event.type == pygame.QUIT:
#            pygame.quit()
#            sys.exit(0)
         global pos_x
         global pos_y
         events = pygame.event.get()
         for event in events:
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LEFT:
                    pos_x -= 1
                    #my_sprite.rect(pos_x,pos_y,64,64)
                 if event.key == pygame.K_RIGHT:
                    pos_x += 1
                    #my_sprite.rect(pos_x,pos_y,64,64)
                    #pygame.image[0].move_me()
                    
                 if event.key == pygame.K_UP:
                    pos_y += 1
                 if event.key == pygame.K_DOWN:
                    pos_y -= 1
                 print('x= ',pos_x,' y= ',pos_y)  
        # Calling the 'my_group.update' function calls the 'update' function of all 
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.
        #screen.blit(radio, (0, 0))
         #print('do we ever get here?')
         eyeballs.update()
         eyeballs.draw(screen)
         
         my_group.update()
         my_group.draw(screen)
         pygame.display.flip()

if __name__ == '__main__':
    main()