lyrico
========

``lyrico`` is a command line application which downloads lyrics for your songs. When given a folder, ``lyrico`` will:

- scan it, and all inner folders, for audio files
- read the metadata for all songs that it detects
- download the lyrics for each song
- embed the lyrics downloaded into the song (as standard lyrics tag) and also save it to a text file

Current version of ``lyrico`` supports only **unsynced lyrics**.

Support
=========

- **Audio Formats** - mp3, flac, m4a, mp4, wma, ogg/oga (Vorbis and FLAC).

- **Python** - Python 27 and Python 3 (tested on Python 3.5 Python 3.4)

- **OS** - Windows, Linux (tested on Ubuntu).


Installation
=============
Use the standard ``pip`` install::

    pip install lyrico

This will also install the dependencies. Hence, it is recommended to install ``lyrico`` on a separate `virtual environment <https://pypi.python.org/pypi/virtualenv>`_.

You can test if ``lyrico`` was installed correctly by running the 'lyrico' command, which now should be available::
    
    lyrico

This would give the following output::

    source_dir is not set. Please use the "set" command to set source_dir.
    use "lyrico --help" to view commands.
    Your current settings:

    ACTIONS
        save_to_file = True
        save_to_tag = False
        overwrite = False


    PATHS
        source_dir = None
        lyrics_dir = None


    SOURCES
        lyric_wikia = True
        musix_match = True
        lyricsmode = True
        az_lyrics = False

If you get this screen, that means ``lyrico`` and its dependencies were installed correctly.


If you see an error like ``ImportError: No module named mutagen.id3``, this means that the dependencies were not installed for some reason. In that case you can install them very easily with single command. Here's what you do:

1. Go to ``lyrico``'s `GitHub page <https://github.com/abhimanyuPathania/lyrico>`_.
2. Download repository as ZIP and extract the ``requirements.txt`` file from it. It is in the root directory of repository. This is the only file you need.
3. Open command prompt in directory containing the ``requirements.txt`` and run following command (if you're using a virtual environment, activate it before running the command)::

    pip install -r requirements.txt

   This will install all of the ``lyrico``'s dependencies and now you can try testing with the 'lyrico' command. It should give no errors.


Running ``lyrico``
=====================
``lyrico`` operates using two directories (folders):

- Source Directory (``source_dir``): This is the directory which ``lyrico`` scans for audio files. The scan also includes all the directories contained within.

- Lyrics Directory (``lyrics_dir``): This is where ``lyrico`` will save the lyrics' text files.

Before running ``lyrico`` you must set these using the ``set`` command. Values must be absolute paths to the directories. Once set, ``lyrico`` will remember your settings (which can be changed easily at any time). So this has to be done only for the first time.

This is how an example first-run would look like on Windows.

1. Set the ``source_dir``::
  
    lyrico set source_dir D:\test\Music

   This logs the following message::
       
       source_dir updated.
       lyrico will scan the following folder for audio files:
           D:\test\Music
   
   When setting ``source_dir``, the directory must exist beforehand. ``lyrico`` will **not create** the ``source_dir`` for you.

2. Set the ``lyrics_dir``::
    
    lyrico set lyrics_dir D:\test\Lyrics

   This logs the following in command prompt::

       Directory does not exist. Creating new one.
       lyrics_dir updated.
       lyrico will save lyrics files in the following folder:
           D:\test\Lyrics

   Unlike ``source_dir``, when setting the ``lyrics_dir`` to folder that does not exist (as in this example); ``lyrico`` **will** create it for you.

3. Run lyrico::

    lyrico

   This will start the application and it will start downloading the lyrics for songs that it detects in the ``source_dir``. You will be able to see the status (song name, lyrics URL) in the command prompt as it downloads, one at a time, the lyrics for each song.

   Finally it builds the log of whole operation and saves it in the ``log.txt`` file. ``log.txt`` is located in your ``lyrics_dir``.


Other Settings and Commands
=============================

Basic settings like ``source_dir`` and ``lyrics_dir`` can be repeatedly changed using the ``set`` command as described in the example above. There are few more settings that are available to control ``lyrico``'s actions. These actions can be either disabled or enabled.

- ``save_to_file`` - When enabled, ``lyrico`` will save the lyrics downloaded to a text file and put it in the ``lyrics_dir``. The naming convention of file is as follows:

   [artist name] - [title].txt
   
  where  [artist name] and [title] are extracted from the song's metadata. It either of this is not found, lyrics won't be downloaded and you will see that in the final ``log.txt``. This naming convention in the current version cannot be changed.

  **enabled by default**

- ``save_to_tag`` - When enabled, ``lyrico`` will embed the lyrics downloaded into song tags. ``lyrico`` uses the standard lyrics tags for different formats. This means, as long as your music player can read standard lyrics tags from the song's metadata, it should display them.
  
  **disabled by default**

- ``overwrite`` - When enabled, ``lyrico`` will always download the lyrics for a song ignoring they might already be present in the lyrics tag or in the ``lyrics_dir`` as a text file. After the download, it overwrites any existing lyrics in the tag or the text file.

  This setting is meant to avoid repetitive download of lyrics. For example, if there is a song 'ABC' in the ``source_dir``. And ``overwrite`` is **disabled**. When ``lyrico`` is run, it will first look into ``lyrics_dir`` if it already has lyrics. If yes, then it would ignore the song.

  ``overwrite`` takes into account, the ``save_to_file`` and ``save_to_tag`` settings to decide what to do. For ``save_to_file``, it looks in ``lyrics_dir`` and for ``save_to_tag`` it searches for existing lyrics in songs's metadata. Whenever there is a void, download happens and old lyrics will be replaced by downloaded ones in both, text file and song metadata as per your settings.

  **disabled by default**

The above three settings can be changed using ``enable`` and ``disable`` commands. This is how you will enable ``save_to_tag`` from its default 'disabled' setting::

    lyrico enable save_to_tag

This would log::

    save_to_tag enabled
    lyrico will embed the downloaded lyrics into song tags.

Similarly to disable ``save_to_file``::

    lyrico disable save_to_file

This gives following message in command prompt::

    save_to_file disabled
    lyrico will not save the downloaded lyrics to text files.


- *Viewing current settings* - To view current settings use the following command::

   lyrico --settings 

- *Help* - You can always view all the commands by asking for the help screen::

    lyrico --help

- ``lyrico`` **quick invocation** - you can supply ``source_dir`` along with ``lyrico`` command. The following command::

   lyrico full_path_to_source_dir

  is same as running the two commands::

    lyrico set source_dir full_path_to_source_dir
    lyrico
  
  However this won't work for the very first run. When running ``lyrico`` for the first time after installation, the ``source_dir`` must be set explicitly using the ``set`` command.

Lyrics Sources
================
``lyrico`` uses the following sources from where it downloads the lyrics:

1. `Lyric Wikia <http://lyrics.wikia.com/wiki/Lyrics_Wiki>`_ : ``lyric_wikia``

2. `musiXmatch <https://www.musixmatch.com/>`_ : ``musix_match``

3. `LYRICSMODE <http://www.lyricsmode.com/>`_ : ``lyricsmode``

4. `AZLyrics <http://www.azlyrics.com/>`_ : ``az_lyrics`` (**disabled by default**)

The search order is same as enumerated above and cannot be changed. You can, however, disable or enable any of the sources using the same ``enable`` and ``disable`` commands. When a source is disabled, it is simply skipped during the search.

For example, to enable AZLyrics::

    lyrico enable az_lyrics

Use the command line name for the source, which is mentioned after the link to the source in the above list. This logs the following message indicating that ``az_lyrics`` will be used as a source::

    az_lyrics enabled
    lyrico will use AZLyrics as a source for lyrics.

Or to disable Lyric Wikia::

    lyrico disable lyric_wikia:

This logs the following message::

    lyric_wikia disabled
    lyrico will not use Lyric Wikia as a source for lyrics.


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

``lyrico`` goodness
=====================

Here are somethings that ``lyrico`` does well:

- **No junk** - ``lyrico`` will not insert junk text into your lyrics files or audio tags. It won't create blank files or blank lyrics tags. Neither it would create lyrics files or tags containing errors etc.

- **Language** - Since ``lyrico`` uses your song's artist name and title to construct the URLs; so as long as they are correct and the source has the lyrics, it would work no matter which language.

- **foobar2000** - The poor performance of the `Lyric Show Panel 3 <https://www.foobar2000.org/components/view/foo_uie_lyrics3>`_ component was main reason I wrote this application. It simply won't work for me. ``lyrico`` plays nicely with 'Lyric Show Panel'. ``lyrico``'s file-naming convention matches 'Lyric Show Panel's default settings. Just point 'Lyric Show Panel' to your ``lyrics_dir`` and done.

  I recommend simply removing all of 'Lyric Show Panel' online sources and use offline mode (Tag search, Files search, Associations search) with ``lyrico``. It is the next best thing to automatic search. Because 'Lyric Show Panel' on failure embeds errors in lyrics files and tags!

  Even if you don't use foobar2000 or your music player cannot read lyrics from text files like that, you can always embed lyrics into tags which should work with any decent music player including **iTunes**.

- **log.txt** - ``log.txt`` created at end of every ``lyrico`` run is nice way to see what have you fetched. It show list of every song present in ``source_dir`` along with status of download or errors that happened. 

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

- **windows console** - If you are using Windows, like me, you must use some other font than the default 'raster fonts' in the command prompt to view in-prompt logging for songs using other characters than English in their metadata.

  But the problem does not end here. Even after enabling other allowed fonts like ``Consolas`` or ``Lucida Console``, you still won't be able to see in-prompt logging (you will see question marks or boxes) for Asian languages like Mandarin, Japanese, Korean etc. Though European language are displayed correctly.

  Despite any issues with windows console display, ``lyrico`` downloads and saves the lyrics correctly to files and tags.


Dependencies
================
``lyrico`` uses and thanks the following python packages:

- `glob2 <https://pypi.python.org/pypi/glob2>`_: to allow simple recursive directory search in Python 27.

- `requests <https://pypi.python.org/pypi/requests>`_: HTTP for Humans.

- `mutagen <https://pypi.python.org/pypi/mutagen>`_: to read tags from audio files and embed lyrics in tags for multiple audio formats.

- `beautifulsoup4 <https://pypi.python.org/pypi/beautifulsoup4>`_: to extract the lyrics.

- `win_unicode_console <https://pypi.python.org/pypi/win_unicode_console>`_: because Python 27, Unicode and command prompt is a nightmare.


- `docopt <https://pypi.python.org/pypi/docopt>`_: to create beautiful command-line interfaces.


A note on mass downloading
===========================

Since ``lyrico`` is simply scraping lyrics off the HTML pages of the sources, please don't set ``source_dir`` to a folder having thousands of songs.

They might ban your bot. ``az_lyrics`` sometimes bans your IP (not sure if permanent) if you hit them with too many failed requests. Though, refreshing your IP by restarting your router or using a VPN solves that. Hence, ``az_lyrics`` as a source is disabled by default. Only use it if you are looking for recent lyrics.

Also, downloading 1000s of lyrics will be slow since ``lyrico`` does not batch-download. It sends one request to one source at a time. This is by design.

I personally use it at one or two albums at time and keep checking for any errors in ``log.txt``.

Integration tests
=================
Run them:

    $ python -m unittest discover

Changelog
==========
- 0.6.0 Added support for ``oga`` audio format. Detect uppercase extensions in Linux.
- 0.5.0 Added musiXmatch and LYRICSMODE to sources. Include detection for licensing errors.
- 0.4.0 Added LYRICSnMUSIC and AZLyrics as sources. Expanded the command line interface to control sources. Added `requests <https://pypi.python.org/pypi/requests>`_ to dependencies.
- 0.3.0 Added support for ``ogg`` and ``wma`` audio formats. Replaced ``UNSYNCED LYRICS`` with ``LYRICS`` tags to embed lyrics in Vorbis Comments.
- 0.2.0 Added documentation and tutorial.
- 0.1.0 Initial release.
