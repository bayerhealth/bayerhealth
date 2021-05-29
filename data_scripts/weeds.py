 
import os
import pandas as pd
import shutil

os.chdir("../Downloads/DeepWeeds_Images_256")
try:
    os.mkdir("train")
    os.mkdir("val")
except:
    pass
train = pd.read_csv("../train_set_labels.csv")
val = pd.read_csv("../test_set_labels.csv")

print(train)
for j,i in train.iterrows():
    try:
        os.mkdir("train/"+str(i.Species))
    except:
        pass
    shutil.copyfile(i.Label, "train/"+i.Species+"/"+i.Label)

for j,i in val.iterrows():
    try:
        os.mkdir("val/"+str(i.Species))
    except:
        pass
    shutil.copyfile(i.Label, "val/"+i.Species+"/"+i.Label)