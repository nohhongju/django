import numpy as np
import pandas as pd
from context.domains import Reader, File
import googlemaps
import folium
from sklearn import preprocessing

class Solution(Reader):
    def __init__(self):
        self.file = File()
        self.file.context = './data/'
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']

    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. crime_in_seoul.csv, 구글맵 API 를 이용해서 서울시내 경찰서 주소목록파일을 작성하시오.')
            print('2. us-states.json, us_unemployment.csv 를 이용해서 미국 실업률 지도를 작성하시오.')
            print('3. cctv_in_seoul.csv, pop_in_seoul.csv 를 이용해서 서울시내 경찰서 주소목록파일(cctv_pop.csv)을 작성하시오.')
            print('4. ')
            print('5. 주어진 데이터를 활용해서 서울시내 경찰서 범죄발생과 검거율 현황지도(폴리움)를 작성하시오 ')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            if menu == '1':
                self.save_police_pos()
            if menu == '2':
                self.folium_test()
            if menu == '3':
                self.save_cctv_pos()
            if menu == '4':
                self.save_police_norm()
            if menu == '5':
                self.draw_crime_map()
            elif menu == '0':
                break

    def save_police_pos(self):
        file = self.file
        file.fname = 'crime_in_seoul'
        crime = self.csv(file)
        print('********')
        # print(crime)
        station_names = []
        for name in crime['관서명']:
            station_names.append(f'서울{str(name[:-1])}경찰서')
        # print(f'station_names range: {len(station_names)}')
        ''' 서울시내 경찰서는 31개이다. '''
        # print([{i:name} for i, name in enumerate(station_names) ])
        '''
        [{0: '서울중부경찰서'}, {1: '서울종로경찰서'}, {2: '서울남대문경찰서'}, ... , {21: '서울종암경찰서'}
        '''
        gmaps = self.gmaps()

        '''
        a = gmaps.geocode('서울중부경찰서', language='ko')
        print(a)
        [{'address_components': 
            [{'long_name': '２７', 'short_name': '２７', 'types': ['premise']}, 
            {'long_name': '수표로', 'short_name': '수표로', 'types': ['political', 'sublocality', 'sublocality_level_4']}, 
            {'long_name': '중구', 'short_name': '중구', 'types': ['political', 'sublocality', 'sublocality_level_1']}, 
            {'long_name': '서울특별시', 'short_name': '서울특별시', 'types': ['administrative_area_level_1', 'political']}, 
            {'long_name': '대한민국', 'short_name': 'KR', 'types': ['country', 'political']}, 
            {'long_name': '100-032', 'short_name': '100-032', 'types': ['postal_code']}], 
            'formatted_address': '대한민국 서울특별시 중구 수표로 27', 
            'geometry': {'location': 
                {'lat': 37.56361709999999, 'lng': 126.9896517}, 
                'location_type': 'ROOFTOP', 
                'viewport': {'northeast': {'lat': 37.5649660802915, 'lng': 126.9910006802915}, 
                'southwest': {'lat': 37.5622681197085, 'lng': 126.9883027197085}}}, 
                'partial_match': True, 'place_id': 'ChIJc-9q5uSifDURLhQmr5wkXmc', 
                'plus_code': {'compound_code': 'HX7Q+CV 대한민국 서울특별시', 'global_code': '8Q98HX7Q+CV'}, 
                'types': ['establishment', 'point_of_interest', 'police']}]
        서울종암경찰서는 2021.12.20부터 이전함
        '''

        station_addrs = []
        station_lats = []
        station_lngs = []

        for i, name in enumerate(station_names):
            if name != '서울종암경찰서':
                temp = gmaps.geocode(name, language='ko')
            else:
                temp = [{'address_components':
                     [{'long_name': '32', 'short_name': '32', 'types': ['premise']},
                      {'long_name': '화랑로7길', 'short_name': '화랑로7길',
                       'types': ['political', 'sublocality', 'sublocality_level_4']},
                      {'long_name': '성북구', 'short_name': '성북구',
                       'types': ['political', 'sublocality', 'sublocality_level_1']},
                      {'long_name': '서울특별시', 'short_name': '서울특별시',
                       'types': ['administrative_area_level_1', 'political']},
                      {'long_name': '대한민국', 'short_name': 'KR', 'types': ['country', 'political']},
                      {'long_name': '100-032', 'short_name': '100-032', 'types': ['postal_code']}],
                         'formatted_address': '대한민국 서울특별시 성북구 화랑로7길 32',
                         'geometry': {'location':
                                          {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                                      'location_type': 'ROOFTOP',
                                      'viewport': {'northeast': {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                                                   'southwest': {'lat': 37.60388169879458, 'lng': 127.04001571848704}}},
                         'partial_match': True, 'place_id': 'ChIJc-9q5uSifDURLhQmr5wkXmc',
                         'plus_code': {'compound_code': 'HX7Q+CV 대한민국 서울특별시', 'global_code': '8Q98HX7Q+CV'},
                         'types': ['establishment', 'point_of_interest', 'police']}]
            # print(f'name {i} = {temp[0].get("formatted_address")}')
            '''
            0번 중부서인경우는 "대한민국 서울특별시 중구 수표로 27" 이 담긴다.
            1번 종로서인경우는 "대한민국 서울특별시 종로구 율곡로 46" 이 담긴다.
            '''
            station_addrs.append(temp[0].get('formatted_address'))
            t_loc = temp[0].get('geometry')
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])

        gu_names = []
        for name in station_addrs:
            temp = name.split()
            # temp = ['대한민국', '서울특별시', '중구', '수표로', '27']
            gu_name = [gu for gu in temp if gu[-1] == '구'][0]
            gu_names.append(gu_name)
        crime['구별'] = gu_names
        # print(crime)

        # for name in crime['구별']:
        #     print(name)

        crime.to_csv('./save/police_pos.csv', index=False)  # index 랜덤생성 방지



    def save_cctv_pos(self):
        file = self.file
        file.fname = 'cctv_in_seoul'
        cctv = self.csv(file)
        file.fname = 'pop_in_seoul'
        pop = self.xls(file, 1, 'B,D,G,J,N', 2)  # fname, header, skiprows, cols
        '''
             기관명    소계  2013년도 이전  2014년  2015년  2016년
        0    강남구  2780       1292       430    584    932
        1    강동구   773        379        99    155    377
        2    강북구   748        369       120    138    204
        3    강서구   884        388       258    184     81

        '''
        cctv.rename(columns={'기관명': '구별'}, inplace=True)
        cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis=1, inplace=True)
        print(cctv)

        '''
             자치구          합계        한국인     등록외국인   65세이상고령자
        0     합계        10197604.0  9926968.0  270636.0  1321458.0
        1    종로구        162820.0   153589.0    9231.0    25425.0
        2     중구        133240.0   124312.0    8928.0    20764.0
        3    용산구        244203.0   229456.0   14747.0    36231.0
        4    성동구        311244.0   303380.0    7864.0    39997.0

        '''
        pop.rename(columns={pop.columns[0]: '구별',
                            '합계': '인구수',
                            '등록외국인': '외국인',
                            '65세이상고령자': '고령자'}, inplace=True)  # inplace는 원본을 수정할지의 여부
        # pop 에서 26   NaN         NaN        NaN       NaN        NaN 을 제거하시오
        # pop.dropna(how='all', inplace=True) # 전부 NaN값이면 날림
        pop.drop([26], inplace=True)
        pop['외국인비율'] = pop['외국인'].astype(int) / pop['인구수'].astype(int) * 100  # .astype(int) - int로 바꿔줌
        pop['고령자비율'] = pop['고령자'].astype(int) / pop['인구수'].astype(int) * 100

        cctv_pop = pd.merge(cctv, pop, on='구별', how='outer')

        cor1 = np.corrcoef(cctv_pop['고령자비율'], cctv_pop['소계'])
        cor2 = np.corrcoef(cctv_pop['외국인비율'], cctv_pop['소계'])
        print(f'고령자비율과 CCTV의 상관계수 {str(cor1)} \n'
              f'외국인비율과 CCTV의 상관계수 {str(cor2)} ')
        """
         고령자비율과 CCTV 의 상관계수 [[ 1.         -0.28078554]
                                     [-0.28078554  1.        ]] 
         외국인비율과 CCTV 의 상관계수 [[ 1.         -0.13607433]
                                     [-0.13607433  1.        ]]
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        고령자비율 과 CCTV 상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
                                    [-0.28078554  1.        ]]
        외국인비율 과 CCTV 상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
                                    [-0.13607433  1.        ]]                        
         """
        cctv_pop.to_csv('./save/cctv_pop.csv')

    def save_police_norm(self):  # rescalring
        file = self.file
        file.context = './data/'
        file.fname = 'crime_in_seoul'
        crime_in_seoul = self.csv(file)
        # print(crime_in_seoul)
        '''
                관서명  살인 발생  살인 검거  강도 발생  강도 검거  강간 발생  강간 검거  절도 발생  절도 검거  폭력 발생  폭력 검거
           0    중부서      2      2           3      2        105         65      1395      477      1355     1170
           1    종로서      3      3           6      5        115         98      1070      413      1278     1070
        '''
        file.context = './save/'
        file.fname = 'police_pos'
        police_pos = self.csv(file)
        police = pd.pivot_table(police_pos, index='구별', aggfunc=np.sum)
        police['살인검거율'] = police['살인 검거'].astype(int) / police['살인 발생'].astype(int) * 100
        police['강도검거율'] = police['강도 검거'].astype(int) / police['강도 발생'].astype(int) * 100
        police['강간검거율'] = police['강간 검거'].astype(int) / police['강간 발생'].astype(int) * 100
        police['절도검거율'] = police['절도 검거'].astype(int) / police['절도 발생'].astype(int) * 100
        police['폭력검거율'] = police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int) * 100
        police.drop(columns={'살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거'}, axis=1, inplace=True)  # axis=0 행방향, axis=1 열방향

        for i in self.crime_rate_columns:
            # loc() 는 데이터프레임의 행이나 컬럼에 index로 접근한다.
            # 그래서 police[i] 로 접근하도록 한다.
            police[i].loc[police[i] > 100] = 100  # 데이터값의 기간 오류로 100을 넘으면 100으로 계산
        police.to_csv('./save/police.csv', sep=',', encoding='UTF-8')
        police.rename(columns={
            '살인 발생': '살인',
            '강도 발생': '강도',
            '강간 발생': '강간',
            '절도 발생': '절도',
            '폭력 발생': '폭력'
        }, inplace=True)
        print(police)
        '''
             Unnamed: 0   강간   강도   살인  ...       강도검거율       강간검거율       절도검거율       폭력검거율
           구별                               ...                                                
           강남구           47  449   21   13  ...   85.714286   77.728285   42.857143   86.484594
           강동구          100  100  100  100  ...  100.000000  100.000000  100.000000  100.000000
        '''
        x = police[self.crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """     
        피쳐 스케일링(Feature scalining)은 해당 피쳐들의 값을 일정한 수준으로 맞춰주는 것이다.
        이때 적용되는 스케일링 방법이 표준화(standardization) 와 정규화(normalization)다.

        1단계: 표준화(공통 척도)를 진행한다.
            표준화는 정규분포를 데이터의 평균을 0, 분산이 1인 표준정규분포로 만드는 것이다.
            x = (x - mu) / sigma
            scale = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
        2단계: 이상치 발견 및 제거
        3단계: 정규화(공통 간격)를 진행한다.
            정규화에는 평균 정규화, 최소-최대 정규화, 분위수 정규화가 있다.
             * 최소최대 정규화는 모든 데이터를 최대값을 1, 최솟값을 0으로 만드는 것이다.
            도메인은 데이터의 범위이다.
            스케일은 데이터의 분포이다.
            목적은 도메인을 일치시키거나 스케일을 유사하게 만든다.     
        """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        police_norm = pd.DataFrame(x_scaled, columns=self.crime_columns, index=police.index)
        police_norm[self.crime_rate_columns] = police[self.crime_rate_columns]
        police_norm['범죄'] = np.sum(police_norm[self.crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[self.crime_columns], axis=1)
        police_norm.to_csv('./save/police_norm.csv', sep=',', encoding='UTF-8')




    def folium_test(self):
        file = self.file
        file.fname = 'us-states.json'
        # states = self.json(file)
        states = self.new_file(file)
        file.fname = 'us_unemployment'
        unemployment = self.csv(file)

        bins = list(unemployment["Unemployment"].quantile([0, 0.25, 0.5, 0.75, 1]))
        m = folium.Map(location=[39, -97], zoom_start=5)
        folium.Choropleth(
            geo_data=states, # dataframe 이 아님
            name="choropleth",
            data=unemployment,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name="Unemployment Rate (%)",
            bins=bins,
            reset=True
        ).add_to(m)
        m.save("./save/folium_test.html")

    def draw_crime_map(self):
        file = self.file
        file.context = './data/'
        file.fname = 'geo_simple'  # 서울시지도 geo_simple.json
        seoul_map = self.map_json(file)
        print(seoul_map)
        # 범죄현황 데이터 crime_in_seoul.csv
        file.fname = 'crime_in_seoul'
        crime = self.csv(file)
        file.context = './save/'
        # 검거율 정규화 데이터 police_norm.csv
        file.fname = 'police_norm'
        police_norm = self.csv(file)
        # 경찰서위치 police_pos.csv
        file.fname = 'police_pos'
        police_pos = self.csv(file)
        station_names = []
        for name in crime['관서명']:
            station_names.append(f'서울{str(name[:-1])}경찰서')

        gmaps = self.gmaps()
        station_addrs = []
        station_lats = []
        station_lngs = []

        for i, name in enumerate(station_names):
            if name != '서울종암경찰서':
                temp = gmaps.geocode(name, language='ko')
            else:
                temp = self.jongam_police_info()
            station_addrs.append(temp[0].get('formatted_address'))
            t_loc = temp[0].get('geometry')
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])
        police_pos['lat'] = station_lats
        police_pos['lng'] = station_lngs
        col = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
        tmp = police_pos[col] / police_pos[col].max()
        police_pos['검거'] = np.sum(tmp, axis=1)
        folium_map = folium.Map(location=[37.5502, 126.982], zoom_start=12, title='Stamen Toner')

        folium.Choropleth(
            geo_data=seoul_map,
            data=tuple(zip(police_norm['구별'], police_norm['범죄'])),
            columns=["State", "Crime Rate"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Crime Rate (%)",
            reset=True,
        ).add_to(folium_map)
        for i in police_pos.index:
            folium.CircleMarker([police_pos['lat'][i], police_pos['lng'][i]],
                                radius=police_pos['검거'][i] * 10,
                                fill_color='#0a0a32').add_to(folium_map)

        folium_map.save('./save/crime_map.html')

    def jongam_police_info(self):
        return [{'address_components':
                 [{'long_name': '32', 'short_name': '32', 'types': ['premise']},
                  {'long_name': '화랑로7길', 'short_name': '화랑로7길',
                   'types': ['political', 'sublocality', 'sublocality_level_4']},
                  {'long_name': '성북구', 'short_name': '성북구',
                   'types': ['political', 'sublocality', 'sublocality_level_1']},
                  {'long_name': '서울특별시', 'short_name': '서울특별시',
                   'types': ['administrative_area_level_1', 'political']},
                  {'long_name': '대한민국', 'short_name': 'KR', 'types': ['country', 'political']},
                  {'long_name': '100-032', 'short_name': '100-032', 'types': ['postal_code']}],
                    'formatted_address': '대한민국 서울특별시 성북구 화랑로7길 32',
                    'geometry': {'location':
                    {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                    'location_type': 'ROOFTOP',
                    'viewport': {'northeast': {'lat': 37.60388169879458, 'lng': 127.04001571848704},
                    'southwest': {'lat': 37.60388169879458, 'lng': 127.04001571848704}}},
                'partial_match': True, 'place_id': 'ChIJc-9q5uSifDURLhQmr5wkXmc',
                'plus_code': {'compound_code': 'HX7Q+CV 대한민국 서울특별시', 'global_code': '8Q98HX7Q+CV'},
                'types': ['establishment', 'point_of_interest', 'police']}]


if __name__ == '__main__':
    Solution().hook()
