import pygame as pg
import random
import time

from Uncivilization.Hex import *


def convert_images(game):
    t0 = time.time()

    r = game.Renderer
    camera = r.camera

    mid_size = camera.hex_size
    mid_scale = (
        int(mid_size * S3) + r.hex_buff,
        int(2 * mid_size) + r.hex_buff,
    )

    r.assets = {
        img_name: pg.transform.scale(img.convert_alpha(), mid_scale)
        for img_name, img in r.assets.items()
    }

    dt = time.time() - t0
    dt = format(1000*dt,"0.2f")

    print(f"Finished processing {len(r.assets.keys())} assets in {dt}ms")

def random_tiles(game):
    convert_images(game)

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


MAP_TO_FUNC = {
    "random": random_tiles
    }
