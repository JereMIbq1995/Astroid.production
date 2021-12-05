
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
        self._mother_ship = actors.get_first_actor("mother_ship")

        # Only worry about collision if the mothership actually exists
        if self._mother_ship != None:
            # Look through all the astroids, see if any collides with ship
            for actor in actors.get_actors("astroids"):
                if self._physics_service.check_collision(self._mother_ship, actor):
                    actors.remove_actor("astroids", actor)
                    # callback.remove_actor(actor.get_health_bar())
                    self._mother_ship.take_damage(actor.get_hp())
                    self._audio_service.play_sound("astroid/assets/sound/explosion-01.wav", 0.1)
                    if self._mother_ship.get_hp() <= 0:
                        actors.remove_actor("mother_ship", self._mother_ship)
                        self._mother_ship = None
                    break