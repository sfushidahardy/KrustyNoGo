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

def nineteen_to_sixteen(X,filters_n):
    X = Conv2D(filters=filters_n, kernel_size=4, strides=1, kernel_initializer = glorot_uniform, padding='valid')(X)
    X = BatchNormalization(axis = 3)(X)
    X = Activation('relu')(X)

    return X

def res_block(X, filters_n):
    X_bypass = X
    X = Conv2D(filters = filters_n, kernel_size = 3, strides = 1, padding = 'same', kernel_initializer = glorot_uniform)(X)
    X = BatchNormalization(axis = 3)(X)
    X = Activation('relu')(X)
    X = Conv2D(filters = filters_n, kernel_size = 3, strides = 1, padding = 'same', kernel_initializer = glorot_uniform)(X)
    X = BatchNormalization(axis = 3)(X)
    X = Add()([X, X_bypass])
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
    X = nineteen_to_sixteen(X_input, filters_n=32) #drops to 16x16
    X = half_size(X, filters_n=64, dropout_n=0.2)
    X = res_block(X, filters_n=64)
    X = res_block(X, filters_n=64)
    X = half_size(X, filters_n=256, dropout_n=0.2)
    X = res_block(X, filters_n=256)
    X = res_block(X, filters_n=256)
    X = half_size(X, filters_n=512, dropout_n=0.2)
    X = res_block(X, filters_n=512)
    X = Flatten()(X)
    X = Dropout(0.5)(X)
    X = Dense(1, activation='sigmoid')(X)
    model = Model(inputs = X_input, outputs = X)
    return model

model = ConvNetGo()

opt = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['binary_accuracy'])

print(model.summary())

model.fit(
  X_train,
  Y_train,
  epochs=15,
  validation_data=(X_dev, Y_dev),
)

model.save('trained_cnn_deeper.keras')
