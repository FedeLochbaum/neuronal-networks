## inputs:
 # x1 = sepal_length
 # x2 = sepal_width
 # x3 = petal_length
 # x4 = petal_width

## goal column = species ( Iris-setosa | Iris-versicolor | Iris-virginica)

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
import pandas as pn
import torch
import torch.nn as nn
import torch.utils.data as utils
from matplotlib import pyplot as ptl
import torch.utils.data as td

iris = datasets.load_iris()

x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_zie = 0.4, random_start=0)

# pasamos a la estructura a tensores

train_x = torch.Tensor(x_train).float()
train_y = torch.Tensor(y_train).long()
test_x = torch.Tensor(x_test).float()
test_y = torch.Tensor(y_test).long()


train_ds = utils.TensorDataset(train_x, train_y)
test_ds = utils.TensorDataset(test_x, test_y)

train_loader = utils.DataLoader(train_ds, batch_size=10, shuffle=False, num_workers=1)
test_loader = utils.DataLoader(test_ds, batch_size=10, shuffle=False, num_workers=1)




class IrisNet(nn.Module):
  def __init__(self):
    super(IrisNet, self).__init__()
    # 4 inputs (x0.. x3)
    # 3 neuronas
    self.fc1 = nn.Linear(4, 3)
  
  # Linear es como la representacion del layer de la red
  def forward(self, x):
    return self.fc1(x)

#
loss_criteria = nn.CrossEntropyLoss()

learning_rate = 0.01
learning_momentum = 0.9
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=learning_momentum)
#


def train(model, data_loader, optimizer):
  model.train()
  train_loss = 0

  for bach, tensor in enumerate(data_loader):
    data, target = tensor
    optimizer.zero_grad()
    out = model(data)
    loss = loss_criteria(out, target)
    train_loss += loss.item()

    loss.backward()
    optimizer.step()

  return train_loss / len(data_loader.dataset)


def test(model, test_loader):
  model.eval()
  test_loss = 0
  correct = 0

  with torch.no_grad():
    for batch, tensor in enumerate(data_loader):
      data, target = tensor
      out = model(data)

      test_loss += loss_criteria(out, target).item()

      _, predicted = torch.max(out.data, 1)
      correct += torch.sum(target==predicted).item()

  svg_accuracy = correct / len(data_loader.dataset)
  avg_loss = test_loss / 


#
epoch_nums = []
training_loss = []
validation_loss = []

epochs = 100
for epoch in range(1, epochs + 1):
  train_loss = train(model, train_loader, optimizer)
  test_loss, accuracy = test(model, test_loader)

  epoch_nums.append(epoch)
  training_loss.append(train_loss)
  validation_loss.append(test_loss)
#