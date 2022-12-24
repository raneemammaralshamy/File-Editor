import os
import cv2
from PyPDF2 import PdfFileWriter,  PdfFileReader
#from tkinter import *
from PIL import Image



def Bitwaise(pathofPdf,pageNum):

    imglist = []
    i=0

    for filename in os.listdir("image"):

        f = os.path.join("image/", filename)
        img1 = cv2.imread(f)
        imglist.append(f)

        mask = img1[60:120, 75:150]
        img1[0:60, 0:75] = mask




        if(int(pageNum)==i+1):

            img2 = cv2.imread(r"C:/Users/Asus/Desktop/R.png")
            img2 = cv2.resize(img2, (45, 30))
            h1, w1, _ = img1.shape


            r, c, ch = img2.shape
            roi = img1[0:r, 0:c]
            img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 220, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            img1_bg = cv2.bitwise_and(roi, roi, mask=mask)
            img2_fb = cv2.bitwise_and(img2, img2, mask=mask_inv)
            dst = cv2.add(img1_bg, img2_fb)
            img1[0:r , 0:c] = dst
        i=i+1

        cv2.imwrite(f, img1)

    im_list = []
    img1 = Image.open(imglist[0])
    for j in range(len(imglist) - 1):
        im_list.append(Image.open(imglist[j + 1]))
    img1.save(pathofPdf, save_all=True, append_images=im_list)
def re(pdf):

    writer = PdfFileWriter()
    pdf = PdfFileReader(pdf)
    nn = pdf.getNumPages()
    for i in range(nn):
        page0 = pdf.getPage(i)
        page0.scaleBy((0.5))
        writer.addPage(page0)


    with open('result3.pdf','wb+') as f:
        writer.write(f)





