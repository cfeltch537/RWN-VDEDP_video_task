
# -*- coding: utf-8 -*-

#################################
# RWN-VDEDP Project
# 
# video task
#
# ver 0.1 - mbod@asc.upenn.edu 11/20/16
#
#

from __future__ import print_function, division

from psychopy import visual, logging, core, event

# -- set the order of audio libraries
# -- need pygame first for movie audio
from psychopy import prefs
prefs.general['audioLib'] = ['pygame', 'pyo']

import os
import re


##########
# PARAMS #
##########

STIM_DIR = 'stimuli'


DEBUG=True
use_fullscreen = False

globalClock = core.Clock()
localClock = core.Clock()

#logging.console.setLevel(logging.DEBUG)

logger = logging.LogFile('logs/test.log', filemode='w', level=logging.DEBUG)




instructions = ['''In this task, you are going to watch a series of video clips 
                 of two people who are auditioning for a news anchor position. 
                  ###
                  The local news station auditioning the news anchors is trying a 
                  new format. They want to see if combining humor with regular 
                  news stories will change how viewers respond to the news.''', 
                  
                '''You will see the old and new formats in the news clips.
                  You will watch 32 clips in total.
                  ###
                  Please pay attention to them as you will be asked for your
                  opinions about them latter.''' ]



#############################
# set up window and stimuli #
#############################

win = visual.Window([1200,800],  
                monitor="testMonitor", 
                fullscr=use_fullscreen, 
                units="deg")
                
win.setRecordFrameIntervals(False)  

ready_prompt = visual.TextStim(win, text='Ready...', pos=(0,2), height=1.3)

instruction_block = visual.TextStim(win, text='', pos=(0,3), wrapWidth=26, height=1.1)

next_label = visual.TextStim(win, text='[Press space to continue]', pos=(0,-3), height=0.9)

video = visual.MovieStim3(win, filename='stimuli/test1.mov',
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
    #video.play()

    while localClock.getTime() < video_duration:        
        video.draw()
        win.flip()

        if event.getKeys(['escape']):
            break

    logging.flush()


def do_fixation(fix_length, clock=localClock):
    clock.reset()
    while clock.getTime() < fix_length:
        fixation.draw()
        win.flip()
        
        
def show_instructions(display_time=10):
    # instructions
    for instruct_text in instructions:
        instruct_text = re.sub('^\s+','',
                                re.sub('###\s*','\n\n',
                                    re.sub('\s{2,}',' ', instruct_text.strip())))
        instruction_block.setText(instruct_text)
        instruction_block.draw()
        win.flip()
        core.wait(display_time)

def ready_screen():
    ready_prompt.draw()
    next_label.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    


if __name__ == '__main__':


    ready_screen()

    show_instructions()

    # TODO - update here with a specific stimuli for experiment sets
    videos = [vn for vn in os.listdir(STIM_DIR) if vn.endswith('.mov')]
    videos.sort()

    for vid in videos:

        do_fixation(5.0)

        play_video(os.path.join(STIM_DIR, vid))


    do_fixation(1.0)

    # clean up
    win.close()
    core.quit()


# --------------------------------------------------------------------------------
#
# development note 2/2/17 - some videos throwing error discussed in
#   https://discourse.psychopy.org/t/error-while-trying-to-play-movie/1253/5
#   added patch to moviepy/audio/io/readers.py 
#