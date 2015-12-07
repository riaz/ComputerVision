import freenect
from time import sleep
from multiprocessing import Process, Value
import numpy as np
import cv

def convert_depth_to_8bit(depth):
    np.clip(depth, 0, 2**11 - 1, depth)
    depth >>= 3
    depth = depth.astype(np.uint8)
    return depth

def process(quit, callback, **kwargs):
    size = (-1, -1)

    while quit.value == 0:
        use_depth = kwargs.get('use_depth', True)
        use_video = kwargs.get('use_video', False)
        video_format = kwargs.get('video_format', 'ir8')
        index = kwargs.get('index', 0)
        depth = None
        video = None
        depth_str = None
        video_str = None

        video_channels = 0
        if video_format == 'rgb':
            video_format = freenect.VIDEO_RGB
            video_channels = 3
        elif video_format == 'ir8':
            video_format = freenect.VIDEO_IR_8BIT
            video_channels = 1
        else:
            assert('unsupported')

        if use_depth:
            # fetch depth from freenect
            depth = freenect.sync_get_depth(index=index)
            if depth is None:
                print 'Kinect: kinect not available, restarting in 5 seconds.'
                sleep(5)
                continue

            video = None
            if use_video:
                video = freenect.sync_get_video(index=index)

            # extract data & timestamp
            data, timestamp = depth

            # update image size from the first image
            if size == (-1, -1):
                size = data.shape[1], data.shape[0]
                print 'Kinect: size is', size

            data = convert_depth_to_8bit(data)

            # convert to opencv image
            depth = cv.CreateImageHeader(size, cv.IPL_DEPTH_8U, 1)
            cv.SetData(depth, data.tostring(), data.dtype.itemsize *
                       data.shape[1])

            cv.Flip(depth, depth, 0)
            depth_str = str(depth.tostring())

        if use_video:
            video = freenect.sync_get_video(index=index, format=video_format)
            if video is None:
                print 'Kinect: kinect not available, restarting in 5 seconds.'
                sleep(5)
                continue

            data, timestamp = video

            if size == (-1, -1):
                size = data.shape[1], data.shape[0]
                print 'Kinect: size is', size

            # convert to opencv image
            video = cv.CreateImageHeader(size, cv.IPL_DEPTH_8U, video_channels)
            cv.SetData(video, data.tostring(), data.dtype.itemsize *
                       data.shape[1] * video_channels)
            cv.Flip(video, video, 0)
            video_str = video.tostring()

        arg = {
            'depth': depth,
            'depth_str': depth_str,
            'video': video,
            'video_str': video_str,
            'size': size
        }

        if callback(arg, kwargs) is False:
            break

    for q in kwargs.values():
        if q.__class__.__name__ == 'Queue':
            while q.qsize(): q.get()

class Kinect(object):
    def __init__(self, callback, **kwargs):
        super(Kinect, self).__init__()
        self.quit = Value('i', 0, lock=True)
        self.kwargs = kwargs
        self.process = Process(target=process,
                               args=(self.quit, callback, ), kwargs=kwargs)
        self.process.daemon = True
        self.process.start()

    def stop(self):
        self.quit.value = 1

    def join(self):
        self.process.join()
