import pandas as pd

from context.domains import Reader, File, Printer


class Solution(Reader):
    def __init__(self):
        self.file = File()
        # self.reader = Reader()
        self.printer = Printer()
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']

    def save_police_pos(self):
        self.file.fname = 'crime_in_seoul'
        self.file.context = './data/'
        a = self.csv(self.file)
        print(a)

    def save_cctv_pos(self):
        pass

    def save_police_norm(self):
        pass

    def folium_test(self):
        pass

    def draw_crime_map(self):
        pass

if __name__ == '__main__':
    Solution().save_police_pos()
