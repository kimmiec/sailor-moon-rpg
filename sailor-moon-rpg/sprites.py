import pygame
from config import *
import math
import random
#^last 2 comes preinstalled with python

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

        self.x_change = 0
        self.y_change = 0
        #^temporary variables that will store the change in movement during one loop. add the x-change to x variable and y-change to y variable 

        self.facing = 'down'
        #^for when we add in animation, want to know what direction the player is facing; have it face down by default

        #add in image/load in img
        image_to_load = pygame.image.load("./imgs/single.png")
        
        self.image = pygame.Surface([self.width, self.height])
        #^creating a rectangle in place of the sprite image right now which is 32x32
        # self.image.fill(GOLD)
        #^filling in the rectangle
        #added in the image so need to load it
        self.image.blit(image_to_load, (0,0)) #second params - position of where to load it to - top left corner of the surface

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

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)

        #all the sprites in the game needs an image so we add them here
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        


