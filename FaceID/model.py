from module import *
import tensorflow as tf

class L1Dist(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, input_embedding, validation_embedding):
        input_embedding = tf.convert_to_tensor(input_embedding)
        validation_embedding = tf.convert_to_tensor(validation_embedding)
        return tf.math.abs(input_embedding - validation_embedding)

def make_embedding():
    inp = tf.keras.layers.Input(shape=(128, 128, 3), name='input_image')

    c1 = tf.keras.layers.Conv2D(64, (10, 10), activation='relu')(inp)
    m1 = tf.keras.layers.MaxPooling2D(64, (2, 2), padding='same')(c1)

    c2 = tf.keras.layers.Conv2D(128, (7, 7), activation='relu')(m1)
    m2 = tf.keras.layers.MaxPooling2D(64, (2, 2), padding='same')(c2)

    c3 = tf.keras.layers.Conv2D(128, (4, 4), activation='relu')(m2)
    m3 = tf.keras.layers.MaxPooling2D(64, (2, 2), padding='same')(c3)

    c4 = tf.keras.layers.Conv2D(256, (4, 4), activation='relu')(m3)
    f1 = tf.keras.layers.Flatten()(c4)
    d1 = tf.keras.layers.Dense(4096, activation='sigmoid')(f1)

    return tf.keras.models.Model(inputs=[inp], outputs=[d1], name='embedding')

def make_siamese_model(embedding): 
    
    input_image = tf.keras.layers.Input(name='input_img', shape=(128,128,3))
    
    validation_image = tf.keras.layers.Input(name='validation_img', shape=(128,128,3))
    
    siamese_layer = L1Dist()
    siamese_layer._name = 'distance'
    distances = siamese_layer(embedding(input_image), embedding(validation_image))
    
    classifier = tf.keras.layers.Dense(1, activation='sigmoid')(distances)
    
    return tf.keras.models.Model(inputs=[input_image, validation_image], outputs=classifier, name='SiameseNetwork')