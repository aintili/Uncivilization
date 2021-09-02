import pygame as pg
import numpy as np
from Uncivilization.HandleInputs import *
from Uncivilization.Hex import *

def updatePositions(game):
    pass    


def checkCollision(game):
    pass


def handleCollisions(game):
    pass

    

def updateState(game):
    cam = game.Renderer.camera
    gamestate = game.GameState
    inputs = game.PlayerInput
    basicUserInputUpdateState(game)
    basicUserInputLogic(game)
    if not gamestate.isPaused:
        updatePositions(game)
        checkCollision(game)
        handleCollisions(game)
    inputs.mc_pos = None    
