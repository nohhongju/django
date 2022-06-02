'''
class1 : bit803
variables : light, temp, attendance, name, age

method: ctrl_light, ctrl_temp, attend, phone_num

요구사항 :
bit803 클래스를 이용하여 학생 5명을 생성하라.
최초 light, temp, attendance의 상태는 0이다.
name은 기존 작성한 우리 반 랜덤선택 함수를 활용한다.(멜론 차트 가수명으로 해도 됨)
age는 20~30 랜덤값이다.
phone_num은 010-xxxx-xxxx로 x값은 랜덤이다.
ctrl_light, ctrl_temp, attend 메소드를 활용하여 상태값을 변경 할 수 있다.

강의실 스토리 :
첫번째 학생이 등원을 하며 전등과 히터를 켰다.
두번째, 세번째, 네번째 학생이 등원을 하였다.
두번째 학생이 아프다고 조퇴를 하였다.
******이떄 첫번째~다섯번째 학생의 정보를 출력하세요*****
******이떄 강의실 정보(전등, 히터 상태)를 출력하세요*****
네번째 학생이 덥다고 히터를 껐다.
******이떄 강의실 정보(전등, 히터 상태)를 출력하세요*****

강의실 정보 메소드
print(f'강의실 현황\n'
              f'전등 : {Bit803.light}\t 냉난방기 : {Bit803.temp}')

학생 정보 메소드
print(f'이름 : {self.name} 나이 : {self.age} 출석 상태 : {self.attendance}')
'''
from hello.domains import myMember, myRandom


class Bit803:
    light = 0
    temp = 0
    def __init__(self):
        self.attendance = 0
        self.name = myMember()
        self.age = myRandom(20, 30)
        self.phone_num = "".join(['-'if i == 0 or i == 5 else str(myRandom(1, 9)) for i in range(10)])

    @staticmethod
    def ctrl_light():
        Bit803.light = '전등 스위치를 눌렀습니다.' if Bit803.light == 0 else 0
        # self.light ^= 1
        print(Bit803.light)

    @staticmethod
    def ctrl_temp():
        Bit803.temp = 1 if Bit803.temp == 0 else 0
        # self.temp ^= 1
        print(Bit803.temp)

    def attend(self):
        pass

    def print_803(self):
        return (f'강의실 현황\n'
          f'전등 : {Bit803.light}\t 냉난방기 : {Bit803.temp}')

    def print_student(self):
        return (f'이름 : {self.name} 나이 : {self.age}  '
                f'전화번호 : 010{self.phone_num} 출석 상태 : {self.attendance}')

if __name__ == '__main__':
    b = Bit803()
    print(b.print_803())
    print(b.print_student())
    b.ctrl_light()
    b.ctrl_temp()
    print(b.print_803())

    c = Bit803()
    print(c.print_803())
    print(c.print_student())
