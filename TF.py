import numpy as np
import cv2
import time
from grab_screen import grab_screen
from getkeys import key_check
import os
import mouse

def keys_to_output(keys):
    #[SPACE]
    output = [0]
    if 'SPACE' in keys or mouse.is_pressed("left"):
        output = 1
    else:
        output = 0

    print(output)
    return output

file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name, allow_pickle=True))
else:
    print('File does not exist, creating a new one!')
    training_data = []

def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    while True:
        global training_data
        screen = grab_screen(region=(0,0,1920,1080))
        screen = cv2.resize(screen, (960, 540))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        keys = key_check()
        output = keys_to_output(keys)
        training_data.append([screen, output])
        #print(f'Frame took {time.time()-last_time} seconds')
        last_time = time.time()

        if 'S' in keys:
            print('Saving training data!')
            print(len(training_data))
            print('Please wait...')
            np.save(file_name, training_data)
            time.sleep(1)
            print('Saved!')

        if 'R' in keys:
            print('Reseting training data!')
            training_data = []

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

main()
