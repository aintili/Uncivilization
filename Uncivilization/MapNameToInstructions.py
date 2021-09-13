import pygame as pg
import numpy as np
import random
import time

from Uncivilization.Hex import *

def convert_hexes(game):
    t0 = time.time()

    r = game.Renderer
    camera = r.camera
    mid_size = camera.hex_size

    _ , twice_hex_size = r.default_hex_asset_size
    mid_scale = get_bordered_hex_scale(game,twice_hex_size,mid_size,hex_buffer=r.default_hex_buff)

    r.assets = {
        img_name: pg.transform.scale(img.convert_alpha(), mid_scale)
        for img_name, img in r.assets.items()
    }

    img = r.assets[list(r.assets.keys())[0]]
    _,img_h = img.get_size()

    r.current_hex_buff = (img_h - 2 * mid_size) / 2

    dt = time.time() - t0
    dt = format(1000 * dt, "0.2f")

    print(f"Finished processing {len(r.assets.keys())} assets in {dt}ms")


def get_random_dots_info(game, rect, rect_color, background_color, text_rect):
    display = game.Renderer.display

    x0, y0 = rect.topleft
    x1, y1 = rect.bottomright

    buffx = (x1 - x0) / 10
    buffy = (y1 - y0) / 10

    pg.draw.rect(display, background_color, rect)
    pg.draw.rect(display, rect_color, rect)

    dots_to_draw = np.random.randint(20, 30)
    r = min(buffx, buffy) // 2

    xtr, ytr = text_rect.topleft
    xtr = xtr - r
    ytr = ytr - r
    wtr = text_rect.width + 2 * r
    htr = text_rect.height + 2 * r
    logical_rect = pg.rect.Rect((xtr, ytr), (wtr, htr))

    redraw_list = []
    for i in range(dots_to_draw):
        color = random.choice(
            [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (255, 255, 0)]
        )
        rx = np.random.uniform(x0 + buffx, x1 - buffx)
        ry = np.random.uniform(y0 + buffy, y1 - buffy)
        while logical_rect.collidepoint((rx, ry)):
            rx = np.random.uniform(x0 + buffx, x1 - buffx)
            ry = np.random.uniform(y0 + buffy, y1 - buffy)
        redraw_list.append([rx, ry, color, r])
    return redraw_list


def draw_random_dots(game, rect, rect_color, timer, background_color=(0, 0, 0)):
    rend = game.Renderer
    display = rend.display

    title_string = "Random"
    largeText = rend.largeText
    TextSurf = largeText.render(title_string, True, (0, 0, 0))
    text_rect = TextSurf.get_rect(center=rect.center)

    if rend.mapSelectRedraw is None:
        game.Renderer.mapSelectRedraw = get_random_dots_info(
            game, rect, rect_color, background_color, text_rect
        )

    if timer.smart_peek_timer() > 0.333333:
        timer.end_timer()
        game.Renderer.mapSelectRedraw = get_random_dots_info(
            game, rect, rect_color, background_color, text_rect
        )
        timer.start_timer()

    to_draw = rend.mapSelectRedraw
    for draw_info in to_draw:
        rx, ry, color, r = draw_info
        pg.draw.circle(display, color, (rx, ry), r)

    display.blit(TextSurf, text_rect)


def random_tiles(game):
    convert_hexes(game)

    state = game.GameState
    grid = state.grid_size
    rows, cols = grid

    imgs = [
        "red",
        "dark_green",
        "light_green",
        "yellow",
        "dark_blue",
        "light_blue",
        "white",
    ]

    # up grid_height//2 and down grid_height // 2
    # same, left and right
    for row in range(-rows // 2, rows // 2 + 1):
        for col in range(-cols, cols + 1, 2):
            cube = doubled_to_cube(row, col)
            img = random.choice(imgs)
            img = f"{img}_hex_and_border.png"
            tile = Hex(cube=cube, images=[img])
            q, r = tile.v
            state.board.update({f"{q},{r}": tile})


MAP_TO_FUNC = {"random": random_tiles}

MAP_TO_DISPLAY = {"random": draw_random_dots}
