from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import cv2


def loadImage(path):
    im = cv2.imread(path)
    return flatten(im)


def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


class NeuralNetwork:
    def __init__(self):
        t = loadImage('../images_train/dirt_cat_1.png')

        self.net = buildNetwork(len(t), len(t), 1)
        self.ds = SupervisedDataSet(len(t), 1)
        self.ds.addSample(loadImage('../images_train/dirt_cat_1.png'), (1,))
        self.ds.addSample(loadImage('../images_train/dirt_dust_1.png'), (2,))
        self.ds.addSample(loadImage('../images_train/dirt_water_1.png'), (3,))

        trainer = BackpropTrainer(self.net, self.ds)
        error = 10
        iteration = 0
        while error > 0.001:
            error = trainer.train()
            iteration += 1
            print "Iteration: {0} Error {1}".format(iteration, error)

    def recognize(self, image):
        return {1.0: "cat", 2.0: "dust", 3.0: "water"}.get(round(self.net.activate(loadImage(image))))
