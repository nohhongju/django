'''

lambda 매개변수 : 표현식
'''
from icecream import ic
from functools import reduce


class Solution(object):
    def __init__(self):
        pass

    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. 메소드 덧셈')
            print('2. 람다 덧셈')
            print('3. 람다 map')
            print('4. 람다 filter')
            print('5. 람다 reduce')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            elif menu == '1':
                res = self.hap(10, 20)
                ic(res)
            elif menu == '2':
                ic((lambda x, y: x + y)(10, 20))
            elif menu == '3':
                self.map_sample()
            elif menu == '4':
                self.filter_sample()
            elif menu == '5':
                self.reduce_sample()

    def hap(self, x, y):
        return (x + y)

    def map_sample(self):
        ic(list(map(lambda x: x ** 2, range(5))))

    def filter_sample(self):
        ic(list(filter(lambda x: x < 5, range(10))))

    def reduce_sample(self):
        ic(reduce(lambda x, y: x + y, [0, 1, 2, 3, 4]))


if __name__ == '__main__':
    Solution().hook()
