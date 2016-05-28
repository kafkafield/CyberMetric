#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

fp = open("h2v1s5.P", "r+")
fp2 = open("h2v1s52.P", "w")
seq = []
while(1):
	buf = fp.readline()
	# print buf
	if not buf:
		break
	pattern = re.compile(r'(CVE-2016-[0-9]+)')
	match = pattern.search(buf) 
	if match:
		buf = re.sub(r'(CVE-2016-[0-9]+)', "'" + match.groups()[0] + "'", buf) 
	print buf
	seq.append(buf + "\n")

fp2.writelines(seq)
fp2.close()
fp.close()