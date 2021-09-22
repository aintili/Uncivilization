import pygame as pg
import numpy as np
import random
import sys
import time

from Uncivilization.Hex import *
from Uncivilization.Camera import *
from Uncivilization.MapNameToInstructions import *


def draw_board(game):
    state = game.GameState
    board = state.board
    rend = game.Renderer
    screen = rend.screen
    cam = rend.camera
    
    #cam.surface.fill((0, 0, 0))
    cam.update_display_as_world_section()
    display = cam.surface

    w = rend.width
    h = rend.height

    # br, tl = cam.get_bottom_right_and_top_left()
    # v0 = pixel_to_axial(game, tl)
    # v1 = pixel_to_axial(game, br)

    # col0, row0 = axial_to_doubled(v0)
    # col1, row1 = axial_to_doubled(v1)
    # subtr = 0
    # for row in range(row0 - 1, row1 + 2):
    #     for col in range(col0 - subtr - 1, col1 + 3, 2):
    #         q, r = doubled_to_axial(row, col)
    #         tile = board.get(f"{q},{r}")
    #         if tile:
    #             tile.draw_tile_images_to_display(game)
    #             #tile.draw_coords(game, ctype="both")
    #     subtr = 1 if subtr == 0 else 0

    display = pg.transform.scale(display, (w, h))
    screen.blit(display, (0, 0))


def diagnosticsDraw(game):
    render = game.Renderer
    w = render.width
    h = render.height
    screen = render.screen
    largeText = render.largeText

    dt_string = "dt: " + format(1000 * game.dt, "4.0f") + "ms"
    fps_string = "FPS: " + format(game.calc_fps(), "4.0f")

    dt_mock = "  dt:  999ms"
    fps_mock = "  FPS:  9999"

    TextSurfMock = largeText.render(fps_mock, False, (255, 255, 255))
    text_rect_mock = TextSurfMock.get_rect(center=(12 * w // 17, 30))

    TextSurf = largeText.render(fps_string, False, (255, 255, 255))
    text_rect = TextSurf.get_rect(center=(12 * w // 17, 30))

    pg.draw.rect(screen, (0, 0, 0), text_rect_mock)
    screen.blit(TextSurf, text_rect)

    TextSurfMock = largeText.render(dt_mock, False, (255, 255, 255))
    text_rect_mock = TextSurfMock.get_rect(center=(9 * w // 10, 30))

    TextSurf = largeText.render(dt_string, False, (255, 255, 255))
    text_rect = TextSurf.get_rect(center=(9 * w // 10, 30))

    pg.draw.rect(screen, (0, 0, 0), text_rect_mock)
    screen.blit(TextSurf, text_rect)

    pg.draw.line(screen, (0, 0, 255), (w // 2, 0), (w // 2, h))
    pg.draw.line(screen, (0, 0, 255), (0, h // 2), (w, h // 2))

    pg.display.update()


def cleanDiagnosticDraw(game):
    if game.cleanDiagnostic:
        # print("clean")
        screen = game.Renderer.screen
        screen.fill(game.Renderer.defaultColor)
        if game.GameState.start_game:
            draw_board(game)
        game.cleanDiagnostic = False
        pg.display.update()


def draw(game):
    r = game.Renderer
    screen = r.screen

    if r.full_redraw:
        r.full_redraw = False
        screen.fill((200, 200, 200))
        draw_board(game)
        pg.display.update()

    diagnosticsDraw(game) if game.drawDiagnostic else cleanDiagnosticDraw(game)


def drawSettingsMenu(game):
    pass


def drawMenu(game):
    r = game.Renderer
    screen = r.screen
    screen.fill((0, 0, 0))
    boxes = r.mainMenuBoxes
    for box_info in boxes:
        surf, rect = box_info
        pg.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(surf, rect)

    pg.display.update()
    diagnosticsDraw(game) if game.drawDiagnostic else cleanDiagnosticDraw(game)


def drawMapSelect(game, timer):
    r = game.Renderer
    screen = r.screen
    screen.fill((0, 0, 0))
    rects = r.mapSelectBoxes
    for rect in rects:
        c = (100, 100, 100)
        pg.draw.rect(screen, c, rect)

    drawEffect = MAP_TO_DISPLAY["random"]
    drawEffect(game, rects[0], c, timer)

    pg.display.update()
    diagnosticsDraw(game) if game.drawDiagnostic else cleanDiagnosticDraw(game)

def distance_to_extrema_rows(n_rows,size):
    return size * (1.5 * n_rows + 1)


def init_world_render(game):
    t_load = time.time()
    gamestate = game.GameState
    rows,cols = gamestate.grid_size

    board = gamestate.board
    rend = game.Renderer
    cam = rend.camera
    s = cam.hex_asset_size[1] / 2

    w_world = cam.world_size[0]
    d_from_bottom = cam.d_from_bottom

    cols_right = len([None for key in board.keys() if key.split(",")[1] == "0" and "-" not in key]) - 1
    origin_x = w_world - (cols_right + 0.5) * cam.hex_asset_size[0]
    origin_y = d_from_bottom
    cam.AXIAL_ORIGIN = (origin_x,origin_y)

    for tile in board.values():
        tile.draw_tile_images_to_world(game)
        tile.draw_coords(game,ctype="both")

    dt = time.time() - t_load
    dt = format(dt,"0.2f")
    byte_size_row = cam.WORLD_SURFACE.get_pitch()
    byte_size = byte_size_row * cam.WORLD_SURFACE.get_size()[1]
    byte_size /= (1024 * 1024 * 1024)
    byte_size = format(byte_size,"0.2f")
    print(f"Finished initializing world in {dt}s.\nIt is ~{byte_size} GB (using pitch * height)")