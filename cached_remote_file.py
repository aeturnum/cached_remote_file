import requests
import json
from os import path

# "API" from https://docs.python.org/2.4/lib/bltin-file-objects.html

class FileMap(object):
    _SECTIONS = 'sections'

    def __init__(self, file_path):
        super(FileMap, self).__init__()
        self.file_path = file_path
        self.map = None

    def load(self):
        if self.map is None:
            map_fp = open(self.meta_file_path, 'r')
            self.map = json.load(map_fp)
            map_fp.close()

    def write(self):
        if self.map is None:
            return

        count = 0
        while count < 10:
            try:
                fp = open(self.file_path, 'w')
                json.dump(fp)
                fp.close()
                return
            except OSError as e:
                sleep(0.1)
                count += 1
                pass

    def add(self, offset, length):
        sections = self.map[_SECTIONS]
        end = offset + length
        extend = None
        eliminate = None
        index = 0
        for sec in sections:

            # s: 0123
            # n:  345678
            if offset == sec[1]:
                extend = sec

            # s: 012  5678
            # n:   234
            if end == sec[0] - 1:
                eliminate = sec

            if offset > sec[0]
                index += 1

        if extend:
            extend[1] = end
            if eliminate:
                sections.remove(eliminate)
        else:
            sections.insert(index, [offset, end])
    
    def missing_pieces(self, offset, length):
        sections = self.map[_SECTIONS]
        end = offset + length






class RemoteRequest(object):
    def __init__(self, target, meta_file_path, data_file_path, offset=0, length=None):
        self.target = target
        self.map = FileMap(meta_file_path)
        self.cache_file_path = data_file_path
        self.offset = 0
        self.length = length

    def _headers(self):
        headers = {}
        if self.length or self.offset:
            range_str = 'bytes={}-'.format(
                offset,
                self.length if self.length else '')
            headers['Range'] = range_str

        return headers

    def _load_map(self):
        self.map.load()

    def _write(self, content):
        count = 0
        while count < 10:
            try:
                self._load_map()
                fp = open(self.cache_file_path, 'wb')
                fp.seek(self.offset)
                fp.write(content)
                fp.close()
                return
            except OSError as e:
                sleep(0.1)
                count += 1
                pass

    def go(self):
        r = requests.get(
                self.target,
                headers = self._headers()
            )

        self._write(r.content)
        return len(r.content)


class CachedRemoteFile(object):
    WHENCE_ABSOLUTE = 0
    WHENCE_RELATIVE = 1
    WHENCE_END = 2

    _DATA_EXT = 'data'
    _META_EXT = 'meta'

    def __init__(self, working_dir, name, remote_location):
        self.working_dir = working_dir
        self.name = name
        self.remote_location = remote_location

        self.data_file_path = path.join(self.working_dir, self.name, self._DATA_EXT)
        self.meta_file_path = path.join(self.working_dir, self.name, self._META_EXT)
        self.data_file = None
        self.meta_file = None

        self.downloaded_ranges = []

        self.offset = 0
        self.closed = False
        self.mode = 'r'
        self.newlines = '\n'

        self._open()

    def _open(self):
        if not path.isfile(self.data_file_path):
            open(self.data_file_path, 'w').close()
        if not path.isfile(self.meta_file_path):
            meta = open(self.meta_file_path, 'w')
            meta.write(json.dumps([]))
            meta.close()

    def close(self):
        if self.data_file:
            self.data_file.close()
        if self.meta_file:
            self.meta_file.close()

    def flush(self):
        self.data_file.flush()
        self.meta_file.flush()

    def fileno(self):
        return None

    def isatty(self):
        return False

    def next(self):
        pass

    def read(self, length=None):
        if length:


    def readline(self, length=None):
        pass

    def readlines(self, length=None):
        pass

    def seek(self, offset, whence=0):
        pass

    def tell(self):
        return self.offset

    def truncate(self, size):
        pass

    def write(self, data):
        pass

    def writelines(self, data):
        for datum in data:
            self.write(datum)