from astroid.script.HandleCollisionsAction import HandleCollisionAction
from astroid.script.HandleShootingAction import HandleShootingAction
from astroid.script.PlayBackgroundMusicAction import PlayBackgroundMusicAction
from genie.director import Director
from genie.services.PygameKeyboardService import PygameKeyboardService
from genie.services.PygamePhysicsService import PygamePhysicsService

from astroid.cast.ship import Ship
from astroid.cast.background import Background
from astroid.cast.playerScore import PlayerScore

from astroid.script.DrawFrameAction import DrawFrameAction
from astroid.script.HandleInputAction import HandleInputAction
from astroid.script.MoveActorsAction import MoveActorsAction
from astroid.script.SpawnAstroidsAction import SpawnAstroidsAction
from astroid.script.HandleOffscreenAction import HandleOffscreenAction

W_SIZE = (500, 700)
START_POSITION = 200, 250
SHIP_WIDTH = 40
SHIP_LENGTH = 55

def main():

    # Create a director
    director = Director()

    # Create all the actors, including the player
    cast = []

    # Create the player
    player = Ship(path="astroid/assets/spaceship/spaceship_yellow.png", 
                    width = 70,
                    height = 50,
                    x = W_SIZE[0]/2,
                    y = W_SIZE[1]/10 * 9,
                    rotation=180)
    # Scale the background to have the same dimensions as the Window,
    # then position it at the center of the screen
    background_image = Background("astroid/assets/space.png", 
                                    width=W_SIZE[0],
                                    height=W_SIZE[1],
                                    x = W_SIZE[0]/2,
                                    y = W_SIZE[1]/2)

    score = PlayerScore(path="", score=0)

    # Give actor(s) to the cast. Append the background first so that it won't
    # be drawn on top of other actors.
    cast.append(background_image)
    cast.append(player)
    cast.append(score)

    # Create all the actions
    script = []

    # Create input actions
    handle_input = HandleInputAction(1, PygameKeyboardService())
    handle_shooting = HandleShootingAction(1, PygameKeyboardService())

    # Create update actions
    move_bodies = MoveActorsAction(1, PygamePhysicsService())
    handle_offscreen = HandleOffscreenAction(1, W_SIZE)
    handle_collision = HandleCollisionAction(1)
    spawn_astroid = SpawnAstroidsAction(1, W_SIZE)

    # Create output actions
    play_background_music = PlayBackgroundMusicAction(1, "astroid/assets/sound/background_music.wav")
    draw_frame = DrawFrameAction(1, W_SIZE, background_image)

    # Give action(s) to the script
    script.append(handle_input)
    script.append(handle_shooting)
    script.append(move_bodies)
    script.append(handle_offscreen)
    script.append(handle_collision)
    script.append(spawn_astroid)
    script.append(play_background_music)
    script.append(draw_frame)

    # Give the cast and script to the dirrector by calling direct_scene.
    # direct_scene then runs the main game loop:
    director.direct_scene(cast, script)

if __name__ == "__main__":
    main()