import numpy as np
import os
import pygame as pg
import pprint
import time

from Uncivilization.GameObject import *
from Uncivilization.HandleInputs import *
from Uncivilization.HandleGameState import *
from Uncivilization.HandleDraw import *
from Uncivilization.IntroAnimation import *
from Uncivilization.MapNameToInstructions import *

S3 = np.sqrt(3)


def init_board(game):
    f = MAP_TO_FUNC[game.GameState.map_type]
    f(game)


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


def mainMenu(raw_assets, sounds, player_config):
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
    Game_Renderer = Renderer(display, camera, raw_assets)
    Game_State = GameState()
    GAME = GameObject(Player_Input, Game_State, Game_Renderer)

    # set game icon
    pg.display.set_icon(raw_assets["icon.png"])

    skip_animation = False
    play_animation(GAME, clock, time.time(), sounds, skip_animation)
    while Game_State.start_game is False:
        clock.tick(MAX_FPS)
        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        GAME.dt = dt
        updateInputs(GAME)
        if Game_State.inMenu:
            # standard game loop, poll inputs, process and update game state, render
            updateStateMenu(GAME)
            drawMenu(GAME)

        elif Game_State.inMapSelect:
            updateStateMapSelect(GAME)
            # drawMapSelect(GAME)

    print("Waiting ~3s to simulate play game -> map select -> loading map")
    time.sleep(3)

    for key in sounds.keys():
        sounds[key].stop()

    start_game(GAME, clock, MAX_FPS)
