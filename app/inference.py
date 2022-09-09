import torch
from torchvision import transforms
from tqdm.notebook import tqdm
from PIL import Image
import numpy as np
import shutil
import os

def save_img(file):
    file_name = os.path.join('receive_image', file.filename)
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_name

def test_submit(img_file, model_path='/Users/jimmyfu87/JupyterNotebook/Save_model/Dogcat_resnet18_moredata',n_img=1):
    transforms_set = transforms.Compose([transforms.Resize((224,224)), transforms.ToTensor()])
    pred_label=[]
    model = torch.load(model_path)
    for i in tqdm(range(1,n_img+1)):
        #讀取照片為PIL圖檔
        img = Image.open(img_file).convert('RGB')
        #PIL圖檔->transforms(resize(224,224),to_tensor)
        img = transforms_set(img)
        #原本img是(3,224,224)但Resnet18需要的維度為4維(a,3,224,224)，a為圖片張數
        #一次讀一張，unsqueeze(0)是在0的index增加一個維度，張數為一張因此變成(1,3,224,224)
        img = img.unsqueeze(0)
        #將圖片丟入模型output[貓的數值,狗的數值]
        with torch.no_grad(): 
            output=model(img)
        #取數值較大的為pred
        pred = output.data.max(dim = 1, keepdim = True)[1]
        pred_label.append(int(pred))
    return pred_label
