#predict added resistance with deep learning

import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


df = pd.read_csv("dataset2_1.csv")

#preprocessing
df = df.dropna( axis=0, how ="any")
df = df[df["label"] < 2]
df = df[df["label"] > 0.5]

X = df.drop(["time","label"], axis=1)
Y = df["label"]
#print(df.info())

print(X.shape)

scalarX, scalarY = MinMaxScaler(), MinMaxScaler()
scalarX.fit(X)
scalarY.fit(Y.reshape(Y.__len__(),1))
X = scalarX.transform(X)
Y = scalarY.transform(Y.reshape(Y.__len__(),1))

#split for training
X_train, X_test, Y_train, Y_test = train_test_split( X, Y, test_size=0.20, random_state=42)

# train model
model = Sequential()

from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import Adagrad

model.add(Dense(100, input_dim=8, activation='relu'))

# now the model will take as input arrays of shape (*, 9)
# and output arrays of shape (*, 32)

model.add(Dense(100, activation='relu'))
# created middle layer

model.add(Dense(32, activation='relu'))
# created middle layer

#model.add(Dense(100))
# created middle layer

model.add(Dense(1,activation='linear'))
# created output layer we have output values as intergers then dimension is 1

model.compile(loss='mse', optimizer='adam')

model.fit(X_train, Y_train)

#serialize model way 1
# serialize model to JSON
model_json = model.to_json()
with open("AR_pred_model_architecture.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("AR_pred_weights.h5")

#serialize model way 2 :
## save full model , achitecture, weights, optimizer used, loss funciton used etc to one binary file
model.save("AR_pred_full.h5")
print(model.summary())

#predict results
Y_pred = model.predict(X_test)

#evaluate model
r2 = r2_score(Y_test, Y_pred)
mse = mean_squared_error(Y_test, Y_pred)
mae = mean_absolute_error(Y_test, Y_pred)

print("mean absolute error: {:.5f}, mean squared error: {:.5f}, r2 score: {:.5f}".format(mae,mse,r2)) # '0.20'

# # Plot outputs
plt.scatter(np.arange(X_test.__len__()), Y_test, color='black')
plt.plot(np.arange(X_test.__len__()), Y_pred, color='blue', linewidth=2)

plt.xticks(())
plt.yticks(())

plt.show()

