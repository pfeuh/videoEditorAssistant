#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---*********************************---
# ---*** Scrolled Text Atari Style ***---
# ---*********************************---

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

def generateScroll(text, font_name="ascii8", nb_pix=1, bg=ATARI_BLUE, fg=ATARI_WHITE, border=False, sound=False):
    vname = "./out/text.mp4"
    console = CONSOLE()
    pattern = "./in/OSVT_%04d.png"
    fname_gen = FNAME_GEN(pattern)
    font = FONT(font_name)
    size = len(text) * frame_per_character + preframes + postframes
    sys.stdout.write("Starting to generate %s size:%d frames\n"%(vname, size))
    clicks = []
    
    if preframes != 0:
        for cnt in range(preframes):
            sheet = SHEET(bg=bg, fg=fg, console=console)
            sheet.initConsole(font=font, border=border)
            createImage(sheet, fname_gen, preframes)

    for car in text:
        clicks.append(fname_gen.getCurrentIndex())
        console.write(car)
        for cnt in range(frame_per_character):
            sheet = SHEET(bg=bg, fg=fg, console=console)
            sheet.initConsole(font=font, border=border)
            createImage(sheet, fname_gen, frame_per_character)
    
    if postframes != 0:
        for cnt in range(postframes):
            sheet = SHEET(bg=bg, fg=fg, console=console)
            sheet.initConsole(font=font, border=border)
            createImage(sheet, fname_gen, postframes)
            
        
    #~ picToVideo(name_gen.getPattern(), vname)
    return clicks

if __name__ == "__main__":

    deleteInputBuffer()
    text = """M'sieur Reflex (Pierre Faller)

Le modele
    Patrick Faller
    
Le photographe
    Marc Kolb



Extérieur 1983
Château de Pourtales

Des images et des sons
libres de droits
ont etes utilises


Arrangements voix
Paul Glaeser / Pierre Faller


Ceci etait un hommage à Richard Gotainer et au Nikon FM sur une idee et des rushes VHS de 1983.







C. 2020"""


    print generateScroll(text, font_name="ascii8", nb_pix=1)
    picToVideo("./in/OSVT_%04d.png", "./out/text.mp4")
