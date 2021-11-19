import pygame
from sprites import *
from config import *
import sys #sys = system

class Game: #--> the main class
    def __init__(self):
        pygame.init()
        #a function that is part of pygame; initializes pygame so we can use it
        #always need to do pygame.init() to use the pygame program whenever you make a game 
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        #need to create our screen^ win_width and win_height are defined in config - since its imported, can use the variables right away
        #pygame.display.set_mode = creates the game window
        #width and height are measured in pixels
        self.clock = pygame.time.Clock()
        #^sets the framerate of the game; framerate: how many times the game updates per sec
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True #<- just a boolean that is used when we want to stop playing the game

        # import font for intro screen
        self.font = pygame.font.Font('Shardee.ttf', 64)
    
        #create multiple walls/create a method bc writing out one by one for each block is inefficent 

        # load in sprite sheets
        self.character_spritesheet = Spritesheet('imgs/sailormoon4.png')
        # Spritesheet = object
        self.character2_spritesheet = Spritesheet('imgs/sailormoon4flip.png')
        # BLOCKS
        self.silver_spritesheet = Spritesheet('imgs/Silver_Millennium_Destroyed.png')
        self.terrain_spritesheet = Spritesheet('imgs/terrain2.png')
        # VILLAINS
        self.enemies_spritesheet = Spritesheet('imgs/sailormoon-villain.gif')
        self.villains_spritesheet = Spritesheet('imgs/sailormoon-villainflip.gif')
        # BACKGROUND
        self.intro_background = pygame.image.load('imgs/introbg3.jpg')
        # self.intro_background = pygame.image.load('imgs/introbg3a.jpg')
        # self.intro_background = pygame.transform.scale(self.intro_background, (640,480), (0,0))
        # self.rect = self.intro_background.get_rect()
        #     self.rect = self.rect.move((30,30))
        #     self.screen.blit(self.intro_background, self.rect)
        #     self.screen = pygame.display.set_mode((640,480))
        self.icon = pygame.image.load('imgs/star3.png')
        self.icon.set_colorkey(WHITE)
        



    def createTilemap(self):
        #iterate thru every row/column to see if its a 'B', 'P' or a '.'
        for i, row in enumerate(tilemap): #enumerate - 2 values (i, row) i -> the position of the list/row -> value of the list 
            #print(i, row) not only getting the content of the list but also the position
            for j, column in enumerate(row):
                Ground(self, j ,i)
                # BLOCKS
                if column == "A":
                    Block2(self, j, i)
                if column == "B":
                    Block(self, j, i) #j = x position / i = y position
                if column == "C":
                    Block3(self, j, i)
                if column == "D":
                    Block4(self, j, i)
                if column == "F":
                    Block5(self, j, i)
                if column == "G":
                    Block6(self, j, i)
                if column == "H":
                    Block7(self, j, i)
                # ENEMIES
                if column == "Z":
                    Enemy(self, j, i)
                if column == "J":
                    Enemy2(self, j, i)
                if column == "Q":
                    Enemy3(self, j, i)
                # PLAYER
                if column == "P":
                    Player(self, j, i)

        #method = name - its called whenever we run the game; set a part all our variables for the game
    def new(self):
        # self.createTilemap() - take this out when adding code into createTilemap method
        #a new game starts
        self.playing = True #used to see if the player died or quit the game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        #^group of spirtes that we can control easily;  object that contains all the sprites -> characters, walls, enemies, etc; have all of them = update all of them together, but can also do individual updates
        self.blocks = pygame.sprite.LayeredUpdates()
        #^all the walls in the game
        self.enemies = pygame.sprite.LayeredUpdates()
        # ^holds all the enemies 
        self.attacks = pygame.sprite.LayeredUpdates()
        # ^holds all the attacks/attack animation

        # self.player = Player(self, 1, 2) #<-- take this away now that we have created a player block
        # ^player object 

        self.createTilemap()
        
    def events(self):
        # game loop events
        for event in pygame.event.get():
            #^get every event in pygame and iterate thru that list
            if event.type == pygame.QUIT:
                #pygame.quit = when we close the button, checks to see if we closed the game and if it does, then we stop playing and running
                self.playing = False
                self.running = False

    def update(self):
        # game loop updates
        self.all_sprites.update()
        #^ the layered updates contains a method called update/ find the update method in every single sprite and call the method in that sprite
    def draw(self):
        # game loop draw
        self.screen.fill(BLACK)
        #^black window at the moment
        self.all_sprites.draw(self.screen)
        #^refers to the all sprites group and call the draw method, look thru all the sprites in the group, finds the image and rect and draws that onto the window
        self.clock.tick(FPS)
        #^update the screen 60x/sec
        pygame.display.update()
        #^update the screen literally

    def main(self): 
        # game loop
        while self.playing:
            self.events()
            #^contains everything like key press events
            self.update()
            #^ update the game to make sure its not a static image
            self.draw()
            #^display all the sprites onto our screen
        # self.running = False
        # ^want to take this out now bc when we hit a game over sequence, we dont want the game to just quit
        # once we collide with an enemy, we get out of this loop above and go to the game over sequence
    def game_over(self):
        text = self.font.render('Game Over', True, RED)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        # get rectangle from the text object/param ^ centers text in the middle of the screen

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, SILVER, PURPLE, 'Restart', 32)

        # want to get everything (sprites) off the screen now when the game over screen displays 
        

    def intro_screen(self):
        intro = True

        title = self.font.render('Sailor Moon', True, MOON)
        # rendering the self.font from line 21 above. title, antialiasing, font color
        title_rect = title.get_rect(x=350, y=200)
        # get the rect from the title and position it with the x and y coordinates/(x=350, y=200)

        # title_rect = title.get_rect(x=10, y=200)
        # flipped image ^^^

        play_button = Button(420, 280, 100, 50, PINK, LIGHT_CRYSTAL, 'Play', 32)
        # x, y, width, height, fg, bg, text, fontsize
        # play_button = Button(10, 280, 100, 50, PINK, LIGHT_CRYSTAL, 'Play', 32)
        # flipped image ^^^

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                    # ^when this loop is broken out of, it'll move on to g.new which is start a new game
            mouse_pos = pygame.mouse.get_pos()
            # grabs the position of the mouse on the screen
            mouse_pressed = pygame.mouse.get_pressed()
            # return whenever theh mouse is clicked and returns a list. if the first item in the list is a left click button, the sec is the right click button and the 3rd is the middle mouse wheel. thats why in the sprites file, we wrote pressed[0], to check that we have a left click button

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            # display bg
            self.screen.blit(self.intro_background, (-62, -260))
            # on the screen, gonna drawa the bg and display at 0,0/(-62,-225)
            # self.screen.blit(self.intro_background, (-120, -260))
            # flipped image ^
            self.screen.blit(self.icon, (399,195))
            self.screen.blit(title, title_rect)
            # display title
            self.screen.blit(play_button.image, play_button.rect)
            # displaying the play button image at the play button rect
            self.clock.tick(FPS)
            # update the game at 60 frames/sec
            pygame.display.update()

# need to turn this class into an object
g = Game()
#^create the game object
g.intro_screen()
#^and run the intro screen method 
g.new()
#^call the new method from earlier and run it
while g.running:
    g.main()
    #^when it runs, calls the main loop and once the loop stops, set the running to false and then break out of the loop then
    g.game_over()
pygame.quit()
# quit out of the game
sys.exit()
# and exit the python program