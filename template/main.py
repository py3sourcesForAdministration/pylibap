#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Docstring: replace
"""
import os, os.path, sys
##### check for minimum python version and MYPYLIB
if sys.version_info < (3,6):
  print("python should be at least version 3.6") ; sys.exit(1)  
if 'MYPYLIB' not in os.environ:
  print("you need to set os.environ['MYPYLIB']") ; sys.exit(1)
else:
  libdir = os.environ['MYPYLIB']
  if libdir not in sys.path:
    sys.path.insert(0, libdir) 
  import myfile.search

(prgdir,fname) = os.path.split(os.path.realpath(__file__))
(prgname,ext) = os.path.splitext(fname)
#globals()['prgname'] = prgname
#globals()['prgdir']  = prgdir
#exec(open(os.path.join(prgdir,prgname+'_imp.py')).read())
###########   M A I N   ######################################################
def main():
  """ Main wrapper part for module calls
  """
  dbg.entersub()
  dbg.leavesub()
###########   D E F A U L T   I N I T   #######################################
if __name__ == "__main__":
  from DBG.py3dbg import dbg
  myfile.search.default_main_init(prgdir,prgname)
  main()
