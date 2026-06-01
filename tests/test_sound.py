import math
import os
import sys

import pygame

# Füge das Projekt-Wurzelverzeichnis zum Python-Pfad hinzu
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    pygame.init()

    print("pygame.mixer.init() versuchen...")
    try:
        pygame.mixer.init(44100, -16, 2, 1024)
        print("   Mixer OK")
    except pygame.error as e:
        print(f"   WARN: Mixer nicht verfügbar ({e}) - Audio-Test überspringen")
        print("   (Dies ist in Headless-CI-Umgebungen erwartungsgemäß)")
        # Sound-Test in headless-Umgebung überspringen — das ist OK
        print("Sound-Test: Übersprungen (headless environment)")
        pygame.quit()
        sys.exit(0)

    samples = []
    for i in range(100):
        t = i/44100
        s = int(32767 * 0.15 * math.sin(2 * math.pi * 440 * t))
        samples.append(((s + 32767) * 255) // 65534)
    sound = pygame.mixer.Sound(bytes(samples))
    sound.set_volume(0.15)
    print('Sound OK, Länge:', len(samples))

except Exception as e:
    print(f"Fehler: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
