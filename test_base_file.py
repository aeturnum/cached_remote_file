import inspect
import unittest
import os

from cached_remote_file import BaseFile

TEST_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
TEST_DATA_DIRECTORY = 'test_data'

class TestCRF(unittest.TestCase):
    def setUp(self):
        self.test_file_base = os.path.join(TEST_DIRECTORY, TEST_DATA_DIRECTORY, 'data')
        self.test_file_path = self.test_file_base + '.test'
        backup_file_path = self.test_file_base

        # reset contents
        test_file = open(self.test_file_path, 'w')
        backup_file = open(backup_file_path, 'r')
        test_file.write(backup_file.read())
        test_file.close()

        self.bf = BaseFile(self.test_file_base, 'test')
        self.bf2 = BaseFile(self.test_file_base, 'test')

    def tearDown(self):
        self.bf.close()
        self.bf2.close()

    def read_file(self, length=-1):
        return open(self.test_file_path, 'r').read(length)

    def test_read_base(self):
        self.assertEqual(self.bf.read(), self.read_file()) 
        self.assertEqual(self.bf.read(10), self.read_file(10)) 

    def test_write_base(self):
        content = 'blah'
        self.bf.save(content)

        self.assertEqual(self.bf.read(), self.read_file())
        self.assertEqual(self.bf.read(2), self.read_file(2))

    def test_write_lock(self):
        self.bf.open('w')
        self.assertTrue(os.path.exists(self.bf.lock_path))

        try:
            open(self.bf.lock_path, 'w')
            self.assertTrue(False)
        except:
            pass

    def test_write_lock_open(self):
        self.bf.open('w')

        self.assertFalse(self.bf2.open('w'))
        self.assertFalse(self.bf2.open('r'))

        self.bf.close()

        self.assertTrue(self.bf2.open('w'))
        self.assertFalse(self.bf2.open('r'))

        self.bf2.close()

        self.assertTrue(self.bf2.open('r'))
        self.assertTrue(self.bf2.open('w'))
