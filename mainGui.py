from tkinter.filedialog import askopenfilename
import time
import pyscreenshot as ImageGrab
import cv2
from tkinter import font as tkfont
from PyPDF2 import PdfFileWriter, PdfFileReader as PDFReader, PdfFileReader
from tkinter import *
import numpy as np
from pdf2image import convert_from_path
from threading import Thread
import fitz
from tkinter.ttk import Progressbar
import math
import os
import Changes
import Bookmark
global Changesimages


## function to control pdf viewer
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


## functions to add/delete  images to/from folders
    def start(path):

        Changes.pathtoi = path
        Changes.list, Changes.W, Changes.H = convert_pdf(path)
        Changesimages = convertPDF2Img(path)
    def end():
        import os, shutil

        folder = r'image/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        folder = r'images/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        folder = r'news/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


## functions to edit pdf view
    def eye_compfort(path):
        Changes.eye_comfort(path)
        checkPDFOpen(path)
    def change_background_color(path):
        Changes.change_background_color(path)
        checkPDFOpen(path)
    def Change_text_color(path):
        Changes.change_text_color(path)
        checkPDFOpen(path)
    def book_mark(filename):
        global a, b
        a, b = scroll_y.get()
        print("a",a)
        print("b",b)
        pdf = PdfFileReader(filename)
        pages_count = pdf.getNumPages()
        pnum = b * pages_count
        pnum = round(pnum)
        Bookmark.Bitwaise(filename, pnum)
        checkPDFOpen(pdfPath)


### functions to control pdf by eyes
    def blinking():
        face_cascade = cv2.CascadeClassifier('C:/Users/Asus/PycharmProjects/pythonProject/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('C:/Users/Asus/PycharmProjects/pythonProject/venv/Lib/site-packages/cv2/data/haarcascade_eye_tree_eyeglasses.xml')

        first_read = True
        closed = False

        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        start_time = time.time()

        while (ret):
            ret, img = cap.read()
            # Coverting the recorded image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Applying filter to remove impurities
            gray = cv2.bilateralFilter(gray, 5, 1, 1)

            # Detecting the face for region of image to be fed to eye classifier
            faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(200, 200))
            if (len(faces) > 0):
                for (x, y, w, h) in faces:
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # roi_face is face which is input to eye classifier
                    roi_face = gray[y:y + h, x:x + w]
                    roi_face_clr = img[y:y + h, x:x + w]
                    eyes = eye_cascade.detectMultiScale(roi_face, 1.3, 5, minSize=(50, 50))

                    # Examining the length of eyes object for eyes
                    if (len(eyes) >= 2):
                        # Check if program is running for detection
                        if (first_read):
                            cv2.putText(img, "Eye detected press s to begin", (70, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                                        (0, 255, 0),
                                        2)
                        else:
                            cv2.putText(img, "Eyes open!", (70, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    else:
                        if (first_read):
                            # To ensure if the eyes are present before starting
                            cv2.putText(img, "No eyes detected", (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
                        else:
                            ttmp = time.time() - start_time
                            if (ttmp >= 5):
                                print("losed")
                                closed = True

                                cap.release()
                                cv2.destroyAllWindows()
                                return closed
                            elif (ttmp < 5):
                                print("Blink detected--------------")
            else:
                cv2.putText(img, "No face detected", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

            # Controlling the algorithm with keys
            cv2.imshow('img', img)
            a = cv2.waitKey(1)
            if (a == ord('q')):
                break
            elif (a == ord('s') and first_read):
                # This will start the detection
                first_read = False

        cap.release()
        cv2.destroyAllWindows()
    def screenShot():
        closed = blinking()
        print('losed')
        print(closed)
        if (closed):
            # part of the screen
            im = ImageGrab.grab(bbox=(10, 10, 800, 600))
            im.show()

            # to file
            ImageGrab.grab_to_file('C:/Users/Asus/Desktop/screenshot.png')
        else:
            print('blinked')
    def eye_scrolling():

        detector_params = cv2.SimpleBlobDetector_Params()
        detector_params.filterByArea = True
        detector_params.maxArea = 1500
        detector = cv2.SimpleBlobDetector_create(detector_params)

        face_cascade = cv2.CascadeClassifier('C:/Users/Asus/PycharmProjects/pythonProject/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('C:/Users/Asus/PycharmProjects/pythonProject/venv/Lib/site-packages/cv2/data/haarcascade_eye_tree_eyeglasses.xml')

        def detect_faces(img, cascade):
            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
            if len(coords) > 1:
                biggest = (0, 0, 0, 0)
                for i in coords:
                    if i[3] > biggest[3]:
                        biggest = i
                biggest = np.array([i], np.int32)
            elif len(coords) == 1:
                biggest = coords
            else:
                return None
            for (x, y, w, h) in biggest:
                frame = img[y:y + h, x:x + w]
            return frame

        def detect_eyes(img, cascade):
            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            eyes = cascade.detectMultiScale(gray_frame, 1.3, 5)  # detect eyes
            width = np.size(img, 1)  # get face frame width
            height = np.size(img, 0)  # get face frame height
            left_eye = None
            right_eye = None
            for (x, y, w, h) in eyes:
                if y > height / 2:
                    pass
                eyecenter = x + w / 2  # get the eye center
                if eyecenter < width * 0.5:
                    left_eye = img[y:y + h, x:x + w]
                else:
                    right_eye = img[y:y + h, x:x + w]
            return left_eye, right_eye

        def cut_eyebrows(img):
            height, width = img.shape[:2]
            eyebrow_h = int(height / 4)
            img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

            return img

        def blob_process(img, threshold, detector):
            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
            img = cv2.erode(img, None, iterations=2)
            img = cv2.dilate(img, None, iterations=4)
            img = cv2.medianBlur(img, 5)
            keypoints = detector.detect(img)
            return keypoints

        def nothing(x):
            pass
        a, b = scroll_y.get()
        cap = cv2.VideoCapture(0)
        cv2.namedWindow('image')
        cv2.createTrackbar('threshold', 'image', 0, 255, nothing)
        left = 0
        right = 0
        while True:
            _, frame = cap.read()
            face_frame = detect_faces(frame, face_cascade)
            if face_frame is not None:
                eyes = detect_eyes(face_frame, eye_cascade)
                for eye in eyes:
                    if eye is not None:
                        height, width = eye.shape[:2]
                        #threshold = 24
                        threshold = r = cv2.getTrackbarPos('threshold', 'image')
                        eye = cut_eyebrows(eye)
                        keypoints = blob_process(eye, threshold, detector)
                        for keyPoint in keypoints:
                            kx = keyPoint.pt[0]
                            ky = keyPoint.pt[1]
                            if ky < (height / 4):
                                left += 1
                                right = 0
                                if (left > 10):
                                    print("left")
                                    text.yview_moveto(a + 0.5)


                                    # cap.release()
                                    # cv2.destroyAllWindows()

                            if ky > ( height *3)/4:
                                right += 1
                                left = 0
                                if (right > 10):
                                    print("right")


                                    text.yview_moveto(a - 0.5)
                                    # cap.release()
                                    # cv2.destroyAllWindows()
                                   # text.xview_moveto(b - 0.2)
                        eye = cv2.drawKeypoints(eye, keypoints, eye, (255, 255, 255),
                                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv2.imshow('image', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()






###############################
### design Gui
    pdframe = Frame(mframe)

    top_bar = Frame(pdframe, height=40)

    button = Button(top_bar, text=" <- ", bg="white", fg='black', command=select_window)
    button.place(width=20, relheight=0.9, x=5, rely=0.05)

    button = Button(top_bar, text="start", bg="white", fg='black', command=lambda: start(pdfPath))
    button.place(width=30, relheight=0.9, x=25, rely=0.05)


    button = Button(top_bar, text=" (+) ", bg="white", fg='red', command=zoomin)
    button.place(width=25, relheight=0.9, x=60, rely=0.05)

    button = Button(top_bar, text=" (-) ", bg="white", fg='red', command=zoomout)
    button.place(width=25, relheight=0.9, x=85, rely=0.05)

    button = Button(top_bar, text=" EyeComfort ", bg="white", fg='black', command=lambda: eye_compfort(pdfPath))
    button.place(width=100, relheight=0.9, x=120, rely=0.05)

    button = Button(top_bar, text=" Change_Bg_Color ", bg="white", fg='black', command=lambda: change_background_color(pdfPath))
    button.place(width=100, relheight=0.9, x=220, rely=0.05)

    button = Button(top_bar, text=" Change_FG_Color ", bg="white", fg='black', command= lambda :Change_text_color(pdfPath))
    button.place(width=100, relheight=0.9, x=320, rely=0.05)

    button = Button(top_bar, text=" Add Bookmark ", bg="white", fg='red', command=lambda: book_mark(pdfPath))
    button.place(width=100, relheight=0.9, x=420, rely=0.05)

    button = Button(top_bar, text=" ScrollEye ", bg="white", fg='red', command=lambda: eye_scrolling())
    button.place(width=100, relheight=0.9, x=520, rely=0.05)

    button = Button(top_bar, text=" ScreenShotEye", bg="white", fg='red', command=lambda: screenShot())
    button.place(width=100, relheight=0.9, x=620, rely=0.05)

    button = Button(top_bar, text=" end", bg="white", fg='red', command=lambda: end())
    button.place(width=50, relheight=0.9, x=720, rely=0.05)

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

# functions to convert pdf to images
def convertPDF2Img (path):

    re(path)
    copyPDf('result3.pdf', path)

    imglist = []
    images = convert_from_path(path)
    for i, image in enumerate(images):
        fname = 'image/page-' + str(i) + ".png"
        image.save(fname, "PNG")
        newsize = (425, 550)
        image = image.resize(newsize)
        imglist.append(image)
    return imglist
def convert_pdf(path):
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
    return list,W,H




# functions to setting files and windows
def copyPDf(fromp, top):
    from_pdf = open(fromp, "rb")
    output = PdfFileWriter()
    input = PdfFileReader(from_pdf)  # open input

    n = input.getNumPages()

    for i in range(n):
        output.addPage(input.getPage(i))  # insert page

    def copyPDf(fromp, top):
        from_pdf = open(fromp, "rb")
        output = PdfFileWriter()
        input = PdfFileReader(from_pdf)  # open input

        n = input.getNumPages()

        for i in range(n):
            output.addPage(input.getPage(i))  # insert page




        with open(top, 'wb+') as f:
            output.write(f)

    def re(pdf):
        writer = PdfFileWriter()
        pdf = PdfFileReader(pdf)
        nn = pdf.getNumPages()
        for i in range(nn):
            page0 = pdf.getPage(i)
            page0.scaleBy((0.5))
            writer.addPage(page0)
        #
        # page0 = pdf.getPage(0)
        # page0.scaleBy(0.5)  # float representing scale factor - this happens in-place
        #   # create a writer to save the updated results

        with open('F:/result3.pdf', 'wb+') as f:
            writer.write(f)
    with open(top,'wb+') as f:
        output.write(f)
def re(pdf):
    writer = PdfFileWriter()
    pdf = PdfFileReader(pdf)
    nn = pdf.getNumPages()
    for i in range(nn):
        page0 = pdf.getPage(i)
        page0.scaleBy((0.5))
        writer.addPage(page0)
    #
    # page0 = pdf.getPage(0)
    # page0.scaleBy(0.5)  # float representing scale factor - this happens in-place
    #   # create a writer to save the updated results

    with open('result3.pdf','wb+') as f:
        writer.write(f)
def resized_window(par=None):
    if text and img_object_li:
        text.place_forget()
        text.place(relheight=1, width=min(pdframe.winfo_width(), img_object_li[0].width()), y=0, relx=0.5, anchor=N)
def select_window():
    pdframe.place_forget()
    window.geometry("600x350")
    main_frame.place(relwidth=1, relheight=1)
def handleFile(fileEntry):

    file = askopenfilename(defaultextension=".pdf",
                           filetypes=[("PDF files", "*.pdf")])
    # files = file
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








### create Gui
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
openFileButton.place(x=247, y=10)

openPDF = Button(main_frame, text="Read", font=('arial', 12, 'bold'),
                 bg="white", fg='red', width=30, height=2,
                 command=lambda: checkPDFOpen(fileEntry.get()))
openPDF.place(x=150, y=120)
window.mainloop()



























# def key_press(key):
#
#     print(key, 'is pressed')
#     a, b = scroll_y.get()
#     text.yview_moveto(a + 0.2)
#
#     print('llllllllll')
#
# def on_configure(event):
#
#     a, b = scroll_y.get()
#     print(a)
#     text.yview_moveto(a + 0.2)
#
#     print('llllllllll')
#     print(a)
#
#
#
# def get_pagge(p):
#     text.yview_moveto(a)
#     # pnum = a*3
#     print('a',a)
#     print('b', b)
#     # print('pnum', pnum)