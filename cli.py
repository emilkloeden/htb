#!/usr/bin/env python3                        
"""HackTheBox                                            
                                               
Usage:                                                                
  cli.py <name> <ip> [--nmap] [--path=<base>]
                                                                                                                                                       
Arguments:                                                                                                                                            
  <name>        htb name of machine
  <ip>          ip address of machine on HTB VPN                                                                                                      
                     
Options:                                                                
  -h --help     print this message and exit.
  -n --nmap     run an nmap scan with default scripts, saving output to nmap directory
  -p --path=<base>     specify a path in which to scaffold into (e.g. --path/<name>)
""" 

import htb
import getpass
import os
from docopt import docopt
from formatting import red, green, yellow
from bad_format_exception import BadFormatException

def main():
        arguments = docopt(__doc__)
        ip = arguments['<ip>']
        name = arguments['<name>']    
        nmap = arguments['--nmap']
        base_path = arguments['--path'] if arguments['--path'] else os.getcwd()
        path = f"{base_path}/{name}"
        ip = htb.massage_ip(ip)
        


        user = getpass.getuser()
        print(htb.welcome(user=user, name=name, nmap=nmap))  

        try:
                htb.add_box_to_etc_hosts(name=name, ip=ip)
        except BadFormatException as e:
                print(red(e))
                exit()
        
        htb.make_scaffolding(path=path)
        
        if nmap:
                htb.run_nmap(path=path, ip=ip)

        print(f"Creating {path}/{green('writeup.md')}...")
        htb.create_write_up(path=path, name=name)
        print(f"Creating {path}/{green('notes.py')}...")
        htb.create_notes(path=path)

if __name__ == '__main__':                                      
        main()