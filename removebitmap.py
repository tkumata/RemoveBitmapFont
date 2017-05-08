#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Usage: python %s step{1|3} font-file-name prefix
#
# argv[1] ... font file name
# argv[2] ... temporary file prefix
#
# eg. python pyFFctrl.py step1 meiryo.ttc rbf-tmp-ttf
#

import sys
import glob
import fontforge
import tempfile
import os
import shutil
import subprocess

fontforge.setPrefs('CoverageFormatsAllowed', 1)

# TTF flags
flags = ('opentype', 'round')

# – antialias: Hints are not applied, use grayscale smoothing.
# – gridfit: Use hinting in Windows.
# – gridfit+smoothing: ClearType GridFitting.
# – symmetric-smoothing: ClearType Antialiasing.
def gasp():
    return (
        (65535, ('antialias', 'symmetric-smoothing', 'gridfit+smoothing')),
    )

def main(argvs):
    argc = len(argvs)
    
    if argc != 3:
        print "==> Usage: python %s font-file-name prefix" % argvs[0]
        print "==>    eg. python %s msgothic.ttc rbf-tmp-ttf" % argvs[0]
        quit()
    
    fontFSName = argvs[1]
    tmpPrefix = argvs[2]
    
    homeDir = os.path.expanduser("~")
    tempDir = tempfile.mkdtemp()
    print tempDir
    
    # font file exist
    if os.path.exists(homeDir + "/Downloads/fonts/" + fontFSName):
        print "==> Start breaking TTC."
        
        # Get packed family names
        familyNames = fontforge.fontsInFile(homeDir + "/Downloads/fonts/" + fontFSName)
        
        # Breake TTC
        i = 0
        for familyName in familyNames:
            # openName: "msgothic.ttc(MS UI Gothic)"
            print "==> %s" % familyName
            openName = "%s(%s)" % (homeDir + "/Downloads/fonts/" + fontFSName, familyName)
            
            # tmp file name: rbf-tmp-ttf0a.ttf and rbf-tmp-ttf1a.ttf and so on.
            tmpTTF = "%s%da.ttf" % (tmpPrefix, i)
            
            # Open font
            font = fontforge.open(openName)
            
            # Edit font
            font.encoding = 'UnicodeFull'
            font.gasp = gasp()
            font.gasp_version = 1
            font.os2_vendor = "maud"
            font.os2_version = 1
            
            # Generate font
            font.generate(tempDir + "/" + tmpTTF, flags=flags)
            font.close()
            #subprocess.call('bash os2version_reviser.sh ' + tempDir + "/" + tmpTTF, shell=True)
            i += 1
        print "==> Finish breaking TTC."
        
        print "==> Starting generate TTC."
        newTTCname = 'new_' + fontFSName
        files = glob.glob(tempDir + "/" + tmpPrefix + '[0-9]a.ttf')
        fontX = []
        
        for file in files:
            fontOpen = fontforge.open(file)
            fontX.append(fontOpen)
            
        # Generate TTC.
        if len(fontX) > 1:
            f = fontX[0]
            fontX.pop(0)
            f.generateTtc(tempDir + "/" + newTTCname, (fontX), ttcflags=("merge",), layer=1)
            
            if os.path.exists(tempDir + "/" + newTTCname):
                os.rename(tempDir + "/" + newTTCname, homeDir + "/Downloads/fonts/" + newTTCname)
            else:
                print "==> new TTC not found."
                quit()
        else:
            print "==> File not found or not enough fonts."
            quit()
            
        for openedFont in fontX:
            openedFont.close()
            
        f.close()
        print "==> Generated TTC."
        
        shutil.rmtree(tempDir)
        
    # file not found
    else:
        print "==> File not found."
        
if __name__ == '__main__':
    main(sys.argv)
