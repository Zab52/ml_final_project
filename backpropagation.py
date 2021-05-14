import sys
import copy
import random
import math

"""
A multilayer perceptron with one hidden layer
Reused from week 5 with with minimal changes 
"""

#calcluate sigmoid function
def sigmoid(x):
    return 1/(1+math.exp(-x))

#an artificial neural network
class ANN():
    #create nodes
    def __init__(self,inpNum, hiddenNum, outNum, learningRate):
        self.hiddenNodes = []

        for i in range(hiddenNum):
            self.hiddenNodes.append(HiddenNode(inpNum,i))

        self.outputNodes = []

        for _ in range(outNum):
            self.outputNodes.append(OutputNode(hiddenNum))

        self.learningRate = learningRate

    #classify a new input
    def classify(self,input):
        for n in self.hiddenNodes:
            n.updateOutput(input)
        outputs = []
        for n in self.outputNodes:
            n.updateOutput(self.hiddenNodes)
            outputs.append(n.getOutput())
        return outputs

    #run the backpropagation algorithm on all nodes
    def backpropagate(self,input,actResult):
        self.classify(input)
        i = 0
        for n in self.outputNodes:
            n.backpropagate(actResult[i], self.learningRate, self.hiddenNodes)
            i += 1
        for n in self.hiddenNodes:
            n.backpropagate(self.outputNodes, self.learningRate, input)

#a class representing a hidden node
class HiddenNode():
    #store all necessary information
    def __init__(self, numWeights, number):
        self.weights = []
        for _ in range(numWeights):
            self.weights.append(random.uniform(-0.5, 0.5)) #initialize weights
        self.output = 0
        self.number = number

    #given a new input, calculate output
    def updateOutput(self, input):
        sum = 0

        for i in range(len(self.weights)):
            sum += self.weights[i]*input[i]

        self.output = sigmoid(sum)

    #return latest output
    def getOutput(self):
        return self.output

    #implements backpropagation algorithm from Mitchell Table 4.2
    def backpropagate(self, outputNodes, learningRate, inputs):
        sum = 0
        for n in outputNodes:
            sum += n.getWeight(self.number) * n.getError()
        delta = self.output * (1 - self.output) * sum
        weightChanges = [input * learningRate * delta for input in inputs]
        self.weights = [old + change for old,change in zip(self.weights,weightChanges)]


#a class representing an output node
class OutputNode():
    #store all necessary information
    def __init__(self, numWeights):
        self.weights = []
        for _ in range(numWeights):
            self.weights.append(random.uniform(-0.5, 0.5)) #initialize weights
        self.output = 0
        self.error = 0

    #given a new input, calculate output
    def updateOutput(self, input):
        sum = 0

        for i in range(len(self.weights)):
            sum += self.weights[i]*(input[i].output)

        self.output = sigmoid(sum)

    #return weight associated with hidden node i
    def getWeight(self,i):
        return self.weights[i]

    #return output
    def getOutput(self):
        return self.output

    #implements backpropagation algorithm from Mitchell Table 4.2
    def backpropagate(self, actResult, learningRate, hiddenNodes):
        self.error = self.output * (1-self.output) * (actResult-self.output)
        i = 0

        for n in self.weights:
            n += learningRate*self.error*hiddenNodes[i].getOutput()
            i += 1

    #return error
    def getError(self):
        return self.error
