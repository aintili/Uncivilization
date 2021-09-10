import os
import pkg_resources
import pygame as pg
import time

from Uncivilization import InitializerFunctions as IF

IMAGES_DIR = pkg_resources.resource_filename("Uncivilization", "images/")
SOUNDS_DIR = pkg_resources.resource_filename("Uncivilization", "sounds/")
CONFIG_DIR = pkg_resources.resource_filename("Uncivilization", "config/")


def main():
    # pip install -e path/to/Uncivilization will install
    # this as a package. Command Unciv will call this function

    assets = load_assets()
    sounds = load_sounds()
    player_config = load_player_config()
    IF.mainMenu(assets, sounds, player_config)


def load_assets():
    # Load assets
    t0 = time.time()
    assets = {img: pg.image.load(os.path.join(IMAGES_DIR, img)) for img in os.listdir(IMAGES_DIR)}
    dt = time.time() - t0
    dt = format(1000 * dt, "0.2f")
    print(f"Found {len(assets.keys())} raw assets in {dt} ms")
    return assets


def load_sounds():
    # Load sounds
    pg.mixer.init()
    t0 = time.time()
    sounds = {
        sound: pg.mixer.Sound(os.path.join(SOUNDS_DIR, sound)) for sound in os.listdir(SOUNDS_DIR)
    }
    dt = time.time() - t0
    dt = format(dt, "0.2f")
    print(f"Found {len(sounds.keys())} wavs in {dt} s\n")
    return sounds


def load_player_config():
    pass


main()
