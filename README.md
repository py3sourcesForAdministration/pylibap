# pylibap
create new python programs sharing the same structure, the same debugging, the same logging

Usually working with systems in different environments it is helpful to use the same structure for all sysadmin programs. This repository holds 
1. a initializing python script pywrap.py. This script is used to get the highest available python3 version on the machine, find a program, initialize this program from its usage and config files and run it. Create a symbolic link in an executable path (i.e. ~HOME/bin) pointing to pywrap.py with the basename of your python script.
2. a template directory containing script_main.py, script_main_usg.py, script_main_cfg.py, sample_module.py all prepared to be rolled out as a new program by
3. the program newpy.py 
4. a small debug library which enables you to show the program flow, print useful messages and other stuff

So the first thing you should do after cloning this project is to create a link named 'newpy' in your ~/bin directory and try 'newpy -h'

Terms of use/License:

    pylibap - Library and Helper to create new python programs with common structure

    Copyright © 2020 Armin Poschmann

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

