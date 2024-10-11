# -*- coding: UTF-8 -*-
import csv
import re

a=[]
with open('data.csv', 'r',encoding="utf-8") as file:
    i = 0
    reader = csv.reader(file)
    for row in reader:
        i=i+1#计算行数
        a.append(row)#向数组中加入数据
    for j in range(i):#转换string到int和float
        for k in range(1,8):
            a[j][k] = float(a[j][k])
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
class KDNode():

    def __init__(self, point=None, split=None, leftNode=None, rightNode=None):
        self.point = point
        self.leftNode = leftNode
        self.rightNode = rightNode
        # 划分维度 当前节点是通过哪一个维度来划分
        self.split = split

    def __str__(self):
        return f'point={self.point}'


class KDTree():
    def __init__(self, data_list):
        # k-d算法维度
        self.dimension = len(data_list[0])
        self.root = self.createKDTree(data_list)

    def createKDTree(self, data_list, n=0):
        """
        将列表数据构建成k-d树
        :param data_list:
        :param n:
        :return:
        """
        length = len(data_list)
        if length == 0:
            return
        # 通过层数计算划分维度
        split = n % self.dimension
        # 排序
        data_list = sorted(data_list, key=lambda x: x[split])
        # 获取中间点
        split_point = data_list[length // 2]
        # 创建节点
        root = KDNode(split_point, split)
        # 递归创建左子树
        root.leftNode = self.createKDTree(data_list[0:length // 2], n + 1)
        # 递归创建右子树
        root.rightNode = self.createKDTree(data_list[length // 2 + 1:], n + 1)

        return root

    def calDistance(self, p1, p2):
        """
        计算维度距离
        :param p1:
        :param p2:
        :return:
        """
        sum = 0.0
        for i in range(len(p1)):
            sum += (p1[i] - p2[i]) ** 2
        return sum ** 0.5

    def KNN(self, query, k):
        # 存储最近的K个点
        node_k = []
        # k个点到目标点的距离
        node_dist = []
        # 存储回溯的父节点
        node_list = []
        # 从根节点开始遍历
        temp_root = self.root
        while temp_root:
            # 保存所有有访问过的父节点
            node_list.append(temp_root)
            # 计算距离
            dist = self.calDistance(query, temp_root.point)
            # 若不足K个, 直接添加
            if len(node_k) < k:
                node_dist.append(dist)
                node_k.append(temp_root.point)
            else:
                # 获取最大距离
                max_dist = max(node_dist)
                # 获取最大距离
                if dist < max_dist:
                    # 已经满足D个 删掉最大值 将整个值补充进去
                    idx = node_dist.index(max_dist)
                    del (node_k[idx])
                    del (node_dist[idx])
                    node_dist.append(dist)
                    node_k.append(temp_root.point)
            split = temp_root.split
            # 找到最靠近的叶节点
            if query[split] <= temp_root.point[split]:
                temp_root = temp_root.leftNode
            else:
                temp_root = temp_root.rightNode
        # 回溯访问父节点,另一个父节点的子节点中可能存在更近的点
        while node_list:
            back_point = node_list.pop()
            split = back_point.split
            max_dist = max(node_dist)
            # 若满足进入该父节点的另外一个子节点的条件
            if len(node_k) < k or abs(query[split] - back_point.point[split]) < max_dist:
                # 进入另外一个子节点
                if query[split] <= back_point.point[split]:
                    temp_root = back_point.rightNode
                else:
                    temp_root = back_point.leftNode
                # 若不为空
                if temp_root:
                    node_list.append(temp_root)
                    # 计算距离
                    calDist = self.calDistance(temp_root.point, query)
                    if max_dist > calDist and len(node_k) == k:
                        # 已经满足D个 删掉最大值 将整个值补充进去
                        idx = node_dist.index(max_dist)
                        del (node_k[idx])
                        del (node_dist[idx])
                        node_dist.append(calDist)
                        node_k.append(temp_root.point)
                    # 不足K个元素 直接添加
                    elif len(node_k) < k:
                        node_dist.append(calDist)
                        node_k.append(temp_root.point)
        # 返回搜索到的点和距离
        return node_k + node_dist

def find(lookingfor,given):#查找数组中的匹配值
    for i in range(len(lookingfor)):
        if given[0] == lookingfor[i][2] and given[1] == lookingfor[i][3] and given[2] == lookingfor[i][4] and given[3] == lookingfor[i][5] and given[4] == lookingfor[i][6] and given[5] == lookingfor[i][7]:
            return lookingfor[i][1]

def main(targetPt):
    find_data = []
    find_data.append(0)
    find_data.append(0)
    find_data.append(0)
    k = 3
    tree = KDTree(pts)
    points = tree.KNN(targetPt, k)#返回[最近的n个数据，各自的距离]
    for j in range(k):
        find_data[j] = find(a,points[j])
    p0 = 0
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    for j in range(k):
        if find_data[j] == 0:
            p0 = p0 + 1
        elif find_data[j] == 1:
            p1 = p1 + 1
        elif find_data[j] == 2:
            p2 = p2 + 1
        elif find_data[j] == 3:
            p3 = p3 + 1
        elif find_data[j] == 4:
            p4 = p4 + 1
    if max(p0,p1,p2,p3,p4) == p0:
        return ("优")
    elif max(p0,p1,p2,p3,p4) == p1:
        return ("良")
    elif max(p0,p1,p2,p3,p4) == p2:
        return ("轻度污染")
    elif max(p0,p1,p2,p3,p4) == p3:
        return ("中度污染")
    elif max(p0,p1,p2,p3,p4) == p4:
        return ("重度污染")
choose = input("自行输入数据输入1，由文件写入数据输入2\n")
if int(choose) == 1:
    while True:
        temp_input = input("输入数据，以空格或逗号分隔\n")# 目标点
        targetPt = re.split(r'[;,\s]\s*', temp_input)
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
        f = open('result.csv', 'w',encoding='utf-8',newline="")
        with f:
            writer = csv.writer(f)
            for row in result:
                writer.writerow(row)