__author__ = 'onebit0fme'

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle, Line, Ellipse, Rotate
from kivy.uix.label import Label
from kivy.uix.scatterlayout import Scatter
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget, EventLoop
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, BooleanProperty, StringProperty
from kivy.clock import Clock
from functools import partial
from kivy.event import EventDispatcher
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, FadeTransition, SwapTransition, WipeTransition, FallOutTransition, RiseInTransition, NoTransition
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.uix.settings import SettingsWithSidebar, SettingsWithSpinner, SettingsWithTabbedPanel, SettingsWithNoMenu, Settings, SettingsPanel
import datetime
from kivy.config import ConfigParser
from pprint import pprint
import re
from datetime import datetime

from os import path
from os import listdir

HOME = path.expanduser("~")
APP_PATH = "PycharmProjects/PhotoPi/"

class ImageCollector(object):
    def __init__(self):
        self.gallery_path = path.join(HOME, APP_PATH, "photos")
        self.folders = [d for d in listdir(self.gallery_path) if path.isdir(path.join(self.gallery_path,d))]
        self.all_images = []
        for file in listdir(path.join(self.gallery_path, self.folders[0])):
            if path.splitext(file)[1].lower() in (".jpg", ".jpeg"):
                self.all_images.append(path.join(self.gallery_path,self.folders[0], file))
        print self.folders

    def get_random_img(self):
        return path.join(self.gallery_path, self.folders[0], self.all_images[0])

    def get_images_from_folder(self, index):
        return self.all_images


class PhotoFrame(FloatLayout):
    image_path = StringProperty('')

class FramedImage(Image):
    pass

class CustomImage(Image):
    pass

class PhotoPiApp(App):

    def build(self):

        # carousel = Carousel(anim_type='out_expo')
        gallery = ImageCollector()
        # for image in gallery.get_images_from_folder(0):
        #     carousel.add_widget(PhotoFrame(image_path=image))

        img = gallery.get_random_img()
        l = Scatter(do_rotation=False)
        l.add_widget(FramedImage(source=img))

        ###############

        layout = GridLayout(orientation='horizontal', rows=1, size_hint_x=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_width=layout.setter('width'))
        for i in gallery.get_images_from_folder(0):
            im = CustomImage(source=i, size_hint_x=None)
            layout.add_widget(im)
        root = ScrollView()
        root.add_widget(layout)

        box = BoxLayout()
        box.add_widget(root)
        ################
        return box

    def on_pause(self):
        return True

    def on_resume(self):
        pass


    def get_color(self, color, opacity=None):
        if opacity:
            return self.colors[color]
        else:
            return self.colors[color]+(opacity,)

if __name__ == '__main__':
    PhotoPiApp().run()