#-*- coding: utf-8 -*-

# MP4 TO MP3 CONVERSION SCRIPT
# script to convert mp4 video files to mp3 audio
# useful for turning video from sites such as www.ted.com into audio files useable
# on any old mp3 player.
#
# usage: python mp4tomp3.py [input directory [output directory]]
# input directory (optional)  - set directory containing mp4 files to convert (defaults to current folder)
# output directory (optional) - set directory to export mp3 files to (defaults to input)
#
# NOTE: you will need python 2, mplayer and lame for this script to work
# sudo apt-get install lame
# sudo apt-get install mplayer
# sudo apt-get install python2.7


#from subprocess import call     # for calling mplayer and lame
import os                       # help with file handling
import sys
import imageio

try:
    from moviepy.editor import *
except imageio.plugins.ffmpeg.NeedDownloadError:
    imageio.plugins.ffmpeg.download()
    from moviepy.editor import *

def check_file_exists(directory, filename, extension):
    path = directory + "/" + filename + extension
    return os.path.isfile(path)


def extract(infile, outfile):
    # print "-- convert from %s" % (infile)
    # print "-- convert to %s" % (outfile)

    try:
        videoclip = VideoFileClip(infile)
        audioclip = videoclip.audio
        audioclip.write_audiofile(outfile)
    finally:
        return True

    # try:
    #     call(["mplayer", "-novideo", "-nocorrect-pts", "-ao", "pcm:waveheader", infile.encode(sys.getfilesystemencoding())])
    #     call(["lame", "-h", "-b", "192", "audiodump.wav", outfile.encode(sys.getfilesystemencoding())])
    #     os.remove("audiodump.wav")
    # finally:
    #     return True


