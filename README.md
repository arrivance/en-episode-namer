# episode namer

As [TVNamer](https://github.com/dbr/tvnamer) failed to work for me, here is a TV show namer using the [tvdb\_api](https://github.com/dbr/tvdb_api).

It's a much simpler, less feature filled version.

- Designed exclusively for Python 3

##Installation:

- Download the latest version from the Releases tab at the top.
- Place the files into a folder, and open up a command prompt (Shift Right-Click > Open command window here)
- Type in `python setup.py install`
- Type ep_namer in the folder you wish to rename files in. 
- Follow the instructions.

##Features:

- Names files in the format 
    - `Showname - [SIDxEPID] - Episode Name`
- Allows for subtitles to be renamed

##Command arguments: 

- '-d': debug, allows for additional output for debugging purposes.
- '-a': aggressive mode, requires no verification for renaming files


##Licensing terms in LICENSE.md. 