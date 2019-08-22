import unittest
from tests.dummy import DummySong
from lyrico.lyrico_sources.az_lyrics import download_from_az_lyrics

class TestAzLyrics(unittest.TestCase):

    def test_download_from_az_lyrics(self):
        song = DummySong(u'Azure Ray', u'Don\'t Make A Sound')
        download_from_az_lyrics(song)
        self.assertIsNone(song.error)
        self.assertIsNotNone(song.lyrics)
        self.assertEqual(song.lyrics[0:21], 'You could go anywhere')
        self.assertEqual(song.lyrics[-21:], '\nand not make a sound')

