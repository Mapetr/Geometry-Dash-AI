import numpy as np
import cv2
import time
from grab_screen import grab_screen
from getkeys import key_check
import os

def keys_to_output(keys):
    #[SPACE]
    output = [0]
    if 'SPACE' in keys:
        output[0] = [1]
    else:
        output[0] = [0]
    return output

file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
else:
    print('File does not exist, creating a new one!')
    training_data = []

def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    while True:
        screen = grab_screen(region=(0,0,1920,1080))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        keys = key_check()
        output = keys_to_output(keys)
        training_data.append([screen, output])
        print(f'Frame took {time.time()-last_time} seconds')
        last_time = time.time()

        if 'S' in keys:
            print('Saving training data!')
            print(len(training_data))
            np.save(file_name, training_data)

        if 'R' in keys:
            print('Reseting training data!')
            training_data = []

main()