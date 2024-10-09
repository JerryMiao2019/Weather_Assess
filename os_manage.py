import os,pandas
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
            df.to_csv(file_dir + '/_all.csv', encoding="utf_8_sig", index=False, header=False, mode='a+')
        else:
            pass


if __name__ == '__main__':
    append('data/xian/')