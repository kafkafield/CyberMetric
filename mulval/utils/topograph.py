#!/usr/bin/python
# -*- coding: UTF-8 -*-

from random import random, choice

import matplotlib as mpl
mpl.use('agg')   # generate postscript output by default

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes

import MySQLdb
import numpy
from numpy import *
import re
import os
import sys
import copy
import Queue

verticeSet = {}
impactLoss = []
impactPoss = []
pointDict = {}
subnet = {}
withoutnet = {}
vunInfo = {}

class verticesAttack:
	id = 0
	prob = -1

	def __init__(self, id, prob, status, exet):
		if (status == 'LEAF'):
			self.prob = prob
		self.status = status
		self.exet = exet
		self.id = id
		self.list = []
		self.list2 = []

	def print_v(self):
		print self.id
		print self.status
		print self.prob
		print self.exet
		print self.list
		print self.list2

class vertices:
	resource = 1
	subnet

	def __init__(self, id):
		self.link2 = []
		self.link = []
		self.id = id

	def loadImport(self, ip):
		self.importance(ip)

	def printId(self):
		print self.id
		print self.link
		print self.link2
		print self.resource

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
				pointDict[dest].link2.append(ori)
				withoutnet[dest].link2.append(ori)

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
				pointDict[dest].link2.append(ori)
				#withoutnet[ori].link.append(dest)

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
			print subnetId
			if subnetId not in subnet.keys():
				subnet[subnetId] = []
			if p3 not in subnet[subnetId]:
				subnet[subnetId].append(p3)
				pointDict[p3].subnet = subnetId
			if p3 in withoutnet.keys():
				del withoutnet[p3]

	fp.close()

	for i in withoutnet.keys():
		pointDict[i].subnet = 'NONE'

def computeVerticeImportance(subnetName):
	buildVertices()
	buildConnectionOrigin()
	getSubnet()
	getAllConnection()
	b = len(subnet[subnetName])
	importance = [0 for i in range(b)]
	narray = [[0x3f3f3f3f for i in range(b)] for i in range(b)]
	for key in Subnet[subnetName]:
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
	#print importance
	return importance
	#print narray

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
	#print importance
	return importance
	#print narray

def distance(a):
	r = 0
	for l in a:
		r = r + pow(l, 2)
	return sqrt(r)

def getAllVun():
	fp = open("h2v1s5.P", "r+") # remember the name!!
	pattern2 = re.compile(r'vulExists\(\s*(\w+),\s*\'(.+)\',\s*(\w+)\)\.')

	id = 1
	while 1:
		buf = fp.readline()
		# print buf
		if not buf:
			break
		match2 = pattern2.search(buf)
		if match2:
			server = match2.groups()[0]
			vun = match2.groups()[1]
			serverId = pointDict[server]
			if serverId.id not in vunInfo.keys():
				vunInfo[serverId.id] = []
			if vun not in vunInfo[serverId.id]:
				vunInfo[serverId.id].append(vun)

	fp.close()

def testD(a):
	r = 0
	for l in a:
		#r = r + pow(l, 2)
		r = r + l
	print r

def importanceMetric(importance):
	importance = importance / distance(importance)
	#print importance
	#testD(importance)
	getAllVun()
	#print vunInfo
	for i in range(len(importance)):
		impact = 0
		if i in vunInfo.keys():
			for k in vunInfo[i]:
				#print k
				vulData = getVulInfo(k)
				#print vulData
				loss, poss = calcVunPoss(vulData)
				#print loss
				impact = impact + loss
				if i == 29:
					print loss
		if impact > 10:
			impact = 10
		#print impact
		importance[i] = pow(importance[i],2) * impact
	metric = 0
	for a in importance:
		metric = metric + a
	print metric
	return metric

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
	#print b
	narray =  [[0 for i in range(b)] for i in range(b)]
	used = [0 for i in range(b)]
	for key in pointDict.keys():
		for key2 in pointDict[key].link:
			#print pointDict[key2].id, pointDict[key].id
			narray[pointDict[key2].id][pointDict[key].id] = narray[pointDict[key].id][pointDict[key2].id] = 1

	#print narray
	#print used

	for i in range(b):
		if used[i] == 0:
			dfs(used, narray, b, i)
			a = a+1
	#print a

	metric = 10.0 * (1 - (a - 1)/(b - 1))
	print metric
	return metric

def convMetricSubnet(subnetName):
	tarSubnet = subnet[subnetName]
	a = 0.0
	b = len(tarSubnet)
	narray =  [[0 for i in range(b)] for i in range(b)]
	used = [0 for i in range(b)]
	for k in tarSubnet:
		for key2 in pointDict[k].link:
			if key2 in tarSubnet:
				narray[tarSubnet.index(k)][tarSubnet.index(key2)] = narray[tarSubnet.index(key2)][tarSubnet.index(k)] = 1

	for i in range(b):
		if used[i] == 0:
			dfs(used, narray, b, i)
			a = a+1
	#print a

	metric = 10.0 * (1 - (a - 1)/(b - 1))
	print metric
	return metric

def convMetricHost(pointName):
	if pointName in pointDict[pointName].link:
		metric = 10
	else:
		metric = 0

	print metric
	return metric

def dfs(used, narray, size, cur):
	used[cur] = 1
	for i in range(size):
		if used[i] == 0 and narray[i][cur] == 1:
			used[i] = 1
			dfs(used, narray, size, i)

def cycleMetric():
	#for i in pointDict.keys():
	#	print i
	#	pointDict[i].printId()
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

	#print narray[29][28]
	#print narray[28][29]
	#print dfn, low, stack

	index = 0

	for i in range(b):
		if dfn[i] == 0:
			#print dfn[28]
			index, a = tarjan(dfn, low, instack, stack, narray, b, i, index, a)
			#print dfn[28]
	#print a
	#print b
	#print index

	metric = 10.0 * (1 - (a - 1)/(b - 1))
	print metric
	return metric

def cycleMetricSubnet(subnetName):
	tarSubnet = subnet[subnetName]
	a = 0.0
	b = len(tarSubnet)
	narray =  [[0 for i in range(b)] for i in range(b)]
	dfn = [0 for i in range(b)]
	low = [0 for i in range(b)]
	stack = []
	instack = [0 for i in range(b)]
	for k in tarSubnet:
		for key2 in pointDict[k].link:
			if key2 in tarSubnet:
				narray[tarSubnet.index(k)][tarSubnet.index(key2)] = 1

	index = 0

	for i in range(b):
		if dfn[i] == 0:
			index, a = tarjan(dfn, low, instack, stack, narray, b, i, index, a)
	#print a

	metric = 10.0 * (1 - (a - 1)/(b - 1))
	print metric
	return metric

def cycleMetricHost(pointName):
	metric = convMetric(pointName)
	print metric
	return metric

def tarjan(dfn, low, instack, stack, narray, size, cur, index, res):
	index = index + 1
	dfn[cur] = low[cur] = index
	instack[cur] = 1
	stack.append(cur)
	for i in range(size):
		#f (i == 29 and cur == 28) or (i == 28 and cur == 29):
			#print 'haha'
		if narray[cur][i] == 1:
			if dfn[i] == 0:
				index, res = tarjan(dfn, low, instack, stack, narray, size, i, index, res)
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
		if key == "internet":
			seq.append('t' + str(pointDict[key].id) + ' [label="' + key + '",shape=none,image="/Users/Saint/Code/CyberMetric/mulval/img/internet.jpeg"];\n')
		else:
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

def readVertices():
	fp = open("VERTICES.CSV", "r+")

	while 1:
		buf = fp.readline().split(',"')
		#print buf
		if(buf[0] == ''):
			break

		id = int(buf[0])
		buf2 = buf[2].split('",')
		prob = float(buf2[1].strip('\n'))
		status = buf2[0]
		exet = buf[1].strip('"')

		verticeSet[id] = verticesAttack(id, prob, status, exet)

	fp.close()

	fp = open("ARCS.CSV", "r+")

	while 1:
		buf = fp.readline().split(',')
		#print buf
		if(buf[0] == ''):
			break

		verticeSet[int(buf[0])].list.append(int(buf[1]))
		verticeSet[int(buf[1])].list2.append(int(buf[0]))

	fp.close()

def fetchNoProb():
	for key in verticeSet.keys():
		if (verticeSet[key].prob == -1):
			return verticeSet[key], key
	return None, None

def calcVunPoss(vulData):
	av = {}
	au = {}
	ac = {}
	ci = {}
	ii = {}
	ai = {}

	av['L'] = 0.395
	av['A'] = 0.646
	av['N'] = 1.0

	au['M'] = 0.45
	au['S'] = 0.56
	au['N'] = 0.704

	ac['H'] = 0.35
	ac['M'] = 0.61
	ac['L'] = 0.71

	ci['N'] = 0.00
	ci['P'] = 0.275
	ci['C'] = 0.66

	ii['N'] = 0.00
	ii['P'] = 0.275
	ii['C'] = 0.66

	ai['N'] = 0.00
	ai['P'] = 0.275
	ai['C'] = 0.66

	poss = av[vulData[6]] * au[vulData[7]] * ac[vulData[8]]

	loss = 10.41 * (1 - (1 - ci[vulData[9]]) * (1 - ii[vulData[10]]) * (1 - ai[vulData[11]]))

	return loss, poss

def metric(node, key, used):
	used[key] = 1
	if(node.prob!=-1):
		return node.prob
	if(node.status=="OR"):
		prob=1
		for h in node.list:
			loss = 0
			if h not in used.keys():
				if(verticeSet[h].exet.split('(')[0] == 'vulExists'):
					vulID = verticeSet[h].exet.split("'")[1]
					vulData = getVulInfo(vulID)
					loss, poss = calcVunPoss(vulData)
				else:
					poss = 1
					loss = 0
				#print h
				prob=prob*(1-metric(verticeSet[h], h, used)*poss)
		node.prob=1-prob
		if (loss > 0):
			impactLoss.append([loss])
			impactPoss.append([node.prob])
		del used[key]
		return node.prob
	if(node.status=="AND"):
		prob=1
		for h in node.list:
			loss = 0
			if h not in used.keys():
				if(verticeSet[h].exet.split('(')[0] == 'vulExists'):
					vulID = verticeSet[h].exet.split("'")[1]
					vulData = getVulInfo(vulID)
					loss, poss = calcVunPoss(vulData)
				else:
					poss = 1
					loss = 0
				#print h
				prob=prob*metric(verticeSet[h], h, used)*poss
		node.prob=prob*0.8
		if (loss > 0):
			impactLoss.append([loss])
			impactPoss.append([node.prob])
		del used[key]
		return node.prob

def calcPossbility():
	used = {}
	while 1:
		temp, tempKey=fetchNoProb()
		if temp is None:
			break
		temp.prob=metric(temp, tempKey, used)

	arrLoss = array(impactLoss)
	arrPoss = array(impactPoss)
	arrPoss /= arrPoss.sum()
	#print arrLoss
	#print arrPoss
	a = impactLoss * arrPoss
	#print a
	metricP = 0
	for i in a:
		for j in i:
			metricP = metricP + j
	print metricP
	return metricP

def metricSubnet(node, key, used, subnetName):
	used[key] = 1
	if(node.prob!=-1):
		return node.prob
	if(node.status=="OR"):
		prob=1
		for h in node.list:
			loss = 0
			if h not in used.keys():
				if(verticeSet[h].exet.split('(')[0] == 'vulExists'):
					vulID = verticeSet[h].exet.split("'")[1]
					host = verticeSet[h].exet.split(",")[0].split("(")[1]
					if host in subnet[subnetName]:
						vulData = getVulInfo(vulID)
						loss, poss = calcVunPoss(vulData)
					else:
						poss = 1
						loss = 0
				else:
					poss = 1
					loss = 0
				#print h
				prob=prob*(1-metric(verticeSet[h], h, used)*poss)
		node.prob=1-prob
		if (loss > 0):
			impactLoss.append([loss])
			impactPoss.append([node.prob])
		del used[key]
		return node.prob
	if(node.status=="AND"):
		prob=1
		for h in node.list:
			loss = 0
			if h not in used.keys():
				if(verticeSet[h].exet.split('(')[0] == 'vulExists'):
					vulID = verticeSet[h].exet.split("'")[1]
					vulData = getVulInfo(vulID)
					loss, poss = calcVunPoss(vulData)
				else:
					poss = 1
					loss = 0
				#print h
				prob=prob*metric(verticeSet[h], h, used)*poss
		node.prob=prob*0.8
		if (loss > 0):
			impactLoss.append([loss])
			impactPoss.append([node.prob])
		del used[key]
		return node.prob

def poMetricSubnet(subnetName):
	used = {}
	while 1:
		temp, tempKey=fetchNoProb()
		if temp is None:
			break
		temp.prob=metricSubnet(temp, tempKey, used, subnetName)

	arrLoss = array(impactLoss)
	arrPoss = array(impactPoss)
	arrPoss /= arrPoss.sum()
	#print arrLoss
	#print arrPoss
	a = impactLoss * arrPoss
	#print a
	metricP = 0
	for i in a:
		for j in i:
			metricP = metricP + j
	print metricP
	return metricP

def metricHost(node, key, used, hostName):
	used[key] = 1
	if(node.prob!=-1):
		return node.prob
	if(node.status=="OR"):
		prob=1
		for h in node.list:
			loss = 0
			if h not in used.keys():
				if(verticeSet[h].exet.split('(')[0] == 'vulExists'):
					vulID = verticeSet[h].exet.split("'")[1]
					host = verticeSet[h].exet.split(",")[0].split("(")[1]
					if host == hostName:
						vulData = getVulInfo(vulID)
						loss, poss = calcVunPoss(vulData)
					else:
						poss = 1
						loss = 0
				else:
					poss = 1
					loss = 0
				#print h
				prob=prob*(1-metric(verticeSet[h], h, used)*poss)
		node.prob=1-prob
		if (loss > 0):
			impactLoss.append([loss])
			impactPoss.append([node.prob])
		del used[key]
		return node.prob
	if(node.status=="AND"):
		prob=1
		for h in node.list:
			loss = 0
			if h not in used.keys():
				if(verticeSet[h].exet.split('(')[0] == 'vulExists'):
					vulID = verticeSet[h].exet.split("'")[1]
					vulData = getVulInfo(vulID)
					loss, poss = calcVunPoss(vulData)
				else:
					poss = 1
					loss = 0
				#print h
				prob=prob*metric(verticeSet[h], h, used)*poss
		node.prob=prob*0.8
		if (loss > 0):
			impactLoss.append([loss])
			impactPoss.append([node.prob])
		del used[key]
		return node.prob

def poMetricHost(hostName):
	used = {}
	while 1:
		temp, tempKey=fetchNoProb()
		if temp is None:
			break
		temp.prob=metricHost(temp, tempKey, used, hostName)

	arrLoss = array(impactLoss)
	arrPoss = array(impactPoss)
	arrPoss /= arrPoss.sum()
	#print arrLoss
	#print arrPoss
	a = impactLoss * arrPoss
	#print a
	metricP = 0
	for i in a:
		for j in i:
			metricP = metricP + j
	print metricP
	return metricP

def test():
	for key in verticeSet.keys():
		verticeSet[key].print_v()

def writeCSV():
	fp = open("VERTICES_P.CSV", "w")

	seq = []
	for key in verticeSet.keys():
		temp = verticeSet[key]
		seq.append(str(temp.id) + ',"' + temp.exet + '","' + temp.status + '",' + str(temp.prob) + '\n')

	fp.writelines(seq)

	fp.close()

def initDB():
	fp = open("config.txt","r+")

	url_list = fp.readline().split('/')[2].split(':')
	url = url_list[0]
	#print url
	port = int(url_list[1])
	#print port
	userName = fp.readline().strip('\n')
	# print userName
	password = fp.readline().strip('\n')
	# print password

	fp.close()

	# 打开数据库连接
	db = MySQLdb.connect(url,userName,password,"nvd",port)

	return db

def getVulInfo(vulName):
	db = initDB()
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# 使用execute方法执行SQL语句
	sql = "SELECT * FROM nvd \
       WHERE id = '%s'" % (vulName)
	try:
		cursor.execute(sql)

		# 使用 fetchone() 方法获取一条数据库。
		data = cursor.fetchone()
		#print data[5]
	except:
		print "Failed!"

	# 关闭数据库连接
	db.close()

	return data

def getResource():
	fp = open("h2v1s5.P", "r+") # remember the name!!
	pattern2 = re.compile(r'hasResource\(\s*(\w+),\s*(\w+)\)\.')

	id = 1
	while 1:
		buf = fp.readline()
		# print buf
		if not buf:
			break
		match2 = pattern2.search(buf)
		if match2:
			server = match2.groups()[0]
			source = match2.groups()[1]
			pointDict[server].resource = int(source)
			#print source

	fp.close()

def fixResource():
	for k in pointDict.keys():
		pattern = re.compile(r'.*fileServer.*')
		pattern2 = re.compile(r'.*DNSServer.*')
		pattern3 = re.compile(r'.*controlServer.*')
		pattern4 = re.compile(r'.*dmz.*')

		match = pattern.search(k)
		match2 = pattern2.search(k)
		match3 = pattern3.search(k)
		match4 = pattern4.search(k)

		if match:
			pointDict[k].resource = pointDict[k].resource + 3.094
		if match2:
			pointDict[k].resource = pointDict[k].resource + 2.072
		if match3:
			pointDict[k].resource = pointDict[k].resource + 5.348
		if match4:
			pointDict[k].resource = pointDict[k].resource - 1.913

		if pointDict[k].resource < 0:
			pointDict[k].resource = 0
		if pointDict[k].resource > 10:
			pointDict[k].resource = 10

def testPointDict():
	for i in pointDict.keys():
		pointDict[i].printId()

def reVulMetric():
	getAllVun()
	getResource()
	fixResource()
	reImportance = [0 for i in range(len(pointDict))]
	temp = {}
	for i in pointDict.keys():
		#print pointDict[i].resource
		reImportance[pointDict[i].id] = pointDict[i].resource
	print reImportance
	reImportance = reImportance / distance(reImportance)
	for i in range(len(reImportance)):
		impact = 0
		if i in vunInfo.keys():
			for k in vunInfo[i]:
				#print k
				vulData = getVulInfo(k)
				#print vulData
				loss, poss = calcVunPoss(vulData)
				#print loss
				impact = impact + loss
		if impact > 10:
			impact = 10
		#print impact
		reImportance[i] = pow(reImportance[i],2) * impact
	metric = 0
	for a in reImportance:
		metric = metric + a
	print metric
	return metric

def reVulMetricSubnet(subnetName):
	tarSubnet = subnet[subnetName]
	getAllVun()
	getResource()
	fixResource()
	reImportance = [0 for i in range(len(tarSubnet))]
	temp = {}
	for i in tarSubnet:
		#print pointDict[i].resource
		reImportance[tarSubnet.index(i)] = pointDict[i].resource
	print reImportance
	reImportance = reImportance / distance(reImportance)
	for i in tarSubnet:
		impact = 0
		if i in vunInfo.keys():
			for k in vunInfo[i]:
				#print k
				vulData = getVulInfo(k)
				#print vulData
				loss, poss = calcVunPoss(vulData)
				#print loss
				impact = impact + loss
		if impact > 10:
			impact = 10
		#print impact
		reImportance[tarSubnet.index(i)] = pow(reImportance[tarSubnet.index(i)],2) * impact
	metric = 0
	for a in reImportance:
		metric = metric + a
	print metric
	return metric

def reVulMetricHost(pointName):
	metric = pointDict[pointName].resource
	print metric
	return metric

def findAttackLocated():
	located = []
	for i in verticeSet.keys():
		#verticeSet[i].print_v()
		pattern = re.compile(r'.*attackerLocated\(internet\).*')
		match = pattern.search(verticeSet[i].exet)
		#print verticeSet[i].exet
		if match:
			located.append(i)
	return located

def deepReMetric():
	depth = [0 for i in range(len(pointDict))]
	searchlist = Queue.Queue(2000)
	reImportance = [0 for i in range(len(pointDict))]
	readVertices()
	located = findAttackLocated()
	for init in located:
		used = {}
		#print init
		temp = {}
		temp[init] = 0
		used[init] = 1
		searchlist.put(init)
		while not searchlist.empty():
			a = searchlist.get()
			#print a
			step = temp[a] + 1
			#print verticeSet[a].list2
			for i in verticeSet[a].list2:
				#print a
				#print i
				if not i in used.keys():
					temp[i] = step
					searchlist.put(i)
					#if i == 378:
					#	print 'nihao '
					pattern = re.compile(r'.*\((.*)\).*')
					if verticeSet[i].status == 'OR':
						#print verticeSet[i].exet
						match = pattern.search(verticeSet[i].exet)
						if match:
							host = match.groups()[0].split(',')[0]
							depth[pointDict[host].id] = 1/float(temp[i])
					used[i] = 1
	#print depth
	depth = depth / distance(depth)
	getResource()
	fixResource()
	reImportance = [0 for i in range(len(pointDict))]
	temp = {}
	for i in pointDict.keys():
		reImportance[pointDict[i].id] = pointDict[i].resource
	#reImportance = reImportance / distance(reImportance)
	#print reImportance
	metric = 0
	#print reImportance
	#print depth
	for i in range(len(pointDict)):
		metric = metric + pow(depth[i], 2) * reImportance[i]
	print metric
	return metric

def outInMetric():
	a = 0.0
	b = 0
	for i in pointDict.keys():
		for k in pointDict[i].link:
			if pointDict[i].subnet == 'NONE' or pointDict[k].subnet == 'NONE' or pointDict[i].subnet != pointDict[k].subnet:
				a = a + 1
			b = b + 1
	metric = 10 * a / b
	print metric
	return metric

def outInMetricSubnet(subnetName):
	a = 0.0
	b = 0
	for i in pointDict.keys():
		for k in pointDict[i].link:
			if k != i:
				a = a + 1
			b = b + 1
	metric = 10 * a / b
	print metric
	return metric

def outInMetricHost(hostName):
	a = 0.0
	b = 0
	for i in pointDict.keys():
		for k in pointDict[i].link:
			if k != i:
				a = a + 1
			b = b + 1
	metric = 10 * a / b
	print metric
	return metric

def cMetric():
	a = 0.0
	b = len(pointDict)
	for i in pointDict.keys():
		if len(pointDict[i].link2) > 0:
			a = a + 1
	metric = 10 * a / b
	print metric
	return metric

def cMetricSubnet(subnetName):
	a = 0.0
	b = len(Subnet[subnetName])
	for i in Subnet[subnetName]:
		if len(pointDict[i].link2) > 0:
			a = a + 1
	metric = 10 * a / b
	print metric
	return metric

def cMetricHost(hostName):
	a = 0.0
	b = 1
	if pointDict[hostName].link2 > 0:
		a = 1
	metric = 10 * a / b
	print metric
	return metric

def metricHost(hostName):
	buildVertices()
	buildConnection()
	getSubnet()
	printDot("TopoAttackGraph")

def metricSubnet(subnetName):
	buildVertices()
	buildConnection()
	getSubnet()
	printDot("TopoAttackGraph")
	Mw = convMetricSubnet(subnetName)
	Ms = cycleMetricSubnet(subnetName)

	Mr = reVulMetricSubnet(subnetName)

	Mp = poMetricSubnet(subnetName)

	Mo = outInMetric(subnetName)
	Md = deepReMetric(subnetName)

def metricAll():
	buildVertices()
	buildConnection()
	getSubnet()
	printDot("TopoAttackGraph")
	Mw = convMetric()
	Ms = cycleMetric()

	Mo = outInMetric()
	Mc = cMetric()

	#readVertices()
	Mr = reVulMetric()
	Md = deepReMetric()

	#pointDict = {}
	#subnet = {}
	#withoutnet = {}
	buildVertices()
	#print pointDict
	#print withoutnet
	buildConnectionOrigin()
	getSubnet()
	getAllConnection()
	importance = computeVerticeImportance()
	Mi = importanceMetric(importance)
	Mp = calcPossbility()
	#writeCSV()
	metricResult = [[0 for i in range(2)] for i in range(4)]
	metricResult[0][0] = Mw
	metricResult[0][1] = Ms
	metricResult[1][0] = Mr
	metricResult[1][1] = Md
	metricResult[2][0] = Mp
	metricResult[2][1] = Mi
	metricResult[3][0] = Mo
	metricResult[3][1] = Mc

	return metricResult

def makeplot(metriclist, filename):
	mpl.rcParams['font.size'] = 10
	fig = plt.figure()

	#plot_extents = 0, 10, 0, 10
	#transform = Affine2D().rotate_deg(45)
	#helper = floating_axes.GridHelperCurveLinear(transform, plot_extents)
	#axis = floating_axes.FloatingSubplot(fig, 111, grid_helper=helper)

	ax = fig.add_subplot(111, projection='3d')

	# compute two-dimensional histogram
	#hist, xedges, yedges = np.histogram2d(x, y, bins=10)

	for z in [1, 2, 3, 4]:
	     xs = xrange(1,3)
	     ys = metriclist[z - 1]

	     color =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	     ax.bar(xs, ys, zs=z, zdir='y', color=color, alpha=0.8, width=0.4)
	     #ax.ylim(0,40)

	ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(xs))
	ax.yaxis.set_major_locator(mpl.ticker.FixedLocator(ys))

	ax.set_xlabel('Dimension')
	ax.set_ylabel('Layer')
	ax.set_zlabel('Metric')
	ax.set_xticks((0,1),(u'D1',u'D2'))
	ax.set_zlim(0,10)

	plt.savefig(filename)
	plt.show()

def autolabel(rects): 
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/3., 1.03*height, '%s' % float(height))

def makeDetailPlot(m, filename):
	#mpl.rcParams['font.sans-serif'] = ['SimSun'] #指定默认字体  
	#mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题  
	fig = plt.figure()
	ax = fig.add_subplot(111)
	color =(0.76655134032754335, 0.72392158508300786, 0.6619146683636834, 1.0)#plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color2 =(0.83790850639343251, 0.62274512052536024, 0.64862746397654203, 1.0)
	index = np.arange(4)
	bar_width = 0.35
	opacity = 0.8
	r1 = plt.bar(index, (m[0][0], m[1][0], m[2][0], m[3][0]), bar_width,alpha=opacity, color=color,label='Dimension1')#,align='center')
	r2 = plt.bar(index+bar_width, (m[0][1], m[1][1], m[2][1], m[3][1]), bar_width,alpha=opacity, color=color2,label='Dimension2')
	plt.title('Metric Detail')
	plt.xlabel('Layer')
	plt.ylabel('Metric Score')
	plt.ylim(0,10)
	plt.xticks((0.5,1.5,2.5,3.5),(u'Network Node',u'Resources',u'Configuration',u'Performance'))
	plt.legend()
	#plt.xticks((0,1),(u'D1',u'D2'))
	plt.savefig(filename+"detail.png")
	plt.show()

	fig2 = plt.figure()
	ax2 = fig.add_subplot(111)
	index = np.arange(2)
	bar_width = 0.5
	color3 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color4 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color5 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color6 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	r1 = plt.bar(index, (m[0][0], m[0][1]), bar_width,alpha=opacity, color=color3,label='Dimension1')
	plt.title('Metric Detail')
	plt.xlabel('Dimension')
	plt.ylabel('Metric Score')
	plt.ylim(0,10)
	autolabel(r1)
	plt.savefig(filename+"network.png")
	plt.show()
	#print color3

	fig3 = plt.figure()
	ax3 = fig.add_subplot(111)
	index = np.arange(2)
	bar_width = 0.5
	color3 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color4 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color5 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color6 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	r1 = plt.bar(index, (m[1][0], m[1][1]), bar_width,alpha=opacity, color=color4,label='Dimension1')
	plt.title('Metric Detail')
	plt.xlabel('Dimension')
	plt.ylabel('Metric Score')
	plt.ylim(0,10)
	autolabel(r1)
	plt.savefig(filename+"resource.png")
	plt.show()

	fig4 = plt.figure()
	ax4 = fig.add_subplot(111)
	index = np.arange(2)
	bar_width = 0.5
	color3 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color4 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color5 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color6 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	r1 = plt.bar(index, (m[2][0], m[2][1]), bar_width,alpha=opacity, color=color5,label='Dimension1')
	plt.title('Metric Detail')
	plt.xlabel('Dimension')
	plt.ylabel('Metric Score')
	plt.ylim(0,10)
	autolabel(r1)
	plt.savefig(filename+"configuration.png")
	plt.show()

	fig5 = plt.figure()
	ax5 = fig.add_subplot(111)
	index = np.arange(2)
	bar_width = 0.5
	color3 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color4 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color5 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	color6 =plt.cm.Set2(choice(xrange(plt.cm.Set2.N)))
	r1 = plt.bar(index, (m[3][0], m[3][1]), bar_width,alpha=opacity, color=color6,label='Dimension1')
	plt.title('Metric Detail')
	plt.xlabel('Dimension')
	plt.ylabel('Metric Score')
	plt.ylim(0,10)
	autolabel(r1)
	plt.savefig(filename+"performance.png")
	plt.show()

if __name__ == "__main__":
	#m = metricAll()
	#makeplot(m, '3dresult.png')
	#makeDetailPlot(m, 'h5v1s5')
	if len(sys.argv) == 1:
		print "please enter the granularity!"
		exit(0)
	#getVulInfo('CVE-2003-0012')
	else:
		if sys.argv[1] == '-g' or sys.argv[1] == '--global':
			m = metricAll()
			print m
			makeplot(m, '3dresult.png')
			makeDetailPlot(m, 'h5v1s5')
		if sys.argv[1] == '-s' or sys.argv[1] == '--subnet':
			if len(sys.argv) == 2:
				print "please enter the subnet name!"
				exit(0)
			metricSubnet(sys.argv[2])
		if sys.argv[1] == '-h' or sys.argv[1] == '--host':
			if len(sys.argv) == 2:
				print "please enter the host name!"
				exit(0)
			metricHost(sys.argv[2])
		if sys.argv[1] == '-d' or sys.argv[1] == '--draw':
			buildVertices()
			buildConnectionOrigin()
			getSubnet()
			getAllConnection()
			printDot("originnet")
		if sys.argv[1] == '-w' or sys.argv[1] == '--wayto':
			buildVertices()
			buildConnection()
			getSubnet()
			printDot("TopoAttackGraph")
    #writeCSV()

	#buildVertices()
	#buildConnection()
	#buildConnectionOrigin()
	#getSubnet()
	#getAllConnection()
	#convMetric()
	#printDot("TopoAttackGraph")
	#importance = computeVerticeImportance()
	#importanceMetric(importance)
	#getResource()
	#reVulMetric()
	#deepReMetric()
	#outInMetric()
	#cMetric()