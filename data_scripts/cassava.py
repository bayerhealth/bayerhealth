 
import os
import shutil
import pandas as pd
import random

df = pd.read_csv("train.csv")

os.chdir("train")
try:
    os.mkdir("train")
    os.mkdir("val")
except:
    pass
print(df.head)
k=1
for filename in os.listdir('.'):
    for j,i in df.iterrows():
        if(i.image_id==filename):
            try:
                os.mkdir("train/"+i.label)
                os.mkdir("val/"+i.label)
            except:
                pass
            if(random.randint(0,100)<=20):
                shutil.copyfile(i.image_id, "val/"+i.label+"/"+i.image_id)
            else:
                shutil.copyfile(i.image_id, "train/"+i.label+"/"+i.image_id)
            print(k)
            k+=1
            break