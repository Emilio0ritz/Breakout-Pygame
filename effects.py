"""Central configuration. All tunable values live here."""

# Window
WIDTH, HEIGHT = 900, 640
FPS = 60
TITLE = "Breakout"

# Colors (R, G, B)
BG_COLOR = (16, 18, 26)
WHITE = (235, 238, 245)
ACCENT = (120, 200, 255)
PADDLE_COLOR = (235, 238, 245)
BALL_COLOR = (255, 214, 102)
BRICK_ROWS_COLORS = [
    (239, 83, 80),   # red
    (255, 167, 38),  # orange
    (255, 213, 79),  # yellow
    (102, 187, 106), # green
    (66, 165, 245),  # blue
]

# Paddle
PADDLE_W, PADDLE_H = 110, 14
PADDLE_SPEED = 540  # px/sec
PADDLE_Y_OFFSET = 40  # distance from bottom

# Ball
BALL_RADIUS = 8
BALL_SPEED = 380       # px/sec
BALL_SPEED_MAX = 620
BALL_SPEEDUP = 1.03    # multiplier per brick hit

# Bricks
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_H = 26
BRICK_GAP = 6
BRICK_TOP = 70

# Scoring / lives
POINTS_PER_BRICK = 10
START_LIVES = 3

# Effects
SHAKE_BRICK = 4      # screen shake magnitude on brick hit
SHAKE_DEATH = 12     # on losing a ball
PARTICLES_PER_BRICK = 14
