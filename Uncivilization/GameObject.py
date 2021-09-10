import pygame as pg
import numpy as np
import copy
import json
import pickle
import random

from Uncivilization.Camera import *
from Uncivilization.MapNameToInstructions import *
NUM_MAPS = 6

class GameObject:
    def __init__(self, player_input, game_state, renderer,audio_mixer):
        self.eps = 0.005
        self.dt = 2 ** 31
        self.TARGET_FPS = 60
        self.MAX_FPS = 60
        self.drawDiagnostic = False
        self.cleanDiagnostic = False
        self.PlayerInput = player_input
        self.GameState = game_state
        self.Renderer = renderer
        self.AudioMixer = audio_mixer

    def calc_fps(self):
        return 1 / self.dt


class PlayerInput:
    def __init__(self):
        self.events = None
        self.keyboard_dictionary = None
        self.prevEvents = None
        self.scroll_dir = 0
        self.mc_pos = None
        self.m_pos = None
        self.lc_held0 = None
        self.lc_held1 = None
        self.scrolling = False
        self.custom_inputs = {}


class GameState:
    def __init__(self):
        self.isPaused = False
        self.grid_size = (25, 50)
        self.board = {}
        self.inMainMenu = True
        self.inMapSelect = False
        self.start_game = False
        self.map_type = None
        self.skip_animation = False


class AudioMixer:
    def __init__(self,sounds):
        self.sounds_dict = sounds

    def stop_all(self):
        for sound in self.sounds_dict.values():
            sound.stop()
    
    def stop_all_except(self,exception_list):
        for name,sound in self.sounds_dict.items():
            if name not in exception_list:
                sound.stop()

class Renderer:
    def __init__(self, display, camera, assets):
        self.assets = assets
        self.defaultColor = (0, 0, 0)
        self.extraLargeText = pg.font.SysFont("ubuntucondensed", 60)
        self.largeText = pg.font.SysFont("ubuntucondensed", 30)
        self.smallText = pg.font.SysFont("ubuntucondensed", 20)
        self.display = display
        self.width = pg.display.get_surface().get_width()
        self.height = pg.display.get_surface().get_height()
        self.origin = (self.width // 2, self.height // 2)
        self.to_update = []
        self.camera = camera
        self.full_redraw = True
        self.hex_buff = 5
        self.mainMenuBoxes = self.getMainMenuBoxes()
        self.mapSelectBoxes = self.getMapSelectBoxes()

    def getMainMenuBoxes(
        self,
        text_color=(255, 255, 255),
        background_color_1=(0, 0, 0),
        background_color_2=(0, 0, 0),
        center_1=None,
    ):
        title_string_1 = "UN"
        title_string_2 = "Civilization"
        game_string = "Play Game"
        settings = "Settings"
        w = self.width
        h = self.height
        largeText = self.largeText
        extraLargeText = self.extraLargeText

        TextSurfA = extraLargeText.render(title_string_1, True, (255, 0, 0), (0, 0, 0))
        TextSurfB = extraLargeText.render(title_string_2, True, text_color, (0, 0, 0))

        sa, _ = TextSurfA.get_size()
        sb, _ = TextSurfB.get_size()
        centerax = (w - sb) / 2
        centeray = h // 2 if (center_1 is None or center_1 > h // 2) else center_1
        centerbx = (w + sa) / 2

        text_rectA = TextSurfA.get_rect(center=(centerax, centeray))
        text_rectB = TextSurfB.get_rect(center=(centerbx, h // 2))

        TextSurf1 = largeText.render(game_string, True, text_color, background_color_1)
        text_rect1 = TextSurf1.get_rect(center=(w // 2 - w // 10, h // 2 + h // 10))

        TextSurf2 = largeText.render(settings, True, text_color, background_color_2)
        text_rect2 = TextSurf2.get_rect(center=(w // 2 + w // 10, h // 2 + h // 10))

        return [
            [TextSurfA, text_rectA],
            [TextSurfB, text_rectB],
            [TextSurf1, text_rect1],
            [TextSurf2, text_rect2],
        ]

    def updateMainMenuBoxes(
        self, background_color_1=(0, 0, 0), background_color_2=(0, 0, 0), center_1=None
    ):
        self.mainMenuBoxes = self.getMainMenuBoxes(
            background_color_1=background_color_1,
            background_color_2=background_color_2,
            center_1=center_1,
        )
    

    def getMapSelectBoxes(self):
        rows = 2
        cols = NUM_MAPS // rows
        
        w = self.width
        h = self.height

        x_buff = max(w//50, 1)
        y_buff = max(w//50, 1)
        
        x0 = w//8
        y0 = h//8

        w_takeup = (3*w)//4  
        h_takeup = (3*h)//4
        
        space_xbuff = (cols + 1) * x_buff
        space_ybuff = (rows + 1) * y_buff

        r_w = (w_takeup - space_xbuff) // cols
        r_h = (h_takeup - space_ybuff) // rows

        wh = (r_w,r_h)
        
        rects = []
        for i in range(NUM_MAPS):
            row_num = i // (rows + 1)
            col_num = i % (rows + 1) 
            
            tl_point = (
                x0 + col_num * r_w + (col_num + 1) * x_buff,
                y0 + row_num * r_h + (row_num + 1) * y_buff
            )

            rect = pg.Rect(tl_point,wh)
            rects.append(rect)
        
        return rects
        


