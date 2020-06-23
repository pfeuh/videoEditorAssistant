#!/usr/bin/python
# -*- coding: utf-8 -*-

from PILdrawer import *

NB_CHARS = 128
CHAR_WIDTH = 8
CHAR_HEIGHT = 8
CHAR_RATIO = 5

class FONT():
    def __init__(self, fname):
        self.__font = open(fname, "rb").read(-1)
        self.__fname = fname
        assert len(self.__font) == 1024
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
            print char_fname
            sheet.save(char_fname)

if __name__ == "__main__":
    
    font = FONT("./ressource/font/ascii8.fnt")
    font.createGlyphes("./ressource/font/font_ascii8")
