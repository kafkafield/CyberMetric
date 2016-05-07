#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import os
import copy

pointDict = {}
subnet = {}
withoutnet = {}

class vertices:

	def __init__(self, id):
		self.link = []
		self.id = id

	def loadImport(self, ip):
		self.importance(ip)

	def printId(self):
		print self.id
		print self.link

def buildVertices():
	fp = open("h2v1s5.P", "r+") # remember the name!!
	pattern1 = re.compile(r'hacl\(\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)\.')
	pattern2 = re.compile(r'^inSubnet\(\s*(\w+),\s*(\w+)\)\.')

	id = 0
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
			if dest not in pointDict[ori].link:
				pointDict[ori].link.append(dest)
				withoutnet[ori].link.append(dest)

	fp.close()

def buildConnectionOrigin():
	fp = open("h2v1s5.P", "r+")

	while(1):
		buf = fp.readline()
		# print buf
		if not buf:
			break
		pattern = re.compile(r'hacl\(\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)\.') 
		match = pattern.search(buf) 

		if match:
			# print match.groups()[0] 
			ori = match.groups()[0]
			dest = match.groups()[1]
			if dest not in pointDict[ori].link:
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
			if p3 not in subnet[subnetId]:
				subnet[subnetId].append(p3)
			if p3 in withoutnet.keys():
				del withoutnet[p3]

	fp.close()

def computeVerticeImportance():
	buildVertices()
	buildConnectionOrigin()
	getSubnet()
	getAllConnection()
	b = len(pointDict.keys())
	importance = [0 for i in range(b)]
	narray = [[0x3f3f3f3f for i in range(b)] for i in range(b)]
	for key in pointDict.keys():
		for key2 in pointDict[key].link:
			#print pointDict[key2].id, pointDict[key].id
			narray[pointDict[key2].id][pointDict[key].id] = narray[pointDict[key].id][pointDict[key2].id] = 1
	#print narray
	distance = computeDistance(narray)
	#print distance
	for i in range(b):
		n1 = copy.deepcopy(narray)
		#print n1
		for j in range(b):
			n1[i][j] = n1[j][i] = 0x3f3f3f3f
		distance2 = computeDistance(n1)
		tlos = 0
		#print distance2
		for k1 in range(b):
			for k2 in range(b):
				if distance2[k1][k2] == 0x3f3f3f3f and distance[k1][k2] != 0x3f3f3f3f:
					tlos = tlos + 1 / float(distance[k1][k2])
		importance[i] = tlos
	print importance
	#print narray

def computeDistance(narray):
	l = len(pointDict.keys())
	distance = [[0x3f3f3f3f for i in range(l)] for i in range(l)]
	distance = copy.deepcopy(narray)
	#print distance
	for k in range(l):
		for j in range(l):
			for i in range(l):
				if distance[i][j] > distance[i][k] + distance[k][j]:
					 distance[i][j] = distance[i][k] + distance[k][j]
	#print distance
	return distance


def getAllConnection():
	for subID in subnet.keys():
		sub = subnet[subID]
		#print subID
		for n1 in sub:
			for n2 in sub:
				if n1 != n2:
					pointDict[n1].link.append(n2)

def convMetric():
	#for key in pointDict.keys():
		#pointDict[key].printId()

	a = 0.0
	b = len(pointDict.keys())
	print b
	narray =  [[0 for i in range(b)] for i in range(b)]
	used = [0 for i in range(b)]
	for key in pointDict.keys():
		for key2 in pointDict[key].link:
			#print pointDict[key2].id, pointDict[key].id
			narray[pointDict[key2].id][pointDict[key].id] = narray[pointDict[key].id][pointDict[key2].id] = 1

	#print narray
	print used

	for i in range(b):
		if used[i] == 0:
			dfs(used, narray, b, i)
			a = a+1
	#print a

	metric = 10.0 * (1 - (a - 1)/(b - 1))
	print metric

def dfs(used, narray, size, cur):
	used[cur] = 1
	for i in range(size):
		if used[i] == 0 and narray[i][cur] == 1:
			used[i] = 1
			dfs(used, narray, size, i)

def cycleMetric():
	a = 0.0
	b = len(pointDict.keys())
	#print b
	narray =  [[0 for i in range(b)] for i in range(b)]
	dfn = [0 for i in range(b)]
	low = [0 for i in range(b)]
	stack = []
	instack = [0 for i in range(b)]
	for key in pointDict.keys():
		for key2 in pointDict[key].link:
			#print pointDict[key2].id, pointDict[key].id
			narray[pointDict[key].id][pointDict[key2].id] = 1

	#print narray
	#print dfn, low, stack

	index = 0

	for i in range(b):
		if dfn[i] == 0:
			index, a = tarjan(dfn, low, instack, stack, narray, b, 0, index, a)
	#print a
	#print index

	metric = 10.0 * (1 - (a - 1)/(b - 1))
	#print metric

def tarjan(dfn, low, instack, stack, narray, size, cur, index, res):
	index = index + 1
	dfn[cur] = low[cur] = index
	instack[cur] = 1
	stack.append(cur)
	for i in range(size):
		if narray[i][cur] == 1:
			if dfn[i] == 0:
				index, res = tarjan(dfn, low, instack, stack, narray, size, i, index)
				if low[i] < low[cur]:
					low[cur] = low[i]
			else:
				if instack[i] > 0 and dfn[i] < low[cur]:
					low[cur] = dfn[i]

	if dfn[cur] == low[cur]:
		res = res + 1
		j = stack.pop()
		instack[j] = 0
		while j != cur:
			j = stack.pop()
			instack[j] = 0

	return index, res

def printDot(name):
	fp = open(name + ".dot", "w")
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
	os.system('dot -Tpng ' + name + '.dot > ' + name + '.png')

if __name__ == "__main__":
	#buildVertices()
	#buildConnectionOrigin()
	#getSubnet()
	#getAllConnection()
	#cycleMetric()
	#printDot("TopoAttackGraph")
	computeVerticeImportance()
