#!/usr/bin/env python3
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2013 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys
import argparse
from ArffReader import *

def check(d, todo):
	for col,val in todo:
		if d[col] != val: return False
	return True

def checkor(d, todo):
	for col,val in todo:
		if d[col] == val: return True
	return False

def main(src, todo, invert, useor):
	src = ArffReader(src)

	if useor:
		func = checkor
	else:
		func = check

	if invert:
		for d in src:
			if not func(d, todo): src.printd(d)
	else:
		for d in src:
			if func(d, todo): src.printd(d)

if __name__ == "__main__":
	p = argparse.ArgumentParser(description='Filter ARFF files by column values', epilog='''
		E.g. in order to skip flows where c1 is 0, use %(prog)s -v c1,0''')
	p.add_argument('expression', nargs='+', help='column,value')
	p.add_argument('-v','--invert-match', action='store_true', help='invert the sense of matching')
	p.add_argument('-o','--or', dest='useor', action='store_true', help='use OR instead of AND for expressions')
	p.add_argument("--exe", help="exec given Python file first")
	args = p.parse_args()

	todo = [p.split(',') for p in args.expression]

	if args.exe: exec(open(args.exe).read())

	main(sys.stdin, todo, args.invert_match, args.useor)
