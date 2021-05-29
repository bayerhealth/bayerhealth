from tensorflow import keras
from keras.preprocessing import image
import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   fill_mode='nearest')

valid_datagen = ImageDataGenerator(rescale=1./255)

batch_size = 128
base_dir = "../Downloads/dataset/dataset/"


training_set = train_datagen.flow_from_directory(base_dir+'train',
                                                 target_size=(224, 224),
                                                 batch_size=batch_size,
                                                 class_mode='categorical')

valid_set = valid_datagen.flow_from_directory(base_dir+'val',
                                            target_size=(224, 224),
                                            batch_size=batch_size,
                                            class_mode='categorical')


train_num = training_set.samples
valid_num = valid_set.samples


#Model
num_classes = 47
old = keras.models.load_model('model.hdf5')

model = Sequential()
for layer in old.layers[:-1]:
    model.add(layer)
for layer in model.layers:
    layer.trainable = False

model.add(Dense(num_classes, name='new_Dense', activation='softmax'))
model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

history = model.fit(training_set,
                         steps_per_epoch=train_num//batch_size,
                         validation_data=valid_set,
                         epochs=2,
                         validation_steps=valid_num//batch_size)

model.save("model.h5")