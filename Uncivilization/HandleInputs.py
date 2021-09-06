import pygame as pg
import numpy as np

from Uncivilization.Hex import *


def updateInputs(game):
    inputs = game.PlayerInput
    inputs.events = pg.event.get()
    inputs.keyboard_dictionary = pg.key.get_pressed()


def basicUserInputUpdateState(game):
    r = game.Renderer
    inputs = game.PlayerInput
    gamestate = game.GameState
    cam = r.camera
    events = inputs.events
    for event in events:
        if event.type == pg.QUIT:
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                gamestate.isPaused = not gamestate.isPaused

                if gamestate.isPaused:
                    # trigger load pause screen
                    a = 1

                else:
                    # trigger clean pause screen
                    # resume game
                    a = 2

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                if game.drawDiagnostic:
                    game.cleanDiagnostic = True
                game.drawDiagnostic = not game.drawDiagnostic
            elif event.button == 1:
                m_pos = pg.mouse.get_pos()
                inputs.mc_pos = m_pos

        elif event.type == pg.MOUSEWHEEL:
            if inputs.scrolling is False:
                inputs.scroll_dir = event.y
                inputs.scrolling = True

    if pg.mouse.get_pressed()[0]:
        inputs.lc_held0 = inputs.lc_held1
        inputs.lc_held1 = pg.mouse.get_pos()
    else:
        inputs.lc_held0 = None
        inputs.lc_held1 = None


def basicUserInputLogic(game):
    rend = game.Renderer
    gs = game.GameState
    inputs = game.PlayerInput
    mc_pos = inputs.mc_pos
    cam = rend.camera
    size = cam.hex_size

    # if mc_pos:
    #     v = screen_pixel_to_axial(game, mc_pos)
    #     col, row = axial_to_doubled(v)
    #     q, r = v
    #     print(f"{q},{r} | {col},{row}\n")

    if inputs.lc_held1 is not None and inputs.lc_held0 is not None:
        x0, y0 = inputs.lc_held0
        x1, y1 = inputs.lc_held1

        diffx = x1 - x0
        diffy = y1 - y0
        diff = (-diffx, -diffy)
        cam.add_to_center(diff, game)

        rend.full_redraw = True
        if inputs.lc_held1 == inputs.lc_held0:
            rend.full_redraw = False

    if inputs.scrolling:
        cam.zoom_recenter_method2(game)
        inputs.scrolling = False
        rend.full_redraw = True

