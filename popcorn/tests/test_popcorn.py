from datetime import date
import unittest

import redis

from popcorn import configs
configs.rdb = rdb = redis.Redis('localhost', db='13')
from popcorn import server


class TestPopcorn(unittest.TestCase):
    def test_submit_success(self):
        submission = ("POPCORN 0.1 x86_64 a564f30e-1e15-4546-831f-b000608b9889\n"
                      "v python 2.5 1.1 x86_64 openSUSE-11.4\n"
                      "v python-lint 1.1 1 noarch openSUSE-11.4\n")
        server.parse_popcorn(submission)
        self.assertEqual(rdb.get('global:nextSubmissionId'), '1')
        self.assertEqual(rdb.get('global:nextSystemId'), '1')
        self.assertEqual(rdb.get('global:nextPackageId'), '2')

    def tearDown(self):
        rdb.flushdb()