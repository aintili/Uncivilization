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


def start_game():
    # t0
    t0 = time.time()

    # initialize pygame
    pg.init()
    pg.font.init()

    # get screen info, ie the monitor info
    infoObject = pg.display.Info()

    # set default w/h
    width = 9 * infoObject.current_w // 10
    height = 9 * infoObject.current_h // 10

    #width = 4*infoObject.current_w//10
    #height = 4*infoObject.current_h//10

    # init screen
    display = pg.display.set_mode((width, height), pg.SRCALPHA)

    # Load assets
    print("Loading assets ")
    IMAGES_DIR = pkg_resources.resource_filename("Uncivilization", "images/")
    assets = {
        img: pg.image.load(os.path.join(IMAGES_DIR, img)).convert_alpha()
        for img in os.listdir(IMAGES_DIR)
    }
    print("Found assets:")
    pprint.pprint(assets)


    # set game icon
    pg.display.set_icon(assets["icon.png"])

    # set default FPS and make timer to maintain it
    MAX_FPS = 60
    clock = pg.time.Clock()

    # initialize Game object
    camera = Camera(width, height, (width // 2, height // 2))
    Player_Input = PlayerInput()
    Game_Renderer = Renderer(display, assets, camera)
    Game_State = GameState()

    GAME = GameObject(Player_Input, Game_State, Game_Renderer)

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
    pass
