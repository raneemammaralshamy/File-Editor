import cv2
from cv2 import cv2 as cv
from tkinter import *
import numpy as np
from PIL import Image
import os


### global variable
pathtoi = ""
list =[]
W=0
H= 0
images = []

def nothing(x):
    pass
def gamma_function(channel, gamma):
    invGamma = 1 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")  # creating lookup table
    channel = cv2.LUT(channel, table)
    return channel
def detect_color():
    test = np.zeros((300,512,3),np.uint8)
    cv.namedWindow('image')
    cv.createTrackbar('B', 'image', 0, 255, nothing)
    cv.createTrackbar('G', 'image', 0, 255, nothing)
    cv.createTrackbar('R', 'image', 0, 255, nothing)
    while (1):
        cv.imshow('image', test)
        k = cv.waitKey(1)
        if k == 27:
            break
        b = cv.getTrackbarPos('B', 'image')
        g = cv.getTrackbarPos('G', 'image')
        r = cv.getTrackbarPos('R', 'image')
        test[:]=b,g,r
    cv.destroyAllWindows()
    return r,g,b

def eye_comfort(path):

    imglist =[]

    for filename in os.listdir("image"):
        f = os.path.join("image/", filename)
        imglist.append(f)
        img = cv2.imread(f)
        #print(img.shape)
        height = img.shape[0]
        width = img.shape[1]
        img[:, :, 0] = gamma_function(img[:, :, 0], 0.75)  # down scaling blue channel
        img[:, :, 2] = gamma_function(img[:, :, 2], 1.25)  # up scaling red channel
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = gamma_function(hsv[:, :, 1], 1.2)  # up scaling saturation channel
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        final = img.copy()
        for page in list:
            if page[0] == f:
                img = cv.imread(page[1])
                h_s= img.shape[0]
                w_s = img.shape[1]
                coord = page[2]
                x0 = coord[0]
                y0 = coord[1]
                x1 = coord[2]
                y1 = coord[3]
                new_x0 = int((x0 * width) / W)
                new_y0 = int((y0 * height) / H)
                new_x1 = int((x1 * width) / W)
                new_y1 = int((y1 * height) / H)
                img = cv.resize(img, (new_x1 - new_x0, new_y1 - new_y0))
                final[new_y0:new_y1, new_x0:new_x1] = img
        cv.imwrite(f, final)

    im_list = []
    img1 = Image.open(imglist[0])
    for j in range(len(imglist) - 1):
        im_list.append(Image.open(imglist[j + 1]))
    img1.save(path, save_all=True, append_images=im_list)
def change_background_color(path):

    imglist = []

    r, g, b = detect_color()
    for filename in os.listdir("image"):
        f = os.path.join("image/", filename)
        img = cv2.imread(f)
        imglist.append(f)
        height = img.shape[0]
        width = img.shape[1]
        # print(img.shape)
        copy = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        ret, mask = cv2.threshold(copy, 127, 255, cv.THRESH_BINARY)
        # if np.sum(img == 255) < np.sum(img == 0):
        #     # mask = cv.adaptiveThreshold(copy,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,53,17)
        #     ret, mask = cv2.threshold(copy, 127, 255, cv.THRESH_BINARY_INV)
        mask
        mask = cv.adaptiveThreshold(copy, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 53, 17)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)))
        # cv.imshow('mask1',mask)
        mask = cv2.bitwise_not(mask)  # invert mask
        # cv.imshow('mask2',mask)
        # load background (could be an image too)
        bk = np.full(img.shape, 170, dtype=np.uint8)

        bk[:, :, 0] = b
        bk[:, :, 1] = g
        bk[:, :, 2] = r
        # # get masked foreground
        fg_masked = cv2.bitwise_and(img, img, mask=mask)
        # cv.imshow('fg_masked',fg_masked)
        # # get masked background, mask must be inverted
        mask = cv2.bitwise_not(mask)
        bk_masked = cv2.bitwise_and(bk, bk, mask=mask)
        # # combine masked foreground and masked background
        final = cv2.bitwise_or(fg_masked, bk_masked)
        mask = cv2.bitwise_not(mask)  # revert mask to original

        for page in list:
            if page[0] == f:
                img = cv.imread(page[1])
                h_s = img.shape[0]
                w_s = img.shape[1]
                # print(img.shape)
                coord = page[2]
                x0 = coord[0]
                y0 = coord[1]
                x1 = coord[2]
                y1 = coord[3]
                new_x0 = int((x0 * width) / W)
                new_y0 = int((y0 * height) / H)
                new_x1 = int((x1 * width) / W)
                new_y1 = int((y1 * height) / H)
                img = cv.resize(img, (new_x1 - new_x0, new_y1 - new_y0))
                final[new_y0:new_y1, new_x0:new_x1] = img
        cv.imwrite(f, final)

    im_list = []
    img1 = Image.open(imglist[0])
    for j in range(len(imglist) - 1):
        im_list.append(Image.open(imglist[j + 1]))
    img1.save(path, save_all=True, append_images=im_list)
def change_text_color(path):
    imglist = []

    r, g, b = detect_color()
    for filename in os.listdir("image"):
        f = os.path.join("image/", filename)
        imglist.append(f)
        img = cv2.imread(f)
        height = img.shape[0]
        width = img.shape[1]
        # print(img.shape)
        copy = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

        ret, mask = cv2.threshold(copy, 127, 255, cv.THRESH_BINARY)
        # if np.sum(img == 255) < np.sum(img == 0):
        #     # mask = cv.adaptiveThreshold(copy,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,53,17)
        #     ret, mask = cv2.threshold(copy, 127, 255, cv.THRESH_BINARY_INV)

        mask = cv.adaptiveThreshold(copy, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 41, 11)

        mask = cv2.bitwise_not(mask)  # invert mask

        # load foreground (could be an image too)

        fk = np.full(img.shape, 255, dtype=np.uint8)
        fk[:, :, 0] = b
        fk[:, :, 1] = g
        fk[:, :, 2] = r

        # get masked foreground
        fg_masked = cv2.bitwise_and(fk, fk, mask=mask)

        # get masked background, mask must be inverted
        mask = cv2.bitwise_not(mask)
        bk_masked = cv2.bitwise_and(img, img, mask=mask)

        # combine masked foreground and masked background
        final = cv2.bitwise_or(fg_masked, bk_masked)
        mask = cv2.bitwise_not(mask)  # revert mask to original

        for page in list:
            if page[0] == f:
                img = cv.imread(page[1])
                h_s = img.shape[0]
                w_s = img.shape[1]
                # print(img.shape)
                coord = page[2]
                x0 = coord[0]
                y0 = coord[1]
                x1 = coord[2]
                y1 = coord[3]
                new_x0 = int((x0 * width) / W)
                new_y0 = int((y0 * height) / H)
                new_x1 = int((x1 * width) / W)
                new_y1 = int((y1 * height) / H)
                img = cv.resize(img, (new_x1 - new_x0, new_y1 - new_y0))
                final[new_y0:new_y1, new_x0:new_x1] = img
        cv.imwrite(f, final)

    im_list = []
    img1 = Image.open(imglist[0])
    for j in range(len(imglist) - 1):
        im_list.append(Image.open(imglist[j + 1]))
    img1.save(path, save_all=True, append_images=im_list)