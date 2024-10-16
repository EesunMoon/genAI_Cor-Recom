import pandas as pd
import numpy as np
import json
pd.set_option('display.max_seq_items', None)

"""
    [file] FineTuning dataset format으로 변환  
        csv -> json 형식으로 변환
        <US> question
        <CO> answer
"""

#-- variable setting --#
data_absolute_path = '/Users/eesun/CODE/KoAlpaca/fine_tuning_data/'
data_filename = 'extracted_data'
preprocessed_tag = '_preprocessed'
data_file_name_suffix = '.ddata'
data_fileformat_csv = '.csv'
data_fileformat_json = '.json'
flag = 2 # 0: subtask3, 1: subtask4, 2: total

'''
#-- data load --#
load_data_filename1 = data_absolute_path + data_filename + data_fileformat_csv
data1 = pd.read_csv(load_data_filename1, names=['tag','text'])
print("총 instruction-answer pair 개수 :", len(data[data['tag']=='<CO>']))
'''

"""

#-- instruction format --#

[
	{
		"instruction" : "직원들의 급여를 기록하는 데이터베이스를 설계하십시오.",
		"input" :, # 필수 사항이 아님
		"output" : "~~~~~~"
	},
	{
		"instruction" : "아래 문장의 각 단어에 품사를 지정하십시오",
		"input" : "새끼 고양이는 종종 신나게 뛰어다니기도 합니다.",
		"output" : "새끼(Noun) 고양이(Noun) 는 은 종종 Adverb 신나게 Adverb 뛰어다니기도 합니다."
		},
	...
]

"""

def convert_json(filename):
    load_data_filename = data_absolute_path + filename + data_fileformat_csv
    data = pd.read_csv(load_data_filename, names=['tag','text'])
    print(filename, "의 총 instruction-answer pair 개수 :", len(data[data['tag']=='<CO>']))

    #question_index_list = list(data[data['tag'] == '<US>'].index)
    #print(question_index_list)

    list_data = list()

    for idx in range(len(data)):
        sub_dict_data = dict()
        if data['tag'][idx] == '<US>':
            ques = data['text'][idx]
            continue
        if data['tag'][idx] == '<CO>':
            ans = data['text'][idx]
            sub_dict_data['instruction'] = ques
            sub_dict_data['input'] = ""
            sub_dict_data['output'] = ans
            list_data.append(sub_dict_data)

    print(len(list_data))
    # convert csv to json format
    json_data = json.dumps(list_data, ensure_ascii=False, indent='\t')
    # print(len(json_data))

    # save json data
    save_data_filename = data_absolute_path + filename + data_fileformat_json
    with open(save_data_filename, 'w') as f:
        f.write(json_data)


if flag==2:
    convert_json('total_extracted_data' + data_file_name_suffix)
else:

    if flag == 1:
        data_filename = 'subtask4_' + data_filename
    convert_json(data_filename + data_file_name_suffix)
    convert_json(data_filename + preprocessed_tag+ data_file_name_suffix)