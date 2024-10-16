import pandas as pd

"""
    [file] text file encoding -> dataframe으로 변환 & 저장
"""

### task3 data preprocessing
#-- variables --#
load_data_absolute_path = '/Users/eesun/CODE/KoAlpaca/data/'
save_data_absolute_path = '/Users/eesun/CODE/KoAlpaca/fine_tuning_data/'
data_file_name_prefix = 'task'
data_file_name_suffix = '.ddata.wst'
data_fileformat_txt = '.txt'
data_fileformat_csv = '.csv'

for idx in range(0,7):
    data_filename = data_file_name_prefix + str(idx) + data_file_name_suffix
    load_data_filename = load_data_absolute_path + data_filename + data_fileformat_txt
    save_data_filename = save_data_absolute_path + data_filename + data_fileformat_csv

    if idx ==0:
        load_data_task4_absolute_path = '/Users/eesun/CODE/KoAlpaca/data_task4/'
        load_data_filename = load_data_task4_absolute_path + data_filename + data_fileformat_txt
    
    
    data = pd.read_csv(load_data_filename, encoding='cp949', 
                        sep='\t', names=['index','tag','text', 'etc'])
    # data = data.loc[:, ['tag', 'text']]
    data = data.drop(data[['index', 'etc']], axis=1)
    print('idx :', idx)
    print(data)

    data.to_csv(save_data_filename, index=None)