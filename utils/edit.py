import cv2
from utils.editor import Editor
import keyboard as kb

KEYS = {
    'ESC': 27,
    'ENTER': 13,
    'F1': 7340032,
    'F2': 7405568,
    'F3': 7471104,
    'F4': 7536640,
    'F5': 7602176,
    'LEFT': 2424832,
    'RIGHT': 2555904,
    'DEL': 3014656,
    'NUM0': 48,
    'TAB': 9,
    'SPACE': 32,
    'SQUARE_BRACKETS_LEFT': 91,
    'SQUARE_BRACKETS_RIGHT': 93
}

def key_event_common(editor, key):
    d = 1
    if kb.is_pressed("shift") == True:
        d = 10
    if key==KEYS['LEFT']:
        editor.move_frame(-d)
    if key==KEYS['RIGHT']:
        editor.move_frame(d)
    if key==KEYS['DEL']:
        editor.remove_frame()
    if key==KEYS['F5']:
        editor.reset()
    if key==KEYS['SQUARE_BRACKETS_LEFT']:
        editor.trim_left()
    if key==KEYS['SQUARE_BRACKETS_RIGHT']:
        editor.trim_right()

def key_event_mode(editor, key, mode):
    if key>=KEYS['NUM0'] and key < KEYS['NUM0']+10:
        mode = key-KEYS['NUM0']
        if mode == 1:
            editor.message = 'Contrast Mode'
        if mode == 2:
            editor.message = 'Brightness Mode'
        if mode == 3:
            editor.message = 'Saturation Mode'
        if mode == 4:
            print('준비중')
    return mode

def key_event_action(editor, key, mode):
    d = 1
    if kb.is_pressed("shift") == True:
        d = 10
    if (key==ord('q') or key==ord('Q')) and mode==1:
        editor.move_contrast(-d)
    if (key==ord('w') or key==ord('W')) and mode==1:
        editor.move_contrast(d)
    if (key==ord('q') or key==ord('Q')) and mode==2:
        editor.move_brightness(-d)
    if (key==ord('w') or key==ord('W')) and mode==2:
        editor.move_brightness(d)
    if (key==ord('q') or key==ord('Q')) and mode==3:
        editor.move_saturation(-d)
    if (key==ord('w') or key==ord('W')) and mode==3:
        editor.move_saturation(d)

def edit(frames, filename, fps):
    editor = Editor(frames, filename, fps)
    mode = 0
    while True:
        vis = editor.get_vis()
        cv2.imshow('editor', vis)
        key = cv2.waitKeyEx()
        #print(key)
        if key==KEYS['ESC']:
            cv2.destroyAllWindows()
            exit()
        if key==KEYS['F3']:
            return None
        if key==KEYS['SPACE']:
            print('Encoding ...')
            return editor.get()
        if key==KEYS['TAB']:
            editor.set_source_view_mode()
        key_event_common(editor, key)
        mode = key_event_mode(editor, key, mode)
        key_event_action(editor, key, mode)
