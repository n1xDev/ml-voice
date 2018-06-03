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

n = buildNetwork(5000, 2000, 5)
print 'Initializaing completed'

def file2Arr(fname):
	arr = []
	f = open(fname)
	line = f.readline()
	while line:
	    arr.append(line[:-1])
	    line = f.readline()
	f.close()
	return arr

dataSet = SupervisedDataSet(5000, 5)
sets = file2Arr('new_1.txt')
dataSet.addSample( (sets), (1) )
sets = file2Arr('new_2.txt')
dataSet.addSample( (sets), (1) )
sets = file2Arr('new_3.txt')
dataSet.addSample( (sets), (1) )
sets = file2Arr('new_4.txt')
dataSet.addSample( (sets), (1) )
sets = file2Arr('new_5.txt')
dataSet.addSample( (sets), (1) )
print("Datasets ready")

#tstdata, trndata = dataSet.splitWithProportion( 0.25 )
#trndata._convertToOneOfMany()
#tstdata._convertToOneOfMany()
'''
f = open('_learned', 'r')
n = pickle.load(f)
f.close()
'''
trainer = BackpropTrainer(n, dataSet, 0.0001, 1.0, 0.99)
print("Backprop ready")
trainer.trainOnDataset(dataSet, 100)
#trainer.trainUntilConvergence(dataSet);
print("Learning completed")
trainer.testOnData()
print("Testing completed")

f = open('_learned', 'w')
pickle.dump(n, f)
f.close()

print("Serializing completed")

sets = file2Arr('new_1.txt')
out = n.activate(sets)
print('-----------A-----------')
for i in range(0, len(out)):
	print round(out[i])
sets = file2Arr('new_2.txt')
out = n.activate(sets)
print('-----------B-----------')
for i in range(0, len(out)):
	print round(out[i])
sets = file2Arr('new_3.txt')
out = n.activate(sets)
print('-----------V-----------')
for i in range(0, len(out)):
	print round(out[i])
sets = file2Arr('new_4.txt')
out = n.activate(sets)
print('-----------G-----------')
for i in range(0, len(out)):
	print round(out[i])
sets = file2Arr('new_5.txt')
out = n.activate(sets)
print('-----------D-----------')
for i in range(0, len(out)):
	print round(out[i])
print 'DONE'