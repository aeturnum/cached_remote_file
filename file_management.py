import os
from os import path

class BaseFile(object):
    def __init__(self, path, extension=None):
        self._path = path
        self.extension = extension
        self.handle = None
        self.mode = None
        self.lock = None

    def __del__(self):
        self.close()

    @property
    def path(self):
        if self.extension is None:
            raise ValueError("Must set an extension for this file!")
        return "{}.{}".format(self._path, self.extension)

    @property
    def lock_path(self):
        return "{}.{}".format(self.path, 'lock')

    @property
    def locked(self):
        return path.exists(self.lock_path)

    def open(self, mode='r'):
        if self.handle and self.mode == mode:
            return True

        if self.locked:
            return False

        if mode == 'r':
            try:
                self.handle = open(self.path, 'r')
                self.mode = 'r'
            except Exception as e:
                print e
                return False

        elif mode == 'w':
            try:
                # ghetto touch
                self.lock = open(self.lock_path, 'w')
                # write file
                self.handle = open(self.path, 'w')
                self.mode = 'w'
            except Exception as e:
                print e
                return False

        return True

    def close(self):
        if not self.handle:
            return

        self.handle.close()
        if self.lock:
            self.lock.close()
            os.remove(self.lock_path)

        self.lock = None # clear
        self.handle = None
        self.mode = None

    def save(self, content):
        if self.open('w'):
            self.handle.seek(0)
            self.handle.write(content)
            self.close()
            return True

        return False

    def read(self, length=-1, offset=0):
        if self.open():
            self.handle.seek(offset)
            result = self.handle.read(length)
            self.close()
            return result

        return None

    def __str__(self):
        l = 'L' if self.locked else '_'
        return "BF[{}|{}]:{}".format(self.mode or '_', l, self.path)

    def __repr__(self):
        return str(self)