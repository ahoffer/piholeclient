import os
import unittest

from piholeclient.controllers import YouTubeRule
from piholeclient.models import Pihole


class PiholeClientTest(unittest.TestCase):
    # client = Pihole('localhost', os.getenv('PI_PASSWD'), port=8000)
    client = Pihole('192.168.0.2', os.getenv('PI_PASSWD'))

    def test_constructor(self):
        self.assertIsNotNone(self.client.password)
        self.assertIsNotNone(self.client.session)

    def test_authentication(self):
        self.client.authenticate()

    def test_bad_token(self):
        self.client.token = 'expired'
        x = self.client.get_domains()
        pass

    def test_get_domains(self):
        x = self.client.get_domains()
        pass

    def test_youtube(self):
        yt_rule = YouTubeRule(self.client)
        is_blocked = yt_rule.youtube_is_blocked()
        yt_rule.flip()
        new_status = yt_rule.youtube_is_blocked()
        self.assertNotEqual(is_blocked, new_status)


# TODO: Test multiple groups

if __name__ == '__main__':
    unittest.main()
