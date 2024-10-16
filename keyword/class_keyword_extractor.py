import re
import pandas as pd
import numpy as np
from konlpy.tag import Mecab
from setuptools import sic           # tokenizer
# from class_keyword_extractor import Noun_Extractor


class Noun_Extractor:
  def __init__(self):
    self.designed_stop_words = ["날씨", "현재", "비", "날", "햇볓", "맑음", '하늘', '색부', '것', '색', '핑크',
                                "하늘색", "핑크색", "하얀색", "파란색", "빨간색", '검정색', "노란색", "주황색", '초록색', "보라색", '흰색',
                                '청순', '사랑', '차분', '스러운', '컬러', '어울리', '티', '부',
                                '여성', '느낌', '대표', '아이템', '색상', '디자인', '선택', '폭',
                                "상황", "추천", "의상", "옷", "키워드",  "여자", "남자", "옷차림", '상의', '하의', '룩', '데이트']
    self.one_stop_words = ['은','는','이','가','하','아','것','들','의','있','되','수', '고', '에서',
                        '보','주','등','한','과','랑', '을', '를', '와', '도', '어요', '다']                   # 지정 불용어
    self.candidate_stop_words = self.Candidate_Stopwords_list_Load()                                    # 한국어불용어100사전
    self.stop_words = list(set(self.one_stop_words + self.candidate_stop_words + self.designed_stop_words))       # 가게 이름까지 합친 불용어


  def Candidate_Stopwords_list_Load(self):
    '''
    Candidate_Stopwords_list_Load() : 한국어불용어100.text 파일을 열어서 불용어 단어 반환
        input parameter : None
        output : (list)불용어
    '''

    ##-- (수정하기) 경로 수정 --##
    file_name = '/Users/eesun/CODE/KoAlpaca/한국어불용어100.txt' 

    korean_stopwords100 = pd.read_csv(file_name, sep = '\t', header = None, names=['word', 'morph', 'rate'])
    return korean_stopwords100['word'].tolist()


  def cleaning(self, answer):
    '''
    cleaning() : 데이터 정제
                토큰화(Tokenization)
                불용어(Stopword)
                정규 표현식 (Regular Expression)
                정수 인코딩(Integer Encoding)
        input parameter : (str)answer
        output : (str)정제된 정보
    '''
    print("전처리할 answer text :", answer)
    # self.tag = Okt()
    self.tag = Mecab()
    if type(answer) == str:                 # main_text가 빈 리스트가 아닌 경우
        # 영어 및 한글을 제외한 문자 모두 제거
        answer_text = re.sub('[^가-힣0-9]','',answer)
        
        # 형태소 토큰화 - 명사 추출
        answer_words = self.tag.nouns(answer_text)
        print('answer_words :', answer_words)

        # 불용어 제거
        cleaned_words = [token for token in answer_words if not token in self.stop_words]
        print('cleaned_words :', cleaned_words)
    else:
        cleaned_words = []
    
    cleaned_words = list(set(cleaned_words))

    return cleaned_words                # list로


"""
##-- 사용법 --##

# koalpaca에서 생성된 generated answer
prompt = '이와 같은 상황에서는 여성스럽고 우아한 느낌을 주는 원피스를 추천드립니다. 원피스는 여성스럽고 우아한 느낌을 주는 대표적인 아이템으로, 다양한 색상과 디자인이 있어 선택의 폭이'
answer_data = prompt

# Noun_Extractor class 호출
noun_extractor = Noun_Extractor()
# keyword 추출
noun_keyword = noun_extractor.cleaning(answer_data)
print("의류추천 Keyword :", noun_keyword)
"""