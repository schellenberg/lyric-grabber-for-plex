# -*- coding: utf-8 -*-

"""
	Contains general helper functions and Error classes.
"""

from __future__ import print_function
from __future__ import unicode_literals

import sys
import re
import os
from appdirs import *


class BadConfigError(Exception):
	def __init__(self, errno, value):
		self.value = value
		self.errno = errno
	
	def __str__(self):
		return repr(self.value)


def get_config_path():
	
	"""
		Gets the absolute path of dir containing script running the function.
		Uses that to get the path of config file, since it is located in same dir.
		If config file is missing, a new one is created.
	"""
	config_path = user_config_dir("lyrico") + ".ini"
	if not os.path.isfile(config_path):
		write_default_config(config_path)

	return config_path

def sanitize_data(s):
	"""Removes excess white-space from strings"""

	# If string only empty spaces return None
	if not s or s.isspace():
		return None

	# remove any white-space from beginning or end of the string
	s = s.strip()

	# remove double white-spaces or tabs if any
	s = re.sub(r'\s+', ' ', s)

	return s

def write_default_config(config_path):
	# Import ConfigParser
	try:
		# >3.2
		from configparser import ConfigParser
	except ImportError:
		# python27
		# Refer to the older SafeConfigParser as ConfigParser
		from ConfigParser import SafeConfigParser as ConfigParser

	# Load lyrico.ini
	config = ConfigParser()

	# Force all settings to intended defaults
	config.add_section('actions')
	config.set('actions', 'save_to_file', 'True')
	config.set('actions', 'save_to_tag', 'False')
	config.set('actions', 'overwrite', 'False')

	config.add_section('paths')
	config.set('paths', 'source_dir', 'None')
	config.set('paths', 'lyrics_dir', 'None')

	config.add_section('sources')
	config.set('sources', 'lyric_wikia', 'True')
	config.set('sources', 'lyrics_n_music', 'True')
	config.set('sources', 'musix_match', 'True')
	config.set('sources', 'lyricsmode', 'True')
	config.set('sources', 'az_lyrics', 'False')

	# save to config.ini
	with open(config_path, 'w') as configfile:
		config.write(configfile)
