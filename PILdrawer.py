#!/usr/bin/python
# -*- coding: utf-8 -*-

from console import *
from PIL import Image, ImageDraw, ImageFont
import sys
import os
import subprocess

INPUT_DIR = "./in/"
OUTPUT_DIR = "./out/"
FRM_EXT = ".PNG"
VIDEO_EXT = ".mp4"

#collecting arguments
DEBUG = "-debug" in sys.argv
for argnum, arg in enumerate(sys.argv):
    if arg == ("-w"):
        SHEET.WIDTH = int(argv[argnum+1])
    elif arg == ("-h"):
        SHEET.HEIGHT = int(argv[argnum+1])

if DEBUG:
    sys.stdout.write("debug mode active\n")

class SHEET():
    WIDTH = 1920
    HEIGHT = 1080
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    RED = (255, 0, 0, 255)
    GREEN = (0, 255, 0, 255)
    BLUE = (0, 0, 255, 255)
    TRANSPARENT = (0, 0, 0, 0)

    def __init__(self, width=None, height=None, bg=None, fg=None, console=None):
        if not width: width = SHEET.WIDTH
        if not height: height = SHEET.HEIGHT
        if not bg: bg = SHEET.TRANSPARENT
        if not fg: fg = SHEET.WHITE
        if not console: console = CONSOLE()
        self.__width = width
        self.__height = height
        self.__bg = bg
        self.__fg = fg
        self.__img = Image.new('RGBA', (self.__width, self.__height), self.__bg)
        self.__sheet = ImageDraw.Draw(self.__img)
        self.__x_origin = 0
        self.__y_origin = 0

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
        
    def save(self, fname):
        self.__img.save(fname, "PNG")

    def drawEllipse(self, x1, y1, x2, y2, color, **kwds):
        self.__sheet.ellipse([(x1, y1), (x2, y2)], fill=color, **kwds)

    def putDisc(self, x, y, d, color, **kwds):
        x, y, = self.__relocate(x, y)
        self.drawEllipse(x - d / 2, y - d / 2, x + d / 2, y + d / 2, color, **kwds)

    def putCircle(self, x, y, d, color, **kwds):
        x, y, = self.__relocate(x, y)
        self.__sheet.ellipse([(x - d / 2, y - d / 2), (x + d / 2, y + d / 2)], outline=color, fill=None, **kwds)

    def drawRectangle(self, x1, y1, x2, y2, color=None, **kwds):
        if not color: color = self.__fg
        self.__sheet.rectangle([(x1, y1,), (x2, y2,)], fill=color, **kwds)

    def putRectangle(self, x, y, w, h, color, **kwds):
        x, y, = self.__relocate(x, y)
        self.drawRectangle(x- w /2, y - h / 2, x + w / 2, y + h / 2, color, **kwds)
        
    def putText(self, x, y, text, color, **kwds):
        x, y, = self.__relocate(x, y)
        self.__sheet.text((x, y), text, fill=color, align="center", **kwds)

    def putBitmap(self, x, y, bitmap, color=None, **kwds):
        if not color: color = self.__fg
        x, y = self.__relocate(x, y)
        x -= bitmap.size[0] / 2
        y -= bitmap.size[1] / 2
        self.__sheet.bitmap((x, y), bitmap, fill=color, **kwds)

class COUNTER:
    # for image(s) naming
    def __init__(self):
        self.reset()
        
    def get(self):
        self.__counter += 1
        return self.__counter

    def reset(self):
        self.__counter = 0

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

def loadSheet():
    Image.open("./ressource/nikonSpeed.png")


Image.open("./ressource/nikonSpeed.png")

if __name__ == "__main__":

    ATARI_BLUE = (0x49, 0x92, 0xB9, 0xff)

    sheet = SHEET(bg=ATARI_BLUE)
    sheet.putDisc(0, 0, 100, SHEET.RED)
    sheet.setOrigin(sheet.getWidth()/2, sheet.getHeight()/2)
    sheet.putDisc(0, 0, 100, SHEET.GREEN)
    sheet.setOrigin(sheet.getWidth()-1, sheet.getHeight()-1)
    sheet.putDisc(0, 0, 100, SHEET.BLUE)
    sheet.setOrigin(0, 0)
    
    sheet.drawRectangle(100, 100, 200, 200, SHEET.RED)
    
    sheet.putBitmap(100, 100, Image.open("./ressource/nikonSpeed.png"), SHEET.WHITE)
    sheet.putBitmap(200, 200, Image.open("./ressource/nikonSpeed.png"), SHEET.WHITE)
    sheet.putBitmap(300, 300, Image.open("./ressource/nikonSpeed.png"), SHEET.WHITE)

    
    
    
    
    sheet.show()
    
    
    
    