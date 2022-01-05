import csv
from tempfile import NamedTemporaryFile
from keras import Sequential
import tensorflow as tf
from keras.layers import Dense
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers

def load_data(filename):
    data = []
    output = []

    path_file = os.path.dirname(os.path.dirname(__file__))
    path_file = path_file + '\\data\\' + filename

    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(path_file, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')

        for row in reader:
            data.append([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
            output.append(int(row[4]))

    output = tf.keras.utils.to_categorical(output, 2)

    return data, output

def min_max(list,type):

    min = 1
    max = 0
    for i in list:
        if i < min:
            min = i
        if i> max:
            max = i

    print(type + "=> min: " + str(min) + " max: "+ str(max))

def clasification_sex(data, output):
    k = int(0.8 * len(data))

    train_data = np.asarray(data[:k])
    train_output = np.asarray(output[:k])

    valid_data = np.asarray(data[k:])
    valid_output = np.asarray(output[k:])

    # model = Sequential()
    # model.add(Dense(20, activation='relu', input_dim=4))
    # model.add(Dense(40, activation='relu'))
    # model.add(Dense(2, activation='sigmoid'))
    # opt = keras.optimizers.Adam(learning_rate=0.0001)
    # model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])
    # model.summary()

    model = keras.Sequential()
    model.add(layers.Dense(20, activation='relu', input_shape=(4,)))
    model.add(Dense(40, activation='relu'))
    model.add(Dense(2, activation='sigmoid'))

    # lr_schedule = keras.optimizers.schedules.ExponentialDecay(
    #     initial_learning_rate=0.01,
    #     decay_steps=70,
    #     decay_rate=0.96)

    lr_schedule = keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=0.01,
        decay_steps=55,
        decay_rate=0.98)

    opt = keras.optimizers.Adam(learning_rate=lr_schedule)
    model.compile(loss='binary_crossentropy', optimizer=opt,metrics=['accuracy'])

    history = model.fit(train_data, train_output, validation_data=(valid_data, valid_output), epochs=800, batch_size=20)

    print(history.history)
    print(history.history.keys())
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    epochs = range(1, len(loss) + 1)
    plt.title('Humerus')
    #plt.plot(epochs, loss, 'y', label='Loss')
    plt.plot(epochs, val_acc, color='red', label='Accuracy Validation')
    plt.plot(epochs, acc, color='black', label='Accuracy Test')
    #plt.plot(epochs, val_loss, 'y', color='black', label='Loss Validation')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    min_max(acc,"Acuratete test")
    min_max(val_acc,"Acuratete Validation")

    print(history.history['val_loss'])


def run(bone_type):
    if bone_type == 'humerus':
        data, output = load_data('humerus.csv')
        clasification_sex(data, output)
    else:
        data, output = load_data('femur.csv')
        clasification_sex(data, output)


if __name__ == '__main__':
    run('humerus')
