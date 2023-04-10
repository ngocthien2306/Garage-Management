import torch
from api.license_plates.characters_recognition.model.Net import Net
import cv2
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
from api.license_plates.characters_recognition.helper.device import get_default_device, to_device
device = get_default_device()
class CharactersRecognition:
    def __init__(self):
        self.model = to_device(Net(), device)
        self.model.load_state_dict(torch.load('src/api/license_plates/characters_recognition/model/ocr32class-cnn2D_update_30.pth'))
        self.transform = transforms.Compose([
            transforms.Resize(32),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    def loadimg_Test(self,gray_img):
        #image = Image.open(pathImage).convert('RGB')
        #gray_img = cv2.imread(pathImage, cv2.IMREAD_GRAYSCALE)
        # Resize the image using cv2.resize()
        
        
        
        #img_tensor = transform(gray_img)
        img_tensor = self.transform(gray_img)
        img_tensor = img_tensor.unsqueeze(0)
        # Make prediction
        with torch.no_grad():
            output = self.model(img_tensor)
            # Pick index with highest probability
            preds  = output.argmax(dim=1, keepdim=True)
            return preds