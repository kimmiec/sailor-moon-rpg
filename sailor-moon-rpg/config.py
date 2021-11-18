WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32
HEIGHTSIZE = 40
FPS = 60

PLAYER_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3

GOLD = (255,215,0)
BLACK = (0,0,0)
BLUE = (0,0, 255)


#has rows and columns - grid. height = 480/tilesize = 32 = 15 rows
#columns = 20 rows bc 640 width/32 tilesize
#B - block, for every B, gonna place a wall there so going to need 20 'B' for the 20 rows
# . - to show that theres nothing there
#P - where our player spawns
tilemap = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B..................B',
    'B..................B',
    'B....BBB....B......B',
    'B...........B......B',
    'B........P..B......B',
    'B..................B',
    'B..................B',
    'B.......BBB........B',
    'B.........B........B',
    'B.........B........B',
    'B..................B',
    'B..................B',
    'BBBBBBBBBBBBBBBBBBBB',
]