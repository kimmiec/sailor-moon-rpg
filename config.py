WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32
HEIGHTSIZE = 40
WIDTHSIZE = 40
FPS = 60

PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 2
ENEMY_SPEED = 1

GOLD = (255,215,0)
BLACK = (0,0,0)
BLUE = (0,0, 255)
# SAILOR MOON THEME COLORS
WHITE = (255,255,255)
YELLOW = (250,241,114)
# MOON = (254,252,215)
MOON = (250,240,117)
PINK = (254,163,220)
CRYSTAL = (124,195,241)
LIGHT_CRYSTAL = (219,240,251)
# RED = (248,135,132)
RED = (184,0,0)
DARK_RED = (225,67,68)
# DARK_RED = (226,2,2)
BRIGHT_RED = (203,0,0)
PURPLE = (205,199,247)
DARK_PURPLE = (169,146,226)
# DARK_PURPLE = (193,135,229)
SILVER = (243,251,253)
# SILVER = (186,217,248)


#has rows and columns - grid. height = 480/tilesize = 32 = 15 rows
#columns = 20 rows bc 640 width/32 tilesize
#B - block, for every B, gonna place a wall there so going to need 20 'B' for the 20 rows
# . - to show that theres nothing there
#P - where our player spawns
tilemap = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B........Z.........B',
    'B..................B',
    'B....BBB....F......B',
    'B...........G......B',
    'B........P..H......B',
    'B..................B',
    'B...............J..B',
    'B.......DAC........B',
    'B.........B........B',
    'B...Q.....B........B',
    'B..................B',
    'B..................B',
    'BBBBBBBBBBBBBBBBBBBB',
]