import pygame as pg
import time

def play_animation(game,clock,t0,sounds):
    r = game.Renderer
    tfps = game.TARGET_FPS
    display = r.display
    h = r.height
    box,_,_,_ = r.mainMenuBoxes
    surf,_ = box
    center_y = -surf.get_size()[1]/2
    timer = 0
    violin = sounds["violin.wav"]
    record = sounds["record.wav"]
    fall = sounds["fall.wav"]
    crash = sounds["crash.wav"]
    doom = sounds["doom.wav"]

    violin.play()
    violin_needs_stop = True
    record_needs_play = True
    fall_needs_play = True
    while center_y <= h//2:
        clock.tick(tfps)

        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        game.dt = dt
        timer+=dt

        if timer > 6:
            if violin_needs_stop:
                violin.stop()
                violin_needs_stop = False
            if record_needs_play:
                record.play()
                record_needs_play = False

        if timer > 7:
            if fall_needs_play:
                fall.play()
                fall_needs_play = False
            r.updateMainMenuBoxes(center_1= center_y)
            boxes = [r.mainMenuBoxes[0],r.mainMenuBoxes[1]]
            center_y += game.dt * tfps * max(h/200,1)
        else:
            boxes = [r.mainMenuBoxes[1]]

        for box_info in boxes:
            surf, rect = box_info
            pg.draw.rect(display, (0, 0, 0), rect)
            display.blit(surf, rect)

        pg.display.update()

    r.updateMainMenuBoxes(center_1= h//2)
    boxes = [r.mainMenuBoxes[0],r.mainMenuBoxes[1]]
    for box_info in boxes:
        surf, rect = box_info
        pg.draw.rect(display, (0, 0, 0), rect)
        display.blit(surf, rect)

    pg.display.update()

    fall.stop()
    record.stop()
    crash.play()
    time.sleep(2)
    crash.stop()
    doom.play()

