#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---*********************************---
# ---*** Scrolled Text Atari Style ***---
# ---*********************************---

from PILdrawer import *
import screenBuffer

ATARI_BLUE = (0x49, 0x92, 0xB9, 0xff)
ATARI_WHITE = (0xe0, 0xe0, 0xe0, 0xff)
CURSOR = loadImage("./ressource/cursorFull.png")

def createImage(sheet, fname_gen):
    sheet.drawText()
    fname = fname_gen.get()
    sheet.save(fname)
    sys.stdout.write("Image %s generated!\n"%fname)

def generateScroll(text, font_name="ascii8", nb_pix=1, bg=ATARI_BLUE, fg=ATARI_WHITE, border=False, sound=False):
    pass
    #~ vname = "./out/text.mp4"
    pattern = "./in/OSVT_%04d.png"
    fname_gen = FNAME_GEN(pattern)
    font = FONT(font_name)
    console = CONSOLE()

    line_num = 0
    while 1:
        console.clearScreen()
        start = line_num * console.getCols()
        stop = start + console.getCols() * console.getRows()
        console.write(text[start:stop])
        sheet = SHEET(bg=bg, fg=fg, console=console)
        sheet.initConsole(x=0, y=0, font=font, border=True)
        createImage(sheet, fname_gen)
        line_num += 1
        if line_num * console.getCols() >= len(text):
            break
    
    
    
    #~ for car in text:
        #~ clicks.append(fname_gen.getCurrentIndex())
        #~ console.write(car)
        #~ for cnt in range(frame_per_character):
            #~ sheet = SHEET(bg=bg, fg=fg, console=console)
            #~ sheet.initConsole(font=font, border=border)
            #~ createImage(sheet, fname_gen, frame_per_character)
    
    #~ picToVideo(name_gen.getPattern(), vname)
    #~ return clicks

if __name__ == "__main__":

    deleteInputBuffer()
    text = open("scrolls/msieurReflex.txt").read(-1)
    screen_text = screenBuffer.SCREEN_BUFFER(text).getFormatedText()
    #~ print str(screen_text)
    generateScroll(screen_text, font_name="ascii8", nb_pix=1)
    
    
    
    
    #~ print generateScroll(text, font_name="ascii8", nb_pix=1)
    #~ picToVideo("./in/OSVT_%04d.png", "./out/text.mp4")
