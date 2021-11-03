import pygame
from genie.cast.actor import Actor

class PygamePhysicsService:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()

    def _get_rectangle(self, actor: Actor):
        return pygame.Rect(actor.get_top_left()[0], actor.get_top_left()[1], actor.get_width(), actor.get_height())

    def rotate_actors(self, actors : list):
        for actor in actors:
            actor.rotate()

    def move_actors(self, actors : list):
        for actor in actors:
            actor.move_with_vel()

    def check_collision(self, actor1 : Actor, actor2 : Actor):
        """
            - create pygame.Shape
            - call colliderect
        """
        return self._get_rectangle(actor1) \
                .colliderect(
                self._get_rectangle(actor2)
                )
        

    def is_above(self, actor1 : Actor, actor2 : Actor):
        """
            Return true if actor1 is above actor2, and false otherwise
        """
        return actor1.get_top_left()[1] < actor2.get_top_left()[1]

    def is_below(self, actor1 : Actor, actor2 : Actor):
        """
            Return true if actor1 is below actor2, false otherwise
        """
        return actor1.get_bottom_left()[1] > actor2.get_bottom_left()[1]

    def is_left_of(self, actor1 : Actor, actor2 : Actor):
        """
            Return true if actor1 is on the left of actor2, false otherwise
        """
        return actor1.get_top_left()[0] < actor2.get_top_left()[0]

    def is_right_of(self, actor1 : Actor, actor2 : Actor):
        """
            Return true if actor1 is on the right of actor2, false otherwise
        """
        return actor1.get_top_right()[0] > actor2.get_top_right()[0]