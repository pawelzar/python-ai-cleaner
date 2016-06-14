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

        dirt_cat_1 = NeuralTrain(cv2.imread('../images_train/cat1.png'), self.encodingDict["cat"])
        dirt_cat_2 = NeuralTrain(cv2.imread('../images_train/cat2.png'), self.encodingDict["cat"])
        dirt_cat_3 = NeuralTrain(cv2.imread('../images_train/cat3.png'), self.encodingDict["cat"])
        dirt_dust_1 = NeuralTrain(cv2.imread('../images_train/dust1.png'), self.encodingDict["dust"])
        dirt_dust_2 = NeuralTrain(cv2.imread('../images_train/dust2.png'), self.encodingDict["dust"])
        dirt_dust_3 = NeuralTrain(cv2.imread('../images_train/dust3.png'), self.encodingDict["dust"])
        dirt_water_1 = NeuralTrain(cv2.imread('../images_train/water1.png'), self.encodingDict["water"])
        dirt_water_2 = NeuralTrain(cv2.imread('../images_train/water2.png'), self.encodingDict["water"])
        dirt_water_3 = NeuralTrain(cv2.imread('../images_train/water3.png'), self.encodingDict["water"])

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
            data.addSample((x.contours / 100.0, x.color[0] / 1000.0,
                            x.color[1] / 1000.0, x.color[2] / 1000.0), x.output)

        trainer = BackpropTrainer(self.net, momentum=0.1, verbose=True, weightdecay=0.01)
        trainer.trainOnDataset(data, 0)  # 1000 iterations
        trainer.testOnData(verbose=True)

    def test_network(self, test):
        """Return name of recognized object."""
        output = np.around(self.net.activate([test.contours / 100.0, test.color[0] / 1000.0,
                                              test.color[1] / 1000.0, test.color[2] / 1000.0]))
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
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # get a bi-level (binary) image out of a gray scale image
        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        contours, h = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

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
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # get a bi-level (binary) image out of a gray scale image
        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        contours, h = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            self.contours = len(approx)
