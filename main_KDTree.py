import math
d = [['2020-4-1',1,26,53,9,30,0.68,61],
    ['2020-4-2',1,36,57,6,29,0.57,63],
    ['2020-4-3',1,38,55,7,32,0.65,66],
    ['2020-4-4',2,23,188,6,24,0.51,68],
    ['2020-4-5',1,27,79,17,40,0.66,73],
    ['2020-4-6',2,82,152,12,54,1.03,76],
    ['2020-4-7',1,42,93,8,39,0.74,60],
    ['2020-4-8',1,22,65,15,45,0.93,56],
    ['2020-4-9',0,21,40,7,24,0.48,85],
    ['2020-4-10',1,43,53,5,38,0.55,68],
    ['2020-4-11',1,36,60,6,42,0.55,66],
    ['2020-4-12',1,35,93,8,45,0.67,68],
    ['2020-4-13',1,54,101,12,61,0.82,76],
    ['2020-4-14',1,71,92,11,45,0.86,96],
    ['2020-4-15',1,60,88,14,33,0.80,135],
    ['2020-4-16',2,67,95,6,27,1.01,92],
    ['2020-4-17',1,36,63,4,33,0.71,93],
    ['2020-4-18',1,66,76,7,49,0.91,103],
    ['2020-4-19',1,68,66,6,30,0.83,121],
    ['2020-4-20',0,11,32,3,13,0.38,79]]
#下为KD树
pts=[[26,53,9,30,0.68,61],
    [36,57,6,29,0.57,63],
    [38,55,7,32,0.65,66],
    [23,188,6,24,0.51,68],
    [27,79,17,40,0.66,73],
    [82,152,12,54,1.03,76],
    [42,93,8,39,0.74,60],
    [22,65,15,45,0.93,56],
    [21,40,7,24,0.48,85],
    [43,53,5,38,0.55,68],
    [36,60,6,42,0.55,66],
    [35,93,8,45,0.67,68],
    [54,101,12,61,0.82,76],
    [71,92,11,45,0.86,96],
    [60,88,14,33,0.80,135],
    [67,95,6,27,1.01,92],
    [36,63,4,33,0.71,93],
    [66,76,7,49,0.91,103],
    [68,66,6,30,0.83,121],
    [11,32,3,13,0.38,79]]  # 点集，任意维度的点集
targetPt = [27,53,9,30,0.68,61] # 目标点，任意维度的点
class Node():
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
        return (dimension + 1) % len(targetPt)
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
def find(lookingfor,given):
    for i in range(len(lookingfor)):
        if given[0] == lookingfor[i][2] and given[1] == lookingfor[i][3] and given[2] == lookingfor[i][4] and given[3] == lookingfor[i][5] and given[4] == lookingfor[i][6] and given[5] == lookingfor[i][7]:
            return lookingfor[i][1]
if __name__ == "__main__":
    kdtree = KDTree(pts)
    root = kdtree.createKDTree(pts, 0)
    pt, minDis = kdtree.getNearestPt(root, targetPt)
    #print("最近的点是", pt, "最小距离是", str(minDis))
    if find(d, pt) == 0:
        print("优")
    elif find(d, pt) == 1:
        print("良")
    elif find(d, pt) == 2:
        print("轻度污染")
    elif find(d, pt) == 3:
        print("中度污染")
    else:
        print("重度污染")



