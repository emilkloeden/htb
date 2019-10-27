                                                                                     
import os
import subprocess


class BadFormatException(Exception):
        pass

def sentence_case(string: str) -> str:
        """
        Return a string with its first character in Uppercase and the rest in lowercase
        """
        if len(string) > 1:
                return f"{string[0].upper()}{string[1:].lower()}"
        elif len(string) == 1:
                return string[0].upper()
        return ""


def welcome(user: str, name: str, nmap: bool = False) -> str:
        """
        Return a banner welcome message
        """
        welcome_msg = ""
        second_line = f"Building scaffolding for HackTheBox's '{sentence_case(name)}' box.\n"
        try:
                import pyfiglet
                from termcolor import colored
                import colorama
                colorama.init()

                result = pyfiglet.figlet_format("HTB.py", font = "larry3d")
                welcome_msg += colored(result, 'green')
                welcome_msg += f"Welcome {colored(user,'green', attrs=['bold'])}!\n"
        
        except ModuleNotFoundError:
                welcome_msg += f"Welcome {user}!\n"
        finally:
                welcome_msg += second_line
        
        if nmap:
                welcome_msg += "Nmap scan option selected. This may take while.\n"
        
        return welcome_msg

        

def add_box_to_etc_hosts(name: str, ip: str) -> None:
        """
        Add an ipv4 entry to /etc/hosts file using <name>.htb as the hostname.
        Since this is so important, if it fails, the whole execution stops.
        """ 
        with open('/etc/hosts', 'r') as f:                        
                hostnames = []        
                ips = []                                                                                                                              
                lines = list(f.readlines())
                try:
                        ipv6_break = lines.index("\n")
                except ValueError:
                        raise BadFormatException("No blank line demarcating ipv4 and ipv6 addresses found. Unable to update /etc/hosts. Exiting")

                ipv4_lines = lines[:ipv6_break]
                rest = lines[ipv6_break:]

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

def run_nmap(path: str, ip: str) -> None:
        """
        Create an nmap directory and run a scan with default scripts. Output to stdout and file.
        """
        nmap_cmd = ['nmap', '-sC', '-sV', '-oN', 'nmap/nmap', ip]
        nmap_string = " ".join(nmap_cmd)
        print(f"Running {nmap_string}...")
        try:
                os.makedirs(f"{path}/nmap")
                os.chdir(path)
                with open(f"{path}/nmap/nmap", "w") as h:
                        io = subprocess.Popen(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)                                      
                        for line in io.stdout:
                                print(line.decode('utf8').strip())
                                h.write(line.decode('utf8'))
                        for line in io.stderr:
                                print(line.decode('utf8').strip())
        except FileExistsError:
                print(f"Directory: {path}/nmap already exists. Skipping nmap run.")

def massage_ip(ip: str) -> str:
        """
        Prepend 10.10.10 to a string. Allow the user to pass just the last segment of an ipv4 address.
        """
        dots = len([c for c in ip if c == "."])
        if dots == 0:                                                    
                return f"10.10.10.{ip}"
        return ip 

def make_scaffolding(path: str) -> None:
        """
        Create directory at <path> if not exists
        """
        try:
                os.makedirs(path)
                print(f"Creating directory: {path}...")
        except FileExistsError:
                print(f"Directory: {path} already exists. Skipping.")


def create_write_up(path: str, name: str) -> None:
        """
        Scaffold out a writeup markdown file in <path>/
        """
        with open(f"{path}/writeup.md", "w") as f:
                f.write(f"""
# {sentence_case(name)} HackTheBox writeup
## Initial Foothold


## User


## Root
                """)

def create_notes(path: str) -> None:
        """
        Create a file in which to keep notes. I like iterating in an executable fashion so I've saved it with a .py extension.
        """
        with open(f"{path}/notes.py", "w") as f:
                f.write("#!/usr/bin/env python\n\n")


                
