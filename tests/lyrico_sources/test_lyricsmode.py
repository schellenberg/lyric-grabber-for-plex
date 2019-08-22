import unittest
from tests.dummy import DummySong
from lyrico.lyrico_sources.lyricsmode import download_from_lyricsmode

class TestLyricsmode(unittest.TestCase):

    def test_download_from_lyricsmode(self):
        song = DummySong(u'Azure Ray', u'4th of july')
        download_from_lyricsmode(song)
        self.assertIsNone(song.error)
        self.assertIsNotNone(song.lyrics)
        self.assertEqual(song.lyrics[0:24], 'We met on that wednesday')
        self.assertEqual(song.lyrics[-31:], 'I know this love will never die')

