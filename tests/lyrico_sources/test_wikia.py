import unittest
from tests.dummy import DummySong
from lyrico.lyrico_sources.lyric_wikia import download_from_lyric_wikia

class TestWikia(unittest.TestCase):

    def test_download_from_lyric_wikia(self):
        song = DummySong('Azure Ray', 'Scattered Like Leaves')
        download_from_lyric_wikia(song)
        self.assertIsNone(song.error)
        self.assertIsNotNone(song.lyrics)
        self.assertEqual(song.lyrics[0:22], 'If you could guess how')
        self.assertEqual(song.lyrics[-12:], ' keep moving')
