#!/usr/bin/python
# -*- coding: utf-8 -*-

import wave
import os
import sys

FRAME_PER_SECOND = 25
SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2
NB_CHANNELS = 2
SAMPLE2FRAME = SAMPLE_RATE / FRAME_PER_SECOND

class SOUND(wave.Wave_read):
    def __init__(self, fname=None):
        if fname == None:
            fname = "./ressource/keyClick.wav"
        if not os.path.exists(fname):
            sys.stderr.write("file %s not found!\n"%fname)
            sys.exit(-1)
        wave.Wave_read.__init__(self, fname)
        if self.getnchannels() != 2:
            self.raiseError(fname)
        if self.getframerate() != SAMPLE_RATE:
            self.raiseError(fname)
        if self.getsampwidth() != 2:
            self.raiseError(fname)
        if self.getcomptype() != "NONE":
            self.raiseError(fname)
        
    def raiseError(self, filename):
        self.close()
        raise Exception("file \"%s\" should be mono, 16 bits resolution, 44100 samples/second and not compressed"%filename)

class OUT_WAVE(wave.Wave_write):
    def __init__(self, fname):
        wave.Wave_write.__init__(self, fname)
        self.setnchannels(NB_CHANNELS)
        self.setframerate(SAMPLE_RATE)
        self.setsampwidth(SAMPLE_WIDTH)

    def ww__writeSound(self, sound, position):
        blank = chr(0) + chr(0)
        while position > self.tell():
            self.writeframes(blank)
        sound.rewind()
        samples = sound.readframes(-1)
        self.writeframes(samples)
        
    def xx__writeSound(self, sound, position= None):
        sys.stdout.write("sample:%8d frame:%04d second:%04d head:%8d "%(position, position/SAMPLE2FRAME, position/SAMPLE2FRAME/FRAME_PER_SECOND, self.tell()))

        if position != None:
            if position > self.tell():
                silence = chr(0) * SAMPLE_WIDTH * NB_CHANNELS * (position - SAMPLE_WIDTH)
                sys.stdout.write("%02x %02x %02x %02x size:%08d\n"%(ord(silence[0]), ord(silence[0]), ord(silence[0]), ord(silence[0]), len(silence)))
                self.writeframes(silence)
            else:
                sys.stdout.write("position <= tell() %08d\n"%self.tell())
        else:
            sys.stdout.write("position != None\n")
            
        
        #~ blank = chr(0) + chr(0)
        #~ if position > self.tell():
            #~ self.writeframes(blank)
        sound.rewind()
        samples = sound.readframes(-1)
        self.writeframes(samples)
        
    def writeSound(self, sound, sample_num= None):
        sys.stdout.write("sample_num:%8d head:%8d\n"%(sample_num, self.tell()))

        if sample_num == None:
            pass
        elif sample_num == self.tell():
            pass
        elif sample_num <= self.tell():
            self.close()
            raise Exception("attempt to overwrite!")
        else:
            silence = chr(0) * SAMPLE_WIDTH * NB_CHANNELS
            silence *= sample_num - self.tell()
            self.writeframes(silence)
            
        sound.rewind()
        samples = sound.readframes(-1)
        self.writeframes(samples)
        
def generateKeyClick(outname=None, soundname=None, frm_nums=[0]):
    if outname == None:
        outname = "./out/test.wav"
    output = OUT_WAVE(outname)
    sound = SOUND(soundname)
    
    for frm_num in frm_nums:
        output.writeSound(sound, frm_num * SAMPLE2FRAME)
        
    sound.close()
    output.close()
        
if __name__ == "__main__":
    
    frm_nums = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275]
    generateKeyClick("./out/test.wav", "./ressource/keyClick.wav", frm_nums)
