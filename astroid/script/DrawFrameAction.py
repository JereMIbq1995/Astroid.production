from astroid.cast.background import Background
from astroid.cast.astroid import Astroid
from astroid.cast.playerScore import PlayerScore
from genie.script.action import OutputAction
from genie.services.PygameScreenService import PygameScreenService

class DrawFrameAction(OutputAction):
    def __init__(self, priority, window_size, background):
        super().__init__(priority)
        self._score = None
        self._window_size = window_size
        self._background_image = background
        self._screen_service = PygameScreenService(window_size)

    def get_priority(self):
        return super().get_priority()
    
    def set_priority(self, priority):
        return super().set_priority(priority)
    
    def _draw_health_bar(self, actor):
        if isinstance(actor, Astroid) and actor.get_hp_percent() < 1:
            bottom_left = actor.get_bottom_left()
            health_bar_width = actor.get_hp_percent() * actor.get_width()
            
            center_x = bottom_left[0] + health_bar_width / 2
            center_y = bottom_left[1] + 5

            health_bar_center = (center_x, center_y)
            print("Got here!")
            self._screen_service.draw_rectangle(center=health_bar_center, width=health_bar_width, height= 5, color = (255, 0, 0), border_width=0)


    def execute(self, actors, actions, clock, callback):
        if (self._score == None):
            for actor in actors:
                if isinstance(actor, PlayerScore):
                    self._score = actor
                    break;

        self._screen_service.draw_actors(actors)
        for actor in actors:
            self._draw_health_bar(actor)
        self._screen_service.draw_text("Score: " + str(self._score.get_score()), font_size=48, color=(255,255,255),position= (20,20))
        self._screen_service.update_screen()