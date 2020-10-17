#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" helper programm to search and start python programs. 
    selects an available version > 3.6 to run.
    preference according to the order in 
      myfile.search.get_latest_python3
    Also sets the environment variable MYPYLIB  
"""
import os, os.path, sys
#(realdir,rname) = os.path.split(pathlib.Path(__file__).resolve())
(realdir,rname) = os.path.split(os.path.realpath(__file__))
(calldir,cname) = os.path.split(os.path.abspath(__file__))
if "--DEBUG+" in sys.argv[1:] or "--DEBUG" in sys.argv[1:]:
  print("DEBUG   : called as",cname,"in dir",calldir,"but is",rname,"in",realdir )
if cname == rname:
  print("This program is a wrapper and not meant to be called itself !")
  sys.exit(1)
libdir = os.environ['MYPYLIB'] = realdir
if libdir not in sys.path:
  sys.path.append(0, libdir)

(prgname,ext) = os.path.splitext(cname)
import myfile.search
py = myfile.search.get_latest_python3(sys.argv)
from DBG.py3dbg import dbg  
##############################################################################
def main():
##### Work on sys.argv 
  if len(sys.argv) > 1:
    if "--DEBUG+" in sys.argv[1:] :
      dbg.setlvl(+7) 
    elif "--DEBUG" in sys.argv[1:] :
      dbg.setlvl(+3) 
  globals()['prgargs'] = [ value for value in sys.argv[1:] if not value.startswith('--DEBUG')]
##### Check things
  dbg.dprint(2,"Wanted is",prgname, "called from", __file__ , "with args", prgargs )
##### Now search for program in srcdir wait for execution and exit
  # dbg.dprint(1, "Python Version:",sys.version)
  for top, dirs, files in os.walk(os.path.dirname(libdir)):
    for nm in files:
      path = os.path.join(top, nm)
      dbg.dprint(4,path)
      if nm.startswith(prgname) and '_' not in nm and nm.endswith('.py') :
        fullname = os.path.join(top, nm)
        dbg.dprint(2,"found", fullname )
##### Execute the first found python prog and 
        from subprocess import Popen
        dbg.setlvl()
        if "--DEBUG" in sys.argv[1:] or "--DEBUG+" in sys.argv[1:]:
          dbg.dprint(0,  py,fullname, ' '.join(prgargs[0:]),"\n")   
        p = Popen([py] + [fullname] + prgargs[0:])
        p.wait()
        #dbg.leavesub()
        return
        
##### Nothing found      
  print(prgname, "could not be found")
  
##############################################################################
### ----------------------------------------------------
if __name__ == "__main__":
  main()

