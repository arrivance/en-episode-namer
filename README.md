# episode namer

An alternative to [TVNamer](https://github.com/dbr/tvnamer), built using the [tvdb\_api](https://github.com/dbr/tvdb_api).
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
    - with the Episode Name being pulled from tvdb.
- Allows for subtitles to be renamed

##Command arguments: 

- '-d': debug, allows for additional output for debugging purposes.
- '-a': aggressive mode, requires no verification for renaming files


###Licensing terms in LICENSE.md. 