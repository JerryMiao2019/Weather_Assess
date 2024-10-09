import csv
a = []
with open('_all.csv', 'r', encoding='utf-8') as file:
    i = 0
    reader = csv.reader(file)
    for row in reader:
        i = i + 1  # 计算行数
        del row[2]
        del row[2]
        if row[1] == "优":
            row[1] = 0
        elif row[1] == "良":
            row[1] = 1
        elif row[1] == "轻度污染":
            row[1] = 2
        elif row[1] == "中度污染":
            row[1] = 3
        elif row[1] == "重度污染" or row[1] == "严重污染":
            row[1] = 4
        a.append(row)  # 向数组中加入数据
    for j in range(i):  # 转换string到int和float
        for k in range(1, 8):
            if k == 1:
                a[j][k] = int(a[j][k])
            else:
                a[j][k] = float(a[j][k])
    print(a)
    f = open('data.csv', 'w', encoding='utf-8', newline='')
    with f:
        writer = csv.writer(f)
        writer.writerows(a)