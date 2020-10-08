# pylibap
create new python programs sharing the same structure, the same debugging, the same logging

Usually working with systems in different environments it is helpful to use the same structure for all sysadmin programs. This repository holds 
1. a initializing python script pywrap.py. This script is used to get the highest available python3 version on the machine, find a program, initialize this program from its usage and config files and run it. Create a symbolic link in an executable path (i.e. ~HOME/bin) pointing to pywrap.py with the basename of your python script.
2. a template directory containing script_main.py, script_main_usg.py, script_main_cfg.py, sample_module.py all prepared to be rolled out as a new program by
3. the program newpy.py 
4. a small debug library which enables you to show the program flow, print useful messages and other stuff

So the first thing you should do after cloning this project is to create a link named 'newpy' in your ~/bin directory and try 'newpy -h'
