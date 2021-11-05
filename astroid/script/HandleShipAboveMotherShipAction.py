
from astroid.cast.astroid import Astroid
from astroid.cast.mothership import MotherShip
from astroid.cast.ship import Ship
from astroid.cast.bullet import Bullet

from genie.script.action import UpdateAction

class HandleShipAboveMotherShipAction(UpdateAction):
    def __init__(self, priority,  window_size):
        super().__init__(priority)
        self._window_size = window_size
        self._ship = None
        self._mother_ship = None
    
    def _get_ship_and_mother_ship(self, actors):
        # Look for the ship and mother ship
        self._ship = None
        self._mother_ship = None
        for actor in actors:
            if isinstance(actor, Ship):
                self._ship = actor
            if isinstance(actor, MotherShip):
                self._mother_ship = actor

    def execute(self, actors, actions, clock, callback):
        """
            Handle all actors' behavior when they're about to
            go off the screen
        """
        # Find ship and mothership among the actors
        self._get_ship_and_mother_ship(actors)

        if (self._ship != None and self._mother_ship != None):
        # Determine the line between ship an mothership:
            line = self._mother_ship.get_top_left()[1] - self._ship.get_height()/2

            # Don't allow the ship to go into the mothership
            if (self._ship != None and self._ship.get_y() > line):
                self._ship.set_y(line)
            