#!/usr/bin/env python
# this script makes the folders and possibly copies the SAC files??
# for now its just making the folders

import os
import shutil

INVERSIONDIR="inversion"
OUTPUTDIR="output"
# directory of input data
DATADIRIN="data-orig/"

# directory of output data
DATADIROUT="data-proc"
DATADIROUTRT="data-proc-RT"


# creating folder "inversion"
if os.path.isdir(INVERSIONDIR):
	print "Folder '" + INVERSIONDIR + "' already exists, will not create\n"
elif os.path.isfile(INVERSIONDIR):
	print "'" +INVERSIONDIR+"' must be a folder, not a file\n"
	shutil.move(INVERSIONDIR,INVERSIONDIR+".old") 
else:
	print "creating folder '"+INVERSIONDIR+"' \n"
	os.mkdir(INVERSIONDIR)

# creating folder "output"
if os.path.isdir(OUTPUTDIR):
	print "Folder '" + OUTPUTDIR + "' already exists, will not create\n"
elif os.path.isfile(OUTPUTDIR):
	print "'" +OUTPUTDIR+"' must be a folder, not a file\n"
	shutil.move(OUTPUTDIR,OUTPUTDIR+".old") 
else:
	print "creating folder '"+OUTPUTDIR+"' \n"
	os.mkdir(OUTPUTDIR)

# checking DATAIROUT folder
if os.path.isdir(DATADIROUT):
	print "will remove previous '"+DATADIROUT+"' folder to make new one"
	shutil.rmtree(DATADIROUT)
elif os.path.isfile(DATADIROUT):
	shutil.move(DATADIROUT,DATADIROUT+".old")
print "Creating folder "+DATADIROUT
os.mkdir(DATADIROUT)

# Do for DATAIROUTRT the same as DATAIROUT:
if os.path.isdir(DATADIROUTRT):
	print "will remove previous '"+DATADIROUTRT+"' folder to make new one"
	shutil.rmtree(DATADIROUTRT)
elif os.path.isfile(DATADIROUTRT):
	shutil.move(DATADIROUTRT,DATADIROUTRT+".old") 
print "Creating Folder "+DATADIROUTRT
os.mkdir(DATADIROUTRT)





exit(0)
