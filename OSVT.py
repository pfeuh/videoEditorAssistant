#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---*****************************---
# ---*** Old School Video Text ***---
# ---*****************************---

from PILdrawer import *

ATARI_BLUE = (0x49, 0x92, 0xB9, 0xff)
ATARI_WHITE = (0xe0, 0xe0, 0xe0, 0xff)
CURSOR = loadImage("./ressource/cursorFull.png")

def createImage(sheet, fname_gen, frame_per_character):
    sheet.drawText()
    if fname_gen.getCurrentIndex() % 24 < 12:
        sheet.addCursor(CURSOR)
    sheet.save(fname_gen.get(), frame_per_character)
    sys.stdout.write('.')
    if not fname_gen.getCurrentIndex() % 25:
        sys.stdout.write('\n')

def generateVideoText(text, font_name="ascii8", frame_per_character=5, preframes=0, postframes=50, bg=ATARI_BLUE, fg=ATARI_WHITE, border=False):
    vname = "./out/text.mp4"
    console = CONSOLE()
    pattern = "./in/OSVT_%04d.png"
    fname_gen = FNAME_GEN(pattern)
    font = FONT(font_name)
    size = len(text) * frame_per_character + preframes + postframes
    sys.stdout.write("Starting to generate %s size:%d frames\n"%(vname, size))
    
    if preframes != 0:
        for cnt in range(preframes):
            sheet = SHEET(bg=bg, fg=fg, console=console)
            sheet.initConsole(font=font, border=border)
            createImage(sheet, fname_gen, preframes)

    for car in text:
        for cnt in range(frame_per_character):
            sheet = SHEET(bg=bg, fg=fg, console=console)
            sheet.initConsole(font=font, border=border)
            sheet.write(car)
            createImage(sheet, fname_gen, frame_per_character)
    
    if postframes != 0:
        for cnt in range(postframes):
            sheet = SHEET(bg=bg, fg=fg, console=console)
            sheet.initConsole(font=font, border=border)
            createImage(sheet, fname_gen, postframes)
        
    #~ picToVideo(name_gen.getPattern(), vname)

if __name__ == "__main__":

    deleteInputBuffer()
    text = "Pfeuh proundly presents\n\nFUSEE INTERPLANETAIRE"
    #~ text = "\n\n\n\n\n\n\n\n\n\nPfeuh proundly presents\n\nFUSEE INTERPLANETAIRE"
    #~ generateVideoText(text, font_name="ascii8", frame_per_character=1, preframes=0, postframes=2, border=True)
    generateVideoText(text, font_name="ascii8", frame_per_character=1, preframes=0, postframes=2)
    #~ generateVideoText(text)
    #~ picToVideo("./in/OSVT_%04d.png", "./out/text.mp4")
