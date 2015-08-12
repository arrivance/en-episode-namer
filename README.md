# episode namer

As [TVNamer](https://github.com/dbr/tvnamer) failed to work for me, here is a TV show namer using the [tvdb\_api](https://github.com/dbr/tvdb_api).

THIS SOFTWARE IS PROVIDED AS-IS, NO RESPONSIBILITY IS TAKEN FOR ANY DAMAGES THAT OCCUR DUE TO RESULT OF THE PROGRAM.

How-to:

- Download ep_namer.py
- Place it in the folder containing all the media you wish to rename.
- Run ep_namer.py
	- Note: If you wish to verify all the files you can naming, open up a command prompt in the folder with ep_namer, and type: `ep_namer.py -s`
- Follow the instructions

Features:

- Names files in the format
	- `Showname - [SIDxEPID] - Episode Name`
- Allows for multiple file formats in the same folder
- Allows for subtitles to be renamed

Command arguments: 
	- '-d': debug, allows for additional output for debugging purposes.
	- '-s': safe mode, requires the user to verify all renaming. recommend for novice users.

Licensing terms in LICENSE.md. 