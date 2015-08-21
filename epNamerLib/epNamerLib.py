import os
import sys
import re

import tvdb_api
import hachoir.parser

"""
Functions
"""
class epNamerLibFunc():
    def __init__(self, debug=False):
        self.debug = debug

    def debugOutput(self, text): 
        """Prints verbose output if -d is in the flags"""
        if self.debug == True: 
            print("DEBUG: ", text)

        pass

    def debugRaise(self, error):
        """Instead of ignoring errors, raises them if debug is one"""
        if self.debug == True:
            raise error
        pass

    def episodeNamer(self, episodeNumber, season, showName):
        """Prepares a file name """

        # instance of tvdb
        tvdb = tvdb_api.Tvdb()

        # attempts to contact tvdb for the episode name
        showInstance = tvdb[showName]
        # episode number
        episodeName = showInstance[season][episodeNumber]["episodename"]
        # we might have the showname, /but/ it might not be properly capitalized
        showName = showInstance["seriesname"]

        # replaces invalid characters that can"t be file names
        episodeName = episodeName.replace("/", "").replace(":", "").replace("?", "")
        
        # if the episode number is 1 digit, we up it to 2 by prefixing an 0
        # so 1 would become 01
        if len(str(episodeNumber)) != 2: episodeNumber = "0" + str(episodeNumber)

        # we make the filename in the format
        fileName = showName + " - [" + str(season) + "x" + str(episodeNumber) + "] - " + episodeName

        return fileName
 
    def fileRenamer(self, fileItem, fileNewName):
        """Adds the file extension to the file name generated, and renames the file."""

        fileName, fileExtension = os.path.splitext(fileItem)
        fileNewName = fileNewName + fileExtension

        os.rename(fileItem, fileNewName)

    def is_vid(self, fileName): 
        """Uses the hachoir library to determine whether the file is a video"""

        try:
            # tries parsing the files and returning the mime type
            fileInstance = hachoir.parser.createParser(fileName)
            mimetype = str(fileInstance.mime_type)
        except Exception as e: 
            # it'll fail on subtitles, but rather than crashing, we 
            # simply ignore it and assume the error 100% confirms
            # it isn't a video
            return False

        if mimetype[0:5] == "video":
            # if the mimetype starts with video, it's a video!
            return True
        
        return False

    def fileFilterVid(self, fileList):
        """Filters videos from the file list"""

        fileFilterTemp = []
        for fileItem in fileList:
            if self.is_vid(fileItem) == True: 
                # if its a video, we add it to the list
                fileFilterTemp.append(fileItem)
            else:
                # debug output
                self.debugOutput("non-vid removed " + fileItem)

        return sorted(fileFilterTemp)

    def fileFilterSub(self, fileList):
        """Filters subtitles from the file list"""

        fileFilterTemp = []
        for fileItem in fileList: 
            fileName, fileExtension = os.path.splitext(fileItem)
            if fileExtension == ".srt":
                fileFilterTemp.append(fileItem)
            else:
                self.debugOutput("non-sub removed " + fileItem)

        return sorted(fileFilterTemp)

