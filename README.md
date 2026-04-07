# Space Invader Template

A simple, modular Space Invader game built with [Pyxel](https://github.com/kitao/pyxel), a retro game engine for Python.

## Features

- Modular architecture (entities, config, game logic separated)
- Configurable settings in `config.py`
- Multiple enemy formations (classic, diamond, circle)
- Progressive difficulty (speed increases per level)

## Controls

| Key | Action |
|-----|--------|
| ← → or A/D | Move player |
| SPACE | Fire |
| R | Restart (game over) |
| Q | Quit |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Configuration

Edit `config.py` to customize:

```python
# Game settings
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 180
LIVES = 3

# Player settings
PLAYER_SPEED = 2
PLAYER_COLOR = 7
PLAYER_FIRE_RATE = 15

# Enemy settings
ENEMY_ROWS = 3
ENEMY_COLS = 8
ENEMY_SPEED = 0.5
ENEMY_SCORE = 10

# Enemy formations: "classic", "diamond", "circle"
DEFAULT_FORMATION = "classic"
```

## Project Structure

```
space-invader/
├── config.py       # All configurable settings
├── entities.py     # Game entities (Player, Enemy, Bullets, Explosion)
├── main.py         # Main game loop and logic
├── requirements.txt
├── LICENSE
├── README.md
└── .gitignore
```

## License

MIT License - feel free to use and modify!
