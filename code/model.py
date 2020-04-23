"""This file contains GRU model."""

import warnings
# Disabling Future Warnings0
warnings.filterwarnings(action='ignore', category=FutureWarning)

from keras.callbacks import ModelCheckpoint
from keras.models import Model, load_model, Sequential
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