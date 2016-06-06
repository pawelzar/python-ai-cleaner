import cv2
import numpy as np
from pybrain.supervised import BackpropTrainer
from pybrain import TanhLayer, SoftmaxLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork


class NeuralNetwork:
    def __init__(self):
        self.encodingDict = {
            "cat": [1, 0, 0],
            "dust": [0, 1, 0],
            "water": [0, 0, 1]
        }

        self.trainData = []

        dirt_cat_1 = NeuralTrain(cv2.imread('../images_train_2/cat1.png'), self.encodingDict["cat"])
        dirt_cat_2 = NeuralTrain(cv2.imread('../images_train_2/cat2.png'), self.encodingDict["cat"])
        dirt_cat_3 = NeuralTrain(cv2.imread('../images_train_2/cat3.png'), self.encodingDict["cat"])
        dirt_dust_1 = NeuralTrain(cv2.imread('../images_train_2/dust1.png'), self.encodingDict["dust"])
        dirt_dust_2 = NeuralTrain(cv2.imread('../images_train_2/dust2.png'), self.encodingDict["dust"])
        dirt_dust_3 = NeuralTrain(cv2.imread('../images_train_2/dust3.png'), self.encodingDict["dust"])
        dirt_water_1 = NeuralTrain(cv2.imread('../images_train_2/water1.png'), self.encodingDict["water"])
        dirt_water_2 = NeuralTrain(cv2.imread('../images_train_2/water2.png'), self.encodingDict["water"])
        dirt_water_3 = NeuralTrain(cv2.imread('../images_train_2/water3.png'), self.encodingDict["water"])

        self.trainData.append(dirt_cat_1)
        self.trainData.append(dirt_cat_2)
        self.trainData.append(dirt_cat_3)
        self.trainData.append(dirt_dust_1)
        self.trainData.append(dirt_dust_2)
        self.trainData.append(dirt_dust_3)
        self.trainData.append(dirt_water_1)
        self.trainData.append(dirt_water_2)
        self.trainData.append(dirt_water_3)

        for x in self.trainData:
            x.prepare_train_data()

        self.net = buildNetwork(4, 3, 3, hiddenclass=TanhLayer, outclass=SoftmaxLayer)
        data = SupervisedDataSet(4, 3)

        for x in self.trainData:
            data.addSample((x.contours/100.0, x.color[0]/1000.0, x.color[1]/1000.0, x.color[2]/1000.0), x.output)

        trainer = BackpropTrainer(self.net, momentum=0.1, verbose=True, weightdecay=0.01)
        trainer.trainOnDataset(data, 1000)
        trainer.testOnData(verbose=True)

    def test_network(self, test):
        output = np.around(self.net.activate([test.contours/100.0, test.color[0]/1000.0,
                                              test.color[1]/1000.0, test.color[2]/1000.0]))
        for key, value in self.encodingDict.items():
            if (value == output).all():
                return key


class NeuralTrain:
    def __init__(self, img, output):
        self.img = img
        self.height, self.width, self.depth = self.img.shape
        self.color = np.int_(img[self.height / 2, self.width / 2])
        self.output = output
        self.contours = 0

    def prepare_train_data(self):
        for x in range(self.height):
            for y in range(self.width):
                if (self.img[x, y] == self.color).all():
                    self.img[x, y] = [255, 255, 255]
                elif (self.img[x, y] != [255, 255, 255]).any():
                    self.img[x, y] = [0, 0, 0]

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, 1)  # get a bi-level (binary) image out of a gray scale image
        contours, h = cv2.findContours(thresh, 1, 2)

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            self.contours = len(approx)


class NeuralTest:
    def __init__(self, img):
        self.img = img
        self.height, self.width, self.depth = self.img.shape
        self.color = np.int_(img[self.height / 2, self.width / 2])
        self.contours = 0

    def prepare_test_data(self):
        for x in range(self.height):
            for y in range(self.width):
                if (self.img[x, y] == self.color).all():
                    self.img[x, y] = [0, 0, 0]
                else:
                    self.img[x, y] = [255, 255, 255]

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, 1)  # get a bi-level (binary) image out of a gray scale image
        contours, h = cv2.findContours(thresh, 1, 2)

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            self.contours = len(approx)
