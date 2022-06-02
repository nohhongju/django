from hello.domains import myMember, myRandom


class Way(object):
    def __init__(self):
        self.name = myMember()
        self.number = myRandom(10, 200)
        self.passenger = myRandom(0, 100)
        self.money = myRandom(2000, 10000)

    def bus(self) -> object:

        return self.number, self.passenger, self.money

    def subway(self) -> object:
        pass

    def taxi(self) -> object:
        pass


if __name__ == '__main__':
    print()