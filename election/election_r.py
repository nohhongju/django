import matplotlib
import numpy as np
import pandas as pd
import re
import folium
import warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)
from icecream import ic
from matplotlib import pyplot as plt, font_manager
from context.domains import Reader, File
import platform
import matplotlib.pyplot as plt


class Solution(Reader):
    def __init__(self):
        self.file = File()
        self.file.context = './data/'

    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. preprocess')
            print('2. draw_korea')
            print('3. draw_korea_geo')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            if menu == '1':
                self.preprocess()
            if menu == '2':
                self.draw_korea()
            if menu == '3':
                self.draw_korea_geo()
            elif menu == '0':
                break

    def preprocess(self):
        file = self.file
        file.fname = 'election_result'
        election_result = self.csv(file)
        # ic(election_result.head())
        election_result = self.change_char_sido(election_result)
        election_result = self.calc_percent_vote(election_result)
        file.fname = 'draw_korea'
        draw_korea = self.csv(file)
        # draw_korea.head()
        self.create_final_data(draw_korea, election_result)

    def compare_percent_vote(self, final_elect_data):
        # 문재인 후보와 홍준표 후보의 득표율 차이
        final_elect_data['moon_vs_hong'] = final_elect_data['rate_moon'] - final_elect_data['rate_hong']
        # 문재인 후보와 안철수 후보의 득표율 차이
        final_elect_data['moon_vs_ahn'] = final_elect_data['rate_moon'] - final_elect_data['rate_ahn']
        # 안철수 후보와 홍준표 후보의 득표율 차이
        final_elect_data['ahn_vs_hong'] = final_elect_data['rate_ahn'] - final_elect_data['rate_hong']
        # ic(final_elect_data.head())
        '''
         Unnamed: 0  Unnamed: 0_x   광역시도  ... moon_vs_hong  moon_vs_ahn  ahn_vs_hong
         0           0             0  서울특별시  ...    19.681961    19.693661    -0.011700
         1           1             1  서울특별시  ...    19.505866    17.730411     1.775455
         2           2             2  서울특별시  ...    15.423503    17.530053    -2.106549
         3           3             3  서울특별시  ...    22.699643    20.185554     2.514089
         4           4             4  서울특별시  ...    24.640253    21.950590     2.689664
        '''
        # 문재인 후보와 홍준표 후보의 득표율 차이가 큰 지역들과 작은 지역들을 확인
        # 전라도에서 문재인 후보의 득표율이 압도적으로 높기 때문에, 홍준표 후보와의 득표율 차이가 굉장히 높게 나왔다
        final_elect_data.sort_values(['moon_vs_hong'], ascending=[False]).head(10)
        '''
        Unnamed: 0  Unnamed: 0_x   광역시도  ... moon_vs_hong  moon_vs_ahn  ahn_vs_hong
        181         181           182   전라남도  ...    65.069909    45.282749    19.787160
        165         165           166   전라북도  ...    63.958791    45.331283    18.627508
        164         164           165   전라북도  ...    63.724549    45.320941    18.403608
        63           63            63  광주광역시  ...    62.644384    37.757293    24.887091
        171         171           172   전라북도  ...    62.349928    43.476869    18.873059
        '''
        # 반면, 경상도의 경우에는 홍준표 후보의 득표율이 훨씬 더 높게 나왔다
        final_elect_data.sort_values(['moon_vs_hong'], ascending=[True]).head(10)
        '''
        Unnamed: 0  Unnamed: 0_x  광역시도  ... moon_vs_hong  moon_vs_ahn  ahn_vs_hong
        218         218           219  경상북도  ...   -53.327282     1.770012   -55.097294
        219         219           220  경상북도  ...   -48.672566     1.579712   -50.252278
        222         222           223  경상북도  ...   -47.954067     2.124402   -50.078469
        215         215           216  경상북도  ...   -42.391498     5.152706   -47.544204
        212         212           213  경상북도  ...   -42.342174     2.596190   -44.938364
        '''
        final_elect_data.to_csv('./save/final_elect_data.csv', index=False)
        return final_elect_data

    def create_final_data(self, draw_korea, election_result):
        # draw_korea의 ID와 election_result의 ID가 서로 일치하는 지 확인
        # 두 개를 집합으로 보고, 서로의 차집합을 구해서 둘 다 공집합이면 된다.
        # 집합으로 보기 위해, set() 함수를 사용한다.
        set(draw_korea['ID'].unique()) - set(election_result['ID'].unique())
        set(election_result['ID'].unique()) - set(draw_korea['ID'].unique())

        # '고성'의 경우, 강원도 고성과 경남 고성을 구분 해준다.
        # ic(election_result[election_result['ID'] == '고성'])
        '''
         Unnamed: 0  광역시도   시군      pop    moon     hong     ahn  ID
         125    125   강원도  고성군  18692.0  5664.0   6511.0  3964.0  고성
         233    233  경상남도  고성군  34603.0  9848.0  16797.0  4104.0  고성
        '''
        election_result.loc[125, 'ID'] = '고성(강원)'
        election_result.loc[233, 'ID'] = '고성(경남)'
        # ic(election_result[election_result['시군'] == '고성군'])
        '''
        Unnamed: 0  광역시도   시군      pop    moon     hong     ahn      ID
         125   125   강원도  고성군  18692.0  5664.0   6511.0  3964.0  고성(강원)
         233   233  경상남도  고성군  34603.0  9848.0  16797.0  4104.0  고성(경남)
        '''
        # 창원시 마산합포구는 '합포'라고 줄이고, 창원시 마산회원구는 '회원'이라고 변경한다.
        # ic(election_result[election_result['광역시도'] == '경상남도'])
        '''
        Unnamed: 0  광역시도        시군       pop      moon     hong      ahn       ID
        228    228  경상남도  창원시마산합포구  119281.0   35592.0  54488.0  14686.0  창원 마산합포
        229    229  경상남도  창원시마산회원구  136757.0   45014.0  56340.0  17744.0  창원 마산회원
        '''
        election_result.loc[228, 'ID'] = '창원 합포'
        election_result.loc[229, 'ID'] = '창원 회원'
        # ic(election_result[election_result['광역시도'] == '경상남도'])
        '''
        Unnamed: 0  광역시도        시군       pop      moon     hong      ahn      ID
        228    228  경상남도  창원시마산합포구  119281.0   35592.0  54488.0  14686.0   창원 합포
        229    229  경상남도  창원시마산회원구  136757.0   45014.0  56340.0  17744.0   창원 회원
        '''

        # draw_korea의 데이터에는 부천시의 구가 존재하고, election_result에는 없다.
        # 원칙적으로는 각 동의 인구를 다시 조사하고 이를 엣 지역구에 맞춰야 하지만, 부천시는 단순히 '3'으로 나눠서 진행한다.
        # 단, 득표율인 'rate_moon', 'rate_hong', 'rate_ahn'은 '3'으로 나눌 필요가 없다.

        # ic(election_result[election_result['시군'] == '부천시'])
        '''
        Unnamed: 0 광역시도   시군       pop      moon      hong       ahn  ID
        85      85  경기도  부천시  543777.0  239697.0  100544.0  128297.0  부천
        '''

        # '부천시'는 단순히 '3(소사, 오정, 원미)'으로 나눠서 진행
        ahn_tmp = election_result.loc[85, 'ahn'] / 3
        hong_tmp = election_result.loc[85, 'hong'] / 3
        moon_tmp = election_result.loc[85, 'moon'] / 3
        pop_tmp = election_result.loc[85, 'pop'] / 3

        # 단, 득표율은 '3'으로 나눠 주지 않는다
        rate_moon_tmp = election_result.loc[85, 'rate_moon']
        rate_hong_tmp = election_result.loc[85, 'rate_hong']
        rate_ahn_tmp = election_result.loc[85, 'rate_ahn']

        election_result.loc[250] = [250, '경기도', '부천시',
                                    pop_tmp, moon_tmp, hong_tmp, ahn_tmp, '부천 소사',
                                    rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp]
        election_result.loc[251] = [251, '경기도', '부천시',
                                    pop_tmp, moon_tmp, hong_tmp, ahn_tmp, '부천 오정',
                                    rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp]
        election_result.loc[252] = [252, '경기도', '부천시',
                                    pop_tmp, moon_tmp, hong_tmp, ahn_tmp, '부천 원미',
                                    rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp]

        # 이제 남아 있는 '[85]부천시'는 제거한다.
        election_result.drop([85], inplace=True)

        # 다시 한 번 draw_korea의 ID와 election_result의 ID가 서로 일치하는 지 확인한다.
        set(draw_korea['ID'].unique()) - set(election_result['ID'].unique())
        set(election_result['ID'].unique()) - set(draw_korea['ID'].unique())

        # election_result와 draw_korea를 merge()를 사용해서 최종 데이터 셋을 생성한다.
        final_elect_data = pd.merge(election_result, draw_korea, how='left', on=['ID'])
        # ic(final_elect_data.head())
        final_elect_data = self.compare_percent_vote(final_elect_data)

        return final_elect_data

    # '중구', '남구'와 같은 두 글자 이름은 그대로 보내고, '중랑구', '서초구'와 같은 두 글자 이상의 이름은 '중랑', '서초'와 같이 줄인다.
    def cut_char_sigu(self, name):
        return name if len(name) == 2 else name[:-1]

    def change_char_sido(self, election_result):
        # '광역시도' 이름에서 앞 두글자 따오기
        sido_candi = election_result['광역시도']
        sido_candi = [name[:2] if name[:2] in ['서울', '부산', '대구', '광주', '인천', '대전', '울산']
                      else '' for name in sido_candi]
        '''
       Unnamed: 0   광역시도   시군       pop      moon     hong      ahn
                        0           0  서울특별시  종로구  102566.0   42512.0  22325.0  22313.0
                        1           1  서울특별시   중구   82852.0   34062.0  17901.0  19372.0
                        2           2  서울특별시  용산구  148157.0   58081.0  35230.0  32109.0
                        3           3  서울특별시  성동구  203175.0   86686.0  40566.0  45674.0
                        4           4  서울특별시  광진구  240030.0  105512.0  46368.0  52824.0
        '''

        # 광역시가 아닌 '시군'에 대해 '안양 만안', '안양 동안'과 같이 정리한다.
        sigun_candi = [''] * len(election_result)
        for n in election_result.index:
            each = election_result['시군'][n]
            if each[:2] in ['수원', '성남', '안양', '안산', '고양',
                            '용인', '청주', '천안', '전주', '포항', '창원']:
                sigun_candi[n] = re.split('시', each)[0] + ' ' + \
                                 self.cut_char_sigu(re.split('시', each)[1])
            else:
                sigun_candi[n] = self.cut_char_sigu(each)
        # ic(sigun_candi)

        # sido_candi 변수에서 그냥 공란이 있으면 첫 글자가 띄어쓰기가 될 수 있다.
        # 따라서 첫 글자가 공백인 경우, 그 다음 글자부터 읽어오도록 한다.
        # 또한, '세종시'의 경우는 예외로 따로 처리해준다.
        ID_candi = [sido_candi[n] + ' ' + sigun_candi[n] for n in range(0, len(sigun_candi))]
        ID_candi = [name[1:] if name[0] == ' ' else name for name in ID_candi]
        ID_candi = [name[:2] if name[:2] == '세종' else name for name in ID_candi]
        election_result['ID'] = ID_candi
        # ic(election_result.head(10))
        return election_result

    def calc_percent_vote(self, election_result):
        # 득표율 = 득표수 / 투표자수
        # 문재인, 홍준표, 안철수 후보의 득표율 계산
        election_result[['rate_moon', 'rate_hong', 'rate_ahn']] = election_result[['moon', 'hong', 'ahn']] \
            .div(election_result['pop'], axis=0)
        election_result[['rate_moon', 'rate_hong', 'rate_ahn']] *= 100
        # ic(election_result.head())
        '''
         Unnamed: 0   광역시도   시군       pop  ...     ID  rate_moon  rate_hong   rate_ahn
        0           0  서울특별시  종로구  102566.0  ...  서울 종로  41.448433  21.766472  21.754773
        1           1  서울특별시   중구   82852.0  ...  서울 중구  41.111862  21.605996  23.381451
        2           2  서울특별시  용산구  148157.0  ...  서울 용산  39.202333  23.778829  21.672280
        3           3  서울특별시  성동구  203175.0  ...  서울 성동  42.665682  19.966039  22.480128
        4           4  서울특별시  광진구  240030.0  ...  서울 광진  43.957839  19.317585  22.007249
        '''

        # 문재인 후보가 높은 비율로 득표한 지역 확인
        election_result.sort_values(['rate_moon'], ascending=[False]).head(10)
        '''
             Unnamed: 0   광역시도      시군  ...  rate_moon  rate_hong   rate_ahn
        182         182   전라남도     순천시  ...  67.563695   2.493786  22.280946
        166         166   전라북도  전주시덕진구  ...  66.716865   2.758074  21.385582
        165         165   전라북도  전주시완산구  ...  66.687114   2.962565  21.366173
        175         175   전라북도     장수군  ...  66.633497   4.459233  20.853287
        184         184   전라남도     광양시  ...  65.927955   4.253818  20.833333                                                  
        '''
        # 홍준표 후보가 높은 비율로 득표한 지역 확인
        election_result.sort_values(['rate_hong'], ascending=[False]).head(10)
        '''
         Unnamed: 0  광역시도   시군      pop  ...  ID  rate_moon  rate_hong   rate_ahn
        219         219  경상북도  군위군  17627.0  ...  군위  12.770182  66.097464  11.000170
        220         220  경상북도  의성군  37855.0  ...  의성  14.172500  62.845067  12.592788
        223         223  경상북도  영덕군  26125.0  ...  영덕  14.491866  62.445933  12.367464
        247         247  경상남도  합천군  33021.0  ...  합천  21.631689  59.655976   9.318313
        216         216  경상북도  고령군  22396.0  ...  고령  16.761922  59.153420  11.609216
        '''
        # 안철수 후보가 높은 비율로 득표한 지역 확인
        election_result.sort_values(['rate_ahn'], ascending=[False]).head(10)
        '''
         Unnamed: 0   광역시도   시군       pop  ...     ID  rate_moon  rate_hong   rate_ahn
       196         196   전라남도  진도군   21189.0  ...     진도  49.044315   2.411629  41.790552
       201         201   전라남도  신안군   28950.0  ...     신안  49.637306   2.462867  41.450777
       193         193   전라남도  강진군   25175.0  ...     강진  49.557100   2.991063  40.325720
       195         195   전라남도  해남군   48351.0  ...     해남  53.568696   2.394987  37.552481
       197         197   전라남도  영암군   36402.0  ...     영암  52.192187   2.266359  37.388056
        '''
        return election_result

    def visualize_percent_vote(self, target_data, blocked_map, cmap_name):
        BORDER_LINES = [
            [(5, 1), (5, 2), (7, 2), (7, 3), (11, 3), (11, 0)],  # 인천
            [(5, 4), (5, 5), (2, 5), (2, 7), (4, 7), (4, 9), (7, 9),(7, 7), (9, 7), (9, 5), (10, 5), (10, 4), (5, 4)],  # 서울
            [(1, 7), (1, 8), (3, 8), (3, 10), (10, 10), (10, 7),(12, 7), (12, 6), (11, 6), (11, 5), (12, 5), (12, 4),(11, 4), (11, 3)],  # 경기도
            [(8, 10), (8, 11), (6, 11), (6, 12)],  # 강원도
            [(12, 5), (13, 5), (13, 4), (14, 4), (14, 5), (15, 5),(15, 4), (16, 4), (16, 2)],  # 충청북도
            [(16, 4), (17, 4), (17, 5), (16, 5), (16, 6), (19, 6),(19, 5), (20, 5), (20, 4), (21, 4), (21, 3), (19, 3), (19, 1)],  # 전라북도
            [(13, 5), (13, 6), (16, 6)],  # 대전시
            [(13, 5), (14, 5)],  # 세종시
            [(21, 2), (21, 3), (22, 3), (22, 4), (24, 4), (24, 2), (21, 2)],  # 광주
            [(20, 5), (21, 5), (21, 6), (23, 6)],  # 전라남도
            [(10, 8), (12, 8), (12, 9), (14, 9), (14, 8), (16, 8), (16, 6)],  # 충청북도
            [(14, 9), (14, 11), (14, 12), (13, 12), (13, 13)],  # 경상북도
            [(15, 8), (17, 8), (17, 10), (16, 10), (16, 11), (14, 11)],  # 대구
            [(17, 9), (18, 9), (18, 8), (19, 8), (19, 9), (20, 9), (20, 10), (21, 10)],  # 부산
            [(16, 11), (16, 13)],  # 울산
            [(27, 5), (27, 6), (25, 6)]]

        gamma = 0.75
        whitelabelmin = 20.
        datalabel = target_data
        tmp_max = max([np.abs(min(blocked_map[target_data])), np.abs(max(blocked_map[target_data]))])
        vmin, vmax = -tmp_max, tmp_max

        mapdata = blocked_map.pivot_table(index='y', columns='x', values=target_data)
        masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)

        plt.figure(figsize=(9, 11))
        plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmap_name,
                   edgecolor='#aaaaaa', linewidth=0.5)

        # 지역 이름 표시
        for idx, row in blocked_map.iterrows():
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

            annocolor = 'white' if np.abs(row[target_data]) > whitelabelmin else 'black'
            plt.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                         fontsize=fontsize, ha='center', va='center', color=annocolor,
                         linespacing=linespacing)

        # 시도 경계 그린다.
        for path in BORDER_LINES:
            ys, xs = zip(*path)
            plt.plot(xs, ys, c='black', lw=2)

        plt.gca().invert_yaxis()

        plt.axis('off')

        cb = plt.colorbar(shrink=0.1, aspect=10)
        cb.set_label(datalabel)

        plt.tight_layout()
        plt.show()

    def draw_korea(self):
        # 한글 깨짐 문제
        path = "c:\Windows\Fonts\gulim.ttc"
        font_name = font_manager.FontProperties(fname=path).get_name()
        matplotlib.rc('font', family=font_name)

        file = self.file
        file.fname = 'final_elect_data'
        self.file.context = './save/'
        final_elect_data = self.csv(file)
        # "문재인 후보 vs 홍준표 후보" 득표율 격차를 시각화
        self.visualize_percent_vote('moon_vs_hong', final_elect_data, 'RdBu')
        # "문재인 후보 vs 안철수 후보" 득표율 격차를 시각화
        self.visualize_percent_vote('moon_vs_ahn', final_elect_data, 'RdBu')
        # "안철수 후보 vs 홍준표 후보" 득표율 격차를 시각화
        self.visualize_percent_vote('ahn_vs_hong', final_elect_data, 'RdBu')

    def draw_korea_geo(self):
        file = self.file
        file.fname = 'final_elect_data'
        self.file.context = './save/'
        final_elect_data = self.csv(file)
        self.file.context = './data/'
        file.fname = 'skorea_municipalities_geo_simple'
        geo_path = self.mpa_json(file)

        # Folium을 사용해서 득표율 격차를 지도에 시각화
        # 'ID'를 index로
        pop_folium = final_elect_data.set_index('ID')
        # '광역시도', '시군' 변수는 필요가 없으니 삭제
        del pop_folium['광역시도']
        del pop_folium['시군']
        pop_folium.head()
        map = folium.Map(location=[36.2002, 127.054], zoom_start=6)
        # "문재인 후보 vs 홍준표 후보" 득표율 격차 시각화
        map.choropleth(geo_data=geo_path,
                       data=pop_folium['moon_vs_hong'],
                       columns=[pop_folium.index, pop_folium['moon_vs_hong']],
                       fill_color='PuBu',  # 'PuRd', 'YlGnBu'
                       key_on='feature.id')
        map.save('./save/moon_vs_hong_map.html')
        # "문재인 후보 vs 안철수 후보" 득표율 격차 시각화
        map.choropleth(geo_data=geo_path,
                       data=pop_folium['moon_vs_ahn'],
                       columns=[pop_folium.index, pop_folium['moon_vs_ahn']],
                       fill_color='PuBu',  # 'PuRd', 'YlGnBu'
                       key_on='feature.id')
        map.save('./save/moon_vs_ahn_map.html')
        # "안철수 후보 vs 홍준표 후보" 득표율 격차 시각화
        map.choropleth(geo_data=geo_path,
                       data=pop_folium['ahn_vs_hong'],
                       columns=[pop_folium.index, pop_folium['ahn_vs_hong']],
                       fill_color='PuBu',  # 'PuRd', 'YlGnBu'
                       key_on='feature.id')
        map.save('./save/ahn_vs_hong_map.html')


if __name__ == '__main__':
    Solution().hook()
