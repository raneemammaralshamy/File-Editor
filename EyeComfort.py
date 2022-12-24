import os
import numpy as np
import cv2
from cv2 import cv2 as cv
import remove_image
import img2pdf
from PIL import Image

def gamma_function(channel, gamma):
    invGamma = 1 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")  # creating lookup table
    channel = cv2.LUT(channel, table)
    return channel


def convertPDF2Img (path):
    imglist = []
    images = convert_from_path(path)
    for i, image in enumerate(images):
        fname = 'image/page-' + str(i) + ".png"
        image.save(fname, "PNG")
        imglist.append(image)
    return imglist

def convert_pdf(path):
    global W
    global H
    mat = fitz.Matrix(fitz.Identity)
    doc = fitz.open(path)
    for page in doc:  # iterate through the pages
            pix = page.get_pixmap(matrix=mat)  # render page to an image

            pix.save('images/page-' + str(page.number) +'.png')

            # print(pix.width)
            W = pix.width
            H = pix.height
            # print(pix.height)
            # print("***************")


    list=[]
    for i in range(len(doc)):
        page = doc[i]
        j=0
        url_page = 'image/page-' + str(i) + '.png'
        imglist.append(url_page)
        for img in doc.get_page_images(i,full=True):
            j+=1
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.save("news/page-%s-%s.png" % (i, j))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.save("news/page-%s-%s.png" % (i, j))
                pix1 = None
            # print(pix.width)
            # print(pix.height)
            # print("***************")
            url_image = "news/page-%s-%s.png" % (i, j)
            # print(url)
            # print(pix)
            pix = None
            coord = page.get_image_bbox(img).round()
            list.append([url_page,url_image,coord])
    return(list)



def eye_comfort(path):

    imglist=[]
    images = convertPDF2Img(path)
    list =convert_pdf(path)

    for filename in os.listdir('image'):
        f = os.path.join("image", filename)
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
    img1.save('training.pdf', save_all=True, append_images=im_list)
    remove_image.checkPDFOpen('training.pdf')