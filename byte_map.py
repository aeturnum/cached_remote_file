
class Chunk(object):
    def __init__(self, start, end, tag=None):
        if start > end:
            raise ValueError("Start[{}] must be smaller than end[{}]!".format(start, end))
        self.start = start
        self.end = end
        self.tag = tag

    def overlap(self, other):
        """
        :param Chunk chunk: 
        :return Chunk, list[Chunk]: Part within this chunk, list of non-overlapping chunks
        """
        other = self._check_type(other)

        #print('{}:{}'.format(self, other))
        first = None
        mid = None
        last = None
        # no overlap
        if other > self:
            # no overlap
            #print('{}:{} - No Overlap'.format(self, other))
            return [self, other]
        if other < self:
            # no overlap
            #print('{}:{} - No Overlap'.format(self, other))
            return [other, self]


        if other.start != self.start:
            # one block starts before the other
            # [self]
            #    [other]
            # -or-
            #     [self]
            # [other]
            if other.start < self.start:
                first = other.child(e=self.start - 1)
            else:
                first = self.child(e=other.start - 1)
            #print('{}:{} -> first: {}'.format(self, other, first))

        if other.end != self.end:
            # one block ends after the other
            # [self]
            #    [other]
            # -or-
            #     [self]
            # [other]
            if other.end > self.end:
                last = other.child(s=self.end + 1)
            else:
                last = self.child(s=other.end + 1)
            #print('{}:{} -> last: {}'.format(self, other, last))

        mid = self.child(s = first.end + 1 if first else None, e = last.start - 1 if last else None)
        #print('{}:{} -> mid:{}'.format(self, other, mid))

        final = [chunk for chunk in [first, mid, last] if chunk]
        #print('{}:{} -> {}'.format(self, other, final))
        return final


    def child(self, s=None, e=None):
        if not s:
            s = self.start
        if not e:
            e = self.end
        return Chunk(s, e, self.tag)

    def _check_type(self, other):
        if type(other) is list:
            return Chunk(other[0], other[1])
        if type(self) is not type(other):
            raise ValueError("Chunk only works on other chunks!")
        return other

    def __lt__(self, other):
        other = self._check_type(other)
        return self.end < other.start

    def __le__(self, other):
        other = self._check_type(other)
        return self < other or self == other

    def __eq__(self, other):
        other = self._check_type(other)
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        other = self._check_type(other)
        return not (self.start == other.start and self.end == other.end)

    def __gt__(self, other):
        other = self._check_type(other)
        return self.start > other.end

    def __ge__(self, other):
        other = self._check_type(other)
        return self > other or self == other

    def does_overlap(self, other):
        other = self._check_type(other)
        return not (other.start > self.end or other.end < self.start)

    def merge(self, other):
        other = self._check_type(other)
        if self.tag != other.tag:
            raise ValueError('Tags do not match! Cannot merge!')
        if not self.does_overlap(other):
            raise ValueError('Chunks do not overlap!')
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)

    def range(self):
        return [self.start, self.end]

    @staticmethod
    def from_dict(self, d):
        return Chunk(d['start'], d['end'], d['tag'])

    def to_dict(self):
        return {
            'start': self.start,
            'end': self.end,
            'tag': self.tag
        }

    def __str__(self):
        tag = ''
        if self.tag:
            tag = '|{}'.format(self.tag)
        return 'C{}[{}:{}]'.format(tag, self.start, self.end)

    def __repr__(self):
        return str(self)

class ByteMap(object):
    def __init__(self, size, default_tag='remote'):
        self.chunks = [Chunk(0, size - 1, default_tag)]

    def classify(self, new_chunk):
        for chunk in self.chunks:
            if chunk.does_overlap(chunk):
                return chunk.overlap(new_chunk)

        raise ValueError('Chunk {} does not overlap at all!')

    def add(self, new_chunk):
        chunk_to_remove = None
        for i, chunk in enumerate(self.chunks):
            if chunk.does_overlap(new_chunk):
                # break up old chunk into new 
                new_chunk, old_chunks = new_chunk.overlap(chunk)
                # add new data to split old data
                old_chunks.append(new_chunk)
                # sort the result
                old_chunks.sort()
                # remove the chunk we overlap with
                self.chunks.remove(chunk)
                for j, piece in enumerate(old_chunks):
                    # insert newly generated chunks in order
                    self.chunks.insert(i + j, piece)

                return

        raise ValueError("No overlap at all!")

    def __str__(self):
        return 'ByteMap[{}]'.format(','.join(map(str,self.chunks)))


