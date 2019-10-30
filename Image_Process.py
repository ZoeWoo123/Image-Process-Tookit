import skimage.io as io
import skimage.filters as f
import skimage.util as u
import scipy.ndimage as nd
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import ttk
import math
import skimage.transform as trans
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Img:

    def __init__(self, path):
        self.path = path
        self.process = tk.Toplevel()

        self.img = io.imread(self.path, as_gray = True)
        self.pro_img = self.img

        self.process.title('Processed Image')
        self.process.geometry('800x530')

        # image show
        self.canvas_processed = tk.Canvas(self.process, bg='white', height=350, width=350)
        self.canvas_processed.place(x=400, y=30, anchor='nw')

        # image processing
        # Point Processing
        labelTop = tk.Label(self.process,text="Point Processing",fg ='red')
        labelTop.place(x=25, y=10)
        # Negative / Contrast Stretching / Histogram Equalization
        label_intro_1 = tk.Label(self.process,text="Negative / Contrast Stretching / Histogram Equalization",fg='blue')
        label_intro_1.place(x=25, y=30)
        self.comboxlist_pp = ttk.Combobox(self.process, values=["Negative", "Contrast Stretching","Histogram Equalization"])
        self.comboxlist_pp.place(x=25, y=50)
        self.comboxlist_pp.bind("<<ComboboxSelected>>", self.point_process)
        #Intensity-Level Slicing
        label_intro_2 = tk.Label(self.process, text="Intensity-Level Slicing",fg='blue')
        label_intro_2.place(x=25, y=80)
        label_intro_2_1 = tk.Label(self.process, text="Min Value = ")
        label_intro_2_1.place(x=25, y=100)
        self.e1_min = tk.Entry(self.process, font=('Arial', 12))
        self.e1_min.place(x=110,y=100)
        label_intro_2_2 = tk.Label(self.process, text="Max Value = ")
        label_intro_2_2.place(x=25, y=130)
        self.e1_max = tk.Entry(self.process, font=('Arial', 12))
        self.e1_max.place(x=110, y=130)
        button_Intensity = tk.Button(self.process, text='Process', font=('Arial', 15), command=self.Intensity_level_slicing)
        button_Intensity.place(x=280, y=130)
        #Power-Law
        label_intro_3 = tk.Label(self.process, text="Power Law", fg='blue')
        label_intro_3.place(x=25, y=160)
        label_intro_3_1 = tk.Label(self.process, text="Gamma = ")
        label_intro_3_1.place(x=25, y=180)
        self.e1_gamma = tk.Entry(self.process, font=('Arial', 12))
        self.e1_gamma.place(x=110, y=180)
        button_power_law= tk.Button(self.process, text='Process', font=('Arial', 15), command=self.power_law)
        button_power_law.place(x=280, y=180)
        #Neighborhood Processing
        labelTop_2 = tk.Label(self.process, text="Neighborhood Processing", fg='red')
        labelTop_2.place(x=25, y=210)
        #smoothing
        label_intro_4 = tk.Label(self.process, text="Smoothing",fg='blue')
        label_intro_4.place(x=25, y=230)
        #box
        label_intro_4_1 = tk.Label(self.process, text="Box (m can be 3,11,21...)",fg='green')
        label_intro_4_1.place(x=25, y=250)
        label_intro_4_1_1 = tk.Label(self.process, text="m = ")
        label_intro_4_1_1.place(x=25, y=270)
        self.e2_m = tk.Entry(self.process, font=('Arial', 12))
        self.e2_m.place(x=60, y=270)
        button_box = tk.Button(self.process, text='Process', font=('Arial', 15), command=self.box)
        button_box.place(x=280, y=270)
        #Gaussian_kernel
        label_intro_4_2 = tk.Label(self.process, text="Gaussian (sigma can be 3.5,7..., truncation can be 6,12...)",fg='green')
        label_intro_4_2.place(x=25, y=300)
        label_intro_4_2_1 = tk.Label(self.process, text="sigma = ")
        label_intro_4_2_1.place(x=25, y=320)
        self.e2_sigma = tk.Entry(self.process, font=('Arial', 12))
        self.e2_sigma.place(x=120, y=320)
        label_intro_4_2_2 = tk.Label(self.process, text="truncation = ")
        label_intro_4_2_2.place(x=25, y=350)
        self.e2_truncation = tk.Entry(self.process, font=('Arial', 12))
        self.e2_truncation.place(x=120, y=350)
        button_box = tk.Button(self.process, text='Process', font=('Arial', 15), command=self.gaussian)
        button_box.place(x=280, y=350)
        #sharping
        label_intro_5 = tk.Label(self.process, text="Sharping", fg='blue')
        label_intro_5.place(x=25, y=380)
        #laplacian
        label_intro_5_1 = tk.Label(self.process, text="Laplacian", fg='green')
        label_intro_5_1.place(x=25, y=400)
        self.comboxlist_lap = ttk.Combobox(self.process,
                                          values=["[[0,1,0],[1,-4,1],[0,1,0]]", "[[1,1,1],[1,-8,1],[1,1,1]]"])
        self.comboxlist_lap.place(x=25, y=420)
        self.comboxlist_lap.bind("<<ComboboxSelected>>", self.laplacian)
        #Unsharp mask and highboost
        label_intro_5_2 = tk.Label(self.process, text="Unsharp mask and highboost", fg='green')
        label_intro_5_2.place(x=25, y=450)
        self.comboxlist_unsharp = ttk.Combobox(self.process,
                                           values=["gaussian, sigma = 0.4", "guassian, sigma = 1"])
        self.comboxlist_unsharp.place(x=25, y=470)
        self.comboxlist_unsharp.bind("<<ComboboxSelected>>", self.unsharp_mask)
        #Order Statistic
        label_intro_6 = tk.Label(self.process, text="Order Statistic", fg='blue')
        label_intro_6.place(x=300, y=420)
        label_intro_6_1 = tk.Label(self.process, text="Blur Mode", fg='green')
        label_intro_6_1.place(x=300, y=450)
        self.comboxlist_blur = ttk.Combobox(self.process,
                                               values=["gaussian", "salt", "pepper"])
        self.comboxlist_blur.place(x=300, y=470)
        self.comboxlist_blur.bind("<<ComboboxSelected>>", self.blur)
        button_blur = tk.Button(self.process, text='Show Blur', font=('Arial', 15), command=self.show_blur)
        button_blur.place(x=420, y=420)

        #draw hist and remapped Laplacian
        label_intro_7_1 = tk.Label(self.process, text="|", fg='red')
        label_intro_7_1.place(x=550, y=420)
        label_intro_7_2 = tk.Label(self.process, text="|", fg='red')
        label_intro_7_2.place(x=550, y=440)
        label_intro_7_3 = tk.Label(self.process, text="|", fg='red')
        label_intro_7_3.place(x=550, y=460)
        label_intro_7_4 = tk.Label(self.process, text="|", fg='red')
        label_intro_7_4.place(x=550, y=480)
        button_ori_hist = tk.Button(self.process, text='Origin-Image-Histogram', font=('Arial', 15), command=self.show_ori_hist)
        button_ori_hist.place(x=600, y=420)
        button_pro_hist = tk.Button(self.process, text='Processed-Image-Histogram', font=('Arial', 15), command=self.show_after_hist)
        button_pro_hist.place(x=600, y=460)


        self.process.mainloop()


    def point_process(self, *args):
        img_process = np.copy(self.img)
        x = self.img.shape[0]
        y = self.img.shape[1]
        if(self.comboxlist_pp.get() == 'Negative'):
            for i in range(x):
                for j in range(y):
                    img_process[i][j] = 255 - img_process[i][j]

        if(self.comboxlist_pp.get() == 'Contrast Stretching'):
            min = img_process.min()
            max = img_process.max()
            for i in range(x):
                for j in range(y):
                    img_process[i][j] = 255 * (img_process[i][j] - min) / (max - min)
                    img_process[i][j] = img_process[i][j].astype(np.uint8)
                    if (img_process[i][j] < 0):
                        img_process[i][j] = 0

        if(self.comboxlist_pp.get() == 'Histogram Equalization'):
            hist_stat = [0 for i in range(256)]
            for i in range(x):
                for j in range(y):
                    gray = img_process[i][j]
                    hist_stat[gray] += 1

            # equalization
            size = x * y
            equa = [0 for i in range(256)]
            equa[0] = 1.0 * hist_stat[0] / size * 255
            sum = hist_stat[0]
            for i in range(1, 255):
                sum += hist_stat[i]
                equa[i] = 1.0 * sum / size * 255
            for i in range(x):
                for j in range(y):
                    img_process[i][j] = equa[img_process[i][j]]
                    img_process[i][j] = img_process[i][j].astype(np.uint8)
        self.pro_img = img_process
        self.show(img_process)

    def Intensity_level_slicing(self):
        img_process = np.copy(self.img)
        x,y = self.img.shape
        min_range = int(self.e1_min.get())
        max_range = int(self.e1_max.get())
        if (min_range < 0 or max_range > 255):
            tk.messagebox.showerror(title='Error', message='Range should be 0 - 255')
        for i in range(x):
            for j in range(y):
                if img_process[i, j] > min_range and img_process[i, j] < max_range:
                    img_process[i, j] = 255
                else:
                    img_process[i, j] = 0
        self.pro_img = img_process
        self.show(img_process)

    def power_law(self):
        img_process = np.copy(self.img)
        try:
            g = float(self.e1_gamma.get())
        except ValueError:
            tk.messagebox.showerror(title='Error', message='Invalid Input')
        img_process = np.array(255*(img_process/255)**g,dtype='uint8')
        self.pro_img = img_process
        self.show(img_process)

    def box(self):
        img_process = np.copy(self.img)
        try:
            m = int(self.e2_m.get())
        except ValueError:
            tk.messagebox.showerror(title='Error', message='Invalid Input')
        box = np.ones((m, m)) / (m * m)
        img_process_box = nd.convolve(img_process, box, mode='constant')
        self.pro_img = img_process_box
        self.show(img_process_box)

    def gaussian(self):
        img_process = np.copy(self.img)
        try:
            sigma= float(self.e2_sigma.get())
            truncation = int(self.e2_truncation.get())
        except ValueError:
            tk.messagebox.showerror(title='Error', message='Invalid Input')
        flmag = nd.gaussian_filter(img_process, sigma, mode='constant', truncate=truncation)
        self.pro_img = flmag
        self.show(flmag)

    def laplacian(self, *args):
        img_process = np.copy(self.img)
        c = -1
        if(self.comboxlist_lap.get() == '[[0,1,0],[1,-4,1],[0,1,0]]'):
            laplace_filter = np.array([[0,1,0],[1,-4,1],[0,1,0]])
        if(self.comboxlist_lap.get() == '[[1,1,1],[1,-8,1],[1,1,1]]'):
            laplace_filter = np.array([[1,1,1],[1,-8,1],[1,1,1]])
        img_copy = img_process.astype(np.float64)
        img_sharpen = img_copy + nd.convolve(img_copy, laplace_filter * c, mode='constant')
        self.pro_img = img_sharpen
        self.show(img_sharpen)

    def unsharp_mask(self, *args):
        img_process = np.copy(self.img)
        img_process_2 = np.copy(self.img)
        if(self.comboxlist_unsharp.get() == 'gaussian, sigma = 0.4'):
            mask = img_process - f.gaussian(img_process, sigma=0.4)
        if(self.comboxlist_unsharp.get() == 'guassian, sigma = 1'):
            mask = img_process - f.gaussian(img_process, sigma=1)
        img_add_mask = mask + img_process_2
        img_add_mask = img_add_mask - np.full(img_add_mask.shape, np.min(img_add_mask))
        img_add_mask = img_add_mask * 255 / np.max(img_add_mask)
        img_add_mask = img_add_mask.astype(np.uint8)
        self.pro_img = img_add_mask
        self.show(img_add_mask)

    def blur(self, *args):
        img_process = np.copy(self.img)
        if (self.comboxlist_blur.get() == 'gaussian'):
            img_blur = u.random_noise(img_process, mode ='gaussian', seed=None, clip=True)
        if (self.comboxlist_blur.get() == 'salt'):
            img_blur = u.random_noise(img_process, mode='salt', seed=None, clip=True)
        if (self.comboxlist_blur.get() == 'pepper'):
            img_blur = u.random_noise(img_process, mode='pepper', seed=None, clip=True)
        x,y = self.img.shape
        for i in range(1,x-1):
            for j in range(1,y-1):
                nums = [img_blur[i - 1][j - 1], img_blur[i][j - 1], img_blur[i + 1][j - 1], img_blur[i - 1][j],
                        img_blur[i][j],img_blur[i + 1][j], img_blur[i - 1][j + 1], img_blur[i][j + 1], img_blur[i + 1][j + 1]]
                img_blur[i][j] = np.median(nums)
        self.show(img_blur)

    def rescale(self, image):
        min_b = image.min()
        max_b = image.max()
        max_a = self.img.max()
        min_a = self.img.min()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                image[i][j] = math.floor((image[i][j] - min_b) / (max_b - min_b) * (max_a - min_a) + min_a)
        return image


    def show_blur(self,*args):
        img_process = np.copy(self.img)
        if (self.comboxlist_blur.get() == 'gaussian'):
            img_blur = u.random_noise(img_process, mode='gaussian', seed=None, clip=True)
        if (self.comboxlist_blur.get() == 'salt'):
            img_blur = u.random_noise(img_process, mode='salt', seed=None, clip=True)
        if (self.comboxlist_blur.get() == 'pepper'):
            img_blur = u.random_noise(img_process, mode='pepper', seed=None, clip=True)
        blur_win = tk.Toplevel()
        blur_win.title('Blurred Image')
        blur_win.geometry('400x400')
        canvas_blur = tk.Canvas(blur_win, bg='green', height=350, width=350)
        canvas_blur.pack()
        image_2 = trans.resize(img_blur, (350, 350), anti_aliasing=True)
        image_blur_b = self.rescale(image_2)
        img_blur_a = Image.fromarray(image_blur_b)
        self.img_ready_2 = ImageTk.PhotoImage(img_blur_a)
        canvas_blur.create_image(0, 0, anchor='nw', image=self.img_ready_2)

    def show_ori_hist(self):
        img_process = np.copy(self.img)
        ori_hist = tk.Toplevel()
        ori_hist.title('Origin Image Histgram')
        ori_hist.geometry('400x400')
        image_ori_hist = trans.resize(img_process, (350, 350), anti_aliasing=True)
        image_ori_hist = self.rescale(image_ori_hist)
        fig = Figure(figsize=(5, 4), dpi=100)
        gray_level_n = []
        for i in range(image_ori_hist.shape[0]):
            for j in range(image_ori_hist.shape[1]):
                gray_level_n.append(image_ori_hist[i][j])
        fig.add_subplot(111).hist(gray_level_n)

        canvas = FigureCanvasTkAgg(fig, master=ori_hist)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def show_ori_hist(self):
        img_process = np.copy(self.img)
        ori_hist = tk.Toplevel()
        ori_hist.title('Origin Image Histgram')
        ori_hist.geometry('400x400')
        image_ori_hist = trans.resize(img_process, (350, 350), anti_aliasing=True)
        image_ori_hist = self.rescale(image_ori_hist)
        fig = Figure(figsize=(5, 4), dpi=100)
        gray_level_n = []
        for i in range(image_ori_hist.shape[0]):
            for j in range(image_ori_hist.shape[1]):
                gray_level_n.append(image_ori_hist[i][j])
        fig.add_subplot(111).hist(gray_level_n)

        canvas = FigureCanvasTkAgg(fig, master=ori_hist)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def show_after_hist(self):
        img_process = np.copy(self.pro_img)
        pro_hist = tk.Toplevel()
        pro_hist.title('Processed Image Histgram')
        pro_hist.geometry('400x400')
        image_pro_hist = trans.resize(img_process, (350, 350), anti_aliasing=True)
        image_pro_hist = self.rescale(image_pro_hist)
        fig = Figure(figsize=(5, 4), dpi=100)
        gray_level_n = []
        for i in range(image_pro_hist.shape[0]):
            for j in range(image_pro_hist.shape[1]):
                gray_level_n.append(image_pro_hist[i][j])
        fig.add_subplot(111).hist(gray_level_n)

        canvas = FigureCanvasTkAgg(fig, master=pro_hist)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def show(self, img_process):
        image = trans.resize(img_process, (350, 350), anti_aliasing=True)
        image_b = self.rescale(image)
        image = Image.fromarray(image_b)
        self.img_ready = ImageTk.PhotoImage(image)
        self.canvas_processed.create_image(0, 0, anchor='nw', image=self.img_ready)




