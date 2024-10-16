import re
import pandas as pd
import numpy as np
from konlpy.tag import Okt, Mecab, Hannanum, Kkma, Komoran
from setuptools import sic           # tokenizer

"""
    [file] KoAlpaca로 나온 답변의 의류 keyword 추출

    noun_extractor.py :: keyword noun extraction
        text preprocessing : 한글 제외 문자 제거 -> 토큰화 -> 불용어 제거
"""

class Noun_Extractor:
    def __init__(self):
        '''
        self.answer_data_example = ["현재 날씨에서 추천하는 의상은 하늘색 10부 팬츠와 흰색 상의입니다.",
                                    '여자에게 추천하는 데이트룩은 "사랑스러운 원피스"입니다.',
                                    "오늘 비오는 날에 어울리는 옷차림은 차분한 컬러의 원피스일 것 같습니다.",
                                    "파란색 비옷",
                                    "하늘하늘한 원피스를 추천드려요!",
                                    "'핑크'와 '하얀색'이라는 키워드로 추천하는 옷은 핑크색 블라우스와 하얀색 치마입니다.",
                                    "파란색 반팔 티에 흰색 5부 팬츠를 추천합니다.",
                                    "상황에 어울리는 깔끔한 '청순한' 파란색 원피스를 추천해드릴게요!"]
        '''
        self.designed_stop_words = ["날씨", "현재", "비", "날", "햇볓", "맑음", '하늘', '색부', '것', '색', '핑크',
                                    "하늘색", "핑크색", "하얀색", "파란색", "빨간색", '검정색', "노란색", "주황색", '초록색', "보라색", '흰색',
                                    '청순', '사랑', '차분', '스러운', '컬러', '어울리', '티', '부',
                                    "상황", "추천", "의상", "옷", "키워드",  "여자", "남자", "옷차림", '상의', '하의', '룩', '데이트']
        self.one_stop_words = ['은','는','이','가','하','아','것','들','의','있','되','수', '고', '에서',
                            '보','주','등','한','과','랑', '을', '를', '와', '도', '어요', '다']                   # 지정 불용어
        self.candidate_stop_words = self.Candidate_Stopwords_list_Load()                                    # 한국어불용어100사전
        self.stop_words = list(set(self.one_stop_words + self.candidate_stop_words + self.designed_stop_words))       # 가게 이름까지 합친 불용어

        self.text_preprocessing()


    def Candidate_Stopwords_list_Load(self):
        '''
        Candidate_Stopwords_list_Load() : 한국어불용어100.text 파일을 열어서 불용어 단어 반환
            input parameter : None
            output : (list)불용어
        '''
        file_name = '한국어불용어100.txt'
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
        
        if type(answer) == str:                 # main_text가 빈 리스트가 아닌 경우
            # 영어 및 한글을 제외한 문자 모두 제거
            # answer_text = re.sub('[^A-Za-z가-힣]','',answer)
            answer_text = re.sub('[^가-힣0-9]','',answer)
            #print('answer_text :', answer_text)

            # 영어는 소문자로 convert
            # cleaned_lowercase = answer_text.lower()
            
            # 형태소 토큰화 - 명사 추출
            # answer_words = self.tag.morphs(cleaned_lowercase)
            # answer_words = self.tag.morphs(answer_text)
            answer_words = self.tag.nouns(answer_text)
            print('answer_words :', answer_words)

            # 불용어 제거
            cleaned_words = [token for token in answer_words if not token in self.stop_words]
            print('cleaned_words :', cleaned_words)
        else:
            cleaned_words = []
            
        # return " ".join(cleaned_words)    # 하나의 문장으로
        return cleaned_words                # list로


    def text_preprocessing(self):
        self.tag = Mecab()

        '''
        answer_data = self.answer_data_example
        noun_list = self.cleaning(answer_data)
        #print(noun_list)
        '''

        data=pd.DataFrame()
        data['answer'] = self.answer_data_example
        data['keyword'] = data['answer'].apply(self.cleaning)

        print(data)

        return data
    

if __name__ == "__main__":
    '''
    Preprocessing class 실행
    '''

    # text 전처리
    noun_keyword = Noun_Extractor()
