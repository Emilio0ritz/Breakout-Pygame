# Breakout

A small, finished arcade game built with **Python + PyGame** to demonstrate game-loop fundamentals: fixed-timestep updates, collision handling, a state machine, and "game feel" effects.

![Gameplay](screenshot.png)

## Run It

    pip install -r requirements.txt
    python main.py

**Controls:** ← / → or A / D to move · SPACE to launch · R to restart

## What's Inside

| File | Responsibility |
|------|----------------|
| `main.py` | Entry point |
| `game.py` | State machine (ready / playing / game over / win) and the update–draw loop |
| `entities.py` | Paddle, ball, and brick wall — movement and collision response |
| `effects.py` | Particles, screen shake, and runtime-synthesized sound (zero binary assets) |
| `config.py` | Every tunable value in one place |

## Design Notes

- **Delta-time movement** with a clamped timestep so physics stay stable through lag spikes
- **Angle-based paddle bounces** — where the ball strikes the paddle controls the exit angle
- **Axis-of-least-penetration brick collision** for believable side vs. top bounces
- **Juice**: screen shake, particle bursts on brick destruction, and per-hit ball speedup
- **All audio is synthesized at startup** with NumPy waveforms — the repo ships no asset files

Built in a weekend to demonstrate game-loop fundamentals across engines I'm actively learning (PyGame → Godot).
