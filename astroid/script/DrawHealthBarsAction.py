from astroid.cast.HasLifeActor import HasLifeActor
from genie.script.action import OutputAction
from genie.services import colors

class DrawHealthBarsAction(OutputAction):
    def __init__(self, priority, screen_service):
        super().__init__(priority)
        self._screen_service = screen_service

    def get_priority(self):
        return super().get_priority()
    
    def set_priority(self, priority):
        return super().set_priority(priority)

    def execute(self, actors, actions, clock, callback):
        """
            Look at all the actors that "has life", draw their health bars
        """
        for actor in actors.get_all_actors():
            if isinstance(actor, HasLifeActor) and actor.get_hp_percent() < 1:
                
                # Figure out dimensions of the health portion of the hp bar
                # using the HasLifeActor
                bottom_left = actor.get_bottom_left()
                health_width = actor.get_hp_percent() * actor.get_width()
                health_height = actor.get_health_bar_height()

                # Position of the health (red) portion of the hp bar
                center_x = bottom_left[0] + health_width / 2
                center_y = actor.get_y() + actor.get_health_bar_y_offset()

                # Position of the empty (grey) portion of the hp bar
                empty_bar_width = actor.get_width() - health_width
                empty_bar_x = center_x + health_width/2 + empty_bar_width/2
                empty_bar_y = center_y

                # Draw the health (red) portion
                self._screen_service.draw_rectangle(center=(center_x, center_y), width=health_width, 
                                                    height= health_height, color = colors.RED,
                                                    border_width=0)

                # Draw the empty (grey) portion
                # (The height of the empty bar should be the same as health_height)
                self._screen_service.draw_rectangle(center=(empty_bar_x,empty_bar_y), width=empty_bar_width, 
                                                    height= health_height, color = colors.GRAY,
                                                    border_width=0)
                
                # If that actor wants to show health in text, draw it at the
                # center of the health bar
                if actor.show_text_health():
                    # color = colors.WHITE if actor.get_hp_percent() > 0.5 else colors.BLACK
                    self._screen_service.draw_text(str(actor.get_hp()) + "/" + str(actor.get_max_hp()),
                                                    font_size= actor.get_health_bar_height(), color = colors.WHITE,
                                                    position = (actor.get_x(), actor.get_y()+actor.get_health_bar_y_offset()),
                                                    position_center=True)