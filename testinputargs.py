#!/usr/bin/env python
# this script tests arguments as inputs for the rapid.inp file

import argparse


parser = argparse.ArgumentParser(description='test input arguments for rapidinv.inp files')
parser.add_argument('-P','--PARAMETERS',nargs='+',help='input argument name and value as FLAGNAME1 3.15 FLAGNAME2 TRUE. Values can be numners or logical as per variable required')
args = parser.parse_args()

print len(args.PARAMETERS)


exit(0)
