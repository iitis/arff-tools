# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2013 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys

class ArffReader:
	def __init__(self, src):
		self.header = []
		self.src = src
		self.fields = []
		self.seekbuf = dict()

		# read field definitions
		for line in src:
			self.header.append(line)
			line = line.strip()
			if line[0:11] == '@attribute ':
				self.fields.append(line.split()[1])
			elif line[0:5] == '@data':
				break

	def __iter__(self): return self
	def next(self): return self.__next__()
	def __next__(self):
		for line in self.src:
			line = line.strip()
			return dict(zip(self.fields, line.split(',')))
		raise StopIteration

	def seek(self, fid):
		if type(fid) == str:
			fid = int(fid)

		if fid in self.seekbuf:
			return self.seekbuf.pop(fid)

		# TODO?: garbage collector

		for d in self:
			fid2 = int(d["fc_id"])
			if fid == fid2:
				return d
			else:
				self.seekbuf[fid2] = d

		raise Exception("flow %d not found" % fid)

	def printl(self, line):
		if self.header:
			sys.stdout.writelines(self.header)
			self.header = None

		sys.stdout.write(line + "\n")

	def printd(self, d):
		if self.header:
			sys.stdout.writelines(self.header)
			self.header = None

		sys.stdout.write(",".join([d[k] for k in self.fields]) + "\n")
