#!/usr/bin/env python3                        
"""htb.py                                            
                                               
Usage:                                                                
  htb.py <name> <ip> [--nmap]                                              
                                                                                                                                                       
Arguments:                                                                                                                                            
  <name>        htb name of machine
  <ip>          ip address of machine on HTB VPN                                                                                                      
                     
Options:                                                                
  -h --help     print this message and exit.              
"""                                                                                      
import os                                                            
import subprocess                                                          
import getpass                                                                                                                                        
import colorama                                                                                                                                        
from termcolor import colored  
from docopt import docopt                                                                                                                              
                     
if __name__ == '__main__':                                              
        USER = getpass.getuser()                          
        colorama.init()                                
        arguments = docopt(__doc__)              
        ip = arguments['<ip>']
        name = arguments['<name>']    
        nmap = arguments['--nmap']
        dots = len([c for c in ip if c == "."])
        if dots == 0:                                                    
                ip = f"10.10.10.{ip}"          
        try:                                      
                import pyfiglet
                result = pyfiglet.figlet_format("HTB.py", font = "larry3d")
                print(colored(result, 'green'))
        except ModuleNotFoundError:                              
                pass                                                                                                                                  
        welcome_msg = f"Welcome {colored(USER,'green', attrs=['bold'])}!\nBuilding scaffolding for HackTheBox's '{name[0].upper()}{name[1:]}' box.\n"
        if nmap:                                                  
                welcome_msg += "Nmap scan option selected. This may take while.\n"
        print(welcome_msg)                            
        with open('/etc/hosts', 'r') as f:                        
                hostnames = []        
                ips = []                                                                                                                              
                lines = list(f.readlines())
                ipv6_break = lines.index("\n")
                if not ipv6_break:
                        print("No blank line demarcating ipv4 and ipv6 addresses found. Unable to update /etc/hosts. Exiting")
                        exit()        
                ipv4_lines = lines[:ipv6_break]  

                rest = lines[ipv6_break:]                                                                                                         [0/52]
                for line in ipv4_lines:
                        data = line.strip().split("\t")
                        etc_hosts_ip = data[0]
                        etc_hosts_hostnames = data[1:]
                        ips.append(etc_hosts_ip)
                        for etc_hosts_hostname in etc_hosts_hostnames:
                                hostnames.append(etc_hosts_hostname.lower())
                if name.lower() in hostnames or f"{name}.htb".lower() in hostnames:                                                                    
                        print(f"Hostname {name} already found in /etc/hosts. Skipping.")                                                              
                elif ip in ips:
                        print(f"Ip address {ip} already found in /etc/hosts. Skipping.")                                                              
                else:
                        ipv4_lines.append(f"{ip}\t{name.lower()}.htb\n")
                        with open('/etc/hosts', 'w') as g:
                                g.writelines(ipv4_lines)
                                g.writelines(rest)

        path = f"/root/ctf/htb/{name}"

        if nmap:
                nmap_cmd = ['nmap', '-sC', '-sV', '-oN', 'nmap/nmap', ip]
                nmap_string = " ".join(nmap_cmd)
                print(f"Running {nmap_string}...")
                try:
                        os.makedirs(f"{path}/nmap")
                        os.chdir(path)
                        with open(f"{path}/nmap/nmap", "w") as h:
                                io = subprocess.Popen(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)                                      
                                for line in io.stdout:
                                        print(line.decode('utf8'))
                                        h.write(line.decode('utf8'))
                                for line in io.stderr:
                                        print(line.decode('utf8'))
                except FileExistsError:
                        print(f"Directory: {path}/nmap already exists. Exiting.")                                                                      
                        exit()
        else:
                try:
                        os.makedirs(path)
                except FileExistsError:
                        print(f"Directory: {path} already exists. Exiting.")
                        exit()
