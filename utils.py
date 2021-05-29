from tensorflow import keras
from keras.preprocessing import image
import numpy as np
import os
#Poland
poland = keras.models.load_model('Poland.h5')
poland_dict = {'Apple.Scab': 0, 'Apple.Black rot': 1, 'Apple.Cedar apple rust': 2, 'Apple.Healthy': 3, 'Blueberry.healthy': 4, 'Cherry (including sour).Powdery mildew': 5, 'Cherry (including sour).healthy': 6, 'Corn (maize).Cercospora leaf spot Gray leaf spot': 7, 'Corn (maize).Common rust': 8, 'Corn  (maize).Northern  Leaf  Blight': 9, 'Corn  (maize).healthy': 10, 'Grape.Black  rot': 11, 'Grape.Esca  (Black  Measles)': 12, 'Grape.Leaf  blight  (Isariopsis  Leaf  Spot)': 13, 'Grape.healthy': 14, 'Other.Weed': 15, 'Peach.Bacterial  spot': 16, 'Peach.healthy': 17, 'Pepper,  bell.Bacterial  spot': 18, 'Pepper,  bell.healthy': 19, 'Potato.Early  blight': 20, 'Potato.Late  blight': 21, 'Potato.healthy': 22, 'Raspberry.healthy': 23, 'Soybean.healthy': 24, 'Squash.Powdery  mildew': 25, 'Strawberry.Leaf  scorch': 26, 'Strawberry.healthy': 27, 'Tomato.Bacterial  spot': 28, 'Tomato.Early  blight': 29, 'Tomato.Late  blight': 30, 'Tomato.Leaf  Mold': 31, 'Tomato.Septoria  leaf  spot': 32, 'Tomato.Spider  mites Two-spotted  spider  mite': 33, 'Tomato.Target  Spot': 34, 'Tomato.Tomato  Yellow  Leaf  Curl  Virus': 35, 'Tomato.Tomato  mosaic  virus': 36, 'Tomato.healthy': 37}
poland_list = list(poland_dict.keys())

#World
world = keras.models.load_model('World.h5')
world_dict = {'Apple.Apple scab': 0,'Apple.Black rot': 1,'Apple.Cedar apple rust': 2,'Apple.Healthy': 3,'Arjun.diseased': 4,'Arjun.Healthy': 5,'Blueberry.Healthy': 6,'Cassava.Bacterial blight': 7,'Cassava.Brown Streak Disease': 8,'Cassava.Green Mottle': 9,'Cassava.Mosaic Disease': 10,'Cassava.Healthy': 11,'Cherry (including sour).Powdery mildew': 12,'Cherry (including sour).Healthy': 13,'Chinair.diseased': 14,'Chinair.Healthy': 15,'Chinee Apple.Weed': 16,'Corn (maize).Cercospora leaf spot Gray leaf spot': 17,'Corn (maize).Common rust ': 18,'Corn (maize).Northern Leaf Blight': 19,'Corn (maize).Healthy': 20,'Gauva.diseased': 21,'Gauva.Healthy': 22,'Grape.Black rot': 23,'Grape.Esca (Black Measles)': 24,'Grape.Leaf blight (Isariopsis Leaf Spot)': 25,'Grape.Healthy': 26,'Jamun.diseased': 27,'Jamun.Healthy': 28,'Jatropha.diseased': 29,'Jatropha.Healthy': 30,'Lantana.Weed': 31,'Lemon.diseased': 32,'Lemon.Healthy': 33,'Mango.diseased': 34,'Mango.Healthy': 35,'Orange.Haunglongbing (Citrus greening)': 36,'Other.Weed': 37,'Papaya.anthracnose': 38,'Papaya.black spot': 39,'Papaya.phytophthora': 40,'Papaya.powdery mildew': 41,'Papaya.ring spot': 42,'Parkinsonia.Weed': 43,'Parthenium.Weed': 44,'Peach.Bacterial spot': 45,'Peach.Healthy': 46,'Pepper, bell.Bacterial spot': 47,'Pepper, bell.Healthy': 48,'Pomegranate.diseased': 49,'Pomegranate.Healthy': 50,'Potato.Early blight': 51,'Potato.Late blight': 52,'Potato.Healthy': 53,'Prickly Acacia.Weed': 54,'Raspberry.Healthy': 55,'Rice.Bacterial leaf blight': 56,'Rice.blast': 57,'Rice.brownspot': 58,'Rubber Vine.Weed': 59,'Siam Weed.Weed': 60,'Snake Weed.Weed': 61,'Soybean.Healthy': 62,'Squash.Powdery mildew': 63,'Strawberry.Leaf scorch': 64,'Strawberry.Healthy': 65,'Tomato.Bacterial spot': 66,'Tomato.Early blight': 67,'Tomato.Late blight': 68,'Tomato.Leaf Mold': 69,'Tomato.Septoria leaf spot': 70,'Tomato.Spider mites Two-spotted spider mite': 71,'Tomato.Target Spot': 72,'Tomato.Tomato Yellow Leaf Curl Virus': 73,'Tomato.Tomato mosaic virus': 74,'Tomato.Healthy': 75,'Wheat.Healthy': 76,'Wheat.leaf rust': 77,'Wheat.stem rust': 78}
world_list = list(world_dict.keys())

def handle_img(img, model):
    filepath = 'static/plants/'+img+'.jpg'
    print("Uploaded: " + filepath)
    new_img = image.load_img(filepath, target_size=(224, 224))
    img = image.img_to_array(new_img)
    img = np.expand_dims(img, axis=0)
    img = img/255
    if(model=="World"):
        prediction = world.predict(img)
        d = prediction.flatten()
        j = d.max()
        for index,item in enumerate(d):
            if item == j:
                class_name = world_list[index]
    else:
        prediction = poland.predict(img)
        d = prediction.flatten()
        j = d.max()
        for index,item in enumerate(d):
            if item == j:
                class_name = poland_list[index]
    return class_name.split(".")