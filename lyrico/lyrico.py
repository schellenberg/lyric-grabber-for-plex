# -*- coding: utf-8 -*-

"""lyrico

Usage:
  lyrico [<source_dir>]
  lyrico (enable | disable) (<lyrico_action>)
  lyrico set (<dir_type>) (<full_path_to_dir>)
  lyrico (-h | --help)
  lyrico --version
  lyrico --settings

Options:
  -h --help     Show this screen.
  --version     Show version.
  --settings    Show current settings.
"""

from __future__ import print_function
from __future__ import unicode_literals

import platform

from .docopt import docopt

from .song import Song
from .song_helper import get_song_list
from .config import Config

# testpypi 0.6.0
__version__ = "0.6.0"


def main():

	# Fix console for windows users
	if platform.system() == 'Windows':
		import win_unicode_console
		win_unicode_console.enable()

	args = docopt(__doc__, version = ('lyrico ' + __version__))

	Config.load_config()
	
	if args['--settings']:
		# show current settings
		Config.show_settings()
		return

	if args['set']:
		# setting 'lyrics_dir' or 'source_dir'

		# This general try catch block is intended for os.makedirs call if
		# it raises OSError which is not due to directory already existing or
		# some other error than OSError
		try:
			Config.set_dir(args['<dir_type>'], args['<full_path_to_dir>'])
			Config.save()
		except Exception as e:
			print(e)
		return

	if args['enable'] or args['disable']:
		# setting 'save_to_file', 'save_to_tag' or 'overwrite'.
		# detect wether user wants to enable or disable a lyrico action
		update_type = 'enable' if args['enable'] else 'disable'
		Config.update_lyrico_actions(args['<lyrico_action>'], update_type)
		Config.save()
		return

	# User wants to download lyrics.

	if args['<source_dir>']:
		# if lyrico <source_dir> invocation is used:
		# update user's "source_dir" in config
		# update Config class' 'source_dir' class variable

		# This general try catch block is intended for os.makedirs call if
		# it raises OSError which is not due to directory already existing or
		# some other error than OSError
		try:
			set_dir_success = Config.set_dir('source_dir', args['<source_dir>'])
		except Exception as e:
			print(e)
			# Don't go ahead with excution since user gave bad path or might have
			# correct system settings?
			return

		# For this usage if user provides non existing dir, return by using boolean
		# return value of Config.set_dir
		if not set_dir_success:
			return

	#settings changes are done, we need a valid config now
	if not Config.check():
		return
				
	song_list = [Song(song_path) for song_path in get_song_list(Config.source_dir)]
	print(len(song_list), 'songs detected.')
	print('Metadata extracted for', (str(Song.valid_metadata_count) + '/' + str(len(song_list))), 'songs.')
	for song in song_list:
		# Only download lyrics if 'title' and 'artist' is present
		# Error str is already present in song.error
		if song.artist and song.title:
			song.download_lyrics()

		# Show immidiate log in console
		else:
			# If title was present, use that
			if song.title:
				print(song.title, 'was ignored.', song.error)
			# else use audio file path
			else:
				print(song.path, 'was ignored.', song.error)


	print('\nBuilding log...')
	Song.log_results(song_list)
	print(
		'{songs} songs, {tagged} tagged, {files} lyric files, {existing} existing, {errors} errors'.format(
			songs = len(song_list),
			tagged = Song.lyrics_saved_to_tag_count,
			files = Song.lyrics_saved_to_file_count,
			existing = Song.lyrics_existing_count,
			errors = Song.lyrics_errors_count
		)
	)
	print('FINISHED')
		
	# Disable windows unicode console anyways
	if platform.system() == 'Windows':
		win_unicode_console.disable()
