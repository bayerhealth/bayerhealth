!wget --user-agent Mozilla/4.0 'https://download.wetransfer.com/eugv/6d938fc020e6b7f186ed2f2bbd152f2620210528214457/cb5d124605156c8235f8bfddeb7570b53a777fa5/model.hdf5?token=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MjIyOTk4MDQsImV4cCI6MTYyMjMwMDQwNCwidW5pcXVlIjoiNmQ5MzhmYzAyMGU2YjdmMTg2ZWQyZjJiYmQxNTJmMjYyMDIxMDUyODIxNDQ1NyIsImZpbGVuYW1lIjoibW9kZWwuaGRmNSIsIndheWJpbGxfdXJsIjoiaHR0cDovL3N0b3JtLWludGVybmFsLnNlcnZpY2UuZXUtd2VzdC0xLndldHJhbnNmZXIubmV0L2FwaS93YXliaWxscz9zaWduZWRfd2F5YmlsbF9pZD1leUpmY21GcGJITWlPbnNpYldWemMyRm5aU0k2SWtKQmFIQkNTVEphT1VFNFBTSXNJbVY0Y0NJNklqSXdNakV0TURVdE1qbFVNVFU2TURBNk1EUXVNREF3V2lJc0luQjFjaUk2SW5kaGVXSnBiR3hmYVdRaWZYMC0tMzE1YTJlZDIwODM4NzQ3NDUyYmM2ZTU5Mzk4MzA1ZTE5ZmI5ZDg5NTNlNGZmOWZhNzk1MTUxZTRkMTZjMDFhZiIsImZpbmdlcnByaW50IjoiY2I1ZDEyNDYwNTE1NmM4MjM1ZjhiZmRkZWI3NTcwYjUzYTc3N2ZhNSIsImNhbGxiYWNrIjoie1wiZm9ybWRhdGFcIjp7XCJhY3Rpb25cIjpcImh0dHA6Ly9wcm9kdWN0aW9uLmZyb250ZW5kLnNlcnZpY2UuZXUtd2VzdC0xLnd0OjMwMDAvd2ViaG9va3MvYmFja2VuZFwifSxcImZvcm1cIjp7XCJ0cmFuc2Zlcl9pZFwiOlwiNmQ5MzhmYzAyMGU2YjdmMTg2ZWQyZjJiYmQxNTJmMjYyMDIxMDUyODIxNDQ1N1wiLFwiZG93bmxvYWRfaWRcIjoxMjIyMjI3ODIzOH19In0.BWJwQYldQGoAk5-TjCcZDQEB1oll-FR_nI8mxOis5wk&cf=y' -O model.hdf5
#!rm -r dataset
!git clone https://github.com/bayerhealth/dataset
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
base_dir = "dataset/"


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
num_classes = 60
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
                         epochs=10,
                         validation_steps=valid_num//batch_size)

model.save("model.h5")