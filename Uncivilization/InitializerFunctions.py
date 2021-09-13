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
from Uncivilization.Timer import Timer


S3 = np.sqrt(3)
SUPPORTED_RESOLUTIONS = sorted(
    [
        (720, 480),
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1280, 800),
        (1366, 768),
        (1440, 900),
        (1600, 900),
        (1680, 1050),
        (1920, 1080),
        (1920, 1200),
    ]
)


def closest_res(width, height):
    if width < height:
        print(f"{width} < {height}, swapping dimensions")
        store = width
        width = height
        height = store

    if (width, height) in SUPPORTED_RESOLUTIONS:
        return width, height

    r_user = width / height
    r_supported = [w / h for w, h in SUPPORTED_RESOLUTIONS]
    r_diffs = [abs(r_user - r) for r in r_supported]
    min_diff = min(r_diffs)
    i_first_min_diff = r_diffs.index(min_diff)
    new_res = SUPPORTED_RESOLUTIONS[i_first_min_diff]
    print(
        f"{width} x {height} not supported!\nReformatting to smallest supported resolution which is closest by ratio: {new_res[0]} x {new_res[1]}"
    )
    return new_res


def initialize_game_object(raw_assets, sounds, player_config):
    # initialize pygame
    pg.init()
    pg.font.init()

    # get screen info, ie the monitor info
    infoObject = pg.display.Info()

    # set default w/h
    width = infoObject.current_w
    height = infoObject.current_h

    # init screen
    video_info = player_config["VIDEO DISPLAY OPTIONS"]["SCREEN_SIZE"]
    video_info = video_info.lower().strip(" ").split("x")
    video_info = video_info[0] if len(video_info) == 1 else (int(video_info[0]), int(video_info[1]))
    width, height = video_info if len(video_info) == 2 else (width, height)
    # video_flags = pg.SRCALPHA | pg.FULLSCREEN | pg.SCALED if video_info == "fullscreen" else pg.SRCALPHA
    # display = pg.display.set_mode(size = (width, height), flags = video_flags)
    width, height = closest_res(width, height)
    display = pg.display.set_mode(size=(width, height))

    clock = pg.time.Clock()

    # initialize Game object
    camera = Camera(width, height, (width // 2, height // 2))
    Player_Input = PlayerInput()
    Game_Renderer = Renderer(display, camera, raw_assets)
    Game_State = GameState()
    Audio_Mixer = AudioMixer(sounds)
    GAME = GameObject(Player_Input, Game_State, Game_Renderer, Audio_Mixer)

    # set game icon
    pg.display.set_icon(raw_assets["icon.png"])
    menuSelector(GAME, clock)


def menuSelector(game, clock):
    s = True
    gamestate = game.GameState
    while s:
        if gamestate.inMainMenu:
            mainMenu(game, clock)

        if gamestate.inMapSelect:
            mapSelect(game, clock)

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


def mapSelect(game, clock):
    t0 = time.time()
    gamestate = game.GameState
    map_select_timer = Timer()
    map_select_timer.start_timer()

    while gamestate.inMapSelect:
        clock.tick(game.MAX_FPS)

        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        game.dt = dt

        updateInputs(game)
        updateStateMapSelect(game)
        drawMapSelect(game, map_select_timer)

    if gamestate.start_game:
        game.AudioMixer.fadeout_all()


def mainMenu(game, clock):
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
