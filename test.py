#!/usr/bin/python
# -*- coding: utf-8 -*-

from PILdrawer import *

def test_01():
    sheet = SHEET(width=800, height = 640)

    sheet.putDisc(0, 0, 100, SHEET.RED)
    sheet.setOrigin(sheet.getWidth()/2, sheet.getHeight()/2)
    sheet.putDisc(0, 0, 100, SHEET.GREEN)
    sheet.setOrigin(sheet.getWidth()-1, sheet.getHeight()-1)
    sheet.putDisc(0, 0, 100, SHEET.BLUE)

    sheet.save("./out/test.png")
    sheet.show()

if __name__ == "__main__":
    
    test_01()

    w = 40 * 8
    h = 25 *8
    for ratio in range(1, 11):
        print ratio, w, h, w* ratio, h* ratio
    
    

#~ sheet = SHEET(width=800, height = 640)

#~ sheet.putDisc(0, 0, 100, SHEET.RED)
#~ sheet.setOrigin(sheet.getWidth()/2, sheet.getHeight()/2)
#~ sheet.putDisc(0, 0, 100, SHEET.GREEN)
#~ sheet.setOrigin(sheet.getWidth()-1, sheet.getHeight()-1)
#~ sheet.putDisc(0, 0, 100, SHEET.BLUE)

#~ sheet.save("./out/test.png")
#~ sheet.show()

