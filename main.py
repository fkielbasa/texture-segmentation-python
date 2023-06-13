import tkinter as tk
from random import random
from tkinter import ttk, filedialog
import random
import PIL
import cv2
import numpy
import numpy as np
from PIL import ImageTk, ImageOps
from PIL.Image import Image
from matplotlib import pyplot as plt
from numpy import indices
from skimage import data
from skimage.color import rgb2gray
from skimage.feature import local_binary_pattern
from skimage.filters import gabor, try_all_threshold
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage.restoration import estimate_sigma, denoise_nl_means
from skimage.util import img_as_float, img_as_ubyte
from sklearn import preprocessing
from sklearn.cluster import KMeans

root = tk.Tk()
root.title("Segmentacja teksturowa")
root.geometry("1200x700")
root.configure(bg="#b4bbbf")

style = ttk.Style()
style.configure('Custom.TButton',
                background='#000000',
                borderwidth=6,
                focuscolor='#f0687c',
                relief=tk.SOLID,
                padding=10,
                bordercolor='black',
                borderradius=50,
                font=('Helvetica', 12))

def wczytaj_obraz():
    filepath = filedialog.askopenfilename(filetypes=[("Obrazy", "*.jpg;*.jpeg;*.png")])

    if filepath:
        image = PIL.Image.open(filepath)
        width, height = image.size
        aspect_ratio = width / height

        label_width = frame1.winfo_width()
        label_height = frame1.winfo_height()

        if label_width / label_height > aspect_ratio:
            new_width = int(label_height * aspect_ratio)
            new_height = label_height
        else:
            new_width = label_width
            new_height = int(label_width / aspect_ratio)

        image = image.resize((new_width, new_height), PIL.Image.LANCZOS)


        image_tk = PIL.ImageTk.PhotoImage(image)


        frame1.configure(image=image_tk)
        frame1.image = image_tk
        frame1.configure(bg="#b4bbbf")

        # frame2.configure(image=image_tk)
        # frame2.image = image_tk
        # frame2.configure(bg="#b4bbbf")
        # frame3.configure(image=image_tk)
        # frame3.image = image_tk
        # frame3.configure(bg="#b4bbbf")
        # frame4.configure(image=image_tk)
        # frame4.image = image_tk
        # frame4.configure(bg="#b4bbbf")

def segmentuj():
    obraz = frame1.image
    obraz_pil = ImageTk.getimage(obraz)  # Konwersja do formatu PIL Image
    xd = np.array(obraz_pil)

    gray_img = cv2.cvtColor(xd, cv2.COLOR_BGR2GRAY)



    ret, bw = cv2.threshold(gray_img, int(slider.get() * 255), 255, cv2.THRESH_BINARY)

    # Konwersja z obiektu typu numpy array do PIL Image
    bw_img = PIL.Image.fromarray(bw)
    # Konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
    bw_img = ImageTk.PhotoImage(bw_img)
    # Wyświetlanie zbinaryzowanego obrazu
    frame2.configure(image=bw_img)
    frame2.image = bw_img
    frame2.configure(bg="#b4bbbf")

    # Tworzenie maski trzeciego obrazu
    mask = cv2.inRange(bw, 0, 50)

    # Zastosowanie maski na trzecim obrazie
    masked_img = apply_mask(xd, mask)

    # Konwersja obrazu do formatu RGB
    masked_img_rgb = cv2.cvtColor(masked_img, cv2.COLOR_BGR2RGB)

    # Tworzenie obiektu PIL Image
    masked_img_pil = PIL.Image.fromarray(masked_img_rgb)

    # Konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
    masked_img_tk = ImageTk.PhotoImage(masked_img_pil)

    # Wyświetlanie segmentowanego obrazu
    frame3.configure(image=masked_img_tk)
    frame3.image = masked_img_tk
    frame3.configure(bg="#b4bbbf")

def apply_mask(image, mask, mask_color=[255,255,255]):
    # Sprawdzenie rozmiarów obrazu i maski
    if image.shape[:2] != mask.shape:
        raise ValueError("Rozmiary obrazu i maski są niezgodne")

    # Kopiowanie obrazu
    masked_image = np.copy(image)

    # Przygotowanie koloru maski do pasującego rozmiaru obrazu
    mask_color = np.array(mask_color)
    mask_color = np.resize(mask_color, image.shape)

    # Nałożenie maski na obraz oryginalny
    masked_image[mask > 0] = mask_color[mask > 0]

    return masked_image

def update_threshold(value):
    slider = float(value)
    segmentuj()

def change_language():
    translations = {
        "Wczytaj obraz": "Load Image",
        "Segmentuj": "Segment",
        "Zapisz obraz": "Save Image",
        "Zmień język": "Change Language",
        "Segmentacja teksturowa": "Texture Segmentation"
    }

    reverse_translations = {v: k for k, v in translations.items()}

    wczytaj_text = button1['text']
    segmentuj_text = button2['text']
    zapisz_text = button3['text']
    zmien_text = button4['text']
    title_text = title_label['text']

    if wczytaj_text in translations.values():
        button1.configure(text=reverse_translations[wczytaj_text])
        button2.configure(text=reverse_translations[segmentuj_text])
        button3.configure(text=reverse_translations[zapisz_text])
        button4.configure(text=reverse_translations[zmien_text])
        title_label.configure(text=reverse_translations[title_text])
    else:
        button1.configure(text=translations[wczytaj_text])
        button2.configure(text=translations[segmentuj_text])
        button3.configure(text=translations[zapisz_text])
        button4.configure(text=translations[zmien_text])
        title_label.configure(text=translations[title_text])



title_label = tk.Label(root, text="Segmentacja teksturowa", font=("Helvetica", 24),bg="#b4bbbf", fg="black")
title_label.pack(pady=20)

label = tk.Label(root, width=30, height=100, bg="#b4bbbf", anchor='e')
label.pack(fill='y', side='left')

#button = tk.Button(label, text="Wczytaj obraz", width=20, font=('Helvetica', 12),bg="white",pady=8)
button1 = ttk.Button(label, text="Wczytaj obraz", width=20,  style='Custom.TButton', command=wczytaj_obraz)
button1.pack(padx=30, pady=30)
button2 = ttk.Button(label, text="Segmentuj", width=20,  style='Custom.TButton',command=segmentuj)
button2.pack(padx=30, pady=30)
button3 = ttk.Button(label, text="Zapisz obraz", width=20,  style='Custom.TButton')
button3.pack(padx=30, pady=30)
button4 = ttk.Button(label, text="Zmień język", width=20,  style='Custom.TButton',command=change_language)
button4.pack(padx=30, pady=30)

slider = tk.Scale(label, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL,length=200,command=update_threshold)
slider.set(0.5)
slider.pack(pady=10)

label_img = tk.Label(root, width= 100, height=100, bg="white")
label_img.pack(fill='x', padx=100, pady=50)

frame1_container = tk.Frame(label_img, bg="#b4bbbf", padx=20, pady=20)
frame1_container.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)


frame2_container = tk.Frame(label_img, bg="#b4bbbf", padx=20, pady=20)
frame2_container.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)

frame3_container = tk.Frame(label_img, bg="#b4bbbf", padx=20, pady=20)
frame3_container.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5)

frame4_container = tk.Frame(label_img, bg="#b4bbbf", padx=20, pady=20)
frame4_container.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)

frame1 = tk.Label(frame1_container)
frame1.pack(fill='both', expand=True)

frame2 = tk.Label(frame2_container)
frame2.pack(fill='both', expand=True)

frame3 = tk.Label(frame3_container)
frame3.pack(fill='both', expand=True)

frame4 = tk.Label(frame4_container)
frame4.pack(fill='both', expand=True)


root.mainloop()
