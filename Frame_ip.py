#!/usr/bin/python3
import tkinter as tk
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfilename
import Image_Process as ip

class Frame_IPTK:
    file_path = ''


    def __init__(self):
        self.window = tk.Tk()

        self.window.title('Image Processing Toolkit')
        self.window.geometry('450x450')

        menubar = tk.Menu(self.window)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu)

        lable_origin = tk.Label(self.window, text='Origin Image', bg='white', font=('Arial', 20), width=30, height=2)
        lable_origin.place(x=35, y=10)

        self.canvas_origin = tk.Canvas(self.window, bg='green', height=350, width=350)
        self.canvas_origin.place(x=25, y=50, anchor='nw')


        self.button_origin = tk.Button(self.window, text='Select File', font=('Arial', 15), command=self.open)
        self.button_origin.place(x=25, y=420)



        self.window.config(menu=menubar)
        self.window.mainloop()


    def open(self):
        self.file_path = askopenfilename()
        im = Image.open(self.file_path, mode='r')
        self.img_origin = ImageTk.PhotoImage(im.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_origin)
        self.img_process = ip.Img(self.file_path)
