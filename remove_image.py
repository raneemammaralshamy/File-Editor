import fitz
import cv2
import img2pdf
from cv2 import cv2 as cv
import numpy as np
import os
import shutil
from PIL import Image
from pdf2image import convert_from_path
import cv2
from tkinter import *
from tkinter import font as tkfont
from PyPDF2 import PdfFileWriter, PdfFileReader as PDFReader
from tkPDFViewer import tkPDFViewer as pdf
from pdf2image import convert_from_path
from PIL import ImageTk
from PIL.PpmImagePlugin import Image
import numpy as np
from tkinter import *
import numpy as np
import PIL.PpmImagePlugin
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import cv2 as cv
from threading import Thread
import fitz
from tkinter.ttk import Progressbar
import math
import os
import subprocess







#*****************************************************************************************************



imglist=[]
path_of_the_directory = 'C:/Users/Asus/Desktop/image/'
copy_path = 'C:/Users/Asus/Desktop/copy'
file=r'C:/Users/Asus/Desktop/sample.pdf'

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


def convertPDF2Img (path):
    imglist = []
    images = convert_from_path(path)
    for i, image in enumerate(images):
        fname = 'C:/Users/Asus/Desktop/image/page-' + str(i) + ".png"
        image.save(fname, "PNG")
        imglist.append(image)
    return imglist

def convert_pdf():
    global W
    global H
    mat = fitz.Matrix(fitz.Identity)
    doc = fitz.open('C:/Users/Asus/Desktop/core.pdf')
    for page in doc:  # iterate through the pages
            pix = page.get_pixmap(matrix=mat)  # render page to an image

            pix.save('C:/Users/Asus/Desktop/images/page-' + str(page.number) +'.png')

            # print(pix.width)
            W = pix.width
            H = pix.height
            # print(pix.height)
            # print("***************")


    list=[]
    for i in range(len(doc)):
        page = doc[i]
        j=0
        url_page = 'C:/Users/Asus/Desktop/image/page-' + str(i) + '.png'
        imglist.append(url_page)
        for img in doc.get_page_images(i,full=True):
            j+=1
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.save("C:/Users/Asus/Desktop/news/page-%s-%s.png" % (i, j))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.save("C:/Users/Asus/Desktop/news/page-%s-%s.png" % (i, j))
                pix1 = None
            # print(pix.width)
            # print(pix.height)
            # print("***************")
            url_image = "C:/Users/Asus/Desktop/news/page-%s-%s.png" % (i, j)
            # print(url)
            # print(pix)
            pix = None
            coord = page.get_image_bbox(img).round()
            list.append([url_page,url_image,coord])
    return(list)

def eye_comfort():
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory, filename)
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
    img1.save(file, save_all=True, append_images=im_list)
    checkPDFOpen(file)

def change_background_color():
    r, g, b = detect_color()
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory, filename)
        img = cv2.imread(f)
        height = img.shape[0]
        width = img.shape[1]
        # print(img.shape)
        copy = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        # mask
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
    img1.save(file, save_all=True, append_images=im_list)
    checkPDFOpen(file)

def change_text_color():
    r, g, b = detect_color()
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory, filename)
        img = cv2.imread(f)
        height = img.shape[0]
        width = img.shape[1]
        # print(img.shape)
        copy = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
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
    im_list=[]
    img1 = Image.open(imglist[0])
    for j in range(len(imglist) - 1):
        im_list.append(Image.open(imglist[j + 1]))
    img1.save(file, save_all=True, append_images=im_list)
    checkPDFOpen(file)

def pdf_viewer(pdfPath, reader):
    global pdframe, percentage_view, percentage_load, img_object_li, original_dpi, text
    main_frame.place_forget()
    window.resizable(1, 1)
    window.geometry("800x600")
    original_dpi = 72

    def zoomin():
        global original_dpi
        original_dpi += 20
        add_img(original_dpi)

    def zoomout():
        global original_dpi
        original_dpi -= 20
        add_img(original_dpi)

    # def book_mark():


    # def book_mark(filename, bname, page):
    #     # print("klkllkkkjkljlk")
    #     bookmark.set_bookMark(filename, bname, page)
    #     #############
    #     tep = PDFReader("E:result3.pdf")
    #
    #     bookmark.copyPDf2("E:result3.pdf", filename)
    #     reader1 = PDFReader(filename)
    #     tt2 = bookmark.bookmark_dict(reader1.getOutlines(), reader1)
    #     print("book mark")
    #     print(tt2)

        #########

    pdframe = Frame(mframe)

    top_bar = Frame(pdframe, height=40)

    button = Button(top_bar, text=" <- ", bg="white", fg='black', command=select_window)
    button.place(width=50, relheight=0.9, x=5, rely=0.05)


    button = Button(top_bar, text=" zoom(+) ", bg="white", fg='red', command=zoomin)
    button.place(width=50, relheight=0.9, x=60, rely=0.05)

    button = Button(top_bar, text=" zoom(-) ", bg="white", fg='red', command=zoomout)
    button.place(width=50, relheight=0.9, x=110, rely=0.05)

    button = Button(top_bar, text=" EyeComfort ", bg="white", fg='black', command=lambda: eye_comfort())
    button.place(width=100, relheight=0.9, x=165, rely=0.05)

    button = Button(top_bar, text=" Change_Bg_Color ", bg="white", fg='black', command=lambda: change_background_color())
    button.place(width=100, relheight=0.9, x=265, rely=0.05)

    button = Button(top_bar, text=" Change_FG_Color ", bg="white", fg='black', command= lambda :change_text_color())
    button.place(width=100, relheight=0.9, x=365, rely=0.05)

    button = Button(top_bar, text=" Add Bookmark ", bg="white", fg='red', command=lambda: change_text_color())
    button.place(width=100, relheight=0.9, x=470, rely=0.05)

    button = Button(top_bar, text=" ScrollEye ", bg="white", fg='red', command=lambda: change_text_color())
    button.place(width=100, relheight=0.9, x=570, rely=0.05)

    button = Button(top_bar, text=" ScreenShotEye", bg="white", fg='red', command=lambda: change_text_color())
    button.place(width=100, relheight=0.9, x=670, rely=0.05)


    # label = Label(top_bar,text="Enter Book_Mark name")
    # label.pack()
    # T = Text(top_bar,width=80,height = 2).pack()
    #

    # button = Button(top_bar, text="add a  Bookmark", bg="gray", fg='gold',
    #                 command=lambda: book_mark(pdfPath, "Book_Mark2", 30))
    # button.place(width=80, relheight=0.9, x=320, rely=0.05)

    top_bar.pack(side=TOP, fill=X)

    pdf_frame = Frame(pdframe)

    width, height = (800, 600)

    frame = Frame(pdf_frame)

    img_object_li = []
    percentage_view = 0
    percentage_load = StringVar()

    display_msg = Label(textvariable=percentage_load)
    display_msg.pack(pady=10)

    loading = Progressbar(frame, orient=HORIZONTAL, length=100, mode='determinate')
    loading.pack(side=TOP, fill=X)

    text = Text(frame)

    scroll_y = Scrollbar(frame, orient="vertical", command=text.yview)
    scroll_x = Scrollbar(frame, orient="horizontal", command=text.xview)

    scroll_x.pack(fill="x", side="bottom")
    scroll_y.pack(fill="y", side="right")

    # # temps = Scrollbar.getint()
    # print(type(text.xview))

    text.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    text.configure(bg="#c1c1c1")
    text.pack(side=LEFT, expand=1, fill=BOTH)

    scroll_x.config(command=text.xview)
    scroll_y.config(command=text.yview)

    def add_img(dpi):
        global percentage_view, percentage_load, img_object_li
        img_object_li = []
        precentage_dicide = 0
        open_pdf = fitz.open(pdfPath)
        for page in open_pdf:
            pix = page.get_pixmap(dpi=dpi)
            pix1 = fitz.Pixmap(pix, alpha=0) if pix.alpha else pix
            img = pix1.tobytes("ppm")

            timg = PhotoImage(data=img)
            img_object_li.append(timg)
            precentage_dicide = precentage_dicide + 1
            percentage_view = (float(precentage_dicide) /
                               float(len(open_pdf)) *float(100))
            loading['value'] = percentage_view
            percentage_load.set(f"loading.. {int(math.floor(percentage_view))}%")
        loading.pack_forget()
        display_msg.pack_forget()

        text.delete("1.0", END)

        for i in img_object_li:
            text.image_create(END, image=i)
            text.insert(END, "\n\n")
        text.place_forget()
        text.place(relheight=1, width=min(pdframe.winfo_width(), img_object_li[0].width()), y=0, relx=0.5, anchor=N)

    def start_pack():
        t1 = Thread(target=lambda: add_img(72))
        t1.start()

    frame.pack(side=BOTTOM, expand=1, fill=BOTH)

    pdf_frame.pack(expand=1, fill=BOTH, side=BOTTOM)

    pdf_frame.after(250, start_pack)

    pdframe.place(relwidth=1, relheight=1)






def resized_window(par=None):
    if text and img_object_li:
        text.place_forget()
        text.place(relheight=1, width=min(pdframe.winfo_width(), img_object_li[0].width()), y=0, relx=0.5, anchor=N)


def select_window():
    pdframe.place_forget()
    window.geometry("600x350")
    main_frame.place(relwidth=1, relheight=1)


def handleFile(fileEntry):
    from tkinter.filedialog import askopenfilename
    file = askopenfilename(defaultextension=".pdf",
                           filetypes=[("PDF files", "*.pdf")])
    files = file
    if file == "":
        file = None
    else:
        fileEntry.delete(0, END)
        fileEntry.config(fg="blue")
        fileEntry.insert(0, file)


def checkPDFOpen(pdfPath):
    if pdfPath == "":
        return
    if not os.path.exists(pdfPath):
        return
    try:
        reader = PDFReader(pdfPath)
        pdf_viewer(pdfPath, reader)
    except Exception:
        pass










####################################################################################


path = 'C:/Users/Asus/Desktop/core.pdf'
images = convertPDF2Img(path)
list = convert_pdf()


for file_name in os.listdir(path_of_the_directory):
    # construct full file path
    source = path_of_the_directory + file_name
    destination = copy_path + file_name
    # copy only files
    if os.path.isfile(source):
        shutil.copy(source, destination)



window = Tk()
window.title_font = tkfont.Font(family='Helvetica', size=26, weight="bold", slant="italic")
window.title("Pdf Viewer")
window.geometry("600x350")
window.config(bg='gray')
window.resizable(0, 0)

window.bind('<Configure>', resized_window)

mframe = Frame(window)
mframe.place(relwidth=1, relheight=1)
main_frame = Frame(mframe)
main_frame.place(relwidth=1, relheight=1)
pdframe = None
text = None
percentage_view = None
original_dpi = None
percentage_load = None
img_object_li = []

fileEntry = Entry(main_frame, font=('arial', 12), width=50)
fileEntry.place(x=100, y=55)
# ===========button to access openFile method=================================
openFileButton = Button(main_frame, text="Select Pdf File", font=('arial', 12, 'bold'), width=12,
                        bg="white", fg='black', command=lambda: handleFile(fileEntry))
openFileButton.place(x=250, y=10)

openPDF = Button(main_frame, text="Read", font=('arial', 12, 'bold'),
                 bg="white", fg='red', width=30, height=2,
                 command=lambda: checkPDFOpen(fileEntry.get()))
openPDF.place(x=150, y=120)
window.mainloop()


# eye_comfort()
# change_background_color()
# change_text_color()

#
#
#
#
