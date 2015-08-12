import os
import tvdb_api
import sys

def debug_print(text): 
    if "-d" in sys.argv: 
        print("DEBUG: ", text)

    return None

def file_renamer(file_item, ep_no, file_extension):
    print("Original: " + file_item)
    episode = t[title][season][ep_no]
    episodename = episode['episodename']

    episodename = episodename.replace('/', '')
    episodename = episodename.replace(':', '')
    
    if len(str(ep_no)) != 2:
        ins_ep_no = "0" + str(ep_no)
    else:
        ins_ep_no = str(ep_no)


    if file_extension == None:
        filename, file_extension = os.path.splitext(file_item)
    filename = title + " - " + "[" + str(season) + "x" + ins_ep_no + "]" + " - " + episodename  + file_extension
    ep_no += 1
    print("Changed:  " + filename)

    if safe == True:
        verify = input("Are you sure? y/n | ")
        if verify != "y":
            sys.exit()
        else: 
            os.rename(file_item, filename)
    else:
        os.rename(file_item, filename)
    print("Changed filename")
    print("---")

title = str(input("What is the name of the show?: "))
season = int(input("What season?: "))
file_format = str(input("What file format(s) are the files stored in? (seperate different formats with a comma): "))
file_format = file_format.split(',')
file_format_temp = []

for x in file_format: 
    x = x.replace(' ', '')
    file_format_temp.append(x)

file_format = file_format_temp
del(file_format_temp)

ep_no = 1
subtitles = str(input("Are there subtitles? y/n: "))

if "-s" in sys.argv: 
    safe = True
else:
    safe = False

t = tvdb_api.Tvdb()
 
file_list = os.listdir()
file_list_temp = []

sub_list = []
for x in file_list:
    filename, file_extension = os.path.splitext(x)

    if file_extension.replace('.', '') in file_format: 
        file_list_temp.append(x)
    elif subtitles == "y" and file_extension == ".srt":
        sub_list.append(x)
    else:
        debug_print("removed " + filename+ " fileext " + file_extension)

file_list = sorted(file_list_temp)
del(file_list_temp)

debug_print(file_list)

for file_item in file_list: 
    file_renamer(file_item, ep_no, None)

print("Proceeding to subtitles...")

ep_no = 1
if subtitles == "y":
    for file_item in sub_list: 
        file_renamer(file_item, ep_no, ".srt")
