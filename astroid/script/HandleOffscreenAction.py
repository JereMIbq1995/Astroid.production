
from astroid.cast.astroid import Astroid
from astroid.cast.ship import Ship
from astroid.cast.bullet import Bullet

from genie.script.action import UpdateAction

class HandleOffscreenAction(UpdateAction):
    def __init__(self, priority,  window_size):
        super().__init__(priority)
        self._window_size = window_size
        self._ship = None
    
    def execute(self, actors, actions, clock, callback):
        """
            Handle all actors' behavior when they're about to
            go off the screen
        """
        # Look for the ship
        for actor in actors:
            if (isinstance(actor, Ship)):
                self._ship = actor
                break
        
        # Don't allow the ship to go off the screen
        if (self._ship != None):
            if self._ship.get_x() > self._window_size[0]:
                self._ship.set_x(self._window_size[0])
            if self._ship.get_x() < 0:
                self._ship.set_x(0)
            if self._ship.get_y() > self._window_size[1]:
                self._ship.set_y(self._window_size[1])
            if self._ship.get_y() < 0:
                self._ship.set_y(0)
        
        # If it's a bullet or astroid goin off the screen, just remove it.
        for actor in actors:
            if isinstance(actor, Astroid) or isinstance(actor, Bullet):
                if (actor.get_x() > self._window_size[0]
                    or actor.get_x() < 0
                    or actor.get_y() > self._window_size[1]
                    or actor.get_y() < 0):
                    callback.remove_actor(actor)