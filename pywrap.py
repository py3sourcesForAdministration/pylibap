#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Hilfsprogramm zur Suche und zum Start von Python Programmen. 
    Es ist notwendig, dass der private Bibliothekspad über die
    Environment Variable MYPYLIB gesetzt ist, andernfalls wird im 
    Homeverzeichnis des Users nach einem Directory mit dem Namen 
    pylibname (zu setzen unter diesem doctext) gesucht. 
"""
import os, os.path, sys, re
pylibname = 'pylibap'
searches = ['^'+pylibname+'$']
search   = re.compile('|'.join(searches))
stype    = 'is_dir' 
regexExclude = ['^__pycache__$','^\.local$']
excludes     = re.compile('|'.join(regexExclude))
##############################################################################
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
def filepath_search_names(top, stype, search, ignore = re.compile('^$') ):
  """ Search for files,dir or symlinks in file system. Takes two
      required parameters and one optional with keyword ignore.
      1. stype:   one of 'is_file', 'is_dir', 'is_symlink' (required)
      2. search: a precompiled regex that must be matched (required)
      3. ignore=precompiled_regex to ignore names         (optonal)

      Returns a generator for file paths matching the search regex
  """     
  try:
    for entry in os.scandir(top):
      if entry.__getattribute__(stype)():
        if search.match(entry.name):   
          yield entry.path
      if entry.is_dir():    
        if not ignore.match(entry.name) :
          for res in filepath_search_names(entry.path, stype, search, ignore): 
            yield res
  except OSError as e:
    print(e, file=sys.stderr)
    pass
### ----------------------------------------------------


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
  
### ----------------------------------------------------
if __name__ == "__main__":
  import sys
  import os
### ----------------------------------------------------
  try:
    libdir = os.environ['MYPYLIB']
  except KeyError:
    for found in filepath_search_names(os.environ['HOME'],stype,search,excludes):
      libdir = found
      if libdir:
        print("Please set the environment variable MYPYLIB to",libdir)
        os.environ['MYPYLIB'] = libdir
      break
    pass 

  try:
    files  = [ os.path.join(libdir, "globaldefs.py"),]
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

