from typing import Any
from astroid.cast.HasLifeActor import HasLifeActor
from astroid.cast.playerScore import PlayerScore
from genie.script.action import OutputAction
from genie.services.PygameScreenService import WHITE

class DrawFrameAction(OutputAction):
    def __init__(self, priority, window_size, background, screen_service):
        super().__init__(priority)
        self._score = None
        self._window_size = window_size
        self._background_image = background
        self._screen_service = screen_service

    def get_priority(self):
        return super().get_priority()
    
    def set_priority(self, priority):
        return super().set_priority(priority)
    
    def _draw_score(self, actors):
        """
            - Look for the score actor in the actors list
            - Print the score on the screen
        """
        if (self._score == None):
            for actor in actors:
                if isinstance(actor, PlayerScore):
                    self._score = actor
                    break
        if self._score != None:
            self._screen_service.draw_text("Score: " + str(self._score.get_score()), font_size=48, color=(255,255,255),position= (20,20))
        

    def _draw_health_bars(self, actors):
        """
            This function looks through all the actors and see which one
            needs a health bar drawn, then draws it for that actor
        """
        for actor in actors:
            if isinstance(actor, HasLifeActor) and actor.get_hp_percent() < 1:
                bottom_left = actor.get_bottom_left()
                health_bar_width = actor.get_hp_percent() * actor.get_width()
                health_bar_height = actor.get_health_bar_height()

                center_x = bottom_left[0] + health_bar_width / 2
                center_y = actor.get_y() + actor.get_health_bar_y_offset()

                empty_bar_width = actor.get_width() - health_bar_width
                empty_bar_x = center_x + health_bar_width/2 + empty_bar_width/2
                empty_bar_y = center_y

                self._screen_service.draw_rectangle(center=(center_x, center_y), width=health_bar_width, 
                                                    height= health_bar_height, color = (255, 0, 0),
                                                    border_width=0)

                self._screen_service.draw_rectangle(center=(empty_bar_x,empty_bar_y), width=empty_bar_width, 
                                                    height= health_bar_height, color = (160, 160, 160),
                                                    border_width=0)
                
                # If that actor wants to show health in text, draw it at the
                # center of the health bar
                if actor.show_text_health():
                    self._screen_service.draw_text(str(actor.get_hp()) + "/" + str(actor.get_max_hp()),
                                                    font_size= actor.get_health_bar_height(), color = WHITE,
                                                    position = (actor.get_x(), actor.get_y()+actor.get_health_bar_y_offset()),
                                                    position_center=True)

    def execute(self, actors, actions, clock, callback):
        """
            - First, draw all the actors
            - Next, draw all their health_bars
            - Next, draw the score
            - Finally, update the screen so everything shows up
        """
        self._screen_service.draw_actors(actors)
        self._draw_health_bars(actors)
        self._draw_score(actors)
        self._screen_service.update_screen()