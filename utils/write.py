import cv2
import os
from config import *

def write(target, filename, fps):
    print('Writing ...')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    filename = os.path.splitext(os.path.basename(filename))[0] + '.mp4'
    print(filename)
    path = os.path.join(os.getcwd(), OUTPUT_FOLDER)
    path = os.path.join(path, filename)
    writer = cv2.VideoWriter(path, fourcc, fps, (WIDTH, HEIGHT))
    print('Done! - {}'.format(path))
    for frame in target:
        writer.write(frame)
    writer.release()
    cv2.destroyAllWindows()
