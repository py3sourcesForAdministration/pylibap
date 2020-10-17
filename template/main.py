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
##### Set global vars needed for init
(prgdir,fname) = os.path.split(os.path.realpath(__file__))
(prgname,ext) = os.path.splitext(fname)

###########   M A I N   #######################################################
def main():
  """ Main wrapper part for module calls
  """
  dbg.entersub()
  dbg.leavesub()

###########   D E F A U L T   I N I T   #######################################
if __name__ == "__main__":
  try:
    libdir = os.environ['MYPYLIB']
    if prgdir not in sys.path:
      sys.path.insert(0, prgdir)
    if libdir not in sys.path:
      sys.path.insert(0, libdir)
    from DBG.py3dbg import dbg
    files  = [ os.path.join(prgdir, prgname+"_imp.py"),
               os.path.join(prgdir, prgname+"_cfg.py"), 
               os.path.join(prgdir, prgname+"_usg.py")]
    for f in (files):
      exec(open(f).read())
  except KeyError as message:
    raise KeyError(message)
    sys.exit(1)
  except IOError as e:
    print("Unable to read: {0} {1}".format(f, e.strerror)) 
    sys.exit(1)
  except sys.exc_info()[0]:
    if not ( repr(sys.exc_info()[1]) == "SystemExit(0,)" or \
            repr(sys.exc_info()[1]) == "SystemExit(0)" ):     # py3.9 
      print("error exit: \"{0}\" in {1}".format(sys.exc_info()[1], f))
    sys.exit(1)
  except:  
    print("Init: Some unknown error in loading file ",f); sys.exit(1)
  main()
