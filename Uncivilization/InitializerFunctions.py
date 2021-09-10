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


def initialize_game_object(raw_assets, sounds, player_config):
    # initialize pygame
    pg.init()
    pg.font.init()

    # get screen info, ie the monitor info
    infoObject = pg.display.Info()

    # set default w/h
    #width = 9 * infoObject.current_w // 10
    #height = 9 * infoObject.current_h // 10

    width = 15*infoObject.current_w//20
    height = 15*infoObject.current_h//20

    # init screen
    display = pg.display.set_mode((width, height), pg.SRCALPHA)

    clock = pg.time.Clock()

    # initialize Game object
    camera = Camera(width, height, (width // 2, height // 2))
    Player_Input = PlayerInput()
    Game_Renderer = Renderer(display, camera, raw_assets)
    Game_State = GameState()
    Audio_Mixer = AudioMixer(sounds)
    GAME = GameObject(Player_Input, Game_State, Game_Renderer,Audio_Mixer)

    # set game icon
    pg.display.set_icon(raw_assets["icon.png"])
    menuSelector(GAME,clock)


def menuSelector(game,clock):
    s = True
    gamestate = game.GameState
    while s:
        if gamestate.inMainMenu:
            mainMenu(game,clock)
        
        if gamestate.inMapSelect:
            mapSelect(game,clock)
        
        if gamestate.start_game:
            start_game(game, clock)


def start_game(game, clock):
    t0 = time.time()
    init_board(game)
    s = True
    while s:
        # Frame rate no higher than FPS
        clock.tick(game.MAX_FPS)

        # Framerate independence, use dt
        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        game.dt = dt

        # standard game loop, poll inputs, process and update game state, render
        updateInputs(game)
        updateState(game)
        draw(game)


def mapSelect(game,clock):
    t0 = time.time()
    gamestate = game.GameState
    while gamestate.inMapSelect:
        clock.tick(game.MAX_FPS)
        
        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        game.dt = dt

        updateInputs(game)
        updateStateMapSelect(game)
        drawMapSelect(game)
    
    if gamestate.start_game:
        game.AudioMixer.stop_all()

def mainMenu(game,clock):
    gamestate = game.GameState

    play_animation(game, clock)
    
    # t0
    t0 = time.time()
    while gamestate.inMainMenu:
        clock.tick(game.MAX_FPS)
        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        game.dt = dt
        updateInputs(game)
        if gamestate.inMainMenu:
            # standard game loop, poll inputs, process and update game state, render
            updateStateMenu(game)
            drawMenu(game)


def init_board(game):
    f = MAP_TO_FUNC[game.GameState.map_type]
    f(game)