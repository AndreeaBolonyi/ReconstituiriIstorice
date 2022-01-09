import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
import csv
from tempfile import NamedTemporaryFile
from keras import Sequential
import tensorflow as tf
from keras.layers import Dense
import os
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import confusion_matrix



import numpy as np
import pandas as pd
from tempfile import NamedTemporaryFile
import shutil
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.tree import DecisionTreeClassifier, export_graphviz, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay

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

    return data, output

def load_data_age(filename):
    data = []
    output = []

    path_file = os.path.dirname(os.path.dirname(__file__))
    path_file = path_file + '\\data\\' + filename

    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(path_file, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')

        for row in reader:
            data.append([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
            x = 0
            if row[5] == "20-30":
                x = 1
            elif row[5] == "30-40":
                x=2
            elif row[5] == "40-50":
                x = 3
            elif row[5] == "50+":
                x = 4
            output.append(x)

    print(output)

    output = tf.keras.utils.to_categorical(output, 5)

    return data, output

def min_max(list,type):

    min = list[0]
    max = 0.0
    for i in list:
        if i < min:
            min = i
        if i> max:
            max = i

    print("medie: " + str(float(sum(list)/len(list))))

    print(min)
    print(max)

def clasification_sex2(data, output,prop):
    p = 1 - prop
    k = int(p * len(data))

    train_data = np.asarray(data[:k])
    train_output = tf.keras.utils.to_categorical(output[:k], 2)
    train_output = np.asarray(train_output)

    valid_data = np.asarray(data[k:])
    valid_output = np.asarray(output[k:])

    model = keras.Sequential()
    model.add(layers.Dense(20, activation='relu', input_shape=(4,)))
    model.add(Dense(40, activation='relu'))
    model.add(Dense(2, activation='sigmoid'))

    #femur bun
    # lr_schedule = keras.optimizers.schedules.ExponentialDecay(
    #     initial_learning_rate=0.01,
    #     decay_steps=50,
    #     decay_rate=1)

    # lr_schedule = keras.optimizers.schedules.ExponentialDecay(
    #     initial_learning_rate=0.01,
    #     decay_steps=43,
    #     decay_rate=1)

    #humerus
    # lr_schedule = keras.optimizers.schedules.ExponentialDecay(
    #     initial_learning_rate=0.01,
    #     decay_steps=55,
    #     decay_rate=0.98)

    opt = keras.optimizers.Adam(learning_rate=lr_schedule)
    model.compile(loss='binary_crossentropy', optimizer=opt,metrics=['accuracy'])

    history = model.fit(train_data, train_output, epochs=800, batch_size=20)

    print(history.history)
    print(history.history.keys())
    loss = history.history['loss']
    acc = history.history['accuracy']
    epochs = range(1, len(loss) + 1)
    plt.title('Humerus')
    plt.plot(epochs, loss, 'y', label='Loss')
    plt.plot(epochs, acc, color='black', label='Accuracy Test')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    pred = model.predict_classes(valid_data)

    k = 0
    for i in range(len(pred)):
        if pred[i] == valid_output[i]:
            k+=1

    acc= float((k*100)/len(pred))

    cm = confusion_matrix(valid_output, pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               )
    disp.plot()
    plt.show()

    return acc

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

<<<<<<< Updated upstream
    # lr_schedule = keras.optimizers.schedules.ExponentialDecay(
    #     initial_learning_rate=0.01,
    #     decay_steps=70,
    #     decay_rate=0.96)

    lr_schedule = keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=0.01,
        decay_steps=55,
        decay_rate=0.98)
=======
    history = model.fit(train_data, train_output, validation_data=(valid_data, valid_output), epochs=1000, batch_size=50)
>>>>>>> Stashed changes

    opt = keras.optimizers.Adam(learning_rate=lr_schedule)
    model.compile(loss='binary_crossentropy', optimizer=opt,metrics=['accuracy'])

    history = model.fit(train_data, train_output,validation_data=(valid_data, valid_output), epochs=800, batch_size=20)

    print(history.history)
    print(history.history.keys())
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    epochs = range(1, len(loss) + 1)
<<<<<<< Updated upstream
    plt.title('Humerus')
    #plt.plot(epochs, loss, 'y', label='Loss')
=======
    plt.plot(epochs, loss, 'y', label='Loss')
    plt.plot(epochs, acc, color='black', label='Accuracy')
    plt.plot(epochs, val_loss, 'y', color='black', label='Loss Validation')
>>>>>>> Stashed changes
    plt.plot(epochs, val_acc, color='red', label='Accuracy Validation')
    plt.plot(epochs, acc, color='black', label='Accuracy Test')
    #plt.plot(epochs, val_loss, 'y', color='black', label='Loss Validation')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    #plt.show()


    #
    Xnew = np.asarray([[295.0,54.0,42.51,19.34],
[302.0,55.0,42.06,20.21],
[270.5,55.0,39.74,19.22],
[281.0,55.5,39.84,19.74],
[314.5,63.0,47.18,25.91],
[4306.5,60.0,46.6,25.48],
[322.0,57.0,44.11,22.99],
[304.5,63.5,44.87,25.54],
[307.0,62.0,44.34,26.04],
[287.0,57.0,40.02,18.32]])
    corect= np.asarray([1,1,1,1,0,0,0,0,0,1])
    # make a prediction
    pred = model.predict_classes(Xnew)
    print(pred)


    cm = confusion_matrix(corect, pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               )
    disp.plot()
    plt.show()

def clasification_age(data, output):
    k = int(0.8 * len(data))

    train_data = np.asarray(data[:k])
    train_output = np.asarray(output[:k])

    valid_data = np.asarray(data[k:])
    valid_output = np.asarray(output[k:])

    model = keras.Sequential()
    model.add(layers.Dense(20, activation='relu', input_shape=(4,)))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(5, activation='softmax'))

    lr_schedule = keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=0.001,
        decay_steps=20,
        decay_rate=0.7)

    opt = keras.optimizers.Adam(learning_rate=lr_schedule)
    # model.compile(loss='categorical_crossentropy', optimizer=opt,metrics=['accuracy'])
    #
    # history = model.fit(train_data, train_output, validation_data=(valid_data, valid_output), epochs=800, batch_size=20)

    model.compile(optimizer=opt, loss=keras.losses.CategoricalCrossentropy(), metrics=['accuracy'])

    model.summary()

    history = model.fit(train_data, train_output, validation_data=(valid_data, valid_output), batch_size=20,
                        epochs=100)

    # model = keras.Sequential([keras.layers.Dense(2, input_dim=4, activation=tf.nn.relu),
    #                           keras.layers.Dense(20, activation=tf.nn.relu),
    #                           keras.layers.Dense(5, activation=tf.nn.softmax)
    #                           ])
    #
    # model.compile(optimizer='adam', loss=keras.losses.CategoricalCrossentropy(), metrics=['accuracy'])
    #
    # model.summary()
    #
    # history = model.fit(train_data, train_output, validation_data=(valid_data, valid_output), batch_size=10,
    #                     epochs=1000)
    print(history.history)
    print(history.history.keys())

    print(history.history)
    print(history.history.keys())
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    epochs = range(1, len(loss) + 1)
    plt.title('Humerus')
    plt.plot(epochs, loss, 'y', label='Loss')
    #plt.plot(epochs, val_acc, color='red', label='Accuracy Validation')
    #plt.plot(epochs, acc, color='black', label='Accuracy Test')
    plt.plot(epochs, val_loss, 'y', color='black', label='Loss Validation')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    min_max(acc,"Acuratete test")
    #min_max(val_acc,"Acuratete Validation")


def clasification_age2(data, output,prop):
    p = 1 - prop
    k = int(p * len(data))

    train_data = np.asarray(data[:k])
    train_output = tf.keras.utils.to_categorical(output[:k], 5)
    train_output = np.asarray(train_output)

    valid_data = np.asarray(data[k:])
    valid_output = np.asarray(output[k:])

    model = keras.Sequential()
    model.add(layers.Dense(20, activation='relu', input_shape=(4,)))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(5, activation='softmax'))

    lr_schedule = keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=0.001,
        decay_steps=20,
        decay_rate=0.7)

    opt = keras.optimizers.Adam(learning_rate=lr_schedule)

    model.compile(optimizer=opt, loss=keras.losses.CategoricalCrossentropy(), metrics=['accuracy'])

    model.summary()

    history = model.fit(train_data, train_output, batch_size=20,
                        epochs=100)

    print(history.history)
    print(history.history.keys())

    loss = history.history['loss']
    acc = history.history['accuracy']
    epochs = range(1, len(loss) + 1)
    plt.title('Humerus')
    plt.plot(epochs, loss, 'y', label='Loss')
    plt.plot(epochs, acc, color='black', label='Accuracy Test')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    min_max(acc,"Acuratete test")

    pred = model.predict_classes(valid_data)

    k = 0
    for i in range(len(pred)):
        if pred[i] == valid_output[i]:
            k += 1

    acc = float((k * 100) / len(pred))

    cm = confusion_matrix(valid_output, pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  )
    disp.plot()
    plt.show()

    return acc


def plot_test(list_acc,test_size):
    plt.scatter(test_size, list_acc)
    plt.scatter(test_size, list_acc)
    plt.title("Determinare sex")
    plt.xlabel("% date de test")
    plt.ylabel("acuratete")
    plt.show()

def plot_test1(list_acc_femur,lista_acc_humerus,test_size):
    plt.scatter(test_size, lista_acc_humerus)
    plt.scatter(test_size, list_acc_femur)
    plt.title("Determinare sex")
    plt.xlabel("% date de test")
    plt.ylabel("acuratete")
    plt.show()


def run(bone_type):
    list = [0.2,0.35,0.4,0.7,0.8]
    list_acc = []
    if bone_type == 'humerus':
        data, output = load_data('humerus.csv')
        for i in list:
            acc = clasification_sex2(data, output,i)
            list_acc.append(acc)
        print(list_acc)
        min_max(list_acc,acc)
        plot_test(list_acc,list);
    else:
        data, output = load_data('femur.csv')
        for i in list:
            acc = clasification_sex2(data, output,i)
            list_acc.append(acc)
        print(list_acc)
        min_max(list_acc,acc)
        plot_test(list_acc,list)



def run_age(bone_type):
    list = [0.2, 0.35, 0.4, 0.7, 0.8]
    list_acc = []
    if bone_type == 'humerus':
        data, output = load_data_age('humerus.csv')
        for i in list:
            acc = clasification_age2(data, output,i)
            list_acc.append(acc)
        print(list_acc)
        min_max(list_acc, acc)
        plot_test(list_acc, list)
    else:
        data, output = load_data_age('femur.csv')
        for i in list:
            acc = clasification_age2(data, output, i)
            list_acc.append(acc)
        print(list_acc)
        min_max(list_acc, acc)
        plot_test(list_acc, list)

def run_age2(bone_type):
    if bone_type == 'humerus':
        data, output = load_data_age('humerus.csv')

        acc = clasification_age(data, output)

    else:
        data, output = load_data_age('femur.csv')

        acc = clasification_age(data, output)



if __name__ == '__main__':
<<<<<<< Updated upstream
    #run('femur')
    run_age2("humerus")
    # list = [0.2, 0.35, 0.4, 0.7, 0.8]
    # list_acc_humerus=[96.875, 83.03571428571429, 82.8125, 78.125, 71.59533073929961]
    # list_acc_femur=[86.66666666666667, 87.61904761904762, 90.0, 80.47619047619048, 80.91286307053942]
    # plot_test(list_acc_femur,list_acc_humerus,list)
=======
    run('humerus')
>>>>>>> Stashed changes
