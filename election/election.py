import pandas as pd
import numpy as np
import platform
import matplotlib.pyplot as plt
import matplotlib as mpl
from icecream import ic
from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from context.domains import File, Reader


class Solution(Reader):
    def __init__(self):
        self.file = File()
        self.file.context = './save/'
        self.driver = webdriver.Chrome('C:/Users/bitcamp/Downloads/chromedriver_win32/chromedriver.exe')
        self.driver.get(
            "http://info.nec.go.kr/main/showDocument.xhtml?electionId=0000000000&topMenuId=VC&secondMenuId=VCCP09")

    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. crawling')
            print('2. read_result')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            if menu == '1':
                self.crawling()
            if menu == '2':
                self.read_result()
            if menu == '3':
                pass
            elif menu == '0':
                break

    def crawling(self):
        driver = self.driver
        driver.find_element(By.ID, 'electionType1').click()
        driver.find_element(By.ID, 'electionName').send_keys('제 19대')
        time.sleep(1)
        driver.find_element(By.ID, 'electionCode').send_keys('대통령선거')
        time.sleep(2)
        sido_list_raw = driver.find_element(By.XPATH, """//*[@id="cityCode"]""")
        sido_list = sido_list_raw.find_elements(By.TAG_NAME, 'option')
        sido_names_values = [option.text for option in sido_list]
        sido_names_values = sido_names_values[2:]  # 시도 명이 2번째 index부터 시작함
        print(sido_names_values)

        election_result_raw = {'광역시도': [],
                               '시군': [],
                               'pop': [],
                               'moon': [],
                               'hong': [],
                               'ahn': []}

        for each_sido in sido_names_values:
            self.move_sido(each_sido)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table')
            df = pd.read_html(str(table))
            self.append_data(df, each_sido, election_result_raw)
        election_result = pd.DataFrame(election_result_raw,
                                       columns=['광역시도', '시군', 'pop', 'moon', 'hong', 'ahn'])
        self.file.fname = 'election_result.csv'
        path = self.new_file(self.file)
        election_result.to_csv(path, encoding='utf-8', sep=',')
        driver.close()

    def get_num(self, tmp):
        return float(re.split('\(', tmp)[0].replace(',', ''))

    def move_sido(self, name):
        driver = self.driver
        element = driver.find_element(By.ID, "cityCode")
        element.send_keys(name)
        make_xpath = """//*[@id="searchBtn"]"""
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, make_xpath)))
        driver.find_element(By.XPATH, make_xpath).click()

    def append_data(self, df, sido_name, data):
        for each in df[0].values[1:]:
            data['광역시도'].append(sido_name)
            data['시군'].append(each[0])
            data['pop'].append(self.get_num(each[2]))
            data['moon'].append(self.get_num(each[3]))
            data['hong'].append(self.get_num(each[4]))
            data['ahn'].append(self.get_num(each[5]))

    def read_result(self):
        self.file.fname = 'election_result.csv'
        path = self.new_file(self.file)
        election_result = pd.read_csv(path, encoding='utf-8', index_col=0)
        ic(election_result)


if __name__ == '__main__':
    Solution().hook()