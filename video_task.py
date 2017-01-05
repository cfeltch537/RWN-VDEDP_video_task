
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

DEBUG=True
use_fullscreen = False

globalClock = core.Clock()
localClock = core.Clock()

#logging.console.setLevel(logging.DEBUG)

logger = logging.LogFile('logs/test.log', filemode='w', level=logging.DEBUG)


#############################
# set up window and stimuli #
#############################

win = visual.Window([1200,800],  
                monitor="testMonitor", 
                fullscr=use_fullscreen, 
                units="deg")
                
win.setRecordFrameIntervals(False)  


video = visual.MovieStim3(win, filename='stimuli/test1.mp4',
                             pos=(0,0),
                             size=(1024,576),
                             flipVert=False, flipHoriz=False, loop=False)                           


fixation = visual.TextStim(win, text="+", pos=[0,0], height=2)




def play_video(filename):
    
    video.loadMovie(filename)
    localClock.reset()
    video_duration = video.duration

    if DEBUG:
        print("Video {} duration is {}".format(filename,video_duration))

    # play video
    video.play()

    while localClock.getTime() < video_duration:
        
        video.draw()
        win.flip()

        if event.getKeys(['escape']):
            break

    logging.flush()



if __name__ == '__main__':

    fixation.draw()
    win.flip()
    core.wait(2.0)

    play_video('stimuli/test1.mp4')

    # clean up
    win.close()
    core.quit()


