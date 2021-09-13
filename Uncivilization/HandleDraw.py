import pygame as pg
import numpy as np
import random
import time

from Uncivilization.Hex import *
from Uncivilization.Camera import *
from Uncivilization.MapNameToInstructions import *


def draw_board(game):
    state = game.GameState
    board = state.board
    r = game.Renderer
    origin = r.origin
    cam = r.camera
    size = cam.hex_size
    w = r.width
    h = r.height

    br, tl = cam.get_bottom_right_and_top_left()
    v0 = pixel_to_axial(game, tl)
    v1 = pixel_to_axial(game, br)

    col0, row0 = axial_to_doubled(v0)
    col1, row1 = axial_to_doubled(v1)
    subtr = 0
    for row in range(row0 - 1, row1 + 2):
        for col in range(col0 - subtr - 1, col1 + 3, 2):
            q, r = doubled_to_axial(row, col)
            tile = board.get(f"{q},{r}")
            if tile:
                tile.draw_tile_images(game)
                # tile.draw_outline(game)
                # tile.draw_coords(game, ctype="doubled")
        subtr = 1 if subtr == 0 else 0


def diagnosticsDraw(game):
    render = game.Renderer
    w = render.width
    h = render.height
    display = render.display
    largeText = render.largeText

    dt_string = "dt: " + format(1000 * game.dt, "4.0f") + "ms"
    fps_string = "FPS: " + format(game.calc_fps(), "4.0f")

    dt_mock = "  dt:  999ms"
    fps_mock = "  FPS:  9999"

    TextSurfMock = largeText.render(fps_mock, False, (255, 255, 255))
    text_rect_mock = TextSurfMock.get_rect(center=(12 * w // 17, 30))

    TextSurf = largeText.render(fps_string, False, (255, 255, 255))
    text_rect = TextSurf.get_rect(center=(12 * w // 17, 30))

    pg.draw.rect(display, (0, 0, 0), text_rect_mock)
    display.blit(TextSurf, text_rect)

    TextSurfMock = largeText.render(dt_mock, False, (255, 255, 255))
    text_rect_mock = TextSurfMock.get_rect(center=(9 * w // 10, 30))

    TextSurf = largeText.render(dt_string, False, (255, 255, 255))
    text_rect = TextSurf.get_rect(center=(9 * w // 10, 30))

    pg.draw.rect(display, (0, 0, 0), text_rect_mock)
    display.blit(TextSurf, text_rect)

    pg.draw.line(display, (0, 0, 255), (w // 2, 0), (w // 2, h))
    pg.draw.line(display, (0, 0, 255), (0, h // 2), (w, h // 2))

    pg.display.update()


def cleanDiagnosticDraw(game):
    if game.cleanDiagnostic:
        # print("clean")
        display = game.Renderer.display
        display.fill(game.Renderer.defaultColor)
        draw_board(game)
        game.cleanDiagnostic = False
        pg.display.update()


def draw(game):
    r = game.Renderer
    display = r.display

    if r.full_redraw:
        r.full_redraw = False
        display.fill((200, 200, 200))
        draw_board(game)
        pg.display.update()

    diagnosticsDraw(game) if game.drawDiagnostic else cleanDiagnosticDraw(game)


def drawMenu(game):
    r = game.Renderer
    display = r.display
    boxes = r.mainMenuBoxes
    for box_info in boxes:
        surf, rect = box_info
        pg.draw.rect(display, (0, 0, 0), rect)
        display.blit(surf, rect)

    pg.display.update()
    diagnosticsDraw(game) if game.drawDiagnostic else cleanDiagnosticDraw(game)


def drawMenu(game):
    r = game.Renderer
    display = r.display
    display.fill((0, 0, 0))
    boxes = r.mainMenuBoxes
    for box_info in boxes:
        surf, rect = box_info
        pg.draw.rect(display, (0, 0, 0), rect)
        display.blit(surf, rect)

    pg.display.update()
    diagnosticsDraw(game) if game.drawDiagnostic else cleanDiagnosticDraw(game)


def drawMapSelect(game, timer):
    r = game.Renderer
    display = r.display
    display.fill((0, 0, 0))
    rects = r.mapSelectBoxes
    for rect in rects:
        c = (100, 100, 100)
        pg.draw.rect(display, c, rect)

    drawEffect = MAP_TO_DISPLAY["random"]
    drawEffect(game, rects[0], c, timer)

    pg.display.update()
    diagnosticsDraw(game) if game.drawDiagnostic else cleanDiagnosticDraw(game)
