#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import numpy
from numpy import *

verticeSet = {}
impactLoss = []
impactPoss = []

class vertices:
	id = 0
	prob = -1

	def __init__(self, id, prob, status, exet):
		if (status == 'LEAF'):
			self.prob = prob
		self.status = status
		self.exet = exet
		self.id = id
		self.list = []

	def print_v(self):
		print self.id
		print self.status
		print self.prob
		print self.exet
		print self.list

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

		verticeSet[id] = vertices(id, prob, status, exet)

	fp.close()

	fp = open("ARCS.CSV", "r+")

	while 1:
		buf = fp.readline().split(',')
		#print buf
		if(buf[0] == ''):
			break

		verticeSet[int(buf[0])].list.append(int(buf[1]))

	fp.close()

def fetchNoProb():
	for key in verticeSet.keys():
		if (verticeSet[key].prob == -1):
			return verticeSet[key]
	return 

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

def metric(node):
	if(node.prob!=-1):
		return node.prob
	if(node.status=="OR"):
		prob=1
		for h in node.list:
			if(verticeSet[h].exet.split('(')[0] == 'vulExists'):
				vulID = verticeSet[h].exet.split("'")[1]
				vulData = getVulInfo(vulID)
				loss, poss = calcVunPoss(vulData)
			else:
				poss = 1
				loss = 0
			prob=prob*(1-metric(verticeSet[h])*poss)
		node.prob=1-prob
		if (loss > 0):
			impactLoss.append([loss])
			impactPoss.append([node.prob])
		return node.prob
	if(node.status=="AND"):
		prob=1
		for h in node.list:
			if(verticeSet[h].exet.split('(')[0] == 'vulExists'):
				vulID = verticeSet[h].exet.split("'")[1]
				vulData = getVulInfo(vulID)
				loss, poss = calcVunPoss(vulData)
			else:
				poss = 1
				loss = 0
			prob=prob*metric(verticeSet[h])*poss
		node.prob=prob*0.8
		if (loss > 0):
			impactLoss.append([loss])
			impactPoss.append([node.prob])
		return node.prob

def calcPossbility():
	while 1:
		temp=fetchNoProb()
		if temp is None:
			break
		temp.prob=metric(temp)

	arrLoss = array(impactLoss)
	arrPoss = array(impactPoss)
	arrPoss /= arrPoss.sum()
	print arrLoss
	print arrPoss
	a = impactLoss * arrPoss
	print a

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

if __name__ == "__main__":
	#getVulInfo('CVE-2003-0012')
    readVertices()
    calcPossbility()
    writeCSV()