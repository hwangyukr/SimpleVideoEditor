import cv2
import logging
from utils.read import read
from utils.edit import edit
from utils.write import write
logging.basicConfig(filename='./log.txt', level=logging.DEBUG)

def run():
    reader = enumerate(read())
    for idx, video in reader:
        (frames, filename, fps) = video
        edited = edit(frames, filename, fps)
        if edited != None:
            write(edited, filename, fps)

if __name__=='__main__':
    try:
        run()
    except Exception as ex:
        print('ERROR : ' + str(ex))
        logging.exception(ex)
