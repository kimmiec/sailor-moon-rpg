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
        
        self.image = self.game.character_spritesheet.get_sprite(243, 189, self.width, self.height)
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
        self.collide_enemy()
        # calls the enemy collision method
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

# ENEMY COLLISION
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        # false params - if you want to destroy enemies on impact, but we dont want that so false
        if hits:
            # self.animate2()
            # if we collide with any of the enemies do this
            self.kill()
            # remove player from the all sprites group so they wont appear on the screen anymore
            self.game.playing = False
            # ^ this causes the game to quit

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
        down_animations = [self.game.character_spritesheet.get_sprite(243,192, self.width, self.height), 
                            self.game.character_spritesheet.get_sprite(281, 192, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(317, 192, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(324, 505, self.width, self.height), 
                            self.game.character_spritesheet.get_sprite(361, 505, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(402, 504, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(355, 136, self.width, self.height), 
                            self.game.character_spritesheet.get_sprite(396, 139, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(352, 189, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(243, 242, self.width, self.height), 
                            self.game.character_spritesheet.get_sprite(208, 241, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(171, 241, self.width, self.height)]
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(243,192, self.width, self.height)
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
                self.game.character_spritesheet.get_sprite(324, 505, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.game.character_spritesheet.get_sprite(355, 136, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1
                    
        if self.facing == 'right':
            if self.x_change == 0:
                self.game.character_spritesheet.get_sprite(243, 242, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1
# death animation
    # def animate2(self):
    #     left_animations = [self.game.character_spritesheet.get_sprite(126, 138, self.width, self.height),
    #     self.game.character_spritesheet.get_sprite(203, 152, self.width, self.height)]
    #     right_animations = [self.game.character_spritesheet.get_sprite(359, 4, self.width, self.height),
    #     self.game.character_spritesheet.get_sprite(400, 59, self.width, self.height)]

    #     if self.facing == 'left':
    #         self.image = left_animations[math.floor(self.animation_loop)]
    #         self.animation_loop += 0.2
    #         if self.animation_loop >= 2:
    #             self.animation_loop = 1
    #     if self.facing == 'right':
    #         self.image = right_animations[math.floor(self.animation_loop)]
    #         self.animation_loop += 0.2
    #         if self.animation_loop >= 2:
    #             self.animation_loop = 1
    #     if self.facing == 'down':
    #         self.image = left_animations[math.floor(self.animation_loop)]
    #         self.animation_loop += 0.2
    #         if self.animation_loop >= 2:
    #             self.animation_loop = 1
    #     if self.facing == 'up':
    #         self.image = left_animations[math.floor(self.animation_loop)]
    #         self.animation_loop += 0.2
    #         if self.animation_loop >= 2:
    #             self.animation_loop = 1


# ENEMY/VILLAINS
# JADEITE
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = HEIGHTSIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0 # <- enemy moves back and forth on the screen
        self.max_travel = random.randint(30, 30)
        # move to and fro b/t 7 and 30 pixels 

        self.image = self.game.enemies_spritesheet.get_sprite(82, 237, self.width, self.height)
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0
    
    # MOVEMENT 1
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            # every frame, take away from x_change of speed
            self.movement_loop -= 1
            # subtract from the movement loop
            if self.movement_loop <= -self.max_travel:
                # and if its ever below the minus value of self.max_travel
                self.facing = 'right'
                # turn around and face right
        # do the same for the right
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    # ANIMATION
    def animate(self):
        left_animations = [self.game.enemies_spritesheet.get_sprite(118, 234, self.width, self.height), 
                            self.game.enemies_spritesheet.get_sprite(118, 278, self.width, self.height),
                            self.game.enemies_spritesheet.get_sprite(118, 278, self.width, self.height)]

        right_animations = [self.game.villains_spritesheet.get_sprite(280, 234, self.width, self.height), 
                            self.game.villains_spritesheet.get_sprite(278, 279, self.width, self.height),
                            self.game.villains_spritesheet.get_sprite(278, 279, self.width, self.height)]
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.game.enemies_spritesheet.get_sprite(118, 234, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1
                    
        if self.facing == 'right':
            if self.x_change == 0:
                self.game.villains_spritesheet.get_sprite(280, 234, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1

# KUNZITE
class Enemy2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = HEIGHTSIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['up', 'down'])
        self.animation_loop = 1
        self.movement_loop = 0 # <- enemy moves back and forth on the screen
        self.max_travel = random.randint(30, 30)
        # move to and fro b/t 7 and 30 pixels 

        self.image = self.game.enemies_spritesheet.get_sprite(321, 116, self.width, self.height)
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    # MOVEMENT 1
    def movement(self):
        if self.facing == 'up':
            self.y_change -= ENEMY_SPEED
            # every frame, take away from y_change of speed
            self.movement_loop -= 1
            # subtract from the movement loop
            if self.movement_loop <= -self.max_travel:
                # and if its ever below the minus value of self.max_travel
                self.facing = 'down'
                # turn around and face down
        # do the same for the down
        if self.facing == 'down':
            self.y_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'up'

    def animate(self):
        down_animations = [self.game.enemies_spritesheet.get_sprite(321, 116, self.width, self.height), 
                            self.game.enemies_spritesheet.get_sprite(319, 158, self.width, self.height),
                            self.game.enemies_spritesheet.get_sprite(319, 158, self.width, self.height)]

        up_animations = [self.game.enemies_spritesheet.get_sprite(402, 114, self.width, self.height), 
                            self.game.enemies_spritesheet.get_sprite(402, 114, self.width, self.height),
                            self.game.enemies_spritesheet.get_sprite(402, 114, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.enemies_spritesheet.get_sprite(321, 116, self.width, self.height)
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
                self.game.enemies_spritesheet.get_sprite(402, 114, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1


# QUEEN BERYL
class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = HEIGHTSIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0 # <- enemy moves back and forth on the screen
        self.max_travel = random.randint(30, 30)
        # move to and fro b/t 7 and 30 pixels 

        # enemy 3 - beryl 
        self.image = self.game.enemies_spritesheet.get_sprite(161, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        # beryl
        self.movement()
        self.animate()
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0
    
    # MOVEMENT 1
    def movement(self):
        # + means heading to the right!! so if want to make them go right first, make sure to have +=
        if self.facing == 'left':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'right'
        # - means going to the left! so head left first, make sure to have -=
        if self.facing == 'right':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'left'

    # ANIMATION
    def animate(self):
        left_animations = [self.game.enemies_spritesheet.get_sprite(195, 0, self.width, self.height), 
                            self.game.enemies_spritesheet.get_sprite(195, 0, self.width, self.height),
                            self.game.enemies_spritesheet.get_sprite(195, 0, self.width, self.height)]

        right_animations = [self.game.villains_spritesheet.get_sprite(201, 0, self.width, self.height), 
                            self.game.villains_spritesheet.get_sprite(201, 0, self.width, self.height),
                            self.game.villains_spritesheet.get_sprite(201, 0, self.width, self.height)]
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.game.enemies_spritesheet.get_sprite(195, 0, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1
                    
        if self.facing == 'right':
            if self.x_change == 0:
                self.game.villains_spritesheet.get_sprite(201, 0, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >=3:
                    self.animation_loop = 1



# SPRITE SHEET/WALLS
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

class Block2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks 
        pygame.sprite.Sprite.__init__(self, self.groups) 

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = HEIGHTSIZE

        self.image = self.game.silver_spritesheet.get_sprite(960, 1386, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks 
        pygame.sprite.Sprite.__init__(self, self.groups) 

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = HEIGHTSIZE

        self.image = self.game.silver_spritesheet.get_sprite(989, 1386, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks 
        pygame.sprite.Sprite.__init__(self, self.groups) 

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = HEIGHTSIZE

        self.image = self.game.silver_spritesheet.get_sprite(929, 1386, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block5(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks 
        pygame.sprite.Sprite.__init__(self, self.groups) 

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = HEIGHTSIZE

        self.image = self.game.silver_spritesheet.get_sprite(767, 1036, self.width, self.height)
        # self.image = self.game.silver_spritesheet.get_sprite(865, 1174, self.width, self.height)
        # self.image = self.game.silver_spritesheet.get_sprite(1306, 1258, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block6(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks 
        pygame.sprite.Sprite.__init__(self, self.groups) 

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = HEIGHTSIZE

        self.image = self.game.silver_spritesheet.get_sprite(767, 1070, self.width, self.height)
        # self.image = self.game.silver_spritesheet.get_sprite(865, 1206, self.width, self.height)
        # self.image = self.game.silver_spritesheet.get_sprite(1306, 1285, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block7(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks 
        pygame.sprite.Sprite.__init__(self, self.groups) 

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = HEIGHTSIZE

        self.image = self.game.silver_spritesheet.get_sprite(767, 1099, self.width, self.height)
        # self.image = self.game.silver_spritesheet.get_sprite(865, 1241, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# GROUND
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

# BUTTON - INTRO SCREEN
class Button:
    # does not need inherit from a pygame sprite so it will be its own class
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        # content = the text itself/ fg = foreground/ bg = background
        self.font = pygame.font.Font('Shardee.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        # creating a pygame surface which is a rectangle
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        # pretty much a hit box of the button

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        # call the self.font and render it/ 2nd param,anti-aliasing, do we want it on or off? it means whether the font will be smooth or not so typically yes we do want it on so --> True
        # self.fg = color of the text
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        # position of the text. width and height to make sure its centered in the middle of the button
        self.image.blit(self.text, self.text_rect)
        # render the image, render the text, and throwing the text onto the image
    
    # HOVER ANIMATION
    # padding = 25
    # outline =2

    # def __init__(self, surface, font, text, color1, color2, x, y):
    #     self.hovered = False
    #     self.surface = surface
    #     self.font = font

    #     self.text = self.font.render(text, 1, color1)
    #     if x == None:
    #         self.x = (self.surface.get_width()-self.text.get_width())/2
    #     else:
    #         self.x = x
    #     if y == None: 
    #         self.y = (self.surface.get_height()-self.text.get_height())/2
    #     else:
    #         self.y = y
    #     self.width = self.text.get_width()
    #     self.height = self.text.get_height()
    #     self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    #     self.hovered_text = self.font.render(text, 1, color2)
    #     self.hovered_x = self.x - self.padding/2
    #     self.hovered_y = self.y - self.padding/2
    #     self.hovered_width = self.text.get_width() + self.padding       
    #     self.hovered_height = self.text.get_height() + self.padding
    #     self.hovered_rect = pygame.Rect(self.hovered_x, self.hovered_y, self.hovered_width, self.hovered_y)
    
    # def render(self):
    #     if self.hovered:
    #         pygame.draw.rect(self.surface, GOLD, self.hovered_rect)
    #         self.surface.blit(self.hovered_text, (self.hovered_x + (self.hovered_width-self.hovered_text.get_width())/2, self.hovered_y + (self.hovered_height - self.hovered_text.get_height())/2))
    #     else:
    #         pygame.draw.rect(self.surface, GOLD, self.hovered_rect)
    #         pygame.draw.rect(self.surface, CRYSTAL, (self.hovered_x + self.outline, self.hovered_y + self.outline, self.hovered_width - self.outline*2, self.hovered_height - self.outline*2))
    #         self.surface.blit(self.x + (self.width - self.text.get_width())/2, self.y + (self.height - self.text.get_height())/2)

    def is_pressed(self, pos, pressed):
        # get the position[pos] of the mouse
        if self.rect.collidepoint(pos):
            # check if the mouse is colliding with the button
            if pressed[0]:
                # check if we pressed (clicked on) it or not
                return True
                # ^ if it was pressed, then return true
            return False
            # ^ if we havent, return false
        return False

# ATTACK
class Attack(pygame.sprite.Sprite):
    # inheriting from the pygame sprite
    def __init__ (self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        # will call the init function for the pygame.sprite.Sprite. add attack class to the all_sprites group and the attacks group
        self.x = x
        self.y = y
        self.width = WIDTHSIZE 
        self.height = HEIGHTSIZE

        self.animation_loop = 0 

        self.image = self.game.attack_spritesheet.get_sprite(111, 476, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        # self.game.enemies = checking for collision b/t attack animation and the enemies
        # true = bc if it there is a collision, then we want to kill the enemies/if it was false, then the enemies wont die
        # if hits: 
        #     self.game.enemies == 0
           
    
    def animate(self):
        direction = self.game.player.facing

        down_animations = [self.game.attack_spritesheet.get_sprite(111, 476, self.width, self.height), 
                            self.game.attack_spritesheet.get_sprite(139, 476, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(165, 468, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(216, 457, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(111, 476, self.width, self.height), 
                            self.game.attack_spritesheet.get_sprite(139, 476, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(165, 468, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(180, 405, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(111, 476, self.width, self.height), 
                            self.game.attack_spritesheet.get_sprite(139, 476, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(165, 468, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(109, 504, self.width, self.height)]

        right_animations = [self.game.attack_spritesheet.get_sprite(111, 476, self.width, self.height), 
                            self.game.attack_spritesheet.get_sprite(139, 476, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(165, 468, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(167, 514, self.width, self.height)]
        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            # if we're facing up, we're setting it to an image in the up animation. index = self.animation_loop but using math.floor 
            self.animation_loop += 0.5
            # add 0.5 = 1.5, math.floor then rounds down to the nearest number and you get it, 1 which will then go to the animation of index 1 and repeat. adding 0.5, we're going to be changing the image of the attack for every 2 frames.
            if self.animation_loop >= 4:
            # if the animation loop is greater than 4, then we'll kill the sprites and they will disappear
                self.kill()
        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 
            if self.animation_loop >= 4:
                self.kill()
        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()

