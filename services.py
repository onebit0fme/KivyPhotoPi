__author__ = 'onebit0fme'
from os import path
from os import listdir
from datetime import date, time, datetime
from PIL import Image as PIL_Image
from PIL import ExifTags
import datetime
from random import choice, shuffle, sample

HOME = path.expanduser("~")
# TODO: choose photo library path by user input
GALLERY_PATH = path.join(HOME, "PycharmProjects/PhotoPi/photos/")


class Media(object):
    def __init__(self, media_path, ext, timestamp, size, tags=[], description=""):
        if ext in (".jpg", ".jpeg", ".png", ".gif"):
            self._type = "IMG"
        elif ext in (".mov", ".avi", ".mkv"):
            self._type = "VID"
        self._ext = ext

        self.path = media_path
        if timestamp:
            self.date = timestamp.date()
            self.time = timestamp.time()
            self.timestamp = timestamp
        else:
            self.date = self.time = self.timestamp = None
        self.tags = tags
        self.description = description
        self._size = size
        self.height = size[1]
        self.width = size[0]

    def __repr__(self):
        return str(self.path)

    @property
    def is_image(self):
        return self._type == "IMG"

    @property
    def is_video(self):
        return self._type == "VID"

    @property
    def is_todays_date(self):
        n = date.today()
        return n.day == self.date.day and n.month == self.date.month


class ImageCollector(list):
    """
    class contains a list of Image objects retrieved from gallery folder
    Gallery folder format: single-level folders containing images/videos, description.txt, and tags.txt
    Accepted image formats: .jpg, .jpeg, .png
    Accepted video formats: .mov, .avi, .mkv
    """
    def __init__(self, **kwargs):
        super(ImageCollector, self).__init__(**kwargs)
        # TODO: get path from input
        self.gallery_path = GALLERY_PATH
        self.tags = set()
        self.folders = [d for d in listdir(self.gallery_path) if path.isdir(path.join(self.gallery_path, d))]

        for folder in self.folders:
            folder_path = path.join(self.gallery_path, folder)
            # READ tags.txt FILE
            tags = []
            if path.exists(path.join(folder_path, "keywords.txt")):
                tags_file = open(path.join(folder_path, "keywords.txt"), "r")
                tags = tags_file.read().split(',')   # I assume no one would make any new lines
                tags_file.close()
            ###
            # READ description.txt FILE
            description = ""
            if path.exists(path.join(folder_path, "description.txt")):
                d_file = open(path.join(folder_path, "description.txt"), "r")
                description = d_file.read()
                d_file.close()
            ###
            for f in listdir(folder_path):
                # NOTE: skipping any nested folders intentionally to keep gallery flat and clean.
                if path.splitext(f)[1].lower() in (".jpg", ".jpeg", ".png"):

                    image_path = path.join(folder_path, f)
                    open_image = PIL_Image.open(image_path)   # I strongly believe PIL closes image by itself ;)
                    # Retrieve exif info
                    try:
                        _exif = open_image._getexif()
                        # exif = {
                        #     ExifTags.TAGS[k]: v
                        #     for k, v in _exif.items()
                        #     if k in ExifTags.TAGS
                        # }
                        dto = _exif.get(0x9003)
                        timestamp = datetime.datetime.strptime(dto, '%Y:%m:%d %H:%M:%S')
                    except (AttributeError, KeyError, TypeError):
                        timestamp = None
                    ###
                    image = Media(media_path=str(image_path),
                                  ext=path.splitext(f)[1].lower(),
                                  size=open_image.size,
                                  timestamp=timestamp,
                                  tags=tags,
                                  description=description)
                    self.tags.update(tags)
                    self.append(image)

    def get_random_img(self):
        return choice(self)

    def get_images_from_folder(self, index):
        return self.all_images

    def generator_this_day_in_history(self, length=None):
        length = len(self) if length > len(self) or not length else length
        for image in sample(self, length):
            if image.is_todays_date:
                yield image

    def generator_shuffled(self, length=None):
        length = len(self) if length > len(self) or not length else length
        for image in sample(self, length):
            yield image

    def generator_by_tags(self, tags, length=None):
        length = len(self) if length > len(self) or not length else length
        for image in sample(self, length):
            if all(tag in image.tags for tag in tags):
                yield image

    def get_sorted_by_date(self, reverse=False):
        l = [img for img in self if img.timestamp]
        s = sorted(l, key=lambda img: img.timestamp, reverse=reverse)
        for image in s:
            yield image
