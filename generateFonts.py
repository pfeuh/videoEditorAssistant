#!/usr/bin/python
# -*- coding: utf-8 -*-

from PILdrawer import *
import os

ERROR_TEXT = """Bad parameter(s)
-all   : rebuild all application's fonts
-iname : builds and adds the font -iname
-oname : (optional) change name of the new built font
"""

FONT_DIR = "./font/"
FONT_FILE_SIZE = 1024
FONT_EXT = ".FNT"
NB_CHARS = 128
CHAR_WIDTH = 8
CHAR_HEIGHT = 8
CHAR_RATIO = 5

class FONT():
    def __init__(self, fname):
        if not os.path.exists(fname):
            raise Exception("file %s not found!"%fname, 2)
        self.__font = open(fname, "rb").read(-1)
        self.__fname = fname
        if len(self.__font) != FONT_FILE_SIZE:
            raise Exception("Bad font size on \"%s\": got %d, expected %d"%(fname, len(self.__font), FONT_FILE_SIZE))
        self.__glyphes = []
        for x in range(NB_CHARS):
            glyphe = []
            stuff = self.__font[x*8: x*8 + 8]
            for col in range(8):
                line = []
                value = ord(stuff[col])
                for idx in range(8):
                    if (value & NB_CHARS):
                        line.append(1)
                    else:
                        line.append(0)
                    value *= 2
                glyphe.append(line)
            self.__glyphes.append(glyphe)

    def drawPixel(self, sheet, x, y, ratio):
        sheet.drawRectangle(x*ratio, y*ratio, x*ratio+ratio-1, y*ratio+ratio-1)

    def getGlyphes(self):
        return self.__glyphes
        
    def createGlyphes(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
        for carnum in range(NB_CHARS):
            glyphe = self.__glyphes[carnum]
            sheet = SHEET(width=CHAR_WIDTH*CHAR_RATIO, height=CHAR_HEIGHT*CHAR_RATIO, bg=SHEET.TRANSPARENT, fg=SHEET.WHITE)
            for y in range(CHAR_HEIGHT):
                for x in range(CHAR_WIDTH):
                    if glyphe[y][x]:
                        self.drawPixel(sheet, x, y, CHAR_RATIO)
            fn, ext = os.path.splitext(self.__fname)
            char_fname = os.path.join(folder, "%03d"%carnum + ".png")
            sheet.save(char_fname)

def generateFont(fname, font_name=None):
    if font_name == None:
        font_dir_name = FONT_DIR + os.path.splitext(os.path.basename(fname))[0]
    else:
        font_dir_name = FONT_DIR + font_name
    sys.stdout.write("%s -> %s\n"%(fname, font_dir_name))
    font = FONT(fname)
    font.createGlyphes(font_dir_name)

def generateAllFonts():
    for fname in os.listdir(FONT_DIR):
        filename = os.path.join(FONT_DIR, fname)
        if os.path.isfile(filename):
            if not os.path.isdir(filename):
                dir_name = os.path.join(FONT_DIR, os.path.splitext(fname)[0])            
                if os.path.splitext(fname)[1].upper() == FONT_EXT:
                    generateFont(filename)

if __name__ == "__main__":

    iname = None
    oname = None

    for index, arg in enumerate(sys.argv):
        if arg == "-all":
            generateAllFonts()
            sys.exit(0)
        elif arg == "-iname":
            iname = sys.argv[index + 1]
        elif arg == "-oname":
            oname = sys.argv[index + 1]
            
    if iname != None:
        generateFont(iname, oname)
        sys.exit(0)
    else:
        sys.stderr.write(ERROR_TEXT)
        sys.exit(1)
