import pygame
from genie.cast.actor import Actor

class PygamePhysicsService:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()

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
        rect1 = pygame.Rect(actor1.get_top_left()[0], actor1.get_top_left()[1], actor1.get_width(), actor1.get_height())
        rect2 = pygame.Rect(actor2.get_top_left()[0], actor2.get_top_left()[1], actor2.get_width(), actor2.get_height())
        return rect1.colliderect(rect2)

    def is_above(self, actor1 : Actor, actor2 : Actor):
        """
            Return true if actor1 is above actor2, and false otherwise
        """
        pass

    def is_below(self, actor1, actor2):
        pass

    def is_left_of(self, actor1, actor2):
        pass

    def is_right_of(self, actor1, actor2):
        pass