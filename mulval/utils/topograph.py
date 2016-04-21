#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import os

pointDict = {}
subnet = {}
withoutnet = {}

class vertices:

	def __init__(self, id):
		self.link = []
		self.id = id

	def printId(self):
		print self.id
		print self.link

def buildVertices():
	fp = open("h2v1s5.P", "r+") # remember the name!!
	pattern1 = re.compile(r'hacl\(\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)\.')
	pattern2 = re.compile(r'^inSubnet\(\s*(\w+),\s*(\w+)\)\.')

	id = 1
	while 1:
		buf = fp.readline()
		# print buf
		if not buf:
			break
		match1 = pattern1.search(buf)
		match2 = pattern2.search(buf)
		p1 = p2 = p3 = ''
		if match1:
			p1 = match1.groups()[0]
			p2 = match1.groups()[1]
		if match2:
			p3 = match2.groups()[0]
		if p1 != '' and p1 not in pointDict.keys():
			pointDict[p1] = vertices(id)
			withoutnet[p1] = vertices(id)
			id=id+1
			#print p1
		if p2 != '' and p2 not in pointDict.keys():
			pointDict[p2] = vertices(id)
			withoutnet[p2] = vertices(id)
			id=id+1
			#print p2
		if p3 != '' and p3 not in pointDict.keys():
			pointDict[p3] = vertices(id)
			withoutnet[p3] = vertices(id)
			id=id+1
			#print p3

	fp.close()


def buildConnection():
	fp = open("AttackGraph.dot", "r+")

	while(1):
		buf = fp.readline()
		# print buf
		if not buf:
			break
		pattern = re.compile(r'hacl\(\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\).') 
		match = pattern.search(buf) 

		if match:
			# print match.groups()[0] 
			ori = match.groups()[0]
			dest = match.groups()[1]
			pointDict[ori].link.append(dest)
			withoutnet[ori].link.append(dest)

	fp.close()

def getSubnet():
	fp = open("h2v1s5.P", "r+") # remember the name!!
	pattern2 = re.compile(r'^inSubnet\(\s*(\w+),\s*(\w+)\)\.')

	id = 1
	while 1:
		buf = fp.readline()
		# print buf
		if not buf:
			break
		match2 = pattern2.search(buf)
		if match2:
			p3 = match2.groups()[0]
			subnetId = match2.groups()[1]
			if subnetId not in subnet.keys():
				subnet[subnetId] = []
			subnet[subnetId].append(p3)
			if p3 in withoutnet.keys():
				del withoutnet[p3]

	fp.close()

def convMetric():
	#for key in pointDict.keys():
		#pointDict[key].printId()

	a = 0
	b = len(pointDict.keys())
	print b
	narray = [[0] * b] * b
	used = [0] * b
	for key in pointDict.keys():
		for key2 in pointDict[key].link:
			print pointDict[key2].id, pointDict[key].id
			narray[pointDict[key2].id][pointDict[key].id] = narray[pointDict[key].id][pointDict[key2].id] = 1

	print narray
	print used

	for i in range(b):
		if used[i] == 0:
			dfs(used, narray, b, i)
			a = a+1
	print a

def dfs(used, narray, size, cur):
	used[cur] = 1
	for i in range(size):
		if used[i] == 0 and narray[i][cur] == 1:
			used[i] = 1
			dfs(used, narray, size, i)


def printDot():
	fp = open("TopoAttackGraph.dot", "w")
	seq = []
	seq.append('digraph G {\n')

	for key in withoutnet.keys():
		seq.append('t' + str(pointDict[key].id) + ' [label="' + key + '",shape=none,image="/Users/Saint/Code/CyberMetric/mulval/img/server.jpeg"];\n')

	for sub in subnet.keys():
		seq.append('subgraph cluster_'+ sub + '{\nlabel="' + sub + '";\nbgcolor="mintcream";\n')
		for key in subnet[sub]:
			seq.append('t' + str(pointDict[key].id) + ' [label="' + key + '",shape=none,image="/Users/Saint/Code/CyberMetric/mulval/img/server.jpeg"];\n')
		seq.append('}\n')

	for key in pointDict.keys():
		for value in pointDict[key].link:
			seq.append('t' + str(pointDict[key].id) + ' -> t' + str(pointDict[value].id) + ';\n')

	seq.append('}\n')
	#print seq
	fp.writelines(seq)
	fp.close()
	os.system('dot -Tpng TopoAttackGraph.dot > TopoAttackGraph.png')

if __name__ == "__main__":
	buildVertices()
	#print withoutnet
	#print pointDict
	buildConnection()
	#print pointDict
	getSubnet()
	convMetric()
	#printDot()
