import pygame
from config import *
import math
import random
#^last 2 comes preinstalled with python
class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
        #^just for loaded image, we created this class so we dont slow down the game by adding in every single image/ convert - helps load image faster so dont slow down the game
    def get_sprite(self, x, y, width, height):
    # cut out section from the sprite sheet
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        # want to blit the self.sheet onto the surface/ xy selects a cut out from the loaded img
        sprite.set_colorkey(BLACK) # make sure the bkg is transparent
        return sprite


class Player(pygame.sprite.Sprite):
# ^ pygame.sprite.Sprite - a class in the pygame module that makes it easier to make sprites
    def __init__ (self, game, x, y):
        # game - pass in game to access the variables in main. x and y coordinate for the player to appear on the screen
        self.game = game
        self._layer = PLAYER_LAYER
        # ^setting the layer in main, in here, we can tell pygame what layer of the screen we want the sprite to appear. ex: grass at bottom, then rock, then player
        self.groups = self.game.all_sprites
        # ^ add in player into the all sprites group and can access the all sprites group bc we passed in game earlier
        pygame.sprite.Sprite.__init__(self, self.groups)
        #^passing in self.groups, we add in the player to the all sprites group
        self.x = x * TILESIZE
        # ^ passed in x into the function and multiply with the tilesize 
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.height_two = HEIGHTSIZE

        self.x_change = 0
        self.y_change = 0
        #^temporary variables that will store the change in movement during one loop. add the x-change to x variable and y-change to y variable 

        self.facing = 'down'
        #^for when we add in animation, want to know what direction the player is facing; have it face down by default

        #add in image/load in img
        # image_to_load = pygame.image.load("./imgs/single.png")
        # take this away ^ bc we wrote a class to load in the imgs without slowing the game down
        
        self.image = self.game.character_spritesheet.get_sprite(85, 8, self.width, self.height_two)
        # referring to the sprite sheet and the method inside the class spritesheet
        # 32 & 40 are the width and height which we had already set as self.width and self.height but bc my image is a rectangle rather than a square, i needed to put in numbers to figure out where and how long i needed it to be but can add another variable for it =]

        # self.image = pygame.Surface([self.width, self.height]) can take this out too bc we're getting our image from the sprite sheet
        #^creating a rectangle in place of the sprite image right now which is 32x32
        # self.image.fill(GOLD)
        #^filling in the rectangle
        #added in the image so need to load it
        # self.image.blit(image_to_load, (-5,-5)) #second params - position of where to load it to - top left corner of the surface/we get rid of that line of code too after writing a class to load all the imgs
        # self.image.set_colorkey(BLACK)
        # ^if the images background continues to show and sets the image bkg to black/transparent
        self.rect = self.image.get_rect()
        #^every sprite in pygame has an image and a rect; rect is the position and how big it is/image.get_rect() - makes sure its the same size as the image
        self.rect.x = self.x
        self.rect.y = self.y
        # tell pygame the coordinates of our player

    def update(self):
        self.movement()
        #^this calls the movement method under
        self.rect.x += self.x_change
        self.rect.y += self.y_change #temp variable, add that to the coordinates of a player in update method
        self.x_change = 0
        self.y_change = 0


    #ADDING MOVEMENT
    def movement (self):
        keys = pygame.key.get_pressed()
        #^list of every key thats pressed on the keyboard stored in keys and this lets us check if certain keys are pressed
        if keys[pygame.K_LEFT]:
            #if we press the left arrow key, want to take away from x-change bc it goes from left to right. to move to the left, need to take away from the x-axis 
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            # want to take away player speed from the y change/y-axis
            #y-axis starts at top with 0 and when we go down the y-axis, it increases. so top = 0 and bottom = 480 pixels
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks #self.blocks - another group, testing for collisions. test to see if all the blocks have been collided with
        pygame.sprite.Sprite.__init__(self, self.groups) #calling the init method of the inherited class of pygame.sprite.Sprite. self.groups - adding block class to all the sprite groups/blocks to line before
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # a square with a width and height of 32 pixels 
        self.height_two = HEIGHTSIZE

        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill(BLUE)
        # replace these with the spritesheet class

        # attempt at adding different parts of an image into the same block
        # self.image = self.game.terrain_spritesheet.get_sprite("A", 966, 1396, self.width, self.height_two)

        self.image = self.game.silver_spritesheet.get_sprite(201, 488, self.width, self.height_two)
        # self.image = self.game.terrain_spritesheet.get_sprite(201, 488, self.width, self.height_two)
        # self.image = self.game.terrain_spritesheet.get_sprite(1310, 675, self.width, self.height_two)

        # self.image = self.game.terrain_spritesheet.get_sprite("C", 632, 1367, self.width, self.height_two)
    
        #all the sprites in the game needs an image so we add them here
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x , y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        # ^ this calls the pygame.sprite.Sprite and the inherited glass

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.height_two = HEIGHTSIZE

        # self.image = self.game.terrain_spritesheet.get_sprite(893, 290, self.width, self.height)
        self.image = self.game.terrain_spritesheet.get_sprite(507, 618, self.width, self.height)
        # self.image = self.game.terrain_spritesheet.get_sprite(307, 496, self.width, self.height)
        # self.image = self.game.terrain_spritesheet.get_sprite(319, 1354, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



        


