#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Helper Functions to search files """
import os,sys,re
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
def get_latest_python3(args):
  """ function to switch to the highest available python version
      if needed, but always return the path to found python
  """
  pythons = [ '/usr/bin/python3.5','/usr/bin/python3.6',
            '/usr/bin/python3.8','/usr/bin/python3.9' ]
  py      = list(filter( os.path.isfile, pythons ))
  if py:
    py = py.pop()
    foundpy = int( py[-3:-2] + py[-1:] )
    currentpy  = int( ''.join( map(str, sys.version_info[0:2]) ) )
    if "--DEBUG" in args[1:] or "--DEBUG+" in args[1:]:
        print(str("DEBUG   : Python Version: Current: " + str(currentpy) + \
                            ", Available: " + str(foundpy)))
    if currentpy < 36 and foundpy > currentpy:
      if "--DEBUG" in sys.argv[1:] or "--DEBUG+" in args[1:]: 
        print("DEBUG   : switching to "+py)
        print()
      newargs = args  
      newargs.insert( 0, args[0] )
      os.execv( py, newargs )

  return(py)

### ----------------------------------------------------
def default_main_init(prgdir,prgname):
  """ function to do the initialization if program is called
      as main
  """     
  try:
    libdir = os.environ['MYPYLIB']
    if prgdir not in sys.path:
      sys.path.insert(0, prgdir)
    if libdir not in sys.path:
      sys.path.insert(0, libdir)
    exec(open(os.path.join(prgdir,prgname+'_imp.py')).read())
    files  = [ 
               os.path.join(prgdir, prgname+"_usg.py"),
               os.path.join(prgdir, prgname+"_cfg.py") ]
    for f in (files):
      exec(open(f).read(), globals())
  except KeyError as missing:
    print("missing key",missing) 
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
  print(globals())  