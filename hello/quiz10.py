import random

from hello.domains import myRandom


class Quiz10:

    def quiz10bubble(self) -> str:
        num = myRandom((1, 100), 10)
        for i in range(num - 1):
            for j in range(num - i - 1):
                if num[j] > num[j+1]:
                    num[j], num[j+1] = num[j+1], num[j]
            print(f'{num}')
        return None

    def quiz11insertion(self) -> str: return None

    def quiz12selection(self) -> str: return None

    def quiz13quick(self) -> str: return None

    def quiz14merge(self) -> str: return None

    def quiz15magic(self) -> str: return None

    def quiz16zigzag(self) -> str: return None

    def quiz17prime(self) -> str: return None

    def quiz18golf(self) -> str: return None

    def quiz19booking(self) -> str: return None