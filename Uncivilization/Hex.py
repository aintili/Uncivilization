import numpy as np
import pygame as pg

TO_PIXEL = np.array([[3 ** (0.5), 0.5 * 3 ** (0.5)], [0, 0.5 * 3]])

TO_AXIAL = np.array([[0.57735027, -0.33333333], [0.0, 0.66666667]])


def doubled_to_axial(row, col):
    return cube_to_axial(doubled_to_cube(row, col))


def axial_to_doubled(ax):
    return cube_to_doubled(axial_to_cube(ax))


def doubled_to_cube(row, col):
    x = (col - row) // 2
    z = row
    y = -x - z
    return x, y, z


def cube_to_doubled(cube):
    x, y, z = cube
    col = 2 * x + z
    row = z
    return col, row


def hex_round(ax):
    return cube_to_axial(cube_round(axial_to_cube(ax)))


def axial_to_cube_rounded(ax):
    return cube_round(axial_to_cube(ax))


def cube_to_axial(cube):
    return cube[0], cube[2]


def cube_round(cube):
    x, y, z = cube
    rx = round(x)
    ry = round(y)
    rz = round(z)

    x_diff = abs(rx - x)
    y_diff = abs(ry - y)
    z_diff = abs(rz - z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry

    return int(rx), int(ry), int(rz)


def axial_to_cube(ax):
    x, z = ax
    return x, -x - z, z


def pixel_to_axial(game, pixel):
    """
    Returns correct axial coord given an unrestricted pixel
    """
    r = game.Renderer
    x0, y0 = r.origin
    cam = r.camera
    size = cam.hex_size
    x, y = pixel
    pixel = np.array([x - x0, y - y0])

    v = (1 / size) * np.matmul(TO_AXIAL, pixel)
    return hex_round(v)


def axial_to_pixel(game, v):
    """
    Given an axial coordinate, return an unrestricted pixel
    """
    r = game.Renderer
    x0, y0 = r.origin
    cam = r.camera
    size = cam.hex_size
    offx, offy = cam.get_camera_offset(game)

    x, y = size * np.matmul(TO_PIXEL, v)
    x = x + x0
    y = y + y0
    return x, y


def axial_to_screen_pixel(game, v):
    """
    Given an axial coordinate, return the center pixel for the screen
    """
    r = game.Renderer
    x0, y0 = r.origin
    cam = r.camera
    size = cam.hex_size
    offx, offy = cam.get_camera_offset(game)

    x, y = size * np.matmul(TO_PIXEL, v)
    x = x + x0 + offx
    y = y + y0 + offy
    return x, y


def screen_pixel_to_axial(game, pixel):
    """
    Returns correct axial coord given a pixel restricted to [[0,w],[0,h]],
    considers camera's location
    """

    r = game.Renderer
    x0, y0 = r.origin
    cam = r.camera
    size = cam.hex_size
    offx, offy = cam.get_camera_offset(game)

    x, y = pixel
    pixel = [x - x0 - offx, y - y0 - offy]
    pixel = np.array(pixel)

    v = (1 / size) * np.matmul(TO_AXIAL, pixel)
    return hex_round(v)


class Hex:
    def __init__(self, cube=None, q=None, r=None, color=(100, 100, 100)):
        if cube is None:
            assert q is not None and r is not None
            self.v = np.array([q, r])
            self.cube = axial_to_cube(self.v)

        elif q is None or r is None:
            assert cube is not None
            self.v = np.array(cube_to_axial(cube))
            self.cube = cube
        self.color = color

    def get_corner(self, center, size, index):
        angle_deg = 60 * index - 30
        angle_rad = np.pi / 180 * angle_deg
        return (center[0] + size * np.cos(angle_rad), center[1] + size * np.sin(angle_rad))

    def draw_outline(self, game):
        render = game.Renderer
        origin = render.origin
        display = render.display
        cam = render.camera
        size = cam.hex_size

        x, y = axial_to_screen_pixel(game, self.v)

        points = []
        for i in range(6):
            points.append(self.get_corner((x, y), size, i))
        # pg.draw.rect(display,(100,100,100), (x+5,y+5,10,10))
        pg.draw.polygon(display, self.color, points, width=2)

    def draw_coords(self, game, ctype="axial"):
        q, r = self.v
        render = game.Renderer
        origin = render.origin
        display = render.display
        cam = render.camera
        size = cam.hex_size

        x, y = axial_to_screen_pixel(game, self.v)

        coord_s = ""
        if ctype == "axial" or ctype == "both":
            coord_s += "{q} , {r}".format(q=int(q), r=int(r))

        if ctype == "both":
            coord_s += "  |  "

        if ctype == "doubled" or ctype == "both":

            col, row = axial_to_doubled([q, r])
            coord_s += f"{col} , {row}"

        TextSurf = render.smallText.render(coord_s, False, (255, 255, 255))
        text_rect = TextSurf.get_rect(center=(x, y))
        display.blit(TextSurf, text_rect)
