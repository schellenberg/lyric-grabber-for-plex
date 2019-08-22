# -*- coding: utf-8 -*-


"""
	This module downloads lyrics from AZLyrics by scraping them off its HTML pages.
	The url structure used is:

		http://www.azlyrics.com/lyrics/<artist>/<title>.html

	AZLyrics only allows lowercase alphanumeric(no '_') URLs.

	This source is least accurate since BeautifulSoup is not able to parse the HTML pages
	correctly and the module depends on regular expressions.

	AZLyrics also hates 'The' in artists name for some reason and removes it. Yet there are some
	exceptions to this rule. 'lyrico' uses the AZLyrics_CORRECTION mapping for this.

"""


from __future__ import print_function
from __future__ import unicode_literals

import re
import sys
import requests

from requests import ConnectionError, HTTPError, Timeout
from bs4 import BeautifulSoup

from .build_requests import get_lyrico_headers
from .lyrics_helper import test_lyrics


# Defining 'request_headers' outside download function makes a single profile
# per lyrico operation and not a new profile per each download in an operation.
request_headers = get_lyrico_headers()

# Holds corerction for Artist names
# key(artist name built from our song metadata): value(corresponding value used by AZLyrics)
AZLyrics_CORRECTION = {
	'the': 'thethe'
}

def download_from_az_lyrics(song):
	
	"""
		Takes reference to the song object as input and
		adds lyrics to self.lyrics or add error string to self.error
		property of the song object. 
	"""


	# temp var to hold value for final checking
	lyrics = None

	# Assume this won't work. Be a realist. 
	error = 'Lyrics not found. Check artist or title name.'

	artist = song.artist
	title = song.title

	# This looks for 'The' followed by a 'space' which is followed by any non-space(\s) char.
	# Caret(^) forces to find it only from beginning
	# If true then remove the 'The' from the artist name.
	regex_the = re.compile(r'^The[ ]{1}\S', re.IGNORECASE)
	match_the = re.search(regex_the, artist)
	if match_the:
		# Remove 'The '
	    artist = artist[4:]
	

	# Convert artist and title to lower case and strip off any
	# non-alphanumeric characters and '_'. '\W' Equivalent to set [^a-zA-Z0-9_] 
	# Make regex Unicode UNAWARE
	if sys.version_info[0] < 3:
		# Python27
		# By default ignores Unicode.
	    regex_url = re.compile('[\W_]+')
	else:
		# Use re.ASCII flag to extract ASCII characters only
	    regex_url = re.compile('[\W_]+', re.ASCII)

	artist = regex_url.sub('', artist.lower())
	title = regex_url.sub('', title.lower())

	# Check if correction for artist is present in lyrico
	if artist in AZLyrics_CORRECTION:
		artist = AZLyrics_CORRECTION[artist]

	azlyrics_url = 'http://www.azlyrics.com/lyrics/%s/%s.html' % (artist, title)
	try:
		print('\tTrying AZLyrics:', azlyrics_url)

		res = requests.get(azlyrics_url, headers = request_headers)
		res.raise_for_status()
		# 'requests' was guessing the encoding from azlyrics as ISO-8859-1.
		# AZLyrics sends 'UTF-8' in its meta tag

		# Force request to use 'UTF-8'. This is used when 'res.text' is read to get 'soup'
		res.encoding = 'utf-8'

	# Catch network errors
	except (ConnectionError, Timeout) as e:
		print(e)
		error = 'No network connectivity.'
	except HTTPError:
		# Already carrying error string
		pass
	
	# No exceptions raised and the HTML for lyrics was downloaded		
	else:
		soup = BeautifulSoup(res.text, 'html.parser')
		lyric_tag = soup.find('div', class_=None, id=None)
		lyrics = lyric_tag.get_text().strip()
			    
	# Final check
	if test_lyrics(lyrics):
		song.lyrics = lyrics
		song.error = None
		song.source = 'AZLr'
	else:
		song.error = error


def check_siblings(sib, title, regex):

	"""
		This function checks the conditions under which buggy parsing seems
		to work for AZLyrics' HTML. Function only returns true if parsing
		conditions are same as when tested during development.

		'sib' is list of 'lyricsh' div's siblings.
		'title' and 'regex' are the one used to build AZLyrics' URL.

	"""

	# The siblings list of 'lyricsh' should contain following structure:
		# i : 'name' 'class'

		# 0 : div ['ringtone']
		# 1 : b None
		# 2 : br None
		# 3 : div ['col-lg-2', 'text-center', 'hidden-md', 'hidden-sm', 'hidden-xs', 'noprint']

		# The third member should be the buggy 'br' tag which contains the lyrics

	if not sib:
		return False

	# Check if silbling has atleast 4 members which exist.
	if not (len(sib) >= 4 and sib[1] and sib[2] and sib[3] and
		sib[2].name == 'br'):
		return False

	# Extract the class list of sib[3] or the <div> to which BeautifulSoup jumps
	# due to buggy <br> tag
	jump_div_class_list = sib[3].attrs.get('class')
	if not jump_div_class_list:
		return False

	# Check for required keywords in the class list
	jump_div_class = ' '.join(jump_div_class_list)
	if not('noprint' in jump_div_class and 'hidden' in jump_div_class and
		'col-lg-2' in jump_div_class):
		return False

	# sib[1] is a <b> tag which contains the title of the song.
	# Test it with the one used to build URL using the same regex
	title_extracted = sib[1].get_text()
	if title_extracted:
		title_extracted = regex.sub('', title_extracted.lower())

	if title_extracted != title:
		return False

	# If all conditions are met return true to extract lyrics out of <br tag>
	return True
