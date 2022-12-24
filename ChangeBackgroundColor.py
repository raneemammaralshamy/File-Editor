# import os
# import glob
# import ttt as bookmark
# import os
# import  MouseBookMark as mouse
# import subprocess
# import cv2
# #import mouse as ms
# from tkinter import *
# from tkinter import font as tkfont
# # from DealWithFiles import PDFReader
# from PyPDF2 import PdfFileWriter, PdfFileReader as PDFReader, PdfFileReader
# from tkPDFViewer import tkPDFViewer as pdf
# from pdf2image import convert_from_path
# from PIL import ImageTk
# from PIL.PpmImagePlugin import Image
# import numpy as np
# from tkinter import *
# import numpy as np
# import PIL.PpmImagePlugin
# from PIL import Image, ImageTk
# from pdf2image import convert_from_path
# import cv2 as cv
# # mport poppler
# from threading import Thread
# import fitz
# from tkinter.ttk import Progressbar
#
# import img2pdf
#
#
#
#
#
#
#
# p ='F:/sample.pdf'
# def change_background_color(path):
#     r, g, b = 25,25,25
#     dicrectoryofphotos = r'C:\Users\asUS\PycharmProjects\pythonProject3'
#     ttt =  BookMark.mypdf2img(path)
#     for i, image in enumerate(ttt):
#         fname = 'image' + str(i) + '.jpg'
#         img = cv2.imread(fname)
#         # print(img.shape)
#         copy = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
#         # mask
#         mask = cv.adaptiveThreshold(copy, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 53, 17)
#         # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)))
#         # cv.imshow('mask1',mask)
#         mask = cv2.bitwise_not(mask)  # invert mask
#         # cv.imshow('mask2',mask)
#         # load background (could be an image too)
#         bk = np.full(img.shape, 170, dtype=np.uint8)
#
#         bk[:, :, 0] = b
#         bk[:, :, 1] = g
#         bk[:, :, 2] = r
#         # # get masked foreground
#         fg_masked = cv2.bitwise_and(img, img, mask=mask)
#         # cv.imshow('fg_masked',fg_masked)
#         # # get masked background, mask must be inverted
#         mask = cv2.bitwise_not(mask)
#         bk_masked = cv2.bitwise_and(bk, bk, mask=mask)
#         # # combine masked foreground and masked background
#         final = cv2.bitwise_or(fg_masked, bk_masked)
#         final = cv.resize(final, (612, 792))
#         mask = cv2.bitwise_not(mask)  #
#         cv.imwrite(fname, final)
#
#     with open(path, "wb") as f:
#         f.write(img2pdf.convert([i for i in os.listdir(dicrectoryofphotos) if i.endswith(".jpg")]))
#         f.close()
#
#
#
# #change_background_color(p)