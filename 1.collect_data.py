import numpy as np
from grabscreen import grab_screen
from win32api import GetSystemMetrics
import cv2
import time
from getkeys import key_check
import os
import mouse

jump = [0,1]
idle = [1,0]

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

starting_value = 1

file_name = 'training_data.npy'


def keys_to_output(keys):
    if 'SPACE' in keys or mouse.is_pressed("left"):
        output = [0,1]
    else:
        output = [1,0]
    return output


def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    print('STARTING!!!')
    while(True):

        screen = grab_screen(region=(0,0,width,height))
        last_time = time.time()
        # resize to something a bit more acceptable for a CNN
        screen = cv2.resize(screen, (480,270))
        # run a color convert:
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        keys = key_check()
        output = keys_to_output(keys)
        training_data.append([screen,output])

        #print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
##      cv2.imshow('window',cv2.resize(screen,(640,360)))
##      if cv2.waitKey(25) & 0xFF == ord('q'):
##          cv2.destroyAllWindows()
##          break

        if 'S' in keys:
            print('Saving training data!')
            print(len(training_data))
            print('Please wait...')
            np.save(file_name, training_data)
            training_data = list(np.load(file_name, allow_pickle=True))
            print('Saved!')

        if 'R' in keys:
            print('Reseting training data!')
            training_data = []
            np.save(file_name, training_data)
            training_data = list(np.load(file_name, allow_pickle=True))

        if 'Q' in keys:
            print('Quitting with saving!')
            print('Please wait...')
            np.save(file_name, training_data)
            time.sleep(1)
            print('Saved!')
            break

        if 'Z' in keys:
            print('Quitting without saving!')
            training_data = []
            break


main(file_name, starting_value)
