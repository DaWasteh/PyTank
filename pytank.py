from __future__ import annotations

import math
import random
import threading
from typing import TypedDict

import pygame

Color = tuple[int, int, int]


class MapConfig(TypedDict, total=False):
    name: str
    desc: str
    type: str
    color: Color
    steel_ratio: float
    brick_ratio: float


MissionEnemy = tuple[int, int, str, str]


class MissionConfig(TypedDict):
    title: str
    difficulty: str
    intro: str
    victory: str
    enemies: list[MissionEnemy]


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

    # Erweiterte Farben für bessere Optik
    COLOR_P1_GLOW = (255, 255, 100)
    COLOR_P2_GLOW = (100, 255, 100)
    COLOR_ENEMY_BRIGHT = (255, 80, 80)
    COLOR_BRICK_LIGHT = (180, 100, 50)
    COLOR_STEEL_HIGHLIGHT = (200, 200, 210)
    COLOR_FIRE = [(255, 80, 0), (255, 160, 0), (255, 220, 0), (255, 255, 50), (255, 60, 0)]
    COLOR_SMOKE = [(80, 80, 80), (100, 100, 100), (120, 120, 120), (60, 60, 60)]
    COLOR_SPARK = [(255, 255, 200), (255, 200, 100), (255, 255, 255)]

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
    MAPS: dict[str, MapConfig] = {
        "classic": {"name": "Classic", "desc": "Faire Spiegelkarte", "type": "symmetric", "color": (255, 220, 60)},
        "industrial": {"name": "Industrial", "desc": "Stahl & Korridore", "steel_ratio": 0.42, "color": (80, 220, 255)},
        "desert": {"name": "Desert", "desc": "Zerstörbare Sandruinen", "brick_ratio": 0.68, "color": (255, 175, 70)},
        "arena": {"name": "Arena", "desc": "Offen, schnell, wenig Deckung", "color": (205, 150, 255)},
        "crossfire": {"name": "Crossfire", "desc": "Vier Basen, zentrale Hotzone", "color": (255, 95, 95)},
        "islands": {"name": "Islands", "desc": "Inseln mit Brückenlinien", "color": (90, 255, 170)},
        "mission_1": {"name": "Mission 1: Tor", "desc": "Tutorial: Pythaner-Tor", "color": (120, 255, 160)},
        "mission_2": {"name": "Mission 2: Rostpass", "desc": "Quest: Konvoi sichern", "color": (255, 195, 80)},
        "mission_3": {"name": "Mission 3: Ferrum-Brücke", "desc": "Finale: Rust-Angriff stoppen", "color": (255, 105, 105)},
    }
    MAP_ORDER: list[str] = ["classic", "industrial", "desert", "arena", "crossfire", "islands"]
    MISSION_ORDER: list[str] = ["mission_1", "mission_2", "mission_3"]
    FFA_TOTAL_TANKS = 8

    MISSION_DATA: dict[str, MissionConfig] = {
        "mission_1": {
            "title": "Die letzte Hoffnung",
            "difficulty": "super leicht",
            "intro": "Kommandant: Die Rusts greifen das Pythaner-Tor an! Ihr seid die letzte Hoffnung, Pythy-Wan {player}. Ziele: Bewegen, zielen, zwei Vorposten ausschalten.",
            "victory": "Kommandant: Hervorragend, Pythy-Wan {player}! Das Tor steht.",
            "enemies": [
                (1350, 210, "scout", "Leicht"),
                (1260, 850, "scout", "Leicht"),
            ],
        },
        "mission_2": {
            "title": "Der Rostpass",
            "difficulty": "leicht",
            "intro": "Kommandant: Die Rusts versperren den Rostpass. Pythy-Wan {player}, räumt die Barrikaden und schützt unseren kleinen Konvoi.",
            "victory": "Kommandant: Saubere Arbeit! Der Rostpass ist frei.",
            "enemies": [
                (1280, 170, "scout", "Leicht"),
                (1370, 520, "gunner", "Leicht"),
                (1180, 870, "gunner", "Mittel"),
                (740, 190, "scout", "Leicht"),
            ],
        },
        "mission_3": {
            "title": "Ferrum-Brücke",
            "difficulty": "mittel",
            "intro": "Kommandant: Letzte Meldung: Ein Rust-Trupp rollt zur Ferrum-Brücke. Pythy-Wan {player}, haltet sie auf, bevor sie Pythania erreichen!",
            "victory": "Kommandant: Fantastisch! Die Rusts ziehen sich zurück.",
            "enemies": [
                (1310, 150, "scout", "Mittel"),
                (1380, 430, "gunner", "Mittel"),
                (1180, 760, "gunner", "Mittel"),
                (920, 930, "brute", "Mittel"),
                (540, 220, "scout", "Mittel"),
                (410, 780, "brute", "Schwer"),
            ],
        },
    }

    # Wave Settings
    TOTAL_WAVES = 10
    BOSS_WAVE = 10  # Boss-Welle am Ende
    TIME_LIMIT = 300  # Sekunden (5 Minuten)

    # Respawn Settings
    RESPAWN_COOLDOWN = 3  # Sekunden

    # AI Settings
    AI_REACTION_FRAMES = 15
    AI_SHOOT_COOLDOWN_MIN = 40
    AI_SHOOT_COOLDOWN_MAX = 90
    AI_FLANK_CHANCE = 0.25
    AI_USE_COVER = True
    AI_COORDINATED_ATTACK = True
    AI_PATROL_AGGRESSIVENESS = 0.4
    AI_SHOOT_ACCURACY = 0.85
    PARTICLE_COUNT_MULTIPLIER = 2
    AMBIENT_VOLUME = 0.08

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
    REPAIR_AMOUNT = 2  # Health-Punkte (max. Config.MAX_LIVES * 2)

    # Sound Settings (Hochwertige synthetisierte Sounds)
    SOUND_SAMPLE_RATE = 48000
    MUSIC_VOLUME = 0.25       # Standard Lautstärke Musik (0.0 - 1.0)
    SFX_VOLUME = 0.6          # Standard Lautstärke SFX (0.0 - 1.0)
    MAX_SOUNDS = 48           # Mehr Kanäle für komplexe Sounds
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
    MISSIONS = "MISSIONS"

class Difficulty:
    EASY = "Leicht"
    MEDIUM = "Mittel"
    HARD = "Schwer"
    MIXED = "Mixed"
    ORDER = [EASY, MEDIUM, HARD, MIXED]
    AI_POOL = [EASY, MEDIUM, HARD]
    LABELS = {
        EASY: "Leicht",
        MEDIUM: "Mittel",
        HARD: "Schwer",
        MIXED: "Mixed",
    }

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
    """Zeichnet Hintergrund mit Grid-Muster, pulsierendem Glow und atmosphärischer Beleuchtung"""
    def __init__(self, grid_size=50) -> None:
        self.grid_size = grid_size
        self.background = None

    def draw(self, surface) -> None:
        """Zeichnet den verbesserten Hintergrund"""
        tick = pygame.time.get_ticks() / 1000

        # Dunkler Hintergrund
        surface.fill((18, 18, 24))

        # Pulsierendes Grid
        grid_color_base = (45, 45, 55)
        for i in range(0, Config.HEIGHT, self.grid_size):
            pulse = int(15 * math.sin(tick * 0.5 + i / 150))
            alpha = 25 + pulse
            color = (*grid_color_base, max(10, min(50, alpha)))
            pygame.draw.line(surface, color, (0, i), (Config.WIDTH, i), 1)

        for i in range(0, Config.WIDTH, self.grid_size):
            pulse = int(15 * math.cos(tick * 0.5 + i / 150))
            alpha = 25 + pulse
            color = (*grid_color_base, max(10, min(50, alpha)))
            pygame.draw.line(surface, color, (i, 0), (i, Config.HEIGHT), 1)

        # Zentrale Beleuchtung (Eagle-Bereich)
        eagle_x, eagle_y = Config.WIDTH // 2, Config.HEIGHT - 60
        glow_radius = 200
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        glow_alpha = int(15 + 5 * math.sin(tick * 0.8))
        glow_color = (255, 215, 0, glow_alpha)
        pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surf, (eagle_x - glow_radius, eagle_y - glow_radius))

class EagleState:
    PROTECTED = "protected"
    HIT = "hit"

# ============================================================================
# BASE CLASSES
# ============================================================================
class GameObject:
    def __init__(self, x, y, width, height, color) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

class Entity(GameObject):
    def __init__(self, x, y, width, height, color) -> None:
        super().__init__(x, y, width, height, color)
        self.direction = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)

    def move(self, dx, dy, walls, screen_shake=0) -> None:
        # Apply screen shake
        shake_x = random.randint(-screen_shake, screen_shake)
        shake_y = random.randint(-screen_shake, screen_shake)

        # Try moving in X
        self.rect.x += dx + shake_x
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                elif dx < 0:
                    self.rect.left = wall.rect.right

        # Check screen boundary X
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Config.WIDTH:
            self.rect.right = Config.WIDTH

        # Try moving in Y
        self.rect.y += dy + shake_y
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                elif dy < 0:
                    self.rect.top = wall.rect.bottom

        # Check screen boundary Y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Config.HEIGHT:
            self.rect.bottom = Config.HEIGHT

# ============================================================================
# GAME OBJECTS
# ============================================================================
class Wall(GameObject):
    """Wand-Objekt mit vorge-renderter Textur für stabile Performance"""

    # Klassen-level Cache für Texturen (eine pro Typ)
    _brick_texture = None
    _steel_texture = None
    TEXTURE_SIZE = 50  # Muss mit Config.GRID_SIZE übereinstimmen

    def __init__(self, x, y, width, height, wall_type) -> None:
        if wall_type == WallType.BRICK:
            color = Config.COLOR_BRICK
            destructible = True
        else:
            color = Config.COLOR_STEEL
            destructible = False
        super().__init__(x, y, width, height, color)
        self.wall_type = wall_type
        self.destructible = destructible

        # Stelle sicher, dass Texturen initialisiert sind
        if Wall._brick_texture is None:
            Wall._init_textures()

    @classmethod
    def _init_textures(cls) -> None:
        """Initialisiert vorge-renderete Texturen mit 3D-Effekten (einmalig)"""
        size = cls.TEXTURE_SIZE

        # Ziegel-Textur mit besserem Design
        brick_tex = pygame.Surface((size, size), pygame.SRCALPHA)
        brick_tex.fill((*Config.COLOR_BRICK, 255))

        # Größere Ziegel mit Fugen
        brick_color = (100, 55, 15)
        brick_light = (180, 100, 50)
        for i in range(0, size, 12):
            pygame.draw.line(brick_tex, brick_color, (i, 0), (i, size), 1)
        for j in range(0, size, 12):
            offset = 6 if j % 24 == 0 else 0
            pygame.draw.line(brick_tex, brick_color, (offset, j), (size, j), 1)

        # 3D-Highlights für Ziegel
        for j in range(0, size, 12):
            offset = 6 if j % 24 == 0 else 0
            pygame.draw.line(brick_tex, brick_light, (offset + 1, j), (offset + 1, j + 11), 1)
            pygame.draw.line(brick_tex, brick_light, (offset, j + 1), (size, j + 1), 1)

        # Subtiles Wärme-Overlay
        overlay = pygame.Surface((size, size), pygame.SRCALPHA)
        overlay.fill((200, 130, 60, 25))
        brick_tex.blit(overlay, (0, 0))

        cls._brick_texture = brick_tex

        # Stahl-Textur mit Metallic-Effekt und Nieten
        steel_tex = pygame.Surface((size, size), pygame.SRCALPHA)
        steel_tex.fill((*Config.COLOR_STEEL, 255))

        steel_color = (140, 140, 150)
        for i in range(0, size, 12):
            pygame.draw.line(steel_tex, steel_color, (i, 0), (i, size), 1)
        for j in range(0, size, 12):
            pygame.draw.line(steel_tex, steel_color, (0, j), (size, j), 1)

        # Nieten an Kreuzungen
        rivet_color = (170, 170, 180)
        for i in range(0, size, 12):
            for j in range(0, size, 12):
                pygame.draw.circle(steel_tex, rivet_color, (i, j), 2)
                pygame.draw.circle(steel_tex, (200, 200, 210), (i - 1, j - 1), 1)

        # Diagonale Metallic-Highlights
        for i in range(0, size, 20):
            pygame.draw.line(steel_tex, (200, 200, 210, 40), (i, 0), (min(i + 10, size), 10), 1)
            pygame.draw.line(steel_tex, (200, 200, 210, 30), (0, i), (10, min(i + 10, size)), 1)

        cls._steel_texture = steel_tex

    def draw(self, surface) -> None:
        """Zeichnet Wand mit vorge-renderter Textur und 3D-Effekt"""
        if self.wall_type == WallType.BRICK:
            tex = Wall._brick_texture
        else:
            tex = Wall._steel_texture

        if tex is None:
            return

        if self.rect.width != Wall.TEXTURE_SIZE or self.rect.height != Wall.TEXTURE_SIZE:
            scaled_tex = pygame.transform.scale(tex, (self.rect.width, self.rect.height))
            surface.blit(scaled_tex, self.rect.topleft)
        else:
            surface.blit(tex, self.rect.topleft)

        # 3D-Schatten (unten und rechts)
        pygame.draw.rect(surface, (50, 50, 50),
                        (self.rect.x, self.rect.y + self.rect.height - 2,
                         self.rect.width, 2))
        pygame.draw.rect(surface, (50, 50, 50),
                        (self.rect.x + self.rect.width - 2, self.rect.y,
                         2, self.rect.height))
        # 3D-Licht (oben und links)
        pygame.draw.rect(surface, (100, 100, 100),
                        (self.rect.x, self.rect.y,
                         self.rect.width, 2))
        pygame.draw.rect(surface, (100, 100, 100),
                        (self.rect.x, self.rect.y,
                         2, self.rect.height))

        pygame.draw.rect(surface, (55, 55, 65), self.rect, 1)

class Bullet(GameObject):
    def __init__(self, x, y, direction, color, owner, trail_length=10, team_id=None, source=None) -> None:
        super().__init__(x, y, 8, 8, color)
        self.direction = direction
        self.owner = owner
        self.team_id = team_id
        self.source = source
        self.trail: list[tuple[int, int]] = []
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

    def draw_with_trail(self, surface) -> None:
        cx, cy = self.rect.centerx, self.rect.centery

        # Trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / self.trail_length) * 0.6)
            color = (*self.color[:3], alpha)
            size = int(2 * (i / self.trail_length))
            pygame.draw.circle(surface, color, (tx, ty), max(1, size))

        # Large outer glow
        glow_surf = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
        glow_color = (*self.color[:3], 60)
        pygame.draw.circle(glow_surf, glow_color, (10, 10), 10)
        surface.blit(glow_surf, (cx - 10, cy - 10))

        # Inner glow
        inner_glow = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
        inner_color = (*self.color[:3], 120)
        pygame.draw.circle(inner_glow, inner_color, (5, 5), 5)
        surface.blit(inner_glow, (cx - 5, cy - 5))

        # Bright core
        pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 2)
        pygame.draw.circle(surface, self.color, (cx, cy), 4)

class Powerup(GameObject):
    """Powerup-Objekt mit verbessertem Design"""
    SHIELD = "shield"
    DOUBLE_SHOT = "double_shot"
    REPAIR = "repair"

    def __init__(self, x, y, powerup_type) -> None:
        super().__init__(x, y, 20, 20, (255, 255, 0))
        self.powerup_type = powerup_type
        self.pulse = 0.0
        self.hitbox = self.rect.inflate(30, 30)

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

    def update(self) -> None:
        """Update Powerup"""
        self.pulse += 0.1

    def draw(self, surface) -> None:
        """Zeichnet Powerup mit verbessertem Puls-Effekt"""
        # Verwende Sinus für pulsierende Größe, damit sie nicht unendlich wächst
        pulse_val = math.sin(pygame.time.get_ticks() / 200)
        pulse_size = 10 + int((pulse_val + 1) * 5)

        # Pulsierender Hintergrund mit Glow
        alpha = int(100 + 100 * pulse_val)
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
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 20, 20, Config.COLOR_EAGLE)
        self.state = EagleState.PROTECTED

    def draw_adler(self, surface) -> None:
        """Zeichnet den Adler mit atmosphärischem Glow und animiertem Schutzring"""
        tick = pygame.time.get_ticks() / 1000

        if self.state == EagleState.HIT:
            # Zerstörter Adler mit Rauch-X
            pygame.draw.rect(surface, (80, 80, 80), self.rect)
            pygame.draw.line(surface, (255, 50, 50),
                           (self.rect.left, self.rect.top),
                           (self.rect.right, self.rect.bottom), 2)
            pygame.draw.line(surface, (255, 50, 50),
                           (self.rect.right, self.rect.top),
                           (self.rect.left, self.rect.bottom), 2)
            return

        cx, cy = self.rect.centerx, self.rect.centery

        # Atmosphärischer Glow
        glow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        pulse = int(20 + 15 * math.sin(tick * 2))
        glow_rgba = (255, 215, 0, pulse)
        pygame.draw.circle(glow_surf, glow_rgba, (30, 30), 30)
        surface.blit(glow_surf, (cx - 30, cy - 30))

        wing_size = 14

        # Flügel (dunkler Umriss)
        pygame.draw.polygon(surface, (180, 150, 0), [
            (cx, cy), (cx - wing_size, cy - wing_size), (cx - wing_size * 2, cy),
            (cx - wing_size, cy + wing_size), (cx, cy + wing_size * 2),
            (cx + wing_size, cy + wing_size), (cx + wing_size * 2, cy),
            (cx + wing_size, cy - wing_size)
        ])
        # Flügel (heller)
        pygame.draw.polygon(surface, Config.COLOR_EAGLE, [
            (cx, cy), (cx - wing_size + 2, cy - wing_size + 2), (cx - wing_size * 2 + 2, cy),
            (cx - wing_size + 2, cy + wing_size - 2), (cx, cy + wing_size * 2 - 2),
            (cx + wing_size - 2, cy + wing_size - 2), (cx + wing_size * 2 - 2, cy),
            (cx + wing_size - 2, cy - wing_size + 2)
        ])

        # Körper mit Glanzpunkt
        pygame.draw.circle(surface, (200, 180, 0), (cx, cy), 8)
        pygame.draw.circle(surface, Config.COLOR_EAGLE, (cx, cy), 7)
        pygame.draw.circle(surface, (255, 255, 200), (cx - 2, cy - 2), 3)

        # Animierte Schutzringe
        pulse = int(3 * math.sin(tick * 3))
        ring_alpha = int(100 + 50 * math.sin(tick * 2))
        pygame.draw.circle(surface, (255, 255, 200, ring_alpha), (cx, cy), 14 + pulse, 2)
        pulse2 = int(2 * math.sin(tick * 1.5 + 1))
        pygame.draw.circle(surface, (255, 215, 0, 60), (cx, cy), 18 + pulse2, 1)

class Particle(GameObject):
    """Partikel-Effekt für Explosionen - Feuer, Rauch, Funken"""
    def __init__(self, x, y, color, vx, vy, life, size=2, particle_type="normal") -> None:
        super().__init__(x, y, size * 2, size * 2, color)
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.size = float(size)
        self.particle_type = particle_type
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-5, 5)

    def update(self) -> None:
        """Update Partikel mit physik-basierter Bewegung"""
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life -= 1
        self.rotation += self.rot_speed

        if self.particle_type == "fire":
            self.vy -= 0.1
            self.vx *= 0.98
        elif self.particle_type == "smoke":
            self.vy -= 0.05
            self.vx *= 0.99
            self.size = max(1, self.size + 0.05)
        elif self.particle_type == "spark":
            self.vy += 0.15
            self.vx *= 0.99
        else:
            self.vx *= 0.97
            self.vy *= 0.97

        if (self.rect.x < -20 or self.rect.x > Config.WIDTH + 20 or
            self.rect.y < -20 or self.rect.y > Config.HEIGHT + 20):
            self.life = 0

    def draw(self, surface) -> None:
        """Zeichnet Partikel mit typ-spezifischem Effekt"""
        life_ratio = self.life / self.max_life
        alpha = int(255 * life_ratio)

        if self.particle_type == "fire":
            size = int(self.size * (0.5 + life_ratio * 1.5))
            glow_surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
            glow_color = (255, min(255, int(200 * life_ratio)), 0, int(80 * life_ratio))
            pygame.draw.circle(glow_surf, glow_color, (size * 2, size * 2), size * 2)
            surface.blit(glow_surf, (int(self.rect.x - size * 2), int(self.rect.y - size * 2)))
            core_color = (255, min(255, int(150 + 105 * life_ratio)), int(50 * life_ratio), alpha)
            pygame.draw.circle(surface, core_color, (int(self.rect.centerx), int(self.rect.centery)), max(1, size))
        elif self.particle_type == "smoke":
            size = int(self.size * (1 + (1 - life_ratio) * 2))
            smoke_surf = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
            smoke_color = (60, 60, 60, int(60 * life_ratio))
            pygame.draw.circle(smoke_surf, smoke_color, (size * 1.5, size * 1.5), size * 1.5)
            surface.blit(smoke_surf, (int(self.rect.x - size * 1.5), int(self.rect.y - size * 1.5)))
        elif self.particle_type == "spark":
            size = max(1, int(self.size * life_ratio))
            spark_color = (255, 255, min(255, int(200 + 55 * life_ratio)), alpha)
            pygame.draw.circle(surface, spark_color, (int(self.rect.centerx), int(self.rect.centery)), size)
            glow_color = (255, 255, 200, int(50 * life_ratio))
            pygame.draw.circle(surface, glow_color, (int(self.rect.centerx), int(self.rect.centery)), size + 2)
        else:
            size = int(self.size * life_ratio)
            color = (*self.color[:3], alpha)
            pygame.draw.circle(surface, color, (int(self.rect.centerx), int(self.rect.centery)), max(1, size))

# ============================================================================
# SOUND MANAGER (Hochwertige synthetisierte Sounds)
# ============================================================================
class SoundManager:
    """Modernes Audio-System mit hochwertigen synthetisierten Sounds

    Alle Sounds werden in Echtzeit synthetisiert mit:
    - Mehrschichtigen Klangquellen für natürliche Tiefe
    - ADSR-Envelopes für weiche Übergänge
    - Frequenz-modulation für realistische Texturen
    - 3D-Raumklang durch Panning
    """

    # Vorberechnete Sound-Caches für Performance
    _sound_cache: dict = {}
    CACHE_MAX = 64

    def __init__(self, frequency=None, channels=None, buffer=None) -> None:
        # Verwende übergebene Werte oder Defaults
        freq = frequency or Config.SOUND_SAMPLE_RATE
        chans = channels or Config.MAX_SOUNDS
        buf = buffer or 4096
        self._sound_available = False
        try:
            pygame.mixer.init(frequency=freq, size=-16, channels=chans, buffer=buf)
            self._sound_available = True
        except pygame.error:
            # Audio device not available (e.g., in headless CI environments)
            self._sound_available = False

        self._music_playing = False
        self._music_thread: threading.Thread | None = None
        self._music_volume = Config.MUSIC_VOLUME
        self._sfx_volume = Config.SFX_VOLUME
        self._duck_timer = 0
        self._audio_time = 0  # Für zeitbasierte Effekte

        # Sound-Variationen
        self._shoot_variations = 8
        self._brick_variations = 8
        self._steel_variations = 8
        self._tank_variations = 10
        self._current_shoot = 0
        self._current_brick = 0
        self._current_steel = 0
        self._current_tank = 0

    def set_music_volume(self, volume: float) -> None:
        """Setzt die Musiklautstärke (0.0 = stumm, 1.0 = maximal)"""
        self._music_volume = max(0.0, min(1.0, volume))
        Config.MUSIC_VOLUME = self._music_volume

    def set_sfx_volume(self, volume: float) -> None:
        """Setzt die SFX-Lautstärke (0.0 = stumm, 1.0 = maximal)"""
        self._sfx_volume = max(0.0, min(1.0, volume))
        Config.SFX_VOLUME = self._sfx_volume

    def get_music_volume(self) -> float:
        return self._music_volume

    def get_sfx_volume(self) -> float:
        return self._sfx_volume

    def _get_sfx_volume(self, base_volume: float = 0.3) -> float:
        """Ermittelt effektive SFX-Lautstärke mit Basis-Lautstärke"""
        return min(1.0, base_volume * self._sfx_volume * 2.2)

    def _make_key(self, *args) -> str:
        """Erstellt einen Cache-Schlüssel aus Argumenten"""
        return "|".join(str(a) for a in args)

    def _cache_get_or_create(self, key, factory):
        """Holt oder erstellt einen gecachten Sound"""
        if key not in SoundManager._sound_cache:
            sound = factory()
            if len(SoundManager._sound_cache) >= SoundManager.CACHE_MAX:
                # Ältesten Eintrag entfernen
                old_key = next(iter(SoundManager._sound_cache))
                del SoundManager._sound_cache[old_key]
            SoundManager._sound_cache[key] = sound
        return SoundManager._sound_cache[key]

    def _synthesize_wave(self, wave_type: str, frequency: float,
                         duration_ms: float, volume: float, fade_out: float = 0.15,
                         harmonics = None, vibrato: float = 0.0, tremolo: float = 0.0):
        """Hochwertige Sound-Synthese mit Overtones und Modulation

        Args:
            wave_type: 'sine', 'triangle', 'sawtooth', 'square', 'square_soft'
            frequency: Grundfrequenz in Hz
            duration_ms: Dauer in Millisekunden
            volume: Lautstärke (0.0-1.0)
            fade_out: Ausklingzeit in Sekunden
            harmonics: Liste von (multiplikator, gewicht) für Overtones
            vibrato: Vibrato-Tiefe in Hz
            tremolo: Tremolo-Tiefe (0.0-1.0)
        """
        sample_rate = pygame.mixer.get_init()[0]
        num_samples = int(sample_rate * duration_ms / 1000)
        if num_samples < 1:
            num_samples = 1

        # ADSR-Envelope
        attack_ms = max(3, duration_ms * 0.01)
        attack_samples = int(sample_rate * attack_ms / 1000)
        decay_samples = int(sample_rate * (duration_ms * 0.1) / 1000)
        release_samples = min(int(sample_rate * fade_out / 1000), num_samples // 4)

        output = bytearray(num_samples * 2)

        for i in range(num_samples):
            # Envelope
            if i < attack_samples:
                env = i / attack_samples
            elif i < attack_samples + decay_samples:
                env = 1.0 - (i - attack_samples) / decay_samples * 0.2
            elif i > num_samples - release_samples:
                env = (num_samples - i) / release_samples
            else:
                env = 0.8

            # Tremolo
            if tremolo > 0:
                env *= 1.0 - tremolo * 0.5 * (1 + math.sin(2 * math.pi * 5 * i / sample_rate))

            time = i / sample_rate

            # Hauptwelle mit Vibrato
            if vibrato > 0:
                phase = 2 * math.pi * frequency * (time + vibrato * math.sin(2 * math.pi * 4 * time))
            else:
                phase = 2 * math.pi * frequency * time

            # Grundwelle
            if wave_type == 'sine':
                val = math.sin(phase)
            elif wave_type == 'triangle':
                val = 2.0 * abs(2.0 * ((frequency * time) % 1.0) - 1.0) - 1.0
                val = math.tanh(val * 0.7)  # Weichzeichnen
            elif wave_type == 'sawtooth':
                raw = 2.0 * ((frequency * time) % 1.0) - 1.0
                val = math.tanh(raw * 0.4)
            elif wave_type == 'square':
                val = 1.0 if math.sin(phase) > 0 else -1.0
                val = math.tanh(val * 0.3)
            elif wave_type == 'square_soft':
                duty = 0.25 + 0.1 * math.sin(phase * 0.5)
                val = (1.0 if (phase % (2 * math.pi)) / (2 * math.pi) < duty else -1.0)
                val = math.tanh(val * 0.35)
            else:
                val = math.sin(phase)

            # Overtones hinzufügen
            if harmonics:
                for mult, weight in harmonics:
                    harmonic_phase = 2 * math.pi * frequency * mult * time
                    if wave_type == 'sine':
                        harmonic_val = math.sin(harmonic_phase)
                    elif wave_type == 'triangle':
                        harmonic_val = 2.0 * abs(2.0 * ((frequency * mult * time) % 1.0) - 1.0) - 1.0
                        harmonic_val = math.tanh(harmonic_val * 0.5)
                    else:
                        harmonic_val = math.sin(harmonic_phase)
                    val += harmonic_val * weight

            val = math.tanh(val * 0.8)  # Soft-Clipping für warme Klänge
            sample = int(32767 * volume * env * val)
            sample = max(-32767, min(32767, sample))

            # Stereo-Ausgabe (L/R)
            idx = i * 2
            output[idx] = sample & 0xFF
            output[idx + 1] = (sample >> 8) & 0xFF

        return pygame.mixer.Sound(bytes(output))

    def _synthesize_noise(self, duration_ms: float, volume: float,
                          lowpass: float = 200, noise_type: str = 'white',
                          highpass: float = 100, sweep: float = 0):
        """Hochwertiges Rauschen mit Filtern und Frequenz-Sweep

        Args:
            noise_type: 'white', 'pink', 'brown'
            lowpass: Tiefpass-Frequenz
            highpass: Hochpass-Frequenz
            sweep: Frequenz-Sweep am Ende (0 = kein Sweep)
        """
        sample_rate = pygame.mixer.get_init()[0]
        num_samples = int(sample_rate * duration_ms / 1000)
        if num_samples < 1:
            num_samples = 1

        prev_noise = 0.0
        prev_filtered = 0.0
        cutoff_low = lowpass / sample_rate
        max(highpass / sample_rate, 0.01)

        output = bytearray(num_samples * 2)

        for i in range(num_samples):
            time = i / sample_rate

            # ADSR-Envelope
            attack_s = int(sample_rate * 0.002)
            release_s = int(sample_rate * duration_ms / 3000)

            if i < attack_s:
                env = i / attack_s
            elif i > num_samples - release_s:
                env = (num_samples - i) / release_s
            else:
                env = 1.0

            # Noise-Quelle
            if noise_type == 'white':
                noise = random.uniform(-1, 1)
            elif noise_type == 'pink':
                # Pink Rauschen: gleichmäßige Energie pro Oktave
                noise = (random.uniform(-1, 1) + random.uniform(-1, 1) + random.uniform(-1, 1)) / 3
                noise = math.tanh(noise * 0.8)
            elif noise_type == 'brown':
                # Brownes Rauschen: mehr Tiefton
                noise = prev_noise * 0.98 + random.uniform(-1, 1) * 0.15
                noise = math.tanh(noise)
            else:
                noise = random.uniform(-1, 1)

            # Frequenz-Sweep
            if sweep > 0:
                sweep_factor = 1.0 - (i / num_samples) * sweep
                cutoff_low *= sweep_factor

            # Hochpass-Filter
            filtered_high = noise - prev_filtered
            prev_filtered = prev_filtered + filtered_high * 0.1

            # Tiefpass-Filter (IIR)
            filtered = prev_filtered * (1 - cutoff_low) + filtered_high * cutoff_low
            prev_filtered = filtered

            # Sub-Bass-Schicht für Tiefe
            bass_freq = 35 + 15 * math.sin(time * 2)
            bass = math.sin(2 * math.pi * bass_freq * time) * 0.25
            bass = math.tanh(bass)

            # Kombination
            combined = (filtered * 0.6 + bass * 0.4) * volume * env
            combined = math.tanh(combined)

            sample = int(32767 * combined)
            idx = i * 2
            output[idx] = sample & 0xFF
            output[idx + 1] = (sample >> 8) & 0xFF

        return pygame.mixer.Sound(bytes(output))

    def _play_stereo(self, left_sound, right_sound, pan: float = 0.5) -> None:
        """Spielt zwei Sounds mit Panning ab (links-rechts Positionierung)"""
        if pan < 0.3 or pan > 0.7:
            pass
        else:
            pass

        # Einfach: linken Sound mit angepasster Lautstärke abspielen
        if left_sound:
            left_sound.play()

    def play_shoot(self) -> None:
        """Hochwertiger Schuss-Sound mit mehreren Schichten"""
        if not self._sound_available:
            return
        var = self._current_shoot % self._shoot_variations
        self._current_shoot += 1
        vol = self._get_sfx_volume(0.25)

        if var == 0:
            # Klassischer Schuss: Knall + kurzer Ton
            s1 = self._synthesize_wave('square_soft', 180, 80, vol * 0.5, fade_out=0.05)
            s2 = self._synthesize_noise(40, vol * 0.4, lowpass=1500, noise_type='white')
            s1.play()
            s2.play()

        elif var == 1:
            # Tiefer Schuss: Bass-Druck + Knacken
            s1 = self._synthesize_wave('triangle', 120, 100, vol * 0.4, harmonics=[(2, 0.3)])
            s2 = self._synthesize_noise(50, vol * 0.35, lowpass=2000, noise_type='white')
            s1.play()
            s2.play()

        elif var == 2:
            # Schneller Schuss: hochfrequent, kurz
            s1 = self._synthesize_wave('sawtooth', 400, 45, vol * 0.35, harmonics=[(3, 0.2)])
            s2 = self._synthesize_noise(30, vol * 0.3, lowpass=3000, noise_type='white')
            s1.play()
            s2.play()

        elif var == 3:
            # Gedämpfter Schuss: weich, tief
            s1 = self._synthesize_wave('triangle', 150, 90, vol * 0.4, harmonics=[(1.5, 0.2)])
            s2 = self._synthesize_noise(60, vol * 0.3, lowpass=800, noise_type='pink')
            s1.play()
            s2.play()

        elif var == 4:
            # Scharfer Schuss: hochfrequenter Knall
            s1 = self._synthesize_wave('square_soft', 250, 60, vol * 0.45, harmonics=[(2, 0.25), (4, 0.1)])
            s2 = self._synthesize_noise(35, vol * 0.4, lowpass=2500, noise_type='white')
            s1.play()
            s2.play()

        elif var == 5:
            # Schwerer Schuss: viel Bass
            s1 = self._synthesize_wave('triangle', 100, 120, vol * 0.45, harmonics=[(2, 0.3)])
            s2 = self._synthesize_noise(70, vol * 0.35, lowpass=1200, noise_type='brown')
            s1.play()
            s2.play()

        elif var == 6:
            # Präzisionsschuss: klar, hoch
            s1 = self._synthesize_wave('sine', 500, 50, vol * 0.3, vibrato=5)
            s2 = self._synthesize_noise(40, vol * 0.35, lowpass=2000, noise_type='white')
            s1.play()
            s2.play()

        else:
            # Standard-Mix
            s1 = self._synthesize_wave('square_soft', 200, 70, vol * 0.4, harmonics=[(2.5, 0.15)])
            s2 = self._synthesize_noise(55, vol * 0.35, lowpass=1800, noise_type='white')
            s3 = self._synthesize_wave('triangle', 80, 80, vol * 0.25)
            s1.play()
            s2.play()
            s3.play()

        self._duck_music(0.08)

    def play_brick_destroy(self) -> None:
        """Zerstörung einer Ziegelwand - realistisches Zerbröckeln"""
        if not self._sound_available:
            return
        var = self._current_brick % self._brick_variations
        self._current_brick += 1
        vol = self._get_sfx_volume(0.3)

        if var == 0:
            # Staubiges Zerfallen
            s1 = self._synthesize_noise(150, vol * 0.4, lowpass=600, highpass=100, noise_type='pink')
            s2 = self._synthesize_wave('triangle', 120, 80, vol * 0.2)
            s1.play()
            s2.play()

        elif var == 1:
            # Knackiges Brechen
            s1 = self._synthesize_noise(80, vol * 0.5, lowpass=1500, noise_type='white')
            s2 = self._synthesize_wave('square_soft', 200, 60, vol * 0.25)
            s1.play()
            s2.play()

        elif var == 2:
            # Mehrfaches Zerbröckeln
            s1 = self._synthesize_noise(120, vol * 0.4, lowpass=800, noise_type='brown')
            s2 = self._synthesize_wave('triangle', 150, 100, vol * 0.2, harmonics=[(2, 0.2)])
            s1.play()
            s2.play()

        elif var == 3:
            # Hartes Aufprallen
            s1 = self._synthesize_wave('triangle', 250, 70, vol * 0.35, harmonics=[(3, 0.15)])
            s2 = self._synthesize_noise(90, vol * 0.35, lowpass=1000, noise_type='pink')
            s1.play()
            s2.play()

        elif var == 4:
            # Langsames Verfallen
            s1 = self._synthesize_noise(200, vol * 0.35, lowpass=500, highpass=80, noise_type='brown')
            s2 = self._synthesize_wave('sine', 100, 120, vol * 0.2)
            s1.play()
            s2.play()

        elif var == 5:
            # Kurz und knackig
            s1 = self._synthesize_noise(60, vol * 0.5, lowpass=2000, noise_type='white')
            s1.play()

        elif var == 6:
            # Staubwolke
            s1 = self._synthesize_noise(180, vol * 0.3, lowpass=400, noise_type='pink')
            s2 = self._synthesize_wave('triangle', 80, 90, vol * 0.2)
            s1.play()
            s2.play()

        else:
            # Mix aus allem
            s1 = self._synthesize_noise(130, vol * 0.4, lowpass=700, noise_type='pink')
            s2 = self._synthesize_wave('square_soft', 180, 70, vol * 0.2)
            s3 = self._synthesize_noise(50, vol * 0.25, lowpass=1500, noise_type='white')
            s1.play()
            s2.play()
            s3.play()

    def play_steel_destroy(self) -> None:
        """Zerstörung einer Stahlwand - metallisches Klirren"""
        if not self._sound_available:
            return
        var = self._current_steel % self._steel_variations
        self._current_steel += 1
        vol = self._get_sfx_volume(0.35)

        if var == 0:
            # Hohes metallisches Klingeln
            s1 = self._synthesize_wave('sine', 800, 200, vol * 0.3, vibrato=15)
            s2 = self._synthesize_wave('sine', 1200, 150, vol * 0.2, vibrato=20)
            s3 = self._synthesize_noise(100, vol * 0.25, lowpass=2000, noise_type='white')
            s1.play()
            s2.play()
            s3.play()

        elif var == 1:
            # Tiefes metallisches Surren
            s1 = self._synthesize_wave('triangle', 150, 180, vol * 0.35, harmonics=[(2, 0.3), (3, 0.15)])
            s2 = self._synthesize_noise(120, vol * 0.25, lowpass=800, noise_type='white')
            s1.play()
            s2.play()

        elif var == 2:
            # Kurzes metallisches Klicken
            s1 = self._synthesize_wave('square_soft', 600, 40, vol * 0.4)
            s2 = self._synthesize_noise(30, vol * 0.3, lowpass=3000, noise_type='white')
            s1.play()
            s2.play()

        elif var == 3:
            # Metallischer Einschlag
            s1 = self._synthesize_wave('triangle', 200, 120, vol * 0.35, harmonics=[(2.5, 0.2)])
            s2 = self._synthesize_noise(80, vol * 0.3, lowpass=1200, noise_type='white')
            s1.play()
            s2.play()

        elif var == 4:
            # Mehrere metallische Resonanzen
            s1 = self._synthesize_wave('sine', 500, 250, vol * 0.25, vibrato=10)
            s2 = self._synthesize_wave('sine', 750, 200, vol * 0.2, vibrato=12)
            s3 = self._synthesize_wave('sine', 1000, 180, vol * 0.15, vibrato=8)
            s1.play()
            s2.play()
            s3.play()

        elif var == 5:
            # Gedämpftes Metall
            s1 = self._synthesize_wave('triangle', 180, 150, vol * 0.3)
            s2 = self._synthesize_noise(100, vol * 0.25, lowpass=600, noise_type='pink')
            s1.play()
            s2.play()

        elif var == 6:
            # Scharfes Klirren
            s1 = self._synthesize_wave('square_soft', 400, 80, vol * 0.35, harmonics=[(3, 0.2)])
            s2 = self._synthesize_noise(60, vol * 0.3, lowpass=2500, noise_type='white')
            s1.play()
            s2.play()

        else:
            # Komplexer Metall-Sound
            s1 = self._synthesize_wave('triangle', 220, 160, vol * 0.3, harmonics=[(2, 0.25), (4, 0.1)])
            s2 = self._synthesize_noise(110, vol * 0.25, lowpass=1000, noise_type='white')
            s3 = self._synthesize_wave('sine', 660, 140, vol * 0.2, vibrato=10)
            s1.play()
            s2.play()
            s3.play()

    def play_tank_explosion(self) -> None:
        """Tiefe Panzer-Explosion mit mehreren Schichten"""
        if not self._sound_available:
            return
        var = self._current_tank % self._tank_variations
        self._current_tank += 1
        vol = self._get_sfx_volume(0.4)

        if var == 0:
            # Klassische Explosion: Bass-Druck + Rauschen
            s1 = self._synthesize_wave('triangle', 35, 350, vol * 0.5, harmonics=[(2, 0.2)])
            s2 = self._synthesize_noise(300, vol * 0.4, lowpass=150, highpass=30, noise_type='brown')
            s3 = self._synthesize_wave('sine', 60, 200, vol * 0.3)
            s1.play()
            s2.play()
            s3.play()

        elif var == 1:
            # Mehrfach-Explosion
            s1 = self._synthesize_noise(150, vol * 0.4, lowpass=200, noise_type='brown')
            s2 = self._synthesize_wave('triangle', 40, 250, vol * 0.35)
            s3 = self._synthesize_wave('sine', 55, 180, vol * 0.25)
            s1.play()
            s2.play()
            s3.play()

        elif var == 2:
            # Wuchtige Explosion
            s1 = self._synthesize_noise(400, vol * 0.35, lowpass=120, noise_type='brown')
            s2 = self._synthesize_wave('triangle', 30, 300, vol * 0.4, harmonics=[(3, 0.15)])
            s3 = self._synthesize_wave('sine', 45, 250, vol * 0.25)
            s1.play()
            s2.play()
            s3.play()

        elif var == 3:
            # Kurze, scharfe Explosion
            s1 = self._synthesize_noise(120, vol * 0.45, lowpass=300, noise_type='pink')
            s2 = self._synthesize_wave('triangle', 50, 150, vol * 0.35)
            s1.play()
            s2.play()

        elif var == 4:
            # Tiefe, bedrohliche Explosion
            s1 = self._synthesize_wave('triangle', 25, 400, vol * 0.45, harmonics=[(2, 0.25)])
            s2 = self._synthesize_noise(350, vol * 0.35, lowpass=100, noise_type='brown')
            s3 = self._synthesize_wave('sine', 40, 300, vol * 0.3)
            s1.play()
            s2.play()
            s3.play()

        elif var == 5:
            # Feuerwerk-Explosion
            s1 = self._synthesize_noise(200, vol * 0.4, lowpass=250, noise_type='white')
            s2 = self._synthesize_wave('triangle', 45, 200, vol * 0.3)
            s3 = self._synthesize_wave('sine', 70, 150, vol * 0.2)
            s1.play()
            s2.play()
            s3.play()

        elif var == 6:
            # Zerfetzende Explosion
            s1 = self._synthesize_noise(280, vol * 0.35, lowpass=180, noise_type='brown')
            s2 = self._synthesize_wave('triangle', 38, 280, vol * 0.35, harmonics=[(2.5, 0.2)])
            s1.play()
            s2.play()

        elif var == 7:
            # Knallhart
            s1 = self._synthesize_noise(100, vol * 0.5, lowpass=400, noise_type='white')
            s2 = self._synthesize_wave('triangle', 55, 180, vol * 0.3)
            s3 = self._synthesize_wave('sine', 80, 120, vol * 0.2)
            s1.play()
            s2.play()
            s3.play()

        elif var == 8:
            # Langsame, imposante Explosion
            s1 = self._synthesize_noise(450, vol * 0.3, lowpass=80, noise_type='brown')
            s2 = self._synthesize_wave('triangle', 28, 350, vol * 0.4, harmonics=[(2, 0.2)])
            s3 = self._synthesize_wave('sine', 35, 300, vol * 0.25)
            s1.play()
            s2.play()
            s3.play()

        else:
            # Standard-Explosion (Mix)
            s1 = self._synthesize_noise(300, vol * 0.35, lowpass=140, noise_type='brown')
            s2 = self._synthesize_wave('triangle', 38, 250, vol * 0.35, harmonics=[(2, 0.2)])
            s3 = self._synthesize_wave('sine', 50, 200, vol * 0.25)
            s1.play()
            s2.play()
            s3.play()

        self._duck_music(0.06)

    def play_ambient(self) -> None:
        """Atmosphärische Hintergrundgeräusche (Wind, distante Explosionen)"""
        if not self._sound_available:
            return
        vol = Config.AMBIENT_VOLUME
        wind = self._synthesize_noise(2000, vol * 0.5, lowpass=200, noise_type='brown', highpass=30)
        wind.play()
        if random.random() < 0.3:
            distant = self._synthesize_noise(500, vol * 0.3, lowpass=80, noise_type='brown')
            distant.play()

    def play_impact_heavy(self) -> None:
        """Schwerer Einschlag (Player-Treffer)"""
        if not self._sound_available:
            return
        vol = self._get_sfx_volume(0.3)
        s1 = self._synthesize_wave('triangle', 80, 100, vol * 0.4, harmonics=[(2, 0.3)])
        s2 = self._synthesize_noise(80, vol * 0.35, lowpass=800, noise_type='white')
        s3 = self._synthesize_wave('square_soft', 150, 60, vol * 0.2)
        s1.play()
        s2.play()
        s3.play()

    def play_impact_light(self) -> None:
        """Leichter Einschlag (Bullet auf Panzer)"""
        if not self._sound_available:
            return
        vol = self._get_sfx_volume(0.2)
        s1 = self._synthesize_wave('triangle', 200, 40, vol * 0.3, harmonics=[(3, 0.2)])
        s2 = self._synthesize_noise(30, vol * 0.25, lowpass=1500, noise_type='white')
        s1.play()
        s2.play()

    def play_bullet_hit(self) -> None:
        """Kleiner Einschlag-Sound"""
        if not self._sound_available:
            return
        vol = self._get_sfx_volume(0.15)
        s1 = self._synthesize_wave('triangle', 300, 30, vol * 0.3, harmonics=[(2, 0.2)])
        s2 = self._synthesize_noise(25, vol * 0.25, lowpass=2000, noise_type='white')
        s1.play()
        s2.play()

    def play_powerup(self) -> None:
        """Freudige Powerup-Melodie mit mehreren Stimmen"""
        if not self._sound_available:
            return
        vol = self._get_sfx_volume(0.2)

        # Aufsteigende Arpeggio-Melodie (non-blocking: alle Sounds sofort abspielen)
        notes = [523, 659, 784, 1046, 1318]
        for freq in notes:
            s = self._synthesize_wave('sine', freq, 150, vol * 0.4, harmonics=[(2, 0.15)], tremolo=0.1)
            s.play()
        # Nachklingen
        s = self._synthesize_wave('sine', 1318, 300, vol * 0.3, fade_out=0.2)
        s.play()

    def play_music(self) -> None:
        """Atmosphärische Hintergrundmusik mit mehreren Schichten"""
        if not self._sound_available or self._music_playing:
            return
        self._music_playing = True

        # Verbesserte Melodie mit mehr Harmonik
        # C-Dur Pentatonik mit Variationen
        melody_patterns = [
            # Pattern 1: Aufsteigend
            [523, 587, 659, 0, 784, 659, 587, 523],
            # Pattern 2: Absteigend
            [523, 440, 392, 0, 440, 523, 587, 523],
            # Pattern 3: Sprung hoch
            [392, 523, 659, 784, 659, 523, 440, 392],
            # Pattern 4: Auflösung
            [523, 659, 784, 1046, 784, 659, 523, 392],
        ]

        bass_patterns = [
            [262, 0, 262, 0, 330, 0, 262, 0],
            [262, 0, 330, 0, 392, 0, 330, 0],
            [392, 0, 392, 0, 330, 0, 262, 0],
            [262, 0, 330, 0, 392, 0, 523, 0],
        ]

        arp_patterns = [
            [262, 330, 392, 523, 392, 330, 262, 0],
            [262, 392, 523, 392, 330, 262, 330, 0],
            [392, 523, 659, 523, 392, 330, 262, 0],
            [262, 330, 392, 523, 659, 523, 392, 262],
        ]

        note_len = 120  # ms pro Note

        def play_note(freq, duration, volume, wave='triangle', harmonics=None) -> None:
            if freq <= 0:
                return
            try:
                s = self._synthesize_wave(wave, freq, duration, volume,
                                         harmonics=harmonics or [(2, 0.1)])
                s.play()
            except Exception:
                pass

        def music_loop() -> None:
            try:
                pattern_idx = 0
                while self._music_playing:
                    pattern = melody_patterns[pattern_idx % len(melody_patterns)]
                    bass = bass_patterns[pattern_idx % len(bass_patterns)]
                    arp = arp_patterns[pattern_idx % len(arp_patterns)]

                    for i in range(0, len(pattern), 2):
                        if not self._music_playing:
                            break

                        # Melodie (warm, triangle mit Overtones)
                        for j in range(2):
                            idx = i + j
                            if idx < len(pattern):
                                play_note(pattern[idx], note_len,
                                         self._music_volume * 0.1, 'triangle',
                                         [(2, 0.15), (3, 0.05)])

                        # Bass (tief, sine)
                        for j in range(2):
                            idx = i + j
                            if idx < len(bass):
                                play_note(bass[idx], note_len * 2,
                                         self._music_volume * 0.12, 'sine')

                        # Arpeggio (hell, sine mit Vibrato)
                        for j in range(2):
                            idx = i + j
                            if idx < len(arp):
                                play_note(arp[idx], note_len // 2,
                                         self._music_volume * 0.05, 'sine',
                                         [(2, 0.1)])

                        pass  # non-blocking: Sounds sofort abspielen

                    pattern_idx += 1
            except Exception:
                pass

        self._music_thread = threading.Thread(target=music_loop, daemon=True)
        self._music_thread.start()

    def stop_music(self) -> None:
        """Stoppt die Hintergrundmusik sanft"""
        self._music_playing = False
        if self._music_thread and self._music_thread.is_alive():
            self._music_thread.join(timeout=1)

    def play_win(self) -> None:
        """Triumph-Melodie - aufsteigend und feierlich"""
        if not self._sound_available:
            return
        vol = self._get_sfx_volume(0.25)
        # C-Dur Akkord-Arpeggio aufsteigend (non-blocking)
        notes = [(523, 120), (659, 120), (784, 120), (1046, 200), (1318, 200), (1568, 300), (2093, 500)]
        for freq, dur in notes:
            s = self._synthesize_wave('sine', freq, dur, vol * 0.4,
                                     harmonics=[(2, 0.2)], tremolo=0.05)
            s.play()
        # Abschluss-Akkord
        for freq in [523, 659, 784, 1046]:
            s = self._synthesize_wave('sine', freq, 600, vol * 0.2, fade_out=0.4)
            s.play()

    def play_lose(self) -> None:
        """Traurige Melodie - absteigend und langsam (non-blocking)"""
        if not self._sound_available:
            return
        vol = self._get_sfx_volume(0.18)
        notes = [(392, 300), (349, 300), (330, 350), (294, 400), (262, 450), (220, 500), (196, 700)]
        for freq, dur in notes:
            s = self._synthesize_wave('triangle', freq, dur, vol * 0.35,
                                     harmonics=[(2, 0.1)], tremolo=0.08)
            s.play()

    def play_enemy_spawn(self) -> None:
        """Feindliches Aufploppen-Signal (non-blocking)"""
        if not self._sound_available:
            return
        vol = self._get_sfx_volume(0.15)
        s1 = self._synthesize_wave('square_soft', 150, 100, vol * 0.3)
        s2 = self._synthesize_wave('square_soft', 120, 120, vol * 0.25)
        s1.play()
        s2.play()

    def play_eagle_alert(self) -> None:
        """Eagle-Unterwegs-Warnung (non-blocking)"""
        if not self._sound_available:
            return
        vol = self._get_sfx_volume(0.2)
        for _ in range(3):
            s = self._synthesize_wave('square_soft', 440, 80, vol * 0.3)
            s.play()

    def _duck_music(self, volume: float) -> None:
        """Duckt die Musik bei Sound-Effekten"""
        if self._duck_timer == 0:
            self._music_volume = volume
            self._duck_timer = int(0.4 * 60)

    def _update_music_ducking(self) -> None:
        """Reduziert Ducking über die Zeit"""
        if self._duck_timer > 0:
            self._duck_timer -= 1
            if self._duck_timer <= 0:
                self._music_volume = Config.MUSIC_VOLUME
# ============================================================================
# PLAYER CLASS
# ============================================================================
class Player:
    def __init__(self, player_id, x, y, color, controls, team_id=None, display_name=None) -> None:
        self.player_id = player_id
        self.rect = pygame.Rect(x, y, Config.GRID_SIZE - 10, Config.GRID_SIZE - 10)
        self.color = color
        self.controls = controls
        self.team_id = team_id or f"player{player_id}"
        self.display_name = display_name or f"Player {player_id}"
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
            dy -= 1
        if keys[self.controls['down']]:
            dy += 1
        if keys[self.controls['left']]:
            dx -= 1
        if keys[self.controls['right']]:
            dx += 1

        self.direction = pygame.Vector2(dx, dy)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
            self.last_direction = pygame.Vector2(self.direction.x, self.direction.y)
            angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
            self.rotation_angle = angle

        return self.direction * Config.PLAYER_SPEED

    def shoot(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            return None

        direction = self.direction if self.direction.length() > 0 else self.last_direction
        owner = f"player{self.player_id}"

        # Double Shot: zwei leicht gespreizte Schüsse mit eigenem Cooldown.
        # Vorher konnte Double Shot jeden Frame zwei identische Kugeln erzeugen.
        if self.double_shot_active:
            self.shoot_cooldown = 14
            bullets = []
            for angle in (-8, 8):
                shot_dir = direction.rotate(angle)
                if shot_dir.length() > 0:
                    shot_dir.normalize_ip()
                bullets.append(Bullet(self.rect.centerx, self.rect.centery, shot_dir, self.color, owner, team_id=self.team_id, source=self))
            return bullets

        self.shoot_cooldown = 30
        return Bullet(self.rect.centerx, self.rect.centery, direction, self.color, owner, team_id=self.team_id, source=self)

    def draw_tank(self, surface) -> None:
        """Zeichnet detaillierten Panzer mit Glow, animierten Ketten und 3D-Effekten"""
        cx, cy = self.rect.centerx, self.rect.centery
        size = self.rect.width
        half = size // 2
        tick = pygame.time.get_ticks() / 1000

        # AMBIENT GLOW unter dem Panzer
        glow_surf = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
        pulse = int(30 + 20 * math.sin(tick * 3))
        glow_rgba = (*self.color[:3], pulse)
        pygame.draw.circle(glow_surf, glow_rgba, (size * 1.5, size * 1.5), size * 1.5)
        surface.blit(glow_surf, (cx - size * 1.5, cy - size * 1.5))

        # Schatten unter dem Panzer
        pygame.draw.ellipse(surface, (0, 0, 0, 120),
                          (cx - half - 3, cy + half - 4, size + 6, 12))

        # Ketten mit Animation und 3D-Effekt
        chain_color = (70, 70, 70)
        chain_dark = (50, 50, 50)
        chain_width = 5
        # Chain shadows
        pygame.draw.rect(surface, (40, 40, 40),
                        (cx - half - chain_width - 1, cy - half + 1, chain_width, size + 2))
        pygame.draw.rect(surface, (40, 40, 40),
                        (cx + half + 1, cy - half + 1, chain_width, size + 2))
        # Main chains
        pygame.draw.rect(surface, chain_color,
                        (cx - half - chain_width, cy - half, chain_width, size))
        pygame.draw.rect(surface, chain_color,
                        (cx + half, cy - half, chain_width, size))
        # Chain highlights
        pygame.draw.rect(surface, (100, 100, 100),
                        (cx - half - chain_width, cy - half, 1, size))
        pygame.draw.rect(surface, (100, 100, 100),
                        (cx + half, cy - half, 1, size))
        # Animierte Tread-Markierungen
        tread_offset = int(tick * 20) % 8
        for i in range(-half + tread_offset, half, 8):
            pygame.draw.line(surface, chain_dark,
                           (cx - half - chain_width, cy + i),
                           (cx - half, cy + i), 1)
            pygame.draw.line(surface, chain_dark,
                           (cx + half, cy + i),
                           (cx + half + chain_width, cy + i), 1)

        # Hauptkörper mit 3D-Effekt
        pygame.draw.rect(surface, (40, 40, 40),
                        (cx - half + 2, cy - half + 6, size, size - 6))
        pygame.draw.rect(surface, self.color,
                        (cx - half, cy - half + 4, size, size - 8))
        # Körper-Highlight (oben)
        pygame.draw.line(surface, (255, 255, 255, 80),
                        (cx - half + 2, cy - half + 5),
                        (cx + half - 2, cy - half + 5), 1)
        # Kontur
        pygame.draw.rect(surface, (60, 60, 60),
                        (cx - half, cy - half + 4, size, size - 8), 1)
        # Panzerplatten-Linie
        pygame.draw.line(surface, (80, 80, 80),
                        (cx - half + 4, cy),
                        (cx + half - 4, cy), 1)

        # Turm mit Schatten und Highlight
        turret_radius = half - 3
        pygame.draw.circle(surface, (40, 40, 40), (cx + 2, cy + 2), turret_radius)
        pygame.draw.circle(surface, (*self.color[:3], 220), (cx, cy), turret_radius)
        pygame.draw.circle(surface, (255, 255, 255, 40), (cx - 1, cy - 1), turret_radius - 2)
        pygame.draw.circle(surface, (70, 70, 70), (cx, cy), turret_radius, 1)
        # Turm-Mittelteil
        pygame.draw.circle(surface, (*self.color[:3], 180), (cx, cy), 5)
        pygame.draw.circle(surface, (255, 255, 255, 50), (cx, cy), 3)

        # Kanone mit Schatten, Highlight und Mündung
        cannon_length = 22
        cannon_width = 7
        cannon_end_x = cx + math.cos(math.radians(self.rotation_angle)) * cannon_length
        cannon_end_y = cy + math.sin(math.radians(self.rotation_angle)) * cannon_length
        cannon_start_x = cx + math.cos(math.radians(self.rotation_angle)) * 5
        cannon_start_y = cy + math.sin(math.radians(self.rotation_angle)) * 5
        # Kanonen-Schatten
        pygame.draw.line(surface, (50, 50, 50),
                        (cannon_start_x + 1, cannon_start_y + 2),
                        (cannon_end_x + 1, cannon_end_y + 2), cannon_width + 1)
        # Kanone
        pygame.draw.line(surface, (90, 90, 90),
                        (cannon_start_x, cannon_start_y),
                        (cannon_end_x, cannon_end_y), cannon_width)
        # Kanonen-Highlight
        highlight_end_x = cx + math.cos(math.radians(self.rotation_angle)) * (cannon_length - 2)
        highlight_end_y = cy + math.sin(math.radians(self.rotation_angle)) * (cannon_length - 2)
        highlight_start_x = cx + math.cos(math.radians(self.rotation_angle)) * 6
        highlight_start_y = cy + math.sin(math.radians(self.rotation_angle)) * 6
        pygame.draw.line(surface, (140, 140, 140),
                        (highlight_start_x, highlight_start_y),
                        (highlight_end_x, highlight_end_y), 2)
        # Mündung
        pygame.draw.circle(surface, (60, 60, 60),
                          (int(cannon_end_x), int(cannon_end_y)), 4)
        pygame.draw.circle(surface, (40, 40, 40),
                          (int(cannon_end_x), int(cannon_end_y)), 2)

    def take_damage(self, amount=1) -> bool:
        """Nimmt Schaden, wenn unverwundbar oder Shield aktiv, ignoriert Schaden"""
        if self.invulnerable:
            return False

        # Shield: 1-2 Treffer absorbieren
        if self.shield_charges > 0:
            self.shield_charges -= 1
            return False

        self.health -= amount
        return True

    def update(self, walls) -> None:
        """Update Player"""
        # Respawn Timer / kurze Spawn-Unverwundbarkeit
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            self.invulnerable = True
        elif self.invulnerable:
            self.invulnerable = False

        # Double Shot Timer
        if self.double_shot_timer > 0:
            self.double_shot_timer -= 1
            if self.double_shot_timer == 0:
                self.double_shot_active = False

    def move(self, dx, dy, walls, shake) -> None:
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

    def draw_health_bar(self, surface) -> None:
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

    def draw(self, surface) -> None:
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
    def __init__(self, enemy) -> None:
        self.enemy = enemy
        self.state = EnemyState.PATROL
        self.target = None
        self.patrol_points: list[tuple[int, int]] = []
        self.current_patrol_index = 0
        self.state_change_cooldown = 0  # Verhindert zu häufige State-Wechsel
        self.stuck_timer = 0  # Erkennt wenn Enemy steckenbleibt
        self.last_pos = (0, 0)

    def update(self, players, walls, eagle_pos):
        """Aktualisiert die KI basierend auf Zustand und gibt ggf. eine Kugel zurück."""
        self.state_change_cooldown = max(0, self.state_change_cooldown - 1)
        self._update_state(players, eagle_pos)
        return self._execute_state(players, walls)

    def _update_state(self, players, eagle_pos) -> None:
        """Bestimmt den aktuellen Zustand mit Hysterese (keine flackernden Wechsel)"""
        if not players:
            if self.state != EnemyState.PATROL:
                self.state = EnemyState.PATROL
                self.patrol_points = []
            return

        # Priorität 1: Flucht wenn Eagle zerstört
        if self.enemy.game is not None and self.enemy.game.eagle and self.enemy.game.eagle.state == EagleState.HIT:
            if self.state != EnemyState.RETREAT:
                self.state = EnemyState.RETREAT
                self.target = None
            return

        # Finde nächsten Spieler für Distanz-Berechnung
        closest_player = None
        closest_distance = float('inf')
        for player in players:
            distance = math.hypot(self.enemy.rect.centerx - player.rect.centerx,
                                self.enemy.rect.centery - player.rect.centery)
            if distance < closest_distance:
                closest_distance = distance
                closest_player = player

        # State-Übergänge mit Hysterese (mindestens 10 Frames warten)
        if self.state_change_cooldown == 0:
            if closest_player:
                if closest_distance < self.enemy.attack_range:
                    if self.state != EnemyState.ATTACK:
                        self.state = EnemyState.ATTACK
                        self.target = closest_player
                        self.state_change_cooldown = self.enemy.reaction_frames
                elif closest_distance < self.enemy.chase_range:
                    if self.state != EnemyState.CHASE:
                        self.state = EnemyState.CHASE
                        self.target = closest_player
                        self.state_change_cooldown = self.enemy.reaction_frames
                elif self.state in (EnemyState.CHASE, EnemyState.ATTACK):
                    self.state = EnemyState.PATROL
                    self.target = None
                    self.state_change_cooldown = 15
            else:
                if self.state != EnemyState.PATROL:
                    self.state = EnemyState.PATROL
                    self.target = None
                    self.state_change_cooldown = 15

    def _execute_state(self, players, walls):
        """Führt den aktuellen Zustand aus und gibt ggf. eine Kugel zurück."""
        if self.state == EnemyState.PATROL:
            self._patrol(walls)
        elif self.state == EnemyState.CHASE:
            self._chase(players, walls)
        elif self.state == EnemyState.ATTACK:
            return self._attack(players, walls)
        elif self.state == EnemyState.RETREAT:
            self._retreat(walls)
        return None

    def _patrol(self, walls) -> None:
        """Patrouille mit mehreren Wegpunkten in einer Route"""
        # Generiere neue Patrol-Route wenn nötig
        if not self.patrol_points or self.current_patrol_index >= len(self.patrol_points):
            center_x, center_y = self.enemy.rect.centerx, self.enemy.rect.centery
            # Generiere 3-5 Wegpunkte in der Nähe
            num_points = random.randint(3, 5)
            self.patrol_points = []
            for _ in range(num_points):
                angle = random.uniform(0, 2 * math.pi)
                radius = random.randint(80, 200)
                tx = center_x + int(math.cos(angle) * radius)
                ty = center_y + int(math.sin(angle) * radius)
                # Begrenze auf Spielfeld
                tx = max(Config.GRID_SIZE, min(Config.WIDTH - Config.GRID_SIZE, tx))
                ty = max(Config.GRID_SIZE, min(Config.HEIGHT - Config.GRID_SIZE, ty))
                self.patrol_points.append((tx, ty))
            self.current_patrol_index = 0

        target = self.patrol_points[self.current_patrol_index]
        self.enemy.move_toward(target, walls)

        distance = math.hypot(self.enemy.rect.centerx - target[0],
                            self.enemy.rect.centery - target[1])
        if distance < 30:
            self.current_patrol_index += 1
            if self.current_patrol_index >= len(self.patrol_points):
                # Route zurücksetzen für nächste Runde
                self.patrol_points = []

    def _chase(self, players, walls) -> None:
        """Intelligente Jagd-Logik mit Wand-Vermeidung"""
        if not self.target or self.target not in players:
            self.state = EnemyState.PATROL
            self.patrol_points = []
            return

        target_pos = self.target.rect.center
        old_pos = (self.enemy.rect.centerx, self.enemy.rect.centery)

        # Berechne Zielrichtung
        dx = target_pos[0] - old_pos[0]
        dy = target_pos[1] - old_pos[1]
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        # Versuche beide Achsen separat (besser als move_toward)
        move_speed = self.enemy.speed * self.enemy.chase_speed_multiplier
        self.enemy.move(dx * move_speed, 0, walls, 0)
        self.enemy.move(0, dy * move_speed, walls, 0)

        # Update rotation_angle für Kanone
        self.enemy.rotation_angle = math.degrees(math.atan2(dy, dx))

        # Steckenbleiben-Erkennung
        new_pos = (self.enemy.rect.centerx, self.enemy.rect.centery)
        if old_pos == new_pos:
            self.stuck_timer += 1
            if self.stuck_timer > 20:  # ~0.3 Sekunden stecken
                # Ausweich-Manöver: seitlich bewegen
                side_angle = math.atan2(dy, dx) + random.choice([math.pi / 2, -math.pi / 2])
                self.enemy.move(
                    math.cos(side_angle) * self.enemy.speed,
                    math.sin(side_angle) * self.enemy.speed,
                    walls, 0
                )
                self.stuck_timer = 0
        else:
            self.stuck_timer = 0

    def _attack(self, players, walls):
        """Dynamische Angriffs-Logik: Distanz halten, flankieren und kontrolliert schießen."""
        if not self.target or self.target not in players:
            self.state = EnemyState.PATROL
            self.target = None
            return None

        target_pos = self.target.rect.center
        enemy_pos = self.enemy.rect.center
        distance = math.hypot(enemy_pos[0] - target_pos[0], enemy_pos[1] - target_pos[1])

        aim = pygame.Vector2(target_pos[0] - enemy_pos[0], target_pos[1] - enemy_pos[1])
        if aim.length() > 0:
            aim.normalize_ip()
            self.enemy.rotation_angle = math.degrees(math.atan2(aim.y, aim.x))

        if distance > self.enemy.attack_range + 150:
            self.state = EnemyState.CHASE
            return None

        if distance < self.enemy.keep_distance:
            # Zu nah - zurückweichen, damit Gegner nicht ineinander kleben.
            diff = pygame.Vector2(enemy_pos[0] - target_pos[0], enemy_pos[1] - target_pos[1])
            if diff.length() == 0:
                diff = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if diff.length() > 0:
                diff.normalize_ip()
                self.enemy.move(diff.x * self.enemy.speed, diff.y * self.enemy.speed, walls, 0)
        else:
            # Distanz halten und nicht jedes Frame die Seite wechseln.
            if self.enemy.change_direction_timer <= 0:
                self.enemy.flank_side = random.choice([-1, 1])
                self.enemy.change_direction_timer = random.randint(30, 80)
            self.enemy.change_direction_timer -= 1

            flank_dir = pygame.Vector2(target_pos[0] - enemy_pos[0], target_pos[1] - enemy_pos[1]).rotate(90 * getattr(self.enemy, "flank_side", 1))
            if flank_dir.length() > 0:
                flank_dir.normalize_ip()
                self.enemy.move(flank_dir.x * self.enemy.speed * 0.55, flank_dir.y * self.enemy.speed * 0.55, walls, 0)

        # Schießen mit Cooldown, Sichtlinie und kleiner Ungenauigkeit statt Laser-Tracking.
        self.enemy.shoot_timer += 1
        can_shoot = self.enemy.shoot_timer >= self.enemy.shoot_cooldown
        if can_shoot and self._has_line_of_sight(enemy_pos, target_pos, walls):
            self.enemy.shoot_timer = 0
            return self.enemy.shoot_at(target_pos, accuracy=self.enemy.ai_accuracy)
        return None

    def _has_line_of_sight(self, start, end, walls) -> bool:
        """Grobe Sichtlinienprüfung, damit KI nicht stumpf durch Wände zielt."""
        sx, sy = start
        ex, ey = end
        distance = max(1, math.hypot(ex - sx, ey - sy))
        steps = max(4, int(distance // (Config.GRID_SIZE // 2)))
        blocking_walls = [w for w in walls if w.wall_type == WallType.STEEL]
        for i in range(1, steps):
            t = i / steps
            px = sx + (ex - sx) * t
            py = sy + (ey - sy) * t
            for wall in blocking_walls:
                if wall.rect.collidepoint(px, py):
                    return False
        return True

    def _retreat(self, walls) -> None:
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
    def __init__(self, x, y, enemy_type=EnemyType.GUNNER, ai_difficulty=Difficulty.MEDIUM, team_id="rust") -> None:
        self.rect = pygame.Rect(x, y, Config.GRID_SIZE - 10, Config.GRID_SIZE - 10)
        self.color = Config.COLOR_ENEMY
        self.enemy_type = enemy_type
        self.ai_difficulty = ai_difficulty
        self.team_id = team_id
        self.direction = pygame.Vector2(0, 0)
        self.last_direction = pygame.Vector2(random.choice([-1, 1]), 0)
        self.shoot_cooldown = 0
        self.change_direction_timer = 0
        self.flank_side = random.choice([-1, 1])
        self.shoot_timer = random.randint(0, 40)
        self.respawn_timer = 0
        self.rotation_angle = 0
        self.game: GameManager | None = None  # Reference to game manager
        self.speed: float = 0.0

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

        self.max_health = self.health
        self.ai_accuracy = Config.AI_SHOOT_ACCURACY
        self.chase_range = 350
        self.attack_range = 120
        self.keep_distance = 115
        self.reaction_frames = Config.AI_REACTION_FRAMES
        self.chase_speed_multiplier = 0.6
        self._apply_ai_difficulty(ai_difficulty)
        self.ai = EnemyAI(self)  # KI-Controller

    def _apply_ai_difficulty(self, difficulty) -> None:
        """Skaliert Verhalten pro Panzer, damit Leicht/Mittel/Schwer/Mixed echte KI-Varianten sind."""
        if difficulty == Difficulty.EASY:
            self.speed *= 0.78
            self.shoot_cooldown = int(self.shoot_cooldown * 1.55)
            self.ai_accuracy = 0.58
            self.chase_range = 270
            self.attack_range = 105
            self.keep_distance = 95
            self.reaction_frames = 24
        elif difficulty == Difficulty.HARD:
            self.speed *= 1.18
            self.shoot_cooldown = max(25, int(self.shoot_cooldown * 0.65))
            self.health += 1
            self.max_health = self.health
            self.ai_accuracy = 0.94
            self.chase_range = 470
            self.attack_range = 175
            self.keep_distance = 135
            self.reaction_frames = 8
            self.chase_speed_multiplier = 0.82
        else:  # Mittel
            self.ai_accuracy = Config.AI_SHOOT_ACCURACY
            self.chase_range = 350
            self.attack_range = 125
            self.keep_distance = 115
            self.reaction_frames = Config.AI_REACTION_FRAMES

    def move_toward(self, target_pos, walls) -> None:
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

    def shoot_at(self, target_pos, accuracy=1.0):
        """Schießt in Richtung eines Ziels; accuracy < 1 erzeugt leichte Streuung."""
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        direction = pygame.Vector2(dx, dy)
        if direction.length() == 0:
            direction = pygame.Vector2(self.last_direction)
        if accuracy < 1.0:
            miss_angle = random.uniform(-1, 1) * (1.0 - accuracy) * 35
            direction = direction.rotate(miss_angle)
        if direction.length() > 0:
            direction.normalize_ip()
            self.last_direction = pygame.Vector2(direction)
            self.rotation_angle = math.degrees(math.atan2(direction.y, direction.x))

        return Bullet(self.rect.centerx, self.rect.centery, direction, self.color, "enemy", team_id=self.team_id, source=self)

    def move(self, dx, dy, walls, shake) -> None:
        """Bewegt Enemy mit Kollisionserkennung (axis-separated)"""
        # X-Bewegung
        self.rect.x += dx + shake
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                elif dx < 0:
                    self.rect.left = wall.rect.right

        # Bildschirmgrenzen X
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Config.WIDTH:
            self.rect.right = Config.WIDTH

        # Y-Bewegung
        self.rect.y += dy + shake
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                elif dy < 0:
                    self.rect.top = wall.rect.bottom

        # Bildschirmgrenzen Y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Config.HEIGHT:
            self.rect.bottom = Config.HEIGHT

    def take_damage(self) -> bool:
        """Enemy.take_damage() Methode - reduziert Health und gibt True wenn getötet"""
        self.health -= 1
        if self.health <= 0:
            return True  # Enemy ist getötet
        return False  # Enemy lebt noch

    def update_ai(self, players, walls, eagle_pos):
        """Verbesserte KI mit State-Machine - Schießen wird von AI gesteuert.

        In FFA sucht jeder KI-Panzer gegnerische Teams (Spieler oder KI). In Horde/Missionen
        kämpft die Rust-KI gegen Spieler und notfalls gegen die Basis.
        """
        targets = players
        if self.game is not None and self.game.game_mode == GameMode.FFA:
            targets = self.game._ffa_targets_for(self)

        ai_bullet = self.ai.update(targets, walls, eagle_pos)
        if ai_bullet:
            return ai_bullet

        # Schießen nur wenn AI nicht im ATTACK-Modus (da ATTACK schon schießt)
        if self.ai.state != EnemyState.ATTACK:
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_cooldown:
                self.shoot_timer = 0
                if targets:
                    target = min(
                        targets,
                        key=lambda t: math.hypot(self.rect.centerx - t.rect.centerx,
                                                 self.rect.centery - t.rect.centery),
                    )
                    return self.shoot_at(target.rect.center, accuracy=self.ai_accuracy)
                return self.shoot_at(eagle_pos, accuracy=self.ai_accuracy)  # Standardmäßig auf Eagle schießen
        return None

    def respawn(self, x, y) -> None:
        """Enemy respawnet an neuer Position"""
        self.rect.x = x
        self.rect.y = y
        self.health = self.get_max_health()
        self.shoot_cooldown = 0

    def get_max_health(self):
        """Gibt maximale Health basierend auf Typ und KI-Schwierigkeit zurück."""
        return self.max_health

    def draw(self, surface) -> None:
        """Zeichnet detaillierten Enemy-Panzer mit Bedrohlichkeit und Glow"""
        cx, cy = self.rect.centerx, self.rect.centery
        size = self.rect.width
        half = size // 2
        tick = pygame.time.get_ticks() / 1000

        # Bedrohlicher roter Glow
        glow_surf = pygame.Surface((size * 2.5, size * 2.5), pygame.SRCALPHA)
        pulse = int(25 + 15 * math.sin(tick * 4))
        glow_rgba = (255, 50, 50, pulse)
        pygame.draw.circle(glow_surf, glow_rgba, (size * 1.25, size * 1.25), size * 1.25)
        surface.blit(glow_surf, (cx - size * 1.25, cy - size * 1.25))

        # Schatten
        pygame.draw.ellipse(surface, (0, 0, 0, 100),
                          (cx - half - 2, cy + half - 4, size + 4, 10))

        # Ketten mit 3D-Effekt
        chain_color = (60, 60, 60)
        chain_width = 4
        pygame.draw.rect(surface, (40, 40, 40),
                        (cx - half - chain_width - 1, cy - half + 1, chain_width, size + 2))
        pygame.draw.rect(surface, chain_color,
                        (cx - half - chain_width, cy - half, chain_width, size))
        pygame.draw.rect(surface, chain_color,
                        (cx + half, cy - half, chain_width, size))
        pygame.draw.rect(surface, (90, 90, 90),
                        (cx - half - chain_width, cy - half, 1, size))
        pygame.draw.rect(surface, (90, 90, 90),
                        (cx + half, cy - half, 1, size))

        # Hauptkörper mit Schatten und Highlight
        pygame.draw.rect(surface, (35, 35, 35),
                        (cx - half + 1, cy - half + 5, size, size - 5))
        pygame.draw.rect(surface, self.color,
                        (cx - half, cy - half + 4, size, size - 8))
        pygame.draw.line(surface, (255, 100, 100, 60),
                        (cx - half + 2, cy - half + 5),
                        (cx + half - 2, cy - half + 5), 1)
        pygame.draw.rect(surface, (70, 30, 30),
                        (cx - half, cy - half + 4, size, size - 8), 1)

        # Turm mit Schatten und Highlight
        turret_radius = half - 3
        pygame.draw.circle(surface, (40, 20, 20), (cx + 2, cy + 2), turret_radius)
        pygame.draw.circle(surface, (*self.color[:3], 200), (cx, cy), turret_radius)
        pygame.draw.circle(surface, (255, 100, 100, 30), (cx - 1, cy - 1), turret_radius - 2)
        pygame.draw.circle(surface, (70, 30, 30), (cx, cy), turret_radius, 1)
        pygame.draw.circle(surface, (200, 50, 50, 150), (cx, cy), 5)

        # Kanone mit Schatten und Highlight
        cannon_length = 20
        cannon_width = 6
        cannon_end_x = cx + math.cos(math.radians(self.rotation_angle)) * cannon_length
        cannon_end_y = cy + math.sin(math.radians(self.rotation_angle)) * cannon_length
        pygame.draw.line(surface, (50, 20, 20),
                        (cx + 1, cy + 2),
                        (cannon_end_x + 1, cannon_end_y + 2), cannon_width)
        pygame.draw.line(surface, (100, 50, 50),
                        (cx, cy),
                        (cannon_end_x, cannon_end_y), cannon_width)
        highlight_len = int(cannon_length * 0.6)
        hx = cx + math.cos(math.radians(self.rotation_angle)) * highlight_len
        hy = cy + math.sin(math.radians(self.rotation_angle)) * highlight_len
        pygame.draw.line(surface, (180, 80, 80),
                        (cx, cy), (hx, hy), 2)
        pygame.draw.circle(surface, (60, 25, 25),
                          (int(cannon_end_x), int(cannon_end_y)), 3)

    def draw_health_bar(self, surface) -> None:
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
    def __init__(self) -> None:
        self.current_wave = 0
        self.total_waves = Config.TOTAL_WAVES
        self.spawn_timer = 0
        self.enemies_to_spawn = 0
        self.wave_complete = False
        self.level = 1
        self.is_boss_wave = False

    def _is_spawn_valid(self, x, y, players, enemies, walls, eagle) -> bool:
        """Prüft ob Spawn-Position fair ist"""
        test_rect = pygame.Rect(x, y, Config.GRID_SIZE - 10, Config.GRID_SIZE - 10)
        if any(test_rect.colliderect(wall.rect) for wall in walls):
            return False

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

        return True

    def _select_enemy_type(self) -> str:
        """Wählt Enemy-Typ basierend auf Spawn-Chancen und aktueller Welle"""
        # Skalierung mit Wellennummer: spätere Wellen haben mehr BRUTEs
        wave_bonus = min(self.current_wave * 0.03, 0.3)  # Bis +30% BRUTE-Chance

        brute_chance = min(0.55, Config.BRUTE_SPAWN_CHANCE + wave_bonus)
        scout_chance = max(0.12, Config.SCOUT_SPAWN_CHANCE - wave_bonus * 0.5)
        gunner_chance = max(0.0, 1.0 - scout_chance - brute_chance)

        roll = random.random()
        if roll < scout_chance:
            return EnemyType.SCOUT
        if roll < scout_chance + gunner_chance:
            return EnemyType.GUNNER
        return EnemyType.BRUTE

    def spawn_enemy(self, enemies_list, players, walls, eagle, game=None):
        """Spawnet einen neuen Enemy mit fairem Spawn-Schutz, Typ und Modus-Schwierigkeit."""
        if self.enemies_to_spawn > 0:
            # Mehrere Versuche für faire Position
            max_attempts = 50
            for _ in range(max_attempts):
                x = random.randint(Config.GRID_SIZE, Config.WIDTH - Config.GRID_SIZE)
                y = random.randint(Config.GRID_SIZE, Config.HEIGHT - Config.GRID_SIZE)

                if self._is_spawn_valid(x, y, players, enemies_list, walls, eagle):
                    enemy_type = self._select_enemy_type()
                    difficulty = game._resolve_enemy_difficulty() if game else Difficulty.MEDIUM
                    enemy = Enemy(x, y, enemy_type, ai_difficulty=difficulty, team_id="rust")
                    if game:
                        enemy.game = game
                    enemies_list.append(enemy)
                    self.enemies_to_spawn -= 1
                    return enemy

            # Fallback: geordnetes Grid durchsuchen, aber niemals in Wände spawnen.
            for y in range(Config.GRID_SIZE, Config.HEIGHT - Config.GRID_SIZE, Config.GRID_SIZE):
                for x in range(Config.GRID_SIZE, Config.WIDTH - Config.GRID_SIZE, Config.GRID_SIZE):
                    if self._is_spawn_valid(x, y, players, enemies_list, walls, eagle):
                        enemy_type = self._select_enemy_type()
                        difficulty = game._resolve_enemy_difficulty() if game else Difficulty.MEDIUM
                        enemy = Enemy(x, y, enemy_type, ai_difficulty=difficulty, team_id="rust")
                        if game:
                            enemy.game = game
                        enemies_list.append(enemy)
                        self.enemies_to_spawn -= 1
                        return enemy
        return None

    def update(self, enemies_list, players, walls, eagle, game=None) -> None:
        """Update Wave Manager"""
        if self.wave_complete:
            return

        # Spawn Timer
        self.spawn_timer += 1
        if self.spawn_timer >= Config.ENEMY_SPAWN_INTERVAL:
            self.spawn_timer = 0
            enemy = self.spawn_enemy(enemies_list, players, walls, eagle, game)
            if enemy:
                enemy.update_ai(players, walls, eagle.rect.center if eagle else (Config.WIDTH//2, Config.HEIGHT//2))

        # Wave Progress - sofortiges Erkennen wenn alle Spawned und alle tot
        if self.enemies_to_spawn == 0 and len(enemies_list) == 0:
            self.wave_complete = True

    def next_wave(self) -> None:
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
# MAP GENERATOR - Professionelle Labyrinth-Algorithmen
# ============================================================================
class MapTheme:
    """Farbthema für Karten"""
    def __init__(self, name, background, ground_color, wall_colors, accent_color) -> None:
        self.name = name
        self.background = background
        self.ground_color = ground_color
        self.wall_colors = wall_colors
        self.accent_color = accent_color

class MapGenerator:
    """Professioneller Karten-Generator mit mehreren Algorithmen

    Unterstützt:
    - Recursive Backtracking (Labyrinth)
    - Cellular Automata (Höhlen)
    - Drunkard's Walk (Organisch)
    - Symmetrische Maps (Klassisch)
    """

    # Vordefinierte Themes
    THEMES = {
        "classic": MapTheme("Classic", (25, 25, 35), (45, 40, 55),
                           [(139, 69, 19), (160, 100, 60), (169, 169, 169)],
                           (255, 215, 0)),
        "industrial": MapTheme("Industrial", (20, 25, 30), (35, 40, 45),
                               [(80, 85, 90), (100, 105, 110), (120, 125, 130)],
                               (0, 200, 255)),
        "desert": MapTheme("Desert", (45, 38, 25), (70, 60, 40),
                          [(180, 150, 80), (160, 130, 70), (200, 180, 120)],
                          (255, 200, 100)),
        "arena": MapTheme("Arena", (15, 20, 35), (30, 35, 50),
                         [(100, 70, 120), (130, 90, 150), (80, 60, 100)],
                         (200, 150, 255)),
    }

    def __init__(self, map_type="classic", seed=None) -> None:
        self.map_type = map_type
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.theme = self.THEMES.get(map_type, self.THEMES["classic"])
        self.map_config = Config.MAPS.get(map_type, Config.MAPS["classic"])

    def generate(self):
        """Generiert eine Karte basierend auf Map-Typ"""
        if self.map_type == "classic":
            return self._generate_symmetric()
        if self.map_type == "industrial":
            return self._generate_industrial_factory()
        if self.map_type == "desert":
            return self._generate_recursive_backtracking(brick_heavy=True)
        if self.map_type == "arena":
            return self._generate_open_arena()
        if self.map_type == "crossfire":
            return self._generate_crossfire()
        if self.map_type == "islands":
            return self._generate_islands()
        if self.map_type.startswith("mission_"):
            return self._generate_mission_map()
        return self._generate_recursive_backtracking()

    def _clear_rect(self, grid, cx, cy, radius=2) -> None:
        """Räumt einen kleinen Bereich im Grid frei."""
        grid_h = len(grid)
        grid_w = len(grid[0])
        for y in range(max(1, cy - radius), min(grid_h - 1, cy + radius + 1)):
            for x in range(max(1, cx - radius), min(grid_w - 1, cx + radius + 1)):
                grid[y][x] = 0

    def _carve_line(self, grid, start, end, width=1) -> None:
        """Räumt eine horizontale/vertikale Verbindung frei."""
        sx, sy = start
        ex, ey = end
        steps = max(abs(ex - sx), abs(ey - sy), 1)
        for i in range(steps + 1):
            t = i / steps
            x = round(sx + (ex - sx) * t)
            y = round(sy + (ey - sy) * t)
            self._clear_rect(grid, x, y, width)

    def _apply_gameplay_safety(self, grid) -> None:
        """Macht Generator-Maps spielbar: freie Spawns, Eagle-Zone und Hauptwege."""
        grid_h = len(grid)
        grid_w = len(grid[0])
        spawn_points = [(2, 2), (grid_w - 3, 2), (2, grid_h - 3), (grid_w - 3, grid_h - 3)]
        eagle = (grid_w // 2, grid_h - 2)
        center = (grid_w // 2, grid_h // 2)

        for point in spawn_points:
            self._clear_rect(grid, point[0], point[1], 2)
            self._carve_line(grid, point, center, width=1)
        self._clear_rect(grid, eagle[0], eagle[1], 3)
        self._carve_line(grid, eagle, center, width=1)

        # Außenrahmen bleibt stabil aus Stahlwänden.
        for x in range(grid_w):
            grid[0][x] = 1
            grid[grid_h - 1][x] = 1
        for y in range(grid_h):
            grid[y][0] = 1
            grid[y][grid_w - 1] = 1

    def _grid_to_walls(self, grid, brick_heavy=False, steel_heavy=False):
        """Konvertiert ein 0/1-Grid in Wall-Objekte."""
        walls = []
        grid_h = len(grid)
        grid_w = len(grid[0])
        for y in range(grid_h):
            for x in range(grid_w):
                if grid[y][x] == 1:
                    wall_type = self._determine_wall_type(x, y, grid_w, grid_h, brick_heavy, steel_heavy)
                    walls.append(Wall(x * Config.GRID_SIZE, y * Config.GRID_SIZE,
                                    Config.GRID_SIZE, Config.GRID_SIZE, wall_type))
        return walls

    def _generate_recursive_backtracking(self, brick_heavy=False):
        """Labyrinth-Generator mit Recursive Backtracking

        Erzeugt ein vollständiges Labyrinth mit mehreren Lösungswegen.
        """
        grid_w = Config.WIDTH // Config.GRID_SIZE
        grid_h = Config.HEIGHT // Config.GRID_SIZE

        # Grid initialisieren (1 = Wand, 0 = Weg)
        grid = [[1] * grid_w for _ in range(grid_h)]

        # Mehrere Startpunkte für offenere Maps
        start_positions = [(1, 1), (grid_w - 2, 1), (1, grid_h - 2), (grid_w - 2, grid_h - 2)]

        for sx, sy in start_positions:
            if 0 < sx < grid_w - 1 and 0 < sy < grid_h - 1:
                grid[sy][sx] = 0
                self._carve_labyrinth(grid, sx, sy, grid_w, grid_h)

        # Zusätzliche Öffnungen für bessere Spielbarkeit
        self._add_openings(grid, num_openings=int(grid_w * grid_h * 0.02))

        self._apply_gameplay_safety(grid)
        return self._grid_to_walls(grid, brick_heavy=brick_heavy)

    def _carve_labyrinth(self, grid, cx, cy, grid_w, grid_h) -> None:
        """Rekursives Backtracking zum Generieren des Labyrinths"""
        grid[cy][cx] = 0
        stack = [(cx, cy)]

        while stack:
            x, y = stack[-1]
            neighbors = []

            for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
                nx, ny = x + dx, y + dy
                if (0 < nx < grid_w - 1 and 0 < ny < grid_h - 1 and
                    grid[ny][nx] == 1):
                    neighbors.append((nx, ny, x + dx // 2, y + dy // 2))

            if neighbors:
                random.shuffle(neighbors)
                nx, ny, wx, wy = neighbors[0]
                grid[ny][nx] = 0
                grid[wy][wx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

    def _add_openings(self, grid, num_openings=20) -> None:
        """Fügt zusätzliche Öffnungen hinzu für bessere Spielbarkeit"""
        grid_h = len(grid)
        grid_w = len(grid[0])

        for _ in range(num_openings):
            x = random.randint(1, grid_w - 2)
            y = random.randint(1, grid_h - 2)
            # Zähle benachbarte Wege
            path_neighbors = 0
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if grid[y + dy][x + dx] == 0:
                    path_neighbors += 1
            if path_neighbors >= 2:
                grid[y][x] = 0

    def _generate_symmetric(self):
        """Symmetrische Karte für fairen Mehrspieler-Spaß

        Erzeugt eine horizontal symmetrische Karte mit klassischen Elementen.
        """
        grid_w = Config.WIDTH // Config.GRID_SIZE
        grid_h = Config.HEIGHT // Config.GRID_SIZE
        half_w = grid_w // 2

        # Linke Hälfte generieren
        left_grid = [[1] * half_w for _ in range(grid_h)]
        left_grid[1][1] = 0
        self._carve_labyrinth(left_grid, 1, 1, half_w, grid_h)

        # Rechte Hälfte spiegeln
        full_grid = [[0] * grid_w for _ in range(grid_h)]
        for y in range(grid_h):
            for x in range(half_w):
                mirror_x = grid_w - 1 - x
                full_grid[y][x] = left_grid[y][x]
                full_grid[y][mirror_x] = left_grid[y][x]

        # Mitte etwas öffnen
        for y in range(grid_h // 3, 2 * grid_h // 3):
            for x in range(half_w - 2, half_w + 2):
                if 0 <= x < grid_w:
                    full_grid[y][x] = 0

        self._apply_gameplay_safety(full_grid)
        return self._grid_to_walls(full_grid)

    def _generate_industrial_factory(self):
        """Handkuratierte Industrial-Map (Map 2): offen, symmetrisch und taktisch lesbar.

        Die Karte vermeidet zufällige Blockade-Labyrinthe: breite Hauptwege,
        klare Flanken, ein zentraler Reaktorbereich und genug zerstörbare Cover-Crates.
        """
        grid_w = Config.WIDTH // Config.GRID_SIZE
        grid_h = Config.HEIGHT // Config.GRID_SIZE
        grid = [[0] * grid_w for _ in range(grid_h)]

        def set_wall(x, y, tag="machine") -> None:
            if 0 <= x < grid_w and 0 <= y < grid_h:
                grid[y][x] = tag

        def add_block(sx, sy, w, h, tag="machine") -> None:
            for yy in range(sy, sy + h):
                for xx in range(sx, sx + w):
                    if 0 < xx < grid_w - 1 and 0 < yy < grid_h - 1:
                        set_wall(xx, yy, tag)

        def clear_block(cx, cy, radius=2) -> None:
            for yy in range(max(1, cy - radius), min(grid_h - 1, cy + radius + 1)):
                for xx in range(max(1, cx - radius), min(grid_w - 1, cx + radius + 1)):
                    grid[yy][xx] = 0

        # Stabiler Stahlrahmen.
        for x in range(grid_w):
            set_wall(x, 0, "border")
            set_wall(x, grid_h - 1, "border")
        for y in range(grid_h):
            set_wall(0, y, "border")
            set_wall(grid_w - 1, y, "border")

        cx, cy = grid_w // 2, grid_h // 2

        # Symmetrische Maschinenhallen: genug Deckung, aber keine Sackgassen.
        machine_blocks = [
            (4, 4, 4, 2), (grid_w - 8, 4, 4, 2),
            (4, 8, 3, 3), (grid_w - 7, 8, 3, 3),
            (4, 16, 4, 2), (grid_w - 8, 16, 4, 2),
            (9, 6, 2, 4), (grid_w - 11, 6, 2, 4),
            (9, 14, 2, 4), (grid_w - 11, 14, 2, 4),
        ]
        for block in machine_blocks:
            add_block(*block, tag="machine")

        # Zentraler Reaktor: markante Arena mit vier Ein-/Ausgängen.
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 4, cx + 5):
                edge = abs(x - cx) in (3, 4) or abs(y - cy) == 3
                gate = (x == cx) or (y == cy)
                if edge and not gate:
                    set_wall(x, y, "reactor")

        # Kurze Cover-Pods für Feuerpausen und Flankenwinkel.
        cover_pods = [
            (cx - 8, cy - 5), (cx + 7, cy - 5),
            (cx - 8, cy + 4), (cx + 7, cy + 4),
            (cx - 3, cy - 6), (cx + 3, cy + 5),
        ]
        for px, py in cover_pods:
            add_block(px, py, 2, 1, tag="crate")

        # Hauptwege bewusst breit freihalten: links/rechts, Mitte, obere/untere Traverse.
        for lane_x in (3, cx, grid_w - 4):
            self._carve_line(grid, (lane_x, 1), (lane_x, grid_h - 2), width=1)
        for lane_y in (3, cy, grid_h - 4):
            self._carve_line(grid, (1, lane_y), (grid_w - 2, lane_y), width=1)

        # Spawn-, Eagle- und Center-Sicherheit ohne die komplette Factory wegzuräumen.
        for sx, sy in ((2, 2), (grid_w - 3, 2), (2, grid_h - 3), (grid_w - 3, grid_h - 3)):
            clear_block(sx, sy, radius=2)
            self._carve_line(grid, (sx, sy), (cx, cy), width=1)
        clear_block(cx, grid_h - 2, radius=3)
        clear_block(cx, cy, radius=1)
        self._carve_line(grid, (cx, grid_h - 2), (cx, cy), width=1)

        # Außenrahmen nach dem Carving wiederherstellen.
        for x in range(grid_w):
            set_wall(x, 0, "border")
            set_wall(x, grid_h - 1, "border")
        for y in range(grid_h):
            set_wall(0, y, "border")
            set_wall(grid_w - 1, y, "border")

        walls = []
        for y in range(grid_h):
            for x in range(grid_w):
                tag = grid[y][x]
                if not tag:
                    continue
                if tag in ("border", "reactor"):
                    wall_type = WallType.STEEL
                elif tag == "crate":
                    wall_type = WallType.BRICK
                else:
                    # Mehr zerstörbare Elemente als vorher, damit Map 2 nicht zu starr wirkt.
                    pattern = (x * 11 + y * 17) % 100
                    wall_type = WallType.STEEL if pattern < 48 else WallType.BRICK
                walls.append(Wall(x * Config.GRID_SIZE, y * Config.GRID_SIZE,
                                  Config.GRID_SIZE, Config.GRID_SIZE, wall_type))
        return walls

    def _generate_cellular_automata(self, steel_heavy=False):
        """Höhlen-Generator mit Cellular Automata + garantierte Wege

        Erzeugt organische Höhlen mit durchgängigen Korridoren und klaren Spawn-Bereichen.
        """
        grid_w = Config.WIDTH // Config.GRID_SIZE
        grid_h = Config.HEIGHT // Config.GRID_SIZE

        # Initial zufälliges Grid – mehr offene Flächen
        grid = [[1] * grid_w for _ in range(grid_h)]
        for y in range(grid_h):
            for x in range(grid_w):
                grid[y][x] = 0 if random.random() < 0.50 else 1

        # Cellular Automata – nur 3 Iterationen, mildere thresholds
        for _ in range(3):
            new_grid = [row[:] for row in grid]
            for y in range(1, grid_h - 1):
                for x in range(1, grid_w - 1):
                    wall_count = 0
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if grid[y + dy][x + dx] == 1:
                                wall_count += 1
                    if wall_count >= 5:
                        new_grid[y][x] = 1
                    elif wall_count <= 3:
                        new_grid[y][x] = 0
            grid = new_grid

        # Außenwände sicherstellen
        for x in range(grid_w):
            grid[0][x] = 1
            grid[grid_h - 1][x] = 1
        for y in range(grid_h):
            grid[y][0] = 1
            grid[y][grid_w - 1] = 1

        # Horizontale Hauptkorridore ziehen (garantierte Wege)
        corridor_rows = [grid_h // 4, grid_h // 2, 3 * grid_h // 4]
        for cr in corridor_rows:
            for x in range(1, grid_w - 1):
                grid[cr][x] = 0
            # Vertikale Ausläufer an Korridoren
            for y in range(max(1, cr - 2), min(grid_h - 1, cr + 3)):
                for offset in [0, grid_w // 4, grid_w // 2, 3 * grid_w // 4]:
                    if 0 < offset < grid_w - 1:
                        grid[y][offset] = 0

        # Vertikale Hauptkorridore
        corridor_cols = [grid_w // 4, grid_w // 2, 3 * grid_w // 4]
        for cc in corridor_cols:
            for y in range(1, grid_h - 1):
                grid[y][cc] = 0
            # Horizontale Ausläufer
            for x in range(max(1, cc - 2), min(grid_w - 1, cc + 3)):
                for y_offset in [grid_h // 4, grid_h // 2, 3 * grid_h // 4]:
                    if 0 < y_offset < grid_h - 1:
                        grid[y_offset][x] = 0

        # Spawn-Bereiche komplett freiräumen (oben links, oben rechts, unten links, unten rechts)
        # Plus direkte Verbindungen zu den nächsten Korridoren (keine Gefängnisse!)
        spawn_connections = [
            # (start_x, start_y, end_x, end_y) – gerade Linien
            # Oben links → vertikaler Korridor bei grid_w // 4
            [(1, 1, 1, grid_h // 4), (1, grid_h // 4, grid_w // 4, grid_h // 4)],
            # Oben rechts → vertikaler Korridor bei grid_w // 4 oder 3*grid_w // 4
            [(grid_w - 2, 1, grid_w - 2, grid_h // 4), (grid_w - 2, grid_h // 4, 3 * grid_w // 4, grid_h // 4)],
            # Unten links → vertikaler Korridor bei grid_w // 4
            [(1, grid_h - 2, 1, 3 * grid_h // 4), (1, 3 * grid_h // 4, grid_w // 4, 3 * grid_h // 4)],
            # Unten rechts → vertikaler Korridor bei 3*grid_w // 4
            [(grid_w - 2, grid_h - 2, grid_w - 2, 3 * grid_h // 4), (grid_w - 2, 3 * grid_h // 4, 3 * grid_w // 4, 3 * grid_h // 4)],
        ]
        for connection in spawn_connections:
            for (sx2, sy2, ex2, ey2) in connection:
                dx = 1 if ex2 >= sx2 else -1
                dy = 1 if ey2 >= sy2 else -1
                cx, cy = sx2, sy2
                while cx != ex2 + dx or cy != ey2 + dy:
                    if 0 < cx < grid_w - 1 and 0 < cy < grid_h - 1:
                        grid[cy][cx] = 0
                    cx += dx
                    cy += dy

        # Eagle-Bereich freiräumen (unten mitte)
        eagle_x = grid_w // 2
        for y in range(grid_h - 5, grid_h - 1):
            for x in range(eagle_x - 2, eagle_x + 3):
                if 0 <= x < grid_w:
                    grid[y][x] = 0

        self._apply_gameplay_safety(grid)
        return self._grid_to_walls(grid, steel_heavy=steel_heavy)

    def _remove_large_areas(self, grid, max_area=100) -> None:
        """Entfernt Wände um große offene Bereiche zu verkleinern"""
        grid_h = len(grid)
        grid_w = len(grid[0])
        visited = [[False] * grid_w for _ in range(grid_h)]

        for y in range(1, grid_h - 1):
            for x in range(1, grid_w - 1):
                if grid[y][x] == 0 and not visited[y][x]:
                    area = self._flood_fill(grid, visited, x, y, set())
                    if len(area) > max_area:
                        # Wände in der Mitte des Bereichs hinzufügen
                        cx = sum(p[0] for p in area) // len(area)
                        cy = sum(p[1] for p in area) // len(area)
                        grid[cy][cx] = 1

    def _flood_fill(self, grid, visited, x, y, visited_set):
        """Flood Fill um offene Bereiche zu zählen"""
        grid_h = len(grid)
        grid_w = len(grid[0])
        stack = [(x, y)]
        area = set()

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited_set or not (0 <= cx < grid_w and 0 <= cy < grid_h):
                continue
            if grid[cy][cx] == 1:
                continue

            visited_set.add((cx, cy))
            area.add((cx, cy))

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                stack.append((cx + dx, cy + dy))

        return area

    def _generate_open_arena(self):
        """Offene Arena mit wenigen Deckungen

        Ideal für schnelle Matches.
        """
        grid_w = Config.WIDTH // Config.GRID_SIZE
        grid_h = Config.HEIGHT // Config.GRID_SIZE

        # Alles als Weg initialisieren
        grid = [[0] * grid_w for _ in range(grid_h)]

        # Außenwände
        for x in range(grid_w):
            grid[0][x] = 1
            grid[grid_h - 1][x] = 1
        for y in range(grid_h):
            grid[y][0] = 1
            grid[y][grid_w - 1] = 1

        # Einige Deckungs-Strukturen
        structure_count = random.randint(8, 15)
        for _ in range(structure_count):
            sx = random.randint(2, grid_w - 4)
            sy = random.randint(2, grid_h - 4)
            size = random.randint(2, 4)
            for dy in range(size):
                for dx in range(size):
                    if 0 < sy + dy < grid_h - 1 and 0 < sx + dx < grid_w - 1:
                        grid[sy + dy][sx + dx] = 1

        # Spawn-Bereiche frei halten
        spawn_zones = [(2, 2), (grid_w - 4, 2), (2, grid_h - 4), (grid_w - 4, grid_h - 4)]
        for sx, sy in spawn_zones:
            for dy in range(3):
                for dx in range(3):
                    if 0 < sy + dy < grid_h - 1 and 0 < sx + dx < grid_w - 1:
                        grid[sy + dy][sx + dx] = 0

        self._apply_gameplay_safety(grid)
        return self._grid_to_walls(grid, steel_heavy=True)

    def _generate_crossfire(self):
        """Vier Basen mit zentralem Kampfbereich und klaren Schussachsen."""
        grid_w = Config.WIDTH // Config.GRID_SIZE
        grid_h = Config.HEIGHT // Config.GRID_SIZE
        grid = [[0] * grid_w for _ in range(grid_h)]

        for x in range(grid_w):
            grid[0][x] = 1
            grid[grid_h - 1][x] = 1
        for y in range(grid_h):
            grid[y][0] = 1
            grid[y][grid_w - 1] = 1

        cx, cy = grid_w // 2, grid_h // 2
        # Zentrale Festung mit Öffnungen.
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 3, cx + 4):
                if abs(x - cx) in (2, 3) or abs(y - cy) in (2, 3):
                    grid[y][x] = 1
        self._clear_rect(grid, cx, cy, 1)

        # Diagonale Deckungsinseln.
        for sx, sy in [(6, 5), (grid_w - 8, 5), (6, grid_h - 8), (grid_w - 8, grid_h - 8)]:
            for dy in range(3):
                for dx in range(4):
                    grid[sy + dy][sx + dx] = 1

        self._apply_gameplay_safety(grid)
        return self._grid_to_walls(grid)

    def _generate_islands(self):
        """Mehrere Wandinseln mit breiten Brückenlinien, weniger klaustrophobisch als Labyrinth."""
        grid_w = Config.WIDTH // Config.GRID_SIZE
        grid_h = Config.HEIGHT // Config.GRID_SIZE
        grid = [[0] * grid_w for _ in range(grid_h)]

        for x in range(grid_w):
            grid[0][x] = 1
            grid[grid_h - 1][x] = 1
        for y in range(grid_h):
            grid[y][0] = 1
            grid[y][grid_w - 1] = 1

        island_centers = [
            (grid_w // 4, grid_h // 4), (grid_w // 2, grid_h // 4), (3 * grid_w // 4, grid_h // 4),
            (grid_w // 4, grid_h // 2), (3 * grid_w // 4, grid_h // 2),
            (grid_w // 4, 3 * grid_h // 4), (grid_w // 2, 3 * grid_h // 4), (3 * grid_w // 4, 3 * grid_h // 4),
        ]
        for cx, cy in island_centers:
            radius = random.randint(1, 2)
            for y in range(cy - radius, cy + radius + 1):
                for x in range(cx - radius - 1, cx + radius + 2):
                    if 0 < x < grid_w - 1 and 0 < y < grid_h - 1:
                        if random.random() < 0.72:
                            grid[y][x] = 1

        # Breite Brücken / Routen freihalten.
        for y in [grid_h // 4, grid_h // 2, 3 * grid_h // 4]:
            self._carve_line(grid, (1, y), (grid_w - 2, y), width=1)
        for x in [grid_w // 4, grid_w // 2, 3 * grid_w // 4]:
            self._carve_line(grid, (x, 1), (x, grid_h - 2), width=1)

        self._apply_gameplay_safety(grid)
        return self._grid_to_walls(grid, brick_heavy=True)

    def _generate_mission_map(self):
        """Handgebaute Tutorial-/Quest-Maps für die drei Missionen."""
        grid_w = Config.WIDTH // Config.GRID_SIZE
        grid_h = Config.HEIGHT // Config.GRID_SIZE
        grid = [[0] * grid_w for _ in range(grid_h)]

        def set_wall(x, y, tag="brick") -> None:
            if 0 <= x < grid_w and 0 <= y < grid_h:
                grid[y][x] = tag

        def add_block(sx, sy, w, h, tag="brick") -> None:
            for yy in range(sy, sy + h):
                for xx in range(sx, sx + w):
                    if 0 < xx < grid_w - 1 and 0 < yy < grid_h - 1:
                        set_wall(xx, yy, tag)

        for x in range(grid_w):
            set_wall(x, 0, "steel")
            set_wall(x, grid_h - 1, "steel")
        for y in range(grid_h):
            set_wall(0, y, "steel")
            set_wall(grid_w - 1, y, "steel")

        cx, cy = grid_w // 2, grid_h // 2
        if self.map_type == "mission_1":
            # Sehr offene erste Karte: nur wenige Deckungen und klare Wege.
            add_block(8, 5, 3, 1, "brick")
            add_block(17, 6, 3, 1, "brick")
            add_block(9, 14, 3, 1, "brick")
            add_block(20, 14, 3, 1, "brick")
            self._clear_rect(grid, 2, grid_h - 3, 3)
            self._clear_rect(grid, grid_w - 4, 3, 2)
        elif self.map_type == "mission_2":
            # Rostpass: S-förmige Deckung, aber breite Tutorial-Korridore.
            for x in range(5, grid_w - 5):
                if x not in (8, 15, 23):
                    set_wall(x, 6, "brick")
                if x not in (6, 16, 25):
                    set_wall(x, 15, "brick")
            add_block(6, 9, 3, 2, "steel")
            add_block(grid_w - 10, 11, 3, 2, "steel")
            self._carve_line(grid, (2, grid_h - 3), (cx, cy), width=1)
            self._carve_line(grid, (cx, cy), (grid_w - 4, 3), width=1)
        else:
            # Ferrum-Brücke: mittlere Herausforderung mit zentraler Brücke und Flanken.
            for y in range(3, grid_h - 3):
                if y not in (6, cy, grid_h - 7):
                    set_wall(cx - 4, y, "steel")
                    set_wall(cx + 4, y, "steel")
            for x in range(cx - 4, cx + 5):
                set_wall(x, cy - 2, "brick")
                set_wall(x, cy + 2, "brick")
            self._clear_rect(grid, cx, cy, 2)
            self._carve_line(grid, (2, grid_h - 3), (cx, cy), width=1)
            self._carve_line(grid, (grid_w - 4, 3), (cx, cy), width=1)
            self._carve_line(grid, (grid_w - 4, grid_h - 4), (cx, cy), width=1)

        # Spieler- und Basisbereiche immer frei halten.
        for point in ((2, grid_h - 3), (3, grid_h - 4), (grid_w - 4, 3), (grid_w - 4, grid_h - 4), (cx, grid_h - 2)):
            self._clear_rect(grid, point[0], point[1], 2)
        self._clear_rect(grid, cx, cy, 1)

        walls = []
        for y in range(grid_h):
            for x in range(grid_w):
                tag = grid[y][x]
                if not tag:
                    continue
                wall_type = WallType.STEEL if tag == "steel" else WallType.BRICK
                walls.append(Wall(x * Config.GRID_SIZE, y * Config.GRID_SIZE,
                                  Config.GRID_SIZE, Config.GRID_SIZE, wall_type))
        return walls

    def _determine_wall_type(self, x, y, grid_w, grid_h, brick_heavy=False, steel_heavy=False):
        """Bestimmt den Wand-Typ mit verbessertem Algorithmus"""
        # Außenwände sind immer Stahl
        if x == 0 or x == grid_w - 1 or y == 0 or y == grid_h - 1:
            return WallType.STEEL

        # Steel-Ratio basierend auf Map-Typ
        if steel_heavy:
            steel_ratio = 0.5
        elif brick_heavy:
            steel_ratio = 0.3
        elif self.map_type == "industrial":
            steel_ratio = self.map_config.get("steel_ratio", 0.5)
        elif self.map_type == "desert":
            steel_ratio = 1 - self.map_config.get("brick_ratio", 0.7)
        else:
            steel_ratio = 0.4

        # Deterministisch basierend auf Position und Map-Typ (ohne Python hash-randomization)
        map_seed = sum(ord(ch) for ch in self.map_type)
        seed = (x * 7 + y * 13 + map_seed) % 100
        return WallType.STEEL if seed < steel_ratio * 100 else WallType.BRICK

# ============================================================================
# GAME MANAGER mit verbessertem UI
# ============================================================================
class GameManager:
    def __init__(self) -> None:
        pygame.init()
        # mixer wird jetzt von SoundManager initialisiert
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("PyTank - Tank Battle")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.MAIN_MENU
        self.sound_manager = SoundManager()
        self.background = BackgroundRenderer()

        # Game entities
        self.players: list[Player] = []
        self.enemies: list[Enemy] = []
        self.walls: list[Wall] = []
        self.bullets: list[Bullet] = []
        self.particles: list[Particle] = []
        self.powerups: list[Powerup] = []
        self.eagle: Eagle | None = None
        self.wave_manager: WaveManager | None = None

        # Screen shake
        self.screen_shake = 0

        # Score
        self.score = {1: 0, 2: 0}

        # Level selection
        self.selected_map = "classic"

        # Game mode (Singleplayer standard); Co-op ist ein Add-on, kein eigener Modus.
        self.game_mode = GameMode.HORDE
        self.coop_enabled = False
        self.difficulty = Difficulty.MEDIUM
        self.player_name = "Player 1"

        # Mission System
        self.mission = "Eagle Protect"
        self.mission_active = True
        self.mission_intro_text = ""
        self.mission_victory_text = ""
        self.mission_intro_frames = 0

        # Time Limit
        self.game_time = 0
        self.time_limit = Config.TIME_LIMIT
        self.time_running = False

        # Powerup spawn timer
        self.powerup_spawn_timer = 0

        # Vollbildmodus
        self.fullscreen = False

        # Endscreen sound flags
        self._victory_played = False
        self._lose_played = False

        # Menü-Fokus für Tastatur-, Maus- und Touch-Bedienung
        self.main_menu_index = 1  # Horde als empfohlener Standard
        self.overlay_button_index = 0

    def _selectable_map_keys(self):
        """Maps abhängig vom Modus: Missionen haben eigene Quest-Karten."""
        return Config.MISSION_ORDER if self.game_mode == GameMode.MISSIONS else Config.MAP_ORDER

    def _ensure_selected_map_for_mode(self) -> None:
        maps = self._selectable_map_keys()
        if self.selected_map not in maps:
            self.selected_map = maps[0]

    def _mode_label(self) -> str:
        return {
            GameMode.FFA: "Free For All",
            GameMode.HORDE: "Horde",
            GameMode.MISSIONS: "Missionen",
        }.get(self.game_mode, self.game_mode)

    def _coop_label(self) -> str:
        return "Co-op AN" if self.coop_enabled else "Solo"

    def _cycle_difficulty(self) -> None:
        idx = Difficulty.ORDER.index(self.difficulty)
        self.difficulty = Difficulty.ORDER[(idx + 1) % len(Difficulty.ORDER)]

    def _resolve_enemy_difficulty(self, index=None):
        if self.difficulty == Difficulty.MIXED:
            if index is not None:
                return Difficulty.AI_POOL[index % len(Difficulty.AI_POOL)]
            return random.choice(Difficulty.AI_POOL)
        return self.difficulty

    def _enemy_type_from_string(self, value):
        value = str(value).lower()
        if value == EnemyType.SCOUT:
            return EnemyType.SCOUT
        if value == EnemyType.BRUTE:
            return EnemyType.BRUTE
        return EnemyType.GUNNER

    def reset_game(self, mode=GameMode.FFA, map_type="classic") -> None:
        """Resetet das Spiel"""
        self.players = []
        self.enemies = []
        self.walls = []
        self.bullets = []
        self.particles = []
        self.powerups = []
        self.score = {1: 0, 2: 0}
        self.screen_shake = 0
        self.game_mode = mode
        self.selected_map = map_type
        self.game_time = 0
        self.powerup_spawn_timer = 0
        self.mission = "Eagle Protect"
        self.mission_intro_text = ""
        self.mission_victory_text = ""
        self.mission_intro_frames = 0
        self._victory_played = False
        self._lose_played = False

        self._ensure_selected_map_for_mode()

        # FFA ist echtes Deathmatch ohne Basis; Horde und Missionen behalten den Pythaner-Kommandoposten.
        if mode == GameMode.FFA:
            self.eagle = None
        else:
            self.eagle = Eagle(Config.WIDTH//2 - 10, Config.HEIGHT - Config.GRID_SIZE * 2 + 15)
            self.eagle.state = EagleState.PROTECTED

        # Setup wave manager only for Horde; Co-op ist nur zusätzliche Spieleranzahl.
        self.wave_manager = WaveManager() if mode == GameMode.HORDE else None

        # Setup level
        self._setup_level()

    def _find_free_positions(self, walls, count, offset=50, min_distance=None):
        """Findet freie, nicht überlappende Positionen ohne deterministische Top-Left-Bias."""
        positions = []
        min_distance = min_distance or Config.GRID_SIZE * 2
        occupied_rects = [p.rect for p in self.players] + [e.rect for e in self.enemies]
        if self.eagle:
            occupied_rects.append(self.eagle.rect.inflate(Config.GRID_SIZE * 2, Config.GRID_SIZE * 2))

        def is_free(x, y) -> bool:
            test_rect = pygame.Rect(x, y, Config.GRID_SIZE - 10, Config.GRID_SIZE - 10)
            if any(test_rect.colliderect(wall.rect) for wall in walls):
                return False
            if any(test_rect.colliderect(rect) for rect in occupied_rects):
                return False
            for px, py in positions:
                if math.hypot(x - px, y - py) < min_distance:
                    return False
            return True

        # Erst zufällig versuchen, danach geordnetes Grid als Fallback.
        for _ in range(700):
            x = random.randrange(offset, Config.WIDTH - offset - 40, 10)
            y = random.randrange(offset, Config.HEIGHT - offset - 40, 10)
            if is_free(x, y):
                positions.append((x, y))
                if len(positions) >= count:
                    return positions

        for y in range(offset, Config.HEIGHT - offset - 40, 10):
            for x in range(offset, Config.WIDTH - offset - 40, 10):
                if is_free(x, y):
                    positions.append((x, y))
                    if len(positions) >= count:
                        return positions
        return positions

    def _setup_level(self) -> None:
        """Setuppt Level mit Wänden, Spielern und Gegnern"""
        # Generate walls (inkl. Außenwände als Stahl via _determine_wall_type)
        map_generator = MapGenerator(self.selected_map)
        self.walls = map_generator.generate()

        # Create players based on Modus; Co-op wird innerhalb jedes Modus als Add-on angewendet.
        if self.game_mode == GameMode.FFA:
            self._setup_ffa_mode()
        elif self.game_mode == GameMode.MISSIONS:
            self._setup_mission_mode()
        else:
            self._setup_horde_mode()

    def _register_enemy(self, enemy) -> None:
        """Fügt Enemy hinzu und setzt Rückreferenz für KI-Kontext."""
        enemy.game = self
        self.enemies.append(enemy)

    def _create_outer_walls(self):
        """Erstellt die Außenwände (alle Stahl) – DEPRECATED, Map-Generator erstellt Border bereits.
        Nur noch als Backup verfügbar."""
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

    def _controls_for_player(self, player_id):
        if player_id == 2:
            return {
                'up': pygame.K_UP, 'down': pygame.K_DOWN,
                'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                'shoot': pygame.K_RETURN
            }
        return {
            'up': pygame.K_w, 'down': pygame.K_s,
            'left': pygame.K_a, 'right': pygame.K_d,
            'shoot': pygame.K_SPACE
        }

    def _spawn_players(self, team_id="pythons") -> None:
        player_count = 2 if self.coop_enabled else 1
        positions = self._find_free_positions(self.walls, player_count, 100)
        colors = {1: Config.COLOR_P1, 2: Config.COLOR_P2}
        for idx in range(player_count):
            if idx >= len(positions):
                break
            player_id = idx + 1
            x, y = positions[idx]
            self.players.append(Player(player_id, x, y, colors[player_id], self._controls_for_player(player_id),
                                       team_id=team_id, display_name=f"Player {player_id}"))

    def _random_enemy_type(self):
        roll = random.random()
        if roll < Config.SCOUT_SPAWN_CHANCE:
            return EnemyType.SCOUT
        if roll < Config.SCOUT_SPAWN_CHANCE + Config.BRUTE_SPAWN_CHANCE:
            return EnemyType.BRUTE
        return EnemyType.GUNNER

    def _ffa_targets_for(self, enemy):
        """Gegnerische Ziele für echtes Free For All: Spieler und KI aus anderen Teams."""
        targets = [p for p in self.players if p.team_id != enemy.team_id and p.lives > 0]
        targets.extend(e for e in self.enemies if e is not enemy and e.team_id != enemy.team_id)
        return targets

    def _setup_ffa_mode(self) -> None:
        """Setup FFA: Solo = jeder Tank gegen jeden; Co-op = feste 2er-Teams bei gleicher Tankanzahl."""
        self.mission = "Free For All"
        self._spawn_players(team_id="pythons" if self.coop_enabled else "player1")

        total_tanks = Config.FFA_TOTAL_TANKS
        num_enemies = max(0, total_tanks - len(self.players))
        mixed_difficulties = []
        if self.difficulty == Difficulty.MIXED:
            mixed_difficulties = (Difficulty.AI_POOL * ((num_enemies // len(Difficulty.AI_POOL)) + 1))[:num_enemies]
            random.shuffle(mixed_difficulties)
        for i in range(num_enemies):
            positions = self._find_free_positions(self.walls, 1, 50)
            if not positions:
                continue
            x, y = positions[0]
            if self.coop_enabled:
                # Spieler sind ein 2er-Team; KI wird ebenfalls paarweise in Teams verteilt.
                team_id = f"rust_team_{i // 2 + 1}"
            else:
                team_id = f"rust_solo_{i + 1}"
            difficulty = mixed_difficulties[i] if mixed_difficulties else self._resolve_enemy_difficulty(i)
            enemy = Enemy(x, y, self._random_enemy_type(),
                          ai_difficulty=difficulty, team_id=team_id)
            self._register_enemy(enemy)

        for _ in range(random.randint(1, 2)):
            self._spawn_powerup()

    def _setup_horde_mode(self) -> None:
        """Setup Horde: Wellen überleben, solo oder co-op."""
        self.mission = "Horde - Überlebt alle Wellen"
        self._spawn_players(team_id="pythons")

        # Start wave 1
        if self.wave_manager:
            self.wave_manager.next_wave()

    def _setup_mission_mode(self) -> None:
        """Setup Missionen: drei kurze Tutorial-Questkarten mit eigener Gegnerplatzierung."""
        self._spawn_players(team_id="pythons")
        mission = Config.MISSION_DATA.get(self.selected_map, Config.MISSION_DATA["mission_1"])
        self.mission = f"{mission['title']} ({mission['difficulty']})"
        self.mission_intro_text = mission["intro"].format(player=self.player_name)
        self.mission_victory_text = mission["victory"].format(player=self.player_name)
        self.mission_intro_frames = 8 * Config.FPS

        for _i, (x, y, enemy_type, difficulty) in enumerate(mission["enemies"]):
            # Falls eine Missionsposition durch Wände blockiert ist, robust auf freien Spawn ausweichen.
            test_rect = pygame.Rect(x, y, Config.GRID_SIZE - 10, Config.GRID_SIZE - 10)
            if any(test_rect.colliderect(wall.rect) for wall in self.walls):
                positions = self._find_free_positions(self.walls, 1, 80)
                if positions:
                    x, y = positions[0]
            enemy = Enemy(x, y, self._enemy_type_from_string(enemy_type),
                          ai_difficulty=difficulty, team_id="rust")
            self._register_enemy(enemy)

        for _ in range(1 if self.selected_map == "mission_1" else 2):
            self._spawn_powerup()

    def handle_events(self) -> None:
        """Behandelt Eingabe-Events für Tastatur, Maus und Touch."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue

            # Maus: Button-Down reicht als Bestätigung, damit Linksklick zuverlässig funktioniert.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_state == GameState.PLAYING:
                    self._handle_volume_slider_click(event.pos)
                elif self.game_state in [GameState.MAIN_MENU, GameState.LEVEL_SELECT]:
                    self._handle_menu_mouse_click(event.pos)
                elif self.game_state in [GameState.PAUSED, GameState.GAME_OVER, GameState.VICTORY]:
                    self._handle_overlay_click(event.pos)
                continue

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.game_state == GameState.PLAYING:
                    self._handle_volume_slider_click(event.pos)
                elif self.game_state in [GameState.MAIN_MENU, GameState.LEVEL_SELECT]:
                    self._handle_menu_mouse_click(event.pos)
                elif self.game_state in [GameState.PAUSED, GameState.GAME_OVER, GameState.VICTORY]:
                    self._handle_overlay_click(event.pos)
                continue

            if event.type == pygame.MOUSEMOTION:
                if self.game_state == GameState.PLAYING:
                    self._handle_volume_slider_drag(event.pos)
                elif self.game_state in [GameState.MAIN_MENU, GameState.LEVEL_SELECT]:
                    self._handle_menu_pointer_motion(event.pos)
                elif self.game_state in [GameState.PAUSED, GameState.GAME_OVER, GameState.VICTORY]:
                    self._handle_overlay_mouse_motion(event.pos)
                continue

            # Touch-Events nutzen normalisierte Koordinaten (0..1).
            if event.type in (pygame.FINGERDOWN, pygame.FINGERMOTION, pygame.FINGERUP):
                touch_pos = self._touch_to_screen(event)
                if event.type in (pygame.FINGERDOWN, pygame.FINGERMOTION):
                    if self.game_state in [GameState.MAIN_MENU, GameState.LEVEL_SELECT]:
                        self._handle_menu_pointer_motion(touch_pos)
                    elif self.game_state in [GameState.PAUSED, GameState.GAME_OVER, GameState.VICTORY]:
                        self._handle_overlay_mouse_motion(touch_pos)
                    elif self.game_state == GameState.PLAYING and event.type == pygame.FINGERDOWN:
                        self._handle_volume_slider_click(touch_pos)
                elif event.type == pygame.FINGERUP:
                    if self.game_state in [GameState.MAIN_MENU, GameState.LEVEL_SELECT]:
                        self._handle_menu_mouse_click(touch_pos)
                    elif self.game_state in [GameState.PAUSED, GameState.GAME_OVER, GameState.VICTORY]:
                        self._handle_overlay_click(touch_pos)
                continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_f:
                self._toggle_fullscreen()
                continue

            if self.game_state == GameState.MAIN_MENU:
                if event.key == pygame.K_c:
                    self.coop_enabled = not self.coop_enabled
                elif event.key == pygame.K_d:
                    self._cycle_difficulty()
                elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_LEFT, pygame.K_a):
                    self.main_menu_index = (self.main_menu_index - 1) % 3
                elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_RIGHT):
                    self.main_menu_index = (self.main_menu_index + 1) % 3
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self._activate_main_menu_index(self.main_menu_index)
                elif event.key in (pygame.K_1, pygame.K_KP1):
                    self._activate_main_menu_index(0)
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    self._activate_main_menu_index(1)
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    self._activate_main_menu_index(2)

            elif self.game_state == GameState.LEVEL_SELECT:
                self._ensure_selected_map_for_mode()
                maps = self._selectable_map_keys()
                idx = maps.index(self.selected_map)
                number_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
                keypad_keys = [pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6]

                if event.key == pygame.K_c:
                    self.coop_enabled = not self.coop_enabled
                elif event.key == pygame.K_d and self.game_mode != GameMode.MISSIONS:
                    self._cycle_difficulty()
                elif event.key in number_keys[:len(maps)]:
                    self.selected_map = maps[number_keys.index(event.key)]
                elif event.key in keypad_keys[:len(maps)]:
                    self.selected_map = maps[keypad_keys.index(event.key)]
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.selected_map = maps[(idx - 1) % len(maps)]
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.selected_map = maps[(idx + 1) % len(maps)]
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_map = maps[(idx - 2) % len(maps)]
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_map = maps[(idx + 2) % len(maps)]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self._start_game()
                elif event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    self.game_state = GameState.MAIN_MENU

            elif self.game_state == GameState.PLAYING:
                if event.key in (pygame.K_ESCAPE, pygame.K_p):
                    self.overlay_button_index = 0
                    self.game_state = GameState.PAUSED
                elif event.key == pygame.K_v:
                    self.sound_manager.set_music_volume(self.sound_manager.get_music_volume() - 0.1)
                elif event.key == pygame.K_c:
                    self.sound_manager.set_music_volume(self.sound_manager.get_music_volume() + 0.1)
                elif event.key == pygame.K_b:
                    self.sound_manager.set_sfx_volume(self.sound_manager.get_sfx_volume() - 0.1)
                elif event.key == pygame.K_n:
                    self.sound_manager.set_sfx_volume(self.sound_manager.get_sfx_volume() + 0.1)
                elif event.key == pygame.K_m:
                    if self.sound_manager.get_sfx_volume() > 0:
                        self.sound_manager.set_sfx_volume(0)
                        self.sound_manager.set_music_volume(0)
                    else:
                        self.sound_manager.set_sfx_volume(Config.SFX_VOLUME)
                        self.sound_manager.set_music_volume(Config.MUSIC_VOLUME)

            elif self.game_state == GameState.PAUSED:
                if event.key in (pygame.K_UP, pygame.K_w, pygame.K_LEFT, pygame.K_a):
                    self.overlay_button_index = (self.overlay_button_index - 1) % len(self._overlay_buttons_for_state())
                elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_RIGHT, pygame.K_d):
                    self.overlay_button_index = (self.overlay_button_index + 1) % len(self._overlay_buttons_for_state())
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self._activate_overlay_button(self.overlay_button_index)
                elif event.key in (pygame.K_ESCAPE, pygame.K_p):
                    self.game_state = GameState.PLAYING
                elif event.key == pygame.K_r:
                    self._activate_overlay_button(1)
                elif event.key == pygame.K_q:
                    self._activate_overlay_button(2)

            elif self.game_state in (GameState.GAME_OVER, GameState.VICTORY):
                buttons = self._overlay_buttons_for_state()
                if event.key in (pygame.K_UP, pygame.K_w, pygame.K_LEFT, pygame.K_a):
                    self.overlay_button_index = (self.overlay_button_index - 1) % len(buttons)
                elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_RIGHT, pygame.K_d):
                    self.overlay_button_index = (self.overlay_button_index + 1) % len(buttons)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self._activate_overlay_button(self.overlay_button_index)
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self._activate_overlay_button(0)
                elif event.key in (pygame.K_1, pygame.K_KP1):
                    self._activate_overlay_button(1)
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    self._activate_overlay_button(2)

    def _spawn_powerup(self) -> None:
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

    def _start_game(self) -> None:
        """Startet das Spiel"""
        self._ensure_selected_map_for_mode()
        self.reset_game(self.game_mode, self.selected_map)
        self.game_state = GameState.PLAYING

    def _toggle_fullscreen(self) -> None:
        """Schaltet Vollbild an/aus."""
        if not self.fullscreen:
            self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT), pygame.FULLSCREEN)
            self.fullscreen = True
        else:
            self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
            self.fullscreen = False
            pygame.display.flip()

    def _touch_to_screen(self, event) -> tuple[int, int]:
        """Wandelt Pygame-Touch-Koordinaten in Bildschirm-Pixel um."""
        return (int(event.x * Config.WIDTH), int(event.y * Config.HEIGHT))

    def _activate_main_menu_index(self, index: int) -> None:
        """Startet die gewählte Spielmodus-Karte und wechselt zur Map-/Missionsauswahl."""
        modes = [GameMode.FFA, GameMode.HORDE, GameMode.MISSIONS]
        self.main_menu_index = max(0, min(index, len(modes) - 1))
        self.game_mode = modes[self.main_menu_index]
        self._ensure_selected_map_for_mode()
        self.game_state = GameState.LEVEL_SELECT

    def _show_ffa_info(self) -> None:
        """Zeigt FFA-Info (non-blocking)"""
        font = pygame.font.SysFont(None, 36)
        text = font.render("FFA Mode: 2 Players + 6-7 AI Enemies", True, Config.COLOR_TEXT)
        self.screen.blit(text, (Config.WIDTH//2 - 150, Config.HEIGHT//2 + 50))
        pygame.display.flip()

    def _show_horde_info(self) -> None:
        """Zeigt Horde-Info (non-blocking)"""
        font = pygame.font.SysFont(None, 36)
        text = font.render("Horde Mode: Wave-based, 10 Waves", True, Config.COLOR_TEXT)
        self.screen.blit(text, (Config.WIDTH//2 - 150, Config.HEIGHT//2 + 50))
        pygame.display.flip()

    def _show_coop_info(self) -> None:
        """Zeigt Coop-Info (non-blocking)"""
        font = pygame.font.SysFont(None, 36)
        text = font.render("Coop Mode: 2 Players + AI Enemies", True, Config.COLOR_TEXT)
        self.screen.blit(text, (Config.WIDTH//2 - 150, Config.HEIGHT//2 + 50))
        pygame.display.flip()

    def _player_from_owner(self, owner):
        """Gibt Player-Objekt für Bullet-Owner wie 'player1' zurück."""
        if not isinstance(owner, str) or not owner.startswith("player"):
            return None
        try:
            player_id = int(owner.replace("player", ""))
        except ValueError:
            return None
        return next((p for p in self.players if p.player_id == player_id), None)

    def _award_score(self, owner, amount) -> None:
        """Vergibt Score sauber playerbezogen und hält Legacy-Dict synchron."""
        player = self._player_from_owner(owner)
        if not player:
            return
        player.score += amount
        self.score[player.player_id] = player.score

    def _award_wave_bonus(self) -> None:
        """Wellenbonus fair auf aktive Spieler aufteilen."""
        if not self.players:
            return
        share = max(1, Config.WAVE_SCORE // len(self.players))
        for player in self.players:
            player.score += share
            self.score[player.player_id] = player.score

    def _score_summary(self) -> str:
        if not self.players:
            return "Final Score: 0"
        return "  |  ".join(f"P{p.player_id}: {p.score}" for p in self.players)

    def update(self) -> None:
        """Update Game-Logik"""
        if self.game_state != GameState.PLAYING:
            return

        # Musik-Ducking aktualisieren
        self.sound_manager._update_music_ducking()

        keys = pygame.key.get_pressed()

        # Time Limit
        self.game_time += 1
        if self.mission_intro_frames > 0:
            self.mission_intro_frames -= 1
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
            if e.game is None:
                e.game = self
            new_bullet = e.update_ai(self.players, self.walls, eagle_pos)
            if new_bullet:
                self.bullets.append(new_bullet)

        # Modus-spezifische Siegbedingungen.
        if self.game_mode == GameMode.FFA:
            alive_teams = {p.team_id for p in self.players if p.lives > 0}
            alive_teams.update(e.team_id for e in self.enemies)
            player_teams = {p.team_id for p in self.players if p.lives > 0}
            if len(alive_teams) <= 1:
                self.game_state = GameState.VICTORY if alive_teams & player_teams else GameState.GAME_OVER
                return
        elif (self.game_mode == GameMode.MISSIONS and not self.enemies and self.players) or (not self.wave_manager and not self.enemies and self.players):
            self.game_state = GameState.VICTORY
            return

        # Update Wave Manager (Horde Mode)
        if self.wave_manager:
            self.wave_manager.update(self.enemies, self.players, self.walls, self.eagle, self)
            for enemy in self.enemies:
                if enemy.game is None:
                    enemy.game = self

            # Check for wave completion
            if self.wave_manager.wave_complete:
                if self.wave_manager.current_wave >= self.wave_manager.total_waves:
                    self.game_state = GameState.VICTORY
                    return
                self.wave_manager.next_wave()
                self._award_wave_bonus()
                self.screen_shake = 10
                # Boss-Welle Mission
                if self.wave_manager.is_boss_wave:
                    self.mission = "Boss Wave - Defend Eagle!"

        # Update Particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

        # Update Powerups
        for powerup in self.powerups[:]:
            powerup.update()

        # Screen Shake dekrementieren
        if self.screen_shake > 0:
            self.screen_shake = max(0, self.screen_shake - 1)

        # Update Bullets
        for b in self.bullets[:]:
            result = b.update(self.walls)

            if result == "hit_wall" or result == "out_of_bounds":
                self.bullets.remove(b)
            elif isinstance(result, Wall):
                # Nur Player-Bullets geben Score für Block-Zerstörung
                if result.destructible and b.owner in ["player1", "player2"]:
                    self._award_score(b.owner, Config.BRICK_SCORE)
                    self.screen_shake = 5
                    self._create_small_explosion(result.rect.center)
                    self.sound_manager.play_brick_destroy()
                if result.destructible:
                    self.walls.remove(result)
                self.bullets.remove(b)
                continue
            # Check collision with entities
            self._check_bullet_collision(b)

        # Regelmäßig wenige Powerups nachspawnen, ohne das Feld zu überladen.
        self.powerup_spawn_timer += 1
        if self.powerup_spawn_timer >= 10 * Config.FPS:
            self.powerup_spawn_timer = 0
            if len(self.powerups) < 3 and random.random() < Config.POWERUP_SPAWN_CHANCE:
                self._spawn_powerup()

        # Check Powerup collision with players
        for player in self.players:
            for powerup in self.powerups[:]:
                if player.rect.colliderect(powerup.hitbox):
                    # Apply powerup effect
                    if powerup.powerup_type == Powerup.SHIELD:
                        player.shield_charges = Config.SHIELD_MAX_CHARGES
                        self.screen_shake = 5
                    elif powerup.powerup_type == Powerup.DOUBLE_SHOT:
                        player.double_shot_active = True
                        player.double_shot_timer = Config.DOUBLE_SHOOT_DURATION * 60  # In Frames
                        self.screen_shake = 5
                    elif powerup.powerup_type == Powerup.REPAIR:
                        player.health = min(player.health + Config.REPAIR_AMOUNT, Config.MAX_LIVES * 2)
                        self.screen_shake = 5
                    if powerup in self.powerups:
                        self.powerups.remove(powerup)
                    self.sound_manager.play_powerup()
                    break

    def _check_bullet_collision(self, bullet) -> None:
        """Checkt Kollision von Bullet mit Entitäten"""
        if bullet not in self.bullets:
            return

        # Check eagle collision (nur Enemy-Bullets zerstören die Basis)
        if self.eagle and bullet.owner == "enemy" and self.eagle.state == EagleState.PROTECTED and bullet.rect.colliderect(self.eagle.rect):
            self.eagle.state = EagleState.HIT
            self.screen_shake = 20
            self._create_explosion(bullet.rect.center)
            self.game_state = GameState.GAME_OVER
            self.bullets.remove(bullet)
            return

        # Check player collision (Team-Schutz für Co-op und FFA-Teams)
        for player in self.players:
            if bullet.rect.colliderect(player.rect):
                friendly = (bullet.owner == f"player{player.player_id}" or
                            (bullet.team_id is not None and bullet.team_id == player.team_id))
                if friendly:
                    continue
                if player.health > 0:
                    if player.take_damage(1):
                        self.screen_shake = 5
                        self._create_small_explosion(bullet.rect.center)
                        if player.health <= 0:
                            player.lives -= 1
                            if player.lives <= 0:
                                self.game_state = GameState.GAME_OVER
                                self.sound_manager.play_lose()
                            else:
                                # Respawn player mit Unverwundbarkeit
                                free_pos = self._find_free_positions(self.walls, 1, 50)
                                if free_pos:
                                    px, py = free_pos[0]
                                else:
                                    px, py = 80, 80  # Fallback
                                player.rect.x = px
                                player.rect.y = py
                                player.health = Config.MAX_LIVES * 2
                                player.respawn_timer = Config.RESPAWN_COOLDOWN * 60  # In Frames
                                player.invulnerable = True
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                break

        if bullet not in self.bullets:
            return

        # Check enemy collision (in FFA können KI-Panzer sich gegenseitig bekämpfen)
        for e in list(self.enemies):
            if bullet.rect.colliderect(e.rect):
                friendly = (bullet.source is e or (bullet.team_id is not None and bullet.team_id == e.team_id))
                if friendly:
                    continue
                if bullet.owner in ["player1", "player2", "enemy"]:
                    if e.take_damage():
                        if e in self.enemies:
                            self.enemies.remove(e)
                        if bullet.owner in ["player1", "player2"]:
                            self._award_score(bullet.owner, e.score)
                        self.screen_shake = 10
                        self._create_explosion(e.rect.center)
                        self.sound_manager.play_tank_explosion()
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                break

    def _create_particles(self, position, color, count, particle_type="normal") -> None:
        """Erstellt Partikel mit Feuer, Rauch und Funken"""
        multiplier = Config.PARTICLE_COUNT_MULTIPLIER
        actual_count = count * multiplier

        for _ in range(actual_count):
            angle = random.uniform(0, 2 * math.pi)
            if particle_type == "explosion":
                speed = random.uniform(1, 8)
                size = random.uniform(2, 6)
            elif particle_type == "smoke":
                speed = random.uniform(0.5, 3)
                size = random.uniform(3, 8)
            elif particle_type == "sparks":
                speed = random.uniform(3, 10)
                size = random.uniform(1, 3)
            else:
                speed = random.uniform(2, 6)
                size = 2

            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            if particle_type == "explosion":
                fire_color = random.choice(Config.COLOR_FIRE)
                self.particles.append(Particle(
                    position[0] + random.uniform(-5, 5),
                    position[1] + random.uniform(-5, 5),
                    fire_color, vx, vy,
                    random.randint(25, 50),
                    size=int(size),
                    particle_type="fire"
                ))
            elif particle_type == "smoke":
                smoke_color = random.choice(Config.COLOR_SMOKE)
                self.particles.append(Particle(
                    position[0] + random.uniform(-8, 8),
                    position[1] + random.uniform(-8, 8),
                    smoke_color, vx * 0.5, vy * 0.5,
                    random.randint(40, 80),
                    size=int(size),
                    particle_type="smoke"
                ))
            elif particle_type == "sparks":
                spark_color = random.choice(Config.COLOR_SPARK)
                self.particles.append(Particle(
                    position[0], position[1],
                    spark_color, vx, vy,
                    random.randint(15, 35),
                    size=int(size),
                    particle_type="spark"
                ))
            else:
                self.particles.append(Particle(
                    position[0] + random.uniform(-3, 3),
                    position[1] + random.uniform(-3, 3),
                    color, vx, vy,
                    random.randint(20, 40),
                    size=int(size),
                    particle_type="normal"
                ))

    def _create_explosion(self, position) -> None:
        """Vollständige Explosion mit Feuer, Rauch und Funken"""
        self._create_particles(position, Config.COLOR_FIRE[0], 15, "explosion")
        self._create_particles(position, Config.COLOR_SMOKE[0], 10, "smoke")
        self._create_particles(position, Config.COLOR_SPARK[0], 12, "sparks")

    def _create_small_explosion(self, position) -> None:
        """Kleinere Explosion für Wand-Zerstörung"""
        self._create_particles(position, Config.COLOR_BRICK, 8, "explosion")
        self._create_particles(position, Config.COLOR_SMOKE[0], 5, "smoke")

    def draw(self) -> None:
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

    def _draw_rect(self, x, y, width, height, color, border=2, border_color=(100, 100, 150)) -> None:
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

    def _fit_font(self, text, max_width, max_height, font_size=32, bold=False, min_size=16):
        """Gibt eine Font-Größe zurück, die sicher in den Zielbereich passt."""
        for size in range(font_size, min_size - 1, -1):
            font = pygame.font.SysFont(None, size, bold=bold)
            rendered = font.render(text, True, (255, 255, 255))
            if rendered.get_width() <= max_width and rendered.get_height() <= max_height:
                return font
        return pygame.font.SysFont(None, min_size, bold=bold)

    def _draw_text_in_rect(self, text, rect, font_size=32, color=(255, 255, 255), bold=False,
                           align="center", valign="center", shadow=True, min_size=16):
        """Zeichnet Text in einem Rechteck, verkleinert ihn bei Bedarf und verhindert Überlappung."""
        rect = pygame.Rect(rect)
        font = self._fit_font(text, rect.width, rect.height, font_size, bold, min_size)
        rendered = font.render(text, True, color)
        if align == "left":
            x = rect.x
        elif align == "right":
            x = rect.right - rendered.get_width()
        else:
            x = rect.centerx - rendered.get_width() // 2

        if valign == "top":
            y = rect.y
        elif valign == "bottom":
            y = rect.bottom - rendered.get_height()
        else:
            y = rect.centery - rendered.get_height() // 2

        if shadow:
            shadow_surf = font.render(text, True, (0, 0, 0))
            self.screen.blit(shadow_surf, (x + 2, y + 2))
        self.screen.blit(rendered, (x, y))
        return rendered.get_rect(topleft=(x, y))

    def _draw_gradient_background(self, tick, base=(8, 12, 26), accent=(28, 36, 70)) -> None:
        """Ruhiger Menü-Hintergrund mit guter Lesbarkeit."""
        for i in range(0, Config.HEIGHT, 2):
            t = i / max(1, Config.HEIGHT)
            wave = 0.5 + 0.5 * math.sin(tick * 0.35 + i / 140)
            r = int(base[0] * (1 - t) + accent[0] * t + 8 * wave)
            g = int(base[1] * (1 - t) + accent[1] * t + 8 * wave)
            b = int(base[2] * (1 - t) + accent[2] * t + 12 * wave)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (Config.WIDTH, i))

        for i in range(42):
            px = (int(tick * (16 + i % 5)) + i * 151) % Config.WIDTH
            py = (int(tick * (10 + i % 4)) + i * 97) % Config.HEIGHT
            color = (70, 85, 145) if i % 3 else (115, 105, 55)
            pygame.draw.circle(self.screen, color, (px, py), 2)

    def _draw_card_button(self, rect, title, subtitle, key, color, selected=False, hovered=False) -> None:
        """Einheitlicher, großer Button für Maus, Touch und Tastatur-Fokus."""
        rect = pygame.Rect(rect)
        bg = (36, 41, 66) if hovered else (24, 29, 50)
        if selected:
            bg = (48, 45, 32)
        pygame.draw.rect(self.screen, bg, rect, border_radius=14)
        border = color if (selected or hovered) else (82, 91, 132)
        pygame.draw.rect(self.screen, border, rect, 4 if selected else 2, border_radius=14)

        key_rect = pygame.Rect(rect.x + 16, rect.y + 15, 54, rect.height - 30)
        pygame.draw.rect(self.screen, (9, 12, 24), key_rect, border_radius=10)
        pygame.draw.rect(self.screen, color, key_rect, 2, border_radius=10)
        self._draw_text_in_rect(str(key), key_rect.inflate(-8, -8), font_size=30, color=color, bold=True, shadow=False)

        self._draw_text_in_rect(title, (rect.x + 86, rect.y + 12, rect.width - 110, 32),
                                font_size=31, color=(255, 255, 255), bold=True, align="left", shadow=True)
        self._draw_text_in_rect(subtitle, (rect.x + 86, rect.y + 47, rect.width - 110, 24),
                                font_size=22, color=(176, 184, 218), align="left", shadow=False)

    def _main_menu_layout(self):
        box_width = 820
        box_height = 720
        box_x = Config.WIDTH // 2 - box_width // 2
        box_y = Config.HEIGHT // 2 - box_height // 2 - 20
        btn_width = 660
        btn_height = 78
        btn_x = Config.WIDTH // 2 - btn_width // 2
        btn_y = box_y + 205
        buttons = [pygame.Rect(btn_x, btn_y + i * 92, btn_width, btn_height) for i in range(3)]
        toggle_y = btn_y + 3 * 92 + 22
        coop_rect = pygame.Rect(btn_x, toggle_y, 315, 66)
        difficulty_rect = pygame.Rect(btn_x + 345, toggle_y, 315, 66)
        return pygame.Rect(box_x, box_y, box_width, box_height), buttons, coop_rect, difficulty_rect

    def _level_select_layout(self):
        """Zentrale Layoutdaten für Level-Select, damit Zeichnen und Klickflächen synchron sind."""
        box_width = 1120
        box_height = 690
        box_x = Config.WIDTH // 2 - box_width // 2
        box_y = Config.HEIGHT // 2 - box_height // 2 - 10
        preview_rect = pygame.Rect(box_x + 62, box_y + 158, 400, 260)
        cards = []
        card_w, card_h = 260, 82
        start_x = box_x + 520
        start_y = box_y + 158
        self._ensure_selected_map_for_mode()
        for i, map_key in enumerate(self._selectable_map_keys()):
            col = i % 2
            row = i // 2
            rect = pygame.Rect(start_x + col * 292, start_y + row * 104, card_w, card_h)
            cards.append((map_key, rect))
        start_rect = pygame.Rect(Config.WIDTH // 2 - 240, box_y + box_height - 86, 480, 62)
        return box_x, box_y, box_width, box_height, preview_rect, cards, start_rect

    def _overlay_buttons_for_state(self):
        if self.game_state == GameState.PAUSED:
            return [
                ("Weiter spielen", "ESC / P", (80, 235, 120)),
                ("Mission neu starten", "R", (255, 215, 80)),
                ("Zum Hauptmenü", "Q", (255, 105, 105)),
            ]
        if self.game_state == GameState.GAME_OVER:
            return [
                ("Zum Hauptmenü", "Enter", (210, 215, 230)),
                ("Mission neu starten", "1", (80, 235, 120)),
                ("Modus wechseln", "2", (255, 175, 80)),
            ]
        if self.game_state == GameState.VICTORY:
            if self.game_mode == GameMode.MISSIONS and self.selected_map != Config.MISSION_ORDER[-1]:
                return [
                    ("Zum Hauptmenü", "Enter", (210, 215, 230)),
                    ("Nächste Mission", "1", (80, 235, 120)),
                    ("Mission wiederholen", "2", (255, 175, 80)),
                ]
            return [
                ("Zum Hauptmenü", "Enter", (210, 215, 230)),
                ("Noch einmal spielen", "1", (80, 235, 120)),
                ("Nächster Modus", "2", (255, 175, 80)),
            ]
        return []

    def _overlay_layout(self, buttons=None):
        buttons = buttons if buttons is not None else self._overlay_buttons_for_state()
        box_width = 660
        box_height = 470 if buttons else 340
        box_x = Config.WIDTH // 2 - box_width // 2
        box_y = Config.HEIGHT // 2 - box_height // 2
        button_rects = []
        btn_width = 440
        btn_height = 58
        btn_x = Config.WIDTH // 2 - btn_width // 2
        btn_y = box_y + box_height - 220
        for i in range(len(buttons)):
            button_rects.append(pygame.Rect(btn_x, btn_y + i * 72, btn_width, btn_height))
        return pygame.Rect(box_x, box_y, box_width, box_height), button_rects

    def _activate_overlay_button(self, index: int) -> None:
        buttons = self._overlay_buttons_for_state()
        if not buttons:
            return
        index = max(0, min(index, len(buttons) - 1))
        self.overlay_button_index = index

        if self.game_state == GameState.PAUSED:
            if index == 0:
                self.game_state = GameState.PLAYING
            elif index == 1:
                self.reset_game(self.game_mode, self.selected_map)
                self.game_state = GameState.PLAYING
            elif index == 2:
                self.game_state = GameState.MAIN_MENU
            return

        if self.game_state in (GameState.GAME_OVER, GameState.VICTORY):
            if index == 0:
                self.game_state = GameState.MAIN_MENU
            elif index == 1:
                if self.game_state == GameState.VICTORY and self.game_mode == GameMode.MISSIONS and self.selected_map != Config.MISSION_ORDER[-1]:
                    self.selected_map = Config.MISSION_ORDER[Config.MISSION_ORDER.index(self.selected_map) + 1]
                self.reset_game(self.game_mode, self.selected_map)
                self.game_state = GameState.PLAYING
            elif index == 2:
                if self.game_state == GameState.VICTORY and self.game_mode == GameMode.MISSIONS and self.selected_map != Config.MISSION_ORDER[-1]:
                    self.reset_game(self.game_mode, self.selected_map)
                else:
                    modes = [GameMode.FFA, GameMode.HORDE, GameMode.MISSIONS]
                    self.game_mode = modes[(modes.index(self.game_mode) + 1) % len(modes)]
                    self._ensure_selected_map_for_mode()
                    self.reset_game(self.game_mode, self.selected_map)
                self.game_state = GameState.PLAYING

    def _handle_overlay_click(self, pos) -> None:
        """Behandelt Maus- und Touch-Klicks in Overlay-Menüs."""
        for i, btn_rect in enumerate(self._overlay_layout()[1]):
            if btn_rect.collidepoint(pos):
                self._activate_overlay_button(i)
                return

    def _handle_menu_mouse_click(self, pos) -> None:
        """Behandelt Maus- und Touch-Klicks im Hauptmenü und in der Levelauswahl."""
        if self.game_state == GameState.MAIN_MENU:
            _, buttons, coop_rect, difficulty_rect = self._main_menu_layout()
            for i, btn_rect in enumerate(buttons):
                if btn_rect.collidepoint(pos):
                    self._activate_main_menu_index(i)
                    return
            if coop_rect.collidepoint(pos):
                self.coop_enabled = not self.coop_enabled
                return
            if difficulty_rect.collidepoint(pos):
                self._cycle_difficulty()
                return

        elif self.game_state == GameState.LEVEL_SELECT:
            _, _, _, _, _, cards, start_rect = self._level_select_layout()
            for map_key, btn_rect in cards:
                if btn_rect.collidepoint(pos):
                    self.selected_map = map_key
                    self._start_game()
                    return
            if start_rect.collidepoint(pos):
                self._start_game()
                return

    def _handle_menu_pointer_motion(self, pos) -> None:
        """Aktualisiert Fokus/Hover für Maus- und Touch-Bewegungen."""
        if self.game_state == GameState.MAIN_MENU:
            _, buttons, _, _ = self._main_menu_layout()
            for i, rect in enumerate(buttons):
                if rect.collidepoint(pos):
                    self.main_menu_index = i
                    return
        elif self.game_state == GameState.LEVEL_SELECT:
            self._handle_level_select_mouse_motion(pos)

    def _handle_overlay_mouse_motion(self, pos) -> None:
        """Aktualisiert den Tastatur-Fokus passend zum Maus-/Touch-Hover."""
        for i, rect in enumerate(self._overlay_layout()[1]):
            if rect.collidepoint(pos):
                self.overlay_button_index = i
                return

    def _handle_level_select_mouse_motion(self, pos) -> None:
        """Aktualisiert selected_map beim Überfahren der Map-Buttons mit Maus oder Touch."""
        for map_key, btn_rect in self._level_select_layout()[5]:
            if btn_rect.collidepoint(pos):
                self.selected_map = map_key
                return

    def _draw_main_menu(self) -> None:
        """Hauptmenü nach UI-Best-Practices: klare Hierarchie, großer Fokus, keine Textüberlappung."""
        tick = pygame.time.get_ticks() / 1000
        mouse_pos = pygame.mouse.get_pos()
        panel_rect, buttons_rects, coop_rect, difficulty_rect = self._main_menu_layout()
        self._draw_gradient_background(tick)

        glow = pygame.Surface((panel_rect.width + 44, panel_rect.height + 44), pygame.SRCALPHA)
        pygame.draw.rect(glow, (85, 105, 210, 55), glow.get_rect(), border_radius=24)
        self.screen.blit(glow, (panel_rect.x - 22, panel_rect.y - 22))
        pygame.draw.rect(self.screen, (16, 20, 38), panel_rect, border_radius=18)
        pygame.draw.rect(self.screen, (110, 126, 205), panel_rect, 3, border_radius=18)

        self._draw_text_in_rect("PYTANK", (panel_rect.x + 40, panel_rect.y + 34, panel_rect.width - 80, 90),
                                font_size=104, color=(255, 220, 45), bold=True)
        self._draw_text_in_rect("Tank Battle Arena", (panel_rect.x + 40, panel_rect.y + 124, panel_rect.width - 80, 36),
                                font_size=34, color=(178, 188, 232), bold=True, shadow=False)
        self._draw_text_in_rect("Spielmodus wählen", (panel_rect.x + 40, panel_rect.y + 174, panel_rect.width - 80, 32),
                                font_size=29, color=(235, 238, 255), bold=True, shadow=False)

        mode_buttons = [
            ("Free For All", "Solo: jeder gegen jeden  •  Co-op: 2er-Teams", "1", (70, 240, 120)),
            ("Horde", "Wellen überleben - solo oder gemeinsam", "2", (255, 176, 55)),
            ("Missionen", "3 Comic-Tutorial-Quests mit eigenen Maps", "3", (75, 205, 255)),
        ]
        for i, (title, subtitle, key, color) in enumerate(mode_buttons):
            rect = buttons_rects[i]
            self._draw_card_button(rect, title, subtitle, key, color,
                                   selected=(i == self.main_menu_index), hovered=rect.collidepoint(mouse_pos))

        # Co-op und Schwierigkeit sind bewusste Add-ons, keine eigenen Spielmodi.
        coop_color = (80, 235, 120) if self.coop_enabled else (170, 180, 210)
        self._draw_card_button(coop_rect, "Co-op Add-on", self._coop_label(), "C", coop_color,
                               selected=self.coop_enabled, hovered=coop_rect.collidepoint(mouse_pos))
        diff_subtitle = "Missionen nutzen Story-Schwierigkeit" if self.main_menu_index == 2 else Difficulty.LABELS[self.difficulty]
        self._draw_card_button(difficulty_rect, "KI-Schwierigkeit", diff_subtitle, "D", (255, 210, 85),
                               selected=False, hovered=difficulty_rect.collidepoint(mouse_pos))

        hint_rect = pygame.Rect(panel_rect.x + 50, panel_rect.bottom - 76, panel_rect.width - 100, 46)
        self._draw_text_in_rect("↑/↓ Modus  •  C Co-op  •  D Leicht/Mittel/Schwer/Mixed  •  Enter startet Auswahl",
                                hint_rect, font_size=23, color=(168, 176, 214), shadow=False)

        footer_font = pygame.font.SysFont(None, 20)
        footer = footer_font.render("F = Vollbild", True, (112, 122, 164))
        self.screen.blit(footer, (Config.WIDTH // 2 - footer.get_width() // 2, panel_rect.bottom + 22))

    def _draw_level_select(self) -> None:
        """Map-Auswahl mit großen Touch-Zielen, Tastatur-Fokus und überlappungsfreien Texten."""
        tick = pygame.time.get_ticks() / 1000
        mouse_pos = pygame.mouse.get_pos()
        box_x, box_y, box_width, box_height, preview_rect, cards, start_rect = self._level_select_layout()
        panel_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        self._draw_gradient_background(tick, base=(7, 10, 25), accent=(24, 42, 76))

        glow = pygame.Surface((box_width + 44, box_height + 44), pygame.SRCALPHA)
        pygame.draw.rect(glow, (90, 115, 230, 55), glow.get_rect(), border_radius=24)
        self.screen.blit(glow, (box_x - 22, box_y - 22))
        pygame.draw.rect(self.screen, (15, 18, 34), panel_rect, border_radius=18)
        pygame.draw.rect(self.screen, (105, 125, 205), panel_rect, 3, border_radius=18)

        title = "MISSION AUSWÄHLEN" if self.game_mode == GameMode.MISSIONS else "MAP AUSWÄHLEN"
        self._draw_text_in_rect(title, (box_x + 50, box_y + 30, box_width - 100, 60),
                                font_size=58, bold=True, color=(255, 220, 55))
        diff_label = "Story" if self.game_mode == GameMode.MISSIONS else Difficulty.LABELS[self.difficulty]
        header = f"{self._mode_label()}  •  {self._coop_label()}  •  Schwierigkeit: {diff_label}  •  C/D umschalten  •  ESC zurück"
        self._draw_text_in_rect(header,
                                (box_x + 50, box_y + 92, box_width - 100, 32),
                                font_size=24, color=(168, 178, 224), shadow=False)

        preview_panel = preview_rect.inflate(24, 118)
        pygame.draw.rect(self.screen, (9, 12, 24), preview_panel, border_radius=14)
        pygame.draw.rect(self.screen, (74, 88, 140), preview_panel, 2, border_radius=14)
        self._draw_text_in_rect("Taktische Vorschau", (preview_panel.x + 18, preview_panel.y + 14, preview_panel.width - 36, 28),
                                font_size=24, color=(180, 190, 235), bold=True, shadow=False)

        preview_grid_w = 32
        preview_grid_h = 20
        cell_w = max(1, preview_rect.width // preview_grid_w)
        cell_h = max(1, preview_rect.height // preview_grid_h)
        map_keys = self._selectable_map_keys()
        map_idx = map_keys.index(self.selected_map)
        map_conf = Config.MAPS[self.selected_map]
        accent = map_conf.get("color", (255, 215, 0))
        for py in range(preview_grid_h):
            for px in range(preview_grid_w):
                border = px in (0, preview_grid_w - 1) or py in (0, preview_grid_h - 1)
                lane = px in (preview_grid_w // 4, preview_grid_w // 2, 3 * preview_grid_w // 4) or py in (preview_grid_h // 4, preview_grid_h // 2, 3 * preview_grid_h // 4)
                seed = (px * 17 + py * 31 + map_idx * 53) % 100
                if border:
                    cell_color = Config.COLOR_STEEL
                elif self.selected_map == "arena":
                    cell_color = Config.COLOR_STEEL if seed < 14 and not lane else (25, 30, 44)
                elif self.selected_map == "crossfire":
                    centerish = abs(px - preview_grid_w // 2) < 4 and abs(py - preview_grid_h // 2) < 4
                    cell_color = Config.COLOR_STEEL if centerish and not lane else (25, 30, 44)
                elif self.selected_map == "islands":
                    cell_color = Config.COLOR_BRICK if seed < 28 and not lane else (25, 30, 44)
                elif self.selected_map == "industrial":
                    cell_color = Config.COLOR_STEEL if seed < 45 and not lane else (25, 30, 44)
                elif self.selected_map == "desert":
                    cell_color = Config.COLOR_BRICK if seed < 58 and not lane else (32, 26, 18)
                else:
                    cell_color = Config.COLOR_BRICK if seed < 36 and not lane else (25, 30, 44)
                pygame.draw.rect(self.screen, cell_color,
                                 (preview_rect.x + px * cell_w, preview_rect.y + py * cell_h, cell_w, cell_h))

        pygame.draw.rect(self.screen, accent, preview_rect, 4, border_radius=6)
        self._draw_text_in_rect(map_conf["name"], (preview_panel.x + 22, preview_rect.bottom + 18, preview_panel.width - 44, 34),
                                font_size=32, color=accent, bold=True, align="left")
        self._draw_text_in_rect(map_conf.get("desc", ""), (preview_panel.x + 22, preview_rect.bottom + 54, preview_panel.width - 44, 28),
                                font_size=23, color=(205, 210, 236), align="left", shadow=False)

        for i, (map_key, rect) in enumerate(cards):
            conf = Config.MAPS[map_key]
            color = conf.get("color", (180, 180, 220))
            selected = map_key == self.selected_map
            hovered = rect.collidepoint(mouse_pos)
            self._draw_card_button(rect, conf["name"], conf.get("desc", ""), str(i + 1), color,
                                   selected=selected, hovered=hovered)

        start_hover = start_rect.collidepoint(mouse_pos)
        start_color = (255, 226, 65)
        pygame.draw.rect(self.screen, (72, 64, 22) if start_hover else (43, 39, 18), start_rect, border_radius=14)
        pygame.draw.rect(self.screen, start_color, start_rect, 4, border_radius=14)
        start_text = "MISSION STARTEN" if self.game_mode == GameMode.MISSIONS else "SPIEL STARTEN"
        self._draw_text_in_rect(start_text, start_rect.inflate(-28, -10), font_size=34,
                                color=(255, 255, 255), bold=True)

        footer_font = pygame.font.SysFont(None, 20)
        footer = footer_font.render("F = Vollbild  •  Hover zeigt Vorschau  •  Klick/Tap bestätigt  •  C = Co-op", True, (118, 128, 170))
        self.screen.blit(footer, (Config.WIDTH // 2 - footer.get_width() // 2, box_y + box_height + 24))

    def _draw_game(self) -> None:
        """Zeichnet Gameplay"""
        # Hintergrund zeichnen
        self.background.draw(self.screen)

        # Draw Eagle
        if self.eagle:
            self.eagle.draw_adler(self.screen)

        # Draw Walls
        for wall in self.walls:
            wall.draw(self.screen)

        # Draw Players
        for player in self.players:
            player.draw(self.screen)

        # Draw Enemies
        for e in self.enemies:
            e.draw(self.screen)
            e.draw_health_bar(self.screen)

        # Draw Powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # Draw Bullets
        for b in self.bullets:
            b.draw_with_trail(self.screen)

        # Draw Particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw UI
        self._draw_ui()

        if self.game_mode == GameMode.MISSIONS and self.mission_intro_frames > 0:
            self._draw_mission_story_panel()

    def _draw_mission_story_panel(self) -> None:
        """Comic-artige Textbox für Missionsbriefings (Text, kein Ton)."""
        panel = pygame.Rect(170, Config.HEIGHT - 245, Config.WIDTH - 340, 155)
        shadow = panel.move(6, 6)
        pygame.draw.rect(self.screen, (0, 0, 0), shadow, border_radius=18)
        pygame.draw.rect(self.screen, (248, 238, 200), panel, border_radius=18)
        pygame.draw.rect(self.screen, (35, 28, 22), panel, 4, border_radius=18)

        # Kleines Commander-Portrait im 2D-Comic-Stil.
        portrait = pygame.Rect(panel.x + 22, panel.y + 24, 96, 96)
        pygame.draw.rect(self.screen, (65, 75, 95), portrait, border_radius=12)
        pygame.draw.rect(self.screen, (35, 28, 22), portrait, 3, border_radius=12)
        pygame.draw.circle(self.screen, (255, 220, 120), portrait.center, 30)
        pygame.draw.rect(self.screen, (85, 120, 190), (portrait.x + 24, portrait.y + 62, 48, 30), border_radius=8)
        pygame.draw.line(self.screen, (35, 28, 22), (portrait.x + 30, portrait.y + 42), (portrait.x + 66, portrait.y + 42), 3)

        font = pygame.font.SysFont(None, 28, bold=True)
        text_color = (35, 28, 22)
        words = self.mission_intro_text.split()
        lines = []
        current = ""
        max_width = panel.width - 160
        for word in words:
            candidate = f"{current} {word}".strip()
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)

        y = panel.y + 22
        for line in lines[:4]:
            rendered = font.render(line, True, text_color)
            self.screen.blit(rendered, (panel.x + 140, y))
            y += 30

    def _draw_hud_panel(self, x, y, width, height, title=None) -> None:
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

    def _draw_ui(self) -> None:
        """Verbessertes HUD mit Panels und Lautstärkeregler"""
        tick = pygame.time.get_ticks() / 1000

        # === LINKES HUD PANEL ===
        panel_width = 220
        panel_height = 120
        panel_x = 15
        panel_y = 15

        self._draw_hud_panel(panel_x, panel_y, panel_width, panel_height, "MISSION STATUS")

        # Team-/Solo-Score-Summary
        score_y = panel_y + 35
        score_font = pygame.font.SysFont(None, 24, bold=True)
        total_score = sum(p.score for p in self.players)
        score_text = score_font.render(f"Team Score: {total_score}", True, (255, 225, 120))
        self.screen.blit(score_text, (panel_x + 15, score_y))

        # Modus / Wave
        wave_font = pygame.font.SysFont(None, 24)
        if self.wave_manager:
            wave_text = f"Wave: {self.wave_manager.current_wave}/{self.wave_manager.total_waves}"
            wave_rendered = wave_font.render(wave_text, True, Config.COLOR_P2)
            self.screen.blit(wave_rendered, (panel_x + 15, score_y + 35))
        else:
            mode_text = self.mission if self.game_mode == GameMode.MISSIONS else self._mode_label()
            mode_rendered = wave_font.render(mode_text[:24], True, Config.COLOR_P2)
            self.screen.blit(mode_rendered, (panel_x + 15, score_y + 35))

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
        player_panel_height = 125 + len(self.players) * 54

        self._draw_hud_panel(player_panel_x, player_panel_y, panel_width, player_panel_height, "PLAYER STATUS")

        # === LAUTSTÄRKESLIDER (unten rechts) ===
        self._draw_volume_sliders()

        # Spieler-Infos
        info_y = player_panel_y + 35
        for player in self.players:
            player_font = pygame.font.SysFont(None, 24, bold=True)
            p_text = player_font.render(f"P{player.player_id}", True, player.color)
            self.screen.blit(p_text, (player_panel_x + 15, info_y))

            # Lives mit Icon + playerbezogener Score
            lives_text = "♥" * player.lives
            lives_font = pygame.font.SysFont(None, 20)
            lives_rendered = lives_font.render(lives_text, True, player.color)
            self.screen.blit(lives_rendered, (player_panel_x + 70, info_y + 2))

            score_line = lives_font.render(f"Score {player.score}", True, (220, 220, 235))
            self.screen.blit(score_line, (player_panel_x + 15, info_y + 22))
            info_y += 48

            # Shield-Indikator
            if player.shield_charges > 0:
                shield_text = f"🛡️ Shield: {player.shield_charges}"
                shield_font = pygame.font.SysFont(None, 20)
                shield_rendered = shield_font.render(shield_text, True, (0, 255, 255))
                self.screen.blit(shield_rendered, (player_panel_x + 15, info_y))
                info_y += 24

            # Double Shot-Indikator
            if player.double_shot_active:
                ds_pulse = int(50 * math.sin(tick * 5))
                ds_color = (min(255, 255 + ds_pulse), min(255, 255 + ds_pulse), 0)
                ds_text = "⚡ DOUBLE SHOT ACTIVE"
                ds_font = pygame.font.SysFont(None, 20, bold=True)
                ds_rendered = ds_font.render(ds_text, True, ds_color)
                self.screen.blit(ds_rendered, (player_panel_x + 15, info_y))
                info_y += 24

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
        vol_text = vol_font.render("V/C: Musik  B/N: SFX  M: Mute", True, (150, 150, 200))
        self.screen.blit(vol_text, (Config.WIDTH - vol_text.get_width() - 15, status_bar_y + 5))

        # Pause-Hinweis
        pause_font = pygame.font.SysFont(None, 18)
        pause_rendered = pause_font.render("[ESC] Pause", True, (120, 120, 160))
        self.screen.blit(pause_rendered, (Config.WIDTH - pause_rendered.get_width() - 15, status_bar_y + 12))

    def _draw_volume_sliders(self) -> None:
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

    def _handle_volume_slider_click(self, mouse_pos) -> None:
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

    def _handle_volume_slider_drag(self, mouse_pos) -> None:
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

    def _draw_overlay(self, title, subtitle=None, buttons=None) -> None:
        """Einheitliches Overlay mit klarer Fokus-Anzeige und großen Touch-Zielen."""
        tick = pygame.time.get_ticks() / 1000
        buttons = buttons if buttons is not None else self._overlay_buttons_for_state()
        if buttons:
            self.overlay_button_index %= len(buttons)

        overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        panel_rect, button_rects = self._overlay_layout(buttons)
        glow = pygame.Surface((panel_rect.width + 44, panel_rect.height + 44), pygame.SRCALPHA)
        pygame.draw.rect(glow, (100, 110, 220, 55), glow.get_rect(), border_radius=24)
        self.screen.blit(glow, (panel_rect.x - 22, panel_rect.y - 22))
        pygame.draw.rect(self.screen, (18, 22, 42), panel_rect, border_radius=18)
        pygame.draw.rect(self.screen, (112, 128, 210), panel_rect, 3, border_radius=18)

        title_color = (255, 255, 255)
        if "SIEG" in title:
            title_color = (255, 220, 55)
        elif "FEHL" in title:
            title_color = (255, 95, 95)
        self._draw_text_in_rect(title, (panel_rect.x + 46, panel_rect.y + 42, panel_rect.width - 92, 72),
                                font_size=64, color=title_color, bold=True)

        if subtitle:
            self._draw_text_in_rect(subtitle, (panel_rect.x + 58, panel_rect.y + 124, panel_rect.width - 116, 38),
                                    font_size=31, color=(214, 218, 238), bold=True, shadow=False)

        if buttons:
            mouse_pos = pygame.mouse.get_pos()
            for i, (text, key, color) in enumerate(buttons):
                rect = button_rects[i]
                selected = i == self.overlay_button_index
                hovered = rect.collidepoint(mouse_pos)
                bg = (42, 46, 70) if hovered else (25, 29, 48)
                if selected:
                    bg = (50, 48, 34)
                pygame.draw.rect(self.screen, bg, rect, border_radius=13)
                pulse = int(16 * math.sin(tick * 3.0 + i)) if selected else 0
                border = tuple(min(255, max(0, c + pulse)) for c in color) if (selected or hovered) else (80, 88, 130)
                pygame.draw.rect(self.screen, border, rect, 4 if selected else 2, border_radius=13)

                key_rect = pygame.Rect(rect.x + 15, rect.y + 11, 84, rect.height - 22)
                pygame.draw.rect(self.screen, (8, 11, 23), key_rect, border_radius=9)
                pygame.draw.rect(self.screen, color, key_rect, 2, border_radius=9)
                self._draw_text_in_rect(key, key_rect.inflate(-8, -6), font_size=22, color=color,
                                        bold=True, shadow=False)
                self._draw_text_in_rect(text, (rect.x + 116, rect.y + 10, rect.width - 136, rect.height - 20),
                                        font_size=29, color=(255, 255, 255), bold=True, align="left")

            self._draw_text_in_rect("↑/↓ wählen  •  Enter/Space bestätigen  •  Touch/Klick direkt",
                                    (panel_rect.x + 40, panel_rect.bottom - 44, panel_rect.width - 80, 26),
                                    font_size=21, color=(150, 160, 202), shadow=False)

    def _draw_paused(self) -> None:
        """Pause-Screen mit Tastatur-, Maus- und Touch-Bedienung."""
        self._draw_overlay(
            title="PAUSE",
            subtitle="Spiel ist angehalten",
            buttons=self._overlay_buttons_for_state()
        )

    def _draw_gameover(self) -> None:
        """Game-Over-Screen mit denselben zugänglichen Overlay-Controls."""
        self._draw_overlay(
            title="MISSION FEHLGESCHLAGEN",
            subtitle=self._score_summary(),
            buttons=self._overlay_buttons_for_state()
        )
        if not self._lose_played:
            self.sound_manager.play_lose()
            self._lose_played = True

    def _draw_victory(self) -> None:
        """Victory-Screen mit denselben zugänglichen Overlay-Controls."""
        subtitle = self.mission_victory_text if self.game_mode == GameMode.MISSIONS and self.mission_victory_text else self._score_summary()
        self._draw_overlay(
            title="SIEG!",
            subtitle=subtitle,
            buttons=self._overlay_buttons_for_state()
        )

        if not self._victory_played:
            self.sound_manager.play_win()
            self._victory_played = True

        for _ in range(3):
            conf_x = random.randint(0, Config.WIDTH)
            conf_y = random.randint(Config.HEIGHT // 2 - 220, Config.HEIGHT // 2)
            conf_color = random.choice([(255, 215, 0), (255, 90, 90), (80, 255, 120), (80, 150, 255)])
            pygame.draw.circle(self.screen, conf_color, (int(conf_x), int(conf_y)), random.randint(2, 5))

    def run(self) -> None:
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
def main() -> None:
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main()
