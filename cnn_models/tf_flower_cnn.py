# -*- coding: utf-8 -*-
"""tf_flower_cnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-EPubbmKsAlMcspFCtI5ufGuRw-QWDqA
"""

import logging
logging.getLogger("tensorflow").setLevel(logging.DEBUG)
import glob
import PIL
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from matplotlib import pyplot
import os
import numpy as np
import pathlib
import sys

from google.colab import drive
drive.mount('/content/gdrive')

def load_dataset():
# load dataset
  dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
  data_dir = tf.keras.utils.get_file('flower_photos', origin=dataset_url, untar=True)
  data_dir = pathlib.Path(data_dir)

  image_count = len(list(data_dir.glob('*/*.jpg')))
  print(image_count)
  roses = list(data_dir.glob('roses/*'))
  PIL.Image.open(str(roses[0]))

  categories = ["daisy", "dandelion", "roses", "sunflowers", "tulips"]



  daisy = list(data_dir.glob('daisy/*'))
  dandelion = list(data_dir.glob('dandelion/*'))
  roses = list(data_dir.glob('roses/*'))
  sunflowers = list(data_dir.glob('sunflowers/*'))
  tulips = list(data_dir.glob('turlips/*'))

  data = []
  labels = []

  for i in daisy:
    image=tf.keras.preprocessing.image.load_img(i, color_mode='rgb',
    target_size =  (280,280))
    image=np.array(image)
    data.append(image)
    labels.append(0)
  for i in dandelion:
    image=tf.keras.preprocessing.image.load_img(i, color_mode='rgb',
    target_size= (280,280))
    image=np.array(image)
    data.append(image)
    labels.append(1)
  for i in roses:
    image=tf.keras.preprocessing.image.load_img(i, color_mode='rgb',
    target_size= (280,280))
    image=np.array(image)
    data.append(image)
    labels.append(2)
  for i in sunflowers:
    image=tf.keras.preprocessing.image.load_img(i, color_mode='rgb',
    target_size= (280,280))
    image=np.array(image)
    data.append(image)
    labels.append(3)
  for i in tulips:
    image=tf.keras.preprocessing.image.load_img(i, color_mode='rgb',
    target_size= (280,280))
    image=np.array(image)
    data.append(image)
    labels.append(3)
  data = np.array(data)
  labels = np.array(labels)

  from sklearn.model_selection import train_test_split
  train_images, test_images, train_labels, test_labels = train_test_split(data, labels, test_size=0.2,
                                                random_state=42)
	
  return train_images, train_labels, test_images, test_labels

# scale pixels
def prep_pixels(train, test):
	# convert from integers to floats
	train_norm = train.astype('float32')
	test_norm = test.astype('float32')
	# normalize to range 0-1
	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0
	# return normalized images
	return train_norm, test_norm

# plot diagnostic learning curves
def summarize_diagnostics(history):
	# plot loss
	pyplot.subplot(211)
	pyplot.title('Cross Entropy Loss')
	pyplot.plot(history.history['loss'], color='blue', label='train')
	pyplot.plot(history.history['val_loss'], color='orange', label='test')
	# plot accuracy
	pyplot.subplot(212)
	pyplot.title('Classification Accuracy')
	pyplot.plot(history.history['accuracy'], color='blue', label='train')
	pyplot.plot(history.history['val_accuracy'], color='orange', label='test')
	# save plot to file
	filename = sys.argv[0].split('/')[-1]
	pyplot.savefig(filename + '_plot.png')
	pyplot.close()

# define cnn model
def define_model():
  model = Sequential([
    
    # prwto layer
    tf.keras.layers.Conv2D(64, (7, 7), (2, 2), padding='same', use_bias=False, activation='relu'),
    tf.keras.layers.MaxPooling2D((3, 2), padding="same"),
    # prwto layer
    tf.keras.layers.Conv2D(128, (7, 7), (2, 2), padding='same', use_bias=False, activation='relu'),
    tf.keras.layers.MaxPooling2D((3, 2), padding="same"),
    # prwto layer
    tf.keras.layers.Conv2D(256, (7, 7), (2, 2), padding='same', use_bias=False, activation='relu'),
    tf.keras.layers.MaxPooling2D((3, 2), padding="same"),
    # deytero
    tf.keras.layers.Conv2D(256, (3, 3), (1, 1), padding='same', use_bias=False, activation='relu'),
    tf.keras.layers.MaxPooling2D((3, 2), padding="same"),

    # trito
    tf.keras.layers.Conv2D(64, (1, 1), strides=(1, 1), padding='same', use_bias=False, activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2), padding="same"),
    tf.keras.layers.Flatten(),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    # teliko.
    tf.keras.layers.Dense(5, activation='sigmoid')
  ])


  model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
  return model

# load dataset
train_images, train_labels, test_images, test_labels = load_dataset()
# prepare pixel data
train_images, test_images = prep_pixels(train_images, test_images)
# define model
model = define_model()
# fit model
history = model.fit(train_images, train_labels, epochs=20, batch_size=64, validation_data=(test_images, test_labels), verbose=0)
# evaluate model
_, acc = model.evaluate(test_images, test_labels, verbose=0)
print('> %.3f' % (acc * 100.0))
# learning curves
summarize_diagnostics(history)

model.save('/content/gdrive/MyDrive/???????????????????????? ???????????????? ????????????????/saved_models/tf_flower.h5')
