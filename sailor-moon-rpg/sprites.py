import pygame
from pygame.sprite import spritecollide
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
        # self.height = TILESIZE
        self.height = HEIGHTSIZE

        self.x_change = 0
        self.y_change = 0
        #^temporary variables that will store the change in movement during one loop. add the x-change to x variable and y-change to y variable 

        self.facing = 'down'
        #^for when we add in animation, want to know what direction the player is facing; have it face down by default

        # animation loop
        self.animation_loop = 1

        #add in image/load in img
        # image_to_load = pygame.image.load("./imgs/single.png")
        # take this away ^ bc we wrote a class to load in the imgs without slowing the game down
        
        self.image = self.game.character_spritesheet.get_sprite(85, 8, self.width, self.height)
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
        #^this calls the movement method which is under this method
        self.animate()
        # ^calling the animation method
        self.rect.x += self.x_change
        # call the collision between these two lines of code
        self.collide_blocks('x')
        self.rect.y += self.y_change #temp variable, add that to the coordinates of a player in update method
        self.collide_blocks('y')
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

# COLLISION DETECTION
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            # ^checking whether the rect of one sprite is inside the rect of another sprite/comparing character sprite to block sprites. last param checks if you want to delete the sprite so its false bc we dont want the sprite to be deleted when it collides
            if hits:
                if self.x_change > 0:
                # ^we're moving right bc the x-axis is increasing!
                    self.rect.x = hits[0].rect.left - self.rect.width
                    # taking the top left corner and matching it up with the block sprite but then the '- self.rect.width' would push it back so it lines up next to the block sprite rather than overlap it
                if self.x_change < 0:
                # ^we're moving left
                    self.rect.x = hits[0].rect.right
                    # hits[0] - the wall were colliding with 
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0: 
                    # going down
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
    # ANIMATION
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(85, 8, self.width, self.height), 
                            self.game.character_spritesheet.get_sprite(130, 7, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(170, 4, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(89, 93, self.width, self.height), 
                            self.game.character_spritesheet.get_sprite(129, 94, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(169, 92, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(86, 52, self.width, self.height), 
                            self.game.character_spritesheet.get_sprite(127, 50, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(246, 50, self.width, self.height)]

        right_animations = [self.game.character2_spritesheet.get_sprite(334, 50, self.width, self.height), 
                            self.game.character2_spritesheet.get_sprite(293, 51, self.width, self.height),
                            self.game.character2_spritesheet.get_sprite(176, 50, self.width, self.height)]
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(85, 8, self.width, self.height)
            # ^stand still/wont actually animate so need to put in self.y_change code
                # if were standing still, set to static image. if y_change isnt 0 = we're moving
            else: 
                self.image = down_animations[math.floor(self.animation_loop)]
                # self.animation_loop inside math.floor = index which is 1 (choosing the second out of the 3) -> index 1
                self.animation_loop += 0.1
                # reaching 1,2, or 3 for every 10 frames; every 10 frames is going to change the animation loop 
                if self.animation_loop >=3:
                    # set it back to one bc we only have 3 images in each animation list
                    # adding 0.1 to math.floor each time and eventually will reach 2 and then change index of the math.floor which then reaches 3 and then we set it back to index 0 
                    self.animation_loop = 1
        if self.facing == 'up':
            if self.y_change == 0:
                self.game.character_spritesheet.get_sprite(89, 93, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.game.character_spritesheet.get_sprite(86, 52, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1
                    
        if self.facing == 'right':
            if self.x_change == 0:
                self.game.character2_spritesheet.get_sprite(334, 50, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1
                

# SPRITE SHEET
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks #self.blocks - another group, testing for collisions. test to see if all the blocks have been collided with
        pygame.sprite.Sprite.__init__(self, self.groups) #calling the init method of the inherited class of pygame.sprite.Sprite. self.groups - adding block class to all the sprite groups/blocks to line before
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        # self.height = TILESIZE
        # a square with a width and height of 32 pixels 
        self.height = HEIGHTSIZE

        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill(BLUE)
        # replace these with the spritesheet class

        # attempt at adding different parts of an image into the same block
        # self.image = self.game.terrain_spritesheet.get_sprite("A", 966, 1396, self.width, self.height_two)

        self.image = self.game.silver_spritesheet.get_sprite(201, 488, self.width, self.height)
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
        # self.height = TILESIZE
        self.height = HEIGHTSIZE

        # self.image = self.game.terrain_spritesheet.get_sprite(893, 290, self.width, self.height)
        self.image = self.game.terrain_spritesheet.get_sprite(507, 618, self.width, self.height)
        # self.image = self.game.terrain_spritesheet.get_sprite(307, 496, self.width, self.height)
        # self.image = self.game.terrain_spritesheet.get_sprite(319, 1354, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



        


