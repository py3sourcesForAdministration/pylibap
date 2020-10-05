#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This file is loaded first for all my progs,
    it is used to initialize the path and then 
    initializes the global dbg object
"""    
###### Setup Libdir
import sys
import os
###### Set sys.path to "libdir" and "prgdir" 
# print("in globaldefs : ", prgdir) 
if prgdir not in sys.path:
  sys.path.insert(0, prgdir)
if libdir not in sys.path:
  sys.path.insert(0, libdir)
###### Load my Global Libraries 
from DBG.py3dbg import dbg


