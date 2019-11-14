import numpy
import scipy.special
import scipy.misc
import matplotlib.pyplot
import matplotlib.pyplot as plt
import os

# helper to load data from PNG image files
import imageio
# glob helps select multiple files using patterns
import glob

from PIL import Image

class neuralNetwork:
    
    # Инициализация
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):

        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        self.lr = learningrate

        # Заполнение массивов весовых коэффициентов случайными значениями в соответствии с нормальным распределением со средним квадротичным отклонением х^(-0.5) и серединой в точке 0.0
        self.wih = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))
        
        # Функция активации
        self.activation_function = lambda x: scipy.special.expit(x)

        pass
    
    # Обучение
    def train(self, inputs_list, targets_list):

        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        # Вычисление ошибки
        output_errors = targets - final_outputs
        # Вычисление ошибки скрытого слоя
        hidden_errors = numpy.dot(self.who.T, output_errors)

        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1 - final_outputs)), numpy.transpose(hidden_outputs))
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1 - hidden_outputs)), numpy.transpose(inputs))


        pass

    def write_weights(self):
        
        numpy.savetxt("NumReader/weights/wih.csv", self.wih, delimiter=",")
        numpy.savetxt("NumReader/weights/who.csv", self.who, delimiter=",")

        pass

    # Опрос
    def query(self, inputs_list):

        # Преобразовать список входных значений в двумерный транспоннированный массив
        inputs = numpy.array(inputs_list, ndmin=2).T

        ih = numpy.loadtxt('NumReader/weights/wih.csv', delimiter=",", dtype=numpy.float)

        hidden_inputs = numpy.dot(ih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        ho = numpy.loadtxt('NumReader/weights/who.csv', delimiter=",", dtype=numpy.float)

        final_inputs = numpy.dot(ho, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        

        return final_outputs

# number of input, hidden and output nodes
input_nodes = 784
hidden_nodes = 200
output_nodes = 10

# learning rate
learning_rate = 0.1

# create instance of neural network
n = neuralNetwork(input_nodes,hidden_nodes,output_nodes, learning_rate)

training_data_file = open("NumReader/mnist_dataset/mnist_train.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

lrate = 1

if (lrate == 0):

    epochs = 10

    for e in range(epochs):
        # go through all records in the training data set
        for record in training_data_list:
            # split the record by the ',' commas
            all_values = record.split(',')
            # scale and shift the inputs
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            # create the target output values (all 0.01, except the desired label which is 0.99)
            targets = numpy.zeros(output_nodes) + 0.01
            # all_values[0] is the target label for this record
            targets[int(all_values[0])] = 0.99
            n.train(inputs, targets)
            pass
        pass

    n.write_weights()



# test the neural network

try:
    img = Image.open('NumReader/numpic.jpeg')
    width = 28
    height = 28
    resized_img = img.resize((width, height), Image.ANTIALIAS)
    resized_img.save('NumReader/numpic.png')

    os.remove('NumReader/numpic.jpeg')
except:
    print('New file not found.')



# load image data from png files into an array
img_array = imageio.imread('NumReader/numpic.png', as_gray=True)
    
# reshape from 28x28 to list of 784 values, invert values
img_data  = img_array.reshape(784)
    
# then scale data to range from 0.01 to 1.0
img_data = (img_data / 255.0 * 0.99) + 0.01

# plot image
matplotlib.pyplot.imshow(img_data.reshape(28,28), cmap='Greys', interpolation='None')
#plt.show()

# query the network
outputs = n.query(img_data)
#print (outputs)

# the index of the highest value corresponds to the label
label = numpy.argmax(outputs)
print('Network says ', label)