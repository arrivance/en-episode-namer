import os
import tvdb_api
import sys
import re

import hachoir.parser

def debug_print(text): 
    if "-d" in sys.argv: 
        print("DEBUG: ", text)

    return None

def file_renamer(file_item, ep_no, file_extension):
    print("Original: " + file_item)

    try:
        episode = tvdb[title][season][ep_no]
        episodename = episode['episodename']
    except:
        episodename = ""

    episodename = episodename.replace('/', '').replace(':', '').replace('?', '')
    
    if len(str(ep_no)) != 2:
        ins_ep_no = "0" + str(ep_no)
    else:
        ins_ep_no = str(ep_no)

    if file_extension == None:
        filename, file_extension = os.path.splitext(file_item)

    filename = title + " - " + "[" + str(season) + "x" + ins_ep_no + "]" + " - " + episodename  + file_extension
    print("Changed:  " + filename)

    if safe == True:
        verify = input("Are you sure? y/n | ")
        if verify != "y":
            print("File not changed\n---")
            return False
        else: 
            os.rename(file_item, filename)
            return True
    else:
        os.rename(file_item, filename)
        return True
    print("Changed filename\n---")


def is_vid(filename): 
    try:
        file_inst = hachoir.parser.createParser(filename)
        mimetype = str(file_inst.mime_type)
    except: 
        return False

    if "video" in mimetype:
        return True
    else:
        return False


title = str(input("What is the name of the show?: "))
epre = re.compile("(E[0-9]{2,2}|x[0-9]{2,2})", re.IGNORECASE)
seasonre = re.compile("(S[0-9]{2,2}|[0-9]{1,2}x)", re.IGNORECASE)
subtitles = str(input("Are there subtitles? y/n: "))

if "-a" in sys.argv: 
    safe = False
else:
    safe = True

tvdb = tvdb_api.Tvdb()
 
file_list = os.listdir()
file_list_temp = []

sub_list = []

for x in file_list:
    filename, file_extension = os.path.splitext(x)

    if is_vid(x) == True: 
        file_list_temp.append(x)
    elif subtitles == "y" and file_extension == ".srt":
        sub_list.append(x)
    else:
        debug_print("removed " + filename+ " fileext " + file_extension)

file_list = sorted(file_list_temp)
del(file_list_temp)

debug_print(file_list)
debug_print(sub_list)

for file_item in file_list: 
    season = int(seasonre.search(file_item).group(0).replace("x", "").replace("s", "").replace("X", "").replace("S", ""))
    ep_no = int(epre.search(file_item).group(0)[1:])
    file_renamer(file_item, ep_no, None)

if subtitles == "y":
    print("Proceeding to subtitles...")
    for file_item in sub_list: 
        ep_no = int(epre.search(file_item).group(0)[1:])
        file_renamer(file_item, ep_no, ".srt") 
