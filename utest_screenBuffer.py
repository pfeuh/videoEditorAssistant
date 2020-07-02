#!/usr/bin/python
# -*- coding: utf-8 -*-

import screenBuffer as SB
import sys

def printLine(text):
    sys.stdout.write("<%s>\n"%text)

def printParagraph(text, cols):
    line_num = 0
    while 1:
        line = text[line_num * cols: (line_num + 1) * cols]
        if len(line):
            sys.stdout.write("<%s>\n"%line)
            line_num += 1
        else:
            break

text = "abc def ghi jkl"
line = SB.LINE(text)
ftext = line.getFormatedText()
assert len(ftext) == SB.SCREEN_COLS
assert ftext.startswith(text)

text = "abcdef ghijkl mnopqr stuvwx yz0123 456789"
line = SB.LINE(text)
ftext = line.getFormatedText()
print len(text), len(ftext)
printParagraph(ftext, SB.SCREEN_COLS)

text = "\t<>Ceci etait un hommage a Richard Gotainer et au Nikon FM sur une idee et des rushes VHS de 1983."
line = SB.LINE(text)
ftext = line.getFormatedText()
print len(text), len(ftext)
printParagraph(ftext, SB.SCREEN_COLS)

text = "<>\trushes VHS de 1983."
line = SB.LINE(text)
ftext = line.getFormatedText()
print len(text), len(ftext)
printParagraph(ftext, SB.SCREEN_COLS)

