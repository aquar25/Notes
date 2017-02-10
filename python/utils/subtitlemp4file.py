#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from os import listdir
from os.path import isfile, join
import subprocess

base_path = '.'

def add_subtitle():
    files = [onefile for onefile in listdir(base_path) if isfile(join(base_path, onefile))]
    video_file = ''
    subtitile_file = ''
    for onefile in files:
        if onefile.endswith('.mp4'):
            video_file = join(base_path, onefile)
        elif onefile.endswith('.srt'):
            subtitile_file = join(base_path, onefile)

    if subtitile_file != '':
        output_file = subtitile_file.replace('.srt', '.mp4')
        comm = "ffmpeg -i '{0}' -i '{1}' -c copy -c:s mov_text '{2}'".format(
            video_file, subtitile_file, output_file)
        print(comm)
        subprocess.call(comm, shell=True)

if __name__ == '__main__':
    add_subtitle()