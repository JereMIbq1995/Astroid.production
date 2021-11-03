import time

from genie.script.action import InputAction
from genie.services.PygameKeyboardService import PygameKeyboardService
from genie.services.PygameAudioService import PygameAudioService
from genie.services.constants import keys

from astroid.cast.ship import Ship
from astroid.cast.bullet import Bullet

VEL = 4
BULLET_VX = 0
BULLET_VY = -10
ATTACK_INTERVAL = 0.35   # seconds

class HandleShootingAction(InputAction):
    def __init__(self, priority, keyboard_service):
        super().__init__(priority)
        self._ship = None
        self._last_bullet_spawn = time.time()  # seconds
        self._keyboard_service = keyboard_service
        self._audio_service = PygameAudioService()
    
    def _spawn_bullet(self, clock, callback):
        time_since_last_shot = time.time() - self._last_bullet_spawn     #Measured in seconds
        if self._ship != None and time_since_last_shot >= ATTACK_INTERVAL:
            bullet_x = self._ship.get_x()
            bullet_y = self._ship.get_y() - (self._ship.get_height() / 2)
            
            bullet = Bullet("astroid/assets/bullet.png", 20, 30, x = bullet_x, y = bullet_y, vx = BULLET_VX, vy = BULLET_VY)
            callback.add_actor(bullet)
            self._audio_service.play_sound("astroid/assets/sound/bullet_shot.wav", 0.1)
            self._last_bullet_spawn = time.time()

    def _get_ship(self, actors):
        for actor in actors:
            if(isinstance(actor, Ship)):
                return actor
        return None

    def execute(self, actors, actions, clock, callback):        
        self._ship = self._get_ship(actors)
        if self._keyboard_service.is_key_pressed(keys.SPACE):
            self._spawn_bullet(clock, callback)