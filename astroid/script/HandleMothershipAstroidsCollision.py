
from astroid.cast.astroid import Astroid
from astroid.cast.mothership import MotherShip

from genie.script.action import UpdateAction

class HandleMothershipAstroidsCollision(UpdateAction):
    def __init__(self, priority, physics_service, audio_service):
        self._priority = priority
        self._mother_ship = None
        self._physics_service = physics_service
        self._audio_service = audio_service               

    def execute(self, actors, actions, clock, callback):
        """
            This action handles all collisions between the SHIP and the ASTROIDS
        """
        # First look for the ship
        if (self._mother_ship == None):
            for actor in actors:
                if (isinstance(actor, MotherShip)):
                    self._mother_ship = actor

        # Only worry about collision if the ship actually exists
        if self._mother_ship != None:
            # Look through all the astroids, see if any collides with ship
            for actor in actors:
                if isinstance(actor, Astroid) and self._physics_service.check_collision(self._mother_ship, actor):
                    callback.remove_actor(actor)
                    # callback.remove_actor(actor.get_health_bar())
                    self._mother_ship.take_damage(actor.get_hp())
                    self._audio_service.play_sound("astroid/assets/sound/explosion-01.wav", 0.1)
                    if self._mother_ship.get_hp() <= 0:
                        callback.remove_actor(self._mother_ship)
                        self._mother_ship = None
                    break