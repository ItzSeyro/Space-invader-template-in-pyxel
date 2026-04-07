"""
simple Space Invader clone built with Pyxel.
Modular and configurable for easy customization.

Controls:
- LEFT/RIGHT or A/D: Move player
- SPACE: Fire
- R: Restart (when game over)
- Q: Quit
"""

import pyxel
import config
from entities import Player, Enemy, PlayerBullet, EnemyBullet, Explosion


class Game:
    """Main game class handling all game logic."""
    
    def __init__(self):
        """Initialize the game window and state."""
        pyxel.init(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, title="Space Invader By Seyro")
        self.reset_game()
        pyxel.run(self.update, self.draw)
    
    def reset_game(self):
        """Reset all game variables for a new game."""
        self.state = "playing"
        self.score = 0
        self.lives = config.LIVES
        self.level = config.START_LEVEL
        self.formation = config.DEFAULT_FORMATION
        
        self.player = Player()
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        
        self.enemy_direction = 1
        self.enemy_speed = config.ENEMY_SPEED
        self.enemy_fire_timer = 0
        
        self.create_enemies()
    
    def create_enemies(self):
        """Create enemy formation based on current level and formation type."""
        self.enemies.clear()
        spacing_x = 20
        spacing_y = 15
        start_x = (config.SCREEN_WIDTH - (config.ENEMY_COLS - 1) * spacing_x) // 2
        start_y = 20 + (self.level - 1) * 5
        
        for row in range(config.ENEMY_ROWS):
            for col in range(config.ENEMY_COLS):
                if self.formation == "diamond":
                    offset = abs(col - config.ENEMY_COLS // 2)
                    x = start_x + col * spacing_x
                    y = start_y + row * spacing_y + offset * 3
                elif self.formation == "circle":
                    center_col = config.ENEMY_COLS // 2
                    offset = abs(col - center_col)
                    x = start_x + col * spacing_x
                    y = start_y + row * spacing_y + offset * 5
                else:
                    x = start_x + col * spacing_x
                    y = start_y + row * spacing_y
                
                self.enemies.append(Enemy(x, y, self.formation))
    
    def update(self):
        """Main update loop - called every frame."""
        if self.state == "gameover":
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            return
        
        self.update_player()
        self.update_enemies()
        self.update_bullets()
        self.update_explosions()
        self.check_collisions()
        self.check_game_over()
    
    def update_player(self):
        """Update player state."""
        self.player.update(self.player_bullets)
        if not self.player.alive:
            self.lives -= 1
            if self.lives > 0:
                self.player.alive = True
                self.player.x = config.SCREEN_WIDTH // 2
            else:
                self.state = "gameover"
    
    def update_enemies(self):
        """Update enemy positions and handle movement logic."""
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(self.enemy_direction, self.enemy_speed)
        
        hit_edge = False
        for enemy in self.enemies:
            if enemy.alive:
                if enemy.x <= enemy.width // 2 + 2:
                    hit_edge = True
                    break
                if enemy.x >= config.SCREEN_WIDTH - enemy.width // 2 - 2:
                    hit_edge = True
                    break
        
        if hit_edge:
            self.enemy_direction *= -1
            self.enemy_speed += config.ENEMY_SPEED_INCREMENT
            for enemy in self.enemies:
                if enemy.alive:
                    enemy.y += config.ENEMY_DROP_AMOUNT
        
        self.enemy_fire_timer += 1
        if self.enemy_fire_timer >= config.ENEMY_FIRE_RATE:
            alive_enemies = [e for e in self.enemies if e.alive]
            if alive_enemies:
                shooter = alive_enemies[pyxel.rndi(0, len(alive_enemies) - 1)]
                self.enemy_bullets.append(EnemyBullet(shooter.x, shooter.y + 4))
            self.enemy_fire_timer = 0
    
    def update_bullets(self):
        """Update all bullets."""
        for bullet in self.player_bullets:
            bullet.update()
        self.player_bullets = [b for b in self.player_bullets if b.active]
        
        for bullet in self.enemy_bullets:
            bullet.update()
        self.enemy_bullets = [b for b in self.enemy_bullets if b.active]
    
    def update_explosions(self):
        """Update all explosions."""
        for explosion in self.explosions:
            explosion.update()
        self.explosions = [e for e in self.explosions if e.active]
    
    def check_collisions(self):
        """Check all collision detection."""
        self.check_player_bullet_collisions()
        self.check_enemy_bullet_collisions()
    
    def check_player_bullet_collisions(self):
        """Check if player bullets hit enemies."""
        for bullet in self.player_bullets:
            if not bullet.active:
                continue
            
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                
                if (abs(bullet.x - enemy.x) < enemy.width // 2 + bullet.width // 2 and
                    abs(bullet.y - enemy.y) < enemy.height // 2 + bullet.height // 2):
                    bullet.active = False
                    enemy.alive = False
                    self.score += config.ENEMY_SCORE
                    self.explosions.append(Explosion(enemy.x, enemy.y))
                    break
        
        self.check_level_complete()
    
    def check_enemy_bullet_collisions(self):
        """Check if enemy bullets hit the player."""
        if not self.player.alive:
            return
        
        for bullet in self.enemy_bullets:
            if not bullet.active:
                continue
            
            if (abs(bullet.x - self.player.x) < self.player.width // 2 + bullet.width // 2 and
                abs(bullet.y - self.player.y) < self.player.height // 2 + bullet.height // 2):
                bullet.active = False
                self.player.alive = False
                self.explosions.append(Explosion(self.player.x, self.player.y))
                break
    
    def check_level_complete(self):
        """Check if all enemies are destroyed."""
        alive_enemies = [e for e in self.enemies if e.alive]
        if not alive_enemies:
            self.level += 1
            self.enemy_speed = config.ENEMY_SPEED + (self.level - 1) * 0.2
            
            formations = config.ENEMY_FORMATIONS
            self.formation = formations[(self.level - 1) % len(formations)]
            
            self.create_enemies()
            self.player_bullets.clear()
            self.enemy_bullets.clear()
    
    def check_game_over(self):
        """Check if game should end."""
        for enemy in self.enemies:
            if enemy.alive and enemy.y >= config.SCREEN_HEIGHT - 30:
                self.state = "gameover"
                return
        
        if self.lives <= 0:
            self.state = "gameover"
    
    def draw(self):
        """Main draw loop - called every frame."""
        pyxel.cls(config.BACKGROUND_COLOR)
        
        if self.state == "gameover":
            self.draw_game_over()
            return
        
        self.draw_ui()
        self.player.draw()
        
        for enemy in self.enemies:
            enemy.draw()
        
        for bullet in self.player_bullets:
            bullet.draw()
        
        for bullet in self.enemy_bullets:
            bullet.draw()
        
        for explosion in self.explosions:
            explosion.draw()
    
    def draw_ui(self):
        """Draw HUD elements."""
        pyxel.text(config.SCORE_DISPLAY_X, config.SCORE_DISPLAY_Y, f"SCORE: {self.score}", 7)
        pyxel.text(config.LIVES_DISPLAY_X, config.LIVES_DISPLAY_Y, f"LIVES: {self.lives}", 7)
        pyxel.text(config.LEVEL_DISPLAY_X, config.LEVEL_DISPLAY_Y, f"LVL: {self.level}", 7)
        pyxel.text(5, config.SCREEN_HEIGHT - 10, "ARROWS:MOVE SPACE:FIRE", 3)
    
    def draw_game_over(self):
        """Draw game over screen."""
        pyxel.text(config.SCREEN_WIDTH // 2 - 20, config.SCREEN_HEIGHT // 2 - 10, "GAME OVER", 8)
        pyxel.text(config.SCREEN_WIDTH // 2 - 25, config.SCREEN_HEIGHT // 2, f"SCORE: {self.score}", 7)
        pyxel.text(config.SCREEN_WIDTH // 2 - 30, config.SCREEN_HEIGHT // 2 + 10, "PRESS R TO RESTART", 7)
        pyxel.text(config.SCREEN_WIDTH // 2 - 20, config.SCREEN_HEIGHT // 2 + 20, "Q TO QUIT", 7)


if __name__ == "__main__":
    Game()
