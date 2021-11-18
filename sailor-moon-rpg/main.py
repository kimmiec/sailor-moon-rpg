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



    def createTilemap(self):
        #iterate thru every row/column to see if its a 'B', 'P' or a '.'
        for i, row in enumerate(tilemap): #enumerate - 2 values (i, row) i -> the position of the list/row -> value of the list 
            #print(i, row) not only getting the content of the list but also the position
            for j, column in enumerate(row):
                Ground(self, j ,i)
                # if column == "A":
                #     Block(self, j, i)
                if column == "B":
                    Block(self, j, i) #j = x position / i = y position
                # if column == "C":
                #     Player(self, j, i)
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
        self.running = False
    def game_over(self):
        pass
    def intro_screen(self):
        pass

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