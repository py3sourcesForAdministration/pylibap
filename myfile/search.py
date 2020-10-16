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
#  from __main__ import dbg 
#  dbg.dprint(0, "Hallo",args)
  pythons = [ '/usr/bin/python3.5','/usr/bin/python3.6',
            '/usr/bin/python3.8','/usr/bin/python3.9' ]
  py      = list(filter( os.path.isfile, pythons ))
  if py:
    py = py.pop()
    foundpy = int( py[-3:-2] + py[-1:] )
    currentpy  = int( ''.join( map(str, sys.version_info[0:2]) ) )
    if "--DEBUG" in args[1:] :
        print(str("  DEBUG: Python Version: Current: " + str(currentpy) + \
                            ", Available: " + str(foundpy)))
    if currentpy < 36 and foundpy > currentpy:
      if "--DEBUG" in sys.argv[1:] : 
        print("  DEBUG: switching to "+py)
        print()
      newargs = args  
      newargs.insert( 0, args[0] )
      os.execv( py, newargs )

  return(py)
