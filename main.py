import tkinter as tk
from tkinter import ttk, filedialog

import PIL
import cv2
import numpy as np
from PIL import ImageTk
from PIL.Image import Image

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
    obraz1 = np.array(obraz)
    gray_img = cv2.cvtColor(obraz1, cv2.COLOR_BGR2GRAY)

    # Utworzenie filtrów Gabora o różnych kierunkach i częstotliwościach
    filtry_gabora = []
    for theta in np.arange(0, np.pi, np.pi / 4):
        for sigma in (1, 3):
            filtry_gabora.append(cv2.getGaborKernel((21, 21), sigma, theta, 10, 0.5, 0, ktype=cv2.CV_32F))

    # Konwolucja obrazu z filtrami Gabora
    wynik_konwolucji = np.zeros_like(gray_img)
    for filtr in filtry_gabora:
        filtr_img = cv2.filter2D(gray_img, cv2.CV_8UC3, filtr)
        wynik_konwolucji = np.maximum(wynik_konwolucji, filtr_img)

    # Przygotowanie obrazu dla algorytmu K-means
    dane_wejsciowe = np.float32(wynik_konwolucji.reshape(-1, 1))

    # Zastosowanie algorytmu K-means do segmentacji
    kmeans = cv2.KMeans(n_clusters=5)
    kmeans.fit(dane_wejsciowe)

    # Przypisanie etykiet do pikseli
    etykiety = kmeans.labels_
    obraz_segmentowany = etykiety.reshape(gray_img.shape)

    # Umożliwienie wyrównania histogramu dla lepszej wizualizacji
    obraz_wyrównany = cv2.equalizeHist(obraz_segmentowany)

    return obraz_wyrównany




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
