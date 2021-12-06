from genie.cast.animatedActor import AnimatedActor
from genie.services import *

from genie.cast.cast import Cast
from genie.cast.actor import Actor

from genie.script.script import Script
from genie.script.action import Action

from genie.director import Director

from testAnime.HandleQuitAction import HandleQuitAction
from testAnime.HandleShipMovementAction import HandleShipMovementAction
from testAnime.HandleFrogAttackAction import HandleFrogAttackAction
from testAnime.HandleFrogMovementAction import HandleFrogMovementAction

from testAnime.MoveActorAction import MoveActorsAction

from testAnime.DrawActorsAction import DrawActorsAction
from testAnime.UpdateScreenAction import UpdateScreenAction

W_SIZE = (500, 700)
MAX_FPS = 120
def main():
    
    service_code = 0
    while not (int(service_code) == 1 or int(service_code) == 2):
        service_code = str(input("What service would you like to use? (Input 1 for Pygame or 2 for Raylib): ")).strip()
        if not (int(service_code) == 1 or int(service_code) == 2):
            print (service_code)
            print("Incorrect input! Please try again!")

    if int(service_code) == 1:
        keyboard_service = PygameKeyboardService()
        physics_service = PygamePhysicsService()
        screen_service = PygameScreenService(W_SIZE)
        screen_service.set_fps(MAX_FPS)
        audio_service = PygameAudioService()
        mouse_service = PygameMouseService()
    elif int(service_code) == 2:
        keyboard_service = RaylibKeyboardService()
        physics_service = RaylibPhysicsService()
        screen_service = RaylibScreenService(W_SIZE)
        screen_service.set_fps(MAX_FPS)
        audio_service = RaylibAudioService()
        mouse_service = RaylibMouseService()

    director = Director()
    cast = Cast()
    script = Script()

    # For now there's only the ship in the cast
    # Notice I used the astroid image here for the ship
    #   just so that you can see how the image is flipped
    cast.add_actor("ship", Actor(path="astroid/assets/astroids/astroid_large.png", 
                    width = 70,
                    height = 50,
                    x = W_SIZE[0]/2,
                    # y = W_SIZE[1]/10 * 9,
                    y = W_SIZE[1] - W_SIZE[1]/10,
                    rotation=180))
    
    # Add the animated frog:
    frog_animations = []
    for i in range(1, 11):
        file_index = "0" + str(i) if i < 10 else str(i)
        frog_animations.append(f"testAnime/assets/frog/frame_{file_index}.png")
        # print(f"assets/frog/frame_{file_index}.png") 
    cast.add_actor("frog", AnimatedActor(frog_animations, 256, 128, 30, MAX_FPS, True, W_SIZE[0]/2, W_SIZE[1]/2, flipped=True))
    cast.add_actor("frog", AnimatedActor(frog_animations, 256, 128, 30, MAX_FPS, False, W_SIZE[0]/3, W_SIZE[1]/3))

    # Add actions to the script
    script.add_action("input", HandleQuitAction(1, keyboard_service))
    script.add_action("input", HandleShipMovementAction(2, keyboard_service))
    script.add_action("input", HandleFrogAttackAction(2, keyboard_service))
    script.add_action("input", HandleFrogMovementAction(2, keyboard_service))

    script.add_action("update", MoveActorsAction(1, physics_service))

    script.add_action("output", DrawActorsAction(1, screen_service))
    script.add_action("output", UpdateScreenAction(2, screen_service))

    director.direct_scene(cast, script)

if __name__ == "__main__":
    main()