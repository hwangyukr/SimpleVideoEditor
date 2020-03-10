import cv2
import numpy as np
class Editor:
    def __init__(self, frames, filename, fps):
        self.origin = frames
        self.reset()

    def reset(self):
        self.target = self.origin.copy()
        self.frame = 0
        self.contrast = 1.0
        self.saturation = 0
        self.brightness = 0
        self.source_view_mode = False
        self.message = 'Initialized'

    def move_contrast(self, d):
        self.contrast += d / 100
        if self.contrast < 0.0: self.contrast = 0.0
        if self.contrast > 10.0: self.contrast = 10.0
        self.message = 'contrast : {}'.format(round(self.contrast,2))

    def move_brightness(self, d):
        self.brightness += d
        if self.brightness < -100: self.brightness = -100
        if self.brightness > 100: self.brightness = 100
        self.message = 'brightness : {}'.format(self.brightness)

    def move_saturation(self, d):
        self.saturation += d
        if self.saturation < -100: self.saturation = -100
        if self.saturation > 100: self.saturation = 100
        self.message = 'saturation : {}'.format(self.saturation)

    def move_frame(self, distance):
        self.frame += distance
        if self.frame < 0:
            self.frame = 0
        if self.frame > len(self.target)-1:
            self.frame = len(self.target)-1

    def remove_frame(self):
        if len(self.target) < 3:
            return
        del self.target[self.frame]
        if self.frame > len(self.target)-1:
            self.frame = len(self.target)-1

    def apply_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h = hsv[:,:,0].astype('int32')
        s = hsv[:,:,1].astype('int32')
        v = hsv[:,:,2].astype('int32')

        s = s + self.saturation  # 더하는게 채도
        s[s<0]=0
        s[s>255]=255

        vmin = v.min()
        vmax = v.max()
        #v = (v-vmin) / (vmax-vmin) * 255
        v = v + 0
        v[v>255]=255
        v[v<0]=0

        h = h.astype('uint8')
        s = s.astype('uint8')
        v = v.astype('uint8')

        rgb = cv2.cvtColor(np.array([h, s, v]).transpose(1,2,0), cv2.COLOR_HSV2BGR)
        rgb = rgb.astype('int32')
        rgb = rgb * self.contrast + self.brightness # 곱하는게 명도, 더하는게 밝기
        rgb[rgb>255]=255
        rgb[rgb<0]=0
        rgb = rgb.astype('uint8')
        return rgb

    def get_vis(self):
        vis = self.target[self.frame].copy()
        if self.source_view_mode == False:
            vis = self.apply_frame(vis)
        frame_info = '{}/{}'.format(self.frame, len(self.target)-1)
        vis = cv2.putText(vis, frame_info, (0,20), cv2.FONT_HERSHEY_COMPLEX  , 0.7, (150,0,150), 2)
        src_mode_info = ''
        if self.source_view_mode == True:
            src_mode_info = 'Before'
        vis = cv2.putText(vis, src_mode_info, (120,20), cv2.FONT_HERSHEY_SIMPLEX  , 0.7, (50,50,80), 2)
        vis = cv2.putText(vis, self.message, (250,20), cv2.FONT_HERSHEY_SIMPLEX  , 0.7, (20,150,30), 2)
        return vis

    def get(self):
        dest = []
        for frame in self.target:
            n = self.apply_frame(frame)
            dest.append(n)
            cv2.imshow('encoding...', n)
            if cv2.waitKey(1) == 27:
                break
        return dest
        #dest = map(self.apply_frame, self.target)
        #return list(dest)

    def trim_left(self):
        s = self.frame
        e = len(self.target)
        self.target = self.target[s:e]
        self.frame = 0

    def trim_right(self):
        s = 0
        e = self.frame
        self.target = self.target[s:e+1]
        self.frame = e

    def set_source_view_mode(self, source_view_mode=None):
        if source_view_mode == None:
            self.source_view_mode = not self.source_view_mode
        else:
            self.source_view_mode = self.source_view_mode
