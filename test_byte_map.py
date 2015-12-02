import unittest
from byte_map import Chunk, ByteMap

class TestChunk(unittest.TestCase):

    # 34567
    tchunk = Chunk(3,7)

    def check_overlap(self, comp, expected):
        result = self.tchunk.overlap(comp)

        self.assertEqual(len(expected), len(result))
        for res, exp in zip(result, expected):
            self.assertEqual(res, exp)

    def test_no_overlap(self):
        a = Chunk(1,2)
        b = Chunk(8, 10)

        self.check_overlap(a, [a, self.tchunk])
        self.check_overlap(b, [self.tchunk, b])

    def test_end_overlap(self):
        a = Chunk(1, 3)
        b = Chunk(1, 5)
        c = Chunk(1, 7)

        self.check_overlap(a, [[1,2], [3,3], [4, 7]])
        self.check_overlap(b, [[1,2], [3,5], [6, 7]])
        self.check_overlap(c, [[1,2], [3,7]])

    def test_start_overlap(self):
        a = Chunk(7, 10)
        b = Chunk(6, 12)
        c = Chunk(3, 12)

        self.check_overlap(a, [[3,6], [7,7], [8,10]])
        self.check_overlap(b, [[3,5], [6,7], [8,12]])
        self.check_overlap(c, [[3,7], [8,12]])

    def test_total_overlap(self):
        a = Chunk(3, 7)
        b = Chunk(4, 6)
        c = Chunk(1, 12)

        self.check_overlap(a, [[3,7]])
        self.check_overlap(b, [[3,3], [4,6], [7,7]])
        self.check_overlap(c, [[1,2], [3,7], [8,12]])

    def test_tags(self):
        a = Chunk(1, 3, 'a')
        b = Chunk(2, 4, 'b')

        self.assertTrue('a' in a)
        self.assertTrue('b' not in a)
        self.assertTrue('a' not in b)
        self.assertTrue('b' in b)

        overlaps = a.overlap(b)
        self.assertEqual(len(overlaps), 3)
        self.assertTrue('a' in overlaps[0])
        self.assertTrue('b' not in overlaps[0])
        self.assertTrue('a' in overlaps[1])
        self.assertTrue('b' in overlaps[1])
        self.assertTrue('a' not in overlaps[2])
        self.assertTrue('b' in overlaps[2])

    def test_operators(self):
        a = Chunk(1,4)
        b = Chunk(2,6)
        c = Chunk(6,9)

        self.assertTrue(a < c)
        self.assertFalse(a < b)
        self.assertFalse(a > b)
        self.assertTrue(a <= c)
        self.assertTrue(a == a)
        self.assertTrue(a != b)
        self.assertTrue(a != c)
        self.assertTrue(c > a)

class TestByteMap(unittest.TestCase):

    def setUp(self):
        self.tbm = ByteMap(15, 'a')

    def test_classify(self):
        b = Chunk(5, 10, 'b')

        overlaps = self.tbm.classify(b)

        self.assertTrue('a' in overlaps[0])
        self.assertTrue('b' not in overlaps[0])
        self.assertTrue('a' in overlaps[1])
        self.assertTrue('b' in overlaps[1])
        self.assertTrue('a' in overlaps[2])
        self.assertTrue('b' not in overlaps[2])

    def test_missing(self):
        b = Chunk(5, 10, 'b')

        needed = self.tbm.missing(b)
        self.assertEqual(len(needed), 2)

        for c in needed:
            self.assertTrue('a' in c)
            self.assertTrue('b' not in c)

    def test_add(self):
        b = Chunk(5, 10, 'b')

        self.tbm.add(b)
        tbm_chunks = self.tbm.chunks
        self.assertEqual(len(tbm_chunks), 3) 
        
        self.assertTrue('a' in tbm_chunks[0])
        self.assertTrue('b' not in tbm_chunks[0])
        self.assertTrue('a' in tbm_chunks[1])
        self.assertTrue('b' in tbm_chunks[1])
        self.assertTrue('a' in tbm_chunks[2])
        self.assertTrue('b' not in tbm_chunks[2])