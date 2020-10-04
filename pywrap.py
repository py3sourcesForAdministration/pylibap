#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Hilfsprogramm zur Suche und zum Start von Python Programmen. 
    Es ist notwendig, dass der private Bibliothekspad über die
    Environment Variable MYPYLIB gesetzt ist, andernfalls wird im 
    Homeverzeichnis des Users nach einem Directory mit dem Namen 
    pylibname (zu setzen unter diesem doctext) gesucht. 
"""
pylibname = 'pylibap'
##############################################################################
import os, os.path, sys, re
(prgdir,fname) = os.path.split(os.path.abspath(__file__))
(prgname,ext) = os.path.splitext(fname)
globals()['prgname'] = prgname
globals()['prgdir']  = prgdir

#### Select python to run with and replace 
pythons = [ '/usr/bin/python3.5','/usr/bin/python3.6',
            '/usr/bin/python3.8','/usr/bin/python3.9' ]
py      = list(filter( os.path.isfile, pythons ))
# print(__file__)
if py:
  py = py.pop()
  foundpy = int( py[-3:-2] + py[-1:] )
  currentpy  = int( ''.join( map(str, sys.version_info[0:2]) ) )
  if "--DEBUG" in sys.argv[1:] :
      print(str("  DEBUG: Python Version: Current: " + str(currentpy) + \
                          ", Available: " + str(foundpy)))
  if foundpy > currentpy:
    if "--DEBUG" in sys.argv[1:] : 
      print("  DEBUG:", __file__ ,"executing with "+py)
      print()
    args = sys.argv
    args.insert( 0, sys.argv[0] )
    os.execv( py, args )

### ----------------------------------------------------
def search_dirs(top, searches, ignore = re.compile('^$') ):
  """ Search for dirs matching one of searches, but
      ignore everything from ignore
  """     
  try:
    for entry in os.scandir(top):
      if entry.is_dir():
#         print(entry.path)
        if entry.name in searches:
#          print("-------------- found",entry.name)   
          yield entry.path
        elif not ignore.match(entry.name) :
          for res in search_dirs(entry.path, searches, ignore): 
            yield res
  except OSError as e:
    print(e, file=sys.stderr)
    pass

### ----------------------------------------------------
regs = ['^\.','__pycache__', ]
excludes=re.compile('|'.join(regs))
#for found in search_dirs(path,[search],excludes):
#  print(found) 
#  break

##############################################################################
def main():
##### Work on sys.argv 
  if len(sys.argv) > 1:
    if "--DEBUG+" in sys.argv[1:] :
      dbg.setlvl(+7) 
    elif "--DEBUG" in sys.argv[1:] :
      dbg.setlvl(+3) 
  globals()['prgargs'] = [ value for value in sys.argv[1:] if not value.startswith('--DEBUG')]
  dbg.entersub()
##### Check things
  dbg.dprint(2,"Wanted is",prgname, "called from", __file__ , "with args", prgargs )
##### Now search for program in Srcdir wait for execution and exit
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
        dbg.leavesub()
        return
        
##### Nothing found      
  print(prgname, "could not be found")
  dbg.leavesub()
  
if __name__ == "__main__":
  import sys
  import os
  try:
    libdir = os.environ['MYPYLIB']
  except KeyError:
    for found in search_dirs(path,[pylibname],excludes):
      print(found) 
      libdir = found
      break
  
  try:
    files  = [ os.path.join(libdir, "globaldefs.py"), 
             ]
    for f in (files):
      exec(open(f).read(), globals())
  except KeyError:
    print("Please set the environment variable MYPYLIB") ; sys.exit(1)
  except IOError as e:
    print("Unable to read: {0} {1}".format(f, e.strerror)) ; sys.exit(1)
  except SystemExit:
    sys.exit(1)
  except sys.exc_info()[0]:
      print("error exit: \"{0}\" in {1}".format(sys.exc_info()[1], f))
      sys.exit(1)  
  except:
    print("Something else") ; sys.exit(1)

  main()

