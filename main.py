import tkinter as tk
from tkinter import ttk, filedialog

import PIL
import cv2
import numpy
import numpy as np
from PIL import ImageTk, ImageOps
from PIL.Image import Image
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from skimage.filters import gabor, try_all_threshold

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

    # Zastosowanie binaryzacji z użyciem progu
    ret, bw = cv2.threshold(gray_img, int(0.5 * 255), 255, cv2.THRESH_BINARY)

    # Konwersja z obiektu typu numpy array do PIL Image
    bw_img = PIL.Image.fromarray(bw)
    # Konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
    bw_img = ImageTk.PhotoImage(bw_img)
    # Wyświetlanie zbinaryzowanego obrazu
    frame2.configure(image=bw_img)
    frame2.image = bw_img

    # Tworzenie maski trzeciego obrazu
    # Tworzenie maski trzeciego obrazu
    mask = cv2.inRange(bw, 0, 50)

    # Zastosowanie maski na trzecim obrazie
    masked_img = apply_mask(xd, mask)

    # Konwersja obrazu do formatu RGB
    masked_img_rgb = cv2.cvtColor(masked_img, cv2.COLOR_BGR2RGB)

    # Tworzenie obiektu PIL Image
    masked_img_pil = Image.fromarray(masked_img_rgb)

    # Konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
    masked_img_tk = ImageTk.PhotoImage(masked_img_pil)

    # Wyświetlanie segmentowanego obrazu
    frame3.configure(image=masked_img_tk)
    frame3.image = masked_img_tk







title_label = tk.Label(root, text="Segmentacja teksturowa", font=("Helvetica", 24),bg="#b4bbbf", fg="black")
title_label.pack(pady=20)

label = tk.Label(root, width=30, height=100, bg="#b4bbbf", anchor='e')
label.pack(fill='y', side='left')

#button = tk.Button(label, text="Wczytaj obraz", width=20, font=('Helvetica', 12),bg="white",pady=8)
button = ttk.Button(label, text="Wczytaj obraz", width=20,  style='Custom.TButton', command=wczytaj_obraz)
button.pack(padx=30, pady=30)
button = ttk.Button(label, text="Segmentuj", width=20,  style='Custom.TButton',command=segmentuj)
button.pack(padx=30, pady=30)
button = ttk.Button(label, text="Zapisz obraz", width=20,  style='Custom.TButton')
button.pack(padx=30, pady=30)
button = ttk.Button(label, text="Zmień język", width=20,  style='Custom.TButton')
button.pack(padx=30, pady=30)
button = ttk.Button(label, text="Jebać disa", width=20,  style='Custom.TButton')
button.pack(padx=30, pady=30)

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
