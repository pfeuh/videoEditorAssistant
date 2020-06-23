#!/usr/bin/python
# -*- coding: utf-8 -*-

CHAR_SPACE           = ' '
CHAR_LINE_FEED       = '\n'
CHAR_CARRIAGE_RETURN = '\r'
CHAR_TABULATION      = '\t'
CHAR_BACKSPACE       = '\b'

class CONSOLE():
    def __init__(self, cols=40, rows=25, tab=4, callback=None):
        self.__cols = cols
        self.__rows = rows
        self.__tab = tab
        self.clearScreen()
        self.setCallback(callback)

    def setCallback(self, callback):
        self.__callback = callback

    def getCols(self):
        return self.__cols
        
    def getRows(self):
        return self.__rows

    def read(self, position):
        return ord(self.__console[position])

    def clearScreen(self):
        self.__console = [CHAR_SPACE] * self.__cols * self.__rows
        self.__x = 0
        self.__y = 0

    def gotoXY(self, x, y):
        self.__x = x
        self.__y = y

    def getXY(self):
        return self.__x, self.__y

    def scroll(self):
        for linenum in range(self.__rows - 1):
            for x in range(self.__cols):
                self.__console[linenum * self.__cols + x] = self.__console[(linenum + 1) * self.__cols + x]
        for x in range(self.__cols):
            self.__console[(self.__rows -1 ) * self.__cols + x] = CHAR_SPACE
        self.__y = self.__rows - 1
    
    def forceChar(self, car, x=None, y=None):
        if x == None:x = self.__x
        if y == None:y = self.__y
        self.__console[x + y * self.__cols] = car
        
    def writeChar(self, car):
        position = self.__x + self.__y * self.__cols
        if car == CHAR_LINE_FEED:
            self.__x = 0
            self.__y += 1
            if self.__y >= self.__rows:
                self.scroll()
        elif car == CHAR_CARRIAGE_RETURN:
            self.__x = 0
        elif car == CHAR_TABULATION:
            nb_tabs = (self.__x / self.__tab)
            self.__x = nb_tabs * self.__tab
            if self.__x >= self.__cols:
                self.__x = 0
                self.__y += 1
            if self.__y >= self.__rows:
                self.scroll()
        elif car == CHAR_BACKSPACE:
            if position == 0:
                pass
            else:
                position -= 1
                self.forceChar(CHAR_SPACE, position % self.__cols, position / self.__cols)
                self.__x = position % self.__cols
                self.__y = position / self.__cols              
        else:
            self.__console[position] = car
            position += 1
            self.__x = position % self.__cols
            self.__y = position / self.__cols
            if self.__y >= self.__rows:
                self.scroll()
        if self.__callback:
            self.__callback()
        
    def write(self, text):
        for car in text:
            self.writeChar(car)
            
    def __str__(self):
        text = '-' * self.__cols + CHAR_LINE_FEED
        for position, car in enumerate(self.__console):
            text += car
            if (position % self.__cols) == (self.__cols - 1):
                text += CHAR_LINE_FEED
        text += '-' * self.__cols + CHAR_LINE_FEED
        return text
    
if __name__ == "__main__":
    
    console = CONSOLE()
    #~ console.write(open("./titrage.py", ("r")).read(-1)[:385])
    console.write("1234567890")
    print console.getXY()
    print console
    for x in range(5):
        console.write("\b")
        print console.getXY()
        print console
        
