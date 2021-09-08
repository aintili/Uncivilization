import numpy as np
import os
import pkg_resources
import pygame as pg
import pprint
import time

from Uncivilization.GameObject import *
from Uncivilization.HandleInputs import *
from Uncivilization.HandleGameState import *
from Uncivilization.HandleDraw import *
from Uncivilization.IntroAnimation import *

S3 = np.sqrt(3)


def start_game(GAME, clock, MAX_FPS):
    t0 = time.time()
    init_board(GAME)
    s = True
    while s:
        # Frame rate no higher than FPS
        clock.tick(MAX_FPS)

        # Framerate independence, use dt
        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        GAME.dt = dt

        # standard game loop, poll inputs, process and update game state, render
        updateInputs(GAME)
        updateState(GAME)
        draw(GAME)


def mainMenu():
    # t0
    t0 = time.time()

    # initialize pygame
    pg.init()
    pg.font.init()
    pg.mixer.init()

    # get screen info, ie the monitor info
    infoObject = pg.display.Info()

    # set default w/h
    width = 9 * infoObject.current_w // 10
    height = 9 * infoObject.current_h // 10

    # width = 4*infoObject.current_w//10
    # height = 4*infoObject.current_h//10

    # init screen
    display = pg.display.set_mode((width, height), pg.SRCALPHA)

    # set default FPS and make timer to maintain it
    MAX_FPS = 60
    clock = pg.time.Clock()

    # initialize Game object
    camera = Camera(width, height, (width // 2, height // 2))
    Player_Input = PlayerInput()
    Game_Renderer = Renderer(display, camera)
    Game_State = GameState()
    GAME = GameObject(Player_Input, Game_State, Game_Renderer)

    # Load assets
    t_a = time.time()
    print("Processing assets...\n")
    IMAGES_DIR = pkg_resources.resource_filename("Uncivilization", "images/")
    mid_size = camera.hex_size
    mid_scale = (
        int(mid_size * S3) + Game_Renderer.hex_buff,
        int(2 * mid_size) + Game_Renderer.hex_buff,
    )
    assets = {
        img: pg.transform.scale(
            pg.image.load(os.path.join(IMAGES_DIR, img)).convert_alpha(), mid_scale
        )
        for img in os.listdir(IMAGES_DIR)
    }
    Game_Renderer.assets = assets
    dt_a = 1000 * (time.time() - t_a)
    dt_a = format(dt_a, "0.2f")
    #print(f"Configured assets:\n{pprint.pformat(assets, indent=2)}\n in: {dt_a} ms\n")
    print(f"Configured {len(assets.keys())} assets in {dt_a} ms\n")


    # Load sounds
    t_s = time.time()
    print("Processing assets...\n")
    SOUNDS_DIR = pkg_resources.resource_filename("Uncivilization", "sounds/")
    sounds = {
        sound: pg.mixer.Sound(os.path.join(SOUNDS_DIR, sound)) for sound in os.listdir(SOUNDS_DIR)
    }
    dt_s = 1000 * (time.time() - t_s)
    dt_s = format(dt_s, "0.2f")
    #print(f"Configured assets:\n{pprint.pformat(assets, indent=2)}\n in: {dt_a} ms\n")
    print(f"Configured {sounds} wavs in {dt_s} ms\n")


    # set game icon
    pg.display.set_icon(assets["icon.png"])

    play_animation(GAME,clock,time.time(),sounds)
    while Game_State.inMenu:
        # Frame rate no higher than FPS
        clock.tick(MAX_FPS)

        # Framerate independence, use dt
        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        GAME.dt = dt

        # standard game loop, poll inputs, process and update game state, render
        updateInputs(GAME)
        updateStateMenu(GAME)
        drawMenu(GAME)

    start_game(GAME, clock, MAX_FPS)
