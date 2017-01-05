
# -*- coding: utf-8 -*-

#################################
# RWN-VDEDP Project
# 
# video task
#
# ver 0.1 - mbod@asc.upenn.edu 11/20/16
#

from __future__ import print_function, division

from psychopy import visual, logging, core, event



globalClock = core.Clock()
logging.console.setLevel(logging.DATA)

logger = logging.LogFile('logs/test.log')


#############################
# set up window and stimuli #
#############################

win = visual.Window((1280,720))

video = visual.MovieStim3(win, filename='stimuli/test1.mp4',
                             pos=(0,0),
                             size=(1024,576),
                             flipVert=False, flipHoriz=False, 
                             loop=False)
                             


fixation = visual.TextStim(win, text="+", pos=[0,0], height=1)


fixation.draw()
win.flip()
core.wait(2.0)

# play video
should_flip = True # video.play()

while video.status != visual.FINISHED:
    
    if should_flip:
        video.draw()
        win.flip()
    if event.getKeys():
        break

logger.flush()

# clean up
win.close()
core.quit()


