#Bibliotecas específicas de pytorch    
import torch
import torch.nn as nn
import torch.utils.data as utils

#Importación de las bibliotecas principales
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#El archivo de datos de MNIST está en formato MATLAB
from scipy.io import loadmat

#Graficamos los loss obtenidos
from matplotlib import pyplot as plt

# Variables configurables

test_size = 0.30
batch_size = 500
epochs = 300
count_of_neuroal_hidden_layer_1 = 128

#Definimos nuestro criterio de loss
#Aquí usamos CrossEntropyLoss, que está poensado para clasificación
loss_criteria = nn.CrossEntropyLoss()

#Definimos nuestro optimizer
#Aquí usamos Stochastic Gradient Descent (SGD) - Descenso por Gradiente Estocástico
learning_rate = 0.01
learning_momentum = 0.9

mnist = loadmat('mnist-original.mat')

#los datos vienen transpuestos respecto de como los necesitamos
mndata = mnist['data'].transpose()
mnlabel = mnist['label'].transpose()
#hay que hacer que mnlabels sea un vector en vez de una matriz de Nx1 (para numpy es distinto)
mnlabel = mnlabel.reshape(mnlabel.shape[0],)

#Partición en datos de entrenamiento y testing
x_train, x_test, y_train, y_test = train_test_split(mndata, mnlabel, test_size = test_size, random_state=0)

#Conversión de los datos a formato Tensor
train_x = torch.Tensor(x_train).float()
train_y = torch.Tensor(y_train).long()


#El Dataset y el Dataloader van a ser los que tomen los datos y se los pasen a la red neuronal de a bloques
train_ds = utils.TensorDataset(train_x, train_y)

train_loader = utils.DataLoader(train_ds, batch_size = batch_size, shuffle=False, num_workers=1)

#Mismas conversiones con los datos de test
test_x = torch.Tensor(x_test).float()
test_y = torch.Tensor(y_test).long()
test_ds = utils.TensorDataset(test_x,test_y)
test_loader = utils.DataLoader(test_ds, batch_size = batch_size,shuffle=False, num_workers=1)

#Pausa antes de iniciar la creación y entrenamiento de la red neuronal
print("Hasta aqui se han cargado y separado los datos. Se crearon los loaders.")

input("pausa")

#Definición de la red (En pytorch se hace heredando de Module)
class MNISTNet(nn.Module):
    def __init__(self):
        super(MNISTNet, self).__init__()
        self.fc1 = nn.Linear(784, count_of_neuroal_hidden_layer_1)
        self.drop_out = nn.Dropout(p=0.1)
        self.fc2 = nn.Linear(count_of_neuroal_hidden_layer_1, 10)

    def forward(self, x):
        #Forward establece las funciones de activación entre capas.
        #En este ejemplo se aplica una función Sigmoide luego de pasar por la primera capa.
        x = self.fc1(x)
        x = self.drop_out(x)
        x = torch.sigmoid(x)
        return self.fc2(x)

#Instanciamos la red
model = MNISTNet()

#Función que modela el entrenamiento de la red
def train(model, data_loader, optimizer):
    #El modelo se debe poner en modo training
    model.train()
    train_loss = 0
    
    for batch, tensor in enumerate(data_loader):
        data, target = tensor
        #Se pasan los datos por la red y se calcula la función de loss
        optimizer.zero_grad()
        out = model(data)
        loss = loss_criteria(out, target)
        train_loss += loss.item()

        #Se hace la backpropagation y se actualizan los parámetros de la red
        loss.backward()
        optimizer.step()

    #Se devuelve el loss promedio
    avg_loss = train_loss / len(data_loader.dataset)
    return avg_loss
           
def test(model, data_loader):
    #Ahora ponemos el modelo en modo evaluación
    model.eval()
    test_loss = 0
    correct = 0

    with torch.no_grad():
        for batch, tensor in enumerate(data_loader):
            data, target = tensor
            #Dado el dato, obtenemos la predicción
            out = model(data)

            #Calculamos el loss
            test_loss += loss_criteria(out, target).item()

            #Calculamos la accuracy (exactitud) (Sumando el resultado como
            #correcto si la predicción acertó)
            _, predicted = torch.max(out.data, 1)
            correct += torch.sum(target==predicted).item()
            
    #Devolvemos la exactitud y loss promedio
    avg_accuracy = correct / len(data_loader.dataset)
    avg_loss = test_loss / len(data_loader.dataset)
    return avg_loss, avg_accuracy
       
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=learning_momentum)

#En estas listas vacías nos vamos guardando el loss para los datos de training
#y validación en cada iteración.
epoch_nums = []
training_loss = []
validation_loss = []

#Entrenamiento. Por default lo hacemos por 100 iteraciones (epochs) 
for epoch in range(1, epochs + 1):
    
    #Hacemos el train con los datos que salen del loader
    train_loss = train(model, train_loader, optimizer)
    
    #Probamos el nuevo entrenamiento sobre los datos de test
    test_loss, accuracy = test(model, test_loader)
    
    #Guardamos en nuestras listas los datos de loss obtenidos
    epoch_nums.append(epoch)
    training_loss.append(train_loss)
    validation_loss.append(test_loss)
    
    #Cada 10 iteraciones vamos imprimiendo nuestros resultados parciales
    if (epoch) % 10 == 0:
        print('Epoch {:d}: loss entrenamiento= {:.4f}, loss validacion= {:.4f}, exactitud={:.4%}'.format(epoch, train_loss, test_loss, accuracy))



plt.plot(epoch_nums, training_loss)
plt.plot(epoch_nums, validation_loss)
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(['entrenamiento', 'validacion'], loc='upper right')
plt.show()

input("pausa para ver el grafico de losses")
plt.clf()

for param_tensor in model.state_dict():
    print(param_tensor, "\n", model.state_dict()[param_tensor].numpy())

#Creamos la matriz de confusión, esta es parte del paquete scikit
from sklearn.metrics import confusion_matrix

#Ponemos el modelo en modo evaluación
model.eval()

#Hacemos las predicciones para los datos de test
x = torch.Tensor(x_test).float()
_, predicted = torch.max(model(x).data, 1)

#Graficamos la matriz de confusión
#Recordar que si en cambio ponemos "print(cm)" podemos verla con los números
cm = confusion_matrix(y_test, predicted.numpy())
a_s = accuracy_score(y_test, predicted.numpy())
print(a_s)
plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
# plt.imshow(a_s, interpolation="nearest", cmap=plt.cm.Blues)
plt.colorbar()
tick_marks = np.arange(10)
plt.xticks(tick_marks, rotation=45)
plt.yticks(tick_marks)
plt.xlabel("El modelo predijo")
plt.ylabel("La especie real era")
plt.show()