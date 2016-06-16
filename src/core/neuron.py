import cv2
import numpy as np

from cv2 import imread as load
from pybrain.supervised import BackpropTrainer
from pybrain import TanhLayer, SoftmaxLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork


class NeuralNetwork:
    def __init__(self):
        self.code = {
            "cat": [1, 0, 0],
            "dust": [0, 1, 0],
            "water": [0, 0, 1]
        }

        train_data = [
            (Neuron(load('../images_train/cat1.png')), self.code["cat"]),
            (Neuron(load('../images_train/cat2.png')), self.code["cat"]),
            (Neuron(load('../images_train/cat3.png')), self.code["cat"]),
            (Neuron(load('../images_train/dust1.png')), self.code["dust"]),
            (Neuron(load('../images_train/dust2.png')), self.code["dust"]),
            (Neuron(load('../images_train/dust3.png')), self.code["dust"]),
            (Neuron(load('../images_train/water1.png')), self.code["water"]),
            (Neuron(load('../images_train/water2.png')), self.code["water"]),
            (Neuron(load('../images_train/water3.png')), self.code["water"])
        ]

        for x, output in train_data:
            x.prepare()

        self.net = buildNetwork(4, 3, 3, hiddenclass=TanhLayer,
                                outclass=SoftmaxLayer)
        data = SupervisedDataSet(4, 3)

        for x, output in train_data:
            data.addSample((x.contours / 100.0, x.color[0] / 1000.0,
                            x.color[1] / 1000.0, x.color[2] / 1000.0), output)

        trainer = BackpropTrainer(self.net, momentum=0.1,
                                  verbose=True, weightdecay=0.01)
        trainer.trainOnDataset(data, 1000)  # 1000 iterations
        trainer.testOnData(verbose=True)

    def test_network(self, test):
        """Return name of recognized object."""
        output = np.around(
            self.net.activate(
                [test.contours / 100.0, test.color[0] / 1000.0,
                 test.color[1] / 1000.0, test.color[2] / 1000.0]))

        for key, value in self.code.items():
            if (value == output).all():
                return key


class Neuron:
    def __init__(self, img):
        self.img = img
        self.height, self.width, self.depth = self.img.shape
        self.color = np.int_(img[self.height / 2, self.width / 2])
        self.contours = 0

    def prepare(self):
        """Convert image and acquire information about it."""
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # get a bi-level (binary) image out of a gray scale image
        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        contours, h = cv2.findContours(thresh, cv2.RETR_LIST,
                                       cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            approx = cv2.approxPolyDP(
                cnt, 0.01 * cv2.arcLength(cnt, True), True)
            self.contours = len(approx)
