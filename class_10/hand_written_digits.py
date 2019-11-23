import numpy as np
import torch
import torchvision
import matplotlib.pyplot as plt

from time import time
from torchvision import datasets, transforms
from torch import nn, optim

transform = transforms.Compose(
  # With this, all images will be with the same dimensions
  [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
)

# The part of the dataset used to TRAIN the neuronal network
trainset = datasets.MNIST('PATH_TO_STORE_TRAINSET', download=True, train=True, transform=transform)

# The part of the dataset used to TEST the neuronal network
valset = datasets.MNIST('PATH_TO_STORE_TESTSET', download=True, train=False, transform=transform)

# Load the trainset, setting 64 images by batch
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

# Load the test set, setting 64 images by batch
valloader = torch.utils.data.DataLoader(valset, batch_size=64, shuffle=True)


## Here code to show randomly a sequence of hand written digits

# dataiter = iter(trainloader)
# images, labels = dataiter.next()

# figure = plt.figure()
# num_of_images = 60
# for index in range(1, num_of_images + 1):
#     plt.subplot(6, 10, index)
#     plt.axis('off')
#     plt.imshow(images[index].numpy().squeeze(), cmap='gray_r')

# plt.show()


# Continue:

# Neuronal Network
# output layer of 10 neurons that use softmax
# 2 Hidden layers that use relu

input_size = 784 # 28 x 28 (total of image's pixels)
hidden_sizes = [128, 64]
output_size = 10

# This layer receive 784 (the total of the image inputs) inputs and return 128 outputs
hidden_layer_1 = nn.Linear(input_size, hidden_sizes[0])

# This layer receive 128 inputs and return 64 outputs
hidden_layer_2 = nn.Linear(hidden_sizes[0], hidden_sizes[1])

# This is the output layer that receive 64 inputs and return 10
output_layer = nn.Linear(hidden_sizes[1], output_size)

model = nn.Sequential(hidden_layer_1, nn.ReLU(),
                      hidden_layer_2, nn.ReLU(),
                      output_layer, nn.LogSoftmax(dim=1))

# Configure the NLL loss
criterion = nn.NLLLoss()
images, labels = next(iter(trainloader))
images = images.view(images.shape[0], -1)

logps = model(images) #log probabilities
loss = criterion(logps, labels) #calculate the NLL loss


# Training the model using gradient descent and back propagation
def train(model, criterion, momentum, learning_rate, epochs):
  optimizer = optim.SGD(model.parameters(), lr = learning_rate, momentum = momentum)
  time0 = time()
  for e in range(epochs):
      running_loss = 0
      for images, labels in trainloader:
          # Flatten MNIST images into a 784 long vector
          images = images.view(images.shape[0], -1)
      
          # Training pass
          optimizer.zero_grad()
          
          output = model(images)
          loss = criterion(output, labels)
          
          #This is where the model learns by backpropagating
          loss.backward()
          
          #And optimizes its weights here
          optimizer.step()
          
          running_loss += loss.item()
      else:
          print("Epoch {} - Training loss: {}".format(e, running_loss/len(trainloader)))
  print("\nTraining Time (in minutes) =",(time()-time0)/60)

momentum = 0.9
learning_rate = 0.003
epochs = 15
train(model, criterion, momentum, learning_rate, epochs)

#####

## Show example of prediction

def view_classify(img, ps):
    ''' Function for viewing an image and it's predicted classes.
    '''
    ps = ps.data.numpy().squeeze()

    _, (ax1, ax2) = plt.subplots(figsize=(6,9), ncols=2)
    ax1.imshow(img.resize_(1, 28, 28).numpy().squeeze())
    ax1.axis('off')
    ax2.barh(np.arange(10), ps)
    ax2.set_aspect(0.1)
    ax2.set_yticks(np.arange(10))
    ax2.set_yticklabels(np.arange(10))
    ax2.set_title('Class Probability')
    ax2.set_xlim(0, 1.1)
    plt.tight_layout()

# images, labels = next(iter(valloader))
# img = images[0].view(1, 784)
# with torch.no_grad():
#     logps = model(img)

# ps = torch.exp(logps)
# probab = list(ps.numpy()[0])
# print("Predicted Digit =", probab.index(max(probab)))
# view_classify(img.view(1, 28, 28), ps)


## Test the optimized model

def test(model, valloader):
  correct_count, all_count = 0, 0
  for images, labels in valloader:
    for i in range(len(labels)):
      img = images[i].view(1, 784)
      with torch.no_grad():
          logps = model(img)

      
      ps = torch.exp(logps)
      probab = list(ps.numpy()[0])
      pred_label = probab.index(max(probab))
      true_label = labels.numpy()[i]
      if(true_label == pred_label):
        correct_count += 1
      all_count += 1

  print("Number Of Images Tested =", all_count)
  print("\nModel Accuracy =", (correct_count/all_count))


test(model, valloader)

## Save the model

# torch.save(model, './my_mnist_model.pt')