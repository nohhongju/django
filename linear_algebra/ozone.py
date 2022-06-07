import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
# 미분함수를 다른 파일에 갖다 두고 사용

class Solution:
    def __init__(self):
        url = "https://raw.githubusercontent.com/reisanar/datasets/master/ozone.data.csv"
        # s = requests.get(url).content
        self.df = pd.read_csv(url)

        # 1. Raw Data Loading
        # df = pd.read_csv('./data/ozone.csv')

        # 2. Data Preprocessing(데이터 전처리)
        # 필요한 column(Temp, Ozone)만 추출
        self.training_data = self.df[['temp', 'ozone']]

        # 결측치 제거 - dropna() 함수 이용
        self.training_data = self.training_data.dropna(how='any')

        # 3. Training Data Set
        self.x_data = self.training_data['temp'].values.reshape(-1, 1)
        self.t_data = self.training_data['ozone'].values.reshape(-1, 1)

        # 4. Simple Linear Regression 정의
        self.W = np.random.rand(1, 1)
        self.b = np.random.rand(1)

        # 7. 프로그램에서 필요한 변수들 정의
        learning_rate = 1e-5
        self.f = lambda x: self.loss_func(self.x_data, self.t_data)

    # 4. 미분함수
    def numerical_derivative(self, f, x):
        # f : 미분하려고 하는 다변수 함수
        # x : 모든 변수를 포함하고 있는 ndarray
        delta_x = 1e-4
        # 미분한 결과를 저장할 ndarray
        derivative_x = np.zeros_like(x)

        # iterator를 이용해서 입력된변수 x들 각각에 대해 편미분 수행
        it = np.nditer(x, flags=['multi_index'])

        while not it.finished:
            idx = it.multi_index  # iterator의 현재 index를 tuple 형태로 추출

            # 현재 칸의 값을 잠시 저장
            tmp = x[idx]

            x[idx] = tmp + delta_x
            fx_plus_delta = f(x)  # f(x + delta_x)

            x[idx] = tmp - delta_x
            fx_minus_delta = f(x)  # f(x - delta_x)

            # 중앙치분방식
            derivative_x[idx] = (fx_plus_delta - fx_minus_delta) / (2 * delta_x)

            # 데이터 원상 복구
            x[idx] = tmp

            it.iternext()

        return derivative_x

    # 5. loss function 정의
    def loss_func(self, x, t):
        y = np.dot(x, self.W) + self.b
        return np.mean(np.power((t - y), 2))  # 최소제곱법

    # 6. 학습종료 후 예측값 계산 함수
    def predict(self, x):
        return np.dot(x, self.W) + self.b

    def solution(self):
        # 6. learning rate 정의
        learning_rate = 0.0001
        # 8. 학습 진행
        for step in range(90000):
            self.W -= learning_rate * self.numerical_derivative(self.f, self.W)
            self.b -= learning_rate * self.numerical_derivative(self.f, self.b)

            if step % 9000 == 0:
                print('W : {}, b : {}, loss : {}'.format(self.W, self.b, self.loss_func(self.x_data, self.t_data)))

        # 9. 예측
        result = self.predict(62)
        print(result)  # [[34.56270003]]

        # 10. 그래프로 확인
        plt.scatter(self.x_data, self.t_data)
        plt.plot(self.x_data, np.dot(self.x_data, self.W) + self.b, color='r')
        plt.show()


if __name__ == '__main__':
    Solution().solution()