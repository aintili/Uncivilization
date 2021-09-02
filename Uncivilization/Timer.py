import pygame as pg
import numpy as np


class Timer:
    def __init__(self, id):
        self.id = id
        self.timer = None
        self.start_paused_time = None
        self.end_paused_time = None
        self.dt = 0
        self.time_since_last_collision = 0

    def startTimer(self):
        self.timer = pg.time.get_ticks()

    def checkTimer(self):
        return (pg.time.get_ticks() - self.timer - self.getPausedDeltaTime()) / 1000

    def startPausedTimer(self):
        self.start_paused_time = pg.time.get_ticks()

    def endPausedTimer(self):
        self.end_paused_time = pg.time.get_ticks()

    def getPausedDeltaTime(self):
        if self.start_paused_time == None or self.end_paused_time == None:
            dt = 0
        else:
            dt = self.end_paused_time - self.start_paused_time
        return dt

    def checkFrameCount(self, FPS):
        return int(FPS * self.checkTimer())
