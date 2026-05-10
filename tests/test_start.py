import sys
import traceback
import os
import signal

# Füge das Projekt-Wurzelverzeichnis zum Python-Pfad hinzu
# Dies ist notwendig damit pytank importiert werden kann, besonders in CI-Umgebungen
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    print("1. pygame importieren...")
    import pygame
    print("   OK")
    
    print("2. pygame.init()...")
    pygame.init()
    print("   OK")
    
    print("3. pygame.mixer.init()...")
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        print("   OK")
    except pygame.error as e:
        # Audio device may not be available in headless environments (e.g., CI/CD with xvfb)
        print(f"   WARN: Mixer nicht verfügbar ({e}) - Audio deaktiviert")
        print("   (Dies ist in Headless-CI-Umgebungen erwartungsgemäß)")
    
    print("4. Config importieren...")
    from pytank import Config
    print("   OK")
    
    print("5. GameState importieren...")
    from pytank import GameState
    print("   OK")
    
    print("6. GameMode importieren...")
    from pytank import GameMode
    print("   OK")
    
    print("7. GameManager erstellen...")
    from pytank import GameManager
    game = GameManager()
    print("   OK")
    
    print("8. Kurze Initialisierungsschleife (5 Frames)...")
    # Nicht die unendliche game.run() verwenden — stattdessen nur wenige Frames
    # um sicherzustellen dass Initialisierung, Update und Draw ohne Fehler funktionieren
    for i in range(5):
        game.handle_events()
        game.update()
        game.draw()
        game.clock.tick(Config.FPS)
    print("   OK")
    
    print("9. pygame.quit()...")
    pygame.quit()
    print("   OK")
    
    print("Alle Tests erfolgreich!")
    
except Exception as e:
    print(f"Fehler: {e}")
    traceback.print_exc()
    sys.exit(1)
