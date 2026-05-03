import sys
import traceback

try:
    import pygame
    print("pygame importiert OK")
    pygame.mixer.init(44100, -16, 2, 1024)
    print("pygame.mixer.init OK")
    
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
