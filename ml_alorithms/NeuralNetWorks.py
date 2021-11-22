import csv
from tempfile import NamedTemporaryFile
import tf
from keras import Sequential
import tensorflow as tf
from keras.layers import Conv2D, BatchNormalization, MaxPooling2D, Dropout, Flatten, Dense
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras


def load_data(filename):
    data = []
    output = []

    path_file = os.path.dirname(os.path.dirname(__file__))
    path_file = path_file + '\data\\' + filename

    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(path_file, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')

        for row in reader:
            data.append([float(row[0]),float(row[1]),float(row[2]),float(row[3])])
            output.append(int(row[4]))

    output = tf.keras.utils.to_categorical(output,2)

    return data, output

def clasification_sex(data, output):
    k = int(0.8*len(data))

    train_data = np.asarray(data[:k])
    train_output = np.asarray(output[:k])

    valid_data = np.asarray(data[k:])
    valid_output = np.asarray(output[k:])

    model = Sequential()
    model.add(Dense(20, activation='relu', input_dim=4))
    model.add(Dense(40, activation='relu'))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()

    history = model.fit(train_data, train_output, validation_data=(valid_data, valid_output), epochs=200, batch_size=20)


    print(history.history)
    print(history.history.keys())
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    epochs = range(1, len(loss) + 1)
    #plt.plot(epochs, loss, 'y', label='Loss')
    plt.plot(epochs, acc, color='black', label='Accuracy')
    #plt.plot(epochs, val_loss, 'y', color='black', label='Loss Validation')
    plt.plot(epochs, val_acc, color='red', label='Accuracy Validation')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    print(history.history['val_loss'])


def run(type):
    if type == 'humerus':
        data, output = load_data('humerus.csv')
        clasification_sex(data,output)
    else:
        data, output = load_data('femur.csv')
        clasification_sex(data, output)


if __name__ == '__main__':
    run('femur')
