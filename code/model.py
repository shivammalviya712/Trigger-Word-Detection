"""This file contains GRU model."""

import tensorflow as tf
import warnings
# Disabling Future Warnings0
warnings.filterwarnings(action='ignore', category=FutureWarning)

from keras.callbacks import ModelCheckpoint
from keras.models import Model, Sequential
from keras.models import load_model as load
from keras.layers import Dense, Activation, Dropout, Input, Masking, TimeDistributed, LSTM, Conv1D
from keras.layers import GRU, Bidirectional, BatchNormalization, Reshape
from keras.optimizers import Adam


def model(settings):
    """Creates the model's graph in Keras.

    # Arguments
        settings: An instance of the class settings. 

    # Returns:
        model: Keras model instance.
    """
    X_input = Input(shape = (settings.Tx, settings.n_freq))
    # Convolution Layer
    X = Conv1D(filters=196, kernel_size=15, strides=4)(X_input)
    X = BatchNormalization()(X)
    X = Activation(activation='relu')(X)
    X = Dropout(0.8)(X)

    # First GRU Layer
    X = GRU(units=128, return_sequences=True)(X)
    X = Dropout(0.8)(X)
    X = BatchNormalization()(X)

    # Second GRU Layer
    X = GRU(units=128, return_sequences=True)(X)
    X = Dropout(0.8)(X)
    X = BatchNormalization()(X)
    X = Dropout(0.8)(X)

    # Time-distributed dense layer
    X = TimeDistributed(Dense(1, activation='sigmoid'))(X)

    # Creating model instance
    model = Model(inputs=X_input, outputs=X)

    return model


def load_model():
    """Loads a pretrained model."""
    model = load('./model/model.h5')
    return model


def train_model(model, data):
    """Fit the model on the given data.
    
    # Arguments
        model: An instance of class Model
        data: An instance of class Dataset
    """
    opt = Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, decay=0.01)
    model.compile(loss='binary_crossentropy', optimizer=opt,
                  metrics=[tf.keras.metrics.BinaryAccuracy(threshold=0.1)])
    model.fit(data.X, data.Y, batch_size=5, epochs=1)
    model.save('./model/model_trained.h5')