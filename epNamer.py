import os
import sys
import re

from epNamerLib import epNamerLib

"""
Local functions
"""

def argumentParser(listOfArguments):
    """Parses arguments"""
    argumentParserFilter = {} 
    for argument in listOfArguments: 
        if argument in sys.argv:
            argumentParserFilter[listOfArguments[argument]] = True
        else:
            argumentParserFilter[listOfArguments[argument]] = False
    return argumentParserFilter

def episodeRenamer(fileItem):
    """Renames episodes using the epNamerLib"""
    filename, fileExtension = os.path.splitext(fileItem)
    season = int(seasonRe.search(fileItem).group(0).replace("x", "").replace("s", "").replace("X", "").replace("S", ""))
    epNumber = int(epRe.search(fileItem).group(0)[1:])
    # calls the file renamer function
    try:
        fileNewName = epNamerLibInst.episodeNamer(epNumber, season, options["showname"])
    except Exception as e:
        if "tvdb_shownotfound" in str(e):
            print("Showname not found in the TVDB_API.")
            sys.exit()
        raise e

    print("Original: " + fileItem)
    print("Changed:  " + fileNewName + fileExtension)

    # if it is on safe mode (default), we add in a verification
    if options["aggressive"] == False:
        verify = input("Are you sure? y/n | ")
        # if they don't verify, we skip the file
        if verify != "y":
            print("File not changed.\n---")
            return False
    try:
        epNamerLibInst.fileRenamer(fileItem, fileNewName)
    except Exception as e:
        print("An error occured while trying to rename the file.")
        epNamerLibInst.debugRaise(e)
    else:
        print("Changed filename\n---")

"""
Variables and instances
"""

argumentOptions = {
    "-a": "aggressive",
    "-d": "debug"
} 

acceptableInputs = (
    "yes", 
    "y"
)

options = argumentParser(argumentOptions)
# we let the user put the name of the show themselves
options["showname"] = str(input("What is the name of the show?: "))
# subtitle verification
options["subtitles"] = str(input("Are there subtitles? y/n: "))

epNamerLibInst = epNamerLib.epNamerLibFunc(options["debug"])
epNamerLibInst.debugOutput(options)

# regex for episode name and season
# works for S13E10 and [13x10] formats
epRe = re.compile("(E[0-9]{2,2}|x[0-9]{2,2})", re.IGNORECASE)
seasonRe = re.compile("(S[0-9]{1,2}|[0-9]{1,2}x)", re.IGNORECASE)

"""
File renaming and handling
"""

vidList = epNamerLibInst.fileFilterVid(os.listdir())
epNamerLibInst.debugOutput("list of videos ordered: " + str(vidList))

for fileItem in vidList: 
    # regex's the file name to find the season and episode number
    try:
        episodeRenamer(fileItem)
    except Exception as e:
        print("An error occured while trying to rename the file " + fileItem)
        epNamerLibInst.debugRaise(e)

# if we"re doing subtitles, we repeat the same process but with files in the sub list
if options["subtitles"] in acceptableInputs:
    print("Proceeding to subtitles...")
    subList = epNamerLibInst.fileFilterSub(os.listdir())
    epNamerLibInst.debugOutput("list of subtitles ordered:" + str(subList))
    for fileItem in subList: 
        try:
            episodeRenamer(fileItem)
        except Exception as e:
            epNamerLibInst.debugRaise(e)
            print("An error occured while trying to rename the file " + fileItem)
