import os
import sys
import re

import tvdb_api
import hachoir.parser

"""
Functions
"""

class ep_func():
    def __init__(self, options):
        self.options = options

    def debug_print(self, text): 
        """
        Prints verbose output if -d is in the flags
        """
        if self.options["debug"] == True: 
            print("DEBUG: ", text)

        return None

    def file_renamer(self, file_item, ep_no, season):
        """
        Renames files in the structure:
        Showname - [SIDxEPID] - Episode Name
        """

        filename, file_extension = os.path.splitext(file_item)

        # instance of tvdb
        tvdb = tvdb_api.Tvdb()
        print("Original: " + file_item)

        try:
            # attempts to contact tvdb for the episode name
            episode = tvdb[self.options["showname"]][season][ep_no]
            episodename = episode["episodename"]
        except:
            # if it fails we leave it blank
            episodename = ""

        # replaces invalid characters that can"t be file names
        episodename = episodename.replace("/", "").replace(":", "").replace("?", "")
        
        # if the episode number is 1 digit, we up it to 2 by prefixing an 0
        # so 1 would become 01
        if len(str(ep_no)) != 2:
            ep_no = "0" + str(ep_no)
        else:
            ep_no = str(ep_no)

        # we make the filename in the format
        filename = self.options["title"] + " - [" + str(season) + "x" + ep_no + "] - " + episodename  + file_extension
        # print out the filename 
        print("Changed:  " + filename)

        # if it is on safe mode (default), we add in a verification
        if self.options["aggressive"] == False:
            verify = input("Are you sure? y/n | ")
            # if they don"t verify, we skip the file
            if verify != "y":
                print("File not changed.\n---")
                return False

        # otherwise, we simply rename
        os.rename(file_item, filename)
        print("Changed filename\n---")
        return True

    def is_vid(self, filename): 
        """
        Uses the hachoir library to determine whether the 
        file is a video
        """
        try:
            # tries parsing the files and returning the mime type
            file_inst = hachoir.parser.createParser(filename)
            mimetype = str(file_inst.mime_type)
        except: 
            # if it fails, we presume it isn"t a video
            return False

        self.debug_print("Mimetype of " + filename + " : " + mimetype) 

        if mimetype[0:5] == "video":
            # if the mimetype starts with video, it's a video!
            return True
        else:
            # otherwise, we presume it isn't
            return False

    def file_filter_vid(self, file_list):
        """
        Filters videos from the file list
        """
        file_filter_temp = []
        for file_item in file_list:
            if self.is_vid(file_item) == True: 
                # if its a video, we add it to the list
                file_filter_temp.append(file_item)
            else:
                # debug output
                self.debug_print("non-vid removed " + file_item)

        return sorted(file_filter_temp)

    def file_filter_sub(self, file_list):
        """
        Filters subtitles from the file list
        """
        file_filter_temp = []
        for file_item in file_list: 
            filename, file_extension = os.path.splitext(file_item)
            if file_extension == ".srt":
                file_filter_temp.append(file_item)
            else:
                self.debug_print("non-sub removed " + file_item)

        return sorted(file_filter_temp)


