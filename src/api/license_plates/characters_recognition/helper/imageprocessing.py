import cv2
import numpy as np
from PIL import Image
def processing(image):
    # Resize the image using cv2.resize()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Thêm viền đen để tăng kích thước ảnh

    gray_img = cv2.resize(gray_image, (32, 32))
    #gray_img = cv2.cvtColor(gray_img, cv2.COLOR_BGR2GRAY)
    binary_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 7)
    # # Xác định kích thước kernel cho morphological opening
    kernel_size = 1
    # # print(binary_img.shape)
    # Tạo kernel
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    # Thực hiện morphological opening
    opening_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)
    img_rgb = cv2.cvtColor(opening_img, cv2.COLOR_GRAY2RGB)
    image_RGB = Image.fromarray(img_rgb).convert('RGB')    # Convert to PIL
    print(image_RGB.size)
    return image_RGB