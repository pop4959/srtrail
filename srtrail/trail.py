import struct
import zipfile
import tempfile
import os

from srtrail.imageinfo import ImageInfo
from srtrail.layer import Layer
from srtrail.property import Property


class Trail:
    def __init__(self, name='Untitled', author='Unknown', description=''):
        self.version = 4
        self.name = name
        self.author = author
        self.description = description
        self.last_updated = 0
        self.icon = 'icon'
        self.images = []
        self.layers = []
        self.keep_default_trail = False
        self.workshop_id = 0

    def load(self, path):
        with zipfile.ZipFile(path, 'r') as srt:
            with srt.open('settings.trail', 'r') as settings:
                self.version = struct.unpack('<i', settings.read(4))[0]
                self.name = settings.read(struct.unpack('<b', settings.read(1))[0]).decode('ascii')
                self.author = settings.read(struct.unpack('<b', settings.read(1))[0]).decode('ascii')
                self.description = settings.read(struct.unpack('<b', settings.read(1))[0]).decode('ascii')
                self.last_updated = struct.unpack('<q', settings.read(8))[0]
                self.icon = settings.read(struct.unpack('<b', settings.read(1))[0]).decode('ascii')
                image_count = struct.unpack('<i', settings.read(4))[0]
                for i in range(image_count):
                    key = settings.read(struct.unpack('<b', settings.read(1))[0]).decode('ascii')
                    name = settings.read(struct.unpack('<b', settings.read(1))[0]).decode('ascii')
                    self.images.append(ImageInfo(key, name))
                layer_count = struct.unpack('<i', settings.read(4))[0]
                for i in range(layer_count):
                    type = struct.unpack('<b', settings.read(1))[0]
                    layer = Layer(type)
                    property_count = struct.unpack('<i', settings.read(4))[0]
                    for j in range(property_count):
                        name = settings.read(struct.unpack('<b', settings.read(1))[0]).decode('ascii')
                        value = settings.read(struct.unpack('<b', settings.read(1))[0]).decode('ascii')
                        layer.properties.append(Property(name, value))
                    self.layers.append(layer)
                if self.version >= 2:
                    self.keep_default_trail = False if struct.unpack('<b', settings.read(1))[0] == 0 else True
                if self.version >= 3:
                    self.workshop_id = struct.unpack('<q', settings.read(8))[0]
                self.version = 4

    def save(self, path):
        data = b''
        data += struct.pack(
            '<ib{}sb{}sb{}sqb{}si'.format(len(self.name), len(self.author), len(self.description), len(self.icon)),
            self.version, len(self.name), self.name.encode('ascii'), len(self.author), self.author.encode('ascii'),
            len(self.description), self.description.encode('ascii'), self.last_updated, len(self.icon),
            self.icon.encode('ascii'), len(self.images))
        for image in self.images:
            data += struct.pack('<b{}sb{}s'.format(len(image.key), len(image.name)), len(image.key),
                                image.key.encode('ascii'), len(image.name), image.name.encode('ascii'))
        data += struct.pack('<i', len(self.layers))
        for layer in self.layers:
            data += struct.pack('<bi', layer.type, len(layer.properties))
            for property in layer.properties:
                data += struct.pack('b{}sb{}s'.format(len(property.name), len(property.value)), len(property.name),
                                    property.name.encode('ascii'), len(property.value), property.value.encode('ascii'))
        data += struct.pack('<bq', 1 if self.keep_default_trail else 0, self.workshop_id)
        tempfd, temppath = tempfile.mkstemp()
        os.close(tempfd)
        with zipfile.ZipFile(path, 'r') as infile:
            with zipfile.ZipFile(temppath, 'w') as outfile:
                outfile.comment = infile.comment
                for item in infile.infolist():
                    if item.filename != 'settings.trail':
                        outfile.writestr(item, infile.read(item.filename))
        os.remove(path)
        os.rename(temppath, path)
        with zipfile.ZipFile(path, 'a') as srt:
            srt.writestr('settings.trail', data)
