import pygame
import math

pygame.mixer.init(44100, -16, 2, 1024)
samples = []
for i in range(100):
    t = i/44100
    s = int(32767 * 0.15 * math.sin(2 * math.pi * 440 * t))
    samples.append(((s + 32767) * 255) // 65534)
sound = pygame.mixer.Sound(bytes(samples))
sound.set_volume(0.15)
print('Sound OK, Länge:', len(samples))
