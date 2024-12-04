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

model = Sequential([
  Conv2D(filters=16, kernel_size=3, input_shape=(19, 19, 1)),
  MaxPooling2D(pool_size=2),
  Conv2D(filters=32, kernel_size=3),
  MaxPooling2D(pool_size=2),
  Flatten(),
  Dense(1, activation='sigmoid'),
])

opt = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['binary_accuracy'])

print(model.summary())

model.fit(
  X_train,
  Y_train,
  epochs=100,
  batch_size=64,
  validation_data=(X_dev, Y_dev),
)

model.save('simple_cnn2.keras')
