import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

train_data = np.load('training_data.npy')
print(len(train_data))
df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))

idle = []
jump = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == [1,0]:
        idle.append([img,choice])
    elif choice == [0,1]:
        jump.append([img,choice])
    else:
        print('Hmmm... Weird')

idle = idle[:len(jump)]
jump = jump[:len(idle)]

final_data = idle + jump

shuffle(final_data)
print(len(final_data))

fd = pd.DataFrame(final_data)
print(fd.head())
print(Counter(fd[1].apply(str)))

np.save('training_data_v2.npy')






def show_training_data(img, choice):
    for data in train_data:
        img = data[0]
        choice = data[1]
        show_training_data(img, choice)
        cv2.imshow('Training data', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break