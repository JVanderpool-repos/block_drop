"""
Game constants and configuration
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Cell size
CELL_SIZE = 30

# Colors (RGB)
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'ORANGE': (255, 165, 0),
    'PURPLE': (128, 0, 128),
    'CYAN': (0, 255, 255),
    'GRAY': (128, 128, 128),
    'DARK_GRAY': (64, 64, 64)
}

# Block Drop colors
PIECE_COLORS = {
    'I': COLORS['CYAN'],
    'O': COLORS['YELLOW'],
    'T': COLORS['PURPLE'],
    'S': COLORS['GREEN'],
    'Z': COLORS['RED'],
    'J': COLORS['BLUE'],
    'L': COLORS['ORANGE']
}

# Game timing
INITIAL_FALL_SPEED = 500  # milliseconds
FAST_DROP_SPEED = 50
MOVE_REPEAT_DELAY = 150
MOVE_REPEAT_INTERVAL = 50

# Scoring
SCORE_SINGLE = 100
SCORE_DOUBLE = 300
SCORE_TRIPLE = 500
SCORE_TETRIS = 800
SCORE_SOFT_DROP = 1

# Level progression
LINES_PER_LEVEL = 10
SPEED_INCREASE = 0.9  # Multiply fall speed by this each level