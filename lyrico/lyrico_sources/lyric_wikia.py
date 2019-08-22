# -*- coding: utf-8 -*-


"""
	This module downloads lyrics from Lyric Wikia. Since it lyrics.wikia API is defunct
	since Jan, 2016 it relies on basic URL structure:
	
	http://lyrics.wikia.com/wiki/<artist>:<title>

	and then extracts lyrics from the HTML recieved.

        URL rules: http://lyrics.wikia.com/wiki/LyricWiki:Page_Names
"""

from __future__ import print_function
from __future__ import unicode_literals

import sys
import re
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


def download_from_lyric_wikia(song):
	
	"""
		Takes reference to the song object as input and
		adds lyrics to self.lyrics or add error string to self.error
		property of the song object. 
	"""


	# temp var to hold value for final checking
	lyrics = None


	# replace spaces with underscores. This prints nicer URLs in log.
	# (wikia's URL router converts spaces to underscores). '%20' work fine as well.
	# Replace returns new strings
	artist = lyric_wikia_capitalize(song.artist, False).replace(' ', '_')
	title = lyric_wikia_capitalize(song.title, True).replace(' ', '_')


	
	# Since we are building our own URL and not passing 'params' to request.get;
	# call the 'quote' to fix URL characters like(!@#$%^&*()?) before passing URL. 
	# 'requests' module was passing them as it is.

	# If we were using the 'requests' module's params' argument to build URL
	# as in the lyrics_n_music module, we could have skipped 'quote', 'encode' steps.

	# Though 'requests' module encodes the Unicode(ex kanji) inherently, here the
	# 'quote' function does that as well. Because of that for *Python27*, 
	# the artist and title Unicode objects must be encoded to 'utf-8' manually
	# before they are passed to 'quote' function.

	# Basically we are doing everything manually and not using 'requests' module's
	# automatic URL encoding.

	if sys.version_info[0] < 3:
		artist = artist.encode('utf-8')
		title = title.encode('utf-8')

	lyrics_wikia_url = 'http://lyrics.wikia.com/wiki/%s:%s' % (quote(artist), quote(title))
	try:
		print('\tTrying Lyric Wikia:', lyrics_wikia_url)

		res = requests.get(lyrics_wikia_url, headers = request_headers)
		res.raise_for_status()
		
	# Catch network errors
	except (ConnectionError, Timeout):
		song.error = 'No network connectivity.'
	except HTTPError:
		song.error = 'Lyrics not found. Check artist or title name.'
	
	# No exceptions raised and the HTML for lyrics page was fetched		
	else:
		soup = BeautifulSoup(res.text, 'html.parser')

		# For lyrics.wikia, the lyrics are present in a div with class 'lyricbox'
		lyricbox = soup.find(class_='lyricbox')

		if lyricbox:

			# remove script and div tags from the lyricbox(div)
			junk = lyricbox.find_all(['script', 'div'])
			for html_tag in junk:
				html_tag.decompose()

			# replace '<\br>' tags with newline characters
			br_tags = lyricbox.find_all('br')

			# loop over all <\br> tags and replace with newline characters
			for html_tag in br_tags:
				html_tag.replace_with('\n')

			# lyrics are returned as unicode object
			lyrics = lyricbox.get_text().strip()
	
	# Final check
	if test_lyrics(lyrics):
		song.lyrics = lyrics
		song.source = 'WIKI'
		song.error = None
	else:
		# Don't overwrite and previous errors
		if not song.error:
			song.error = 'Lyrics not found. Check artist or title name.'

def lyric_wikia_capitalize(string, noupper = True):
        """
        lyrics.wikia.com page name rules:
        - Uppercase All Words
        - No all-uppercase WORDS allowed in song titles (but in artist names)
        - Keep StrANgeLy cased words

        See http://lyrics.wikia.com/wiki/LyricWiki:Page_Names
        """
        pattern = re.compile("([\w]+)", re.UNICODE)
        parts = pattern.split(string)

        result = u""
        for part in parts:
                if not pattern.match(part):
                        #no word, keep as it is
                        result += part
                        continue
                if noupper and part.isupper():
                        #everything uppercase? no!
                        part = part.lower()
                result += part[0].upper() + part[1:]

        return result
