import numpy as np
from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey,ReleaseKey, W, A, S, D
from models import inception_v3 as googlenet
from getkeys import key_check
from collections import deque, Counter
import random
from statistics import mode,mean
import numpy as np
import mouse
from motion import motion_detection

GAME_WIDTH = 1920
GAME_HEIGHT = 1080

how_far_remove = 800
rs = (20,15)
log_len = 25

motion_req = 800
motion_log = deque(maxlen=log_len)

WIDTH = 480
HEIGHT = 270
LR = 1e-3
EPOCHS = 10

choices = deque([], maxlen=5)
hl_hist = 250
choice_hist = deque([], maxlen=hl_hist)

jump = [0,1]
idle = [1,0]


t_time = 0.25

def jump():
    mouse.click(button="left")

model = googlenet(WIDTH, HEIGHT, 3, LR, output=2)
MODEL_NAME = ''
model.load(MODEL_NAME)

print('We have loaded a previous model!!!!')

def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    mode_choice = 0

    screen = grab_screen(region=(0,0,GAME_WIDTH,GAME_HEIGHT))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    prev = cv2.resize(screen, (WIDTH,HEIGHT))

    t_minus = prev
    t_now = prev
    t_plus = prev

    while(True):
        
        if not paused:
            screen = grab_screen(region=(0,0,GAME_WIDTH,GAME_HEIGHT))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            last_time = time.time()
            screen = cv2.resize(screen, (WIDTH,HEIGHT))

            delta_count_last = motion_detection(t_minus, t_now, t_plus)

            t_minus = t_now
            t_now = t_plus
            t_plus = screen
            t_plus = cv2.blur(t_plus,(4,4))

            prediction = model.predict([screen.reshape(WIDTH,HEIGHT,3)])[0]
            prediction = np.array(prediction) * np.array([4.5, 0.1, 0.1, 0.1,  1.8,   1.8, 0.5, 0.5, 0.2])

            mode_choice = np.argmax(prediction)

            if mode_choice == 0:
                choice_picked = 'idle'
                
            elif mode_choice == 1:
                jump()
                choice_picked = 'jump'

            print('loop took {} seconds. Motion: {}. Choice: {}'.format( round(time.time()-last_time, 3), choice_picked))
    
        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                time.sleep(1)

main()       
