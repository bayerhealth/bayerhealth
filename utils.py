from tensorflow import keras
from keras.preprocessing import image
import numpy as np
model = keras.models.load_model('model.hdf5')

def handle_img(img):
    filepath = 'static/plants/'+img+'.jpg'
    print("Uploaded: " + filepath)
    new_img = image.load_img(filepath, target_size=(224, 224))
    img = image.img_to_array(new_img)
    img = np.expand_dims(img, axis=0)
    img = img/255
    img_class = model.predict_classes(img)
    img_prob = model    .predict_proba(img)
    print(img_class ,img_prob)