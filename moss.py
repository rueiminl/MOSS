#! /usr/bin/python
import glob
import sys
import os
from subprocess import call
def main():
    """
    motivation: check 18756 java coding assignments plagiarism

    preparation:
    1. put all zip files in the directory
        i.e.
         andrewid1_18756_project1.zip
         andrewid2_18756_project1.zip
         ...
    2. put the original handout zip file in the same directory, and rename to
        andrewid_18756_project1.zip
    3. put moss.py (this file) and moss.pl in the same directory

    note: moss.pl could be retrieved from https://theory.stanford.edu/~aiken/moss/
        by emailing to moss@moss.stanford.edu with two line body
            registeruser
            mail your@email

    script flow:
    for each zip file:
        unzip it into a temp directory
        retrieve the andrewid from filename
        mkdir andrewid
        copy java source code into andrewid

    Note: no idea why call perl would fail. Please copy the output and paste as a new command manually.
    """
    assignments = glob.glob("*.zip")
    i = 0
    andrewids = []
    for assignment in assignments:
        andrewid = assignment.split('_')[0]
        if andrewid != 'andrewid':
            andrewids.append(andrewid)
        i += 1
        temp = 'temp' + '%02d' % i
        call(['rm', '-rf', andrewid])
        call(['mkdir', andrewid])
        call(['mkdir', temp])
        call(['unzip', assignment, '-d', temp])
        for path, subdirs, files in os.walk(temp):
            for name in files:
                filename = os.path.join(path, name)
                if filename.endswith('.java') and not '__MACOSX' in filename:
                    tokens = filename.split('/')
                    call(['cp', filename, andrewid + '/' + tokens[-2] + '.' + tokens[-1]])
        call(['rm', '-rf', temp])
    cmd = 'perl moss.pl -l java -d -b andrewid/*.java '
    for d in andrewids:
        cmd += d + '/*.java '
    print cmd
if __name__ == '__main__':
    main()
