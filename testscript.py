import os
import tvdb_api
import sys

title = str(input("What is the name of the show?: "))
season = int(input("What season?: "))
file_format = str(input("What file format are the files stored in?: "))

t = tvdb_api.Tvdb()
 
file_list = os.listdir()

x = 0
while x < len(file_list): 
    if file_format not in file_list[x]: 
        del(file_list[x])
    x += 1
    
ep_no = 1

for file_item in file_list: 
    print("Original: " + file_item)

    episode = t[title][season][ep_no]

    episodename = episode['episodename']
    
    if len(str(ep_no)) != 2:
        ins_ep_no = "0" + str(ep_no)
    else:
        ins_ep_no = str(ep_no)

    filename = title + " - " + "[" + str(season) + "x" + ins_ep_no + "]" + " - " + episodename + "." + file_format
    ep_no += 1
    print("Changed:  " + filename)
    verify = input("Are you sure? y/n")

    if verify != "y":
        sys.exit()
    else: 
        os.rename(file_item, filename)
    print("Changed filename")
    print("---")