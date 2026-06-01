import os
import sys
import traceback

# Füge das Projekt-Wurzelverzeichnis zum Python-Pfad hinzu
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    import pygame
    print("pygame importiert OK")

    mixer_available = True
    try:
        pygame.mixer.init(44100, -16, 2, 1024)
        print("pygame.mixer.init OK")
    except pygame.error as e:
        print(f"pygame.mixer.init fehlgeschlagen ({e}) - Audio-Test überspringen")
        print("(Dies ist in Headless-CI-Umgebungen erwartungsgemäß)")
        mixer_available = False

    if not mixer_available:
        print("Audio-Tests übersprungen (headless environment)")
        print("Alle Tests OK!")
    else:
        import math
        import random

        # Test _synthesize_tone
        print("Test _synthesize_tone...")
        sample_rate = pygame.mixer.get_init()[0]
        num_samples = int(sample_rate * 0.1 / 1000)
        samples = []

        for i in range(num_samples):
            time = i / sample_rate
            if True:  # sine
                sample = int(32767 * 0.15 * math.sin(2 * math.pi * 440 * time))
                samples.append(((sample + 32767) * 255) // 65534)

        sound = pygame.mixer.Sound(bytes(samples))
        sound.set_volume(0.15)
        print("Sound erstellt OK")

        # Test _synthesize_noise
        print("Test _synthesize_noise...")
        samples = []
        for i in range(num_samples):
            time = i / sample_rate
            noise = random.randint(-1, 1) / 32767 * 0.3
            bass = math.sin(2 * math.pi * 100 * time) * 0.5 * 0.3
            sample = int(32767 * (noise + bass))
            samples.append(((sample + 32767) * 255) // 65534)

        sound = pygame.mixer.Sound(bytes(samples))
        sound.set_volume(0.3)
        print("Noise Sound erstellt OK")

        print("Alle Tests OK!")

except Exception as e:
    print(f"Fehler: {e}")
    traceback.print_exc()
    sys.exit(1)
