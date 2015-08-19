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
    if options["debug"] == True: 
        print("DEBUG: ", text)

    return None

def file_renamer(file_item, ep_no, season, file_extension):
    """
    Renames files in the structure:
    Title - [SEASONxEPISODE] - Name of Episode
    """

    # instance of tvdb
    tvdb = tvdb_api.Tvdb()
    print("Original: " + file_item)

    try:
        # attempts to contact tvdb for the episode name
        episode = tvdb[options['title']][season][ep_no]
        episodename = episode['episodename']
    except:
        # if it fails we leave it blank
        episodename = ""

    # replaces invalid characters that can't be file names
    episodename = episodename.replace('/', '').replace(':', '').replace('?', '')
    
    # if the episode number is 1 digit, we up it to 2 by prefixing an 0
    # so 1 would become 01
    if len(str(ep_no)) != 2:
        ep_no = "0" + str(ep_no)
    else:
        ep_no = str(ep_no)
    # if no file extension is passed as an argument, we take the previous items' one
    if file_extension == None:
        filename, file_extension = os.path.splitext(file_item)

    # we make the filename in the format
    filename = options['title'] + " - [" + str(season) + "x" + ep_no + "] - " + episodename  + file_extension
    # print out the filename 
    print("Changed:  " + filename)

    # if it is on safe mode (default), we add in a verification
    if options["aggressive"] == False:
        verify = input("Are you sure? y/n | ")
        # if they don't verify, we skip the file
        if verify != "y":
            print("File not changed.\n---")
            return False

    # otherwise, we simply rename
    os.rename(file_item, filename)
    print("Changed filename\n---")
    return True

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

def file_filter_vid(file_list):
    file_filter_temp = []
    for x in file_list:
        filename, file_extension = os.path.splitext(x)

        if is_vid(x) == True: 
            # if its a video, we add it to the list
            file_filter_temp.append(x)
        else:
            # debug output
            debug_print("non-vid removed " + filename+ " fileext " + file_extension)

    return sorted(file_filter_temp)

def file_filter_sub(file_list):
    file_filter_temp = []
    for x in file_list: 
        if file_extension == ".srt":
            file_filter_sub.append(x)
        else:
            debug_print("non-sub removed " + filename + "fileext" + file_extension)

    return sorted(file_filter_temp)

def argument_parser(args):
    is_arg_true = {} 
    for argument in args: 
        if argument in sys.argv:
            is_arg_true[args[argument]] = True
        else:
            is_arg_true[args[argument]] = False
    return is_arg_true

"""
Variables and instances
"""

argument_options = {
    "-a": "aggressive",
    "-d": "debug"
} 

options = argument_parser(argument_options)
debug_print(options)

# we let the user put the name of the show themselves
options['title'] = str(input("What is the name of the show?: "))
# subtitle verification
options['subtitles'] = str(input("Are there subtitles? y/n: "))

if options['subtitles'] == "y":
    options['subtitles'] = True
else:
    options['subtitles'] = False


# regex for episode name and season
# works for S13E10 and [13x10] formats
epre = re.compile("(E[0-9]{2,2}|x[0-9]{2,2})", re.IGNORECASE)
seasonre = re.compile("(S[0-9]{2,2}|[0-9]{1,2}x)", re.IGNORECASE)

"""
File renaming and handling
"""

vid_list = file_filter_vid(os.listdir())  
debug_print("list of videos ordered: " + str(vid_list))

for file_item in vid_list: 
    filename, file_extension = os.path.splitext(file_item)
    # regex's the file name to find the season and episode number
    try:
        season = int(seasonre.search(file_item).group(0).replace("x", "").replace("s", "").replace("X", "").replace("S", ""))
        ep_no = int(epre.search(file_item).group(0)[1:])
        # calls the file renamer function
        file_renamer(file_item, ep_no, season, file_extension)
    except:
        print("Unable to find the season/episode number for file: " + file_item)

# if we're doing subtitles, we repeat the same process but with files in the sub list
if options['subtitles'] == True:
    print("Proceeding to subtitles...")
    sub_list = file_filter_sub(os.listdir())
    debug_print("list of subtitles ordered:" + str(sub_list))
    for file_item in sub_list: 
        try:
            season = int(seasonre.search(file_item).group(0).replace("x", "").replace("s", "").replace("X", "").replace("S", ""))
            ep_no = int(epre.search(file_item).group(0)[1:])
            file_renamer(file_item, ep_no, season, ".srt") 
        except:
            print("Unable to find the season/episode number for file: " + file_item)
