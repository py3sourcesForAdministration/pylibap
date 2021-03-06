#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse,sys,os
from __main__ import prgname,dbg

class myFormatter(argparse.RawTextHelpFormatter,argparse.ArgumentDefaultsHelpFormatter): 
  pass

parser = argparse.ArgumentParser(formatter_class=myFormatter)
parser.add_argument('-d', type=int,default=0, metavar="debug", dest="debug",        
                        help="set debug level to num\n\t\t")
args = parser.parse_args()
globals()['prgargs']  = args
dbg._initlvl(prgargs.debug) 
dbg.dprint(2, "prgargs" , prgargs)
