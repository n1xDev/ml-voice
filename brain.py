from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

myNet = buildNetwork(2, 3, 1)

dataSet = SupervisedDataSet(2, 1)
dataSet.addSample((0, 0), (0,))
dataSet.addSample((0, 1), (1,))
dataSet.addSample((1, 0), (1,))
dataSet.addSample((1, 1), (0,))

trainer = BackpropTrainer(myNet, dataSet)
trainer.train()

print(net.activate([0, 1]))