import numpy as np
import time
from prettytable import PrettyTable
import glob


target_words = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl' ,'guitar', 'piano']


def dict_to_file(dic, fname):
    dic_file = open(fname,'w')
    for key, label in dic.items():
        dic_file.write(key + ' ' +  ' '.join(label) + '\n')


def file_to_dic(path):
    output = {}
    for line in file(path):
        line = line.split(' ')
        target, words = line[0], line[1:]
        output[target] = words
    return output

def create_table(list_file):
    dic_list = []
    tables = []

    length = len(list_file)
    for i in xrange(length):
        dic = file_to_dic(list_file[i])
        dic_list.append(dic)

    for word in target_words:
        table = PrettyTable()
        table.title = word
        column_names = ['dependency', 'window']
        for i in xrange(length):
            data = map(str, dic_list[i][word])
            table.add_column(column_names[i], data)

        print table
        tables.append(table)

    return tables

if __name__ == '__main__':
    start = time.time()

    folder_path = '/Users/arie.cattan/Desktop/Papier_Arie/BarIlan/NLP/Assignment/Ass3/word2vec/att/'

    files = glob.glob(folder_path + '*.txt')
    tables = create_table(files)


    #np.savetxt(folder_path + 'similarities.txt', tables, fmt='%s')