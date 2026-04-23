#!/usr/bin/env python3

import argparse

from modules.disk import disk_stats
from modules.cpu import cpu_stats
from modules.ports import ports_stats
from modules.ram import ram_stats
from modules.overview import get_overview

def main():
    # Set up the argument parser to handle command-line options
    parser = argparse.ArgumentParser(description="Sysinfo", usage="main.py [option]")

    # Add arguments for different system information categories
    parser.add_argument("-d", "--disk", action="store_true", help="check disk stats")
    parser.add_argument("-c", "--cpu", action="store_true", help="check cpu stats")
    parser.add_argument("-p", "--ports", action="store_true", help="check listen ports")
    parser.add_argument("-r", "--ram", action="store_true", help="check RAM stats")
    parser.add_argument("-o", "--overview", action="store_true", help="check top 10 processes with most CPU usage")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check which options were provided and call the functions accordingly
    if args.disk:
        disk_stats()
    elif args.cpu:
        cpu_stats()
    elif args.ports:
        ports_stats()
    elif args.ram:
        ram_stats()
    elif args.overview:
        get_overview()
    else:
        print("No option provided. Please use one of the following options:\n")
        parser.print_help()
        
if __name__ == "__main__":    
    main()