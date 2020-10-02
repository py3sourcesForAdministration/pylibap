#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Docstring: replace
"""
import os, os.path, sys
#### Select python to run with and replace 
pythons = [ '/usr/bin/python3.5','/usr/bin/python3.6', '/usr/bin/python3.9' ]
py      = list(filter( os.path.isfile, pythons ))
# print(py)
if py:
  py = py.pop()
  thepy = int( py[-3:-2] + py[-1:] )
  mypy  = int( ''.join( map(str, sys.version_info[0:2]) ) )
  if thepy > mypy:
    print("moving versions to "+py)
    args = sys.argv
    args.insert( 0, sys.argv[0] )
    os.execv( py, args )

############### Normal start of file #########################################
(prgdir,fname) = os.path.split(os.path.abspath(__file__))
(prgname,ext) = os.path.splitext(fname)
globals()['prgname'] = prgname
globals()['prgdir']  = prgdir
exec(open(os.path.join(prgdir,prgname+'_imp.py')).read())
###########   M A I N   ######################################################
def main():
  """ Main wrapper part for module calls
  """
  dbg.entersub()
  newpath = os.path.join(os.environ['MYPYSRC'],prgargs.name)
  try:
    os.mkdir(newpath)
  except:
    dbg.dprint(256,"path already exists:",newpath)

  templdir = os.path.join(os.environ['MYPYLIB'],'template')
  for top, dirs, files in os.walk(templdir):
    for f in files:
      if f.endswith('.py'):
        if f.startswith('main'):
          newf = f.replace('main',prgargs.name)
          shutil.copy2(os.path.join(templdir,f), os.path.join(newpath,newf))
#          if newf == prgargs.name + '.py':
#            os.chmod(os.path.join(newpath,newf),0o755)
          print(newf)
        else: 
          shutil.copy2(os.path.join(templdir,f), os.path.join(newpath,f)) 
          print(f)


  dbg.leavesub()
###########   D E F A U L T   I N I T   #######################################
if __name__ == "__main__":
  try:
    libdir = os.environ['MYPYLIB']
    files  = [ os.path.join(libdir, "globaldefs.py"),
               os.path.join(prgdir, prgname+"_usg.py"),
               os.path.join(prgdir, prgname+"_cfg.py") ]
    for f in (files):
      exec(open(f).read(), globals())
  except KeyError:
    print("Please set the environment variable MYPYLIB") ; sys.exit(1)
  except IOError as e:
    print("Unable to read: {0} {1}".format(f, e.strerror)) ; sys.exit(1)
  except sys.exc_info()[0]:
    if not ( repr(sys.exc_info()[1]) == "SystemExit(0,)" or \
             repr(sys.exc_info()[1]) == "SystemExit(0)" ):     # py3.9 
      print("error exit: \"{0}\" in {1}".format(sys.exc_info()[1], f))
    sys.exit(1)
  except:  
    print("Init: Some unknown error in loading file ",f); sys.exit(1)
  main()
