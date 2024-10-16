import pandas as pd
import numpy as np
pd.set_option('display.max_seq_items', None)

"""
    [file] dataset에서 필요한 정보만 추출하여 한 file로 저장
        <US> question
        <CO> answer
"""

data_absolute_path = '/Users/eesun/CODE/KoAlpaca/fine_tuning_data/'
data_file_name_prefix = 'task'
data_file_name_suffix = '.ddata.wst'
data_fileformat_csv = '.csv'
idx = 1

'''
    Question : start_announcement 다음 문장 -> question_index_list
    Answer : <AC> 다음 문장 -> answer_index_list
        drop_announcement 다음이면 삭제 -> drop_index_list

    ## column info
    tag, text
'''

final_data = pd.DataFrame(index=None, columns=['tag', 'text'])
start_announcement = '안녕하세요. 코디봇입니다. 무엇을 도와드릴까요?'
# 안녕하세요. 어서오세요. 1204

for idx in range(1,7):
    
    data_filename = data_file_name_prefix + str(idx) + data_file_name_suffix
    load_data_filename = data_absolute_path + data_filename + data_fileformat_csv

    ## DATALOAD
    data = pd.read_csv(load_data_filename)

    # print(data.info())
    
    # question index
    start_index_list1 = list(data[data['text'].str.contains('안녕_하 세 요')].index)
    start_index_list2 = list(data[data['text'].str.contains('어서 오 세 요')].index)
    start_index_list = sorted(start_index_list1 + start_index_list2)   
    question_index_list = np.add(start_index_list, 1)
    question_index_list = list(question_index_list)

    # drop index
    drop_index_list1 = list(data[data['text'].str.contains('최종')].index)
    drop_index_list2 = list(data[data['text'].str.contains('전체')].index)
    drop_index_list = sorted(drop_index_list1 + drop_index_list2)
    drop_index_set = set(drop_index_list)

    # answer index
    AC_index_list = list(data[data['tag'] == '<AC>'].index)
    answer_index_list = np.add(AC_index_list, 1)
    answer_index_list = [i for i in answer_index_list if i not in drop_index_set]
    answer_index_list = [i for i in answer_index_list if i not in AC_index_list]

    # 추출할 index
    extract_index_list = question_index_list + answer_index_list
    extract_index_list = sorted(extract_index_list)

    # 추출한 dataframe
    extract_data = data.iloc[extract_index_list, :]

    # dataframe 연결
    final_data = pd.concat([final_data, extract_data], ignore_index=True)
    print('index :', idx)
    

final_data = final_data.loc[final_data['tag']!='<AC>',:]
# print(final_data.loc[final_data['tag']=='<AC>',:])
print(final_data)
print(len(final_data.loc[data['tag']=='<AC>', :]))
save_data_filename = data_absolute_path + 'extracted_data' + data_fileformat_csv
final_data.to_csv(save_data_filename, header=None, index=None)

