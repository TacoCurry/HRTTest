import csv

file_name = "output.csv"

def init():
    f = open(file_name, 'w', encoding='utf-8', newline='')
    f.close()

def write(list):
    f = open(file_name, 'a+', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(list)
    f.close()