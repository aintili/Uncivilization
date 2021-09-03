import pygame as pg
from Uncivilization.Hex import *

S3 = 3 ** (1 / 2)
INV_S3 = S3 * 0.3333333333333333


class Camera:
    def __init__(self, w, h, center, n_min=6, n_max=14):
        self.MIN_HEX_SIZE = w / (n_max * S3)
        self.MAX_HEX_SIZE = w / (n_min * S3)
        self.w = w
        self.h = h
        self.center = center
        self.is_stationary = True
        self.reverse = False
        self.hex_size = (self.MAX_HEX_SIZE + self.MIN_HEX_SIZE) / 2

    def get_bottom_right_and_top_left(self, center=None):
        c_x, c_y = self.center if center is None else center
        br = (c_x + self.w / 2, c_y + self.h / 2)
        tl = (c_x - self.w / 2, c_y - self.h / 2)
        return br, tl

    def get_camera_offset(self, game):
        o_x, o_y = game.Renderer.origin
        c_x, c_y = self.center
        return (o_x - c_x, o_y - c_y)

    def update_hex_size(self, hex_size, game):
        if hex_size > self.MAX_HEX_SIZE:
            self.hex_size = self.MAX_HEX_SIZE
        elif hex_size < self.MIN_HEX_SIZE:
            self.hex_size = self.MIN_HEX_SIZE
        else:
            self.hex_size = hex_size

    def add_to_hex_size(self, incr, game):
        new_hex_size = self.hex_size + incr
        self.update_hex_size(new_hex_size,game)

    def update_center(self, cen, game):
        board = game.GameState.board
        cx, cy = cen
        row, col = game.GameState.grid_size

        max_col = col + 1
        min_col = -col - 1

        max_row = row // 2 + 1
        min_row = -row // 2 - 1

        br, tl = self.get_bottom_right_and_top_left(center=cen)

        # Overshot right
        v0 = doubled_to_axial(0, max_col)
        v1 = doubled_to_axial(1, max_col)

        x0, y0 = axial_to_pixel(game, v0)
        x1, y1 = axial_to_pixel(game, v1)

        if x1 > x0:
            x0 = x1

        max_right = x0 + S3 * self.hex_size / 2
        if br[0] > max_right:
            cx = max_right - self.w / 2

        # Overshot left
        v0 = doubled_to_axial(0, min_col)
        v1 = doubled_to_axial(1, min_col)

        x0, y0 = axial_to_pixel(game, v0)
        x1, y1 = axial_to_pixel(game, v1)

        if x1 < x0:
            x0 = x1

        min_left = x0 - S3 * self.hex_size / 2

        if tl[0] < min_left:
            cx = min_left + self.w / 2

        # Overshot up
        v0 = doubled_to_axial(min_row, 1) if min_row % 2 == 1 else doubled_to_axial(min_row, 0)
        x0, y0 = axial_to_pixel(game, v0)

        min_up = y0 - self.hex_size
        if tl[1] < min_up:
            cy = min_up + self.h / 2

        # Overshot down
        v0 = doubled_to_axial(max_row, 1) if max_row % 2 == 1 else doubled_to_axial(max_row, 0)
        x0, y0 = axial_to_pixel(game, v0)

        max_down = y0 + self.hex_size
        if br[1] > max_down:
            cy = max_down - self.h / 2

        self.center = (cx, cy)

    def add_to_center(self, incr, game):
        x1, y1 = incr
        x0, y0 = self.center
        new_center = (x1 + x0, y1 + y0)
        self.update_center(new_center, game)

    def zoom_recenter_method1(self, game):
        inputs = game.PlayerInput

        # Instead of figuring out how increase the size
        # of a hex proportionally to shrinking camera window
        # we just increase the drawing size and shift
        # the camera as needed

        # Before we do anything, get the 'old' (really the current)
        # pixel value of the center of the hex at camera center
        old_v = pixel_to_axial(game, self.center)
        x_old, y_old = axial_to_pixel(game, old_v)

        # Update the hex_size however we want
        scroll_sp = 5
        scroll_amt = inputs.scroll_dir * game.dt * game.TARGET_FPS * scroll_sp
        self.add_to_hex_size(scroll_amt,game)
        
        # Now get the new center pixel for the same tile
        # and update the camera's position
        x_new, y_new = axial_to_pixel(game, old_v)

        dx = x_new - x_old
        dy = y_new - y_old

        self.add_to_center((dx, dy), game)

        # This is 100% big brain approach, so it means it will probably
        # work most but not all of the time

    def zoom_recenter_method2(self, game):
        inputs = game.PlayerInput

        # through a bit of geometry one can show:
        # Let D1 be the length of the segment from
        # the center of a hex the camera center is on
        # and the center of the camera. If that line continued,
        # Let D2 be the length of the segment from the center of the camera
        # to where-ever that line intersects the hexagon.
        # Then:
        # D1/(D1+D2) = 2Y/(sqrt(3) * size)
        # Where Y is y_camera - y_hex_origin
        # To correctly place the camera after zoom we assert
        # the ratio D1/(D1+D2) is unchanged. That is, Y_new = (size_new/size_old)*Y_old
        # Through a little more geometry and law of sines one can prove
        # X_new = R*( (size_new/2) - (Y_new/sqrt(3)) )/(R-1)

        v = pixel_to_axial(game, self.center)

        x0_old, y0_old = axial_to_pixel(game, v)
        xc, yc = self.center

        Y_old = yc - y0_old
        X_old = xc - x0_old
        size_old = self.hex_size
        H_old = 0.5 * S3 * size_old  # height of equilateral triangle
        R = Y_old / H_old

        scroll_sp = 10
        scroll_amt = inputs.scroll_dir * game.dt * game.TARGET_FPS * scroll_sp
        self.add_to_hex_size(scroll_amt,game)

        x0_new, y0_new = axial_to_pixel(game, v)

        Y_new = (self.hex_size / size_old) * Y_old
        yc_new = Y_new + y0_new

        X_new = (self.hex_size / size_old) * X_old
        xc_new = X_new + x0_new

        self.update_center((xc_new, yc_new), game)
