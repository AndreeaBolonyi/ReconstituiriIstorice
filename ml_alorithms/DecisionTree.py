import csv

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split


class DecisionTree:
    def __init__(self, bone):
        self.__bone = bone
        self.__data_set = None
        self.__filename = ""
        self.__feature_cols = []
        self.__x_train = []
        self.__y_train = []
        self.__x_test = []
        self.__y_test = []
        self.__tree = None

    def import_data(self):
        if self.__bone.get_bone_type() == "Humerus":
            col_names = ['HML', 'HEB', 'HHD', 'HMLD', 'SEX', 'AGE']
            self.__feature_cols = ['HML', 'HEB', 'HHD', 'HMLD']
            self.__filename = "data/humerus.csv"
            self.__data_set = pd.read_csv(self.__filename, header=None, names=col_names, nrows=100)
        elif self.__bone.get_bone_type() == "Femur":
            col_names = ['FML', 'FML', 'FHD', 'FMLD', 'SEX', 'AGE']
            self.__feature_cols = ['FML', 'FML', 'FHD', 'FMLD']
            self.__filename = "data/femur.csv"
            self.__data_set = pd.read_csv(self.__filename, header=None, names=col_names, nrows=100)
        else:
            raise Exception("type not found")

        print("Dataset Length: ", len(self.__data_set))
        print("Dataset Shape: ", self.__data_set.shape)
        print("Dataset: ", self.__data_set.head())

    def split_data(self):
        x = self.__data_set[self.__feature_cols]
        y = self.__data_set.SEX
        self.__x_train, self.__x_test, self.__y_train, self.__y_test = train_test_split(x, y, test_size=0.2,
                                                                                        random_state=1)

    def train_using_gini(self):
        # default se foloseste Gini index: metrica care masoara cat de des un element ales random este clasificat gresit
        # un index Gini mai mic inseamna un atribut care va fi preferat

        self.__tree = DecisionTreeClassifier(criterion="gini")
        self.__tree.fit(self.__x_train, self.__y_train)
        return self.__tree

    def predict(self):
        return self.__tree.predict(self.__x_test)

    def predict_one(self):
        new_features = {k: v for k, v in self.__bone.get_features().items() if k != "SEX" and k != "AGE"}
        new_features = pd.DataFrame(new_features, index=[0])
        pred = self.__tree.predict(new_features)
        return pred[0]

    def accuracy(self, y_pred):
        print("Confusion Matrix: ", confusion_matrix(self.__y_test, y_pred))
        print("Accuracy : ", accuracy_score(self.__y_test, y_pred) * 100)

    def solve(self):
        self.import_data()
        self.split_data()
        self.train_using_gini()
        y_pred = self.predict()

        print("Results using Gini Index:")
        self.accuracy(y_pred)

        plot_data(self.__filename)
        export_graphviz(self.__tree,
                        out_file="tree.dot",
                        feature_names=self.__feature_cols,
                        class_names=['male', 'female'],
                        filled=True)


def plot_data(filename):
    names = ['male', 'female']
    height = [0, 0]
    left = [1, 2]

    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',',)
        k = 0
        for row in lines:
            if k == 100:
                break
            if row[4] == "0":
                height[0] += 1
            else:
                height[1] += 1
            k += 1

    plt.bar(left, height, tick_label=names, width=0.8, color=['red', 'green'])
    plt.xlabel('x-sex')
    plt.ylabel('y-number')
    plt.title(filename)

    plt.show()
