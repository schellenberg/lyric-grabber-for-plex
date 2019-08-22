# -*- coding: utf-8 -*-


"""
	This module downloads lyrics from LYRICSMODE. The URL format is:

		http://www.lyricsmode.com/lyrics/<first char of artist>/<artist>/<title>.html

	LYRICSMODE only uses non-alphanumeric ascii in it its urls. It replaces spaces with
	underscores. It removes every non-alphanumeric except '-' from artist names.
	
	LYRICSMODE also replaces some accented characters in artist with non-accented.
	Uses correction mapping for known exception to artist names.
"""

from __future__ import print_function
from __future__ import unicode_literals

import re
import string
import requests

try:
	from string  import ascii_lowercase as LOWERCASE_CHARS
except ImportError:
	# Python27
	from string  import lowercase as LOWERCASE_CHARS

from requests import ConnectionError, HTTPError, Timeout
from bs4 import BeautifulSoup

from .build_requests import get_lyrico_headers
from .lyrics_helper import remove_accents, test_lyrics


# Defining 'request_headers' outside download function makes a single profile
# per lyrico operation and not a new profile per each download in an operation.
request_headers = get_lyrico_headers()

# This correction mapping only is valid for top approx 3000 artists which LYRICSMODE
# displays as lists.
LYRICSMODE_CORRECTION = {
	'the_all_american_rejects': 'all_american_rejects',
	'acdc':'ac_dc',
	'die_arzte': 'die_rzte',
	'gilbert_becaud': 'gilbert_bcaud',
	'yo': 'y'
}

def download_from_lyricsmode(song=None):
	
	"""
		Takes reference to the song object as input and
		adds lyrics to self.lyrics or add error string to self.error
		property of the song object. 
	"""


	# temp var to hold value for final checking
	lyrics = None

	# Match everything accept lowercase alphabets, numbers, spaces and dashes
	regex_non_alphanumeric = re.compile(r'[^a-z0-9\s\-]+')

	# Replace accented characters by non-accented before parsing regex
	artist = regex_non_alphanumeric.sub('', remove_accents(song.artist).lower())
	title = regex_non_alphanumeric.sub('', song.title.lower())

	# Match multiple spaces or dashes and replace them by underscores 
	regex_underscores = re.compile(r'[\s|\-]+')
	artist = regex_underscores.sub('_', artist)
	title = regex_underscores.sub('_', title)

	# Check for corrections
	if artist in LYRICSMODE_CORRECTION:
		artist = LYRICSMODE_CORRECTION[artist]

	# If the first char of artist is not a alphabet, use '0-9'
	first_artist_char = artist[0]
	if first_artist_char not in LOWERCASE_CHARS:
		first_artist_char = '0-9'

	lyricsmode_url = 'http://www.lyricsmode.com/lyrics/%s/%s/%s.html' % (first_artist_char, artist, title)
	try:
		print('\tTrying LYRICSMODE:', lyricsmode_url)

		res = requests.get(lyricsmode_url, headers = request_headers)
		res.raise_for_status()
		
	# Catch network errors
	except (ConnectionError, Timeout):
		song.error = 'No network connectivity.'
	except HTTPError as e:
		song.error = 'Lyrics not found. Check artist or title name.'
	
	# No exceptions raised and the HTML for lyrics page was fetched		
	else:
		soup = BeautifulSoup(res.text, 'html.parser')

		# For lyricsmode, the lyrics are present in a div with id 'lyrics_text'
		lyrics_text = soup.find(id='lyrics_text')
		for tag in lyrics_text.find_all('div'):
			tag.clear()

		lyrics = lyrics_text.get_text().strip() if lyrics_text else None

	# Final check
	if test_lyrics(lyrics):
		song.lyrics = lyrics
		song.source = 'LrMOD'
		song.error = None
	else:
		# Don't overwrite and previous errors
		if not song.error:
			song.error = 'Lyrics not found. Check artist or title name.'
