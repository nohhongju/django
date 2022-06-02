class Tmp:
    def __init__(self):
        self.name = 'sonata'
        self.speed = 0
        self.oil = 110

    def ctrl_speed(self, speed):
        self.speed += speed
        self.spend_oil(50)

    def spend_oil(self, oil):
        self.oil -= oil
        if self.oil < 20:
            print('위험')

if __name__ == '__main__':
    car = Tmp()
    print(f'변경 전 스피드 : {car.speed}')
    print(f'남은 오일 양 : {car.oil}')
    car.ctrl_speed(50)  # 인자(아규먼트)의 값만큼 스피드 증가
    print(f'변경 후 스피드1 : {car.speed}')
    print(f'남은 오일 양1 : {car.oil}')
    car.ctrl_speed(10)  # 인자(아규먼트)의 값만큼 스피드 증가
    print(f'변경 후 스피드2 : {car.speed}')
    print(f'남은 오일 양2 : {car.oil}')
    car.spend_oil(-100)
    print(f'충전 후 오일 양: {car.oil}')

