import unittest
from tests.dummy import DummySong
from lyrico.lyrico_sources.musix_match import download_from_musix_match

class TestMusixMatch(unittest.TestCase):

    def test_download_from_musix_match(self):
        song = DummySong('Sarah Connor', 'Unendlich')
        download_from_musix_match(song)
        self.assertIsNone(song.error)
        self.assertIsNotNone(song.lyrics)
        self.assertEqual(song.lyrics[0:21], 'Immer wenn ich tiefer')
        self.assertEqual(song.lyrics[-12:], ', unendlich\n')
