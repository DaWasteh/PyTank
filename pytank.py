import pygame
import random
import math
import sys
import threading
from enum import Enum

# ============================================================================
# KONFIGURATION
# ============================================================================
class Config:
    # Spielfeld
    WIDTH = 1600
    HEIGHT = 1200
    GRID_SIZE = 50
    FPS = 60

    # Farben
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_P1 = (255, 255, 0)  # Yellow
    COLOR_P2 = (0, 255, 0)    # Green
    COLOR_ENEMY = (255, 0, 0) # Red
    COLOR_BRICK = (139, 69, 19)
    COLOR_STEEL = (169, 169, 169)
    COLOR_EAGLE = (255, 215, 0)
    COLOR_TEXT = (255, 255, 255)
    COLOR_PARTICLE = (255, 165, 0)

    # Gameplay
    PLAYER_SPEED = 4
    BULLET_SPEED = 7
    ENEMY_SPEED = 2
    ENEMY_HP = 2
    MAX_LIVES = 3
    ENEMY_SPAWN_INTERVAL = 60  # Frames (1 Sekunde)
    WAVE_INTERVAL = 3600       # Frames (60 Sekunden)
    TOTAL_WAVES = 10

    # Score
    START_SCORE = 0
    ENEMY_SCORE = 100
    BRICK_SCORE = 10
    STEEL_SCORE = 50
    WAVE_SCORE = 500

    # Map Settings
    MAPS = {
        "classic": {"name": "Classic", "type": "symmetric"},
        "industrial": {"name": "Industrial", "steel_ratio": 0.4},
        "desert": {"name": "Desert", "brick_ratio": 0.6}
    }

    # Wave Settings
    TOTAL_WAVES = 10
    BOSS_WAVE = 10  # Boss-Welle am Ende
    TIME_LIMIT = 300  # Sekunden (5 Minuten)

    # Respawn Settings
    RESPAWN_COOLDOWN = 3  # Sekunden

    # Enemy Types
    SCOUT_SPEED = 3
    SCOUT_HP = 1
    SCOUT_SPAWN_CHANCE = 0.3

    GUNNER_SPEED = 2
    GUNNER_HP = 2
    GUNNER_SPAWN_CHANCE = 0.5

    BRUTE_SPEED = 1
    BRUTE_HP = 4
    BRUTE_SPAWN_CHANCE = 0.2

    # Powerups
    POWERUP_SPAWN_CHANCE = 0.1
    SHIELD_MAX_CHARGES = 3
    DOUBLE_SHOOT_DURATION = 15  # Sekunden
    REPAIR_AMOUNT = 50  # +50% Health statt fester Wert

    # Sound Settings (Hochwertige synthetisierte Sounds)
    SOUND_SAMPLE_RATE = 48000
    MUSIC_VOLUME = 0.25       # Standard Lautstärke Musik (0.0 - 1.0)
    SFX_VOLUME = 0.6          # Standard Lautstärke SFX (0.0 - 1.0)
    MAX_SOUNDS = 32           # Mehr Kanäle für komplexe Sounds
    VOLUME_SLIDER_HEIGHT = 18 # Höhe der Lautstärkeregler
    VOLUME_SLIDER_WIDTH = 120 # Breite der Lautstärkeregler

# ============================================================================
# ENUMS
# ============================================================================
class GameState:
    MENU = "MENU"
    MAIN_MENU = "MAIN_MENU"
    LEVEL_SELECT = "LEVEL_SELECT"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"
    VICTORY = "VICTORY"

class GameMode:
    FFA = "FFA"
    HORDE = "HORDE"
    COOP = "COOP"  # 2-Spieler Koop

class WallType:
    BRICK = "brick"
    STEEL = "steel"

class EnemyState:
    PATROL = "patrol"
    CHASE = "chase"
    ATTACK = "attack"
    RETREAT = "retreat"

# ============================================================================
# BACKGROUND RENDERER
# ============================================================================
class BackgroundRenderer:
    """Zeichnet Hintergrund mit Grid-Muster und subtiler Struktur"""
    def __init__(self, grid_size=50):
        self.grid_size = grid_size
        self.background = None

    def draw(self, surface):
        """Zeichnet den Hintergrund"""
        # Dunkler Blau-Tint statt COLOR_BLACK
        surface.fill((20, 20, 25))

        # Subtiles Grid mit leichtem Glow-Effekt
        for i in range(0, Config.HEIGHT, self.grid_size):
            alpha = int(30 + 20 * math.sin(i / 100))
            color = (40, 40, 50, alpha)
            pygame.draw.line(surface, color, (0, i), (Config.WIDTH, i), 1)

        for i in range(0, Config.WIDTH, self.grid_size):
            alpha = int(30 + 20 * math.cos(i / 100))
            color = (40, 40, 50, alpha)
            pygame.draw.line(surface, color, (i, 0), (i, Config.HEIGHT), 1)

class EagleState:
    PROTECTED = "protected"
    HIT = "hit"

# ============================================================================
# BASE CLASSES
# ============================================================================
class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Entity(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.direction = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)

    def move(self, dx, dy, walls, screen_shake=0):
        # Apply screen shake
        shake_x = random.randint(-screen_shake, screen_shake)
        shake_y = random.randint(-screen_shake, screen_shake)

        # Try moving in X
        self.rect.x += dx + shake_x
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: self.rect.right = wall.rect.left
                elif dx < 0: self.rect.left = wall.rect.right

        # Check screen boundary X
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > Config.WIDTH: self.rect.right = Config.WIDTH

        # Try moving in Y
        self.rect.y += dy + shake_y
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0: self.rect.bottom = wall.rect.top
                elif dy < 0: self.rect.top = wall.rect.bottom

        # Check screen boundary Y
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > Config.HEIGHT: self.rect.bottom = Config.HEIGHT

# ============================================================================
# GAME OBJECTS
# ============================================================================
class Wall(GameObject):
    def __init__(self, x, y, width, height, wall_type):
        if wall_type == WallType.BRICK:
            color = Config.COLOR_BRICK
            destructible = True
        else:
            color = Config.COLOR_STEEL
            destructible = False
        super().__init__(x, y, width, height, color)
        self.wall_type = wall_type
        self.destructible = destructible
        self.pattern = 0

    def draw(self, surface):
        """Zeichnet Wand mit verbessertem Pattern"""
        if self.wall_type == WallType.BRICK:
            # Schachbrett-Muster mit Textur
            pygame.draw.rect(surface, Config.COLOR_BRICK, self.rect)
            pygame.draw.rect(surface, (101, 67, 17), self.rect, 1)

            # Schachbrett-Linien mit Variation
            for i in range(0, self.rect.width, 10):
                line_color = (80 + random.randint(0, 40), 50 + random.randint(0, 30), 10 + random.randint(0, 20))
                pygame.draw.line(surface, line_color,
                               (self.rect.x + i, self.rect.y),
                               (self.rect.x + i, self.rect.y + self.rect.height), 1)

            for i in range(0, self.rect.height, 10):
                line_color = (80 + random.randint(0, 40), 50 + random.randint(0, 30), 10 + random.randint(0, 20))
                pygame.draw.line(surface, line_color,
                               (self.rect.x, self.rect.y + i),
                               (self.rect.x + self.rect.width, self.rect.y + i), 1)
        else:
            # Gitter-Muster für Stahl mit Metallic-Effekt
            pygame.draw.rect(surface, Config.COLOR_STEEL, self.rect)
            pygame.draw.rect(surface, (127, 127, 127), self.rect, 1)

            # Gitter-Linien mit Variation
            for i in range(0, self.rect.width, 15):
                line_color = (100 + random.randint(0, 60), 100 + random.randint(0, 60), 100 + random.randint(0, 60))
                pygame.draw.line(surface, line_color,
                               (self.rect.x + i, self.rect.y),
                               (self.rect.x + i, self.rect.y + self.rect.height), 1)

            for i in range(0, self.rect.height, 15):
                line_color = (100 + random.randint(0, 60), 100 + random.randint(0, 60), 100 + random.randint(0, 60))
                pygame.draw.line(surface, line_color,
                               (self.rect.x, self.rect.y + i),
                               (self.rect.x + self.rect.width, self.rect.y + i), 1)

class Bullet(GameObject):
    def __init__(self, x, y, direction, color, owner, trail_length=10):
        super().__init__(x, y, 8, 8, color)
        self.direction = direction
        self.owner = owner
        self.trail = []
        self.trail_length = trail_length

    def update(self, walls):
        # Bewegen
        self.rect.x += self.direction.x * Config.BULLET_SPEED
        self.rect.y += self.direction.y * Config.BULLET_SPEED

        # Update trail
        self.trail.append((self.rect.centerx, self.rect.centery))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

        # Check screen boundary
        if not (0 <= self.rect.x <= Config.WIDTH and 0 <= self.rect.y <= Config.HEIGHT):
            return "out_of_bounds"

        # Check wall collision
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if wall.destructible:
                    return wall
                return "hit_wall"
        return None

    def draw_with_trail(self, surface):
        # Draw trail with improved effects
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / self.trail_length) * 0.7)
            color = (*self.color[:3], alpha)
            size = int(3 * (i / self.trail_length))
            pygame.draw.circle(surface, color, (tx, ty), max(1, size))

        # Draw bullet with glow effect
        pygame.draw.circle(surface, self.color, (self.rect.centerx, self.rect.centery), 4)
        glow_color = (*self.color[:3], 100)
        pygame.draw.circle(surface, glow_color, (self.rect.centerx, self.rect.centery), 6)

class Powerup(GameObject):
    """Powerup-Objekt mit verbessertem Design"""
    SHIELD = "shield"
    DOUBLE_SHOT = "double_shot"
    REPAIR = "repair"

    def __init__(self, x, y, powerup_type):
        super().__init__(x, y, 20, 20, (255, 255, 0))
        self.powerup_type = powerup_type
        self.pulse = 0
        self.hitbox = pygame.Rect(x - 15, y - 15, 30, 30)

        # Typ-spezifische Farben und Symbole
        if powerup_type == Powerup.SHIELD:
            self.color = (0, 255, 255)  # Cyan
            self.symbol = "🛡️"
        elif powerup_type == Powerup.DOUBLE_SHOT:
            self.color = (255, 215, 0)  # Gold
            self.symbol = "⚡"
        else:  # REPAIR
            self.color = (255, 165, 0)  # Orange
            self.symbol = "❤️"

    def update(self):
        """Update Powerup"""
        self.pulse += 0.1

    def draw(self, surface):
        """Zeichnet Powerup mit verbessertem Puls-Effekt"""
        pulse_size = 10 + int(self.pulse * 5)

        # Pulsierender Hintergrund mit Glow
        alpha = int(100 + 100 * math.sin(pygame.time.get_ticks() / 200))
        color = (*self.color[:3], alpha)
        pygame.draw.circle(surface, color, (int(self.rect.centerx), int(self.rect.centery)), pulse_size)

        # Powerup-Symbol mit Schatten
        pygame.draw.circle(surface, (0, 0, 0, 150), (int(self.rect.centerx) + 2, int(self.rect.centery) + 2), 10)
        pygame.draw.circle(surface, self.color, (int(self.rect.centerx), int(self.rect.centery)), 10)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.rect.centerx), int(self.rect.centery)), 5)

        # Symbol rendern
        font = pygame.font.SysFont(None, 24)
        symbol_surface = font.render(self.symbol, True, (255, 255, 255))
        surface.blit(symbol_surface, (int(self.rect.centerx) - symbol_surface.get_width()//2,
                                    int(self.rect.centery) - symbol_surface.get_height()//2))

class Eagle(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, Config.COLOR_EAGLE)
        self.state = EagleState.PROTECTED

    def draw_adler(self, surface):
        if self.state == EagleState.HIT:
            # Zerstörtes Adler-Symbol (grau)
            pygame.draw.rect(surface, (100, 100, 100), self.rect)
            return

        # 4-Flügel Adler-Symbol mit verbessertem Design
        cx, cy = self.rect.centerx, self.rect.centery
        wing_size = 12

        # Flügel mit Textur
        pygame.draw.polygon(surface, Config.COLOR_EAGLE, [
            (cx, cy), (cx - wing_size, cy - wing_size), (cx - wing_size * 2, cy),
            (cx - wing_size, cy + wing_size), (cx, cy + wing_size * 2),
            (cx + wing_size, cy + wing_size), (cx + wing_size * 2, cy),
            (cx + wing_size, cy - wing_size)
        ])

        # Körper mit Glow-Effekt
        pygame.draw.circle(surface, Config.COLOR_EAGLE, (cx, cy), 8)
        glow_color = (*Config.COLOR_EAGLE[:3], 150)
        pygame.draw.circle(surface, glow_color, (cx, cy), 10, 1)

        # Schutzring mit Puls-Effekt
        pulse = int(2 * math.sin(pygame.time.get_ticks() / 300))
        pygame.draw.circle(surface, (255, 255, 200), (cx, cy), 10 + pulse, 1)

class Particle(GameObject):
    """Partikel-Effekt für Explosionen mit verbessertem Design"""
    def __init__(self, x, y, color, vx, vy, life):
        super().__init__(x, y, 2, 2, color)
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life

    def update(self):
        """Update Partikel"""
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life -= 1

        if (self.rect.x < -10 or self.rect.x > Config.WIDTH + 10 or
            self.rect.y < -10 or self.rect.y > Config.HEIGHT + 10):
            self.life = 0

    def draw(self, surface):
        """Zeichnet Partikel mit verbessertem Effekt"""
        alpha = int(255 * (self.life / self.max_life))
        color = (*self.color[:3], alpha)
        size = int(2 * (self.life / self.max_life))

        pygame.draw.circle(surface, color, (int(self.rect.centerx), int(self.rect.centery)), size)

# ============================================================================
# SOUND MANAGER (Hochwertige synthetisierte Sounds)
# ============================================================================
class SoundManager:
    """Hochwertiges Audio-System mit synthetisierten 32/64 Bit Sounds"""

    def __init__(self):
        pygame.mixer.init(frequency=Config.SOUND_SAMPLE_RATE, size=-16, channels=Config.MAX_SOUNDS, buffer=4096)
        self._music_playing = False
        self._music_thread = None
        self._music_volume = Config.MUSIC_VOLUME
        self._sfx_volume = Config.SFX_VOLUME
        self._duck_timer = 0

        # Sound-Variationen für natürliche Variation
        self._shoot_variations = 5
        self._brick_variations = 5
        self._steel_variations = 4
        self._tank_variations = 6
        self._current_shoot = 0
        self._current_brick = 0
        self._current_steel = 0
        self._current_tank = 0

    def set_music_volume(self, volume: float):
        """Setzt die Musiklautstärke (0.0 = stumm, 1.0 = maximal)"""
        self._music_volume = max(0.0, min(1.0, volume))
        Config.MUSIC_VOLUME = self._music_volume

    def set_sfx_volume(self, volume: float):
        """Setzt die SFX-Lautstärke (0.0 = stumm, 1.0 = maximal)"""
        self._sfx_volume = max(0.0, min(1.0, volume))
        Config.SFX_VOLUME = self._sfx_volume

    def get_music_volume(self) -> float:
        return self._music_volume

    def get_sfx_volume(self) -> float:
        return self._sfx_volume

    def _get_sfx_volume(self, base_volume: float = 0.3) -> float:
        """Ermittelt effektive SFX-Lautstärke"""
        return min(1.0, base_volume * self._sfx_volume * 2.0)

    def _synthesize_wave(self, samples: list, wave_type: str, frequency: float,
                         duration_ms: float, volume: float, fade_out: float = 0.15):
        """Synthetisiert einen Wellen-Zyklus mit weichen, natürlichen Klängen"""
        sample_rate = pygame.mixer.get_init()[0]
        num_samples = int(sample_rate * duration_ms / 1000)

        # ADSR-Envelope für natürliche Sounds
        attack_ms = max(5, duration_ms * 0.02)
        attack_samples = int(sample_rate * attack_ms / 1000)
        release_samples = int(sample_rate * fade_out / 1000)

        output = []
        for i in range(num_samples):
            # Sanfte Envelope
            if i < attack_samples:
                env = i / attack_samples
            elif i > num_samples - release_samples:
                env = (num_samples - i) / release_samples
            else:
                env = 1.0

            time = i / sample_rate
            phase = 2 * math.pi * frequency * time

            # Weiche Wellenformen (keine harten Square waves)
            if wave_type == 'square':
                val = math.tanh(math.sin(phase)) * 0.8
            elif wave_type == 'sawtooth':
                raw = 2.0 * ((frequency * time) % 1.0) - 1.0
                val = math.tanh(raw * 0.5)
            elif wave_type == 'triangle':
                val = 2.0 * abs(2.0 * ((frequency * time) % 1.0) - 1.0) - 1.0
            elif wave_type == 'square8':
                duty = 0.3 + 0.2 * math.sin(phase * 0.3)
                val = (1.0 if (phase % (2 * math.pi)) / (2 * math.pi) < duty else -1.0)
                val = math.tanh(val * 0.4)
            else:
                val = math.sin(phase)

            sample = int(32767 * volume * env * val)
            sample = max(-32767, min(32767, sample))
            output.append(((sample + 32767) * 255) // 65534)

        return pygame.mixer.Sound(bytes(output))

    def _synthesize_noise(self, duration_ms: float, volume: float,
                          lowpass: float = 200, noise_type: str = 'white'):
        """Synthetisiert Rauschen mit Lowpass-Filter für natürliche Explosionen"""
        sample_rate = pygame.mixer.get_init()[0]
        num_samples = int(sample_rate * duration_ms / 1000)

        # Filter-State
        prev = 0.0
        cutoff = lowpass / sample_rate

        output = []
        for i in range(num_samples):
            time = i / sample_rate

            # ADSR-Envelope
            attack_s = int(sample_rate * 0.003)
            release_s = int(sample_rate * duration_ms / 2000)

            if i < attack_s:
                env = i / attack_s
            elif i > num_samples - release_s:
                env = (num_samples - i) / release_s
            else:
                env = 1.0

            # Noise-Quellen
            if noise_type == 'white':
                noise = random.uniform(-1, 1)
            elif noise_type == 'pink':
                noise = random.uniform(-1, 1) * 0.7
            else:
                noise = random.uniform(-1, 1)

            # Lowpass-Filter (IIR)
            filtered = prev * (1 - cutoff) + noise * cutoff
            prev = filtered

            # Sub-Bass für Tiefe
            bass = math.sin(2 * math.pi * 40 * time) * 0.2

            combined = (filtered * 0.5 + bass * 0.5) * volume * env
            combined = max(-1.0, min(1.0, combined))

            sample = int(32767 * combined)
            output.append(((sample + 32767) * 255) // 65534)

        sound = pygame.mixer.Sound(bytes(output))
        return sound

    def play_shoot(self):
        """Natürlicher Schuss-Sound (gedämpft, kurz)"""
        var = self._current_shoot % self._shoot_variations
        self._current_shoot += 1

        vol = self._get_sfx_volume(0.2)

        if var == 0:
            # Kurzes, gedämpftes Knacken
            sound = self._synthesize_noise(60, vol * 0.5, lowpass=800)
        elif var == 1:
            # Tieferer Schuss
            sound = self._synthesize_wave([], 'triangle', 200, 70, vol * 0.4)
            s2 = self._synthesize_noise(50, vol * 0.3, lowpass=1000)
            s2.play()
        elif var == 2:
            # Schneller Impuls
            sound = self._synthesize_wave([], 'triangle', 300, 50, vol * 0.4)
        elif var == 3:
            # Gedämpfter Schuss
            sound = self._synthesize_noise(70, vol * 0.4, lowpass=600)
            s2 = self._synthesize_wave([], 'triangle', 250, 60, vol * 0.3)
            s2.play()
        else:
            # Standard Schuss
            sound = self._synthesize_wave([], 'triangle', 350, 55, vol * 0.4)

        sound.play()
        self._duck_music(0.08)

    def play_brick_destroy(self):
        """Zerstörung einer Ziegelwand - natürliches Knirschen"""
        var = self._current_brick % self._brick_variations
        self._current_brick += 1

        vol = self._get_sfx_volume(0.25)

        if var == 0:
            # Staubiges Knirschen
            sound = self._synthesize_noise(100, vol * 0.5, lowpass=500, noise_type='pink')
        elif var == 1:
            # Kurz und knackig
            sound = self._synthesize_noise(70, vol * 0.4, lowpass=700)
        elif var == 2:
            # Mehrere kleine Bröckel
            sound = self._synthesize_noise(90, vol * 0.4, lowpass=400, noise_type='pink')
            s2 = self._synthesize_wave([], 'triangle', 180, 60, vol * 0.3)
            s2.play()
        elif var == 3:
            # Niedriges Knacken
            sound = self._synthesize_noise(80, vol * 0.45, lowpass=600)
        else:
            # Gemischt
            sound = self._synthesize_noise(110, vol * 0.45, lowpass=450, noise_type='pink')

        sound.play()

    def play_steel_destroy(self):
        """Zerstörung einer Stahlwand - metallisch, aber nicht nervig"""
        var = self._current_steel % self._steel_variations
        self._current_steel += 1

        vol = self._get_sfx_volume(0.3)

        if var == 0:
            # Gedämpftes metallisches Klirren
            sound = self._synthesize_noise(120, vol * 0.4, lowpass=600)
            s2 = self._synthesize_wave([], 'triangle', 150, 150, vol * 0.3)
            s2.play()
        elif var == 1:
            # Tiefes metallisches Surren
            sound = self._synthesize_wave([], 'triangle', 120, 180, vol * 0.4)
            s2 = self._synthesize_noise(100, vol * 0.3, lowpass=500)
            s2.play()
        elif var == 2:
            # Kurzes metallisches Klicken
            sound = self._synthesize_noise(80, vol * 0.4, lowpass=700)
        else:
            # Metallischer Einschlag
            sound = self._synthesize_wave([], 'triangle', 180, 120, vol * 0.35)
            s2 = self._synthesize_noise(100, vol * 0.3, lowpass=600)
            s2.play()

        sound.play()

    def play_tank_explosion(self):
        """Panzer-Zerstörung - tiefe, dumpfe Explosion"""
        var = self._current_tank % self._tank_variations
        self._current_tank += 1

        vol = self._get_sfx_volume(0.35)

        if var == 0:
            # Tiefe Welle + dumpfes Rauschen
            sound = self._synthesize_wave([], 'triangle', 40, 300, vol * 0.5)
            s2 = self._synthesize_noise(250, vol * 0.4, lowpass=120, noise_type='pink')
            s2.play()
        elif var == 1:
            # Mehrere Explosionsschichten
            sound = self._synthesize_noise(200, vol * 0.4, lowpass=150, noise_type='pink')
            s2 = self._synthesize_wave([], 'triangle', 35, 180, vol * 0.35)
            s2.play()
        elif var == 2:
            # Langsame, tiefe Explosion
            sound = self._synthesize_noise(350, vol * 0.45, lowpass=100, noise_type='pink')
            s2 = self._synthesize_wave([], 'triangle', 30, 250, vol * 0.3)
            s2.play()
        elif var == 3:
            # Dynamisch mit Pausen
            sound = self._synthesize_noise(100, vol * 0.4, lowpass=200, noise_type='pink')
            sound.play()
            pygame.time.wait(80)
            s2 = self._synthesize_wave([], 'triangle', 40, 200, vol * 0.35)
            s2.play()
        elif var == 4:
            # Gedämpfte Explosion
            sound = self._synthesize_noise(280, vol * 0.45, lowpass=130, noise_type='pink')
            s2 = self._synthesize_wave([], 'triangle', 45, 220, vol * 0.3)
            s2.play()
        else:
            # Standard Explosion
            sound = self._synthesize_noise(300, vol * 0.45, lowpass=140, noise_type='pink')
            s2 = self._synthesize_wave([], 'triangle', 38, 200, vol * 0.3)
            s2.play()

        sound.play()
        self._duck_music(0.06)

    def play_bullet_hit(self):
        """Kleiner, gedämpfter Einschlag"""
        vol = self._get_sfx_volume(0.15)
        sound = self._synthesize_noise(40, vol * 0.5, lowpass=1000)
        sound.play()

    def play_powerup(self):
        """Sanfte Powerup-Melodie"""
        vol = self._get_sfx_volume(0.15)
        notes = [523, 659, 784, 1046]  # C5, E5, G5, C6
        for i, freq in enumerate(notes):
            s = self._synthesize_wave([], 'triangle', freq, 100, vol * 0.5)
            pygame.time.wait(i * 80)
            s.play()

    def play_music(self):
        """Atmosphärische Hintergrundmusik (leise, nicht aufdringlich)"""
        if self._music_playing:
            return
        self._music_playing = True

        # Sanfte Melodie (C-Dur Pentatonik, langsamer)
        melody = [
            523, 0, 659, 0, 784, 0, 659, 0,
            523, 0, 659, 0, 523, 0, 392, 0,
            392, 0, 440, 0, 392, 0, 330, 0,
            330, 0, 392, 0, 440, 0, 392, 0,
        ]
        bass_line = [
            262, 0, 0, 0, 262, 0, 0, 0,
            330, 0, 0, 0, 262, 0, 0, 0,
            392, 0, 0, 0, 330, 0, 0, 0,
            262, 0, 0, 0, 262, 0, 0, 0,
        ]
        arp_notes = [
            262, 330, 392, 0,
            330, 392, 523, 0,
            392, 440, 494, 0,
            330, 392, 523, 0,
        ]

        note_len = 150  # ms pro Achtelnote (langsamer)

        def play_chiptune_note(freq: float, duration: float, vol: float, wave: str):
            if freq <= 0:
                return
            try:
                s = self._synthesize_wave([], wave, freq, duration, vol)
                s.play()
            except:
                pass

        def music_loop():
            try:
                while self._music_playing:
                    for i in range(0, len(melody), 4):
                        if not self._music_playing:
                            break

                        # Melodie (sehr leise, triangle)
                        for j in range(4):
                            idx = i + j
                            if idx < len(melody):
                                play_chiptune_note(melody[idx], note_len,
                                                   self._music_volume * 0.12, 'triangle')

                        # Bass (sehr leise, triangle)
                        for j in range(4):
                            idx = i + j
                            if idx < len(bass_line):
                                play_chiptune_note(bass_line[idx], note_len,
                                                   self._music_volume * 0.15, 'triangle')

                        # Arpeggio (extrem leise, triangle)
                        for j in range(4):
                            idx = i + j
                            if idx < len(arp_notes):
                                play_chiptune_note(arp_notes[idx], note_len // 2,
                                                   self._music_volume * 0.06, 'triangle')

                        pygame.time.wait(note_len * 4)
            except:
                pass

        self._music_thread = threading.Thread(target=music_loop, daemon=True)
        self._music_thread.start()

    def stop_music(self):
        """Stoppt die Hintergrundmusik"""
        self._music_playing = False
        if self._music_thread and self._music_thread.is_alive():
            self._music_thread.join(timeout=1)

    def play_win(self):
        """Sanfte Triumph-Melodie"""
        vol = self._get_sfx_volume(0.2)
        melody = [523, 659, 784, 1046, 784, 1046, 880]
        durations = [150, 150, 150, 250, 150, 150, 400]

        for i, (freq, dur) in enumerate(zip(melody, durations)):
            s = self._synthesize_wave([], 'triangle', freq, dur, vol * 0.5)
            pygame.time.wait(dur)
            s.play()

    def play_lose(self):
        """Sanfte, traurige Melodie"""
        vol = self._get_sfx_volume(0.15)
        melody = [392, 349, 330, 294, 262, 220, 196]
        durations = [250, 250, 250, 300, 300, 350, 500]

        for i, (freq, dur) in enumerate(zip(melody, durations)):
            s = self._synthesize_wave([], 'triangle', freq, dur, vol * 0.4)
            pygame.time.wait(dur)
            s.play()

    def _duck_music(self, volume: float):
        """Duckt die Musik bei Sound-Effekten"""
        if self._duck_timer == 0:
            self._music_volume = volume
            self._duck_timer = int(0.4 * 60)  # 0.4 Sekunden

    def _update_music_ducking(self):
        """Reduziert Ducking über die Zeit"""
        if self._duck_timer > 0:
            self._duck_timer -= 1
            if self._duck_timer <= 0:
                self._music_volume = Config.MUSIC_VOLUME

# ============================================================================
# PLAYER CLASS
# ============================================================================
class Player:
    def __init__(self, player_id, x, y, color, controls):
        self.player_id = player_id
        self.rect = pygame.Rect(x, y, Config.GRID_SIZE - 10, Config.GRID_SIZE - 10)
        self.color = color
        self.controls = controls
        self.lives = Config.MAX_LIVES
        self.health = Config.MAX_LIVES * 2
        self.score = Config.START_SCORE
        self.direction = pygame.Vector2(0, 0)
        self.last_direction = pygame.Vector2(0, -1)
        self.shoot_cooldown = 0
        self.respawn_timer = 0
        self.invulnerable = False
        self.shield_charges = 0
        self.double_shot_timer = 0
        self.double_shot_active = False
        self.rotation_angle = 0

    def handle_input(self, keys):
        dx, dy = 0, 0
        if keys[self.controls['up']]:
            dy = -Config.PLAYER_SPEED
            self.last_direction = pygame.Vector2(0, -1)
        elif keys[self.controls['down']]:
            dy = Config.PLAYER_SPEED
            self.last_direction = pygame.Vector2(0, 1)

        if keys[self.controls['left']]:
            dx = -Config.PLAYER_SPEED
            self.last_direction = pygame.Vector2(-1, 0)
        elif keys[self.controls['right']]:
            dx = Config.PLAYER_SPEED
            self.last_direction = pygame.Vector2(1, 0)

        # Diagonale Bewegung: Vektor normalisieren
        self.direction = pygame.Vector2(dx, dy)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
            angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
            self.rotation_angle = angle

        return dx, dy

    def shoot(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            return None

        if not self.double_shot_active:
            self.shoot_cooldown = 30

        direction = self.direction if self.direction.length() > 0 else self.last_direction

        # Double Shot: zwei Schüsse
        if self.double_shot_active:
            bullets = [
                Bullet(self.rect.centerx, self.rect.centery, direction, self.color, f"player{self.player_id}"),
                Bullet(self.rect.centerx, self.rect.centery, direction, self.color, f"player{self.player_id}")
            ]
            return bullets
        return Bullet(self.rect.centerx, self.rect.centery, direction, self.color, f"player{self.player_id}")

    def draw_tank(self, surface):
        """Zeichnet detaillierten Panzer mit Ketten, Turm und Kanone"""
        cx, cy = self.rect.centerx, self.rect.centery
        size = self.rect.width
        half = size // 2

        # Schatten unter dem Panzer
        pygame.draw.ellipse(surface, (0, 0, 0, 100),
                          (cx - half - 2, cy + half - 5, size + 4, 10))

        # Ketten (links und rechts)
        chain_color = (80, 80, 80)
        chain_width = 4
        pygame.draw.rect(surface, chain_color,
                        (cx - half - chain_width, cy - half, chain_width, size))
        pygame.draw.rect(surface, chain_color,
                        (cx + half, cy - half, chain_width, size))

        # Ketten-Detail (kleine Linien)
        for i in range(-half, half, 4):
            pygame.draw.line(surface, (60, 60, 60),
                           (cx - half - chain_width, cy + i),
                           (cx - half, cy + i), 1)
            pygame.draw.line(surface, (60, 60, 60),
                           (cx + half, cy + i),
                           (cx + half + chain_width, cy + i), 1)

        # Hauptkörper (T-Form)
        body_color = (*self.color[:3], 255)
        pygame.draw.rect(surface, self.color,
                        (cx - half, cy - half + 4, size, size - 8))
        pygame.draw.rect(surface, (100, 100, 100),
                        (cx - half, cy - half + 4, size, size - 8), 1)

        # Turm (Kreis in der Mitte)
        turret_radius = half - 2
        pygame.draw.circle(surface, (*self.color[:3], 200), (cx, cy), turret_radius)
        pygame.draw.circle(surface, (100, 100, 100), (cx, cy), turret_radius, 1)

        # Kanone - gedreht in Fahrtrichtung
        cannon_length = 20
        cannon_width = 6
        cannon_end_x = cx + math.cos(math.radians(self.rotation_angle)) * cannon_length
        cannon_end_y = cy + math.sin(math.radians(self.rotation_angle)) * cannon_length
        cannon_start_x = cx + math.cos(math.radians(self.rotation_angle)) * 4
        cannon_start_y = cy + math.sin(math.radians(self.rotation_angle)) * 4

        # Kanone zeichnen
        pygame.draw.line(surface, (80, 80, 80),
                        (cannon_start_x, cannon_start_y),
                        (cannon_end_x, cannon_end_y), cannon_width)
        # Mündungsfeuer bei Schuss (optional)
        pygame.draw.circle(surface, (255, 200, 100),
                          (int(cannon_end_x), int(cannon_end_y)), 3)

    def take_damage(self, amount=1):
        """Nimmt Schaden, wenn unverwundbar oder Shield aktiv, ignoriert Schaden"""
        if self.invulnerable:
            return False

        # Shield: 1-2 Treffer absorbieren
        if self.shield_charges > 0:
            self.shield_charges -= 1
            return False

        self.health -= amount
        return True

    def update(self, walls):
        """Update Player"""
        # Respawn Timer
        if self.respawn_timer > 0:
            self.respawn_timer -= 1

        # Double Shot Timer
        if self.double_shot_timer > 0:
            self.double_shot_timer -= 1
            if self.double_shot_timer == 0:
                self.double_shot_active = False

    def move(self, dx, dy, walls, shake):
        """Bewegt Spieler mit Kollisionserkennung"""
        # Neue Position berechnen
        new_x = self.rect.centerx + dx
        new_y = self.rect.centery + dy

        # Bildschirmgrenzen
        new_x = max(self.rect.width//2, min(new_x, Config.WIDTH - self.rect.width//2))
        new_y = max(self.rect.height//2, min(new_y, Config.HEIGHT - self.rect.height//2))

        # Kollision mit Wänden prüfen
        self.rect.centerx = new_x
        self.rect.centery = new_y

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # X-Achse prüfen
                if dx != 0:
                    self.rect.centerx -= dx
                # Y-Achse prüfen
                if dy != 0:
                    self.rect.centery -= dy

    def draw_health_bar(self, surface):
        """Zeichnet Health-Bar über dem Panzer"""
        cx, cy = self.rect.centerx, self.rect.centery - 10
        bar_width = 30
        bar_height = 4

        # Hintergrund
        pygame.draw.rect(surface, (50, 50, 50), (cx - bar_width//2, cy, bar_width, bar_height))

        # Health-Füllung
        health_ratio = self.health / (Config.MAX_LIVES * 2)
        color = (0, 255, 0) if not self.invulnerable else (255, 255, 0)  # Gelb wenn unverwundbar
        pygame.draw.rect(surface, color, (cx - bar_width//2, cy, bar_width * health_ratio, bar_height))
        pygame.draw.rect(surface, (100, 100, 100), (cx - bar_width//2, cy, bar_width, bar_height), 1)

    def draw(self, surface):
        self.draw_tank(surface)
        self.draw_health_bar(surface)

# ============================================================================
# ENEMY TYPES
# ============================================================================
class EnemyType:
    SCOUT = "scout"
    GUNNER = "gunner"
    BRUTE = "brute"

# ============================================================================
# ENEMY CLASS mit verbessierter KI
# ============================================================================
class EnemyAI:
    def __init__(self, enemy):
        self.enemy = enemy
        self.state = EnemyState.PATROL
        self.target = None
        self.patrol_points = []
        self.current_patrol_index = 0

    def update(self, players, walls, eagle_pos):
        """Aktualisiert die KI basierend auf Zustand"""
        self._update_state(players, eagle_pos)
        self._execute_state(players, walls)

    def _update_state(self, players, eagle_pos):
        """Bestimmt den aktuellen Zustand"""
        if not players:
            self.state = EnemyState.PATROL
            return

        # Wenn Eagle getroffen wurde, fliehen
        if self.enemy.game.eagle and self.enemy.game.eagle.state == EagleState.HIT:
            self.state = EnemyState.RETREAT
            return

        # Wenn Spieler in der Nähe, jagen
        for player in players:
            distance = math.hypot(self.enemy.rect.centerx - player.rect.centerx,
                                self.enemy.rect.centery - player.rect.centery)
            if distance < 300:  # 300 Pixel Radius
                self.state = EnemyState.CHASE
                self.target = player
                return

        # Standard: Patrouillieren
        self.state = EnemyState.PATROL

    def _execute_state(self, players, walls):
        """Führt den aktuellen Zustand aus"""
        if self.state == EnemyState.PATROL:
            self._patrol(walls)
        elif self.state == EnemyState.CHASE:
            self._chase(players, walls)
        elif self.state == EnemyState.ATTACK:
            self._attack(players, walls)
        elif self.state == EnemyState.RETREAT:
            self._retreat(walls)

    def _patrol(self, walls):
        """Patrouillier-Logik"""
        if not self.patrol_points:
            self._generate_patrol_points()

        target = self.patrol_points[self.current_patrol_index]
        self.enemy.move_toward(target, walls)

        distance = math.hypot(self.enemy.rect.centerx - target[0],
                            self.enemy.rect.centery - target[1])
        if distance < 20:
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)

    def _generate_patrol_points(self):
        """Generiert Patrouillier-Punkte"""
        # Einfache Implementierung: 4 Punkte um den Enemy
        center_x, center_y = self.enemy.rect.centerx, self.enemy.rect.centery
        self.patrol_points = [
            (center_x - 100, center_y),
            (center_x, center_y - 100),
            (center_x + 100, center_y),
            (center_x, center_y + 100)
        ]

    def _chase(self, players, walls):
        """Jagden-Logik"""
        if self.target and self.target in players:
            target_pos = self.target.rect.center
            self.enemy.move_toward(target_pos, walls)

            # Wenn nah genug, angreifen
            distance = math.hypot(self.enemy.rect.centerx - target_pos[0],
                                self.enemy.rect.centery - target_pos[1])
            if distance < 150:
                self.state = EnemyState.ATTACK

    def _attack(self, players, walls):
        """Angriff-Logik"""
        if self.target and self.target in players:
            # Bleibe in Angriffsreichweite
            target_pos = self.target.rect.center
            distance = math.hypot(self.enemy.rect.centerx - target_pos[0],
                                self.enemy.rect.centery - target_pos[1])

            if distance > 200:
                self.state = EnemyState.CHASE
            else:
                # Schieße auf Ziel
                self.enemy.shoot_at(target_pos)

    def _retreat(self, walls):
        """Flucht-Logik"""
        # Bewege dich weg von der Mitte (wo der Eagle ist)
        center_x, center_y = Config.WIDTH//2, Config.HEIGHT//2
        enemy_x, enemy_y = self.enemy.rect.centerx, self.enemy.rect.centery

        # Berechne Richtung weg vom Zentrum
        dx = enemy_x - center_x
        dy = enemy_y - center_y
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        # Bewege dich in diese Richtung
        self.enemy.move(dx * self.enemy.speed, dy * self.enemy.speed, walls, 0)

class Enemy:
    def __init__(self, x, y, enemy_type=EnemyType.GUNNER):
        self.rect = pygame.Rect(x, y, Config.GRID_SIZE - 10, Config.GRID_SIZE - 10)
        self.color = Config.COLOR_ENEMY
        self.enemy_type = enemy_type
        self.direction = pygame.Vector2(0, 0)
        self.last_direction = pygame.Vector2(random.choice([-1, 1]), 0)
        self.shoot_cooldown = 0
        self.change_direction_timer = 0
        self.shoot_timer = 0
        self.respawn_timer = 0
        self.rotation_angle = 0
        self.game = None  # Reference to game manager
        self.ai = EnemyAI(self)  # KI-Controller

        # Typ-spezifische Eigenschaften
        if enemy_type == EnemyType.SCOUT:
            self.speed = Config.SCOUT_SPEED
            self.health = Config.SCOUT_HP
            self.shoot_cooldown = 45  # Seltener schießen
            self.color = (255, 165, 0)  # Orange
            self.score = Config.ENEMY_SCORE // 2
        elif enemy_type == EnemyType.GUNNER:
            self.speed = Config.GUNNER_SPEED
            self.health = Config.GUNNER_HP
            self.shoot_cooldown = 90  # Mittel schießen
            self.color = Config.COLOR_ENEMY
            self.score = Config.ENEMY_SCORE
        else:  # BRUTE
            self.speed = Config.BRUTE_SPEED
            self.health = Config.BRUTE_HP
            self.shoot_cooldown = 180  # Sehr selten schießen
            self.color = (139, 69, 19)  # Braun
            self.score = Config.ENEMY_SCORE * 2

    def move_toward(self, target_pos, walls):
        """Bewegt den Enemy in Richtung eines Ziels"""
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        # Normalisiere und bewege
        move_speed = self.speed * 0.5  # Langsamere Bewegung für bessere Steuerung
        self.move(dx * move_speed, dy * move_speed, walls, 0)

    def shoot_at(self, target_pos):
        """Schießt in Richtung eines Ziels"""
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        # Erzeuge Bullet in diese Richtung
        direction = pygame.Vector2(dx, dy)
        return Bullet(self.rect.centerx, self.rect.centery, direction, self.color, "enemy")

    def move(self, dx, dy, walls, shake):
        """Bewegt Enemy mit Kollisionserkennung"""
        # Neue Position berechnen
        new_x = self.rect.centerx + dx
        new_y = self.rect.centery + dy

        # Bildschirmgrenzen
        new_x = max(self.rect.width//2, min(new_x, Config.WIDTH - self.rect.width//2))
        new_y = max(self.rect.height//2, min(new_y, Config.HEIGHT - self.rect.height//2))

        # Kollision mit Wänden prüfen
        self.rect.centerx = new_x
        self.rect.centery = new_y

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # X-Achse prüfen
                if dx != 0:
                    self.rect.centerx -= dx
                # Y-Achse prüfen
                if dy != 0:
                    self.rect.centery -= dy

    def take_damage(self):
        """Enemy.take_damage() Methode - reduziert Health und gibt True wenn getötet"""
        self.health -= 1
        if self.health <= 0:
            return True  # Enemy ist getötet
        return False  # Enemy lebt noch

    def update_ai(self, players, walls, eagle_pos):
        """Verbesserte KI mit State-Machine"""
        self.ai.update(players, walls, eagle_pos)

        # Schießen (typ-spezifischer Cooldown)
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0
            return self.shoot_at(eagle_pos)  # Standardmäßig auf Eagle schießen
        return None

    def respawn(self, x, y):
        """Enemy respawnet an neuer Position"""
        self.rect.x = x
        self.rect.y = y
        self.health = self.get_max_health()
        self.shoot_cooldown = 0

    def get_max_health(self):
        """Gibt maximale Health basierend auf Typ zurück"""
        if self.enemy_type == EnemyType.SCOUT:
            return Config.SCOUT_HP
        elif self.enemy_type == EnemyType.GUNNER:
            return Config.GUNNER_HP
        else:  # BRUTE
            return Config.BRUTE_HP

    def draw(self, surface):
        """Zeichnet detaillierten Enemy-Panzer"""
        cx, cy = self.rect.centerx, self.rect.centery
        size = self.rect.width
        half = size // 2

        # Schatten
        pygame.draw.ellipse(surface, (0, 0, 0, 80),
                          (cx - half - 2, cy + half - 5, size + 4, 10))

        # Ketten
        chain_color = (60, 60, 60)
        chain_width = 3
        pygame.draw.rect(surface, chain_color,
                        (cx - half - chain_width, cy - half, chain_width, size))
        pygame.draw.rect(surface, chain_color,
                        (cx + half, cy - half, chain_width, size))

        # Hauptkörper
        pygame.draw.rect(surface, self.color,
                        (cx - half, cy - half + 4, size, size - 8))
        pygame.draw.rect(surface, (80, 80, 80),
                        (cx - half, cy - half + 4, size, size - 8), 1)

        # Turm
        turret_radius = half - 2
        pygame.draw.circle(surface, (*self.color[:3], 200), (cx, cy), turret_radius)
        pygame.draw.circle(surface, (80, 80, 80), (cx, cy), turret_radius, 1)

        # Kanone
        cannon_length = 18
        cannon_width = 5
        cannon_end_x = cx + math.cos(math.radians(self.rotation_angle)) * cannon_length
        cannon_end_y = cy + math.sin(math.radians(self.rotation_angle)) * cannon_length
        pygame.draw.line(surface, (70, 70, 70),
                        (cx, cy),
                        (cannon_end_x, cannon_end_y), cannon_width)

    def draw_health_bar(self, surface):
        cx, cy = self.rect.centerx, self.rect.centery - 10
        bar_width = 30
        bar_height = 4

        pygame.draw.rect(surface, (50, 50, 50), (cx - bar_width//2, cy, bar_width, bar_height))

        health_ratio = self.health / self.get_max_health()
        pygame.draw.rect(surface, (255, 0, 0), (cx - bar_width//2, cy, bar_width * health_ratio, bar_height))
        pygame.draw.rect(surface, (100, 100, 100), (cx - bar_width//2, cy, bar_width, bar_height), 1)

# ============================================================================
# WAVE MANAGER (Horde Modus)
# ============================================================================
class WaveManager:
    def __init__(self):
        self.current_wave = 0
        self.total_waves = Config.TOTAL_WAVES
        self.spawn_timer = 0
        self.enemies_to_spawn = 0
        self.wave_complete = False
        self.level = 1
        self.is_boss_wave = False

    def _is_spawn_valid(self, x, y, players, enemies, walls, eagle):
        """Prüft ob Spawn-Position fair ist"""
        # Mindestens 2 Grid-Zellen Abstand zu Spielern
        for player in players:
            dist = math.hypot(x - player.rect.centerx, y - player.rect.centery)
            if dist < Config.GRID_SIZE * 2:
                return False

        # Mindestens 2 Grid-Zellen Abstand zum Eagle
        if eagle:
            dist = math.hypot(x - eagle.rect.centerx, y - eagle.rect.centery)
            if dist < Config.GRID_SIZE * 2:
                return False

        # Mindestens 2 Grid-Zellen Abstand zu anderen Enemy
        for enemy in enemies:
            dist = math.hypot(x - enemy.rect.centerx, y - enemy.rect.centery)
            if dist < Config.GRID_SIZE * 2:
                return False

        # Mindestens 2 Grid-Zellen Abstand zu Wänden
        for wall in walls:
            if wall.rect.collidepoint((x, y)):
                wall_margin = Config.GRID_SIZE // 2
                if (wall.rect.left - wall_margin <= x <= wall.rect.right + wall_margin and
                    wall.rect.top - wall_margin <= y <= wall.rect.bottom + wall_margin):
                    if wall.wall_type == WallType.STEEL:
                        return False

        return True

    def spawn_enemy(self, enemies_list, players, walls, eagle):
        """Spawnet einen neuen Enemy mit fairem Spawn-Schutz"""
        if self.enemies_to_spawn > 0:
            # Mehrere Versuche für faire Position
            max_attempts = 50
            for _ in range(max_attempts):
                x = random.randint(Config.GRID_SIZE, Config.WIDTH - Config.GRID_SIZE)
                y = random.randint(Config.GRID_SIZE, Config.HEIGHT - Config.GRID_SIZE)

                if self._is_spawn_valid(x, y, players, enemies_list, walls, eagle):
                    enemy = Enemy(x, y)
                    enemies_list.append(enemy)
                    self.enemies_to_spawn -= 1
                    return enemy

            # Falls keine faire Position gefunden, spawne trotzdem
            x = random.randint(Config.GRID_SIZE, Config.WIDTH - Config.GRID_SIZE)
            y = random.randint(Config.GRID_SIZE, Config.HEIGHT - Config.GRID_SIZE)
            enemy = Enemy(x, y)
            enemies_list.append(enemy)
            self.enemies_to_spawn -= 1
            return enemy
        return None

    def update(self, enemies_list, frame_count, players, walls, eagle):
        """Update Wave Manager"""
        if self.wave_complete:
            return

        # Spawn Timer
        self.spawn_timer += 1
        if self.spawn_timer >= Config.ENEMY_SPAWN_INTERVAL:
            self.spawn_timer = 0
            enemy = self.spawn_enemy(enemies_list, players, walls, eagle)
            if enemy:
                enemy.update_ai(players, walls, eagle.rect.center)

        # Wave Progress
        if self.enemies_to_spawn == 0 and len(enemies_list) == 0:
            self.wave_complete = True

    def next_wave(self):
        """Startet nächste Welle"""
        self.current_wave += 1
        self.wave_complete = False
        self.spawn_timer = 0

        # Boss-Welle am Ende
        if self.current_wave == Config.BOSS_WAVE:
            self.is_boss_wave = True
            self.enemies_to_spawn = 15  # Viele Gegner für Boss-Welle
        else:
            self.is_boss_wave = False
            # Erhöhte Schwierigkeit pro Welle
            base_enemies = 3 + self.current_wave
            self.enemies_to_spawn = base_enemies

        # Level Up nach 10 Wellen
        if self.current_wave % 10 == 0:
            self.level += 1

# ============================================================================
# MAP GENERATOR mit verbessertem Design
# ============================================================================
class MapGenerator:
    def __init__(self, map_type="classic"):
        self.map_type = map_type
        self.map_config = Config.MAPS.get(map_type, Config.MAPS["classic"])
        self.themes = {
            "classic": {"background": (20, 20, 30), "wall_colors": [(139, 69, 19), (169, 169, 169)]},
            "industrial": {"background": (30, 30, 40), "wall_colors": [(80, 80, 80), (120, 120, 120)]},
            "desert": {"background": (50, 40, 20), "wall_colors": [(180, 150, 80), (200, 180, 120)]}
        }

    def generate(self):
        """Generiert ein Labyrinth mit Brotbox Algorithmus"""
        walls = []
        grid_width = Config.WIDTH // Config.GRID_SIZE
        grid_height = Config.HEIGHT // Config.GRID_SIZE

        # Initialize grid: 0 = path, 1 = wall
        grid = [[1 for _ in range(grid_width)] for _ in range(grid_height)]

        # Start point (internal cell)
        start_x, start_y = 1, 1
        grid[start_y][start_x] = 0

        stack = [(start_x, start_y)]

        while stack:
            cx, cy = stack[-1]
            neighbors = []

            # Check neighbors (2 steps away)
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 1 <= nx < grid_width - 1 and 1 <= ny < grid_height - 1 and grid[ny][nx] == 1:
                    neighbors.append((nx, ny, cx + dx//2, cy + dy//2))

            if neighbors:
                nx, ny, wall_x, wall_y = random.choice(neighbors)

                # Carve path
                grid[ny][nx] = 0
                grid[wall_y][wall_x] = 0

                stack.append((nx, ny))
            else:
                stack.pop()

        # Convert grid to Wall objects
        for y in range(grid_height):
            for x in range(grid_width):
                if grid[y][x] == 1:
                    wall_x = x * Config.GRID_SIZE
                    wall_y = y * Config.GRID_SIZE

                    # Determine wall type based on map type
                    wall_type = self._determine_wall_type(x, y, grid_width, grid_height)
                    walls.append(Wall(wall_x, wall_y, Config.GRID_SIZE, Config.GRID_SIZE, wall_type))

        return walls

    def _determine_wall_type(self, x, y, grid_width, grid_height):
        """Bestimmt Wall-Typ basierend auf Map-Konfiguration"""
        # Outer walls are always steel
        if x == 0 or x == grid_width - 1 or y == 0 or y == grid_height - 1:
            return WallType.STEEL

        # Based on map type
        if self.map_type == "industrial":
            # 40% steel, 60% brick
            if random.random() < self.map_config.get("steel_ratio", 0.4):
                return WallType.STEEL
            return WallType.BRICK
        elif self.map_type == "desert":
            # 60% brick, 40% steel
            if random.random() < self.map_config.get("brick_ratio", 0.6):
                return WallType.BRICK
            return WallType.STEEL
        else:
            # Classic: 50/50 mix
            if random.random() < 0.5:
                return WallType.BRICK
            return WallType.STEEL

# ============================================================================
# GAME MANAGER mit verbessertem UI
# ============================================================================
class GameManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=Config.SOUND_SAMPLE_RATE, size=-16, channels=Config.MAX_SOUNDS, buffer=4096)
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("PyTank - Tank Battle")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.MAIN_MENU
        self.sound_manager = SoundManager()
        self.background = BackgroundRenderer()

        # Game entities
        self.players = []
        self.enemies = []
        self.walls = []
        self.bullets = []
        self.particles = []
        self.powerups = []
        self.eagle = None
        self.wave_manager = None

        # Screen shake
        self.screen_shake = 0

        # Score
        self.score = {1: 0, 2: 0}

        # Level selection
        self.selected_map = "classic"

        # Game mode (Singleplayer standard)
        self.game_mode = GameMode.HORDE

        # Mission System
        self.mission = "Eagle Protect"
        self.mission_active = True

        # Time Limit
        self.game_time = 0
        self.time_limit = Config.TIME_LIMIT
        self.time_running = False

        # Powerup spawn timer
        self.powerup_spawn_timer = 0

        # Vollbildmodus
        self.fullscreen = False

        # Victory sound flag
        self._victory_played = False

    def reset_game(self, mode=GameMode.FFA, map_type="classic"):
        """Resetet das Spiel"""
        self.players = []
        self.enemies = []
        self.walls = []
        self.bullets = []
        self.particles = []
        self.score = {1: 0, 2: 0}
        self.screen_shake = 0
        self.selected_map = map_type
        self._victory_played = False

        # Setup eagle
        self.eagle = Eagle(Config.WIDTH//2 - 20, Config.HEIGHT - 40)
        self.eagle.state = EagleState.PROTECTED

        # Setup wave manager for horde mode
        self.wave_manager = WaveManager() if mode == GameMode.HORDE else None

        # Setup level
        self._setup_level()

    def _find_free_positions(self, walls, count, offset=50):
        """Findet mehrere freie Positionen ohne Wand-Kollision"""
        positions = []
        checked = set()

        for y in range(offset, Config.HEIGHT - offset - 40, 10):
            for x in range(offset, Config.WIDTH - offset - 40, 10):
                key = (x, y)
                if key in checked:
                    continue
                checked.add(key)

                test_rect = pygame.Rect(x, y, Config.GRID_SIZE - 10, Config.GRID_SIZE - 10)
                free = True
                for wall in walls:
                    if test_rect.colliderect(wall.rect):
                        free = False
                        break
                if free:
                    positions.append((x, y))
                    if len(positions) >= count:
                        return positions
        return positions

    def _setup_level(self):
        """Setuppt Level mit Wänden, Spielern und Gegnern"""
        # Generate walls
        map_generator = MapGenerator(self.selected_map)
        self.walls = map_generator.generate()

        # Add outer steel walls
        outer_walls = self._create_outer_walls()
        self.walls.extend(outer_walls)

        # Create players based on mode
        if self.game_mode == GameMode.FFA:
            self._setup_ffa_mode()
        else:
            self._setup_horde_mode()

    def _create_outer_walls(self):
        """Erstellt die Außenwände (alle Stahl)"""
        walls = []
        # Top - nur die Mitte, nicht die Ecken
        walls.append(Wall(0, 0, Config.WIDTH - Config.GRID_SIZE * 2, Config.GRID_SIZE, WallType.STEEL))
        # Bottom
        walls.append(Wall(0, Config.HEIGHT - Config.GRID_SIZE, Config.WIDTH - Config.GRID_SIZE * 2, Config.GRID_SIZE, WallType.STEEL))
        # Left - nur die Mitte, nicht die Ecken
        walls.append(Wall(0, 0, Config.GRID_SIZE, Config.HEIGHT - Config.GRID_SIZE * 2, WallType.STEEL))
        # Right
        walls.append(Wall(Config.WIDTH - Config.GRID_SIZE, 0, Config.GRID_SIZE, Config.HEIGHT - Config.GRID_SIZE * 2, WallType.STEEL))
        return walls

    def _setup_ffa_mode(self):
        """Setup FFA Modus"""
        p1_controls = {
            'up': pygame.K_w, 'down': pygame.K_s,
            'left': pygame.K_a, 'right': pygame.K_d,
            'shoot': pygame.K_SPACE
        }
        p2_controls = {
            'up': pygame.K_UP, 'down': pygame.K_DOWN,
            'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
            'shoot': pygame.K_RETURN
        }

        # Find free positions for players
        positions = self._find_free_positions(self.walls, 2, 100)

        if positions:
            self.players.append(Player(1, positions[0][0], positions[0][1], Config.COLOR_P1, p1_controls))
            if len(positions) > 1:
                self.players.append(Player(2, positions[1][0], positions[1][1], Config.COLOR_P2, p2_controls))

        # Spawn 6-7 enemies
        num_enemies = random.randint(6, 7)
        for i in range(num_enemies):
            positions = self._find_free_positions(self.walls, 1, 50)
            if positions:
                x, y = positions[0]
                # Zufälliger Enemy-Typ basierend auf Spawn-Chance
                enemy_type = EnemyType.GUNNER
                if random.random() < Config.SCOUT_SPAWN_CHANCE:
                    enemy_type = EnemyType.SCOUT
                elif random.random() < Config.BRUTE_SPAWN_CHANCE:
                    enemy_type = EnemyType.BRUTE
                self.enemies.append(Enemy(x, y, enemy_type))

        # Spawn Powerups (1-2 pro Runde)
        num_powerups = random.randint(1, 2)
        for _ in range(num_powerups):
            self._spawn_powerup()

    def _setup_horde_mode(self):
        """Setup Horde Modus"""
        # Only player 1 in horde mode
        p1_controls = {
            'up': pygame.K_w, 'down': pygame.K_s,
            'left': pygame.K_a, 'right': pygame.K_d,
            'shoot': pygame.K_SPACE
        }

        # Find free position for player
        positions = self._find_free_positions(self.walls, 1, 100)
        if positions:
            self.players.append(Player(1, positions[0][0], positions[0][1], Config.COLOR_P1, p1_controls))

        # Start wave 1
        if self.wave_manager:
            self.wave_manager.next_wave()

    def handle_events(self):
        """Behandelt Eingabe-Events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Maus-Events für Lautstärkeregler
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_state == GameState.PLAYING:
                    self._handle_volume_slider_click(event.pos)

            if event.type == pygame.MOUSEMOTION:
                if self.game_state == GameState.PLAYING:
                    self._handle_volume_slider_drag(event.pos)

            if event.type == pygame.KEYDOWN:
                if self.game_state == GameState.MAIN_MENU:
                    if event.key == pygame.K_SPACE:
                        self.game_state = GameState.LEVEL_SELECT
                    elif event.key == pygame.K_1:
                        self.game_mode = GameMode.FFA
                        self._show_ffa_info()
                    elif event.key == pygame.K_2:
                        self.game_mode = GameMode.HORDE
                        self._show_horde_info()
                    elif event.key == pygame.K_3:
                        self.game_mode = GameMode.COOP
                        self._show_coop_info()
                    elif event.key == pygame.K_f:
                        # Vollbildmodus umschalten
                        if not self.fullscreen:
                            self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT), pygame.FULLSCREEN)
                            self.fullscreen = True
                        else:
                            self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
                            self.fullscreen = False
                            pygame.display.flip()
                elif self.game_state == GameState.LEVEL_SELECT:
                    if event.key == pygame.K_1:
                        self.selected_map = "classic"
                    elif event.key == pygame.K_2:
                        self.selected_map = "industrial"
                    elif event.key == pygame.K_3:
                        self.selected_map = "desert"
                    elif event.key == pygame.K_SPACE:
                        self._start_game()
                    elif event.key == pygame.K_f:
                        # Vollbildmodus umschalten
                        if not self.fullscreen:
                            self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT), pygame.FULLSCREEN)
                            self.fullscreen = True
                        else:
                            self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
                            self.fullscreen = False
                            pygame.display.flip()
                elif self.game_state == GameState.PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.PAUSED
                    elif event.key == pygame.K_f:
                        # Vollbildmodus umschalten
                        if not self.fullscreen:
                            self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT), pygame.FULLSCREEN)
                            self.fullscreen = True
                        else:
                            self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
                            self.fullscreen = False
                            pygame.display.flip()
                elif self.game_state == GameState.PAUSED:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.game_state = GameState.PLAYING
                    elif event.key == pygame.K_1:
                        self.game_mode = GameMode.FFA
                        self.reset_game(GameMode.FFA, self.selected_map)
                        self.game_state = GameState.LEVEL_SELECT
                    elif event.key == pygame.K_2:
                        self.game_mode = GameMode.HORDE
                        self.reset_game(GameMode.HORDE, self.selected_map)
                        self.game_state = GameState.LEVEL_SELECT
                    elif event.key == pygame.K_3:
                        self.game_mode = GameMode.COOP
                        self.reset_game(GameMode.COOP, self.selected_map)
                        self.game_state = GameState.LEVEL_SELECT
                elif self.game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game(self.game_mode, self.selected_map)
                        self.game_state = GameState.MAIN_MENU
                elif self.game_state == GameState.VICTORY:
                    if event.key == pygame.K_SPACE:
                        self.reset_game(self.game_mode, self.selected_map)
                        self.game_state = GameState.MAIN_MENU

                # Lautstärkeregler: V = Musik leiser, W = Musik lauter
                #            B = SFX leiser, N = SFX lauter
                if self.game_state == GameState.PLAYING:
                    if event.key == pygame.K_v:
                        self.sound_manager.set_music_volume(self.sound_manager.get_music_volume() - 0.1)
                    elif event.key == pygame.K_w:
                        self.sound_manager.set_music_volume(self.sound_manager.get_music_volume() + 0.1)
                    elif event.key == pygame.K_b:
                        self.sound_manager.set_sfx_volume(self.sound_manager.get_sfx_volume() - 0.1)
                    elif event.key == pygame.K_n:
                        self.sound_manager.set_sfx_volume(self.sound_manager.get_sfx_volume() + 0.1)
                    # M = Mute/Unmute alle Sounds
                    elif event.key == pygame.K_m:
                        if self.sound_manager.get_sfx_volume() > 0:
                            self.sound_manager.set_sfx_volume(0)
                            self.sound_manager.set_music_volume(0)
                        else:
                            self.sound_manager.set_sfx_volume(Config.SFX_VOLUME)
                            self.sound_manager.set_music_volume(Config.MUSIC_VOLUME)

    def _spawn_powerup(self):
        """Spawnt ein zufälliges Powerup"""
        powerup_types = [Powerup.SHIELD, Powerup.DOUBLE_SHOT, Powerup.REPAIR]
        powerup_type = random.choice(powerup_types)

        # Faire Position (mindestens 2 Grid-Zellen Abstand zu Spielern, Eagle, Wänden)
        max_attempts = 50
        for _ in range(max_attempts):
            x = random.randint(Config.GRID_SIZE, Config.WIDTH - Config.GRID_SIZE)
            y = random.randint(Config.GRID_SIZE, Config.HEIGHT - Config.GRID_SIZE)

            # Check Abstand zu Spielern
            free = True
            for player in self.players:
                dist = math.hypot(x - player.rect.centerx, y - player.rect.centery)
                if dist < Config.GRID_SIZE * 2:
                    free = False
                    break

            if free:
                # Check Abstand zu Eagle
                if self.eagle:
                    dist = math.hypot(x - self.eagle.rect.centerx, y - self.eagle.rect.centery)
                    if dist < Config.GRID_SIZE * 2:
                        free = False

                if free:
                    # Check Abstand zu Wänden
                    for wall in self.walls:
                        if wall.rect.collidepoint((x, y)):
                            free = False
                            break

                if free:
                    powerup = Powerup(x, y, powerup_type)
                    self.powerups.append(powerup)
                    return

        # Falls keine Position gefunden, spawne trotzdem
        x = random.randint(Config.GRID_SIZE, Config.WIDTH - Config.GRID_SIZE)
        y = random.randint(Config.GRID_SIZE, Config.HEIGHT - Config.GRID_SIZE)
        powerup = Powerup(x, y, powerup_type)
        self.powerups.append(powerup)

    def _start_game(self):
        """Startet das Spiel"""
        self.reset_game(self.game_mode, self.selected_map)
        self.game_state = GameState.PLAYING

    def _show_ffa_info(self):
        """Zeigt FFA-Info"""
        font = pygame.font.SysFont(None, 36)
        text = font.render("FFA Mode: 2 Players + 6-7 AI Enemies", True, Config.COLOR_TEXT)
        self.screen.blit(text, (Config.WIDTH//2 - 150, Config.HEIGHT//2 + 50))
        pygame.display.flip()
        pygame.time.wait(1500)

    def _show_horde_info(self):
        """Zeigt Horde-Info"""
        font = pygame.font.SysFont(None, 36)
        text = font.render("Horde Mode: Wave-based, 10 Waves", True, Config.COLOR_TEXT)
        self.screen.blit(text, (Config.WIDTH//2 - 150, Config.HEIGHT//2 + 50))
        pygame.display.flip()
        pygame.time.wait(1500)

    def _show_coop_info(self):
        """Zeigt Coop-Info"""
        font = pygame.font.SysFont(None, 36)
        text = font.render("Coop Mode: 2 Players + AI Enemies", True, Config.COLOR_TEXT)
        self.screen.blit(text, (Config.WIDTH//2 - 150, Config.HEIGHT//2 + 50))
        pygame.display.flip()
        pygame.time.wait(1500)

    def update(self):
        """Update Game-Logik"""
        if self.game_state != GameState.PLAYING:
            return

        # Musik-Ducking aktualisieren
        self.sound_manager._update_music_ducking()

        keys = pygame.key.get_pressed()

        # Time Limit
        self.game_time += 1
        if self.game_time >= self.time_limit * 60:  # In Frames
            self.game_state = GameState.GAME_OVER
            return

        # Update Players
        for p in self.players:
            # Update Player (Respawn Timer, Unverwundbarkeit)
            p.update(self.walls)

            # Skip input if respawning
            if p.respawn_timer > 0:
                continue

            dx, dy = p.handle_input(keys)
            p.direction = pygame.Vector2(dx/Config.PLAYER_SPEED, dy/Config.PLAYER_SPEED)
            if p.direction.length() > 0:
                p.direction.normalize_ip()
            p.move(dx, dy, self.walls, self.screen_shake)

            # Shooting
            if keys[p.controls['shoot']]:
                bullet = p.shoot()
                if bullet:
                    if isinstance(bullet, list):
                        self.bullets.extend(bullet)
                    else:
                        self.bullets.append(bullet)
                    self.sound_manager.play_shoot()

        # Update Enemies
        eagle_pos = self.eagle.rect.center if self.eagle else (Config.WIDTH//2, Config.HEIGHT//2)
        for e in self.enemies:
            new_bullet = e.update_ai(self.players, self.walls, eagle_pos)
            if new_bullet:
                self.bullets.append(new_bullet)

        # Update Wave Manager (Horde Mode)
        if self.wave_manager:
            self.wave_manager.update(self.enemies, self.wave_manager.spawn_timer, self.players, self.walls, self.eagle)

            # Check for wave completion
            if self.wave_manager.wave_complete:
                self.wave_manager.next_wave()
                self.screen_shake = 10
                # Boss-Welle Mission
                if self.wave_manager.is_boss_wave:
                    self.mission = "Boss Wave - Defend Eagle!"

        # Update Particles
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

        # Update Powerups
        for p in self.powerups[:]:
            p.update()

        # Screen Shake dekrementieren
        if self.screen_shake > 0:
            self.screen_shake = max(0, self.screen_shake - 1)

        # Update Bullets
        for b in self.bullets[:]:
            result = b.update(self.walls)

            if result == "hit_wall" or result == "out_of_bounds":
                self.bullets.remove(b)
            elif isinstance(result, Wall):
                if result.destructible:
                    self.walls.remove(result)
                    self.score[1] += Config.BRICK_SCORE
                    self.screen_shake = 5
                    self._create_particles(result.rect.center, Config.COLOR_BRICK, 10)
                    # Ziegel-Wand: knirschender, staubiger Sound
                    self.sound_manager.play_brick_destroy()
                else:
                    # Stahl-Wand: metallischer Klang (zerstörbar nach mehreren Treffern)
                    self.sound_manager.play_steel_destroy()
                self.bullets.remove(b)
            else:
                # Check collision with entities
                self._check_bullet_collision(b)

        # Check Powerup collision with players
        for p in self.players:
            for powerup in self.powerups[:]:
                if p.rect.colliderect(powerup.hitbox):
                    # Apply powerup effect
                    if powerup.powerup_type == Powerup.SHIELD:
                        p.shield_charges = Config.SHIELD_MAX_CHARGES
                        self.screen_shake = 5
                    elif powerup.powerup_type == Powerup.DOUBLE_SHOT:
                        p.double_shot_active = True
                        p.double_shot_timer = Config.DOUBLE_SHOOT_DURATION * 60  # In Frames
                        self.screen_shake = 5
                    elif powerup.powerup_type == Powerup.REPAIR:
                        p.health = min(p.health + Config.REPAIR_AMOUNT, Config.MAX_LIVES * 2)
                        self.screen_shake = 5
                    powerup.rect = pygame.Rect(0, 0, 0, 0)  # Mark for removal
                    self.sound_manager.play_powerup()
                    break

    def _check_bullet_collision(self, bullet):
        """Checkt Kollision von Bullet mit Entitäten"""
        # Check eagle collision (nur wenn noch nicht getroffen)
        if self.eagle and self.eagle.state == EagleState.PROTECTED and bullet.rect.colliderect(self.eagle.rect):
            self.eagle.state = EagleState.HIT
            self.screen_shake = 20
            self._create_particles(bullet.rect.center, Config.COLOR_EAGLE, 30)
            self.game_state = GameState.GAME_OVER
            self.bullets.remove(bullet)
            return

        # Check player collision
        for p in self.players:
            if bullet.rect.colliderect(p.rect):
                if bullet.owner != f"player{p.player_id}":
                    if p.health > 0:
                        if p.take_damage(1):
                            self.screen_shake = 5
                            self._create_particles(bullet.rect.center, p.color, 10)
                            if p.health <= 0:
                                p.lives -= 1
                                if p.lives <= 0:
                                    self.game_state = GameState.GAME_OVER
                                    self.sound_manager.play_lose()
                                else:
                                    # Respawn player mit Unverwundbarkeit
                                    free_pos = self._find_free_positions(self.walls, 1, 50)
                                    if free_pos:
                                        px, py = free_pos[0]
                                    else:
                                        px, py = 80, 80  # Fallback
                                    p.rect.x = px
                                    p.rect.y = py
                                    p.health = Config.MAX_LIVES * 2
                                    p.respawn_timer = Config.RESPAWN_COOLDOWN * 60  # In Frames
                                    p.invulnerable = True
                    self.bullets.remove(bullet)
                break

        # Check enemy collision
        for e in list(self.enemies):
            if bullet.rect.colliderect(e.rect):
                if bullet.owner in ["player1", "player2"]:
                    if e.take_damage():
                        self.enemies.remove(e)
                        self.score[1] += Config.ENEMY_SCORE
                        self.screen_shake = 10
                        self._create_particles(e.rect.center, Config.COLOR_ENEMY, 20)
                        self.sound_manager.play_tank_explosion()
                    self.bullets.remove(bullet)
                break

    def _create_particles(self, position, color, count):
        """Erstellt Partikel-Effekte"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(
                position[0], position[1], color, vx, vy, random.randint(20, 40)
            ))

    def draw(self):
        """Zeichnet das Spiel"""
        self.screen.fill(Config.COLOR_BLACK)

        if self.game_state == GameState.MAIN_MENU:
            self._draw_main_menu()
        elif self.game_state == GameState.LEVEL_SELECT:
            self._draw_level_select()
        elif self.game_state == GameState.PLAYING:
            self._draw_game()
        elif self.game_state == GameState.PAUSED:
            self._draw_paused()
        elif self.game_state == GameState.GAME_OVER:
            self._draw_gameover()
        elif self.game_state == GameState.VICTORY:
            self._draw_victory()

        pygame.display.flip()

    def _draw_rect(self, x, y, width, height, color, border=2, border_color=(100, 100, 150)):
        """Hilfsfunktion zum Zeichnen von Rechtecken mit Rahmen"""
        if border > 0:
            pygame.draw.rect(self.screen, border_color, (x - border, y - border, width + border*2, height + border*2))
        pygame.draw.rect(self.screen, color, (x, y, width, height))

    def _draw_centered_text(self, text, y_offset, font_size=36, bold=False, color=(255, 255, 255), shadow_offset=2):
        """Zeichnet zentrierten Text mit Schatten"""
        font = pygame.font.SysFont(None, font_size, bold=bold)
        rendered = font.render(text, True, color)
        # Schatten
        shadow = font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (Config.WIDTH//2 - rendered.get_width()//2 + shadow_offset, y_offset + shadow_offset))
        self.screen.blit(rendered, (Config.WIDTH//2 - rendered.get_width()//2, y_offset))
        return rendered.get_height()

    def _draw_main_menu(self):
        """Verbessertes Hauptmenü mit professionellem Design"""
        tick = pygame.time.get_ticks() / 1000

        # Dunkler, animierter Hintergrund mit Gradient
        for i in range(Config.HEIGHT // 4):
            r = int(15 + 10 * math.sin(tick * 0.3 + i / 100))
            g = int(15 + 15 * math.cos(tick * 0.2 + i / 80))
            b = int(30 + 20 * math.sin(tick * 0.4 + i / 120))
            r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
            pygame.draw.line(self.screen, (r, g, b), (0, i * 4), (Config.WIDTH, i * 4))

        # Overlay für bessere Lesbarkeit
        overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))
        self.screen.blit(overlay, (0, 0))

        # Logo-Box mit Rahmen
        box_width = 600
        box_height = 500
        box_x = Config.WIDTH//2 - box_width//2
        box_y = Config.HEIGHT//2 - box_height//2 - 50

        # Box-Hintergrund
        pygame.draw.rect(self.screen, (25, 25, 40), (box_x - 10, box_y - 10, box_width + 20, box_height + 20), border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 180), (box_x - 10, box_y - 10, box_width + 20, box_height + 20), 3, border_radius=10)

        # Titel mit Glow-Effekt
        title_y = box_y + 50
        font = pygame.font.SysFont(None, 100, bold=True)
        title = font.render("PYTANK", True, (255, 215, 0))
        title_shadow = font.render("PYTANK", True, (100, 80, 0))
        self.screen.blit(title_shadow, (Config.WIDTH//2 - title.get_width()//2 + 4, title_y + 4))
        self.screen.blit(title, (Config.WIDTH//2 - title.get_width()//2, title_y))

        # Untertitel
        self._draw_centered_text("TANK BATTLE ARENA", title_y + 80, font_size=40, bold=True, color=(180, 180, 220))

        # Trennlinie
        pygame.draw.line(self.screen, (100, 100, 180),
                        (box_x + 50, title_y + 110), (box_x + box_width - 50, title_y + 110), 2)

        # Menü-Buttons
        button_font = pygame.font.SysFont(None, 32, bold=True)
        buttons = [
            ("1 - FFA Mode", (0, 255, 0), "1"),
            ("2 - Horde Mode", (255, 165, 0), "2"),
            ("3 - Co-op Mode", (0, 200, 255), "3"),
        ]

        btn_y = box_y + 180
        btn_width = 380
        btn_height = 50

        for i, (text, color, key) in enumerate(buttons):
            btn_x = Config.WIDTH//2 - btn_width//2

            # Button-Hintergrund mit Hover-Effekt
            pulse = int(30 * math.sin(tick * 2 + i))
            hover_color = tuple(min(255, max(0, c + pulse)) for c in color)

            pygame.draw.rect(self.screen, (20, 20, 35), (btn_x, btn_y + i * 70, btn_width, btn_height), border_radius=8)
            pygame.draw.rect(self.screen, hover_color, (btn_x, btn_y + i * 70, btn_width, btn_height), 2, border_radius=8)

            # Key-Hint
            key_font = pygame.font.SysFont(None, 28)
            key_rendered = key_font.render(f"[{key}]", True, color)
            self.screen.blit(key_rendered, (btn_x + 15, btn_y + i * 70 + 11))

            # Button-Text
            text_rendered = button_font.render(text, True, (255, 255, 255))
            self.screen.blit(text_rendered, (btn_x + 60, btn_y + i * 70 + 11))

        # SPACE für Main Menu (wenn von Pause)
        self._draw_centered_text("[SPACE] Main Menu", btn_y + 70 * 3 + 30, font_size=28, color=(200, 200, 200))

        # Footer
        footer_y = box_y + box_height + 40
        footer_font = pygame.font.SysFont(None, 22)
        footer = footer_font.render("Press F for Fullscreen", True, (120, 120, 160))
        self.screen.blit(footer, (Config.WIDTH//2 - footer.get_width()//2, footer_y))

    def _draw_level_select(self):
        """Verbesserte Level-Auswahl mit professionellem Design"""
        tick = pygame.time.get_ticks() / 1000

        # Dunkler Hintergrund
        self.screen.fill((20, 20, 30))

        # Titel-Box
        box_width = 700
        box_height = 550
        box_x = Config.WIDTH//2 - box_width//2
        box_y = Config.HEIGHT//2 - box_height//2 - 30

        # Box-Hintergrund
        pygame.draw.rect(self.screen, (25, 25, 40), (box_x - 10, box_y - 10, box_width + 20, box_height + 20), border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 180), (box_x - 10, box_y - 10, box_width + 20, box_height + 20), 3, border_radius=10)

        # Titel
        self._draw_centered_text("SELECT MAP", box_y + 30, font_size=64, bold=True, color=(255, 215, 0))

        # Trennlinie
        pygame.draw.line(self.screen, (100, 100, 180),
                        (box_x + 50, box_y + 80), (box_x + box_width - 50, box_y + 80), 2)

        # Map-Optionen
        maps = [
            ("Classic", "Symmetric Brick/Steel Mix", (255, 255, 0), "1"),
            ("Industrial", "High Steel Content", (0, 255, 0), "2"),
            ("Desert", "Brick-Heavy Terrain", (255, 165, 0), "3"),
        ]

        # Map-Vorschau
        preview_size = 10
        preview_grid_w = 32
        preview_grid_h = 20
        preview_w = preview_grid_w * preview_size
        preview_h = preview_grid_h * preview_size
        preview_x = Config.WIDTH//2 - preview_w//2
        preview_y = box_y + 100

        # Vorschau-Box
        pygame.draw.rect(self.screen, (15, 15, 25), (preview_x - 5, preview_y - 35, preview_w + 10, preview_h + 45), border_radius=5)
        pygame.draw.rect(self.screen, (80, 80, 120), (preview_x - 5, preview_y - 35, preview_w + 10, preview_h + 45), 2, border_radius=5)

        # Vorschau-Titel
        preview_title_font = pygame.font.SysFont(None, 24, bold=True)
        preview_title = preview_title_font.render("MAP PREVIEW", True, (150, 150, 200))
        self.screen.blit(preview_title, (Config.WIDTH//2 - preview_title.get_width()//2, preview_y - 30))

        # Generiere Vorschau
        selected_idx = 0
        for i, (name, desc, color, key) in enumerate(maps):
            brick_ratio = 0.5 if i == 0 else (0.4 if i == 1 else 0.6)

            for py in range(preview_grid_h):
                for px in range(preview_grid_w):
                    seed = px * 7 + py * 13 + i * 47
                    is_brick = (seed % 100) // 1 < (100 * brick_ratio)
                    cell_color = Config.COLOR_BRICK if is_brick else Config.COLOR_STEEL
                    pygame.draw.rect(self.screen, cell_color,
                                   (preview_x + px * preview_size, preview_y + py * preview_size,
                                    preview_size, preview_size))

            # Rahmen um ausgewählte Map
            if i == selected_idx:
                pulse = int(50 * math.sin(tick * 3))
                border_color = tuple(min(255, max(0, c + pulse)) for c in (255, 255, 0))
                pygame.draw.rect(self.screen, border_color,
                               (preview_x - 3, preview_y - 3, preview_w + 6, preview_h + 6), 3, border_radius=3)

        # Map-Buttons unterhalb der Vorschau
        btn_font = pygame.font.SysFont(None, 30, bold=True)
        btn_y = preview_y + preview_h + 30
        btn_width = 400
        btn_height = 55

        for i, (name, desc, color, key) in enumerate(maps):
            btn_x = Config.WIDTH//2 - btn_width//2

            # Button-Hintergrund
            pulse = int(25 * math.sin(tick * 2 + i * 0.5))
            hover_color = tuple(min(255, max(0, c + pulse)) for c in color)

            pygame.draw.rect(self.screen, (20, 20, 35), (btn_x, btn_y + i * 75, btn_width, btn_height), border_radius=8)
            pygame.draw.rect(self.screen, hover_color, (btn_x, btn_y + i * 75, btn_width, btn_height), 2, border_radius=8)

            # Key-Hint
            key_font = pygame.font.SysFont(None, 26)
            key_rendered = key_font.render(f"[{key}]", True, color)
            self.screen.blit(key_rendered, (btn_x + 15, btn_y + i * 75 + 16))

            # Map-Name
            name_rendered = btn_font.render(name, True, (255, 255, 255))
            self.screen.blit(name_rendered, (btn_x + 55, btn_y + i * 75 + 12))

            # Beschreibung
            desc_font = pygame.font.SysFont(None, 22)
            desc_rendered = desc_font.render(desc, True, (160, 160, 180))
            self.screen.blit(desc_rendered, (btn_x + 55, btn_y + i * 75 + 38))

        # Start-Button
        start_y = btn_y + 3 * 75 + 20
        start_pulse = int(40 * math.sin(tick * 4))
        start_color = (min(255, 255 + start_pulse), min(255, 255 + start_pulse), 0)

        pygame.draw.rect(self.screen, (40, 40, 20), (Config.WIDTH//2 - 200, start_y, 400, 55), border_radius=10)
        pygame.draw.rect(self.screen, start_color, (Config.WIDTH//2 - 200, start_y, 400, 55), 3, border_radius=10)

        start_font = pygame.font.SysFont(None, 32, bold=True)
        start_text = start_font.render("[SPACE] START MISSION", True, (255, 255, 255))
        self.screen.blit(start_text, (Config.WIDTH//2 - start_text.get_width()//2, start_y + 12))

        # Footer
        footer_y = box_y + box_height + 30
        footer_font = pygame.font.SysFont(None, 22)
        footer = footer_font.render("Press F for Fullscreen  |  Press ESC to Back", True, (120, 120, 160))
        self.screen.blit(footer, (Config.WIDTH//2 - footer.get_width()//2, footer_y))

    def _draw_game(self):
        """Zeichnet Gameplay"""
        # Hintergrund zeichnen
        self.background.draw(self.screen)

        # Screen shake effect
        shake_x = random.randint(-self.screen_shake, self.screen_shake)
        shake_y = random.randint(-self.screen_shake, self.screen_shake)
        offset_x = shake_x
        offset_y = shake_y

        # Draw Eagle
        if self.eagle:
            self.eagle.draw_adler(self.screen)

        # Draw Walls
        for wall in self.walls:
            wall.draw(self.screen)

        # Draw Players
        for p in self.players:
            p.draw(self.screen)

        # Draw Enemies
        for e in self.enemies:
            e.draw(self.screen)
            e.draw_health_bar(self.screen)

        # Draw Powerups
        for p in self.powerups:
            p.draw(self.screen)

        # Draw Bullets
        for b in self.bullets:
            b.draw_with_trail(self.screen)

        # Draw Particles
        for p in self.particles:
            p.draw(self.screen)

        # Draw UI
        self._draw_ui()

    def _draw_hud_panel(self, x, y, width, height, title=None):
        """Zeichnet ein HUD-Panel mit Hintergrund und Titel"""
        # Panel-Hintergrund mit Transparenz
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 100))
        self.screen.blit(panel, (x, y))

        # Panel-Rahmen
        pygame.draw.rect(self.screen, (80, 80, 120), (x, y, width, height), 2, border_radius=5)

        # Titel
        if title:
            title_font = pygame.font.SysFont(None, 22, bold=True)
            title_rendered = title_font.render(title, True, (180, 180, 220))
            self.screen.blit(title_rendered, (x + 10, y + 8))

    def _draw_ui(self):
        """Verbessertes HUD mit Panels und Lautstärkeregler"""
        tick = pygame.time.get_ticks() / 1000

        # === LINKES HUD PANEL ===
        panel_width = 220
        panel_height = 120
        panel_x = 15
        panel_y = 15

        self._draw_hud_panel(panel_x, panel_y, panel_width, panel_height, "MISSION STATUS")

        # Score
        score_y = panel_y + 35
        score_font = pygame.font.SysFont(None, 28, bold=True)
        score_text = score_font.render(f"Score: {self.score[1]}", True, Config.COLOR_P1)
        self.screen.blit(score_text, (panel_x + 15, score_y))

        # Wave
        if self.wave_manager:
            wave_text = f"Wave: {self.wave_manager.current_wave}/{self.wave_manager.total_waves}"
            wave_font = pygame.font.SysFont(None, 24)
            wave_rendered = wave_font.render(wave_text, True, Config.COLOR_P2)
            self.screen.blit(wave_rendered, (panel_x + 15, score_y + 35))

        # Time Limit
        time_remaining = max(0, self.time_limit - (self.game_time // 60))
        time_color = Config.COLOR_P1 if time_remaining > 60 else Config.COLOR_ENEMY
        time_text = f"Time: {time_remaining}s"
        time_font = pygame.font.SysFont(None, 24, bold=True)
        time_rendered = time_font.render(time_text, True, time_color)
        self.screen.blit(time_rendered, (panel_x + 15, score_y + 65))

        # === RECHTES HUD PANEL (Spieler-Info) ===
        player_panel_x = Config.WIDTH - 220
        player_panel_y = 15
        player_panel_height = 120 + len(self.players) * 30

        self._draw_hud_panel(player_panel_x, player_panel_y, panel_width, player_panel_height, "PLAYER STATUS")

        # === LAUTSTÄRKESLIDER (unten rechts) ===
        self._draw_volume_sliders()

        # Spieler-Infos
        info_y = player_panel_y + 35
        for p in self.players:
            player_font = pygame.font.SysFont(None, 24, bold=True)
            p_text = player_font.render(f"P{p.player_id}", True, p.color)
            self.screen.blit(p_text, (player_panel_x + 15, info_y))

            # Lives mit Icon
            lives_text = f"♥" * p.lives
            lives_font = pygame.font.SysFont(None, 20)
            lives_rendered = lives_font.render(lives_text, True, p.color)
            self.screen.blit(lives_rendered, (player_panel_x + 70, info_y + 2))

            info_y += 28

            # Shield-Indikator
            if p.shield_charges > 0:
                shield_text = f"🛡️ Shield: {p.shield_charges}"
                shield_font = pygame.font.SysFont(None, 20)
                shield_rendered = shield_font.render(shield_text, True, (0, 255, 255))
                self.screen.blit(shield_rendered, (player_panel_x + 15, info_y))
                info_y += 24

            # Double Shot-Indikator
            if p.double_shot_active:
                ds_pulse = int(50 * math.sin(tick * 5))
                ds_color = (min(255, 255 + ds_pulse), min(255, 255 + ds_pulse), 0)
                ds_text = "⚡ DOUBLE SHOT ACTIVE"
                ds_font = pygame.font.SysFont(None, 20, bold=True)
                ds_rendered = ds_font.render(ds_text, True, ds_color)
                self.screen.blit(ds_rendered, (player_panel_x + 15, info_y))

        # === UNTERE STATUSLEISTE ===
        status_bar_height = 40
        status_bar_y = Config.HEIGHT - status_bar_height - 5

        # Status-Panel
        status_panel = pygame.Surface((Config.WIDTH, status_bar_height), pygame.SRCALPHA)
        status_panel.fill((0, 0, 0, 80))
        self.screen.blit(status_panel, (0, status_bar_y))
        pygame.draw.line(self.screen, (80, 80, 120), (0, status_bar_y), (Config.WIDTH, status_bar_y), 2)

        # Eagle Status
        if self.eagle:
            if self.eagle.state == EagleState.PROTECTED:
                eagle_icon = "🦅"
                eagle_text = "EAGLE PROTECTED"
                eagle_color = Config.COLOR_EAGLE
            else:
                eagle_icon = "⚠️"
                eagle_text = "EAGLE UNDER ATTACK"
                eagle_color = Config.COLOR_ENEMY

            eagle_font = pygame.font.SysFont(None, 24, bold=True)
            eagle_rendered = eagle_font.render(f"{eagle_icon} {eagle_text}", True, eagle_color)
            self.screen.blit(eagle_rendered, (Config.WIDTH//2 - eagle_rendered.get_width()//2, status_bar_y + 10))

        # Lautstärkeregler-Hinweis
        vol_font = pygame.font.SysFont(None, 16)
        vol_text = vol_font.render("V/W: Musik  B/N: SFX  M: Mute", True, (150, 150, 200))
        self.screen.blit(vol_text, (Config.WIDTH - vol_text.get_width() - 15, status_bar_y + 5))

        # Pause-Hinweis
        pause_font = pygame.font.SysFont(None, 18)
        pause_rendered = pause_font.render("[ESC] Pause", True, (120, 120, 160))
        self.screen.blit(pause_rendered, (Config.WIDTH - pause_rendered.get_width() - 15, status_bar_y + 12))

    def _draw_volume_sliders(self):
        """Zeichnet Lautstärkeregler für Musik und SFX (unten rechts)"""
        slider_width = Config.VOLUME_SLIDER_WIDTH
        slider_height = Config.VOLUME_SLIDER_HEIGHT
        margin = 10

        # Panel-Hintergrund
        panel_x = Config.WIDTH - slider_width - margin * 2 - 15
        panel_y = Config.HEIGHT - 85
        panel_w = slider_width + margin * 2
        panel_h = 80

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 80))
        self.screen.blit(panel, (panel_x, panel_y))
        pygame.draw.rect(self.screen, (80, 80, 120), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=5)

        # Label-Font
        label_font = pygame.font.SysFont(None, 16, bold=True)
        slider_font = pygame.font.SysFont(None, 14)

        # Musik-Slider
        music_label = label_font.render("MUSIC", True, (200, 200, 255))
        self.screen.blit(music_label, (panel_x + margin, panel_y + margin))

        # Musik-Slider-Balken
        bar_x = panel_x + margin
        bar_y = panel_y + margin + 15
        bar_w = slider_width
        bar_h = slider_height - 6

        # Hintergrund
        pygame.draw.rect(self.screen, (40, 40, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=3)

        # Füllung Musik
        music_fill = int(bar_w * self.sound_manager.get_music_volume())
        music_rect = pygame.Rect(bar_x, bar_y, music_fill, bar_h)
        pygame.draw.rect(self.screen, (100, 200, 255), music_rect, border_radius=3)

        # Musik-Icon + Prozent
        music_icon = slider_font.render("♪", True, (255, 255, 100))
        self.screen.blit(music_icon, (bar_x + bar_w + 5, bar_y))
        music_pct = slider_font.render(f"{int(self.sound_manager.get_music_volume() * 100)}%", True, (200, 200, 255))
        self.screen.blit(music_pct, (bar_x + bar_w + 25, bar_y))

        # SFX-Slider
        sfx_label = label_font.render("SFX", True, (200, 255, 200))
        self.screen.blit(sfx_label, (panel_x + margin, panel_y + margin + 35))

        # SFX-Slider-Balken
        sfx_bar_y = bar_y + 25
        sfx_fill = int(bar_w * self.sound_manager.get_sfx_volume())
        sfx_rect = pygame.Rect(bar_x, sfx_bar_y, sfx_fill, bar_h)
        pygame.draw.rect(self.screen, (40, 40, 60), (bar_x, sfx_bar_y, bar_w, bar_h), border_radius=3)
        pygame.draw.rect(self.screen, (100, 255, 100), sfx_rect, border_radius=3)

        # SFX-Icon + Prozent
        sfx_icon = slider_font.render("♫", True, (255, 255, 100))
        self.screen.blit(sfx_icon, (bar_x + bar_w + 5, sfx_bar_y))
        sfx_pct = slider_font.render(f"{int(self.sound_manager.get_sfx_volume() * 100)}%", True, (200, 255, 200))
        self.screen.blit(sfx_pct, (bar_x + bar_w + 25, sfx_bar_y))

    def _handle_volume_slider_click(self, mouse_pos):
        """Behandelt Klick auf Lautstärkeregler"""
        slider_width = Config.VOLUME_SLIDER_WIDTH
        margin = 10

        panel_x = Config.WIDTH - slider_width - margin * 2 - 15
        panel_y = Config.HEIGHT - 85

        # Slider-Positionen
        bar_x = panel_x + margin
        bar_y = panel_y + margin + 15
        bar_w = slider_width
        bar_h = Config.VOLUME_SLIDER_HEIGHT - 6

        sfx_bar_y = bar_y + 25

        x, y = mouse_pos

        # Musik-Slider (oberer Balken)
        if (bar_x <= x <= bar_x + bar_w and
            bar_y <= y <= bar_y + bar_h):
            ratio = (x - bar_x) / bar_w
            self.sound_manager.set_music_volume(ratio)

        # SFX-Slider (unterer Balken)
        if (bar_x <= x <= bar_x + bar_w and
            sfx_bar_y <= y <= sfx_bar_y + bar_h):
            ratio = (x - bar_x) / bar_w
            self.sound_manager.set_sfx_volume(ratio)

    def _handle_volume_slider_drag(self, mouse_pos):
        """Behandelt Drag auf Lautstärkeregler"""
        slider_width = Config.VOLUME_SLIDER_WIDTH
        margin = 10

        panel_x = Config.WIDTH - slider_width - margin * 2 - 15
        panel_y = Config.HEIGHT - 85

        bar_x = panel_x + margin
        bar_y = panel_y + margin + 15
        bar_w = slider_width
        bar_h = Config.VOLUME_SLIDER_HEIGHT - 6

        sfx_bar_y = bar_y + 25

        x, y = mouse_pos

        # Nur bei gedrückter linker Maustaste
        mouse_buttons = pygame.mouse.get_pressed()
        if not mouse_buttons[0]:
            return

        # Musik-Slider
        if (bar_x <= x <= bar_x + bar_w and
            bar_y <= y <= bar_y + bar_h):
            ratio = max(0.0, min(1.0, (x - bar_x) / bar_w))
            self.sound_manager.set_music_volume(ratio)

        # SFX-Slider
        if (bar_x <= x <= bar_x + bar_w and
            sfx_bar_y <= y <= sfx_bar_y + bar_h):
            ratio = max(0.0, min(1.0, (x - bar_x) / bar_w))
            self.sound_manager.set_sfx_volume(ratio)

    def _draw_overlay(self, title, subtitle=None, buttons=None):
        """Zeichnet ein einheitliches Overlay für Menüs"""
        tick = pygame.time.get_ticks() / 1000

        # Dunkler Overlay-Hintergrund
        overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Hauptbox
        box_width = 550
        box_height = 400 if not buttons else 450
        box_x = Config.WIDTH//2 - box_width//2
        box_y = Config.HEIGHT//2 - box_height//2

        # Box-Hintergrund
        pygame.draw.rect(self.screen, (25, 25, 45), (box_x, box_y, box_width, box_height), border_radius=12)
        pygame.draw.rect(self.screen, (100, 100, 180), (box_x, box_y, box_width, box_height), 3, border_radius=12)

        # Titel
        title_y = box_y + 50
        title_font = pygame.font.SysFont(None, 72, bold=True)
        title_rendered = title_font.render(title, True, (0, 0, 0))
        self.screen.blit(title_rendered, (Config.WIDTH//2 - title_rendered.get_width()//2 + 3, title_y + 3))
        title_color = (255, 215, 0) if "VICTORY" in title else (255, 255, 255)
        if "GAME OVER" in title:
            title_color = (255, 80, 80)
        title_rendered = title_font.render(title, True, title_color)
        self.screen.blit(title_rendered, (Config.WIDTH//2 - title_rendered.get_width()//2, title_y))

        # Subtitle (optional)
        if subtitle:
            sub_y = title_y + 80
            sub_font = pygame.font.SysFont(None, 40, bold=True)
            sub_rendered = sub_font.render(subtitle, True, (200, 200, 200))
            self.screen.blit(sub_rendered, (Config.WIDTH//2 - sub_rendered.get_width()//2, sub_y))

        # Buttons (optional)
        if buttons:
            btn_y = box_y + box_height - 200
            btn_font = pygame.font.SysFont(None, 28, bold=True)

            for i, (text, key, color) in enumerate(buttons):
                btn_width = 380
                btn_height = 45
                btn_x = Config.WIDTH//2 - btn_width//2

                pulse = int(20 * math.sin(tick * 3 + i))
                hover_color = tuple(min(255, max(0, c + pulse)) for c in color)

                pygame.draw.rect(self.screen, (20, 20, 35),
                               (btn_x, btn_y + i * 60, btn_width, btn_height), border_radius=8)
                pygame.draw.rect(self.screen, hover_color,
                               (btn_x, btn_y + i * 60, btn_width, btn_height), 2, border_radius=8)

                # Key-Hint
                key_font = pygame.font.SysFont(None, 26)
                key_rendered = key_font.render(key, True, color)
                self.screen.blit(key_rendered, (btn_x + 15, btn_y + i * 60 + 11))

                # Button-Text
                text_rendered = btn_font.render(text, True, (255, 255, 255))
                self.screen.blit(text_rendered, (btn_x + 55, btn_y + i * 60 + 11))

    def _draw_paused(self):
        """Verbesserter Pause-Screen"""
        self._draw_overlay(
            title="⏸ PAUSED",
            buttons=[
                ("Resume Game", "[ESC/P]", (0, 255, 0)),
                ("Restart Mission", "[R]", (255, 215, 0)),
                ("Quit to Menu", "[Q]", (255, 100, 100)),
            ]
        )

    def _draw_gameover(self):
        """Verbessertes Game Over Screen"""
        self._draw_overlay(
            title="MISSION FAILED",
            subtitle=f"Final Score: {self.score[1]}",
            buttons=[
                ("Return to Menu", "[SPACE]", (200, 200, 200)),
                ("Restart Mission", "[1]", (0, 255, 0)),
                ("New Game Mode", "[2]", (255, 165, 0)),
            ]
        )
        self.sound_manager.play_lose()

    def _draw_victory(self):
        """Verbessertes Victory Screen"""
        tick = pygame.time.get_ticks() / 1000

        self._draw_overlay(
            title="🏆 VICTORY!",
            subtitle=f"Final Score: {self.score[1]}",
            buttons=[
                ("Return to Menu", "[SPACE]", (200, 200, 200)),
                ("Play Again", "[1]", (0, 255, 0)),
                ("Harder Mode", "[2]", (255, 165, 0)),
            ]
        )

        if not self._victory_played:
            self.sound_manager.play_win()
            self._victory_played = True

        # Konfetti-Partikel
        for _ in range(3):
            conf_x = random.randint(0, Config.WIDTH)
            conf_y = random.randint(Config.HEIGHT//2 - 200, Config.HEIGHT//2)
            conf_color = random.choice([(255, 215, 0), (255, 0, 0), (0, 255, 0), (0, 100, 255)])
            pygame.draw.circle(self.screen, conf_color, (int(conf_x), int(conf_y)), random.randint(2, 5))

    def run(self):
        """Haupt-Spiel-Schleife"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(Config.FPS)

        pygame.quit()

# ============================================================================
# MAIN
# ============================================================================
def main():
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main()
