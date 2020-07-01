from Scenes.TitleScreen import TitleScene
import pygame
import Tools.Images


def run_game(width, height, fps, starting_scene):
    pygame.init()  # initialize pygame
    screen = pygame.display.set_mode((width, height))  # set our window stuff and create a pygame surface
    clock = pygame.time.Clock()  # create a clock object so we can manipulate fps

    active_scene = starting_scene  # set the starting scene

    while active_scene is not None:
        # if active scene becomes we None we effectively close the game.
        pressed_keys = pygame.key.get_pressed()  # get an array of the pressed keys from pygame

        # event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                # user hit the red x to quit the game
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                # a key is pressed
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    # user presses the escape key
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    # user presses alt f4
                    quit_attempt = True

            if quit_attempt:
                # terminate the scene
                active_scene.terminate()
            else:
                # add the event on to the filtered events that will be sent to the objects
                filtered_events.append(event)
        if len(filtered_events) > 0:
            # if an event happened then we send it to the scene
            active_scene.process_input(filtered_events, pressed_keys)
        active_scene.update()  # frame update the scene
        active_scene.render(screen)  # drawing frame update the scene

        active_scene = active_scene.next  # change our active scene if it is different

        pygame.display.flip()  # flip the display so that we can draw on it again
        clock.tick(fps)  # limit the fps


if __name__ == "__main__":
    il = Tools.Images.ImageLoader()
    run_game(1200, 800, 60, TitleScene(il))
