from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection

from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
import pickle
'''
n = FeedForwardNetwork()
inLayer = LinearLayer(2)
hiddenLayer = LinearLayer(5)
outLayer = LinearLayer(1)
n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addOutputModule(outLayer)
in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)
n.addConnection(in_to_hidden)
n.addConnection(hidden_to_out)
n.sortModules()
'''

n = buildNetwork(2, 4, 1)

dataSet = SupervisedDataSet(2, 1)
'''
dataSet.addSample( (0, 0), (0) )
dataSet.addSample( (0, 1), (1) )
dataSet.addSample( (1, 0), (1) )
dataSet.addSample( (1, 1), (0) )

#tstdata, trndata = dataSet.splitWithProportion( 0.25 )
#trndata._convertToOneOfMany()
#tstdata._convertToOneOfMany()

trainer = BackpropTrainer(n, dataSet, 0.01, 1.0, 0.99)
trainer.trainOnDataset(dataSet, 10000)
#trainer.trainUntilConvergence(dataSet)
trainer.testOnData()

f = open('_learned', 'w')
pickle.dump(n, f)
f.close()
'''
f = open('_learned', 'r')
n = pickle.load(f)
f.close()


print n.activate((0, 0))
print n.activate((0, 1))
print n.activate((1, 0))
print n.activate((1, 1))