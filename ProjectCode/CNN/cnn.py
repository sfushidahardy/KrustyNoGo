import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, Input, BatchNormalization, Activation, Add
from tensorflow.keras.initializers import random_uniform, glorot_uniform
from tensorflow.keras.models import Model

X_train = np.load('X_train_endgame.npy')
Y_train = np.load('Y_train_endgame.npy')
X_dev = np.load('X_dev_endgame.npy')
Y_dev = np.load('Y_dev_endgame.npy')

def nineteen_to_sixteen(X,filters_n):
    X = Conv2D(filters=filters_n, kernel_size=4, strides=1, kernel_initializer = glorot_uniform, padding='valid')(X)
    X = BatchNormalization(axis = 3)(X)
    X = Activation('relu')(X)

    return X

def half_size(X, filters_n, dropout_n):
    X = Conv2D(filters = filters_n, kernel_size = 3, strides = 1, padding = 'same', kernel_initializer = glorot_uniform)(X)
    X = BatchNormalization(axis = 3)(X)
    X = MaxPooling2D(2)(X)
    if dropout_n != False:
        X = Dropout(dropout_n)(X)
    X = Activation('relu')(X)
    return X

def ConvNetGo(training=False):
    X_input = Input((19,19,1))
    X = nineteen_to_sixteen(X_input, filters_n=16) #drops to 16x16
    X = half_size(X, filters_n=64, dropout_n=False)
    X = half_size(X, filters_n=256, dropout_n=False)
    X = half_size(X, filters_n=1024, dropout_n=0.2)
    X = Flatten()(X)
    X = Dropout(0.5)(X)
    X = Dense(1, activation='sigmoid')(X)
    model = Model(inputs = X_input, outputs = X)
    return model

model = ConvNetGo()

opt = tf.keras.optimizers.Adam(learning_rate=0.00015)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['binary_accuracy'])

print(model.summary())

model.fit(
  X_train,
  Y_train,
  epochs=10,
  validation_data=(X_dev, Y_dev),
)

model.save('trained_cnn_endgame.keras')
