# episode namer

As [TVNamer](https://github.com/dbr/tvnamer) failed to work for me, here is a TV show namer using the [tvdb\_api](https://github.com/dbr/tvdb_api).

It's a much simpler, less feature filled version.

##Pre-requisties: 

- Designed exclusively for Python 3
- All dependencies are in dependencies.txt.

##How-to:

- Download ep_namer.py
- Place it in the folder containing all the media you wish to rename.
- Run ep_namer.py
    - Note: If you wish to verify all the files you can naming, open up a command prompt in the folder with ep_namer, and type: `ep_namer.py -s`
- Follow the instructions

##Features:

- Names files in the format 
    - `Showname - [SIDxEPID] - Episode Name`
- Allows for subtitles to be renamed

##Command arguments: 

- '-d': debug, allows for additional output for debugging purposes.
- '-a': aggressive mode, requires no verification for renaming files


##Licensing terms in LICENSE.md. 