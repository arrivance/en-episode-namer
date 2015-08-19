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

    def file_renamer_prep(self, ep_no, season):
        """
        Prepares a file name 
        """

        # instance of tvdb
        tvdb = tvdb_api.Tvdb()

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
        filename = self.options["title"] + " - [" + str(season) + "x" + ep_no + "] - " + episodename

        return filename
 
    def file_renamer(self, file_item, file_rename):
        """
        Adds the file extension to the file name generated, and
        renames the file.
        """
        filename, file_extension = os.path.splitext(file_item)
        file_rename = file_rename + file_extension

        try:
            os.rename(file_item, file_rename)
        except (IOError, OSError) as exception:
            print("An error occured when trying to rename the file. It may currently be in use.")
            debug_print(exception)
        except:
            print("An unknown error occured while trying to rename to the file.")
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
            # if it fails, we presume it isn't a video
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


