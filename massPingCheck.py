#!/usr/bin/env python

import os
import sys
import commands
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='mass ping check script', epilog='usage: massPingCheck.py [-v] host_file', formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=5))
    parser.add_argument("list_file", default="", help="file containing IPs to process")

    parser.add_argument("-q", "--quiet", action='store_true', default=False, dest="quiet", help="output nothing")
    parser.add_argument("-v", "--verbose", action="store", type=int, default="2", dest="verbose", help="verbosity level", metavar="verbose")
    parser.add_argument("-n", "--no-linebreak", action='store_false', default=True, dest="noLineBreak", help="do not break lines when dumping")
    parser.add_argument("-r", "--retry", action="store", type=int, default="1", dest="retry_number", help="number of retries (default 1)", metavar="retries")
    args = parser.parse_args()
    return args

args = parseArgs()

with open(args.list_file) as input_file: # with a file opened
    host_list = input_file.readlines()  # read this shit
host_list = [i.strip() for i in host_list] # for each shit, remove stuff like \n, spaces, etc...
if args.verbose >= 3:
    print "ip list: %s" % host_list  # uncomment for debug

fail_list = []
for host in host_list:
    if args.verbose >= 2:
        print "%i/%i pinging %s" %(100. * host_list.index(host) / (len(host_list)), 100, host)
    response = os.system("ping -c %s %s 1>/dev/null 2>/dev/null" % (args.retry_number, host))
    if response: # will fail the ping if return code is something else than 0
        fail_list += [host]

if len(fail_list):
    if args.verbose:
        print "\n--------------------------------"
        print "failed hosts! goddamn it johnny!"
        print "--------------------------------\n"
    if args.noLineBreak:
        print " ".join(fail_list)
    else:
        print "\n".join(fail_list)
