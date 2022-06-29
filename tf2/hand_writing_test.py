import tensorflow as tf
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt

_, (x_test, y_test) = mnist.load_data()
x_test = x_test / 255.0  # 데이터 정규화

# 모델 불러오기
model = tf.keras.models.load_model('./save/mnist_model.h5')
# model.summary()
model.evaluate(x_test, y_test, verbose=2)
plt.imshow(x_test[20], cmap="gray")
plt.show()

picks = [20]
# predict = model.predict_classes(x_test[picks])
y_prob = model.predict(x_test[picks], verbose=0)
predict = y_prob.argmax(axis=-1)
print("손글씨 예측값: ", predict)
