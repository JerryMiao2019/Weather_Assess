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
def distance(a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6):#欧几里得距离
    return math.sqrt((a1-b1)**2 + (a2-b2)**2 + (a3-b3)**2 + (a4-b4)**2 + (a5-b5)**2 + (a6-b6)**2)
#前为质量 后为大小
#以下为堆排
def sift_down(a, start, end):
    parent = int(start)
    child = int(parent * 2 + 1)
    while child <= end:
        if child + 1 <= end and a[child][1] < a[child + 1][1]:
            child += 1
        if a[parent][1] >= a[child][1]:
            return
        else:
            a[parent][1], a[child][1] = a[child][1], a[parent][1]
            parent = child
            child = int(parent * 2 + 1)
def heapsort(a, len):
    i = (len - 2) / 2
    while i >= 0:
        sift_down(a, i, len - 1)
        i -= 1
    i = len - 1
    while i> 0:
        a[0], a[i] = a[i], a[0]
        sift_down(a, 0, i - 1)
        i -= 1
def main(x1,x2,x3,x4,x5,x6,kc):
    #将距离输入进a并将a排序
    for i in range(len(d)):
        a[i][1] = distance(d[i][2],d[i][3],d[i][4],d[i][5],d[i][6],d[i][7],x1,x2,x3,x4,x5,x6)
        a[i][0] = d[i][1]
    heapsort(a,20)
    if a[0][0] == 0:
        quality = "优"
    elif a[0][0] == 1:
        quality = "良"
    elif a[0][0] == 2:
        quality = "轻度污染"
    elif a[0][0] == 3:
        quality = "中度污染"
    else :
        quality = "重度污染"
    print("空气质量为"+quality)
a = [list() for i in range(len(d))]
print(a)
for i in range(len(d)):#生成一个空数组
    a[i].append(0)
    a[i].append(0)
main(int(input()),int(input()),int(input()),int(input()),float(input()),int(input()),1)#k值为一



