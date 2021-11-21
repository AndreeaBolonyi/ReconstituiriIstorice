import csv

import pandas as pd
from tempfile import NamedTemporaryFile
import shutil
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier, export_graphviz, export_text
from sklearn.model_selection import train_test_split


def convert_age(age):
    if age.__contains__('+'):
        aux = age.split('+')
        if aux[0].__contains__("-"):
            age = aux[0]
        else:
            aux[0] = int(aux[0])
            if aux[0] <= 20:
                return '<20'
            elif 20 <= aux[0] <= 30:
                return '20-30'
            elif 30 <= aux[0] <= 40:
                return '30-40'
            elif 40 <= aux[0] <= 50:
                return '40-50'
            else:
                return '50+'

    if age.__contains__('-'):
        ages = age.split('-')
        min_age = int(ages[0])
        max_age = int(ages[1])

        if min_age <= 20:
            return '<20'
        elif 20 <= min_age and 30 >= max_age:
            return '20-30'
        elif 30 <= min_age and 40 >= max_age:
            return '30-40'
        elif 40 <= min_age and 50 >= max_age:
            return '40-50'
        else:
            return '50+'

    age = int(age)
    if age <= 20:
        return '<20'
    elif 20 <= age <= 30:
        return '20-30'
    elif 30 <= age <= 40:
        return '30-40'
    elif 40 <= age <= 50:
        return '40-50'
    else:
        return '50+'


def modify_age(filename):
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(filename, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')

        for row in reader:
            new_age = convert_age(row[5])
            row[5] = new_age
            writer.writerow(row)

    shutil.move(tempfile.name, filename)


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
        self.__classes_name = []

    def import_data(self):
        if self.__bone.get_bone_type() == "Humerus":
            col_names = ['HML', 'HEB', 'HHD', 'HMLD', 'SEX', 'AGE']
            self.__feature_cols = ['HML', 'HEB', 'HHD', 'HMLD']
            self.__filename = "data/humerus.csv"

            # modify_age(self.__filename)
            self.__data_set = pd.read_csv(self.__filename, header=None, names=col_names)
        elif self.__bone.get_bone_type() == "Femur":
            col_names = ['FML', 'FHD', 'FEB', 'FMLD', 'SEX', 'AGE']
            self.__feature_cols = ['FML', 'FHD', 'FEB', 'FMLD']
            self.__filename = "data/femur.csv"
            self.__data_set = pd.read_csv(self.__filename, header=None, names=col_names)
        else:
            raise Exception("type not found")

    def split_data_for_sex(self):
        x = self.__data_set[self.__feature_cols]
        y = self.__data_set.SEX
        self.__classes_name = ['male', 'female']
        self.__x_train, self.__x_test, self.__y_train, self.__y_test = train_test_split(x, y, test_size=0.2,
                                                                                        random_state=1)

    def convert_age_to_number(self, age):
        index = 0
        for x in self.__classes_name:
            if x == age:
                return index
            else:
                index += 1

    def split_data_for_age(self):
        x = self.__data_set[self.__feature_cols]
        self.__classes_name = {*self.__data_set.AGE.tolist()}
        y = [self.convert_age_to_number(x) for x in self.__data_set.AGE]
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
        return pred[0], self.__classes_name

    def accuracy(self, y_pred):
        # print("Confusion Matrix: ", confusion_matrix(self.__y_test, y_pred))
        print("Accuracy : ", accuracy_score(self.__y_test, y_pred) * 100)

    def create_decision_tree(self, classification_type):
        self.train_using_gini()
        y_pred = self.predict()

        print("Results using Gini Index for " + classification_type + ":")
        self.accuracy(y_pred)

    def solve_age(self):
        self.import_data()
        self.split_data_for_age()
        self.create_decision_tree("age classification")

        self.plot_data_age()
        export_graphviz(self.__tree,
                        out_file="tree_age.dot",
                        feature_names=self.__feature_cols,
                        class_names=list(self.__classes_name),
                        filled=True)

        export_text(self.__tree, feature_names=self.__feature_cols)

    def solve_sex(self):
        self.import_data()
        self.split_data_for_sex()
        self.create_decision_tree("sex classification")

        self.plot_data_sex()
        export_graphviz(self.__tree,
                        out_file="tree_sex.dot",
                        feature_names=self.__feature_cols,
                        class_names=['male', 'female'],
                        filled=True)

        export_text(self.__tree, feature_names=self.__feature_cols)

    def plot_data_sex(self):
        names = self.__classes_name
        height = [0, 0]
        left = [1, 2]

        with open(self.__filename, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                if row[4] == "0":
                    height[0] += 1
                else:
                    height[1] += 1

        plt.bar(left, height, tick_label=names, width=0.8, color=['red', 'green'])
        plt.xlabel('x-sex')
        plt.ylabel('y-number')
        plt.title(self.__filename)

        plt.show()

    def plot_data_age(self):
        print(self.__classes_name)
        names = list(self.__classes_name)
        height = [0, 0, 0, 0, 0]
        left = [1, 2, 3, 4, 5]

        with open(self.__filename, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                if row[5] == '<20':
                    height[0] += 1
                elif row[5] == '20-30':
                    height[1] += 1
                elif row[5] == '30-40':
                    height[2] += 1
                elif row[5] == '40-50':
                    height[3] += 1
                elif row[5] == '50+':
                    height[4] += 1

        plt.bar(left, height, tick_label=names, width=0.8, color=['red', 'green', 'yellow', 'blue', 'orange'])
        plt.xlabel('x-age')
        plt.ylabel('y-number')
        plt.title(self.__filename)

        plt.show()
