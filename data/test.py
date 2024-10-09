import csv
a = []
with open('../over.csv', 'r', encoding='utf-8') as file:
    i = 0
    reader = csv.reader(file)
    for row in reader:
        i = i + 1  # 计算行数
        a.append(row)  # 向数组中加入数据
    print(a)