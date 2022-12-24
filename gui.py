from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path
from tkPDFViewer import tkPDFViewer as pdf
import os


# Creating Tk container
root = Tk()

root.geometry("800x800")
root.title('Pdf Viewer')
root.configure(bg="white")


def browseFiles():
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                          title = 'select pdf file',
                                          filetype = (('PDF FILE','.pdf'),
                                                      ('PDF FILE','.PDF'),
                                                      ('ALL FILE','.txt')
                                                      ))
    pdf_frame = Frame(root).pack(fill=BOTH, expand=1)
    # Adding Scrollbar to the PDF frame
    scrol_y = Scrollbar(pdf_frame, orient=VERTICAL)
    # Adding text widget for inserting images
    pdf = Text(pdf_frame, yscrollcommand=scrol_y.set, bg="white")
    # Setting the scrollbar to the right side
    scrol_y.pack(side=RIGHT, fill=Y)
    scrol_y.config(command=pdf.yview)
    # Finally packing the text widget
    pdf.pack(fill=BOTH, expand=1)
    # Here the PDF is converted to list of images
    pages = convert_from_path(filename, size=(800, 900))
    imglist = []
    for i, image in enumerate(pages):
        fname = 'C:/Users/Asus/Desktop/images/page' + str(i) + ".png"
        image.save(fname, "PNG")
        imglist.append(image)
    pages = imglist
    # Empty list for storing images
    photos = []
    # Storing the converted images into list
    for i in range(len(pages)):
        photos.append(ImageTk.PhotoImage(pages[i]))
    # Adding all the images to the text widget
    for photo in photos:
        pdf.image_create(END, image=photo)

        # For Seperating the pages
        pdf.insert(END, '\n\n')
    mainloop()

Button(root, text='open', command=browseFiles, width=20, font="arial 20", bd=4).pack()


root.mainloop()