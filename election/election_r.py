import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rc, font_manager
rc('font', family=font_manager.FontProperties(fname='C:/Windows/Fonts/malgunsl.ttf').get_name())

from context.domains import Reader, File
import re


class Solution(Reader):
    def __init__(self):
        self.file = File()
        self.file.context = './data/'

    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. 텍스트 마이닝')
            print('2. DF로 정형화')
            print('3. 토큰화 ')
            print('4. Embedding')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            if menu == '1':
                self.get_data()
            if menu == '2':
                self.final()
            if menu == '3':
                self.token_embedding()
            elif menu == '4':
                pass

    def cut_char_sigu(self, name):
        return name if len(name) == 2 else name[:-1]


    def get_data(self):
        file = self.file
        file.fname = '05. election_result'
        election_result = self.csv(file)
        sido_candi = election_result['광역시도']
        sido_candi = [name[:2] if name[:2]
                                  in ['서울', '부산', '대구', '광주', '인천', '대전', '울산']
                      else '' for name in sido_candi]
        # print(election_result.head())
        '''
           Unnamed: 0   광역시도   시군       pop      moon     hong      ahn
        0           0  서울특별시  종로구  102566.0   42512.0  22325.0  22313.0
        1           1  서울특별시   중구   82852.0   34062.0  17901.0  19372.0
        2           2  서울특별시  용산구  148157.0   58081.0  35230.0  32109.0
        3           3  서울특별시  성동구  203175.0   86686.0  40566.0  45674.0
        4           4  서울특별시  광진구  240030.0  105512.0  46368.0  52824.0
        '''
        sigun_candi = [''] * len(election_result)
        for n in election_result.index:
            each = election_result['시군'][n]
            if each[:2] in ['수원', '성남', '안양', '안산', '고양',
                            '용인', '청주', '천안', '전주', '포항', '창원']:
                sigun_candi[n] = re.split('시', each)[0] + ' ' + \
                                 self.cut_char_sigu(re.split('시', each)[1])
            else:
                sigun_candi[n] = self.cut_char_sigu(each)
        # print(sigun_candi)
        '''
        ['종로', '중구', '용산', '성동', ... , '거창', '합천', '제주', '서귀포']
        '''
        ID_candi = [sido_candi[n] + ' ' + sigun_candi[n] for n in range(0, len(sigun_candi))]
        ID_candi = [name[1:] if name[0] == ' ' else name for name in ID_candi]
        ID_candi = [name[:2] if name[:2] == '세종' else name for name in ID_candi]
        # print(ID_candi)
        '''
        ['서울 종로', '서울 중구', '서울 용산', '서울 성동', ... , '거창', '합천', '제주', '서귀포']
        '''
        election_result['ID'] = ID_candi
        # print(election_result.head(10))
        '''
           Unnamed: 0   광역시도    시군       pop      moon     hong      ahn      ID
        0           0  서울특별시   종로구  102566.0   42512.0  22325.0  22313.0   서울 종로
        1           1  서울특별시    중구   82852.0   34062.0  17901.0  19372.0   서울 중구
        2           2  서울특별시   용산구  148157.0   58081.0  35230.0  32109.0   서울 용산
        3           3  서울특별시   성동구  203175.0   86686.0  40566.0  45674.0   서울 성동
        4           4  서울특별시   광진구  240030.0  105512.0  46368.0  52824.0   서울 광진
        5           5  서울특별시  동대문구  236092.0   98958.0  51631.0  53359.0  서울 동대문
        6           6  서울특별시   중랑구  265706.0  111450.0  56545.0  62778.0   서울 중랑
        7           7  서울특별시   성북구  295866.0  129263.0  57584.0  66518.0   서울 성북
        8           8  서울특별시   강북구  210614.0   89645.0  42268.0  51669.0   서울 강북
        9           9  서울특별시   도봉구  229233.0   94898.0  47461.0  55600.0   서울 도봉
        '''
        election_result[['rate_moon', 'rate_hong', 'rate_ahn']] = \
            election_result[['moon', 'hong', 'ahn']].div(election_result['pop'], axis=0)
        election_result[['rate_moon', 'rate_hong', 'rate_ahn']] *= 100
        # print(election_result.head())
        '''
           Unnamed: 0   광역시도   시군       pop  ...     ID  rate_moon  rate_hong   rate_ahn
        0           0  서울특별시  종로구  102566.0  ...  서울 종로  41.448433  21.766472  21.754773
        1           1  서울특별시   중구   82852.0  ...  서울 중구  41.111862  21.605996  23.381451
        2           2  서울특별시  용산구  148157.0  ...  서울 용산  39.202333  23.778829  21.672280
        3           3  서울특별시  성동구  203175.0  ...  서울 성동  42.665682  19.966039  22.480128
        4           4  서울특별시  광진구  240030.0  ...  서울 광진  43.957839  19.317585  22.007249
        '''
        # print(election_result.sort_values(['rate_moon'], ascending=[False]).head(10))
        '''
             Unnamed: 0   광역시도      시군  ...  rate_moon  rate_hong   rate_ahn
        182         182   전라남도     순천시  ...  67.563695   2.493786  22.280946
        166         166   전라북도  전주시덕진구  ...  66.716865   2.758074  21.385582
        165         165   전라북도  전주시완산구  ...  66.687114   2.962565  21.366173
        175         175   전라북도     장수군  ...  66.633497   4.459233  20.853287
        184         184   전라남도     광양시  ...  65.927955   4.253818  20.833333
        173         173   전라북도     진안군  ...  65.819849   4.523113  21.560722
        172         172   전라북도     완주군  ...  65.722747   3.372819  22.245878
        168         168   전라북도     익산시  ...  64.212728   3.366145  23.795576
        170         170   전라북도     남원시  ...  64.183417   3.501833  25.020317
        63           63  광주광역시     광산구  ...  64.106862   1.462477  26.349568
        '''
        # print(election_result.sort_values(['rate_hong'], ascending=[False]).head(10))
        '''
             Unnamed: 0  광역시도   시군      pop  ...  ID  rate_moon  rate_hong   rate_ahn
        219         219  경상북도  군위군  17627.0  ...  군위  12.770182  66.097464  11.000170
        220         220  경상북도  의성군  37855.0  ...  의성  14.172500  62.845067  12.592788
        223         223  경상북도  영덕군  26125.0  ...  영덕  14.491866  62.445933  12.367464
        247         247  경상남도  합천군  33021.0  ...  합천  21.631689  59.655976   9.318313
        216         216  경상북도  고령군  22396.0  ...  고령  16.761922  59.153420  11.609216
        213         213  경상북도  예천군  32124.0  ...  예천  16.377163  58.719338  13.780974
        215         215  경상북도  청도군  30398.0  ...  청도  17.511020  58.155142  12.020528
        221         221  경상북도  청송군  18418.0  ...  청송  17.472038  57.927028  12.960148
        240         240  경상남도  창녕군  42878.0  ...  창녕  24.044965  57.054900   9.041933
        212         212  경상북도  문경시  49113.0  ...  문경  17.543217  56.669314  14.059414
        '''
        # print(election_result.sort_values(['rate_ahn'], ascending=[False]).head(10))
        '''
             Unnamed: 0   광역시도   시군       pop  ...     ID  rate_moon  rate_hong   rate_ahn
        196         196   전라남도  진도군   21189.0  ...     진도  49.044315   2.411629  41.790552
        201         201   전라남도  신안군   28950.0  ...     신안  49.637306   2.462867  41.450777
        193         193   전라남도  강진군   25175.0  ...     강진  49.557100   2.991063  40.325720
        195         195   전라남도  해남군   48351.0  ...     해남  53.568696   2.394987  37.552481
        197         197   전라남도  영암군   36402.0  ...     영암  52.192187   2.266359  37.388056
        180         180   전라남도  목포시  145476.0  ...     목포  53.545602   1.776238  36.640408
        59           59  광주광역시   동구   66287.0  ...  광주 동구  55.897838   1.973238  35.358366
        192         192   전라남도  장흥군   27149.0  ...     장흥  54.591329   2.342628  35.334635
        190         190   전라남도  보성군   29967.0  ...     보성  55.614509   2.442687  35.085260
        198         198   전라남도  무안군   52516.0  ...     무안  56.203824   1.871810  34.374286
        '''

        file.fname = '05. draw_korea'
        draw_korea = self.csv(file)
        # print(draw_korea.head())
        '''
           Unnamed: 0  y   x      ID
        0           0  0   7      철원
        1           1  0   8      화천
        2           2  0   9      양구
        3           3  0  10  고성(강원)
        4           4  1   3      양주
        '''
        # print(set(draw_korea['ID'].unique()) - set(election_result['ID'].unique()))
        '''
        {'창원 합포', '창원 회원', '부천 원미', '부천 오정', '고성(경남)', '부천 소사', '고성(강원)'}
        '''
        # print(set(election_result['ID'].unique()) - set(draw_korea['ID'].unique()))
        '''
        {'창원 마산회원', '부천', '고성', '창원 마산합포'}
        '''
        # print(election_result[election_result['ID'] == '고성'])
        '''
             Unnamed: 0  광역시도   시군      pop  ...  ID  rate_moon  rate_hong   rate_ahn
        125         125   강원도  고성군  18692.0  ...  고성  30.301733  34.833084  21.206933
        233         233  경상남도  고성군  34603.0  ...  고성  28.459960  48.542034  11.860243
        '''
        election_result.loc[125, 'ID'] = '고성(강원)'
        election_result.loc[233, 'ID'] = '고성(경남)'
        # print(election_result[election_result['시군'] == '고성군'])
        '''
             Unnamed: 0  광역시도   시군      pop  ...      ID  rate_moon  rate_hong   rate_ahn
        125         125   강원도  고성군  18692.0  ...  고성(강원)  30.301733  34.833084  21.206933
        233         233  경상남도  고성군  34603.0  ...  고성(경남)  28.459960  48.542034  11.860243
        '''
        # print(election_result[election_result['광역시도'] == '경상남도'])
        '''
             Unnamed: 0  광역시도        시군  ...  rate_moon  rate_hong   rate_ahn
        226         226  경상남도    창원시의창구  ...  37.036337  34.677257  13.916743
        227         227  경상남도    창원시성산구  ...  41.556282  27.426350  14.950400
        228         228  경상남도  창원시마산합포구  ...  29.838784  45.680368  12.312103
        229         229  경상남도  창원시마산회원구  ...  32.915317  41.197160  12.974839
        230         230  경상남도    창원시진해구  ...  35.937759  34.892271  15.190061
        231         231  경상남도       진주시  ...  33.179841  42.076091  11.977308
        232         232  경상남도       통영시  ...  30.748899  43.603886  12.959990
        233         233  경상남도       고성군  ...  28.459960  48.542034  11.860243
        234         234  경상남도       사천시  ...  31.262665  45.384669  11.669345
        235         235  경상남도       김해시  ...  46.495084  26.042174  14.179285
        236         236  경상남도       밀양시  ...  29.484912  45.827380  12.835458
        237         237  경상남도       거제시  ...  45.457632  25.810424  13.551887
        238         238  경상남도       의령군  ...  26.560390  52.622287  10.302212
        239         239  경상남도       함안군  ...  30.996672  45.157981  12.307938
        240         240  경상남도       창녕군  ...  24.044965  57.054900   9.041933
        241         241  경상남도       양산시  ...  41.740436  29.429780  15.485275
        242         242  경상남도       하동군  ...  32.662277  43.304976  12.090665
        243         243  경상남도       남해군  ...  28.734110  46.894862  12.930350
        244         244  경상남도       함양군  ...  27.732733  48.828829  12.023273
        245         245  경상남도       산청군  ...  26.765390  51.172847  11.230776
        246         246  경상남도       거창군  ...  27.237750  48.338778  11.912886
        247         247  경상남도       합천군  ...  21.631689  59.655976   9.318313
        '''
        election_result.loc[228, 'ID'] = '창원 합포'
        election_result.loc[229, 'ID'] = '창원 회원'
        # print(election_result[election_result['광역시도'] == '경상남도'])
        '''
             Unnamed: 0  광역시도        시군  ...  rate_moon  rate_hong   rate_ahn
        226         226  경상남도    창원시의창구  ...  37.036337  34.677257  13.916743
        227         227  경상남도    창원시성산구  ...  41.556282  27.426350  14.950400
        228         228  경상남도  창원시마산합포구  ...  29.838784  45.680368  12.312103
        229         229  경상남도  창원시마산회원구  ...  32.915317  41.197160  12.974839
        230         230  경상남도    창원시진해구  ...  35.937759  34.892271  15.190061
        231         231  경상남도       진주시  ...  33.179841  42.076091  11.977308
        232         232  경상남도       통영시  ...  30.748899  43.603886  12.959990
        233         233  경상남도       고성군  ...  28.459960  48.542034  11.860243
        234         234  경상남도       사천시  ...  31.262665  45.384669  11.669345
        235         235  경상남도       김해시  ...  46.495084  26.042174  14.179285
        236         236  경상남도       밀양시  ...  29.484912  45.827380  12.835458
        237         237  경상남도       거제시  ...  45.457632  25.810424  13.551887
        238         238  경상남도       의령군  ...  26.560390  52.622287  10.302212
        239         239  경상남도       함안군  ...  30.996672  45.157981  12.307938
        240         240  경상남도       창녕군  ...  24.044965  57.054900   9.041933
        241         241  경상남도       양산시  ...  41.740436  29.429780  15.485275
        242         242  경상남도       하동군  ...  32.662277  43.304976  12.090665
        243         243  경상남도       남해군  ...  28.734110  46.894862  12.930350
        244         244  경상남도       함양군  ...  27.732733  48.828829  12.023273
        245         245  경상남도       산청군  ...  26.765390  51.172847  11.230776
        246         246  경상남도       거창군  ...  27.237750  48.338778  11.912886
        247         247  경상남도       합천군  ...  21.631689  59.655976   9.318313
        '''
        # print(set(draw_korea['ID'].unique()) - set(election_result['ID'].unique()))

        # print(set(election_result['ID'].unique()) - set(draw_korea['ID'].unique()))

        # print(election_result[election_result['시군'] == '부천시'])

        # print(election_result.tail())
        '''
        ahn_tmp = election_result.loc[85, 'ahn'] / 3
        hong_tmp = election_result.loc[85, 'hong'] / 3
        moon_tmp = election_result.loc[85, 'moon'] / 3
        pop_tmp = election_result.loc[85, 'pop'] / 3
        rate_moon_tmp = election_result.loc[85, 'rate_moon']
        rate_hong_tmp = election_result.loc[85, 'rate_hong']
        rate_ahn_tmp = election_result.loc[85, 'rate_ahn']
        election_result.loc[250] = [ahn_tmp, hong_tmp, moon_tmp, pop_tmp,
                                    '경기도', '부천시', '부천 소사',
                                    rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp]
        election_result.loc[251] = [ahn_tmp, hong_tmp, moon_tmp, pop_tmp,
                                    '경기도', '부천시', '부천 오정',
                                    rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp]
        election_result.loc[252] = [ahn_tmp, hong_tmp, moon_tmp, pop_tmp,
                                    '경기도', '부천시', '부천 원미',
                                    rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp]
        print(election_result[election_result['시군'] == '부천시'])
        '''

        election_result.drop([85], inplace=True)
        # print(election_result[election_result['시군'] == '부천시'])
        '''
        Empty DataFrame
        Columns: [Unnamed: 0, 광역시도, 시군, pop, moon, hong, ahn, ID, rate_moon, rate_hong, rate_ahn]
        '''
        # print(set(draw_korea['ID'].unique()) - set(election_result['ID'].unique()))
        # {'부천 오정', '부천 원미', '부천 소사'}????
        # print(set(election_result['ID'].unique()) - set(draw_korea['ID'].unique()))
        # set()

        final_elect_data = pd.merge(election_result, draw_korea, how='left', on=['ID'])
        # print(final_elect_data.head())
        '''
           Unnamed: 0_x   광역시도   시군       pop  ...   rate_ahn  Unnamed: 0_y  y  x
        0             0  서울특별시  종로구  102566.0  ...  21.754773            34  4  6
        1             1  서울특별시   중구   82852.0  ...  23.381451            45  5  6
        2             2  서울특별시  용산구  148157.0  ...  21.672280            56  6  6
        3             3  서울특별시  성동구  203175.0  ...  22.480128            46  5  7
        4             4  서울특별시  광진구  240030.0  ...  22.007249            57  6  7
        '''

        final_elect_data['moon_vs_hong'] = final_elect_data['rate_moon'] - \
                                           final_elect_data['rate_hong']
        final_elect_data['moon_vs_ahn'] = final_elect_data['rate_moon'] - \
                                          final_elect_data['rate_ahn']
        final_elect_data['ahn_vs_hong'] = final_elect_data['rate_ahn'] - \
                                          final_elect_data['rate_hong']
        # print(final_elect_data.head())
        '''
           Unnamed: 0_x   광역시도   시군  ...  moon_vs_hong  moon_vs_ahn  ahn_vs_hong
        0             0  서울특별시  종로구  ...     19.681961    19.693661    -0.011700
        1             1  서울특별시   중구  ...     19.505866    17.730411     1.775455
        2             2  서울특별시  용산구  ...     15.423503    17.530053    -2.106549
        3             3  서울특별시  성동구  ...     22.699643    20.185554     2.514089
        4             4  서울특별시  광진구  ...     24.640253    21.950590     2.689664
        '''

        # print(final_elect_data.sort_values(['moon_vs_hong'], ascending=[False]).head(10))
        '''
             Unnamed: 0_x   광역시도      시군  ...  moon_vs_hong  moon_vs_ahn  ahn_vs_hong
        181           182   전라남도     순천시  ...     65.069909    45.282749    19.787160
        165           166   전라북도  전주시덕진구  ...     63.958791    45.331283    18.627508
        164           165   전라북도  전주시완산구  ...     63.724549    45.320941    18.403608
        63             63  광주광역시     광산구  ...     62.644384    37.757293    24.887091
        171           172   전라북도     완주군  ...     62.349928    43.476869    18.873059
        174           175   전라북도     장수군  ...     62.174265    45.780210    16.394054
        183           184   전라남도     광양시  ...     61.674137    45.094622    16.579515
        172           173   전라북도     진안군  ...     61.296736    44.259126    17.037610
        180           181   전라남도     여수시  ...     61.085143    36.314135    24.771008
        167           168   전라북도     익산시  ...     60.846583    40.417152    20.429431
        '''

        # print(final_elect_data.sort_values(['moon_vs_hong'], ascending=[True]).head(10))
        '''
             Unnamed: 0_x  광역시도   시군  ...  moon_vs_hong  moon_vs_ahn  ahn_vs_hong
        218           219  경상북도  군위군  ...    -53.327282     1.770012   -55.097294
        219           220  경상북도  의성군  ...    -48.672566     1.579712   -50.252278
        222           223  경상북도  영덕군  ...    -47.954067     2.124402   -50.078469
        215           216  경상북도  고령군  ...    -42.391498     5.152706   -47.544204
        212           213  경상북도  예천군  ...    -42.342174     2.596190   -44.938364
        214           215  경상북도  청도군  ...    -40.644121     5.490493   -46.134614
        220           221  경상북도  청송군  ...    -40.454990     4.511891   -44.966880
        211           212  경상북도  문경시  ...    -39.126097     3.483803   -42.609900
        210           211  경상북도  상주시  ...    -38.121890     4.377040   -42.498929
        246           247  경상남도  합천군  ...    -38.024288    12.313376   -50.337664
        '''
        return final_elect_data

    def drawKorea(self, targetData, blockedMap, cmapname):
        BORDER_LINES = [
            [(5, 1), (5, 2), (7, 2), (7, 3), (11, 3), (11, 0)],  # 인천
            [(5, 4), (5, 5), (2, 5), (2, 7), (4, 7), (4, 9), (7, 9),
             (7, 7), (9, 7), (9, 5), (10, 5), (10, 4), (5, 4)],  # 서울
            [(1, 7), (1, 8), (3, 8), (3, 10), (10, 10), (10, 7),
             (12, 7), (12, 6), (11, 6), (11, 5), (12, 5), (12, 4),
             (11, 4), (11, 3)],  # 경기도
            [(8, 10), (8, 11), (6, 11), (6, 12)],  # 강원도
            [(12, 5), (13, 5), (13, 4), (14, 4), (14, 5), (15, 5),
             (15, 4), (16, 4), (16, 2)],  # 충청북도
            [(16, 4), (17, 4), (17, 5), (16, 5), (16, 6), (19, 6),
             (19, 5), (20, 5), (20, 4), (21, 4), (21, 3), (19, 3), (19, 1)],  # 전라북도
            [(13, 5), (13, 6), (16, 6)],  # 대전시
            [(13, 5), (14, 5)],  # 세종시
            [(21, 2), (21, 3), (22, 3), (22, 4), (24, 4), (24, 2), (21, 2)],  # 광주
            [(20, 5), (21, 5), (21, 6), (23, 6)],  # 전라남도
            [(10, 8), (12, 8), (12, 9), (14, 9), (14, 8), (16, 8), (16, 6)],  # 충청북도
            [(14, 9), (14, 11), (14, 12), (13, 12), (13, 13)],  # 경상북도
            [(15, 8), (17, 8), (17, 10), (16, 10), (16, 11), (14, 11)],  # 대구
            [(17, 9), (18, 9), (18, 8), (19, 8), (19, 9), (20, 9), (20, 10), (21, 10)],  # 부산
            [(16, 11), (16, 13)],  # 울산
            [(27, 5), (27, 6), (25, 6)],
        ]
        gamma = 0.75

        whitelabelmin = 20.

        datalabel = targetData

        tmp_max = max([np.abs(min(blockedMap[targetData])),
                       np.abs(max(blockedMap[targetData]))])
        vmin, vmax = -tmp_max, tmp_max

        mapdata = blockedMap.pivot_table(index='y', columns='x', values=targetData)
        masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)

        plt.figure(figsize=(9, 11))
        plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname,
                   edgecolor='#aaaaaa', linewidth=0.5)

        # 지역 이름 표시
        for idx, row in blockedMap.iterrows():
            # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시한다.
            # (중구, 서구)
            if len(row['ID'].split()) == 2:
                dispname = '{}\n{}'.format(row['ID'].split()[0], row['ID'].split()[1])
            elif row['ID'][:2] == '고성':
                dispname = '고성'
            else:
                dispname = row['ID']

            # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시한다.
            if len(dispname.splitlines()[-1]) >= 3:
                fontsize, linespacing = 10.0, 1.1
            else:
                fontsize, linespacing = 11, 1.

            annocolor = 'white' if np.abs(row[targetData]) > whitelabelmin else 'black'
            plt.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                         fontsize=fontsize, ha='center', va='center', color=annocolor,
                         linespacing=linespacing)

        # 시도 경계 그린다.
        for path in BORDER_LINES:
            ys, xs = zip(*path)
            plt.plot(xs, ys, c='black', lw=2)

        plt.gca().invert_yaxis()

        plt.axis('off')

        cb = plt.colorbar(shrink=.1, aspect=10)
        cb.set_label(datalabel)

        plt.tight_layout()
        plt.show()

    def final(self):
        final_elect_data = self.get_data()
        self.drawKorea('moon_vs_hong', final_elect_data, 'RdBu')
        self.drawKorea('moon_vs_ahn', final_elect_data, 'RdBu')
        self.drawKorea('ahn_vs_hong', final_elect_data, 'RdBu')


if __name__ == '__main__':
    Solution().hook()