#!/usr/bin/python
# -*- coding: utf-8 -*-

from console import *
from PIL import Image, ImageDraw, ImageFont
import sys
import os
import subprocess

INPUT_DIR = "./in/"
OUTPUT_DIR = "./out/"
FRM_EXT = ".png"
VIDEO_EXT = ".mp4"
NB_GLYPHES = 128
FONT_DIR = "./font/"

#collecting arguments
DEBUG = "-debug" in sys.argv
for argnum, arg in enumerate(sys.argv):
    if arg == ("-w"):
        SHEET.WIDTH = int(argv[argnum+1])
    elif arg == ("-h"):
        SHEET.HEIGHT = int(argv[argnum+1])

if DEBUG:
    sys.stdout.write("debug mode active\n")

def deleteInputBuffer(idir=INPUT_DIR):
    for entry in os.listdir(idir):
        filename = os.path.join(idir, entry)
        if os.path.isfile(filename):
            os.remove(filename)
    
def loadImage(fname):
    return Image.open(fname)

class SHEET():
    WIDTH = 1920
    HEIGHT = 1080
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    RED = (255, 0, 0, 255)
    GREEN = (0, 255, 0, 255)
    BLUE = (0, 0, 255, 255)
    TRANSPARENT = (0, 0, 0, 0)

    def __init__(self, width=None, height=None, bg=None, fg=None, console=None,fname=None):
        if not width: width = SHEET.WIDTH
        if not height: height = SHEET.HEIGHT
        if not bg: bg = SHEET.TRANSPARENT
        if not fg: fg = SHEET.WHITE
        self.__bg = bg
        self.__fg = fg
        if fname != None:
            self.__img = Image.open(fname)
            self.__width = self.__img.size[0]
            self.__height = self.__img.size[1]
        else:
            self.__width = width
            self.__height = height
            self.__img = Image.new('RGBA', (self.__width, self.__height), self.__bg)
        if not console: console = CONSOLE()
        self.__console = console
        self.initConsole()
        self.__sheet = ImageDraw.Draw(self.__img)
        # one can define a new origin for putXxxxx methods
        self.__x_origin = 0
        self.__y_origin = 0

    def initConsole(self, x=0, y=0, font=None, border=False):
        if font == None:
            self.__font = FONT("./font/font_ascii8")
        else:
            self.__font = font
        self.__glyphe_width = self.__font.getGlyphe(0).size[0]
        self.__glyphe_height = self.__font.getGlyphe(0).size[1]
        w = self.__glyphe_width * self.__console.getCols()
        h = self.__glyphe_height * self.__console.getRows()
        self.__x_console_offset = (self.getWidth() - w) /2
        self.__y_console_offset = (self.getHeight() - h) /2
        if border:
            coordinates = (
                (0, 0 , self.__x_console_offset-1,  self.__height-1), #left border
                (0, 0 , self.__width-1,  self.__y_console_offset-1), #top border
                (self.__width -self.__x_console_offset, 0 , self.__width-1, self.__height-1), # right border
                (0, self.__height-self.__y_console_offset , self.__width-1, self.__height-1 ))
            for x1, y1, x2, y2 in coordinates:
                self.drawRectangle(x1, y1, x2, y2, SHEET.BLACK)

    def write(self, text):
        self.__console.write(text)

    def clearScreen(self):
        self.__console.clearScreen()

    def gotoXY(self, x, y):
        self.__console.gotoXY(x, y)

    def getXY(self):
        return self.__console.getXY()

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getImg(self):
        return self.__img

    def getSheet(self):
        return self.__sheet

    def setOrigin(self, x, y):
        self.__x_origin = x
        self.__y_origin = y
        
    def __relocate(self, x, y):
        return x + self.__x_origin, y + self.__y_origin

    def show(self):
        self.__img.show()
        
    def save(self, fname, nb_frames=1):
        for cnt in range(nb_frames):
            self.__img.save(fname, "PNG")

    def drawEllipse(self, x1, y1, x2, y2, color=None, **kwds):
        if color == None:color = self.__fg
        self.__sheet.ellipse([(x1, y1), (x2, y2)], fill=color, **kwds)

    def putDisc(self, x, y, d, color=None, **kwds):
        if color == None:color = self.__fg
        x, y, = self.__relocate(x, y)
        self.drawEllipse(x - d / 2, y - d / 2, x + d / 2, y + d / 2, color, **kwds)

    def putCircle(self, x, y, d, color=None, **kwds):
        if color == None:color = self.__fg
        x, y, = self.__relocate(x, y)
        self.__sheet.ellipse([(x - d / 2, y - d / 2), (x + d / 2, y + d / 2)], outline=color, fill=None, **kwds)

    def drawRectangle(self, x1, y1, x2, y2, color=None, **kwds):
        if color == None:color = self.__fg
        self.__sheet.rectangle([(x1, y1,), (x2, y2,)], fill=color, **kwds)

    def putRectangle(self, x, y, w, h, color=None, **kwds):
        if color == None:color = self.__fg
        x, y, = self.__relocate(x, y)
        self.drawRectangle(x- w /2, y - h / 2, x + w / 2, y + h / 2, color, **kwds)
        
    def putText(self, x, y, text, color=None, **kwds):
        if color == None:color = self.__fg
        x, y, = self.__relocate(x, y)
        self.__sheet.text((x, y), text, fill=color, align="center", **kwds)

    def putBitmap(self, x, y, bitmap, color=None, **kwds):
        if color == None:color = self.__fg
        x, y = self.__relocate(x, y)
        x -= bitmap.size[0] / 2
        y -= bitmap.size[1] / 2
        self.__sheet.bitmap((x, y), bitmap, fill=color, **kwds)

    def putGlyphe(self, x, y, bitmap, color=None, **kwds):
        if color == None:color = self.__fg
        x = x * self.__glyphe_width + self.__x_console_offset
        y = y * self.__glyphe_height + self.__y_console_offset
        self.__sheet.bitmap((x, y), bitmap, fill=color, **kwds)

    def drawText(self):
        for index in range(self.__console.getRows() *self.__console.getCols()):
            glyphe = self.__font.getGlyphe(self.__console.read(index))
            x = index % self.__console.getCols()
            y = index / self.__console.getCols()
            self.putGlyphe(x, y, glyphe, color=None)

    def addCursor(self, cursor):
        x, y = self.getXY()
        self.putGlyphe(x, y, cursor, color=None)

class COUNTER:
    # for image(s) naming
    def __init__(self):
        self.reset()
        
    def get(self):
        self.__counter += 1
        return self.__counter

    def reset(self):
        self.__counter = 0
        
    def getCurrentIndex(self):
        return self.__counter

class FNAME_GEN():
    def __init__(self, pattern):
        self.__pattern = pattern
        self.__counter = COUNTER()
        
    def get(self):
        return self.__pattern%self.__counter.get()
        
    def reset(self):
        self.__counter.reset()
    
    def getPattern(self):
        return self.__pattern

    def getCurrentIndex(self):
        return self.__counter.getCurrentIndex()
    
class FONT():
    def __init__(self, fname):
        fname = FONT_DIR + fname
        self.__charset=[]
        for index in range(NB_GLYPHES):
            iname = fname + "/%03d.png"%index
            if os.path.exists(iname):
                self.__charset.append(loadImage(iname))
            else:
                self.__charset.append(loadImage("./ressource/defaultGlyphe.png"))
    
    def getGlyphe(self, index):
        return self.__charset[index]

    def getGlypheWidth(self):
        return self.__charset[0].size[0]
        
    def getGlypheHeight(self):
        return self.__charset[0].size[1]
        
def picToVideo(fname, vname):
    if DEBUG:
        sys.stdout.write("creating  video %s\n"%(vname))
        sys.stdout.write("from images %s\n"%(fname))
        
    if os.path.exists(vname):
        if DEBUG:
            sys.stdout.write("video %s already exists, let's overwrite it!!\n"%(vname))
        os.remove(vname)

    params = ["ffmpeg"]
    params.append("-start_number")
    params.append("1")
    params.append("-i")
    params.append(fname)
    params.append(vname)
    subprocess.call(params)

if __name__ == "__main__":

    pass

    sheet = SHEET()
    sheet.initConsole(border=True)
    sheet.show()



    #~ deleteInputBuffer()

    #~ from random import randrange

    #~ ATARI_BLUE = (0x49, 0x92, 0xB9, 0xff)
    #~ ATARI_WHITE = (0xe0, 0xe0, 0xe0, 0xff)

    #~ console = CONSOLE()
    #~ counter = COUNTER()
    #~ font = FONT("arex")

    #~ for car in "Pfeuh proundly presents\n\nFUSEE INTERPLANETAIRE":
        #~ sheet = SHEET(bg=ATARI_BLUE, fg=ATARI_WHITE, console = console)
        #~ sheet.initConsole(font=font)
        #~ sheet.write(car)
        #~ sheet.drawText()
        #~ sheet.save("./in/test_%04d.png"%counter.get())
    
    #~ sheet.show()
    #~ picToVideo("./in/test_%04d.png", "./out/text.mp4")
    
    
    
    
    