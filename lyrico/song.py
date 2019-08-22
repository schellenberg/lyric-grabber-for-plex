
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals


import time
import sys
import os

from mutagen.id3 import USLT
from mutagen.asf import ASFUnicodeAttribute
from mutagen import MutagenError
from bs4 import BeautifulSoup

# Import all the sources modules
from .lyrico_sources.lyric_wikia import download_from_lyric_wikia
from .lyrico_sources.az_lyrics import download_from_az_lyrics
from .lyrico_sources.musix_match import download_from_musix_match
from .lyrico_sources.lyricsmode import download_from_lyricsmode

from .song_helper import get_song_data, get_song_list
from .config import Config
from .audio_format_keys import FORMAT_KEYS

# If we are using python27, import codec module and replace native 'open'
# with 'codec.open' to write unicode strings to file.

if sys.version_info[0] < 3:
    import codecs
    open = codecs.open


class Song():
	"""Container objects repersenting each song globbed from source_dir"""

	# holds count for songs for valid metadata
	valid_metadata_count = 0

	# Count for songs whose lyrics are successfully saved to file.
	lyrics_saved_to_file_count = 0

	# Count for songs whose lyrics are successfully saved to tag.
	lyrics_saved_to_tag_count = 0

	# Number of errors during download or tagging
	lyrics_errors_count = 0

	# Number of songs that already had lyrics
	lyrics_existing_count = 0

	def __init__(self, path):

		self.path = path

		# extract data from song
		data = get_song_data(path)

		# Initialize instance variables from data extracted
		self.tag = data['tag']
		self.artist = data['artist']
		self.title = data['title']
		self.album = data['album']
		self.format = data['format']

		self.lyrics_file_name = data['lyrics_file_name']
		self.lyrics_file_path = data['lyrics_file_path']

		# If the required lyrics file is already present in LYRICS_DIR
		self.lyrics_file_present = data['lyrics_file_present']

		# If the required lyrics is already embedded in tag
		self.lyrics_tag_present = data['lyrics_tag_present']


		# Holds the downloaded lyrics
		self.lyrics = None

		# Final status to build log
		self.saved_to_tag = False
		self.saved_to_file = False
		self.source = None
		self.error = data['error']

		# As the songs are read from the files, update the class variable.
		# This is count of songs that have valid artist and title.
		if self.title and self.artist:
			Song.valid_metadata_count += 1

	def download_lyrics(self):

		"""
			Only called when song has artist and title.
			Calls self.save_lyrics to save them.

		"""

		if not self.download_required():
			Song.lyrics_existing_count += 1
			print('\nSkipping', self.artist, '-', self.title)
			print('Lyrics already present.')
			return

		# At this point there is nothing in self.error
		print('\nDownloading:', self.artist, '-', self.title)

		# Use sources according to user settings
		if Config.lyric_wikia:
			download_from_lyric_wikia(self)

		# Only try other sources if required

		if not self.lyrics and Config.musix_match:
			download_from_musix_match(self)

		if not self.lyrics and Config.lyricsmode:
			download_from_lyricsmode(self)

		if not self.lyrics and Config.az_lyrics:
			download_from_az_lyrics(self)

		self.save_lyrics()

	def save_lyrics(self):

		"""
			Called by self.download_lyrics to save lyrics according to
			Config.save_to_file, Config.save_to_tag settings.

			Handles the case if lyrics is not found. Logs errors to console
			and Song object.

		"""
		
		if not self.lyrics:
			Song.lyrics_errors_count += 1
			print('Failed:', self.error)
			return

		if self.lyrics and Config.save_to_file:
			try:
				with open(self.lyrics_file_path, 'w', encoding='utf-8') as f:
					f.write('Artist - ' + self.artist + '\n')
					f.write('Title - ' + self.title + '\n')

					album_str = 'Album - Unkown'
					if self.album:
						album_str = 'Album - ' + self.album			
					f.write(album_str)
					f.write('\n\n')

					f.write(self.lyrics)

				# update class variable
				Song.lyrics_saved_to_file_count += 1

				# update the Song instance flag
				self.saved_to_file = True

				self.download_status = "ok"
				print('Success: Lyrics saved to file.')

			except IOError as e:
				err_str = str(e)
				if e.errno == 22:
					err_str = 'Cannot save lyrics to file. Unable to create file with song metadata.'
				if e.errno == 13:
					err_str = 'Cannot save lyrics to file. The file is opened or in use.'
				if e.errno == 2:
					err_str = '"lyrics_dir" does not exist. Please set a "lyrics_dir" which exists.'

				self.error = err_str
				Song.lyrics_errors_count += 1
				print('Failed:', err_str)

		if self.lyrics and Config.save_to_tag:
			lyrics_key = FORMAT_KEYS[self.format]['lyrics']
			try:
				if self.format == 'mp3':
					# encoding = 3 for UTF-8
					self.tag.add(USLT(encoding=3, lang = u'eng', desc = u'lyrics.wikia',
									text=self.lyrics))

				if self.format == 'm4a' or self.format == 'mp4':
					# lyrics_key = '\xa9lyr'
					
					if sys.version_info[0] < 3:
						lyrics_key = lyrics_key.encode('latin-1')
					self.tag[lyrics_key] = self.lyrics

				# Both flac and ogg/oga(Vorbis & FLAC), are being read/write as Vorbis Comments.
				# Vorbis Comments don't have a standard 'lyrics' tag. The 'LYRICS' tag is 
				# most common non-standard tag used for lyrics.
				if self.format == 'flac' or self.format == 'ogg' or self.format == 'oga':
					self.tag[lyrics_key] = self.lyrics

				if self.format == 'wma':
					# ASF Format uses ASFUnicodeAttribute objects instead of Python's Unicode
					self.tag[lyrics_key] = ASFUnicodeAttribute(self.lyrics)

				self.tag.save()
				self.saved_to_tag = True
				Song.lyrics_saved_to_tag_count += 1

				print('Success: Lyrics saved to tag.')

			except MutagenError:
				err_str = 'Cannot save lyrics to tag. Codec/Format not supported'
				self.error = err_str
				Song.lyrics_errors_count += 1
				print('Failed:', err_str)
				
			except IOError as e:
				err_str = 'Cannot save lyrics to tag. The file is opened or in use.'
				self.error = err_str
				Song.lyrics_errors_count += 1
				print('Failed:', err_str)

	def download_required(self):
		"""
		Checks if a lyrics are required to be download.
		Uses Config.save_to_file, Config.save_to_tag and Config.overwrite settings
		and returns True when download is required.

		"""
		if Config.overwrite:
			# If user wants to overwite existing lyrics, always download
			# and save according to Config.save_to_file, Config.save_to_tag settings
			return True
		else:

			# Do we need to download lyrics and save to file
			file_required = False

			# Do we need to download lyrics and save to tag
			tag_required = False

			if Config.save_to_file and not self.lyrics_file_present:
				# if user wants to save to file and the file is not
				# present in the set LYRICS_DIR, the we need
				# to download it and save to the file.
				file_required = True

			if Config.save_to_tag and not self.lyrics_tag_present:
				# if user wants to save to tag and the tag does not
				# has lyrics field saved, then we need
				# to download it and save to the tag.
				tag_required = True

			# If either is required, we need to make the download request.
			# Data is then saved accordingly to the settings.
			return file_required or tag_required

	def get_log_string(self):
		"""
		returns the log string of the song which is used in final log.

		"""
		template = '. \t{file}\t{tag}\t{source}\t\t{song}\t\t{error}\n'
		log = {}

		# file_status and tag each have 4 possible values
			# 'Saved' - File or tag was saved successfully
			# 'Failed' - Download or save failed. Show error.
			# 'Ignored' - Ignored according to Config.save_to_file, Config.save_to_tag setting by user.
			# 'Present' - Detected tag or file and skipped download skipped by lyrico as per Config.overwrite setting.

		if Config.save_to_file:
			if not self.download_required():
				file_status = 'Present'
			else:
				if self.saved_to_file:
					file_status = 'Saved'
				else:
					file_status = 'Failed'
		else:
			file_status = 'Ignored'

		if Config.save_to_tag:
			if not self.download_required():
				tag = 'Present'
			else:
				if self.saved_to_tag:
					tag = 'Saved'
				else:
					tag = 'Failed'
		else:
			tag = 'Ignored'
		
		# avoid exceptions raised for concatinating Unicode and None types
		if self.artist and self.title:
			log['song'] = self.artist + ' - ' + self.title
		else:
			log['song'] = self.path

		log['error'] = self.error

		log['file'] = file_status
		log['tag'] = tag
		log['source'] = self.source

		return template.format(**log)

	@staticmethod
	def log_results(song_list):

		try:
			log_date = time.strftime("%H:%M:%S  %d/%m/%y")
			log_file_name = 'log.txt'
			with open(os.path.join(Config.lyrics_dir, log_file_name), 'w', encoding='utf-8') as f:
				
				f.write('\t\t\t\tlyrico\n\n')

				f.write('Log Date ' + log_date + '\n')
				f.write('\n')

				f.write('Audio files detected: ' + str(len(song_list)))
				f.write('\n')

				f.write('Metadata extracted for: ' + str(Song.valid_metadata_count))
				f.write('\n')

				f.write('Lyrics files saved: ' + str(Song.lyrics_saved_to_file_count))
				f.write('\n')

				f.write('Tags saved: ' + str(Song.lyrics_saved_to_tag_count))
				f.write('\n\n')

				table_header = '  \t[FILE]\t[TAG]\t[SOURCE]\t\t\t[ARTIST-TITLE]\t\t\t\t[ERROR]\n'
				table_border = '='*100 + '\n'

				f.write(table_header)
				f.write(table_border)

				# write individual song log strings
				index_number = 1
				for song in song_list:
					f.write(str(index_number))
					f.write(song.get_log_string())
					index_number += 1

				# Add STATUS KEY to log
				f.write('\n\n\t**** STATUS KEY ****\n')

				f.write("\t# 'Saved' - File or tag was saved successfully.")
				f.write("\n")

				f.write("\t# 'Failed' - Download or save failed. See error.")
				f.write("\n")

				f.write("\t# 'Ignored' - Ignored according to 'save_to_file', 'save_to_tag' setting.")
				f.write("\n")

				f.write("\t# 'Present' - Detected tag or file and skipped download as per 'overwrite' setting.")
				f.write("\n")

				# Add source key to log
				f.write('\n\n\t**** SOURCE KEY  ****\n')

				f.write("\t# 'WIKI' - Lyric Wikia")
				f.write("\n")

				f.write("\t# 'mXm' - musiXmatch")
				f.write("\n")

				f.write("\t# 'LrMOD' - LYRICSMODE")
				f.write("\n")

				f.write("\t# 'AZLr' - AZLyrics")
				f.write("\n\n")

				# Add credits
				f.write(table_border)
				
				f.write("'lyrico' has been built and is maintained by Abhimanyu Pathania.")
				f.write("\n\n")

				f.write('If you encounter a bug, please raise an issue on GitHub.')
				f.write("\n")

				f.write('\thttps://github.com/abhimanyuPathania/lyrico/issues')
				f.write("\n")

				f.write('Or you can mail me: abpindia1944@gmail.com')
				f.write("\n\n")

				f.write('Cheers!')
				f.write('\n\n\n\n')

		except IOError as e:
			print('Unable to build log.')
			print('"lyrics_dir" does not exist. Please set "lyrics_dir" to a folder which exists.')


