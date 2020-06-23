#!/usr/bin/python
# -*- coding: utf-8 -*-

from PILdrawer import *
from random import randrange

def createRandomFadeout(cols=8, rows=8):
    if DEBUG:
        sys.stdout.write("creating  random fade out video mask %i columns %i rows\n"%(cols, NB_ROWS))
    frm_name = "randomFadeOut"
    video_name = frm_name
    
    sheet = SHEET(bg=SHEET.BLACK)
    sheet_counter = COUNTER()
    width = sheet.getWidth() / cols
    height = sheet.getHeight() / rows

    sheet.save(INPUT_DIR + frm_name + "_%04d"%sheet_counter.get() + FRM_EXT)
    
    busytab = [False] * cols * rows
    for index in range (cols * rows):
        while 1:
            rnd_idx = randrange(cols * rows)
            if not busytab[rnd_idx]:
                col_num = rnd_idx % cols
                row_num = rnd_idx / cols
                busytab[rnd_idx] = True
                break
        x = col_num * width 
        y = row_num * height 
        sheet.drawRectangle(x, y, x + width, y + height, SHEET.WHITE)
        sheet.save(INPUT_DIR + frm_name + "_%04d"%sheet_counter.get() + FRM_EXT)
    
    picToVideo(INPUT_DIR + frm_name + "_%04d" + FRM_EXT, OUTPUT_DIR + video_name + VIDEO_EXT)

def create4_3to16_9mask():
    if DEBUG:
        sys.stdout.write("creating 4:3 to 16:9 mask picture\n")
    frm_name = OUTPUT_DIR + "4_3to16_9mask" + FRM_EXT
    sheet = SHEET(bg=SHEET.BLACK)

    window_width = (sheet.getWidth() * 3) / 4
    colmin = ((sheet.getWidth() - window_width) / 2)
    colmax = sheet.getWidth() - ((sheet.getWidth() - window_width) / 2)

    sheet.drawRectangle(colmin, 0, colmax -1, sheet.getHeight(), SHEET.TRANSPARENT)
    sheet.save(frm_name)

def createBinocularMask():
    if DEBUG:
        sys.stdout.write("creating  binocular mask picture\n")
    frm_name = OUTPUT_DIR + "binocular" + FRM_EXT
    
    sheet = SHEET(bg=SHEET.BLACK)
    sheet.setOrigin(sheet.getWidth() / 2, sheet.getHeight() / 2)
    d = (sheet.getHeight() * 5) / 6
    sheet.putDisc(-d/3, 0, d, SHEET.TRANSPARENT)
    sheet.putDisc( d/3, 0, d, SHEET.TRANSPARENT)

    sheet.save(frm_name)
    
def createNikonViewerMask():
    if DEBUG:
        sys.stdout.write("creating Nikon viewer mask picture\n")
    frm_name = OUTPUT_DIR + "nikonViewerMask" + FRM_EXT
    
    sheet = SHEET(bg=SHEET.BLACK)
    sheet.setOrigin(sheet.getWidth() / 2, sheet.getHeight() / 2)
    h = (sheet.getHeight() * 9) / 10
    w = (h * 4) / 3
    sheet.putRectangle(0, 0, w, h, SHEET.TRANSPARENT)
    sheet.putRectangle(w/2, 0, w/10, sheet.getHeight()/4, SHEET.BLACK)
    x = (-w*5)/8
    y = h/6
    d = w/3
    sheet.putDisc(x, y, d, SHEET.BLACK)
    sheet.putBitmap(x + w /12, y, Image.open("./ressource/nikonSpeed.png"), SHEET.WHITE)
    
    for d in (w/2, w/3, w/6):
        sheet.putCircle(0, 0, d, SHEET.BLACK)
        sheet.putCircle(0, 0, d-2, SHEET.BLACK)
        sheet.putCircle(0, 0, d-4, SHEET.BLACK)
        sheet.putCircle(0, 0, d+2, SHEET.BLACK)
        sheet.putCircle(0, 0, d+4, SHEET.BLACK)
        sheet.putDisc((w*11)/20, 0, h/40, SHEET.RED)
    sheet.putRectangle(0, 0, w/6, 2, SHEET.BLACK)
    sheet.putBitmap(w/2, 0, Image.open("./ressource/nikonZero.png"), SHEET.WHITE)
    sheet.putBitmap(w/2, -h/12, Image.open("./ressource/nikonPlus.png"), SHEET.WHITE)
    sheet.putBitmap(w/2, +h/12, Image.open("./ressource/nikonMinus.png"), SHEET.WHITE)

    sheet.setOrigin(0, 0)
    sheet.putBitmap(sheet.getWidth() / 2, 28, Image.open("./ressource/nikonAperture.png"), SHEET.WHITE)
    
    sheet.save(frm_name)
    sheet.show()

if __name__ == "__main__":
    
    createRandomFadeout()
    create4_3to16_9mask()
    createBinocularMask()
    createNikonViewerMask()

sys.exit(0)

