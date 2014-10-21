#!/usr/bin/env python
#
# This script  writes the input file for inversion "rapid.inp"
# First Creates the propper output subfolder inside the main output directory
#
# Modified from Original python script  by Susana Custodio
#
# usage: python write_rapidinv_inp.py 
# example: python write_rapidinv_inp.py 2 1 SW_FULLMT True
# example: python write_rapidinv_inp.py 0 0
#
############################################

import sys
import time
import os
import string
from datetime import datetime
import shutil

infofile = "event.info"
with open("../"+infofile,'r') as f:
	t1 = f.read() 
	t2 = string.split(t1)
	date = t2[0]
	yr,mo,day = t2[0].split("-")[0:3] 
	hr,mn,sec = t2[1].split(":")[0:3] 
	msec='000'
	lat,lon,dep,mL = t2[2:7]

#print "year=",yr, "month=",mo, "day=",day  
#print "mm="+mn,"hr="+hr,"sec="+sec  
#print "lat="+lat,"lon="+lon,"dep="+dep,"ml=",ml  
m0=10.**(3./2.*(float(mL)-.2)+16.1)*1.e-7 # converting to Mo
print 'Mo = ' + str(m0) +', ML='+mL + ', adjML='+ str(float(mL)-.2)

#exit(1)

#f = open('../event.info2', 'r')

#t1 = f.read()
#t2 = string.split(t1)
#yr=t2[0]; mo=t2[1]; day=t2[2]; hr=t2[3]; mn=t2[4]; sec=t2[5]; msec='000';
#lat= t2[6]; lon=t2[7]; dep=t2[8]; mL=t2[9];
#f.close()
#m0=10.**(3./2.*(float(mL)-.2)+16.1)*1.e-7
#print 'M0 = ' + str(m0) +', ML='+mL + ', adjML='+ str(float(mL)-.2)

if float(mL)<=4.2:
	BP_F1 = '.0475'
	BP_F2 = '.05'
elif float(mL)<=5.5:
	BP_F1 = '.0225'
	BP_F2 = '.025'
else:
	BP_F1 = '.01'
	BP_F2 = '.015'
	
ninp = sys.argv[1]
nvar = int(sys.argv[2])
OUTPUTMAINDIR="output"  # this folder is created previously. 
                        #if running this script by itself make sure 'eventname'/output already exists. 
OUTPUTDEFAULTNAME="output" 

# creating folder:
if os.path.isdir("../"+OUTPUTMAINDIR+"/"+OUTPUTDEFAULTNAME+ninp):
        print "will remove previous '"+OUTPUTDEFAULTNAME+ninp+"' folder to make new one"
        shutil.rmtree("../"+OUTPUTMAINDIR+"/"+OUTPUTDEFAULTNAME+ninp)
elif os.path.isfile("../"+OUTPUTMAINDIR+"/"+OUTPUTDEFAULTNAME+ninp):
        shutil.move("../"+OUTPUTMAINDIR+"/"+OUTPUTDEFAULTNAME+ninp, "../"+OUTPUTMAINDIR+"/"+OUTPUTDEFAULTNAME+ninp+".old")
print "Creating folder "+"../"+OUTPUTMAINDIR+"/"+OUTPUTDEFAULTNAME+ninp
os.mkdir("../"+OUTPUTMAINDIR+"/"+OUTPUTDEFAULTNAME+ninp)


thisfilename=os.path.basename(__file__) # findout the name of this script (to keep track in case script name changes)
GFDABABASE='/Users/jaimeconvers/geophysics/MTinversions/MTrapidkiwi/lib/GREEN/mod1-stich'
STATIONSFILE='stations.dat.rapid'
DATAFOLDER='data-proc'
#exit(0)

var=[]
val=[]
if nvar > 0:
	for i in range(nvar):
		print i, sys.argv[i*2+3], sys.argv[i*2+4]
		var.append(str(sys.argv[i*2+3]))
		val.append(str(sys.argv[i*2+4]))

fname = 'rapidinv.inp.' + ninp
f = open(fname, 'w')

d=datetime.today()

f.write('# input file for inversion. Created by '+str(os.environ.get( "USER" ))+' on '+ d.strftime("%A, %d. %B %Y %I:%M%p") +'\n')
f.write('# \n')
f.write('# '+fname+' file automatically created using '+thisfilename+' \n')
f.write('# \n')
if nvar == 0:
	f.write('# This is the default cofiguration \n')
if nvar > 0:
	for i in range(nvar):
		f.write('# '+ var[i] + ' \t ' + val[i] +'\n')
f.write('# \n')
f.write('######################################################### \n\n')

os.chdir('..')
evdir = os.getcwd()
os.chdir('inversion')

f.write('# Ouput subdirectory \n')
f.write('INVERSION_DIR \t'+ evdir + '/output/output'+ ninp +'\n\n')

f.write('# Greens functions \n')
f.write('GFDB_STEP1		   '+GFDABABASE+' \n')
f.write('GFDB_STEP2		   '+GFDABABASE+' \n')
f.write('GFDB_STEP3		   '+GFDABABASE+' \n\n')
	

f.write('# Data \n')
f.write('DATA_DIR            '+evdir + '/'+DATAFOLDER+' \n')
f.write('DATA_FILE           PT'+ str(yr) + str(mo) + str(day) +'\n')
f.write('STAT_INP_FILE       '+STATIONSFILE+' \n')
f.write('EPIC_DIST_MIN       25 \n')
f.write('EPIC_DIST_MAX       400 \n')
f.write('DATA_FORMAT         mseed \n')
f.write('SW_DATA_SAMPLING    False \n')
f.write('SW_FILTERNOISY      False \n')
f.write('NOISE_WINDOW	     4mintot0 \n')
f.write('SCALING_FACTOR      1 \n\n')

f.write('# Channels, components, weighting \n')
f.write('SW_APPLY_TAPER      True \n')
f.write('SW_WEIGHT_DIST      True \n')
f.write('COMP_2_USE          une \n\n')

f.write('# Source location and origin time \n')
f.write('YEAR                ' + str(yr) + '\n')
f.write('MONTH               ' + str(mo) + '\n')
f.write('DAY                 ' + str(day) + '\n')
f.write('HOUR                ' + str(hr) + '\n')
f.write('MIN                 ' + str(mn) + '\n')
f.write('SEC                 ' + str(sec) + '\n')
f.write('MSEC                ' + str(msec) + '\n')
f.write('LATITUDE_NORTH      ' + str(lat) + '\n')
f.write('LONGITUDE_EAST     ' + str(lon) + '\n\n')

f.write('# Moment Tensor Inversion \n')
f.write('SW_FULLMT           False \n')
f.write('MT_ISO              True \n')
f.write('MT_DIPOL            True \n')
f.write('MT_CLVD             True \n')
f.write('NUM_INV_STEPS       2 \n')
f.write('CONFIDENCE_INT      68 \n\n')

f.write('# Phases windowing, step 1 \n')
f.write('PHASES_2_USE_ST1    a \n')
f.write('WIN_START_P_ST1     0.25 \n')
f.write('WIN_TAPER_P_ST1     0.05 \n')
f.write('WIN_LENGTH_P_ST1    120 \n')
f.write('WIN_START_A_ST1     0.20 \n')
f.write('WIN_TAPER_A_ST1     0.175 \n')
f.write('WIN_LENGTH_A_ST1    180 \n\n')

f.write('# Inversion of point source parameters step 1 \n')
f.write('#SW_RAPIDSTEP1      FALSE \n')
f.write('DEPTH_1             5 \n')
f.write('DEPTH_2             45 \n')
f.write('DEPTH_STEP          10 \n')
f.write('STRIKE_1            0 \n')
f.write('STRIKE_2            180 \n')
f.write('STRIKE_STEP         15 \n')
f.write('DIP_1               0 \n')
f.write('DIP_2               90 \n')
f.write('DIP_STEP            15 \n')
f.write('RAKE_1              0 \n')
f.write('RAKE_2              90 \n')
f.write('RAKE_STEP           15 \n')
f.write('SCAL_MOM_1          '+str(m0)+' \n')
f.write('SCAL_MOM_2          '+str(m0)+' \n')
f.write('SCAL_MOM_STEP       '+str(m0)+' \n')
f.write('LOOPS_SDS_CONF      1 \n')
f.write('REDUCE_SDS_CONF     3 \n')
f.write('REDUCE_DEP_CONF     2 \n\n')

f.write('# Parameters for inversion step 1 \n')
f.write('EFFECTIVE_DT_ST1    0.2 \n')
f.write('BP_F1_STEP1         '+BP_F1+' \n')
f.write('BP_F2_STEP1         '+BP_F2+' \n')
f.write('BP_F3_STEP1         0.100 \n')
f.write('BP_F4_STEP1         0.110 \n')
f.write('BP_SHAPE_STEP1      trapezoid \n')
f.write('MISFIT_MET_STEP1    ampspec_l2norm \n') 
f.write('#INV_MODE_STEP1     invert_dmsdsok \n')
f.write('INV_MODE_STEP1      invert_dmsdst \n\n')

f.write('# Plot parameters for inversion step 1 \n')
f.write('MAX_STAT_2_PLOT     60 \n')
f.write('#DATA_PLOT_STEP1    seis \n')
f.write('DATA_PLOT_STEP1     amsp \n')
f.write('FILT_PLOT_STEP1     filtered \n')
f.write('START_PLOT_STEP1    0 \n')
f.write('LEN_PLOT_STEP1      300 \n')
f.write('TICK_PLOT_STEP1     60 \n')
f.write('AMPL_PLOT_STEP1     norm \n')
f.write('MISFIT_DEP_RANGE    10 \n')
f.write('MISFIT_DEP_TICK     2 \n\n')

f.write('# Inversion of point source parameters step 2 \n')
f.write('EFFECTIVE_DT_ST2    0.2 \n')
f.write('REL_NORTH_1         -20000 \n')
f.write('REL_NORTH_2         20000 \n')
f.write('REL_NORTH_STEP      2500 \n')
f.write('REL_EAST_1          -20000 \n')
f.write('REL_EAST_2          20000 \n')
f.write('REL_EAST_STEP       2500 \n')
f.write('REL_TIME_1          -0.2 \n')
f.write('REL_TIME_2          1 \n')
f.write('REL_TIME_STEP       0.2 \n')
f.write('BP_F1_STEP2         '+BP_F1+' \n')
f.write('BP_F2_STEP2         '+BP_F2+' \n')
f.write('BP_F3_STEP2         0.1 \n')
f.write('BP_F4_STEP2         0.11 \n')
f.write('MISFIT_MET_STEP2    l2norm  \n')
f.write('INV_MODE_STEP2      grid \n')
f.write('CC_SHIFT1           -5 \n')
f.write('CC_SHIFT2           5 \n')
f.write('LOOPS_LOC_CONF      1 \n')
f.write('REDUCE_LOC_CONF     3 \n\n')


f.write('# Phases windowing, step 2 \n')
f.write('PHASES_2_USE_ST2    a \n')
f.write('WEIGHT_P_ST2        1.00 \n')
f.write('WIN_START_P_ST2     0.25 \n')
f.write('WIN_TAPER_P_ST2     0.05 \n')
f.write('WIN_LENGTH_P_ST2    120 \n')
f.write('WEIGHT_A_ST2        1.00 \n')
f.write('WIN_START_A_ST2     0.20 \n')
f.write('WIN_TAPER_A_ST2     0.175 \n')
f.write('WIN_LENGTH_A_ST2    180 \n')
f.write('BP_F1_STEP2         0.0225 \n')
f.write('BP_F2_STEP2         0.025 \n')
f.write('BP_F3_STEP2         0.100 \n')
f.write('BP_F4_STEP2         0.110 \n')
f.write('SW_FIXTAPER_ST2     True \n')
f.write('SW_VERTICAL_ST2     False \n\n')

f.write('# Plot parameters for inversion step2 \n')
f.write('DATA_PLOT_STEP2     seis \n')
f.write('FILT_PLOT_STEP2     filtered \n')
f.write('START_PLOT_STEP2    0 \n')
f.write('LEN_PLOT_STEP2      300 \n')
f.write('TICK_PLOT_STEP2     50 \n')
f.write('AMPL_PLOT_STEP2     norm \n\n')

if nvar > 0:
	f.write('# Non-default parameters \n')
	for i in range(nvar):
		f.write(var[i]+ ' \t\t ' + val[i] +'\n')

f.flush()
f.close()


exit(0)	

