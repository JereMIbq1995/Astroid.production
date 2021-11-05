from astroid.script.HandleMothershipAstroidsCollision import HandleMothershipAstroidsCollision
from genie.director import Director
from genie.services.PygameAudioService import PygameAudioService
from genie.services.PygameKeyboardService import PygameKeyboardService
from genie.services.PygamePhysicsService import PygamePhysicsService
from genie.services.PygameScreenService import PygameScreenService

from astroid.cast.ship import Ship
from astroid.cast.mothership import MotherShip
from astroid.cast.background import Background
from astroid.cast.playerScore import PlayerScore

from astroid.script.HandleQuitAction import HandleQuitAction
from astroid.script.DrawFrameAction import DrawFrameAction
from astroid.script.HandleShipMovementAction import HandleShipMovementAction
from astroid.script.MoveActorsAction import MoveActorsAction
from astroid.script.SpawnAstroidsAction import SpawnAstroidsAction
from astroid.script.HandleOffscreenAction import HandleOffscreenAction
from astroid.script.HandleShipAboveMotherShipAction import HandleShipAboveMotherShipAction
from astroid.script.HandleShipAstroidsCollision import HandleShipAstroidsCollision
from astroid.script.HandleBulletsAstroidsCollision import HandleBulletsAstroidsCollision
from astroid.script.HandleShootingAction import HandleShootingAction
from astroid.script.PlayBackgroundMusicAction import PlayBackgroundMusicAction

W_SIZE = (500, 700)
START_POSITION = 200, 250
SHIP_WIDTH = 40
SHIP_LENGTH = 55

def main():

    # Create a director
    director = Director()

    # Create all the actors, including the player
    cast = []

    # Create Mothership:
    mother_ship = MotherShip(path="astroid/assets/mother_ship.png",
                            health_bar_y_offset= (int(W_SIZE[0] / 5.7) / 2) - 10,
                            health_bar_height=20,
                            width=W_SIZE[0],
                            height=int(W_SIZE[0] / 5.7),
                            x= W_SIZE[0]/2,
                            y= W_SIZE[1]-int(W_SIZE[0] / 5.7)/2,
                            max_hp=50,
                            show_text_health=True)
                            
    # Create the player
    player = Ship(path="astroid/assets/spaceship/spaceship_yellow.png", 
                    width = 70,
                    height = 50,
                    x = W_SIZE[0]/2,
                    # y = W_SIZE[1]/10 * 9,
                    y = mother_ship.get_top_left()[1] - 30,
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
    cast.append(mother_ship)
    cast.append(score)

    # Create all the actions
    script = []

    # Initialize all services:
    keyboard_service = PygameKeyboardService()
    physics_service = PygamePhysicsService()
    screen_service = PygameScreenService(W_SIZE)
    audio_service = PygameAudioService()

    # Create input actions
    handle_quit_action = HandleQuitAction(1, keyboard_service)
    handle_ship_movement = HandleShipMovementAction(1, keyboard_service)
    handle_shooting = HandleShootingAction(1, keyboard_service)

    # Create update actions
    move_bodies = MoveActorsAction(1, physics_service)
    handle_offscreen = HandleOffscreenAction(1, W_SIZE)
    handle_ship_above_mothership = HandleShipAboveMotherShipAction(1, W_SIZE)
    handle_ship_astroids_collision = HandleShipAstroidsCollision(1, physics_service, audio_service)
    handle_bullets_astroids_collision = HandleBulletsAstroidsCollision(1, physics_service, audio_service)
    handle_mothership_astroids_collision = HandleMothershipAstroidsCollision(1, physics_service, audio_service)
    spawn_astroids = SpawnAstroidsAction(1, W_SIZE)

    # Create output actions
    play_background_music = PlayBackgroundMusicAction(1, "astroid/assets/sound/background_music.wav", audio_service)
    draw_frame = DrawFrameAction(1, W_SIZE, background_image, screen_service)

    # Give action(s) to the script
    script.append(handle_quit_action)
    script.append(handle_ship_movement)
    script.append(handle_shooting)
    script.append(move_bodies)
    script.append(handle_offscreen)
    script.append(handle_ship_above_mothership)
    script.append(handle_ship_astroids_collision)
    script.append(handle_bullets_astroids_collision)
    script.append(handle_mothership_astroids_collision)
    script.append(spawn_astroids)
    script.append(play_background_music)
    script.append(draw_frame)

    # Give the cast and script to the dirrector by calling direct_scene.
    # direct_scene then runs the main game loop:
    director.direct_scene(cast, script)

if __name__ == "__main__":
    main()