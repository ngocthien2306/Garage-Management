
import cv2
import numpy as np
from sklearn.metrics import f1_score
import tensorflow.keras as keras
from api.license_plates.model.BienSoXe.lib_detection import load_model, detect_lp, im2single
import tensorflow as tf
class PlatesServices:
    def __init__(self):
        # Dinh nghia cac ky tu tren bien so
        self.char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ-'
        # Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
        self.Dmax = 608
        self.Dmin = 288
        # Load model LP detection
        self.wpod_net_path = "/data/thinhlv/thiennn/deeplearning/Garage-Management/src/api/license_plates/model/BienSoXe/wpod-net_update1.json"
        self.wpod_net = load_model(self.wpod_net_path)

        # Cau hinh tham so cho model SVM
        self.digit_w = 30 # Kich thuoc ki tu
        self.digit_h = 60 # Kich thuoc ki tu

        self.model = keras.models.load_model('/data/thinhlv/thiennn/deeplearning/Garage-Management/src/api/license_plates/model/BienSoXe/nnt_digit_cnn.h5',custom_objects={"custom_f1score": self.custom_f1score })
    # Metrics for checking the model performance while training
    def f1score(y, y_pred):
        return f1_score(y, tf.math.argmax(y_pred, axis=1), average='micro') 

    def custom_f1score(self,y, y_pred):
        return tf.py_function(self.f1score, (y, y_pred), tf.double)

    # Ham sap xep contour tu trai sang phai
    def sort_contours(self,cnts):

        reverse = False
        i = 0
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][i], reverse=reverse))
        return cnts

    





    # Ham fine tune bien so, loai bo cac ki tu khong hop ly
    def fine_tune(self,lp):
        newString = ""
        for i in range(len(lp)):
            if lp[i] in self.char_list:
                newString += lp[i]
        return newString

    
    def detection1line(self,plate_info , roi):
        # Chuyen anh bien so ve gray
        gray = cv2.cvtColor( roi, cv2.COLOR_BGR2GRAY,)


        # Ap dung threshold de phan tach so va nen
        binary = cv2.threshold(gray, 127, 255,
                                    cv2.THRESH_BINARY_INV)[1]





                # Segment kí tự
        kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
        cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


        plate_info = ""
        print("bat dau nhan dien")
        for c in self.sort_contours(cont):
            (x, y, w, h) = cv2.boundingRect(c)
            ratio = h/w
            if 1.5<=ratio<=3.5: # Chon cac contour dam bao ve ratio w/h
                if h/roi.shape[0]>=0.6: # Chon cac contour cao tu 60% bien so tro len



                    # Tach so va predict
                    curr_num = thre_mor[y:y+h,x:x+w]



                    img = cv2.cvtColor(curr_num, cv2.COLOR_BGR2RGB)

                    img = cv2.resize(img,(28,28),3)
                    img = tf.image.resize_with_pad(img, 28, 28, antialias=True)

                    img = img[np.newaxis, :, :, :]

                    # Dua vao model CNN
                            
                    result = self.model.predict(img)

                    result = np.argmax(result,axis = 1)
                    result_test = result[0]

                    if result_test<=9: # Neu la so thi hien thi luon
                        result_test = str(result_test)
                    else: #Neu la chu thi chuyen bang ASCII
                        result_test = chr(result_test+55)
                    plate_info +=result_test
        return plate_info            
    
                
    def detection(self,Ivehicle):
        print("Bat dau detect")
        print(Ivehicle)
        #Width = Ivehicle.shape[1]
        #Height = Ivehicle.shape[0]

        # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
        ratio = float(max(Ivehicle.shape[:2])) / min(Ivehicle.shape[:2])
        side = int(ratio * self.Dmin)
        bound_dim = min(side, self.Dmax)
        print("test bug")
        _ , LpImg, lp_type = detect_lp(self.wpod_net, im2single(Ivehicle), bound_dim, lp_threshold=0.5)
        print("Type:", lp_type)
        if(LpImg == 0):
            return "Khong nhan dien duoc"
        if(lp_type== 1):
            if (len(LpImg)):

                # Chuyen doi anh bien so
                LpImg[0] = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))

                roi = LpImg[0]
    
                # Chuyen anh bien so ve gray
                gray = cv2.cvtColor( roi, cv2.COLOR_BGR2GRAY,)


                # Ap dung threshold de phan tach so va nen
                binary = cv2.threshold(gray, 127, 255,
                                    cv2.THRESH_BINARY_INV)[1]





                # Segment kí tự
                kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
                cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


                plate_info = ""
                print("bat dau nhan dien")
                for c in self.sort_contours(cont):
                    (x, y, w, h) = cv2.boundingRect(c)
                    ratio = h/w
                    if 1.5<=ratio<=3.5: # Chon cac contour dam bao ve ratio w/h
                        if h/roi.shape[0]>=0.6: # Chon cac contour cao tu 60% bien so tro len



                            # Tach so va predict
                            curr_num = thre_mor[y:y+h,x:x+w]



                            img = cv2.cvtColor(curr_num, cv2.COLOR_BGR2RGB)

                            img = cv2.resize(img,(28,28),3)
                            img = tf.image.resize_with_pad(img, 28, 28, antialias=True)

                            img = img[np.newaxis, :, :, :]

                            # Dua vao model CNN
                            
                            result = self.model.predict(img)
                            result_pro = np.amax(result)
                            result = np.argmax(result,axis = 1)
                            result_test = result[0]
                            
                            if result_test<=9: # Neu la so thi hien thi luon
                                result_test = str(result_test)
                            else: #Neu la chu thi chuyen bang ASCII
                                result_test = chr(result_test+55)
                            plate_info +=result_test
                return plate_info
        elif(lp_type== 2):
            
            LpImg[0] = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))
            roiTemp = LpImg[0]

            height = int(roiTemp.shape[0] / 2)
            roi1 = roiTemp[0:height, :]
            roi2 = roiTemp[height:roiTemp.shape[0], :]


            plate_info = ""
            plate_info=self.detection1line(plate_info, roi1)


            plate_info = plate_info + "-"
            plate_info= self.detection1line(plate_info, roi2)
            return plate_info
        
            
