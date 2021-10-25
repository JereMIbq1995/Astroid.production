import pygame

class PygameAudioService:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        pygame.mixer.init()
        self._sound_cache = {}

    def _load_sound(self, path):
        sound = pygame.mixer.Sound(path)
        if path not in self._sound_cache.keys():
            self._sound_cache[path] = sound
        
        return sound

    def play_sound(self, path):
        if path not in self._sound_cache.keys():
            self._load_sound(path).play()
        else:
            self._sound_cache[path].play()