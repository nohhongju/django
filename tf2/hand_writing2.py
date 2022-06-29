import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import load_model


class Solution(tf.keras.Model):
    def __init__(self):
        super(Solution, self).__init__()
        self.train_ds = None
        self.val_ds = None
        self.x_test = None
        self.y_test = None
        self.hist = None

    def preprocessing(self):
        # MNIST 데이터셋 가져오기
        (x_train, y_train), (self.x_test, self.y_test) = mnist.load_data()
        x_train, self.x_test = x_train / 255.0, self.x_test / 255.0  # 데이터 정규화

        # tf.data를 사용하여 데이터셋을 섞고 배치 만들기
        ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000)
        train_size = int(len(x_train) * 0.7)  # 학습셋:검증셋 = 7:3
        self.train_ds = ds.take(train_size).batch(20)
        self.val_ds = ds.skip(train_size).batch(20)

    def modeling(self):
        # MNIST 분류 모델 구성
        model = Sequential()
        model.add(Flatten(input_shape=(28, 28)))
        model.add(Dense(20, activation='relu'))
        model.add(Dense(20, activation='relu'))
        model.add(Dense(10, activation='softmax'))

        # 모델 생성
        model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
        # model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

        # 모델 학습
        self.hist = model.fit(self.train_ds, validation_data=self.val_ds, epochs=10)

        # 모델 평가
        print('모델 평가')
        model.evaluate(self.x_test, self.y_test)

        # 모델 정보 출력
        model.summary()
        model.save('./save/mnist_model.h5')

        '''
        Model: "sequential"
        _________________________________________________________________
        Layer (type)                 Output Shape              Param #   
        =================================================================
        flatten (Flatten)            (None, 784)               0         
        _________________________________________________________________
        dense (Dense)                (None, 20)                15700     
        _________________________________________________________________
        dense_1 (Dense)              (None, 20)                420       
        _________________________________________________________________
        dense_2 (Dense)              (None, 10)                210       
        =================================================================
        Total params: 16,330
        Trainable params: 16,330
        Non-trainable params: 0
        _________________________________________________________________
        '''

    def draw(self):
        hist = self.hist
        fig, loss_ax = plt.subplots()
        acc_ax = loss_ax.twinx()
        loss_ax.plot(hist.history['loss'], 'y', label='train loss')
        loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')
        acc_ax.plot(hist.history['accuracy'], 'b', label='train acc')
        acc_ax.plot(hist.history['val_accuracy'], 'g', label='val acc')
        loss_ax.set_xlabel('epoch')
        loss_ax.set_ylabel('loss')
        acc_ax.set_ylabel('accuracy')
        loss_ax.legend(loc='upper left')
        acc_ax.legend(loc='lower left')
        plt.show()




if __name__ == '__main__':
    s = Solution()
    # s.preprocessing()
    # s.modeling()
