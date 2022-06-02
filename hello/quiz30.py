import string
import random

import numpy as np
import pandas as pd
from icecream import ic

from hello.domains import myRandom, members
from context.models import Model

'''
        데이터프레임 문제 Q02
    ic| df:     A   B   C
            1   1   2   3
            2   4   5   6
            3   7   8   9
            4  10  11  12
    '''
class Quiz30:
    def quiz30_df_4_by_3(self) -> str:
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], index=range(1, 5), columns=['A', 'B', 'C'])
        # 위 식을 리스트결합 형태로 분해해서 조립하시오
        d1 = [i for i in range(1, 4)]
        d2 = [i for i in range(4, 7)]
        d3 = [i for i in range(7, 10)]
        d4 = [i for i in range(10, 13)]
        d5 = [[i for i in range(j * 3 + 1, j * 3 + 4)] for j in range(4)]

        df1 = pd.DataFrame(d5, index=range(1, 5), columns=['A', 'B', 'C'])
        ic(df1)
        return None

    '''
            데이터프레임 문제 Q03.
            두자리 정수를 랜덤으로 2행 3열 데이터프레임을 생성
            ic| df:     0   1   2
                    0  97  57  52
                    1  56  83  80
        '''
    def quiz31_rand_2_by_3(self) -> str:
        # df = pd.DataFrame([[], []], index=range(0, 2), columns=['0', '1', '2'])
        d1 = [myRandom(10, 99) for i in range(3)]
        d2 = [[myRandom(10, 99) for i in range(3)] for i in range(2)]
        # df1 = pd.DataFrame(d2, index=range(0, 2), columns=['0', '1', '2'])
        df2 = pd.DataFrame(np.random.randint(10, 100, size=(2, 3)), index=range(0, 2), columns=['0', '1', '2'])
        ic(df2)
        return None

    '''
        데이터프레임 문제 Q04.
        국어, 영어, 수학, 사회 4과목을 시험치른 10명의 학생들의 성적표 작성.
         단 점수 0 ~ 100이고 학생은 랜덤 알파벳 5자리 ID 로 표기

          ic| df4:        국어  영어  수학  사회
                    lDZid  57  90  55  24
                    Rnvtg  12  66  43  11
                    ljfJt  80  33  89  10
                    ZJaje  31  28  37  34
                    OnhcI  15  28  89  19
                    claDN  69  41  66  74
                    LYawb  65  16  13  20
                    QDBCw  44  32   8  29
                    PZOTP  94  78  79  96
                    GOJKU  62  17  75  49
    '''
    @staticmethod
    def id(chr_size) -> str: return ''.join([random.choice(string.ascii_letters)for i in range(chr_size)])

    def quiz32_df_grade(self) -> object:

        data1 = np.random.randint(0, 100, size=(10, 4))
        idx = [self.id(chr_size=5) for i in range(10)]
        col = ['국어', '영어', '수학', '사회']
        df1 = pd.DataFrame(data1, index=idx, columns=col)
        col2 = ['국어', '영어', '수학', '사회']
        data2 = {i: j for i, j in zip(idx, data1)}
        # data2 = dict([idx], [data1])
        df2 = pd.DataFrame.from_dict(data2, orient='index', columns=col2)

        ic(df1)
        ic(df2)
        return None

    def quiz33_df_loc(self) -> str:
        # df = self.createDf(keys=['a', 'b', 'c', 'd'],
        #                    vals=np.random.randint(0, 100, 4),
        #                    len=3)
        # a = pd.DataFrame([dict(zip(['a', 'b', 'c', 'd'], np.random.randint(0, 100, 4))) for _ in range(3)])
        # d = [{i: j for i, j in zip(subjects, np.random.randint(0, 100, 4))} for _ in range(3)]
        # print(d)
        # df = pd.DataFrame(d)
        # ic(temp)

        # df = pd.DataFrame
        # ic(df.iloc[0])


        subjects = ['자바', '파이썬', '자바스크립트', 'SQL']
        students = members()
        d = np.random.randint(0, 100, size=(24, 4))
        students_scores_df = pd.DataFrame(d, index=students, columns=subjects)
        ic(students_scores_df)
        model = Model()
        model.save_model(fname='grade.csv', dframe=students_scores_df)

        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html

        grade_df = model.new_model(fname='grades.csv')
        ic(grade_df)
        print('Q1.파이썬의 점수만 출력하시오')
        python_scores = grade_df.loc[:, '파이썬']
        ic(type(python_scores))
        ic(python_scores)
        print('Q2.조현국의 점수만 출력하시오')
        cho_scores = grade_df.loc['조현국']
        ic(type(cho_scores))
        ic(cho_scores)
        print('Q3.조현국의 과목별 점수를 출력하시오')
        cho_subjects_scores = grade_df.loc[['조현국']]
        ic(type(cho_subjects_scores))
        ic(cho_scores)

        return None

    @staticmethod
    def createDf(keys, vals, len):
        return pd.DataFrame([dict(zip(keys, vals)) for _ in range(len)])

    def quiz34_df_iloc(self) -> str:
        '''
        ic| df.iloc[0]: a     4
                        b    41
                        c    21
                        d    16
        Name: 0, dtype: int32
        '''
        # ic(df.iloc[[0]])
        '''
        ic| df.iloc[[0]]:   a   b   c   d
                        0  95  71  61  27
        '''
        # ic(df.iloc[[0, 1]])
        '''
        ic| df.iloc[[0, 1]]:    a   b  c  d
                            0  73  46  6  8
                            1  73  46  6  8
        '''
        # ic(df.iloc[:3])
        '''
        ic| df.iloc[:3]:    a   b   c  d
                        0  21  91  77  2
                        1  21  91  77  2
                        2  21  91  77  2
        '''
        # ic(df.iloc[[True, False, True]])
        '''
        ic| df.iloc[[True, False, True]]:       a   b   c  d
                                            0  24  80  53  4
                                            2  24  80  53  
        '''
        # ic(df.iloc[lambda x:x.index % 2 == 0])
        '''
        ic| df.iloc[lambda x:x.index % 2 == 0]:     a   b   c  d
                                                0  19  12  50  5
                                                2  19  12  50  5
        '''
        # ic(df.iloc[0, 1])
        '''
        ic| df.iloc[0, 1]: 60
        '''
        # ic(df.iloc[[0, 2], [1, 3]])
        '''
        ic| df.iloc[[0, 2], [1, 3]]:   b   d
                                    0  58  26
                                    2  58  26
        '''
        # ic(df.iloc[1: 3, 0: 3])
        '''
        ic| df.iloc[1: 3, 0: 3]:    a  b   c
                                1  17  8  52
                                2  17  8  52
        '''
        # ic(df.iloc[:, [True, False, True, False]])
        '''
        ic| df.iloc[:, [True, False, True, False]]:     a   c
                                                    0  36  28
                                                    1  36  28
                                                    2  36  28
        '''
        # ic(df.iloc[:, lambda df: [0, 2]])
        '''
        ic| df.iloc[:, lambda df: [0, 2]]:      a   c
                                            0  36  28
                                            1  36  28
                                            2  36  28
        '''

        return None

    def quiz35(self) -> str: return None

    def quiz36(self) -> str: return None

    def quiz37(self) -> str: return None

    def quiz38(self) -> str: return None

    def quiz39(self) -> str: return None