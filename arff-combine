#!/usr/bin/env python3
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2013 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys
import argparse
from ArffReader import *

def main(todo):
	readers = []
	cols = []

	# open input files
	for f,c in todo:
		if f == "-":
			f = sys.stdin
		else:
			f = open(f, "r")

		readers.append(ArffReader(f))
		cols.append([s.strip() for s in c.split(',')])

	# read line-by-line
	for d in readers[0]:
		fid = int(d["fc_id"])

		data = [d]
		for r in readers[1:]:
			data.append(r.seek(fid))

		fields = [str(fid)]
		for d,c in zip(data, cols):
			fields.extend([d[x] for x in c])

		print(",".join(fields))

if __name__ == "__main__":
	p = argparse.ArgumentParser(description='Combine ARFF files by first column', epilog='''
		E.g. in order to combine columns c1 and c2 from file1 and
		column c3 from file2, use
		%(prog)s ./file1 ./file2 -f c1,c2 -f c3''')
	p.add_argument('file', nargs='+', help='input ARFF file')
	p.add_argument('-f','--fields', action='append', help='fields to extract (CSV, one by one)')
	p.add_argument("--exe", help="exec given Python file first")
	args = p.parse_args()

	if args.exe: exec(open(args.exe).read())

	main(zip(args.file, args.fields))
