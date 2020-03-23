import os
import sys
from os import listdir
from os.path import isfile, join
#import re
import argparse
import time
from time import gmtime, strftime
import csv
import shutil
import datetime
import pathlib

class MGcsvutils:
    MGcsv_DIRINFO, MGcsv_FILEINFO, MGcsv_DIRDIFFINFO, MGcsv_STATS = [6, 11, 7, 0]
    def __init__(self, mysrcpath=None):
        self.mgcsvdict= dict([('ItemNo',None),
                ('Dirstr',None),
                ('Filestr',None),
                ('Date',None),
                ('Size',0),
                ('DirNode',None),
                ('DupStr',None)])

        self.csvfileR = None
        self.filepath = None
        self.filerecords = {}
        self.dirrecords = {}
        self.dirmatches= {}
        self.dirstats = {}
        self.extstats = {}
        self.mylist = None
        if mysrcpath == None:
            return
        self.filepath = mysrcpath
        self.MGC_opencsv(self.filepath) # the option to open-on-instantiation for one-shot csv processing. or instantiate-then-open-open-open
        return
    def MGC_lookupstring(self, str, nitems=100, controls=['files','dirs','matches']):
        lookuptargets= {'files':self.filerecords, 'dirs':self.dirrecords, 'matches':self.dirmatches}
        returnstrings = []
        teststr = str.lower()
        for j in controls:
            for i in lookuptargets[j]:
                if teststr in i.lower():
                    returnstrings.append(i)
                    #print(returnstrings)
                if len(returnstrings) > nitems:
                    return returnstrings
        return returnstrings

    def MGC_opencsv(self, srcpath):
        self.filepath = srcpath
        try:
                with open(srcpath,'r') as f: #not rb  aka binary
                    reader = csv.reader(f)
                    if not self.mylist:
                        self.mylist = list(reader)
                    else:
                        self.mylist.extend(list(reader))
                return
                #self.csvfileR = open(srcpath, newline='')
                #your_list = map(tuple, reader)
                #self.csvlist = csv.DictReader( self.csvfileR, self.mgcsvdict, delimiter=',', quotechar='\"')

        except:
                self.errorcode = 2 #file failed to open
                print("*,*,*,*,csv_open_failed_%s", srcpath )
                self.csvfileR = None
                self.filepath = None
                return False

    # get next line from csv iterator.
    def MGC_getcsvline(self):
        if not self.filepath:
            return False
        #get the next CSV row from file  
        try:
                p = next(self.mylist) #csv row item path file date size
                print(p)
        except Exception as inst:
                self.errorcode = 5 #csv iterator failed or ended
                self.csverrors += 1
                #print(inst.args)
                #x,y = inst.args Nope, it's one list
                x = inst.args
                #by experimenting, I learned x is None for EOF. it is the unhashable when reading a mismatched csv dict row
                if not x:
                        return False
                print ('0,0,0,%d,"CSVERR:%s"'%(self.csverrors,x))
                print ('CSVERR: row', self.currentrow)
                if (x[0].find('unhashable') == -1): #some other error?
                        return False
        return True # if it's a bad CSV 5 entry line, just ignore

    #while csvinstance.MGC_getcsvline() :
    #    pass
    def MGC_loadcsvdata(self, bNoStructure):
            recordlist = []
            if not self.mylist:
                return
            for i in self.mylist: #and process the csv lines
                if bNoStructure:
                    recordlist.append(i)
                    continue

                if len(i) == self.MGcsv_DIRINFO:
                    try:
                        #print(k,len(i),i)
                        self.dirrecords[i[1]] = i
                        pass
                    except:
                        print("exception", len(i), i[0])
                        pass
                    continue
                if len(i) == self.MGcsv_DIRDIFFINFO:
                    try:
                        if  i[0] == '001**':
                            if (i[3]==i[4]) and (not i[3] == '0'):
                                #print('Comm==Match',len(i),i)
                                self.dirmatches[i[1]] = i
                            else:
                                print(len(i),i)
                        elif i[0] == '0:0':
                           if 'directories' in i[1]:
                               self.dirstats[i[1]] = i
                           elif 'extension' in i[1]:
                               self.extstats[i[1]] = i
                           else:
                               print('Stat 0:0 record not Ext or Dir!', i)
                            #csvinstance.dirrecords[i[1]] = i
                        else:
                            print("not 001*, not 0:0, but difflength matches DIR or STATS", len(i),i)
                        pass
                    except:
                        print("exception", len(i), i[0])
                        pass
                    continue
                if len(i) == self.MGcsv_FILEINFO :
                    # don't include the csv header line in our memory image of entries!
                    if i[0] == 'Path' and i[1] == 'size':
                        continue 
                    self.filerecords[i[0]] = i
                    continue

                print("OTHER RECORD",len(i),i)
            return recordlist

if __name__ == '__main__':
    k = 0 
    csvinstance = csvinstance = MGcsvutils()
    infiles = ["e:\\mgfilecmpfiles-e01-2-2019-11-04-15-17-35.csv","e:\\mgfilecmpfiles-h03-2-2019-11-04-16-04-29.csv",]
    infilexx = ['e:\\wd3TBdrive\\mgfilecmpdirsf3-2-2019-08-12a.csv','e:\\wd3TBdrive\\mgfilecmpfilesf3-2-2019-08-12a.csv' ]
    #infiles = ['e:\\mgfilecmpdirsu3-2-2019-08-12a.csv','e:\\mgfilecmpfiles-h03-2-2019-11-04-16-04-29','e:\\mgfilecmpstatsu3-2-2019-08-12a.csv']
    for ix,j in enumerate(infiles):
        csvinstance.MGC_opencsv(j) #open another file
        #while csvinstance.MGC_getcsvline() :
        #    pass
        csvinstance.MGC_loadcsvdata()
        #mgfilecmpfilesf3-2-2019-08-12a
        input('hit enter. Completed load of %d:<%s>'%(ix,j))
    k += 1
    instr = 'no'
    while not instr == 'quit':
        matchinp = input('Enter targets or just enter')
        if len(matchinp) ==0:
            matchlist = ['dirs','files','matches']
        else:
            matchlist = matchinp.split(",")
        instr = input('Enter search str or quit')
        if instr in csvinstance.filerecords:
            print(csvinstance.filerecords[instr])
            continue
        #if instr in csvinstance.dirmatches:
        #    print(csvinstance.dirmatches[instr])
        #    #continue
        if instr in csvinstance.dirrecords:
            print(csvinstance.dirrecords[instr])
            continue
        if instr == 'matches':
            for i in csvinstance.dirrecords:
                print(i[0],i)
        #matchstrs = csvinstance.MGC_lookupstring(instr,120,matchlist)
        print('--FILES--> %s',instr)
        matchstrs = csvinstance.MGC_lookupstring(instr,120,['files'])
        if len(matchstrs):
            for k in matchstrs:
                print('files: %d'%len(k),k,csvinstance.filerecords[k])
        print('--DIRS--> %s',instr)
        matchstrs = csvinstance.MGC_lookupstring(instr,120,['dirs'])
        if len(matchstrs):
            for k in matchstrs:
                print('dirs: %d'%len(k),k,csvinstance.dirrecords[k])
        print('--MATCHES--> %s',instr)
        matchstrs = csvinstance.MGC_lookupstring(instr,120,['matches'])
        if len(matchstrs):
            for k in matchstrs:
                print('matches: %d'%len(k),k,csvinstance.dirmatches[k])
