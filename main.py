from genie.director import Director
from genie.cast.cast import Cast
from genie.script.script import Script
from genie.services import *

from astroid.cast.ship import Ship
from astroid.cast.mothership import MotherShip
from astroid.cast.background import Background
from astroid.cast.playerScore import PlayerScore
from astroid.cast.startGameButton import StartGameButton

from astroid.script.HandleQuitAction import HandleQuitAction
from astroid.script.HandleShipMovementAction import HandleShipMovementAction
from astroid.script.HandleShootingAction import HandleShootingAction
from astroid.script.HandleStartGameAction import HandleStartGameAction

from astroid.script.MoveActorsAction import MoveActorsAction
from astroid.script.SpawnAstroidsAction import SpawnAstroidsAction
from astroid.script.HandleOffscreenAction import HandleOffscreenAction
from astroid.script.HandleShipAboveMotherShipAction import HandleShipAboveMotherShipAction
from astroid.script.HandleShipAstroidsCollision import HandleShipAstroidsCollision
from astroid.script.HandleBulletsAstroidsCollision import HandleBulletsAstroidsCollision
from astroid.script.HandleMothershipAstroidsCollision import HandleMothershipAstroidsCollision
from astroid.script.PlayBackgroundMusicAction import PlayBackgroundMusicAction

from astroid.script.DrawActorsAction import DrawActorsAction
from astroid.script.DrawHealthBarsAction import DrawHealthBarsAction
from astroid.script.DrawScoreAction import DrawScoreAction
from astroid.script.UpdateScreenAction import UpdateScreenAction

W_SIZE = (500, 700)
START_POSITION = 200, 250
SHIP_WIDTH = 40
SHIP_LENGTH = 55

SCREEN_TITLE = "Asteroids"
FPS = 120

def get_services():
    """
        Ask the user whether they want to use pygame or raylib services
    """
    # Initialize all services:
    service_code = 0
    valid = False
    while not valid:
        service_code = str(input("What service would you like to use? (Input 1 for Pygame or 2 for Raylib): ")).strip()
        if len(str(service_code)) < 1 or not (int(service_code) == 1 or int(service_code) == 2):
            print("Incorrect input! Please try again!")
        else:
            service_code = int(service_code)
            valid = True
    
    return {
        "keyboard" : PygameKeyboardService() if service_code == 1 else RaylibKeyboardService(),
        "physics" : PygamePhysicsService() if service_code == 1 else RaylibPhysicsService(),
        "screen" : PygameScreenService(W_SIZE, SCREEN_TITLE, FPS) if service_code == 1 \
                    else RaylibScreenService(W_SIZE, SCREEN_TITLE, FPS),
        "audio" : PygameAudioService() if service_code == 1 else RaylibAudioService(),
        "mouse" : PygameMouseService() if service_code == 1 else RaylibMouseService()
    }

def main():
    """
        Create director, cast, script, then run the game loop
    """
    # Get all the services needed services 
    services = get_services()

    keyboard_service = services["keyboard"]
    physics_service = services["physics"]
    screen_service = services["screen"]
    audio_service = services["audio"]
    mouse_service = services["mouse"]

    # Create a director
    director = Director()

    # Create all the actors, including the player
    cast = Cast()

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
    ship = Ship(path="astroid/assets/spaceship/spaceship_yellow.png", 
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
    
    # Start game button
    start_button = StartGameButton(path="astroid/assets/others/start_button.png",
                                    width = 305,
                                    height = 113,
                                    x = W_SIZE[0]/2,
                                    y = W_SIZE[1]/2)

    # Give actor(s) to the cast. Append the background first so that it won't
    # be drawn on top of other actors.
    cast.add_actor("background_image", background_image)
    cast.add_actor("ship", ship)
    cast.add_actor("mother_ship", mother_ship)
    cast.add_actor("score", score)
    cast.add_actor("start_button", start_button)

    # Create all the actions
    script = Script()

    # Create input actions
    # script.append(HandleQuitAction(1, keyboard_service))
    script.add_action("input", HandleQuitAction(1, keyboard_service))

    # Add actions that must be added to the script when the game starts
    startgame_actions = {"input" : [], "update" : [], "output": []}
    startgame_actions["input"].append(HandleShootingAction(1, keyboard_service, audio_service))
    startgame_actions["input"].append(HandleShipMovementAction(2, keyboard_service))
    startgame_actions["update"].append(SpawnAstroidsAction(1, W_SIZE))
    script.add_action("input", HandleStartGameAction(2, mouse_service, physics_service, startgame_actions))

    # Create update actions
    script.add_action("update", MoveActorsAction(1, physics_service))
    script.add_action("update", HandleOffscreenAction(1, W_SIZE))
    script.add_action("update", HandleShipAboveMotherShipAction(1, W_SIZE))
    script.add_action("update", HandleShipAstroidsCollision(1, physics_service, audio_service))
    script.add_action("update", HandleBulletsAstroidsCollision(1, physics_service, audio_service))
    script.add_action("update", HandleMothershipAstroidsCollision(1, physics_service, audio_service))
    # script.append(SpawnAstroidsAction(1, W_SIZE))

    # Create output actions
    script.add_action("output", PlayBackgroundMusicAction(1, "astroid/assets/sound/background_music.wav", audio_service))
    script.add_action("output", DrawActorsAction(1, screen_service))
    script.add_action("output", DrawHealthBarsAction(1, screen_service))
    script.add_action("output", DrawScoreAction(1, screen_service))
    script.add_action("output", UpdateScreenAction(2, screen_service))

    # Give the cast and script to the dirrector by calling direct_scene.
    # direct_scene then runs the main game loop:
    director.direct_scene(cast, script)

if __name__ == "__main__":
    main()