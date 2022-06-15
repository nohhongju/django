from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from icecream import ic

from context.domains import Reader, File


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
                self.crawling()
            if menu == '2':
                self.preprocess()
            if menu == '3':
                self.token_embedding()
            elif menu == '4':
                Solution.download()

    def preprocess(self):  # 데이터를 수집해서 가져오는 일
        df = self.stereotype()
        ic(df.head(5))
        print('네이버의 ')

    def crawling(self):
        file = self.file
        file.fname = 'movie_reviews.txt'
        path = self.new_file(file)
        f = open(path, 'w', encoding='UTF-8')

        # -- 500페이지까지 크롤링
        for no in range(1, 501):
            url = 'https://movie.naver.com/movie/point/af/list.naver?&page=%d' % no
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')

            reviews = soup.select('tbody > tr > td.title')
            for rev in reviews:
                title = rev.select_one('a.movie').text.strip()
                score = rev.select_one('div.list_netizen_score > em').text.strip()
                comment = rev.select_one('br').next_sibling.strip()

                # -- 긍정/부정 리뷰 레이블 설정
                if int(score) >= 8:
                    label = 1  # -- 긍정 리뷰 (8~10점)
                elif int(score) <= 4:
                    label = 0  # -- 부정 리뷰 (0~4점)
                else:
                    label = 2

                f.write(f'{title}\t{score}\t{comment}\t{label}\n')
        f.close()

    def stereotype(self):
        file = self.file
        file.fname = 'movie_reviews.txt'
        path = self.new_file(file)
        data = pd.read_csv(path, delimiter='\t',
                           names=['title', 'score', 'comment', 'label'])  # -- 본인 환경에 맞게 설치 경로 변경할 것
        # print(df_data.head(10))
        # print(df_data.info())
        return pd.DataFrame(data)

    def review(self):
        pass

    def tokenization(self):
        pass

    def embedding(self):
        pass

    def remove_comments(self):
        df_data = self.stereotype()
        # 코멘트가 없는 리뷰 데이터(NaN) 제거
        df_reviews = df_data.dropna()
        # 중복 리뷰 제거
        df_reviews = df_reviews.drop_duplicates(['comment'])

        # print(df_reviews.info())
        # print(df_reviews.head(10))
        return df_reviews

    def move_list(self):
        df_reviews = self.remove_comments()
        movie_lst = df_reviews.title.unique()
        print('전체 영화 편수 =', len(movie_lst))
        print(movie_lst[:10])

        cnt_movie = df_reviews.title.value_counts()
        print(cnt_movie[:20])


    def info_movie(self):
        df_reviews = self.remove_comments()
        info_movie = df_reviews.groupby('title')['score'].describe()
        print(info_movie.sort_values(by=['count'], axis=0, ascending=False))


if __name__ == '__main__':
    Solution().hook()