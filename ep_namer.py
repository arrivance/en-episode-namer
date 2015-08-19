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
    # regex"s the file name to find the season and episode number
    try:
        season = int(seasonre.search(file_item).group(0).replace("x", "").replace("s", "").replace("X", "").replace("S", ""))
        ep_no = int(epre.search(file_item).group(0)[1:])
        # calls the file renamer function
        ep_lib_inst.file_renamer(file_item, ep_no, season)
    except:
        print("Unable to find the season/episode number for file: " + file_item)

# if we"re doing subtitles, we repeat the same process but with files in the sub list
if options["subtitles"] == True:
    print("Proceeding to subtitles...")
    sub_list = ep_lib_inst.file_filter_sub(os.listdir())
    ep_lib_inst.debug_print("list of subtitles ordered:" + str(sub_list))
    for file_item in sub_list: 
        try:
            season = int(seasonre.search(file_item).group(0).replace("x", "").replace("s", "").replace("X", "").replace("S", ""))
            ep_no = int(epre.search(file_item).group(0)[1:])
            ep_lib_inst.file_renamer(file_item, ep_no, season) 
        except:
            print("Unable to find the season/episode number for file: " + file_item)
