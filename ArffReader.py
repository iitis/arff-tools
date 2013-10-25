# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2013 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys

class ArffReader:
	def __init__(self, src):
		self.src = src
		self.headers = []
		self.fields = []
		self.types = dict()
		self.relation = "''"
		self.seekbuf = dict()

		# read field definitions
		for line in src:
			self.headers.append(line)

			# yuck!
			v = line.strip().split(None, 2)
			if len(v) == 0:
				continue
			elif len(v) == 1:
				token = v[0].lower()
				name = None
				val = None
			elif len(v) == 2:
				token = v[0].lower()
				name = v[1]
				val = None
			else:
				token = v[0].lower()
				name = v[1]
				val = v[2]

			if token == '@attribute':
				self.fields.append(name)
				self.types[name] = val
			elif token == '@relation':
				self.relation = name
			elif token == '@data':
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

	def printh(self, fields=None):
		if fields:
			sys.stdout.write("@relation %s\n" % self.relation)
			for f in fields:
				sys.stdout.write("@attribute %s %s\n" % (f, self.types[f]))
			sys.stdout.write("@data\n")
		else:
			sys.stdout.writelines(self.headers)

	def printd(self, d, fields=None, sep=","):
		if not fields: fields = self.fields
		sys.stdout.write(sep.join([d[f] for f in fields]) + "\n")
