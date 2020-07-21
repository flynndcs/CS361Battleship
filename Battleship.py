from Scenes.TitleScreen import TitleScene
import pygame
from pygame import *
import Tools.Images
import datetime
pygame.font.init()  # initialize font


def run_game(width, height, fps, starting_scene):
    pygame.init()  # initialize pygame
    screen = pygame.display.set_mode((width, height))  # set our window stuff and create a pygame surface
    clock = pygame.time.Clock()  # create a clock object so we can manipulate fps

    active_scene = starting_scene  # set the starting scene
    time_in_frame = 0
    last_time = datetime.datetime.now()
    while active_scene is not None:

        # getting time stats so that we can force a framerate separate from the drawing frame
        deltatime = (datetime.datetime.now() - last_time).microseconds  # time passed since last frame
        last_time = datetime.datetime.now()  # change our last time to current time
        time_in_frame += deltatime  # add the delta time to our time counter

        if time_in_frame > 15625:
            # if the time between the last frame has passed 15625mcs effectively forcing a tick rate of 64 ticks per sec
            # whereas the drawing rate is uncapped atm

            # if active scene becomes we None we effectively close the game.
            pressed_keys = pygame.key.get_pressed()  # get an array of the pressed keys from pygame

            # event filtering
            filtered_events = []
            for event in pygame.event.get():
                # print(event)
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
        """
        # This block can be used to see your drawing fps
        if deltatime != 0:
            fps = 6000000 / float(deltatime)
            print("fps: " + str(fps))
        """
        active_scene.render(screen)  # drawing frame update the scene

        active_scene = active_scene.next  # change our active scene if it is different

        pygame.display.flip()  # flip the display so that we can draw on it again
        # clock.tick(fps)  # limit the fps

        # mouseX, mouseY = pygame.mouse.get_pos()
        # print(mouseX, mouseY)


if __name__ == "__main__":
    il = Tools.Images.ImageLoader()
    run_game(1000, 955, 60, TitleScene(il))
