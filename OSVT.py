#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---*****************************---
# ---*** Old School Video Text ***---
# ---*****************************---

from PILdrawer import *

ATARI_BLUE = (0x49, 0x92, 0xB9, 0xff)
ATARI_WHITE = (0xe0, 0xe0, 0xe0, 0xff)

def generateVideoText(text, font_name="arex", frame_per_character=5, preframes=0, postframes=50):
    console = CONSOLE()
    counter = COUNTER()
    font = FONT(font)

    if preframes != 0:
        sheet = SHEET(bg=SHEET.TRANSPARENT, fg=ATARI_WHITE, console=console, font=font)
        sheet.save("./in/test_%04d.png"%counter.get(), preframes)

    for car in text:
        sheet = SHEET(bg=SHEET.TRANSPARENT, fg=ATARI_WHITE, console = console)
        sheet.initConsole(font=font)
        sheet.write(car)
        sheet.drawText()
        for x in range(5):
            sheet.save("./in/test_%04d.png"%counter.get())
    
    if postframes != 0:
        sheet = SHEET(bg=SHEET.TRANSPARENT, fg=ATARI_WHITE, console=console, font=font)
        sheet.save("./in/test_%04d.png"%counter.get(), postframes)
        
    #~ picToVideo("./in/test_%04d.png", "./out/text.mp4")

if __name__ == "__main__":

    console = CONSOLE()
    counter = COUNTER()
    font = FONT("arex")

    for car in "Pfeuh proundly presents\n\nFUSEE INTERPLANETAIRE":
        sheet = SHEET(bg=SHEET.TRANSPARENT, fg=ATARI_WHITE, console = console)
        sheet.initConsole(font=font)
        sheet.write(car)
        sheet.drawText()
        for x in range(5):
            sheet.save("./in/test_%04d.png"%counter.get())
    
    picToVideo("./in/test_%04d.png", "./out/text.mp4")
    
    
    
    
    