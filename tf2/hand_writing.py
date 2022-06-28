import numpy as np
import matplotlib.pyplot as plt
from keras import datasets, layers, models
from tensorflow import keras


class Solution:
    def __init__(self):
        self.mnist = keras.datasets.mnist
        (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

        train_images = train_images.reshape((60000, 28, 28, 1))
        test_images = test_images.reshape((10000, 28, 28, 1))

        # 픽셀 값을 0~1 사이로 정규화합니다.
        self.train_images, self.test_images = train_images / 255.0, test_images / 255.0
        self.layers = layers
        self.model = models.Sequential()
        self.train_labels = train_labels

    def solution(self):
        self.modeling()
        self.training()

    def modeling(self):
        model = self.model
        layers = self.layers
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))  # Conv2D - 디멘션의 차원
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(10, activation='softmax'))

        model.summary()

        '''
        Model: "sequential"
        _________________________________________________________________
        Layer (type)                 Output Shape              Param #   
        =================================================================
        conv2d (Conv2D)              (None, 26, 26, 32)        320       
        _________________________________________________________________
        max_pooling2d (MaxPooling2D) (None, 13, 13, 32)        0         
        _________________________________________________________________
        conv2d_1 (Conv2D)            (None, 11, 11, 64)        18496     
        _________________________________________________________________
        max_pooling2d_1 (MaxPooling2 (None, 5, 5, 64)          0         
        _________________________________________________________________
        conv2d_2 (Conv2D)            (None, 3, 3, 64)          36928     
        =================================================================
        Total params: 55,744
        Trainable params: 55,744
        Non-trainable params: 0
        _________________________________________________________________
        '''

    def training(self):
        model = self.model
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        model.fit(self.train_images, self.train_labels, epochs=5)


if __name__ == '__main__':
    Solution().solution()