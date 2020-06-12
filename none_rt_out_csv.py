import csv

def init(file_name):
    f = open(file_name, 'w', encoding='utf-8', newline='')
    f.close()

def write(file_name, list):
    f = open(file_name, 'a+', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(list)
    f.close()