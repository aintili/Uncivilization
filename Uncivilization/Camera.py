import pygame as pg
from Uncivilization.Hex import *

S3 = 3 ** (1 / 2)
INV_S3 = S3 * (1 / 3)


class Camera:
    def __init__(self, hex_asset_size, w_scr, h_scr, rows, cols, n_max=14, n_min=4):
        self.n_min = n_min
        self.n_max = n_max
        self.hex_asset_size = hex_asset_size
        self.hex_size = 0.5 * self.hex_asset_size[1]
        self.w_scr = w_scr
        self.h_scr = h_scr
        self.screen_ratio = h_scr / w_scr
        self.n_mid = (n_max + n_min) // 2
        w = int(self.n_mid * hex_asset_size[0])
        h = int(w * self.screen_ratio)
        self.surface = pg.Surface((w, h))
        self.w_max = n_max * hex_asset_size[0]
        self.h_max = self.w_max * self.screen_ratio
        self.w_min = n_min * hex_asset_size[0]
        self.h_min = self.w_min * self.screen_ratio
        self.center = (0, 0)
        self.screen_to_display_ratio = self.w_scr / w
        self.is_stationary = True
        self.reverse = False
        self.zoom_level = 1

        ###### doubled coords #######
        max_row = rows // 2
        min_row = abs(-rows // 2)
        
        self.pos_x = 0.5 * (cols + 1) * self.hex_asset_size[0]
        self.neg_x = -0.5 * (cols + 2)* self.hex_asset_size[0]

        self.pos_y = self.get_row_boundary(max_row)
        self.neg_y = -self.get_row_boundary(min_row)

        print(self.pos_x - self.neg_x)
        print(self.pos_y - self.neg_y)
        #############################

    def get_row_boundary(self, row):
        r = row // 2
        r *= 3
        r += 1 if row % 2 == 0 else 2.5
        return self.hex_size * r


    def get_surface_center(self):
        w, h = self.surface.get_size()
        return (w / 2, h / 2)

    def get_bottom_right_and_top_left(self, center=None):
        cx, cy = self.center if center is None else center
        hw, hh = [s / 2 for s in self.surface.get_size()]
        br = (cx + hw, cy + hh)
        tl = (cx - hw, cy - hh)
        return br, tl

    def get_camera_offset(self, game):
        return self.center

    def update_zoom_level(self, zl, game):
        cw, ch = self.surface.get_size()
        nw, nh = (cw * zl, ch * zl)

        if nw > self.w_max or nh > self.h_max:
            nw = self.w_max
            nh = self.h_max

        elif nw < self.w_min or nh < self.h_min:
            nw = self.w_min
            nh = self.h_min

        self.surface = pg.Surface((nw, nh))
        self.screen_to_display_ratio = self.w_scr / nw

    def zoom(self, incr, game):
        new_zoom = self.zoom_level + incr
        self.update_zoom_level(new_zoom, game)

    def update_center(self, cen, game):
        gs = game.GameState
        board = gs.board
        cx, cy = cen
        row, col = game.GameState.grid_size
        w, h = self.surface.get_size()

        pos_x = self.pos_x
        pos_y = self.pos_y

        neg_x = self.neg_x
        neg_y = self.neg_y

        br, tl = self.get_bottom_right_and_top_left(center=cen)

        # # Overshot right
        if br[0] > pos_x:
            cx = pos_x - w / 2

        # # Overshot left
        if tl[0] < neg_x:
            cx = neg_x + w / 2

        # # Overshot up
        if tl[1] < neg_y:
            cy = neg_y + h / 2

        # # Overshot down
        if br[1] > pos_y:
            cy = pos_y - h / 2

        self.center = (cx, cy)


    def add_to_center(self, incr, game):
        x1, y1 = incr
        x0, y0 = self.center
        new_center = (x1 + x0, y1 + y0)
        self.update_center(new_center, game)

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
        # Since the new right triangle is a shear transformation of the old right triangle,
        # they are similar, so the ratio X/Y must also be preserved,
        # thus:
        # X_new = (size_new/size_old)*X_old
        # Since this is done entirely through ratios, this works
        # independently of which sub equilateral triangle we are in

        v = pixel_to_axial(game, self.center)

        x0_old, y0_old = axial_to_pixel(game, v)
        xc, yc = self.center

        Y_old = yc - y0_old
        X_old = xc - x0_old
        size_old = self.apparent_hex_size
        H_old = 0.5 * S3 * size_old  # height of equilateral triangle
        R = Y_old / H_old

        scroll_sp = 0.5
        scroll_amt = inputs.scroll_dir * game.dt * game.TARGET_FPS * scroll_sp
        self.update_apparent_hex_size(scroll_amt, game)

        x0_new, y0_new = axial_to_pixel(game, v)

        Y_new = (self.apparent_hex_size / size_old) * Y_old
        yc_new = Y_new + y0_new

        X_new = (self.apparent_hex_size / size_old) * X_old
        xc_new = X_new + x0_new

        self.update_center((xc_new, yc_new), game)

    def zoom_recenter_method3(self, game):
        inputs = game.PlayerInput
        scroll_sp = 0.3
        scroll_amt = -1 * inputs.scroll_dir * game.dt * game.TARGET_FPS * scroll_sp
        self.zoom(scroll_amt, game)
        self.update_center(self.center, game)
