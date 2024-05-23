from pygame.locals import *


# Settings

FRAMERATE_MS = 25
FRAMERATE_PS = 30

TIME_ANIMATION  = 3
SPEED_ANIMATION = 5

# Dimensions

SCREEN_WDTH = 500
SCREEN_HGHT = 700
SCREEN_MIDW = SCREEN_WDTH / 2
SCREEN_MIDH = SCREEN_HGHT / 2
SCREEN_SIZE = SCREEN_WDTH, SCREEN_HGHT

# Dimensions of game elements

FLAPPY_SIZE   = 350, 80
FINGER_SIZE   =  25, 25
TAP_SIZE      =  40, 25
GETREADY_SIZE = 200, 50
SHARE_SIZE    =  60, 40
GAMEOVER_SIZE = 300, 80
MENU_SIZE     = 100, 50
OK_SIZE       = MENU_SIZE

DIGITS_SIDE = 20
DIGITS_SIZE = DIGITS_SIDE, DIGITS_SIDE

# Constants of the game's classes

BEAN_SPEED = -10.5
BEAN_ACCEL =   1.5
BEAN_MAX_TIME  =  8
BEAN_MAX_DELTA = 18
BEAN_SPD_ROTATION =  15
BEAN_MAX_ROTATION =  30
BEAN_FLY_ROTATION = -70
BEAN_MIN_ROTATION = -90
BEAN_WDTH = 50
BEAN_HGHT = 40

BASE_WDTH = SCREEN_WDTH
BASE_HGHT = 80

PIPE_DIST = 200
PIPE_MIN_HGHT = 0
PIPE_MAX_HGHT = SCREEN_HGHT - BASE_HGHT - PIPE_DIST
PIPE_WDTH = 100
PIPE_HGHT = PIPE_MAX_HGHT

# Indent

SPACING   = 10
SPACING_2 = 2 * SPACING
SPACING_3 = 3 * SPACING

FLAPPY_TOP   = 100
FINGER_TOP   = 450
GAMEOVER_TOP = 260
SCORE_LEFT   =  20
SCORE_TOP    =  20

BEAN_PSCW = 200
BEAN_PSCH = 350
PIPE_X    = 700
PIPE_NX   = 600
BASE_TOP  = SCREEN_HGHT - BASE_HGHT

# File path

DECISION_TREE_PATH = 'flappy_bean/models/dtc.pkl'
LOGISTIC_REGR_PATH = 'flappy_bean/models/log_reg.pkl'
SVM_RBF_PATH       = 'flappy_bean/models/svm_rbf.pkl'

BEAN_PATHS         = 'flappy_bean/media/bean1.png', \
                     'flappy_bean/media/bean2.png', \
                     'flappy_bean/media/bean3.png', \
                     'flappy_bean/media/bean2.png'
BASE_PATH          = 'flappy_bean/media/base.png'
PIPE_PATH_TOP      = 'flappy_bean/media/pipe_top.png'
PIPE_PATH_BASE     = 'flappy_bean/media/pipe_base.png'
GAME_BG_PATH       = 'flappy_bean/media/bg.png'
GAME_FLAPPY_PATH   = 'flappy_bean/media/flappy.png'
GAME_FINGER_PATH   = 'flappy_bean/media/finger.png'
GAME_TAPLEFT_PATH  = 'flappy_bean/media/tap_left.png'
GAME_TAPRIGHT_PATH = 'flappy_bean/media/tap_right.png'
GAME_GETREADY_PATH = 'flappy_bean/media/get_ready.png'
GAME_SHARE_PATH    = 'flappy_bean/media/share.png'
GAME_GAMEOVER_PATH = 'flappy_bean/media/game_over.png'
GAME_MENU_PATH     = 'flappy_bean/media/menu.png'
GAME_OK_PATH       = 'flappy_bean/media/ok.png'
GAME_DIGITS_PATH   = [f'flappy_bean/media/{i}.png' for i in range(10)]

GAME_THEME_PATH    = 'flappy_bean/media/epic_at_the_jungle.mp3'
GAME_EFFCT_PATH    = 'flappy_bean/media/gameover.mp3'
