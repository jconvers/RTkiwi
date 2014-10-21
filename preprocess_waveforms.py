#!/usr/bin/env python
#
# Modified by Jaime Convers from s-preproc.py by Susana Custodio
#
# reads data files and outputs lists of stations and components to be used
#
# usage: python preproc.py datain dataout f1 f2 dt2
# example: python preproc.py data-orig/ data-proc/ .01 2. .2
#
############################################

from obspy.core import read
from sys import exit
from math import floor

import sys
import os
import glob 
import string

def factors(n):
 result = []
 for i in range(2,n+1): # test all integers between 2 and n
  s = 0;
  while n/i == floor(n/float(i)): # is n/i an integer?
   n = n/float(i)
   s += 1
  if s > 0:
   for k in range(s):
    result.append(i) # i is a pf s times
   if n == 1:
    return result

import argparse
parser = argparse.ArgumentParser(description='reads data files and outputs lists of stations and components to be used')
parser.add_argument("-D",dest='datain',nargs=1,required=True,
		help="input directory with SAC files and RESP files ( e.g. -Ddata-orig/ ) WARNING: FILE MUST END IN '.SAC' ")
parser.add_argument("-O",dest='dataout',nargs=1,required=True,
		help="folder where displacement miniseed data will be stored. MUST BE CREATED BEFORE ( e.g. -Odata-proc/ )")
parser.add_argument("-f1",dest='f1',nargs=1,required=True,
		help="choose LOWER filtering frequency for deconvolution (e.g. -f1 0.01)")
parser.add_argument("-f2",dest='f2',nargs=1,required=True,
		help="choose UPPER filtering frequency for deconvolution (e.g. -f2 2.)")
parser.add_argument("-t",dest="dt2",nargs=1,required=True,
		help="dt for decimation (e.g. -t0.2)") 
args = parser.parse_args() # read options

datain = args.datain[0]
dataout = args.dataout[0]
f1 = args.f1[0]
f2 = args.f2[0] 
dt2 = args.dt2[0]
print "datain = ",datain
print 'dataout = ',dataout
print 'f1 = ',f1
print 'f2 = ',f2 
print 'dt2 = ',dt2 

#exit(1)
#
#datain = sys.argv[1]
#dataout = sys.argv[2]
#f1 = sys.argv[3]
#f2 = sys.argv[4]
#dt2= sys.argv[5]			# output dt

evdir = os.getcwd()

f = open(evdir + '/event.info', 'r')
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

#print "yr=",yr,"mo=",mo,"day=",day," HH=",hr,"mn=",mn,"sec=",sec

fname2 = dataout + 'run.macro'
fil2 = open(fname2, 'w')
fname3 = dataout + 'stations.dat.rapid'
fil3 = open(fname3, 'w')
j=1
stn = 'ZZZ'
stnl=['ZZZ']

print "Working in ALL '.SAC' files in "+datain+" \n"
for infile in glob.glob(datain + '*.SAC'):

   #print "current file is: " + infile

   st = read(infile)
   tr=st[0]
   
   if infile[len(infile)-4:len(infile)] == '.SAC':
   	tr.stats.channel = infile[len(infile)-7:len(infile)-4]
   id=tr.stats.station + tr.stats.channel[2]

#   print tr.stats.station
#   print stnl
#   print 'id is '+id

   if id not in stnl:
        stnl.append(id)
        
        fname = 't.'+ infile[10:len(infile)] + '.macro'
        fil2.write('macro ' + fname + ' \n')

        if tr.stats.station != stn: 
        	fil3.write(str(j) + ' '+ tr.stats.station +' ' + str(tr.stats.sac.stla) +' '+ str(tr.stats.sac.stlo) +' \n')
        	j=j+1
        stn = tr.stats.station
        
        ######### standard data processing
        f = open(dataout + fname, 'w')
        f.write('r ../'+ infile +' \n')
        f.write('chnhdr KCMPNM '+ tr.stats.channel +' \n')   
        f.write('rtr \n')
        f.write('taper \n')
        f.write('TRANS FROM EVALRESP TO NONE \n')
        f.write('mul 1e-9 \n')
        f.write('lh depmin depmax \n')
        f.write('bp c '+ f1 +' '+ f2 + ' \n')
        
        dt1 = tr.stats.delta
        dt2 = .2
        fact = int(dt2/dt1)
        fact2 = factors(fact)
     #   print dt1, dt2
     #   print fact, fact2
        for i in range(len(fact2)):
        	f.write('decimate '+ str(fact2[i]) + ' \n')
#        f.write('cutim O-30 O+240 \n')			# is not working! :-(
#        f.write('p \n')
#        f.write('pause \n')
     
        fnout = 'DISPL.' + stn + '.BH' + tr.stats.channel[2] + '.sac'
        f.write('w '+ fnout +' \n')

#        f.write('cut 50 E \n')
#        f.write('r '+ fnout +' \n')
#        f.write('w '+ fnout +' \n')
#        f.write('p \n')
        f.close()
# 
#         ######### RT data processing
#			read R and N
# 			then rotate
#			http://eqseis.geosc.psu.edu/~cammon/HTML/RftnDocs/prep01.html
#			http://www.iris.edu/software/sac/commands/rotate.html
#         f.write('chnhdr EVLA '+ lat +' \n')   
#         f.write('chnhdr EVLO '+ lon +' \n')   
#         f.write('wh \n')   
#         f.write('lh gcarc baz \n')   
# 		
#         f.write('sync \n')   
# 
#         f.write('rotate to \n')   
#         fnout = '../data-proc-RT/DISPL.' + stn + '.BH' + tr.stats.channel[2] + '.sac'
#         f.write('w '+ fnout +' \n')
#         f.close()
      
fil2.write('quit \n')
fil2.close()
fil3.close()
exit(0)
