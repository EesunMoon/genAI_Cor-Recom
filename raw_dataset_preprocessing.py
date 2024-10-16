import pandas as pd

"""
    [file] <AC> tag에 해당하는 code를 description으로 변환

    raw_dataset_preprocessing.py
"""


'''
# file error check
with open('sub-task3/data/task1.ddata.wst.txt',encoding='cp949') as f:
    lines = f.readlines()
    
for line in lines:
    print(len(line.split(',')))
'''

"""
    Fine-Tuning dataset 전처리 방식
        <CO> Question
        <US> Answer
        <AC> Answer - 결과
            Feature(Color) + Iteam
            ex) CD-032 BL-216 SK-259 SE-175
"""

"""
    [ TAG INFO ]
        <CO> : 코디 에이전트
        <US> : 사용자
        <AC> : 패션 코디네이션

    [ Clothes Code INFO ]
        code : 패션 아이템 이름
        category : 항목
            ['O ' 'T ' 'B ' 'S ']
                'O ' : outer -> ['CD ' 'CT ' 'JK ' 'JP ' 'VT ']
                'T ' : Top -> ['BL ' 'KN ' 'SH ' 'SW ']
                'B ' : Bottom -> ['OP ' 'PT ' 'SK ']
                'S ' : 신발 -> ['SE ']
        item : 패션 아이템의 종류
            ['CD ' 'CT ' 'JK ' 'JP ' 'BL ' 'KN ' 'SH ' 'SW ' 'VT ' 'OP ' 'PT ' 'SE ', 'SK ']
                # Outer
                'CD ' : 가디건(Cardigan)
                'CT ' : 코트(Coat)
                'JK ' : 자켓(Jacket)
                'JP ' : 후드집업 
                'VT ' : 조끼
                # Top
                'BL ' : 블라우스(Blouse)
                'KN ' : 맨투맨
                'SH ' : 셔츠(Shirts)
                'SW ' : 니트(Sweater)
                # Bottom
                'OP ' : 원피스(Onepiece)
                'PT ' : 바지(Pants)
                'SK ' : 치마(Skirt)
                # Shoes
                'SE ' : 신발       
        feature : 특징 종류
            ['F ' 'M ' 'C ' 'E ']
                'F ' : 장식 및 스타일
                'M ' : 소재
                'C ' : color
                'E ' : 상황 및 형용사
        description : 특징 기술
"""

load_data_absolute_path = '/Users/eesun/CODE/KoAlpaca/data/'
save_data_absolute_path = '/Users/eesun/CODE/KoAlpaca/fine_tuning_data/'

#-- clothes info --#
'''
    clothes_item_info : item 종류 dict
    clothes_feature_color_info : 옷 색 정보 dict
'''
clothes_item_info = {'CD' : '가디건', 'CT' : '코트', 'JK' : '자켓', 'JP' : '후드집업', 'VT' : '조끼',
                        'BL' : '블라우스', 'KN' : '맨투맨', 'SH' : '셔츠', 'SW' : '니트',
                        'OP' : '원피스', 'PT' : '바지', 'SK' : '치마'}
clothes_info_file_name = load_data_absolute_path + 'mdata.wst.txt.2023.01.26'
clothes_info_data = pd.read_csv(clothes_info_file_name, encoding='cp949', sep='\t', names=['code', 'category', 'item', 'feature', 'description'])
clothes_info_data = clothes_info_data.drop(['category', 'item'], axis=1) # code, featutre, description
# a = clothes_info_data[clothes_info_data['item']=='SE ']
# print(a[a['feature']=='F '])
# print(clothes_info_data[clothes_info_data['item']=='CD '])
# print(clothes_info_data[clothes_info_data['category']=='S '])
# print(clothes_info_data[clothes_info_data['code']=='CD-032 '])
# print(clothes_info_data['category'].unique())
clothes_feature_color_info = clothes_info_data[clothes_info_data['feature']=='C '].drop(['feature'], axis=1)
clothes_feature_color_info = dict(zip(clothes_feature_color_info['code'], clothes_feature_color_info['description']))


#-- Text Data Preprocessing --#
data_file_name_prefix = 'task'
data_file_name_suffix = '.ddata.wst'
data_fileformat_txt = '.txt'
data_fileformat_csv = '.csv'
idx = 1

def replace_code_to_text(AC_code):
    flag = 0
    codes = AC_code.split()
    print('code :', codes)
    AC_str_list = []
    for code in codes:
        # print(code)
        if code[2] != '-':
            code = code[0:2] + '-' + code[2:]

        if code[:2] =='SE':
            flag = 1
            continue
        target_item_info = clothes_item_info.get(code[:2]) # item 정보
        code = code + ' '
        target_color_info = clothes_feature_color_info.get(code)
        recommend_clothes = target_color_info + ' ' + target_item_info
        # print(target_color_info, target_item_info)
        print(recommend_clothes)
        AC_str_list.append(recommend_clothes)
    # print(AC_str_list)

    if flag == 0: # shoes 항목만 있지 않는 경우
        AC_str = ', '.join(AC_str_list)
        # print(', '.join(AC_str_list))
        AC_str = AC_str + ' 항목을 추천해요.'
    else: # shoes 항목만 있는 경우
        AC_str = '운동화를 추천해요.'
    # print(AC_str)
    return AC_str

'''
data = pd.read_csv('/Users/eesun/CODE/KoAlpaca/data/task6.ddata.wst.txt',encoding='cp949', sep='\t', names=['index','tag','text', 'etc'])
data = data.drop(data[['index', 'etc']], axis=1)
data.loc[data['tag']=='<AC>', 'text'] = data.loc[data['tag']=='<AC>', 'text'].apply(replace_code_to_text)
print(data)
# print(data.loc[data['tag']=='<AC>', 'text'].isnull().unique())
'''


for idx in range(1,7):
    data_filename = data_file_name_prefix + str(idx) + data_file_name_suffix
    load_data_filename = load_data_absolute_path + data_filename + data_fileformat_txt
    save_data_filename = save_data_absolute_path + data_filename + data_fileformat_csv

    ## DATALOAD
    data = pd.read_csv(load_data_filename, encoding='cp949', 
                        sep='\t', names=['index','tag','text', 'etc'])
    data = data.drop(data[['index', 'etc']], axis=1)
    print('idx :', idx)
    # print(data)

    ## DATA PREPROCESSING
    # replace_code_to_text(' CD-032 BL-216 SK-259 SE-175')
    # print(data.loc[data['tag']=='<AC>', 'text'])
    data.loc[data['tag']=='<AC>', 'text'] = data.loc[data['tag']=='<AC>', 'text'].apply(replace_code_to_text)
    # data[data['tag']=='<AC>']['text'] = replace_code_to_text(data[data['tag']=='<AC>']['text'])
    print(data)

    data.to_csv(save_data_filename, header=None, index=None)
