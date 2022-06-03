from matplotlib import pyplot as plt
from scipy import misc
from matplotlib import rc, font_manager
rc('font', family=font_manager.FontProperties(fname='C:/Windows/Fonts/malgunsl.ttf').get_name())

class Raccoon:
    @staticmethod
    def solution():
        img_rgb = misc.face()
        print(img_rgb.shape)

        plt.subplot(221)
        plt.imshow(img_rgb, cmap=plt.cm.gray)  # 컬러 이미지 출력
        plt.axis("off")
        plt.title("RGB 컬러 이미지")

        plt.subplot(222)
        plt.imshow(img_rgb[:, :, 0], cmap=plt.cm.gray)  # red 채널 출력
        plt.axis("off")
        plt.title("Red 채널")

        plt.subplot(223)
        plt.imshow(img_rgb[:, :, 1], cmap=plt.cm.gray)  # green 채널 출력
        plt.axis("off")
        plt.title("Green 채널")

        plt.subplot(224)
        plt.imshow(img_rgb[:, :, 2], cmap=plt.cm.gray)  # blue 채널 출력
        plt.axis("off")
        plt.title("Blue 채널")

        plt.show()


if __name__ == '__main__':
    Raccoon.solution()