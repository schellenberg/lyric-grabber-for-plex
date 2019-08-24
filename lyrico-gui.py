from __future__ import print_function
from __future__ import unicode_literals

import sys
import PySimpleGUIQt as sg

import platform

from lyrico.docopt import docopt

from lyrico.song import Song
from lyrico.song_helper import get_song_list
from lyrico.config import Config

__version__ = "0.6.0"

#print to debug window
# print = sg.EasyPrint
# sg.EasyPrint(do_not_reroute_stdout=False)

# music_directory = sg.PopupGetFolder('Select Plex Music Folder to Search', title="Select Folder")
music_directory = "/Volumes/music/Adele"

if music_directory:
	Config.load_config()
	try:
		Config.set_dir('source_dir', music_directory)
		Config.save()
	except Exception as e:
		print(e)
	if not Config.check():
		sg.Popup('Config Error', 'Something is not right. Please check the source directory chosen.')


	# 
	# 
	
	layout = [[(sg.Text('This is where standard out is being routed', size=[40, 1]))],
			[sg.Output(size=(80, 20))]]

	window = sg.Window('Search Results', layout, default_element_size=(30, 2))

	# while True:
	# 		event, value = window.Read()
	# 		if event == 'SEND':
	# 			print(value)
	# 		else:
	# 			break


	# 
	# 

	song_list = [Song(song_path) for song_path in get_song_list(Config.source_dir)]
	print(len(song_list), 'songs detected.')
	print('Metadata extracted for', (str(Song.valid_metadata_count) + '/' + str(len(song_list))), 'songs.')
	window.Refresh()
	for song in song_list:
		# window.Refresh()
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

	# sg.Popup('All Done!', 'See the debug screen for more details.')
else:
	sg.PopupError("No music directory selected. Quitting without searching.", title="No Directory")

