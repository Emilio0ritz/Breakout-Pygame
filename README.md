"""Game feel: particles, screen shake, and synthesized sound (no asset files needed)."""
import math
import random

import numpy as np
import pygame

import config as C


# ---------------------------------------------------------------- particles
class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(60, 260)
        self.x, self.y = x, y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(0.25, 0.6)
        self.age = 0.0
        self.color = color
        self.size = random.randint(2, 4)

    def update(self, dt):
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 500 * dt  # gravity

    @property
    def dead(self):
        return self.age >= self.life

    def draw(self, surf):
        fade = max(0.0, 1.0 - self.age / self.life)
        col = tuple(int(c * fade) for c in self.color)
        pygame.draw.rect(surf, col, (int(self.x), int(self.y), self.size, self.size))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def burst(self, x, y, color, n=C.PARTICLES_PER_BRICK):
        self.particles.extend(Particle(x, y, color) for _ in range(n))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if not p.dead]

    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)


# ---------------------------------------------------------------- screen shake
class ScreenShake:
    def __init__(self):
        self.magnitude = 0.0

    def kick(self, amount):
        self.magnitude = max(self.magnitude, amount)

    def update(self, dt):
        self.magnitude = max(0.0, self.magnitude - 30 * dt)

    @property
    def offset(self):
        if self.magnitude <= 0:
            return 0, 0
        m = self.magnitude
        return random.uniform(-m, m), random.uniform(-m, m)


# ---------------------------------------------------------------- sound
def _tone(freq, duration, volume=0.4, sample_rate=22050, shape="sine"):
    """Synthesize a short tone as a pygame Sound (stereo int16)."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    if shape == "square":
        wave = np.sign(np.sin(2 * np.pi * freq * t))
    else:
        wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-4 * t / duration)  # quick decay, softer click
    samples = (wave * envelope * volume * 32767).astype(np.int16)
    stereo = np.column_stack([samples, samples])
    return pygame.sndarray.make_sound(np.ascontiguousarray(stereo))


class Sounds:
    """All audio synthesized at startup - the repo ships zero binary assets."""

    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2)
            self.brick = _tone(660, 0.07, shape="square", volume=0.25)
            self.paddle = _tone(330, 0.06, volume=0.3)
            self.wall = _tone(220, 0.05, volume=0.2)
            self.death = _tone(110, 0.4, volume=0.4)
            self.win = _tone(880, 0.5, volume=0.35)
        except pygame.error:
            self.enabled = False  # no audio device; play silently

    def play(self, name):
        if self.enabled:
            getattr(self, name).play()
