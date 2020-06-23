#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

global CANVAS
global X_OFFSET
global X_OFFSET
global DIA_FONT
global DEBUG

if sys.version_info[0] < 3:
    # python 2 or less
    import Tkinter as gui
    import tkMessageBox as gui_mb
    import tkSimpleDialog as gui_sd
    import tkFileDialog as gui_fd
    import tkFont as gui_font
    USING_PYTHON2 = True
else:
    # python 3 or more
    import tkinter as gui
    from tkinter import messagebox as gui_mb
    from tkinter import simpledialog as gui_sd
    from tkinter import filedialog as gui_fd
    from tkinter import font as gui_font
    USING_PYTHON2 = False

DEBUG = "-debug" in sys.argv
if DEBUG:
        sys.stdout.write("%s\n"%str(sys.version_info))
        sys.stdout.write("debug mode active\n")

def drawRectangle(x, y, w, h, color):
    if DEBUG:
        sys.stdout.write("rectangle x=%i, y=%i, w=%i, h=%i, color=%s\n"%(x, y, w, h, color))
    id = CANVAS.create_rectangle(X_OFFSET+x-w/2, Y_OFFSET+y-h/2, X_OFFSET+x+w/2, Y_OFFSET+y+h/2, fill=color)    
    return id

def drawText(x, y, text, color, font, **kwds):
    if DEBUG:
        sys.stdout.write("text x=%i, y=%i, text=\"\"%s, color=%s, font=%s, kwds=%s\n"%(x, y, text, color, font, str(kwds)))
    id = CANVAS.create_text(X_OFFSET+x, Y_OFFSET+y, fill=color, font=font, text=text, **kwds)    
    return id

def drawCircle(x, y, d, color, **kwds):
    r = d / 2
    if DEBUG:
        sys.stdout.write("text x=%i, y=%i, d=%u, color=%s, kwds=%s\n"%(x, y, d, color, str(kwds)))
    id = CANVAS.create_oval(X_OFFSET+x-r, Y_OFFSET+y-r, X_OFFSET+x+r, Y_OFFSET+y+r, fill=color, **kwds)   
    return id

def quitProperly(event):
    win.quit()

if __name__ == "__main__":

    #***************************************
    #*** VINTAGE NIKON VIEWER SIMULATION ***
    #***************************************

    win = gui.Tk()
    win.geometry("+0+0")
    DIA_FONT = gui_font.Font(size=32, weight='bold')
    win.title("Nikon viewer")
    win.bind("<Escape>", quitProperly)
    
    WIDTH = 1440
    HEIGHT = (WIDTH * 9) / 16
    height = (HEIGHT * 7) / 8
    width = (height * 4) / 3

    CANVAS = gui.Canvas(win, width=WIDTH, height=HEIGHT)
    CANVAS.grid()
    X_OFFSET = WIDTH / 2
    Y_OFFSET = HEIGHT / 2

    drawRectangle(0, 0, WIDTH, HEIGHT, "black")
    #~ Y_OFFSET += HEIGHT / 20
    drawRectangle(0, 0, width, height, "white")
    drawText(0, -(HEIGHT * 46) / 100, "5.6", "white", DIA_FONT)
    cd = (height*8)/20
    cx = (-(width)*60)/100
    cy = (height*10)/100
    drawCircle(cx, cy, cd, "black")
    drawText(cx, cy, "  250", "white", DIA_FONT, anchor="w")
    drawRectangle(width/2, 0, width/10, height/3, "black")
    drawText(width/2, 0, "0", "white", DIA_FONT)
    drawText(width/2, -height / 9, "+", "white", DIA_FONT)
    drawText(width/2, height / 9, "-", "white", DIA_FONT)
    drawCircle(width/2 + width/20, 0, height/25, "red")
    drawCircle(0, 0, height/6, "", outline="black", width=3)
    drawCircle(0, 0, height/2, "", outline="black", width=3)
    drawCircle(0, 0, height/3, "", outline="black", width=3)    
    drawRectangle(0, 0, height/6, 3, "black")
    win.mainloop()
