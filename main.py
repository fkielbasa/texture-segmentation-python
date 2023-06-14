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
original_image = None
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
        global original_image
        original_image = cv2.imread(filepath)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        image = PIL.Image.open(filepath)
        frame4.image = image
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


def segmentuj():
    obraz = frame1.image
    obraz_pil = ImageTk.getimage(obraz)
    first = np.array(obraz_pil)
    obraz = np.copy(original_image)  # Użyj oryginalnego wczytanego obrazu
    second = np.copy(obraz)
    gray_img = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)

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
    masked_img = apply_mask(first, mask)

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
    texture1_mask = cv2.inRange(second, (0, 0, 0), (50, 50, 50))
    texture2_mask = cv2.inRange(second, (200, 200, 200), (255, 255, 255))
    texture3_mask = cv2.inRange(second, (50, 50, 50), (255, 255, 255))
    texture4_mask = cv2.inRange(second, (50, 50, 50), (150, 150, 150))
    texture5_mask = cv2.inRange(second, (100, 100, 100), (200, 200, 200))
    texture6_mask = cv2.inRange(second, (150, 150, 150), (255, 255, 255))

    label_matrix = np.zeros_like(texture1_mask)
    label_matrix[texture1_mask == 255] = 1
    label_matrix[texture2_mask == 255] = 2
    label_matrix[texture3_mask == 255] = 3
    label_matrix[texture4_mask == 255] = 4
    label_matrix[texture5_mask == 255] = 5
    label_matrix[texture6_mask == 255] = 6

    texture1 = cv2.bitwise_and(second, second, mask=texture1_mask)
    texture2 = cv2.bitwise_and(second, second, mask=texture2_mask)
    texture3 = cv2.bitwise_and(second, second, mask=texture3_mask)
    texture4 = cv2.bitwise_and(second, second, mask=texture4_mask)
    texture5 = cv2.bitwise_and(second, second, mask=texture5_mask)
    texture6 = cv2.bitwise_and(second, second, mask=texture6_mask)

    label_colored = np.zeros_like(second)
    label_colored[label_matrix == 1] = [0, 255, 0]
    label_colored[label_matrix == 2] = [0, 0, 255]
    label_colored[label_matrix == 3] = [255, 0, 255]
    label_colored[label_matrix == 4] = [255, 0, 0]
    label_colored[label_matrix == 5] = [255, 255, 0]
    label_colored[label_matrix == 6] = [0, 255, 255]

    texture1_colored = cv2.addWeighted(texture1, 0.5, label_colored, 0.5, 0)
    texture2_colored = cv2.addWeighted(texture2, 0.5, label_colored, 0.5, 0)
    texture3_colored = cv2.addWeighted(texture3, 0.5, label_colored, 0.5, 0)
    texture4_colored = cv2.addWeighted(texture4, 0.5, label_colored, 0.5, 0)
    texture5_colored = cv2.addWeighted(texture5, 0.5, label_colored, 0.5, 0)
    texture6_colored = cv2.addWeighted(texture6, 0.5, label_colored, 0.5, 0)

    temp = cv2.add(texture1_colored, texture2_colored)
    temp = cv2.add(temp, texture3_colored)
    temp = cv2.add(temp, texture4_colored)
    temp = cv2.add(temp, texture5_colored)
    result = cv2.add(temp, texture6_colored)
    result_pil = PIL.Image.fromarray(result)
    if result_pil:
        width, height = result_pil.size
        aspect_ratio = width / height

        label_width = frame4.winfo_width()
        label_height = frame4.winfo_height()

        if label_width / label_height > aspect_ratio:
            new_width = int(label_height * aspect_ratio)
            new_height = label_height
        else:
            new_width = label_width
            new_height = int(label_width / aspect_ratio)

        result_pil = result_pil.resize((new_width, new_height), PIL.Image.LANCZOS)

        result_tk = ImageTk.PhotoImage(result_pil)
        frame4.configure(image=result_tk)
        frame4.image = result_tk
        frame4.configure(bg="#b4bbbf")


def apply_mask(image, mask, mask_color=[0,255,0]):
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

def save_image_1():
    obraz = frame3.image
    if obraz:
        save_path = filedialog.asksaveasfilename(
            title="Zapisz segmentowany obraz",
            defaultextension=".png",
            filetypes=(("PNG files", "*.png"), ("All files", "*.*")),
        )
        if save_path:
            # Konwersja PhotoImage do Image
            image_pil = obraz
            image_pil = image_pil._PhotoImage__photo
            image_pil = ImageTk.getimage(image_pil)

            # Zapisywanie segmentowanego obrazu
            image_pil.save(save_path)

def save_image_2():
    obraz = frame4.image
    if obraz:
        save_path = filedialog.asksaveasfilename(
            title="Zapisz segmentowany obraz",
            defaultextension=".png",
            filetypes=(("PNG files", "*.png"), ("All files", "*.*")),
        )
        if save_path:
            # Konwersja PhotoImage do Image
            image_pil = obraz
            image_pil = image_pil._PhotoImage__photo
            image_pil = ImageTk.getimage(image_pil)

            # Zapisywanie segmentowanego obrazu
            image_pil.save(save_path)

def change_language():
    translations = {
        "Wczytaj obraz": "Load Image",
        "Segmentuj": "Segment",
        "Zapisz obraz 1": "Save Image 1",
        "Zapisz obraz 2": "Save Image 2",
        "Zmień język": "Change Language",
        "Segmentacja teksturowa": "Texture Segmentation"
    }

    reverse_translations = {v: k for k, v in translations.items()}

    wczytaj_text = button1['text']
    segmentuj_text = button2['text']
    zapisz_text = button3['text']
    zapisz_text1 = button4['text']
    zmien_text = button5['text']
    title_text = title_label['text']

    if wczytaj_text in translations.values():
        button1.configure(text=reverse_translations[wczytaj_text])
        button2.configure(text=reverse_translations[segmentuj_text])
        button3.configure(text=reverse_translations[zapisz_text])
        button4.configure(text=reverse_translations[zapisz_text1])
        button5.configure(text=reverse_translations[zmien_text])
        title_label.configure(text=reverse_translations[title_text])
    else:
        button1.configure(text=translations[wczytaj_text])
        button2.configure(text=translations[segmentuj_text])
        button3.configure(text=translations[zapisz_text])
        button4.configure(text=translations[zapisz_text1])
        button5.configure(text=translations[zmien_text])
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
button3 = ttk.Button(label, text="Zapisz obraz 1", width=20,  style='Custom.TButton',command=save_image_1)
button3.pack(padx=30, pady=30)
button4 = ttk.Button(label, text="Zapisz obraz 2", width=20,  style='Custom.TButton',command=save_image_2)
button4.pack(padx=30, pady=30)
button5 = ttk.Button(label, text="Zmień język", width=20,  style='Custom.TButton',command=change_language)
button5.pack(padx=30, pady=30)

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
