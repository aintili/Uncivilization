import pygame as pg
import numpy as np
import copy
import json
import pickle
import random

from Uncivilization.Camera import *


class GameObject:
    def __init__(self, player_input, game_state, renderer):
        self.eps = 0.005
        self.dt = 2 ** 31
        self.TARGET_FPS = 60
        self.drawDiagnostic = False
        self.cleanDiagnostic = False
        self.PlayerInput = player_input
        self.GameState = game_state
        self.Renderer = renderer

    def calc_fps(self):
        return 1 / self.dt


class PlayerInput:
    def __init__(self):
        self.events = None
        self.keyboard_dictionary = None
        self.prevEvents = None
        self.scroll_dir = 0
        self.mc_pos = None
        self.lc_held0 = None
        self.lc_held1 = None
        self.scrolling = False


class GameState:
    def __init__(self):
        self.isPaused = False
        self.grid_size = (25, 50)
        self.board = {}


class Renderer:
    def __init__(self, display, assets, camera):
        self.assets = assets
        self.defaultColor = (0, 0, 0)
        self.largeText = pg.font.SysFont("ubuntucondensed", 30)
        self.smallText = pg.font.SysFont("ubuntucondensed", 15)
        self.display = display
        self.width = pg.display.get_surface().get_width()
        self.height = pg.display.get_surface().get_height()
        self.origin = (self.width // 2, self.height // 2)
        self.to_update = []
        self.camera = camera
        self.full_redraw = True

    def draw(self, Sprite=None, coord=None, screen=None, color=None, bounds=None, surface=None):
        if screen != None:
            if Sprite is not None and coord != (None, None):
                screen.blit(Sprite, coord)
            elif color is not None and bounds is not None:
                pg.draw.rect(screen, color, bounds)
            elif surface is not None and bounds is not None:
                screen.blit(surface, bounds)
