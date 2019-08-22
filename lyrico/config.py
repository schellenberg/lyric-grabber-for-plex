# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import unicode_literals

import os
import glob2


try:
	# Import the base class for all configparser errors as BaseConfigParserError
	# >3.2
	from configparser import ConfigParser
	from configparser import Error as BaseConfigParserError
except ImportError:
	# python27
	# Refer to the older SafeConfigParser as ConfigParser
	from ConfigParser import SafeConfigParser as ConfigParser
	from ConfigParser import Error as BaseConfigParserError

from .helper import get_config_path
from .helper import BadConfigError

# Maintian a dict of lyrico actions to check target on update_lyrico_actions()
# Also save the corresponding section in 

LYRICO_ACTIONS = {
	'save_to_file': 'actions',
	'save_to_tag': 'actions',
	'overwrite': 'actions',

	'lyric_wikia': 'sources',
	'musix_match': 'sources',
	'lyricsmode' : 'sources',
	'az_lyrics': 'sources',
}

# Used to print commandline logging for enable/disable sources 
SOURCE_STR_MAP = {
	'lyric_wikia' : 'Lyric Wikia',
	'musix_match': 'musiXmatch',
	'lyricsmode': 'LYRICSMODE',
	'az_lyrics': 'AZLyrics',
}

class Config():
	
	"""
		Class wrapper build around user settings loaded from
		config.ini

		All setting are stored are class variables and all methods are
		static methods. 

		A Config object is never instantiated, only the class is imported
		into other modules to access class variables and methods. 

	"""

	# Audio formats supported are not loaded from config.ini

	# This list is used by the 'glob2' module to scan 'source_dir' for audio files.
	audio_formats = ['mp3', 'flac', 'm4a', 'mp4', 'ogg', 'oga', 'wma']

	lyrics_dir = None
	source_dir = None

	save_to_file = True
	save_to_tag = False

	overwrite = False
	lyric_files_in_dir = None

	@staticmethod
	def check():
		"""
		Check if the configuration is valid
		"""
		# This forces user to set dirs before running the app for first time.
		if len(Config.lyrics_dir) == 0:
			# see which directory in not set and raise BadConfigError with that as value
			print('lyrics_dir is not set.')
			print('Please use the "set" command to set lyrics_dir.')
			print('use "lyrico --help" to view commands.')
			return False

		if len(Config.source_dir) == 0:
			# see which directory in not set and raise BadConfigError with that as value
			print('source_dir is not set.')
			print('Please use the "set" command to set source_dir or pass it as parameter.')
			print('use "lyrico --help" to view commands.')
			return False

		# if user disable both saving mode. Notify & force user to correct on next run.
		if not Config.save_to_file and not Config.save_to_tag:
			print('Both "save_to_file" and "save_to_tag" modes are disabled. Please enable one.')
			print('use "lyrico --help" to view commands.')
			return False

		# if user disables all sources. Notify & force user to enable one.
		if (not Config.lyric_wikia
		    and not Config.az_lyrics
		    and not Config.musix_match
		    and not Config.lyricsmode):
			print('All lyrics sources are disabled. Please enable one.')
			print('use "lyrico --help" to view commands.')
			return False
		return True

	@staticmethod
	def load_config():
		"""
		Called only once by main to read user settings from config.ini
		and save them to the class variables.
		"""
		try:
			conf = ConfigParser()

			config_path = get_config_path()
			conf.read(config_path)

			# save references to conf, and config_path in class variables
			Config.config_path = config_path
			Config.conf = conf

			Config.source_dir = conf.get('paths', 'source_dir')
			Config.lyrics_dir = conf.get('paths', 'lyrics_dir')

			Config.save_to_file = conf.getboolean('actions', 'save_to_file')
			Config.save_to_tag = conf.getboolean('actions', 'save_to_tag')

			Config.overwrite = conf.getboolean('actions', 'overwrite')

			# Load all the sources
			Config.lyric_wikia = conf.getboolean('sources', 'lyric_wikia')
			Config.musix_match = conf.getboolean('sources', 'musix_match')
			Config.lyricsmode = conf.getboolean('sources', 'lyricsmode')
			Config.az_lyrics = conf.getboolean('sources', 'az_lyrics')

			# Loading this with user config, we need to call the load_config only once at start.
			Config.lyric_files_in_dir = glob2.glob(os.path.join(Config.lyrics_dir, '**/*.txt'))


		# Catch file handling errors
		except IOError as e:
			print('Unable to load config.')
			print(e)

	@staticmethod
	def save():
		"""
		Save configuration file contents
		"""
		try:
			#paths
			Config.conf.set('paths', 'source_dir', Config.source_dir)
			Config.conf.set('paths', 'lyrics_dir', Config.lyrics_dir)

			#actions
			Config.setBool('actions', 'save_to_file', Config.save_to_file)
			Config.setBool('actions', 'save_to_tag', Config.save_to_tag)

			#sources
			Config.setBool('sources', 'lyric_wikia', Config.lyric_wikia)
			Config.setBool('sources', 'musix_match', Config.musix_match)
			Config.setBool('sources', 'lyricsmode', Config.lyricsmode)
			Config.setBool('sources', 'az_lyrics', Config.az_lyrics)

			with open(Config.config_path, 'w') as configfile:
				Config.conf.write(configfile)
			return True

		# Catch all config parser errors
		except BaseConfigParserError as e:
			print('Unable to save settings to config.')
			print(e)
			return False

		# Catch file handling errors
		except IOError as e:
			print('Unable to save settings to config.')
			print(e)
			return False

	@staticmethod
	def setBool(section, option, value):
		svalue = 'True' if value == True else 'False'
		Config.conf.set(section, option, svalue)


	@staticmethod
	def set_dir(dir_type, path):

		"""
			Takes an absolute path as saves it as 'source_dir' or 'lyrics_dir'
			in config.ini.
			path is user input from the cmdline.
		"""

		if dir_type != 'source_dir' and dir_type != 'lyrics_dir':
			print('Invalid "dir_type". Only "source_dir" or "lyrics_dir" are valid types.')
			print('You gave "dir_type":', dir_type)
			print('use "lyrico --help" to view commands.')
			return False

		# If user is setting "source_dir", return if the path provided does not exist.
		# This improves the usage - lyrico <source_dir>
		if dir_type == 'source_dir':
			if not os.path.isdir(path):
				print('"source_dir" does not exist. ', end="")
				print('You gave "source_dir":', path)
				print('Please enter path to an existing folder.')
				return False
			Config.source_dir = path
		# make directory if user is setting "lyrics_dir" and it does not exists.
		# Refer http://stackoverflow.com/a/14364249/2426469
		elif dir_type == 'lyrics_dir':
			try:
				os.makedirs(path)
				print('Directory does not exist. Creating new one.')
			except OSError:
				if not os.path.isdir(path):
					# this exception is handled by function calling set_dir
					raise
			Config.lyrics_dir = path

		print(dir_type, 'updated.')
		if dir_type == 'source_dir':
			print('lyrico will scan the following folder for audio files:')
		else:
			print('lyrico will save lyrics files in the following folder:')
		print('    ', path)
		return True

	@staticmethod
	def update_lyrico_actions(target, update_type):

		if target not in LYRICO_ACTIONS:
			print('Invalid lyrico action change attempted')
			print('''"save_to_file", "save_to_tag" and "overwrite" are the only settings that can be enabled or disabled.''')
			print('''"lyric_wikia", "musix_match", "lyricsmode" and "az_lyrics" are the only sources that can be enabled or disabled.''')
			print('You attempted to change:', target)
			print('use "lyrico --help" to view commands.')
			return 

		# User is updating valid action/source
		bval = True if update_type == 'enable' else False
		log_str = '' if update_type == 'enable' else 'not '
		
		setattr(Config, target, bval)
		print(target, (update_type + 'd'))

		if target == 'save_to_file':
			print('lyrico will %ssave the downloaded lyrics to text files.' % log_str)

		elif target == 'save_to_tag':
			print('lyrico will %sembed the downloaded lyrics into song tags.' % log_str)

		elif target == 'overwrite':
			if update_type == 'disable':
				print('lyrico will detect the songs that already have lyrics, and will ignore them.')
			else:
				print('''lyrico will download lyrics for all songs detected in "source_dir" and overwrite lyrics if already present.''')
		else:
			# Action is to enable/disable a source.
			print('lyrico will %suse %s as a source for lyrics.' % (log_str, SOURCE_STR_MAP[target]))

	@staticmethod
	def show_settings():
		
		print('Your current settings:\n')
		# get list of section in config
		for section in Config.conf.sections():
			# for each section get list items.
			# items are returned as list of tuples of type (key, value)
			print(section.upper())
			for item in Config.conf.items(section):
				print('   ', item[0], '=', item[1])
			print('\n')
