import sys
import traceback

try:
    print("1. pygame importieren...")
    import pygame
    print("   OK")
    
    print("2. pygame.init()...")
    pygame.init()
    print("   OK")
    
    print("3. pygame.mixer.init()...")
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    print("   OK")
    
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
    
    print("8. game.run() starten...")
    game.run()
    print("   OK")
    
    print("Alle Tests erfolgreich!")
    
except Exception as e:
    print(f"Fehler: {e}")
    traceback.print_exc()
    sys.exit(1)
