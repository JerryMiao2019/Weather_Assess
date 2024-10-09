# -*- coding: UTF-8 -*-
import math
import csv
import re

a=[]
with open('over.csv', 'r',encoding='utf-8') as file:
    i = 0
    reader = csv.reader(file)
    for row in reader:
        i=i+1#计算行数
        a.append(row)#向数组中加入数据
    i = int(i/2)
    for j in range(i):
        del a[-i]
    print(a)
    for j in range(i):#转换string到int和float
        for k in range(1,8):
            a[j][k] = float(a[j][k])
            print(j)
            print(k)
                
pts = [list() for k in range(i)]# 生成一个空数组
for k in range(i):  # 初始化pts
    pts[k].append(0)
    pts[k].append(0)
    pts[k].append(0)
    pts[k].append(0)
    pts[k].append(0)
    pts[k].append(0)
for j in range(i):#将天气数据写入pts
    for k in range(6):
        pts[j][k] = a[j][k+2]
#下为KD树
class Node:
    def __init__(self, pt, leftBranch, rightBranch, dimension):
        self.pt = pt
        
        self.leftBranch = leftBranch
        self.rightBranch = rightBranch
        self.dimension = dimension
        
class KDTree():
    def __init__(self, data):
        self.nearestPt = None
        self.nearestDis = math.inf
    def createKDTree(self, currPts, dimension):
        if (len(currPts) == 0):
            return None
        mid = self.calMedium(currPts)
        sortedData = sorted(currPts, key=lambda x: x[dimension])
        leftBranch = self.createKDTree(sortedData[:mid], self.calDimension(dimension))
        rightBranch = self.createKDTree(sortedData[mid + 1:], self.calDimension(dimension))
        return Node(sortedData[mid], leftBranch, rightBranch, dimension)
    def calMedium(self, currPts):
        return len(currPts) // 2
    def calDimension(self, dimension):  # 区别就在于这里，几维就取余几
        #return (dimension + 1) % len(targetPt)
        return (dimension + 1) % 6
    def calDistance(self, p0, p1):
        return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)
    def getNearestPt(self, root, targetPt):
        self.search(root, targetPt)
        return self.nearestPt, self.nearestDis
    def search(self, node, targetPt):
        if node == None:
            return
        dist = node.pt[node.dimension] - targetPt[node.dimension]
        if (dist > 0):  # 目标点在节点的左侧或上侧
            self.search(node.leftBranch, targetPt)
        else:
            self.search(node.rightBranch, targetPt)
        tempDis = self.calDistance(node.pt, targetPt)
        if (tempDis < self.nearestDis):
            self.nearestDis = tempDis
            self.nearestPt = node.pt
        # 回溯
        if (self.nearestDis > abs(dist)):
            if (dist > 0):
                self.search(node.rightBranch, targetPt)
            else:
                self.search(node.leftBranch, targetPt)
                
def find(lookingfor,given):#查找数组中的最小数
    for i in range(len(lookingfor)):
        if given[0] == lookingfor[i][2] and given[1] == lookingfor[i][3] and given[2] == lookingfor[i][4] and given[3] == lookingfor[i][5] and given[4] == lookingfor[i][6] and given[5] == lookingfor[i][7]:
            return lookingfor[i][1]

def main(targetPt):
    kdtree = KDTree(pts)
    root = kdtree.createKDTree(pts, 5)
    pt, minDis = kdtree.getNearestPt(root, targetPt)
    #最近的点是pt，最小距离是str(minDis))
    if find(a, pt) == 0:
        return "优"
    elif find(a, pt) == 1:
        return "良"
    elif find(a, pt) == 2:
        return "轻度污染"
    elif find(a, pt) == 3:
        return "中度污染"
    else:
        return "重度污染"
choose = input("自行输入数据输入1，由文件写入数据输入2\n")
if int(choose) == 1:
    while True:
        temp = input("输入数据，以空格或逗号分隔\n")# 目标点
        targetPt = re.split(r'[;,\s]\s*', temp)
        for i in range(6):
            targetPt[i] = float(targetPt[i])
        print(main(targetPt))
elif int(choose) == 2:
    #while True:
        i = 0
        input_1=[]
        b=[]
        with open('input.csv', 'r',encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                i=i+1#计算行数
                input_1.append(row)#向数组中加入数据
                b.append(row)
        result = [list() for k in range(i)]
        for k in range(i):  # 生成一个空数组
            result[k].append(0)
            result[k].append(0)
        print(result)
        for j in range(i):#转换string到int和float
            result[j][0] = input_1[j][0]
            for k in range(1,7):
                input_1[j][k] = float(input_1[j][k])
                #if k ==5:
                b[j][k] = float(b[j][k])
        for j in range(i):
            del b[j][0]
            result[j][1] = main(b[j])
        print(result)
        f = open('result.csv', 'w',encoding='utf-8')
        with f:
            writer = csv.writer(f)
            for row in result:
                writer.writerow(row)



