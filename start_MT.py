#!/usr/bin/env python
#
# This takes in the information from the event.info file and 
# writes event.info2 and the .txt file for the GMT plot 
# This should be run from the event folder
#
#
############################################

import sys
import time
import os
import string

from datetime import datetime

evdir = os.getcwd()
infofile = "event.info"
f = open(evdir + '/' + infofile, 'r')
# example: 2009-12-17 	 01:37:51  +36.4870  -9.9940 	  31  6.0
t1 = f.read()
t2 = string.split(t1)
f.close()



date=t2[0]
yr=date.split("-")[0]
#yr=date[0:4]
mo=date.split("-")[1]
#mo=date[5:7]
day=date.split("-")[2]
#day=date[8:10]
time=t2[1];
hr=time.split(":")[0]
#hr=time[0:2]
mn=time.split(":")[1]
#mn=time[3:5]
sec=time.split(":")[2]
#sec=time[6:8]
lat=t2[2];
lon=t2[3];
dep=t2[4];
ML=t2[5];

#print t1
#print "yr=",yr,"mo=",mo,"day=",day," HH=",hr,"mn=",mn,"sec=",sec

# write event.info2 file
eventinfo2 = infofile + "2"
with open(eventinfo2,'w') as f:
	f.write(yr + ' '+ mo + ' '+ day + ' '+ hr + ' '+ mn + ' '+sec + ' '+lat + ' '+lon + ' '+dep + ' '+ ML +' \n')

# write the gmttitle.txt
gmttitlefile = "gmttitle.txt"
with open(gmttitlefile,'w') as f:
	f.write( yr + '-'+ mo + '-'+ day + ' '+ hr + mn + sec + ' ML='+ ML + ' \n')
	

exit(1)


fname = '1-preparefolders.bash'
f=open(fname, 'w')

f.write('#!/bin/bash \n\n')

f.write('# create event.info2 \n')
f.write('echo '+ yr + ' '+ mo + ' '+ day + ' '+ hr + ' '+ mn + ' '+sec + ' '+lat + ' '+lon + ' '+dep + ' '+ ML +' > event.info2 \n\n')

f.write('# create gmttitle.txt \n')
f.write('echo '+ yr + '-'+ mo + '-'+ day + ' '+ hr + mn + sec + ' ML='+ ML +' > gmttitle.txt \n\n')

f.write('# copy scripts \n')
f.write('cp /Users/susana/_kiwi-runs/codes-n-scripts/inversionscripts2copy/* . \n\n')
 
f.write('# create data directory \n')
f.write('mkdir data-orig \n\n')
 
f.write('# create inversion directory \n')
f.write('mkdir inversion \n\n')
 
f.write('# create output directory \n')
f.write('mkdir output \n\n')
 
f.write('# populate inversion folder \n')
f.write('cp /Users/susana/_kiwi-runs/codes-n-scripts/rapidinv-copy/* inversion/. \n\n')

f.write('# echo message to copy files \n')
f.write('echo ================================================ \n')
f.write('echo ================================================ \n')
f.write('echo now copy data files in sac format into data-orig \n')
f.write('echo ================================================ \n')
f.write('echo ================================================ \n')

f.close()
