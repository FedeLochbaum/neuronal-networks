#Importación de las bibliotecas principales
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split

#El dataset de iris viene directamente incorporado en el paquete sklearn
iris = datasets.load_iris()
   
#Partición en datos de entrenamiento y testing
x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.40, random_state=0)

#Bibliotecas específicas de pytorch    
import torch
import torch.nn as nn
import torch.utils.data as utils

#Conversión de los datos a formato Tensor
train_x = torch.Tensor(x_train).float()
train_y = torch.Tensor(y_train).long()
#El Dataset y el Dataloader van a ser los que tomen los datos y se los pasen a la red neuronal de a bloques
train_ds = utils.TensorDataset(train_x,train_y)
train_loader = utils.DataLoader(train_ds, batch_size=10,
    shuffle=False, num_workers=1)

#Mismas conversiones con los datos de test
test_x = torch.Tensor(x_test).float()
test_y = torch.Tensor(y_test).long()
test_ds = utils.TensorDataset(test_x,test_y)
test_loader = utils.DataLoader(test_ds, batch_size=10,
    shuffle=False, num_workers=1)

#Pausa antes de iniciar la creación y entrenamiento de la red neuronal
print("Hasta aqui se han cargado los datos, separado, y creado los loaders.")
input("pausa")

#Definición de la red (En pytorch se hace heredando de Module)
class IrisNet(nn.Module):
    def __init__(self):
        super(IrisNet, self).__init__()
        #Capa única - 4 entradas y 3 salidas
        self.fc1 = nn.Linear(4, 3)

    def forward(self, x):
        #Forward establece las funciones de activación entre capas.
        #En este ejemplo no se aplica ninguna.
        x = self.fc1(x)
        return x

#Instanciamos la red
model = IrisNet()

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
       


#Definimos nuestro criterio de loss
#Aquí usamos CrossEntropyLoss, que está poensado para clasificación
loss_criteria = nn.CrossEntropyLoss()

#Definimos nuestro optimizer
#Aquí usamos Stochastic Gradient Descent (SGD) - Descenso por Gradiente Estocástico
learning_rate = 0.01
learning_momentum = 0.9
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=learning_momentum)

#En estas listas vacías nos vamos guardando el loss para los datos de training
#y validación en cada iteración.
epoch_nums = []
training_loss = []
validation_loss = []

#Entrenamiento. Por default lo hacemos por 100 iteraciones (epochs) 
epochs = 100
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


#Graficamos los loss obtenidos
from matplotlib import pyplot as plt

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
cm = confusion_matrix(y_test, predicted.numpy())
plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
plt.colorbar()
tick_marks = np.arange(len(iris.target_names))
plt.xticks(tick_marks, iris.target_names, rotation=45)
plt.yticks(tick_marks, iris.target_names)
plt.xlabel("El modelo predijo")
plt.ylabel("La especie real era")
plt.show()


#Creo un vector X arbitrario con algunos valores
#Lo usamos como ejemplo de cómo hacer una predicción de un dato nuevo
x_new = [[6.6,3.2,5.8,2.4]]
print ('Muestra: {}'.format(x_new[0]))
#Ponemos el modelo en modo evaluación
model.eval()
#Hacemos pasar el valor nuevo por el modelo e interpretamos su salida
x = torch.Tensor(x_new).float()
_, predicted = torch.max(model(x).data, 1)
print('El modelo dice que la muestra es de tipo:',iris.target_names[predicted.item()])