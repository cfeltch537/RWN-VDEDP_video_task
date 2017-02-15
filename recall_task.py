
# -*- coding: utf-8 -*-

#################################
# RWN-VDEDP Project
# 
# recall task
#
# ver 0.1 - mbod@asc.upenn.edu 2/13/17
#

from __future__ import print_function, division

from psychopy import visual, logging, core, event, microphone

# -- set the order of audio libraries
# -- need pygame first for movie audio
from psychopy import prefs
prefs.general['audioDriver'] = ['portaudio','coreaudio']


import os
import re
import time
import datetime
import random
import csv


##########
# PARAMS #
##########

DEBUG=True
use_fullscreen = False

# seconds for open recall period (5 mins/300 secs for full task?)
open_recall_duration = 30  

closed_recall_duration = 10


open_recall_instructions = '''
        Now we would like you to tell the driver about as many 
        of the 16 news items you saw before this drive using as much detail as you can remember.
        ###
        Try to use as much as the time as possible and be as specific as you can about what was described
        in the news items and your opinion of them.
'''

closed_recall_instructions = '''
        Now you will be reminded of each of the 16 news items one by one. We would like you to tell the
        driver as much as you can remember about the news item for one minute.
        ###
        Try to use as much as the time as possible and be as specific as you can about what was described
        in the news items and your opinion of them.
'''


#############################
# set up clocks and logging #
#############################
globalClock = core.Clock()
localClock = core.Clock()


if not os.path.exists('logs'):
    os.mkdir('logs')
    
if not os.path.exists('audio'):
    os.mkdir('audio') 
    
logger = logging.LogFile('logs/recall_test.log', level=logging.DATA, filemode='w')
logging.setDefaultClock(globalClock)


#############################
# set up window and stimuli #
#############################

win = visual.Window([1200,800],  
                monitor="testMonitor", 
                fullscr=use_fullscreen, 
                units="deg")
                
win.setRecordFrameIntervals(False)  

ready_prompt = visual.TextStim(win, text='Please start this task once you have driven onto the highway', pos=(0,2), height=1.3)

instruction_block = visual.TextStim(win, text='', pos=(0,3), wrapWidth=26, height=1.1)

next_label = visual.TextStim(win, text='[Press space to continue]', pos=(0,-4), height=0.8)

counter_label = visual.TextStim(win, text='0:00', pos=(0,-4), height=0.9)

fixation = visual.TextStim(win, text="+", pos=[0,0], height=2)

actor_img = visual.ImageStim(win, pos=[0,2] )
prompt_text = visual.TextStim(win, text='', pos=[0,4] )


#####################
# Set up microphone #
#####################
microphone.switchOn() 
mic=microphone.AdvAudioCapture()


#############
# FUNCTIONS #
#############

class CountDownTimer:
    
    def __init__(self, secs=60):
        self.remaining = core.CountdownTimer(secs)
        
    def get_remaining_time(self):
        return self.remaining.getTime()
        
    def show_remaining_time(self):
        mins, seconds = divmod(self.get_remaining_time(), 60)
        return "{:0>2}:{:0>2}".format(int(mins), int(seconds))
        

def do_fixation(fix_length, clock=localClock):
    
    
    logging.log(level=logging.DATA, msg='FIXATION dur {}\tsys:{}'.format(fix_length, time.time()))

    clock.reset()
    while clock.getTime() < fix_length:
        fixation.draw()
        win.flip()
        
        
def show_instructions(display_time=None):
    # instructions
    for idx, instruct_text in enumerate(instructions):
        
        logging.log(level=logging.DATA, msg='Showing instruction screen {}\tsys:{}'.format(idx+1, time.time()))

        instruction_block.setText(format_text(instruct_text))
        instruction_block.draw()
        
        
        if display_time is None:
           next_label.draw()
           win.flip()
           event.waitKeys(keyList=['space'])
        else:
           win.flip()
           core.wait(display_time)
           
           
def ready_screen():
    ready_prompt.draw()
    next_label.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    
    globalClock.reset()
    logging.log(level=logging.DATA, msg='*********** TASK STARTED *************\tsys:{}'.format(time.time()))


def format_text(txt):
    
    return re.sub('^\s+','',
            re.sub('###\s*','\n\n',
                re.sub('\s{2,}',' ', txt.strip())))
    

def open_recall(subj_id='test'):
    
    open_recall_audio_filename = os.path.join('audio','open_recall_{}.wav'.format(subj_id))
        
    instruction_block.setText(format_text(open_recall_instructions))
    
    instruction_block.draw()
    next_label.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    logging.log(level=logging.DATA, msg='START open recall\tsys:{}'.format(time.time()))
    
    tr=CountDownTimer(open_recall_duration)
    
    
    mic.record(open_recall_duration+2, filename = open_recall_audio_filename)
    
    while tr.get_remaining_time()>0:
        counter_label.setText(tr.show_remaining_time())
        counter_label.draw()
        instruction_block.draw()
        win.flip()
    
    do_fixation(2.0)
    
    mic.reset()
    
    logging.log(level=logging.DATA, msg='END open recall\tsys:{}'.format(time.time()))
    logging.flush()
    
    
def closed_recall(subj_id='test'):
    
    stimuli_list = [r for r in csv.DictReader(open('stimuli.csv'))]
    random.shuffle(stimuli_list)
    
    instruction_block.setText(format_text(closed_recall_instructions))
    
    instruction_block.draw()
    next_label.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    logging.log(level=logging.DATA, msg='START closed recall\tsys:{}'.format(time.time()))


    for row in stimuli_list:
        
        logging.log(level=logging.DATA, msg='stim - {}\tsys:{}'.format(row['file2'],time.time()))

        
        actor_img.setImage('img/actor{}.png'.format(row['actor']))
        prompt_text.setText(row['prompt'])
        
        closed_recall_audio_filename = "audio/closed_recall_{}_{}.wav".format(subj_id, row['file2'])
        
        tr=CountDownTimer(closed_recall_duration)
    
    
        mic.record(closed_recall_duration+5, filename = closed_recall_audio_filename)
        
        while tr.get_remaining_time()>0:
            actor_img.draw()
            prompt_text.draw()
            counter_label.setText(tr.show_remaining_time())

            counter_label.draw()
            win.flip()
        
        do_fixation(5.0)
        mic.reset()
    logging.log(level=logging.DATA, msg='END closed recall\tsys:{}'.format(time.time()))
    logging.flush()


#------------------------------- MAIN -----------------------------

if __name__ == "__main__":
    
    
    ready_screen()
    
    open_recall()
    
    closed_recall()
    
    do_fixation(10.0)

    logging.log(level=logging.DATA, msg='*********** TASK ENDED *************\tsys:{}'.format(time.time()))

    # clean up
    logging.flush()
    win.close()
    core.quit()
    
    
###################################
# dev note - 2/14/17
#    - see https://discourse.psychopy.org/t/microphone-recording-not-ending-properly/1039/10
#          re. issue with microphone capture hanging task
#
