import os
import sys
import cv2
from config import *

def read():
    path = os.path.join(os.getcwd(), INPUT_FOLDER)
    listdir = os.listdir(path)
    for filename in listdir:
        input_file = os.path.join(path, filename)
        cap = cv2.VideoCapture(input_file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print('loading... {}'.format(filename))
        frames=[]
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==False:
                break
            clip = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
            frames.append(clip)
        assert len(frames) > 0, input_file
        cap.release()
        cv2.destroyAllWindows()
        yield(frames, filename, fps)
