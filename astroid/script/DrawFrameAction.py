from astroid.cast.background import Background
from genie.script.action import OutputAction
from genie.services.PygameScreenService import PygameScreenService

class DrawFrameAction(OutputAction):
    def __init__(self, priority, window_size, background):
        super().__init__(priority)
        self._window_size = window_size
        self._background_image = background
        self._screen_service = PygameScreenService(window_size)

    def get_priority(self):
        return super().get_priority()
    
    def set_priority(self, priority):
        return super().set_priority(priority)

    def execute(self, actors, actions, clock, callback):
        self._screen_service.draw_actors(actors)
        self._screen_service.draw_text("Hello World!", position= (20,20))
        self._screen_service.update_screen()