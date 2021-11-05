from genie.script.action import UpdateAction
from astroid.cast.astroid import Astroid

import random
import time

SPAWN_INTERVAL = 1.5          # seconds
LARGE_SIZE = (175, 175)
MEDIUM_SIZE = (100, 100)
SMALL_SIZE = (40, 40)

LARGE = 1
MEDIUM = 2
SMALL = 3

class SpawnAstroidsAction(UpdateAction):
    def __init__(self, priority, window_size):
        super().__init__(priority)
        self._last_spawn = time.time() # seconds
        self._window_size = window_size
        self._astroid_spawn = False

    def _create_astroid(self, type: int, x: int, y:int):
        """
            This is a helper function that creates an astroid based on
            the input "type" and the initial position
        """
        if type == LARGE:
            vel_x = -1 if x > self._window_size[0] / 2 else 1
            vel_y = 3
            return Astroid("astroid/assets/astroids/astroid_large.png", 
                            *LARGE_SIZE,
                            x = x, y = y,
                            vx = vel_x, vy = vel_y,
                            rotation_vel=1,
                            points=5, max_hp=5)
        elif type == MEDIUM:
            vel_x = -2 if x > self._window_size[0] / 2 else 2
            vel_y = 6
            return Astroid("astroid/assets/astroids/astroid_med.png",
                            *MEDIUM_SIZE, 
                            x = x, y = y,
                            vx = vel_x, vy = vel_y,
                            rotation_vel=1,
                            points=3, max_hp=3)
        elif type == SMALL:
            vel_x = -3 if x > self._window_size[0] / 2 else 3
            vel_y = 8
            return Astroid("astroid/assets/astroids/astroid_small.png",
                            *SMALL_SIZE,
                            x = x, y = y,
                            vx = vel_x, vy = vel_y,
                            rotation_vel=1,
                            points=1, max_hp=1)

    def execute(self, actors, actions, clock, callback):
        """
            - Check to see if it's time to spawn another astroid
            - Randomly pick Small, Medium, or Large
            - Pick and initial position for the astroid
            - Create the astroid by calling self._create_astroid_by_type
            - Add the astroid to the cast
            - Record the most recent spawn
        """
        if time.time() - self._last_spawn >= SPAWN_INTERVAL:
            # Pick a random type of astroid: Small, Medium, Large
            astroid_type = random.randint(1,3)

            # Generate a random position on top of the screen,
            #  limit the spawn range from 1/8 of the screen to 7/8 of the screen
            lower_x_bound = int(self._window_size[0] / 8)
            upper_x_bound = int(self._window_size[0] - lower_x_bound)

            start_pos_x = random.randint(lower_x_bound, upper_x_bound)
            start_pos_y = 0

            # spawn an astroid
            astroid = self._create_astroid(astroid_type, start_pos_x, start_pos_y)
            callback.add_actor(astroid)

            # set last_spawn to current frame
            self._last_spawn = time.time()