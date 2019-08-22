# -*- coding: utf-8 -*-


"""
	This module downloads lyrics from musixmatch. The URL structure is:
	
	https://www.musixmatch.com/lyrics/<artist>/<title>

	musixmatch uses dashes, '-', for spaces and removes every other non-alphanumeric characters.
	It also replaces apostrophes with dashes. So "Don't" becomes "Don-t". There are few
	exceptions but the server seems to be a bit flexible with URLs.
"""

from __future__ import print_function
from __future__ import unicode_literals

import re
import sys
import requests

try:
	from urllib.parse  import quote
except ImportError:
	# Python27
	from urllib import quote

from requests import ConnectionError, HTTPError, Timeout
from bs4 import BeautifulSoup

from .build_requests import get_lyrico_headers
from .lyrics_helper import test_lyrics

# Defining 'request_headers' outside download function makes a single profile
# per lyrico operation and not a new profile per each download in an operation.
request_headers = get_lyrico_headers()


def download_from_musix_match(song):
	
	"""
		Takes reference to the song object as input and
		adds lyrics to self.lyrics or add error string to self.error
		property of the song object. 
	"""


	# temp var to hold value for final checking
	lyrics = None

	# Replace upper(apostrophe) commas with dashes '-'
	artist = song.artist.replace("'", '-')
	title = song.title.replace("'", '-')

	# This regex mathches anything other than Alphanumeric, spaces and dashes
	# and removes them.
	# Make regex unicode aware 're.UNICODE' for Python27. It is redundant for Python3.
	regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
	artist = regex_non_alphanum.sub('', artist)
	title = regex_non_alphanum.sub('', title)
	
	# Replace spaces with dashes to imporve URL logging. 
	regex_spaces = re.compile(r'[\s]+', re.UNICODE)
	artist = regex_spaces.sub('-', artist)
	title = regex_spaces.sub('-', title)

	# See lyric_wikia module for comments on manual encoding
	if sys.version_info[0] < 3:
		artist = artist.encode('utf-8')
		title = title.encode('utf-8')

	mxm_url = 'https://www.musixmatch.com/lyrics/%s/%s' % (quote(artist), quote(title))

	try:
		print('\tTrying musixmatch:', mxm_url)

		res = requests.get(mxm_url, headers = request_headers)
		res.raise_for_status()

	# Catch network errors
	except (ConnectionError, Timeout) as e:
		song.error = 'No network connectivity.'
	except HTTPError as e:
		print(e)
		song.error = 'Lyrics not found. Check artist or title name.'
	
	# No exceptions raised and the HTML for lyrics page was fetched		
	else:
		soup = BeautifulSoup(res.text, 'html.parser')

		# For musixmatch, lyrics are in <span class="lyrics__content__ok">
		lyric_html = ""
		lyric_tags = soup.find_all('span','lyrics__content__ok')
		for tag in lyric_tags:
			lyric_html += tag.get_text().strip() + "\n"
		lyrics = lyric_html if lyric_html else None

	# Final check
	if test_lyrics(lyrics):
		song.lyrics = lyrics
		song.source = 'mXm'
		song.error = None
	else:
		# Don't overwrite and previous errors
		if not song.error:
			song.error = 'Lyrics not found. Check artist or title name.'
