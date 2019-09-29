Lyric Grabber for Plex
=======================

Lyric Grabber for Plex allows you to select a folder of music, then click Start. Lyric Grabber will scan the folder (and any inner folder) for audio files, read their metadata, and download the lyrics for any song it can. The lyrics are saved into the same folder as the music file was in, named the same thing as the audio file, but with a .txt file extension. This is the format [Plex](https://www.plex.tv/) expects to find lyrics.


Installation
=============

Download the Mac or Windows file [from the most recent release here](https://github.com/schellenberg/lyric-grabber-for-plex/releases)


Configuring Plex
=================

Enable "Local Media Assets" in Settings. [Read this support article for full details.](https://support.plex.tv/articles/215916117-adding-local-lyrics/)


About
======

Lyric Grabber for Plex is a simple GUI wrapper (built with [Gooey](https://github.com/chriskiehl/Gooey)) over a slightly customized version of the Python command line program [lyrico](https://github.com/abhimanyuPathania/lyrico).


Audio Formats and Tags
=======================
Below is the table of supported audio formats and their supported tags:

+--------------------------------------------+----------------------------------------------+
| Audio Format                               | Tag                                          |
+============================================+==============================================+
| mp3                                        | ID3 Tags                                     |
+--------------------------------------------+----------------------------------------------+
| flac                                       | Vorbis Comments                              |
+--------------------------------------------+----------------------------------------------+
| m4a, mp4                                   | MP4 Tags (iTunes metadata)                   |
+--------------------------------------------+----------------------------------------------+
| wma                                        | ASF                                          |
+--------------------------------------------+----------------------------------------------+
| ogg, oga                                   | Vorbis Comments                              |
+--------------------------------------------+----------------------------------------------+


``lyrico`` gotchas
====================

Here are few points you should know before using ``lyrico``:

- **Your tags** - ``lyrico`` uses metadata in your tags for building URLs. Hence your songs should be tagged with correct 'artist', 'title' information.

  ``lyrico`` also assumes that you're using standard tags for each format (container) of your songs. For example, ``lyrico`` assumes that your ``.mp3`` files are using the standard ``ID3`` tags and only reads metadata for those. If you are using something like an ``APEv2`` tag with an ``.mp3`` file,  ``lyrico`` won't be able to read it and would log the pertinent error in the ``log.txt``.

  You don't need to be concerned about this unless you have forcibly embedded non-standard tags in your songs with some other software. *Table of supported tags for audio formats is given above.*

- **ID3 tag versions** - ``lyrico`` will convert any old ID3 tag to ID3v2.4 if ``save_to_tag`` is enabled. This is the default behavior of *mutagen*; the underlying dependency used by ``lyrico`` to read ID3 tags.

  This has never caused any problem for me till date. And from my understanding you should be using ID3v2.4 tags anyways. I have used ``lyrico`` on hundreds of mp3 files and had no issues. You can always test ``lyrico`` on few songs and check. Or you can just disable ``save_to_tag``.

- **Song metadata** - Lyrics are fetched using a URL generated using song's artist name and title. This means that if the song has titles like:

  - ABC(acoustic)
  - ABC(live version)
  
  or an artist like:

  - XYZ(feat. Blah)

  the download might fail. Sometimes artist-name or title contain characters like '?'.  For this, Windows won't be able to create the text file as it is a restricted character. But the lyrics will be downloaded anyways and saved to tag if ``save_to_tag`` is enabled.

A note on mass downloading
===========================

Since ``lyrico`` is simply scraping lyrics off the HTML pages of the sources, please don't set ``source_dir`` to a folder having thousands of songs.

They might ban your bot. ``az_lyrics`` sometimes bans your IP (not sure if permanent) if you hit them with too many failed requests. Though, refreshing your IP by restarting your router or using a VPN solves that. Hence, ``az_lyrics`` as a source is disabled by default. Only use it if you are looking for recent lyrics.

Also, downloading 1000s of lyrics will be slow since ``lyrico`` does not batch-download. It sends one request to one source at a time. This is by design.

I personally use it at one or two albums at time and keep checking for any errors in ``log.txt``.


