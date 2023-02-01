
import cv2
import numpy as np
from sklearn.metrics import f1_score
import tensorflow.keras as keras
from BienSoXe.lib_detection import load_model, detect_lp, im2single
import tensorflow as tf

# Metrics for checking the model performance while training
def f1score(y, y_pred):
  return f1_score(y, tf.math.argmax(y_pred, axis=1), average='micro') 

def custom_f1score(y, y_pred):
  return tf.py_function(f1score, (y, y_pred), tf.double)

# Ham sap xep contour tu trai sang phai
def sort_contours(cnts):

    reverse = False
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts

# Dinh nghia cac ky tu tren bien so
char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ-'





# Ham fine tune bien so, loai bo cac ki tu khong hop ly
def fine_tune(lp):
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString

# Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
Dmax = 608
Dmin = 288
# Load model LP detection
wpod_net_path = "BienSoXe/wpod-net_update1.json"
wpod_net = load_model(wpod_net_path)

# Cau hinh tham so cho model SVM
digit_w = 30 # Kich thuoc ki tu
digit_h = 60 # Kich thuoc ki tu

model = keras.models.load_model('D:/KhoaLuanTonNghiep/License/CauHinhFlashAPI/BienSoXe/nnt_digit_cnn.h5',custom_objects={"custom_f1score": custom_f1score })

def detection(Ivehicle):


    Width = Ivehicle.shape[1]
    Height = Ivehicle.shape[0]

    # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
    ratio = float(max(Ivehicle.shape[:2])) / min(Ivehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)

    _ , LpImg, lp_type = detect_lp(wpod_net, im2single(Ivehicle), bound_dim, lp_threshold=0.5)

    if (len(LpImg)):

        # Chuyen doi anh bien so
        LpImg[0] = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))

        roi = LpImg[0]
        print("Roi",roi.shape)
        # Chuyen anh bien so ve gray
        gray = cv2.cvtColor( roi, cv2.COLOR_BGR2GRAY,)
        print(gray.shape)

        # Ap dung threshold de phan tach so va nen
        binary = cv2.threshold(gray, 127, 255,
                            cv2.THRESH_BINARY_INV)[1]


        print("Anh bien so sau threshold",binary.shape)


        # Segment kí tự
        kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
        cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


        plate_info = ""

        for c in sort_contours(cont):
            (x, y, w, h) = cv2.boundingRect(c)
            ratio = h/w
            if 1.5<=ratio<=3.5: # Chon cac contour dam bao ve ratio w/h
                if h/roi.shape[0]>=0.6: # Chon cac contour cao tu 60% bien so tro len


                    print("e khung chu nhat quanh so",roi.shape)
                    # Tach so va predict
                    curr_num = thre_mor[y:y+h,x:x+w]



                    img = cv2.cvtColor(curr_num, cv2.COLOR_BGR2RGB)

                    img = cv2.resize(img,(28,28),3)
                    img = tf.image.resize_with_pad(img, 28, 28, antialias=True)

                    print("Anh bien so sau khi convert",img.shape)

                    img = img[np.newaxis, :, :, :]

                    print("Anh bien so sau khi 4D",img.shape)
                    # 
                    # Dua vao model SVM
                    
                    result = model.predict(img)

                    result = np.argmax(result,axis = 1)
                    result_test = result[0]
                    print("ket qua tra ve MAX tu model",result[0])
                    if result_test<=9: # Neu la so thi hien thi luon
                        result_test = str(result_test)
                    else: #Neu la chu thi chuyen bang ASCII
                        print("result_test",result_test)
                        result_test = chr(result_test+55)
                    print(result[0])
                    plate_info +=result_test
        return plate_info





# cv2.destroyAllWindows()


# if __name__== "__main__":
#     detection_SVM(image)