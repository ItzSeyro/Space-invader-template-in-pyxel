"""
Game entities (Player, Enemy, Bullet, Explosion).
"""

import pyxel
import config


class Player:
    """Represents the player's spaceship."""
    
    def __init__(self):
        self.x = config.SCREEN_WIDTH // 2
        self.y = config.SCREEN_HEIGHT - 20
        self.width = config.PLAYER_WIDTH
        self.height = config.PLAYER_HEIGHT
        self.speed = config.PLAYER_SPEED
        self.color = config.PLAYER_COLOR
        self.alive = True
        self.fire_timer = 0
        self.fire_rate = config.PLAYER_FIRE_RATE
    
    def update(self, bullets):
        """Update player position and handle shooting."""
        if not self.alive:
            return
        
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.x += self.speed
        
        self.x = pyxel.clamp(self.x, self.width // 2, config.SCREEN_WIDTH - self.width // 2)
        
        self.fire_timer += 1
        if pyxel.btn(pyxel.KEY_SPACE) and self.fire_timer >= self.fire_rate:
            bullets.append(PlayerBullet(self.x, self.y - self.height // 2))
            self.fire_timer = 0
    
    def draw(self):
        """Draw the player ship."""
        if not self.alive:
            return
        
        pyxel.circ(self.x, self.y, 3, self.color)
        pyxel.rect(self.x - 4, self.y + 2, 8, 4, self.color)


class Enemy:
    """Represents an enemy alien."""
    
    def __init__(self, x, y, formation="classic"):
        self.x = x
        self.y = y
        self.width = config.ENEMY_WIDTH
        self.height = config.ENEMY_HEIGHT
        self.color = config.ENEMY_COLOR
        self.alive = True
        self.formation = formation
    
    def update(self, direction, speed):
        """Update enemy position."""
        self.x += direction * speed
    
    def draw(self):
        """Draw the enemy."""
        if not self.alive:
            return
        
        pyxel.rect(self.x - 4, self.y - 4, 8, 8, self.color)
        pyxel.rect(self.x - 6, self.y - 2, 2, 4, self.color)
        pyxel.rect(self.x + 4, self.y - 2, 2, 4, self.color)
        pyxel.pset(self.x - 2, self.y - 6, self.color)
        pyxel.pset(self.x + 2, self.y - 6, self.color)


class PlayerBullet:
    """Bullet fired by the player."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = config.BULLET_WIDTH
        self.height = config.BULLET_HEIGHT
        self.speed = config.BULLET_SPEED
        self.color = config.BULLET_COLOR
        self.active = True
    
    def update(self):
        """Move bullet upward."""
        self.y -= self.speed
        if self.y < 0:
            self.active = False
    
    def draw(self):
        """Draw the bullet."""
        pyxel.rect(self.x - 1, self.y, self.width, self.height, self.color)


class EnemyBullet:
    """Bullet fired by enemies."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = config.BULLET_WIDTH
        self.height = config.BULLET_HEIGHT
        self.speed = config.ENEMY_BULLET_SPEED
        self.color = config.ENEMY_BULLET_COLOR
        self.active = True
    
    def update(self):
        """Move bullet downward."""
        self.y += self.speed
        if self.y > config.SCREEN_HEIGHT:
            self.active = False
    
    def draw(self):
        """Draw the bullet."""
        pyxel.rect(self.x - 1, self.y - self.height, self.width, self.height, self.color)


class Explosion:
    """Visual explosion effect when enemies are destroyed."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.max_frames = config.EXPLOSION_DURATION
        self.color = config.EXPLOSION_COLOR
        self.active = True
    
    def update(self):
        """Update explosion animation."""
        self.frame += 1
        if self.frame >= self.max_frames:
            self.active = False
    
    def draw(self):
        """Draw explosion effect."""
        radius = self.frame // 2 + 1
        pyxel.circ(self.x, self.y, radius, self.color)
