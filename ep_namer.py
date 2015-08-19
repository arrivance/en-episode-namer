import os
import sys
import re

from ep_lib import ep_lib

"""
Local functions
"""

def argument_parser(args):
    is_arg_true = {} 
    for argument in args: 
        if argument in sys.argv:
            is_arg_true[args[argument]] = True
        else:
            is_arg_true[args[argument]] = False
    return is_arg_true

def file_renamer(file_item):
    filename, file_extension = os.path.splitext(file_item)
    season = int(seasonre.search(file_item).group(0).replace("x", "").replace("s", "").replace("X", "").replace("S", ""))
    ep_no = int(epre.search(file_item).group(0)[1:])
    # calls the file renamer function
    file_rename = ep_lib_inst.file_renamer_prep(ep_no, season)

    print("Original: " + file_item)
    print("Changed:  " + file_rename + file_extension)

    # if it is on safe mode (default), we add in a verification
    if options["aggressive"] == False:
        verify = input("Are you sure? y/n | ")
        # if they don't verify, we skip the file
        if verify != "y":
            print("File not changed.\n---")
            return False
    else:
        if ep_lib_inst.file_renamer(file_item, file_rename) == True:
            print("Changed filename\n---")

"""
Variables and instances
"""

argument_options = {
    "-a": "aggressive",
    "-d": "debug"
} 

options = argument_parser(argument_options)
# we let the user put the name of the show themselves
options["showname"] = str(input("What is the name of the show?: "))
# subtitle verification
options["subtitles"] = str(input("Are there subtitles? y/n: "))


if options["subtitles"] == "y":
    options["subtitles"] = True
else:
    options["subtitles"] = False

ep_lib_inst = ep_lib.ep_func(options)

ep_lib_inst.debug_print(options)

# regex for episode name and season
# works for S13E10 and [13x10] formats
epre = re.compile("(E[0-9]{2,2}|x[0-9]{2,2})", re.IGNORECASE)
seasonre = re.compile("(S[0-9]{2,2}|[0-9]{1,2}x)", re.IGNORECASE)

"""
File renaming and handling
"""

vid_list = ep_lib_inst.file_filter_vid(os.listdir())  
ep_lib_inst.debug_print("list of videos ordered: " + str(vid_list))

for file_item in vid_list: 
    # regex's the file name to find the season and episode number
    try:
        file_renamer(file_item)
    except:
        print("An error occured while trying to rename the file " + file_item)

# if we"re doing subtitles, we repeat the same process but with files in the sub list
if options["subtitles"] == True:
    print("Proceeding to subtitles...")
    sub_list = ep_lib_inst.file_filter_sub(os.listdir())
    ep_lib_inst.debug_print("list of subtitles ordered:" + str(sub_list))
    for file_item in sub_list: 
        try:
            file_renamer(file_item)
        except:
            print("An error occured while trying to rename the file " + file_item)
