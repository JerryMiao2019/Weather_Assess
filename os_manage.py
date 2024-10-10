import os,pandas,csv
def file_name(file_dir):
    file_list=[]
    for files in os.listdir(file_dir):
        if os.path.splitext(files)[1] == '.csv':
            file_list.append(files)
    return file_list

def append(file_dir):
    list = file_name(file_dir)
    for i in range(1, len(list)):
        if list[i] != '_all.csv':
            df = pandas.read_csv(file_dir + '/' + list [ i ])
            df.drop([0],inplace= True)
            print(df)
            df.to_csv('_all.csv', encoding="utf_8_sig", index=False, header=False, mode='a+')
        else:
            pass

def change(file_name):
    print()
    a = []
    with open(file_name, 'r', encoding='utf-8') as file:
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

if __name__ == '__main__':
    append('data/xian/')
    change('_all.csv')
