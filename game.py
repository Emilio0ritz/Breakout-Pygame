"""Game entities: Paddle, Ball, Brick."""
import math
import random

import pygame

import config as C


class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, C.PADDLE_W, C.PADDLE_H)
        self.rect.centerx = C.WIDTH // 2
        self.rect.bottom = C.HEIGHT - C.PADDLE_Y_OFFSET
        self.vx = 0.0

    def update(self, dt, keys):
        self.vx = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -C.PADDLE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = C.PADDLE_SPEED
        self.rect.x += round(self.vx * dt)
        self.rect.clamp_ip(pygame.Rect(0, 0, C.WIDTH, C.HEIGHT))

    def draw(self, surf):
        pygame.draw.rect(surf, C.PADDLE_COLOR, self.rect, border_radius=7)


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = C.WIDTH / 2
        self.y = C.HEIGHT / 2
        angle = random.uniform(math.radians(225), math.radians(315))  # downward
        self.vx = math.cos(angle) * C.BALL_SPEED
        self.vy = -math.sin(angle) * C.BALL_SPEED
        self.speed = C.BALL_SPEED

    def speed_up(self):
        self.speed = min(self.speed * C.BALL_SPEEDUP, C.BALL_SPEED_MAX)
        mag = math.hypot(self.vx, self.vy) or 1.0
        self.vx = self.vx / mag * self.speed
        self.vy = self.vy / mag * self.speed

    def bounce_off_paddle(self, paddle):
        """Reflect upward; exit angle depends on where the ball hit the paddle."""
        offset = (self.x - paddle.rect.centerx) / (paddle.rect.width / 2)
        offset = max(-1.0, min(1.0, offset))
        angle = math.radians(90 - abs(offset) * 60)  # up to 60 degrees off vertical
        self.vx = math.copysign(math.cos(angle) * self.speed, offset or self.vx)
        self.vy = -abs(math.sin(angle)) * self.speed
        self.y = paddle.rect.top - C.BALL_RADIUS

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Wall bounces
        if self.x - C.BALL_RADIUS <= 0:
            self.x = C.BALL_RADIUS
            self.vx = abs(self.vx)
        elif self.x + C.BALL_RADIUS >= C.WIDTH:
            self.x = C.WIDTH - C.BALL_RADIUS
            self.vx = -abs(self.vx)
        if self.y - C.BALL_RADIUS <= 0:
            self.y = C.BALL_RADIUS
            self.vy = abs(self.vy)

    @property
    def rect(self):
        r = C.BALL_RADIUS
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)

    def draw(self, surf):
        pygame.draw.circle(surf, C.BALL_COLOR, (int(self.x), int(self.y)), C.BALL_RADIUS)


class Brick:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color
        self.alive = True

    def draw(self, surf):
        if self.alive:
            pygame.draw.rect(surf, self.color, self.rect, border_radius=4)


def build_brick_wall():
    bricks = []
    total_gap = C.BRICK_GAP * (C.BRICK_COLS + 1)
    brick_w = (C.WIDTH - total_gap) // C.BRICK_COLS
    for row in range(C.BRICK_ROWS):
        color = C.BRICK_ROWS_COLORS[row % len(C.BRICK_ROWS_COLORS)]
        for col in range(C.BRICK_COLS):
            x = C.BRICK_GAP + col * (brick_w + C.BRICK_GAP)
            y = C.BRICK_TOP + row * (C.BRICK_H + C.BRICK_GAP)
            bricks.append(Brick(pygame.Rect(x, y, brick_w, C.BRICK_H), color))
    return bricks
