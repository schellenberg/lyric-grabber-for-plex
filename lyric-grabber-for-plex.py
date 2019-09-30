'''
Lyric Grabber for Plex
Made by Dan Schellenberg
'''

from __future__ import print_function
from __future__ import unicode_literals

from gooey import Gooey, GooeyParser

import sys
import time

import platform
import glob2
import os

from lyrico.docopt import docopt

from lyrico.song import Song
from lyrico.song_helper import get_song_list
from lyrico.config import Config

@Gooey(default_size=(610, 565))
def main():
    parser = GooeyParser(
        description='Lyric Grabber for Plex',
    )

    directory_group = parser.add_argument_group(
    "", 
    ""
    )

    directory_group.add_argument(
        'music_directory',
        metavar='Music Directory',
        help='Select the music directory you want to search',
        widget='DirChooser')

    timeout_group = parser.add_argument_group(
    "Timeout Values", 
    "These values will allow a pause after a certain number of song lyric requests are sent. This can help avoid hitting the lyric servers with too many requests in a row (which could theoretically lead to your IP being banned)."
    )

    timeout_group.add_argument(
        'number_of_requests_before_pause',
        metavar='Number of Consecutive Requests',
        help='How many requests to send before a pause?\n(set to 0 for no pause)',
        default=100,
        type=int)

    timeout_group.add_argument(
        'pause_length',
        metavar='Wait Time',
        help='How many seconds to wait after the consecutive requests?',
        default=30,
        type=int)

    create_log = False  #replace with an argument to Gooey?

    args = parser.parse_args()

    requests_sent = 0
    if args.music_directory:
        try:
            Config.set_dir('source_dir', args.music_directory)
        except Exception as e:
            raise Exception(e)

        # set default PLEX-MODE values for lyrico
        Config.set_dir('lyrics_dir', "PLEX-MODE")
        Config.save_to_file = True
        Config.save_to_tag = False
        Config.overwrite = False

        Config.lyric_wikia = True
        Config.musix_match = True
        Config.lyricsmode = True
        Config.az_lyrics = True

        Config.lyric_files_in_dir = glob2.glob(os.path.join(Config.lyrics_dir, '**/*.txt'))

        song_list = [Song(song_path) for song_path in get_song_list(Config.source_dir)]
        print(len(song_list), 'songs detected.')
        print('Metadata extracted for', (str(Song.valid_metadata_count) + '/' + str(len(song_list))), 'songs.')
        print(" ", flush = True)
        for song in song_list:
            # Only download lyrics if 'title' and 'artist' is present
            # Error str is already present in song.error
            if song.artist and song.title:
                song.download_lyrics()

            # Show immediate log in console
            else:
                # If title was present, use that
                if song.title:
                    print(song.title, 'was ignored.', song.error)
                # else use audio file path
                else:
                    print(song.path, 'was ignored.', song.error)
            
            print(" ", flush = True) #avoid output buffering


            if args.number_of_requests_before_pause and args.pause_length:
                if args.pause_length != 0:
                    try:
                        requests_sent += 1
                        if requests_sent >= args.number_of_requests_before_pause:
                            requests_sent = 0
                            time.sleep(args.pause_length)
                    except:
                        raise Exception("No music directory chosen.")
                
        if create_log:
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

        print('FINISHED', flush = True)

    else:
        raise Exception("No music directory chosen.")


if __name__ == '__main__':
    main()
