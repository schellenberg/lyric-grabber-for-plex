
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import unicodedata


def remove_accents(input_str):
	
	"""
		Convert accented into non-accented characters
		http://stackoverflow.com/a/517974/2426469
	"""

	nfkd_form = unicodedata.normalize('NFKD', input_str)
	return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def test_lyrics(lyrics):
	
	"""
		Test lyrics downloaded to detect license restrinction string:
		'We are not in a position to display these lyrics due to licensing restrictions.
		Sorry for the inconvinience.'

		Also test lyrics by looking for multiple new line characters.

		Returns booleans accordingly
	"""

	if not lyrics:
		return False
	
	license_str1 = 'We are not in a position to display these lyrics due to licensing restrictions. Sorry for the inconvinience.'
	license_str2 = 'display these lyrics due to licensing restrictions'
	license_str3 = 'We are not in a position to display these lyrics due to licensing restrictions.\nSorry for the inconvinience.'

	# If either of license string is found in lyrics downloaded or it has less than 4 new line characters
	if (license_str1 in lyrics or license_str2 in lyrics or license_str3 in lyrics or
		lyrics.count('\n') < 4):
		return False
		
	return True
