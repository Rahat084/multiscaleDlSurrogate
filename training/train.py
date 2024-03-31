import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

@tf.function(input_signature=[tf.TensorSpec(shape=(None, 3), dtype=tf.float32)])
def scale_strain(strain):
    return (strain - x_mean) / x_std


class ModelWithScalar(tf.keras.Model):
    """
    Embed scalar with the trained model
    """
    def __init__(self, x2stress_model, scale_strain):
        super().__init__()

        self._model = x2stress_model
        self._scale_strain = scale_strain

    def call(self, strain):
        batch_size = tf.shape(strain)[0]
        dim = tf.shape(strain)[1]

        with tf.GradientTape(watch_accessed_variables=False) as tape:
            tape.watch(strain)
            x = self._scale_strain(strain)
            stress = self._model(x)

        tangent_op = tape.batch_jacobian(stress, strain)
        return tf.concat([stress, tf.reshape(tangent_op, (batch_size, dim * dim))], axis=1)
