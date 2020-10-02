#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Class for Debugging a la perl """

import sys
import os
import pprint
import importlib
import numbers
from   colorama import init, Fore, Back, Style
 
reset    = Style.RESET_ALL
fgg      = Style.BRIGHT + Fore.GREEN
fgy      = Style.BRIGHT + Fore.YELLOW
fgr      = Style.BRIGHT + Fore.RED
etok1    = Style.BRIGHT + "-> ENTER" + Style.RESET_ALL
etok2    = Style.BRIGHT + "FROM" + Style.RESET_ALL
ltok1    = Style.BRIGHT + "<- LEAVE" + Style.RESET_ALL
ltok2    = Style.BRIGHT + " TO " + Style.RESET_ALL
warn     = fgy + "WARN" + reset + "  "
error    = fgr + "ERROR" + reset
tab      = " "*2
tbs      = ' '*2
dicton   = '{'
dictoff  = '}'
liston   = '['
listoff  = ']'
tupleon  = '('
tupleoff = ')' 

def singleton(cls):
  return cls()

@singleton
class dbg:
  """ Class and Instance for debugging which is
      automatically returned via singleton
  """    
  def __init__(self, lvl=0, idt=-1,col=fgg):
    self.__lvl = lvl
    self.__initlvl = lvl
    self.__idt = idt
    self.__col = fgg

  @property
  def initlvl(self):
    return self.__initlvl
  @property
  def lvl(self):
    return self.__lvl
  @property
  def idt(self):
    return self.__idt
  @property
  def col(self):
    return self.__col


  def __repr__(self):
    return "dbg(lvl=" + str(self.lvl) + ")"  

#############################################
####### User Functions ######################
#############################################
  def _initlvl(self, *new):
    """ Should only be used once to store initial 
    program debug option.              
    """   
    if new: 
      if isinstance(new[0],numbers.Number):
        new = int(new[0])
        if new >= 0 and new <= 255:
          self.__initlvl = new
          self.__lvl = new
          return self.lvl
    else:  
      return self.__initlvl

#############################################
  def setlvl(self, *new):
    """ Method to change the debug level """
    if new:
#      self.dprint(256,"new gesehen",new[0])
      if isinstance(new[0],numbers.Number):
        new = int(new[0]) 
#        self.dprint(0,"Leveländerung mit",new)

        if new > 255:
          return self.lvl
        elif new > 0: 
          res = self.__lvl | new
          self.__lvl = res
#          self.dprint(0,"+ self.__lvl: ",self.__lvl)  
        elif new < 0: 
          new = abs(new)
          self.__lvl = self.__lvl & ~new
#          self.dprint(0,"- self.__lvl: ",self.__lvl) 
          if self.__lvl < 0:
            dbg.dprint(256,"Das sollte aber nicht vorkommen! Level",self.__lvl)
            self.__lvl = 0
        else:
          self.__lvl = 0
#          self.dprint(0,"= self.__lvl: ",self.__lvl)
    else:
#      self.dprint(256,"Zurücksetzen")
      self.__lvl = self.__initlvl
#    self.dprint(256,"self.__lvl: ",self.__lvl)  
    return self.__lvl

#############################################
  def entersub(self):
    """     Method to print the function name on 
    enter at debuglevel 1 
    """
    self.__idt += 1
    if self.__lvl & 1: 
      me = os.path.basename(os.path.splitext( \
           sys._getframe(1).f_code.co_filename)[0]) + "." + \
           sys._getframe(1).f_code.co_name
      last = os.path.basename(os.path.splitext( \
           sys._getframe(2).f_code.co_filename)[0]) + "." + \
           sys._getframe(2).f_code.co_name
      print("%s %s %s %s %s" % (self.idt  * "  ", etok1, me, etok2, last))

#############################################
  def myname(self):
    """ Method to print the function name on enter at debuglevel 1 """
    me = os.path.basename(os.path.splitext( \
         sys._getframe(1).f_code.co_filename)[0]) + "." + \
         sys._getframe(1).f_code.co_name
    return(me)  

#############################################
  def myself(self):
    modname = os.path.basename(os.path.splitext( \
              sys._getframe(1).f_code.co_filename)[0])  
    fncname = sys._getframe(1).f_code.co_name
    mod = importlib.import_module(modname)
    return getattr(mod, fncname)

#############################################
  def mycaller(self):
    """ Method to print the function name on leave at debuglevel 1 """
    last = os.path.basename(os.path.splitext( \
           sys._getframe(2).f_code.co_filename)[0]) + "." + \
           sys._getframe(2).f_code.co_name
    return(last)       

#############################################
  def __precaller(self):
    """ Method to print the function name on leave at debuglevel 1 """
    last = os.path.basename(os.path.splitext( \
           sys._getframe(3).f_code.co_filename)[0]) + "." + \
           sys._getframe(3).f_code.co_name
    return(last)       

#############################################
  def leavesub(self):
    """ Method to print the function name on leave at debuglevel 1 """
    if self.__lvl & 1: 
      me = os.path.basename(os.path.splitext( \
                sys._getframe(1).f_code.co_filename)[0]) + "." + \
                sys._getframe(1).f_code.co_name
      last = os.path.basename(os.path.splitext( \
                sys._getframe(2).f_code.co_filename)[0]) + "." + \
                sys._getframe(2).f_code.co_name
      print("%s %s %s %s %s" % (self.idt  * "  ", ltok1, me, ltok2, last))
    self.__idt -= 1

    
#############################################
### Zusatz für dprintr
  def __dprintroff(self,start,depth,token): 
    """ Decides to place a ',' at end of recursion """
    depth -= 1  
    if token:  
      if depth == 0: 
        print(f"{start}{tab*(depth+1)}{token}")
      else:
        print(f"{start}{tab*(depth+1)}{token},")
    else:
      if depth > 0:
        print(f",")
      else: print()

#############################################
  def __printout(func):
    """ decorator to decide if printfunction is called """
    def function_wrapper(self,lvl,*args,**kwargs):
      if lvl == 0 :
        self.__col = fgy  
        func(self,lvl,*args,**kwargs)
      elif lvl >= 256 : 
        self.__col = fgr
        func(self,lvl,*args,**kwargs)
      elif self.lvl & lvl :
        self.__col = fgg
        func(self,lvl,*args,**kwargs)
      else: 
        pass
    return function_wrapper 
  

#############################################
  @__printout
  def dprint(self,lvl,*args,**kwargs):
    """ Method for debug prints at some level """
    start = tbs*(self.idt+1)
    strargs = []
    tok_name = []
    myargs  = ''
    prc = 0
    head = "DBG"
    pcont = '>>>'
    for i in range(0,len(args)):
      ### Die typen behandeln, die mit dprintr ausgegeben werden
      if isinstance(args[i],dict) or \
         isinstance(args[i],list) or \
         isinstance(args[i],tuple) :
        if len(args[i]) > 0 :
          if len(strargs):
            myargs = ' '.join(map(str, strargs))
            if prc > 0 :
              head = pcont
            print(f"{start}{head} {self.col}{lvl:03d}{reset} : {myargs}")
            prc +=1
            strargs.clear()
            myargs = ''
          self.dprintr(lvl,args[i],cont=prc)
          prc += 1
        else:
          strargs.append(args[i])
      ### Alles andere einsammeln    
      else:    
        strargs.append(args[i])
    ### Zum Schluß noch einmal gesammelt ausgeben    
    if len(strargs):
      myargs = ' '.join(map(str, strargs))
      if prc > 0 :
        head = pcont 
      print(f"{start}{head} {self.col}{lvl:03d}{reset} : {myargs}")
#    print(f"{start}---------")


#############################################
  @__printout
  def dprintr(self,lvl,ref,name='ref',depth=0,cont=0):
    """ Method for debug prints of objects """
    start = tbs*(self.idt+1) 
#    if len(args) == 1: name = args[0]
    if depth == 0:
      if cont and self.__precaller() == 'py3dbg.dprint':
        head = '>>>'
      else: 
        head = 'DBG'
#      print(f"{start}DBG {fgr}{self.__precaller()}{reset}")
      print(f"{start}{head} {self.col}{lvl:03d}{reset} : {name} = ",end='')
      dbg.dprintr(lvl,ref,depth=depth+1)
    else:
      ### handle dicts 
      if isinstance(ref,dict): 
        print(f"{dicton}")   
        for k,v in sorted(ref.items()):
          print(f"{start}{tab*(depth+1)}'{k}'{' '*(20-len(k))}: ",end='')
          dbg.dprintr(lvl,v,depth=depth+1)
        dbg.__dprintroff(start,depth,dictoff)
      ### handle lists 
      elif isinstance(ref,list):
        print(f"{liston}")
        for item in (ref):
          print(f"{start}{tab*(depth+1)}",end='')
          dbg.dprintr(lvl,item,depth=depth+1) 
        dbg.__dprintroff(start,depth,listoff)
      ### handle tuples  
      elif isinstance(ref,tuple):
        print(f"{tupleon}")
        for item in (ref):
          print(f"{start}{tab*(depth+1)}",end='')
          dbg.dprintr(lvl,item,depth=depth+1) 
        dbg.__dprintroff(start,depth,tupleoff)
      ### simple types without recursion  
      elif isinstance(ref,str):
        print(f"'{ref}'",end="")
        dbg.__dprintroff(start,depth,False)
      elif isinstance(ref,numbers.Number):
        print(f"{ref}",end='')
        dbg.__dprintroff(start,depth,False)
      else:
          print(f"repr: {repr(ref)}")

#############################################
### old funtions dprintl is old dprint. dprintref is unchanged      
#############################################
  @__printout
  def dprintl(self,lvl,*args):
    """ Method for debug print as list at some level """
    myargs = ' '.join(map(str, args))
    start = tbs*(self.idt+1)
    print(f"{start}DBG {self.col}{lvl:03d}{reset} : {myargs}")

#############################################
  @__printout
  def dprintref(self,lvl,ref,pname):   
    """ Method for debug prints of objects """
    print("%s  DBG %s%03d%s START: %s" % (tab*self.idt ,
            self.col, lvl ,Style.RESET_ALL, pname))
    pprint.pprint(ref)
    print("%s  DBG %s%02d%s   END: %s" % (self.idt * "  " ,
            self.col, lvl ,Style.RESET_ALL, pname))


    
    
###################################################################################
###            Muell
#  @lvl.setter
#  def lvl(self,lvl):
#    self.__lvl = lvl
#  @idt.setter
#  def idt(self,idt):
#    self.__idt = idt

#  @col.setter
#  def col(self,col):
#    self.__col = col

#  @oldlvl.setter
#  def oldlvl(self,lvl):
#    """ Method to set the debuglevel """
#    self.__initlvl = lvl

#    if lvl == 0:
#      print("%s  %s: %s" % (self.idt * "  " ,warn,myargs))
#    if self.lvl & lvl:
#      print("%s  DBG %s%02d%s: %s" % (self.idt * "  " ,
#            Fore.GREEN, lvl ,Style.RESET_ALL, myargs))
#    self.leavesub()
###   """ 
### #############################################
###   @__printout
###   def dprint(self,lvl,*args,**kwargs):
### #     Method for debug prints at some level 
###     start = tbs*(self.idt+1)
###     strargs = []
###     tok_name = []
###     myargs  = ''
###     for i in range(0,len(args)):
### #      print(type(args[i])) 
###       ##### angefüllte name= löschn und einen überspringen  
###       if (len(tok_name) == 2):
###         tok_name.clear()
###         continue
###       ### Standard literale Behandeln
###       if isinstance(args[i],str) : 
###         strargs.append(args[i])
###       elif isinstance(args[i],bool) :
###         strargs.append(args[i])
###       elif isinstance(args[i],numbers.Number) : 
###         strargs.append(args[i])
###       ### Die typen behandeln, die mit dprintr ausgegeben werden
###       elif isinstance(args[i],dict) or \
###            isinstance(args[i],list) or \
###            isinstance(args[i],tuple) :
###         print("candidate for dprintr")     
###         if len(args[i]) > 0 :
###           self.dprintr(lvl,args[i])
### #          if len(strargs):
### #            myargs = ' '.join(map(str, strargs))
### #            print(f"{start}DBG {self.col}{lvl:03d}{reset} : {myargs}")
### #            strargs.clear()
### #            myargs = ''
### #          if i+1 < len(args):
### #            if isinstance(args[i+1],str):
### #              tok_name = args[i+1].split('=',1)
### #              if len(tok_name) == 2 and tok_name[0].strip() == 'name':
### #                print("call to dprintr 1") 
### #                self.dprintr(lvl,args[i],name=tok_name[1].strip())
### #              else:
### #                print("call to dprintr 2") 
### #                self.dprintr(lvl,args[i]) 
### #          else:
### #            print("call to dprintr 2") 
### #            self.dprintr(lvl,args[i])
###         else:
###           print("append to strings")
###           strargs.append(args[i])
###           
###       ### Fallback
###       elif isinstance(repr(args[i]),str):
###         print("fallback") 
###         strargs.append(repr(args[i]))
###       ### und Notausgang  
###       else: 
###         print(f"{start}DBG {fgr}Dont know: {args[i]}{reset}")
###     ### Zum Schluß noch einmal gesammelt ausgeben    
###     if len(strargs):
###       myargs = ' '.join(map(str, strargs))
###       print(f"{start}DBG {self.col}{lvl:03d}{reset} : {myargs}")
###           
### #    myargs = ' '.join(map(str, args))
### #    print(f"{start}DBG {self.col}{lvl:03d}{reset} : {myargs}")
### #    print("%s  DBG %s%03d%s : %s" % (tab*self.idt,
### #            self.col, lvl ,Style.RESET_ALL, myargs))
###   """
