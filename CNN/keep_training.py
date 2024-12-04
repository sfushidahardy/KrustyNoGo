import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, Input, BatchNormalization, Activation, Add
from tensorflow.keras.initializers import random_uniform, glorot_uniform
from tensorflow.keras.models import Model

X_train = np.load('X_train.npy')
Y_train = np.load('Y_train.npy')
X_dev = np.load('X_dev.npy')
Y_dev = np.load('Y_dev.npy')

model = keras.models.load_model('trained_cnn_1.keras')

print(model.summary())

model.fit(
  X_train,
  Y_train,
  epochs=10,
  validation_data=(X_dev, Y_dev),
)

model.save('trained_cnn_1.keras')
