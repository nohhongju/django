import numpy as np
import matplotlib.pyplot as plt
from keras import datasets
from tensorflow import keras


class Solution:
    def __init__(self):
        self.mnist = keras.datasets.mnist

        (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

        train_images = train_images.reshape((60000, 28, 28, 1))
        test_images = test_images.reshape((10000, 28, 28, 1))

        # 픽셀 값을 0~1 사이로 정규화합니다.
        self.train_images, self.test_images = train_images / 255.0, test_images / 255.0

    def solution(self):
        models = keras.models
        layers = keras.layers
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))  # Conv2D - 디멘션의 차원
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))