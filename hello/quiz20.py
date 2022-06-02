import random
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

from hello import Quiz00
from hello.domains import myRandom, members, myMember


class Quiz20:

    def quiz20list(self) -> str:
        list1 = [1, 2, 3, 4]
        print(list1, type(list1))
        print(list1[0], list1[-1], list1[-2], list1[1:3])

        list2 = ['math', 'english']
        print(list2[0])
        print(list2[0][1])

        list3 = [1, '2', [1, 2, 3]]
        print(list3)

        list4 = [1, 2, 3]
        list5 = [4, 5]
        print(list4 + list5)
        print(2 * list4)

        list4.append(list5)
        print(list4)

        list4[-2] = []
        print(list4)

        a = [1, 2]
        b = [0, 5]
        c = [a, b]
        print(c)

        print(c[0][1])

        c[0][1] = 10
        print(c)

        a = range(10)
        print(a)

        print(sum(a))

        b = [2, 10, 0, -2]
        print(sorted(b))

        b.index(0)
        len(b)
        print(b.index(0), len(b))
        return None

    def quiz21tuple(self) -> str:
        a = (1, 2)
        print(a, type(a))

        a[0] = 4

        a = (1, 2)
        b = (0, (1, 4))
        print(a + b)
        return None

    def quiz22dict(self) -> str:
        a = {"class": ['deep learning', 'machine learning'], "num_students": [40, 20]}

        print(type(a))

        print(a["class"])

        a['grade'] = ['A', 'B', 'C']
        print(a)

        print(a.keys())

        print(list(a.keys()))

        print(a.values())

        print(a.ltems)

        print(a.get('class'))

        print("class" in a)
        return None

    def quiz23listcom(self) -> str:
        print('---------legacy---------')
        a = []
        for i in range(5):
            a.append(i)
        print(a)
        print('------comprehension------')
        a2 = [i for i in range(5)]
        print(a2)
        return None

    def quiz24zip(self) -> {}:
        url = 'https://music.bugs.co.kr/chart/track/realtime/total'
        html_doc = urlopen(url)
        soup = BeautifulSoup(html_doc, 'lxml') # html.parser VS lxml
        ls1 = self.find_music(soup, 'p', 'class', 'title')
        ls2 = self.find_music(soup, 'p', 'class', 'artist')
        d = {i: j for i, j in zip(ls1, ls2)}
        l = [i + j for i, j in zip(ls1, ls2)]
        l2 = list(zip(ls1, ls2))
        d1 = dict(zip(ls1, ls2))
        print(d)
        # self.dict1(ls1, ls2)
        # self.dict2(ls1, ls2)
        # self.dict3(ls1, ls2)
        return d

    def quiz27melon(self) -> str:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://www.melon.com/chart/index.htm?dayTime=2022030816'
        req = urllib.request.Request(url, headers=headers)
        soup = BeautifulSoup(urlopen(req).read(), 'lxml')
        ls1 = self.find_music(soup, 'div', 'class', 'ellipsis rank01')
        ls2 = self.find_music(soup, 'span', 'class', 'checkEllipsis')
        dict = {}
        # self.dict1(ls1, ls2)
        # self.dict2(ls1, ls2)
        return dict

    @staticmethod
    def dict1(ls1, ls2) -> None:
        dict = {}
        for i in range(0, len(ls1)):
            print(type(f'타입: {ls1[i]}'))
            dict[ls1[i]] = ls2[i]
        print(dict)

    @staticmethod
    def dict2(ls1, ls2) -> None:
        dict = {}
        for i, j in enumerate(ls1):
            dict[j] = ls2[i]
        print(dict)

    @staticmethod
    def dict3(ls1, ls2) -> None:
        dict = {}
        for i, j in zip(ls1, ls2):
            dict[i] = j
        print(dict)

    '''def print_music_list(self, soup) -> None:
        artists = soup.find_all('p', {'class': 'artist'})
        artists = [i.get_text() for i in artists]
        # print(''.join(i for i in artists))
        # print(type(artists))
        # print(soup.prettify())
        titles = soup.find_all('p', {'class': 'title'})
        titles = [i.get_text() for i in titles]
        # print(''.join(i for i in titles))

        for i, j in enumerate(['artist', 'title']):
            print(''.join(i for i in [i for i in self.find_music(soup, j)]))
        # a = [i for i in self.bugs(soup, 'artist')]
        # a = [i for i in self.bugs(soup, 'title')]'''

    def find_rank(self, soup):
        for i, j in enumerate(['artist', 'title']):
            for i, j in enumerate(self.find_music(soup, j)):
                print(f'{i}위: {j}')

    @staticmethod
    def find_music(soup, a, b, cls_nm) -> []:
        ls = soup.find_all(a, {b: cls_nm})
        return [i.get_text() for i in ls]
        # print(''.join(i for i in ls))

    def quiz25dictcom(self) -> None:
        # students = random.sample(members(), 5)
        b = set([myMember() for i in range(5)])
        print(f'set len : {len(b)}')
        while len(b) != 5:
            b.add(myMember())
        students = list(b)
        scores = [myRandom(0, 100) for i in range(5)]
        a = {i: j for i, j in zip(students, scores)}
        print(f'dict: {a}')

    def quiz26map(self) -> str: return None

    def quiz28dataframe(self) -> None:
        dict = self.quiz24zip()
        df = pd.DataFrame.from_dict(dict, orient='index')
        print(df)
        df.to_csv('./save/bugs.csv', sep=',', na_rep='NaN')

    '''
    다음 결과 출력
        a   b   c
    1   1   3   5
    2   2   4   6
    '''
    def quiz29_pandas_01(self) -> object:
        d1 = {'a': [1, 2], 'b': [3, 4], 'c': [5, 6]}
        d1_1 = ['1', '2']
        df1 = pd.DataFrame(d1, d1_1)
        '''
           a  b  c
        1  1  3  5
        2  2  4  6
        '''

        d2 = {"1": [1, 3, 5], "2": [2, 4, 6]}
        df2 = pd.DataFrame.from_dict(d2, orient='index', columns=['a', 'b', 'c'])
        c = [chr(i) for i in range(97, 100)] #['a', 'b', 'c']
        d3 = {"1": [1, 3, 5]}
        d4 = {"2": [2, 4, 6]}
        df3 = pd.DataFrame.from_dict(d2, orient='index', columns=c)

        odds = []
        evens = []
        d3_1 = [odds.append(i) if i % 2 == 1 else evens.append(i) for i in range(1, 7)]
        a = [odds, evens]
        a2 = ['1', '2']
        b = {i: j for i, j in zip(a2, a)}
        df4 = pd.DataFrame.from_dict(b, orient='index', columns=c)
        print(df2)

        return None
