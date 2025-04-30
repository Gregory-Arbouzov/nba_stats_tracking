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
from torch.utils.data import Dataset, dataloader

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

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(14, 7)
        self.fc2 = nn.Linear(7, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, input):
        input = self.fc1(input)
        input = self.relu(input)
        input = self.fc2(input)
        input = self.sigmoid(input)
        return input

def run_network():
    X_train, X_test, y_train, y_test = get_train_test_data()
    scale_data(X_train, X_test)
    #dataset = 

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = get_train_test_data()
    X_train, X_test = scale_data(X_train, X_test)
    #network = Net()
    #network.forward(X_train[0])
    print(torch.tensor(X_train[0]), torch.tensor(y_train[0]))
    input_data = torch.tensor(X_train[0]), torch.tensor(y_train[0])
    print("success")
