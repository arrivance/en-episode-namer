import os
import sys
import re

import tvdb_api
import hachoir.parser

"""
Functions
"""

def debug_print(text): 
    """
    Prints verbose output if -d is in the flags
    """
    if "-d" in sys.argv: 
        print("DEBUG: ", text)

    return None

def file_renamer(file_item, ep_no, file_extension):
    """
    Renames files in the structure:
    Title - [SEASONxEPISODE] - Name of Episode
    """
    print("Original: " + file_item)

    try:
        # attempts to contact tvdb for the episode name
        episode = tvdb[title][season][ep_no]
        episodename = episode['episodename']
    except:
        # if it fails we leave it blank
        episodename = ""

    # replaces invalid characters that can't be file names
    episodename = episodename.replace('/', '').replace(':', '').replace('?', '')
    
    # if the episode number is 1 digit, we up it to 2 by prefixing an 0
    # so 1 would become 01
    if len(str(ep_no)) != 2:
        ins_ep_no = "0" + str(ep_no)
    else:
        ins_ep_no = str(ep_no)
    # if no file extension is passed as an argument, we take the previous items' one
    if file_extension == None:
        filename, file_extension = os.path.splitext(file_item)

    # we make the filename in the format
    filename = title + " - [" + str(season) + "x" + ins_ep_no + "] - " + episodename  + file_extension
    # print out the filename 
    print("Changed:  " + filename)

    # if it is on safe mode (default), we add in a verification
    if safe == True:
        verify = input("Are you sure? y/n | ")
        # if they don't verify, we skip the file
        if verify != "y":
            print("File not changed\n---")
            return False
        else: 
            # if it's y, we rename the file
            os.rename(file_item, filename)
            return True
    # otherwise, we simply rename
    else:
        os.rename(file_item, filename)
        return True
    print("Changed filename\n---")

def is_vid(filename): 
    """
    Uses the hachoir library to determine whether the 
    file is a video
    """
    try:
        # tries parsing the files and returning the mime type
        file_inst = hachoir.parser.createParser(filename)
        mimetype = str(file_inst.mime_type)
    except: 
        # if it fails, we presume it isn't a video
        return False

    if "video" in mimetype:
        # if the mime has video in it, we presume it is a video
        return True
    else:
        # otherwise, we presume it isn't
        return False



"""
Variable initilisation

"""
# we let the user put the name of the show themselves
title = str(input("What is the name of the show?: "))
# regex for episode name and season
# works for S13E10 and [13x10] formats
epre = re.compile("(E[0-9]{2,2}|x[0-9]{2,2})", re.IGNORECASE)
seasonre = re.compile("(S[0-9]{2,2}|[0-9]{1,2}x)", re.IGNORECASE)
# subtitle verification
subtitles = str(input("Are there subtitles? y/n: "))
sub_list = []

# list of all files in the directory
file_list = os.listdir()
# temporary file list, which we use to filter out non videos
file_list_temp = []

# instance of tvdb
tvdb = tvdb_api.Tvdb()

"""
One time processes
"""
# is safe mode on or not
if "-a" in sys.argv: 
    safe = False
else:
    safe = True

for x in file_list:
    filename, file_extension = os.path.splitext(x)

    if is_vid(x) == True: 
        # if its a video, we add it to the list
        file_list_temp.append(x)
    elif subtitles == "y" and file_extension == ".srt":
        # if we are checking for subtitles, (and it is one), we add it 
        # to the list
        sub_list.append(x)
    else:
        # debug output
        debug_print("removed " + filename+ " fileext " + file_extension)

# make the file list be the new list, and delete the temp one
file_list = sorted(file_list_temp)
del(file_list_temp)

debug_print(file_list)
debug_print(sub_list)


"""
File renaming and handling
"""

for file_item in file_list: 
    filename, file_extension = os.path.splitext(file_item)
    # regex's the file name to find the season and episode number
    season = int(seasonre.search(file_item).group(0).replace("x", "").replace("s", "").replace("X", "").replace("S", ""))
    ep_no = int(epre.search(file_item).group(0)[1:])
    # calls the file renamer function
    file_renamer(file_item, ep_no, file_extension)

# if we're doing subtitles, we repeat the same process but with files in the sub list
if subtitles == "y":
    print("Proceeding to subtitles...")
    for file_item in sub_list: 
        season = int(seasonre.search(file_item).group(0).replace("x", "").replace("s", "").replace("X", "").replace("S", ""))
        ep_no = int(epre.search(file_item).group(0)[1:])
        file_renamer(file_item, ep_no, ".srt") 
