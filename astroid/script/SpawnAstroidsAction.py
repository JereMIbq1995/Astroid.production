from genie.script.action import UpdateAction
from astroid.cast.astroid import Astroid

import random
import time

SPAWN_INTERVAL = 1.5          # seconds
LARGE_SIZE = (175, 175)
MEDIUM_SIZE = (100, 100)
SMALL_SIZE = (40, 40)

class SpawnAstroidsAction(UpdateAction):
    def __init__(self, priority, window_size):
        super().__init__(priority)
        self._last_spawn = time.time() # seconds
        self._window_size = window_size
        self._astroid_spawn = False

    def execute(self, actors, actions, clock, callback):
        #  and self._astroid_spawn == False
        if time.time() - self._last_spawn >= SPAWN_INTERVAL:

            # Generate a random position on top of the screen
            lower = int(self._window_size[0] / 8)
            higher = int(self._window_size[0] - lower)

            start_pos_y = 0
            start_pos_x = random.randint(lower, higher)

            # Generate a reasonable velocity
            vel_x = 1
            if start_pos_x > self._window_size[0] / 2:
                vel_x *= -1
            vel_y = 4

            # Pick a random type of astroid: Small, Medium, Large
            as_type = random.randint(0,3)
            image_path = ""
            size = ()
            point = 0
            hp = 0
            if as_type == 1:
                image_path = "astroid/assets/astroids/astroid_large.png"
                size = LARGE_SIZE
                points = 3
                hp = 5
            elif as_type == 2:
                image_path = "astroid/assets/astroids/astroid_med.png"
                size = MEDIUM_SIZE
                points = 2
                hp = 3
            else:
                image_path = "astroid/assets/astroids/astroid_small.png"
                size = SMALL_SIZE
                points = 1
                hp = 1


            # spawn an astroid
            astroid = Astroid(image_path, *size, x = start_pos_x, y = start_pos_y, vx = vel_x, vy = vel_y, rotation_vel=1, points=points, max_hp=hp)
            callback.add_actor(astroid)

            # set last_spawn to current frame
            self._last_spawn = time.time()