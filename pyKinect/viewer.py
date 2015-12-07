from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from multiprocessing import Queue
from libkinect import Kinect

class KinectViewer(FloatLayout):
    index = NumericProperty(None)
    kinect = ObjectProperty(None)
    queue = ObjectProperty(None)
    texture = ObjectProperty(None)

    def on_index(self, instance, value):
        self.queue = Queue()
        self.texture = Texture.create((640, 480))
        self.kinect = Kinect(self.process_kinect, index=value,
                             colorfmt='luminance', use_video=True,
                             use_depth=False)
        Clock.schedule_interval(self.pop_queue, 0)

    def process_kinect(self, kinect, kwargs):
        self.queue.put(kinect['video_str'])

    def pop_queue(self, *largs):
        try:
            depth = self.queue.get(0)
        except:
            return
        self.texture.blit_buffer(depth, colorfmt='luminance')
        self.canvas.ask_update()

class KinectViewerApp(App):
    def build(self):
        root = BoxLayout()
        root.add_widget(KinectViewer(index=0))
        root.add_widget(KinectViewer(index=1))
        return root

KinectViewerApp().run()
