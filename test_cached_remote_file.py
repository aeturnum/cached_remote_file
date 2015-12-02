import unittest
import os
import inspect
import subprocess
import requests
import time

TEST_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
TEST_DATA_DIRECTORY = 'test_data'
REMOTE_FILE = 'http://localhost:8100/data'

class TestCRF(unittest.TestCase):
    def setUp(self):
        python_server_args = ['python', '-m', 'SimpleHTTPServer', '8100']
        cwd = os.path.join(TEST_DIRECTORY, TEST_DATA_DIRECTORY)
        self.server = subprocess.Popen(
            python_server_args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        time.sleep(0.1)

    def tearDown(self):
        self.server.kill()

    def test_read(self):
        data = requests.get(REMOTE_FILE)
        print 'data.content: {}'.format(data.content)
