
"""
	This module only holds the keys used to extract data from
	mutagen's tag objects for the supported audio formats.
"""

from __future__ import print_function
from __future__ import unicode_literals


VORBIS_COMMENTS_KEYS = {
	'artist': 'artist',
	'title': 'title',
	'album':'album',
	'lyrics':'LYRICS'
}

MP4_KEYS = {
	'artist': '\xa9ART',
	'title': '\xa9nam',
	'album':'\xa9alb',
	'lyrics':'\xa9lyr'
}



FORMAT_KEYS = {
	
	#ID3 TAGS
	'mp3': {
		'artist': 'TPE1',
		'title': 'TIT2',
		'album':'TALB',
		'lyrics':'USLT'
	},

	'mp4' : MP4_KEYS,
	'm4a' : MP4_KEYS,

	'flac': VORBIS_COMMENTS_KEYS,
	'ogg' : VORBIS_COMMENTS_KEYS,
	'oga' : VORBIS_COMMENTS_KEYS,

	'wma' : {
		'artist': 'Author',
		'title': 'Title',
		'album':'WM/AlbumTitle',
		'lyrics':'WM/Lyrics'
	}
}


