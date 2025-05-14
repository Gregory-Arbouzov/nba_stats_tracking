#  What defines a model?
# 1. training data
# 2. test data
# 3. ML algorithm
# 4. hyperparameters
#
# What can instances of models do?
# 1. evaluate individual data points
# 2. be saved / called
#

from db import data_cleaning

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

torch.set_default_dtype(torch.float64)

def get_train_test_data():
    all_data_df = data_cleaning.game_results_cleaning()
    X = all_data_df.iloc[:,:-1]
    y = all_data_df.iloc[:,-1]
    
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=101)

    return X_train, X_test, y_train, y_test

def scale_data(X_train, X_test):
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test

class MLP(nn.Module):

    def __init__(self):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(14, 7)
        self.fc2 = nn.Linear(7, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, input):
        #self = self.double()
        input = self.fc1(input)
        input = self.relu(input)
        input = self.fc2(input)
        input = self.sigmoid(input)
        return input

def all_data_transforms():
    X_train, X_test, y_train, y_test = get_train_test_data()
    X_train, X_test = scale_data(X_train, X_test)

    y_train_list = y_train.to_list()
    y_test_list = y_test.to_list()

    training_data = [(torch.tensor(X_train[i]), torch.tensor(float(y_train_list[i])).unsqueeze(0)) for i in range(len(X_train))]
    test_data = [(torch.tensor(X_test[i]), torch.tensor(float(y_test_list[i])).unsqueeze(0)) for i in range(len(X_test))]

    return training_data, test_data

def train_nn(training_data, batch_size = 1000, epochs = 10):
    dataloader = DataLoader(training_data, batch_size = batch_size, shuffle = True)
    model = MLP()
    loss_function = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr = 0.001)

    for epoch in range(epochs):
        total_loss = 0
        for features, outcome in dataloader:
            prediction = model(features)
            loss = loss_function(prediction, outcome)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

    return model

def get_nn_accuracy(model, test_data):
    correct = 0
    total = 0
    loss = 0

    loss_function = nn.BCELoss()

    for features, outcomes in test_data:
        outputs = model.forward(features)
        loss += loss_function(outputs, outcomes)

        predictions = torch.round(outputs)
        #print("prediction: " + str(predictions) + ", correct: " + str(outcomes))

        total += outcomes.size(0)
        correct += (predictions == outcomes).sum().item()

    print("the test accuracy of the model on the test set is: {}%".format(100 * correct/total))

if __name__ == "__main__":
    training_data, test_data = all_data_transforms()
    trained_model = train_nn(training_data)
    get_nn_accuracy(trained_model, test_data)


