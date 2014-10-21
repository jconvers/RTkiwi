#!/usr/bin/env python
#
# Converts all files in folder from sac to mseed
#
# example: python sac2mseed.py


#!/usr/bin/env python
import glob 

from obspy.core import read

for infile in glob.glob('DISP*.sac'):

   print "Converting file " + infile + " to mseed format"

   st = read(infile)
   st.write(infile[0:len(infile)-3] + 'mseed', format='MSEED')
