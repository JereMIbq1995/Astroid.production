from genie.script.action import InputAction
from genie.services import keys

# from astroid.cast.ship import Ship

VEL = 4

class HandleFrogMovementAction(InputAction):
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
            # Check which keys are pressed and update the ship's velocity accordingly
            keys_state = self._keyboard_service.get_keys_state(keys.A, keys.D, keys.S, keys.W)
            if keys_state[keys.A]:
                if (not self._frog.flipped()):
                    self._frog.flip_image()
                self._frog.set_vx(-VEL)
            if keys_state[keys.D]:
                if (self._frog.flipped()):
                    self._frog.flip_image()
                self._frog.set_vx(VEL)
            if keys_state[keys.S]:
                self._frog.set_vy(VEL)
            if keys_state[keys.W]:
                self._frog.set_vy(-VEL)
            
            # If keys in either dirrection are not pressed, set velocity of that direction to 0
            if not keys_state[keys.A] and not keys_state[keys.D]:
                self._frog.set_vx(0)
            if not keys_state[keys.W] and not keys_state[keys.S]:
                self._frog.set_vy(0)