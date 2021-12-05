from genie.script.action import InputAction
from genie.services import keys

# from astroid.cast.ship import Ship

VEL = 4

class HandleFrogAttackAction(InputAction):
    def __init__(self, priority, keyboard_service):
        super().__init__(priority)
        self._keyboard_service = keyboard_service
        self._frog = None
    
    def execute(self, actors, actions, clock, callback):
        """
            This action handles the movement of the ship
        """
        # Look for the ship among the actors if we haven't already known it
        self._frog = actors.get_first_actor("frog")
        
        # Don't worry about it if ship doesn't exist
        if (self._frog != None):
            # Check which keys are pressed and update the ship's velocity accordingly
            if self._keyboard_service.is_key_down(keys.SPACE):
                self._frog.set_animating(True)