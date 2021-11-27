import os
import unittest

from Pyhole import Pyhole
from YouTubeRule import YouTubeRule


class TestPyhole(unittest.TestCase):
    pyhole = Pyhole('192.168.0.2', os.getenv('PI_PASSWD'))

    def test_constructor(self):
        self.assertIsNotNone(self.pyhole.host)
        self.assertIsNotNone(self.pyhole.password)
        self.assertIsNotNone(self.pyhole.session)

    def test_authentication(self):
        self.pyhole.authenticate()

    def test_bad_token(self):
        self.pyhole.token = 'expired'
        x = self.pyhole.get_domains()
        pass

    def test_get_domains(self):
        x = self.pyhole.get_domains()
        pass

    def test_youtube(self):
        yt_rule = YouTubeRule(self.pyhole)
        is_blocked = yt_rule.youtube_is_blocked()
        yt_rule.flip()
        new_status = yt_rule.youtube_is_blocked()
        self.assertNotEqual(is_blocked, new_status)


# TODO: Test multiple groups

if __name__ == '__main__':
    unittest.main()
