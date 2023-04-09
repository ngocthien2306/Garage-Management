from api.license_plates.model.detectRoboflow.loadRoboflow import RoboflowModel
from api.license_plates.characters_recognition.characters_recognition import CharactersRecognition
import cv2
import pytesseract
from api.license_plates.characters_recognition.helper.imageprocessing import processing
roboflow = RoboflowModel("66nm8eEysyrDBVqqkTTV","license-plates-recognition-iuk6u")
cRecognition = CharactersRecognition()
class ocr_service:
    def __init__(self):
        self.lables = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'Error', 'F', 'G','H','K','L','M','N','P','R','S','T','U','V','X','Y','Z']
    def crop_image(self,image, x_min, y_min, w, h):
    # Load image using OpenCV
        # Calculate the coordinates of the top-left and bottom-right corners of the rectangle
        x_max = x_min + w
        y_max = y_min + h
        # Crop the image
        cropped_img = image[y_min:y_max, x_min:x_max] 
        return cropped_img
    def ocr(self,image):
        kitu,typelp,typevehicle = roboflow.detect_objects(image)
        # cat ki tu 
        characters = []

        for object in kitu:
            
            cropped_img = self.crop_image(image, object[0], object[1], object[2], object[3])
            ## Chuyen doi anh xam
            imgProcessing=processing(cropped_img)
            # đưa vào nhận diện  .............. 

            result_test= cRecognition.loadimg_Test(imgProcessing)
            #result_test = pytesseract.image_to_string(imgProcessing)
            if(False): # Cài đặt ngưỡng kết quả
                continue
            print("result_test", result_test.item())
            print("result_test", result_test)
            character= self.lables[result_test.item()]
            characters+= character
        # Concat the characters
        result = "".join(characters)
        return result,typelp,typevehicle
    # def crop_imageyolo(self, image, x_min, y_min, w, h):

    def ocrYolo(self,image,predictions):
        kitu,typelp,typevehicle = roboflow.detect_objectYolo(predictions)
        characters = []
        i = 0
        for object in kitu:
            cropped_img = self.crop_image(image,int(object[0]), int(object[1]), int(object[2]), int(object[3]))
            ## Convert Processing image
            imgProcessing=processing(cropped_img)
            result_test= cRecognition.loadimg_Test(imgProcessing)
            if(False): # Settting threshold
                continue
            print("result_test", result_test.item())
            print("result_test", result_test)
            character= self.lables[result_test.item()]
            characters+= character
        # Concat the characters
        result = "".join(characters)
        return result,typelp,typevehicle
