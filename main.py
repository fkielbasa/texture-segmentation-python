import tkinter as tk
from tkinter import filedialog
from skimage.filters import threshold_otsu
from skimage.measure import label
import numpy
from PIL import ImageTk, Image
import cv2
from matplotlib import pyplot as plt
import numpy as np


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Segmentacja teksturowa")
        self.img_path = ""
        self.img = None
        self.bw_img = None
        self.segmented_img = None
        self.threshold = 0.5

        # Ustawienie tła na czarne
        self.master.configure(bg="black")

        # Ramka dla przycisku wyboru pliku
        self.select_frame = tk.Frame(self.master, bg="black")
        self.select_frame.pack(anchor="nw", padx=10, pady=10)

        # Przycisk do wyboru pliku
        self.select_button = tk.Button(
            self.select_frame, text="Wybierz obraz", command=self.select_image
        )
        self.select_button.pack(side="left")

        # Ramka dla obrazów
        self.image_frame = tk.Frame(self.master, bg="black")
        self.image_frame.pack()

        # Etykieta do wyświetlenia oryginalnego obrazu
        self.orig_label = tk.Label(self.image_frame, bg="black")
        self.orig_label.pack(side="left", padx=10)

        # Etykieta do wyświetlenia zbinaryzowanego obrazu
        self.bw_label = tk.Label(self.image_frame, bg="black")
        self.bw_label.pack(side="left", padx=10)

        # Suwak do ustawiania progu binaryzacji
        self.threshold_slider = tk.Scale(
            self.master,
            from_=0,
            to=1,
            length=200,
            resolution=0.01,
            command=self.update_threshold,
            orient="horizontal",
            bg="black",
            fg="white",
            highlightbackground="black",
            troughcolor="gray",
        )
        self.threshold_slider.set(self.threshold)
        self.threshold_slider.pack(anchor="n", padx=10, pady=10)

        # Etykieta dla suwaka
        self.threshold_label = tk.Label(
            self.master, text="Próg binaryzacji:", bg="black", fg="white"
        )
        self.threshold_label.pack(anchor="n", padx=10)

        # Etykieta do wyświetlenia segmentowanego obrazu
        self.segmented_label = tk.Label(self.master, bg="black")
        self.segmented_label.pack(padx=10, pady=10)

        # Minimalna wielkość okna
        self.master.minsize(width=800, height=400)

    def select_image(self):
        # Wybieranie pliku z obrazem
        self.img_path = filedialog.askopenfilename(title="Wybierz obraz")
        if self.img_path:
            # Ładowanie obrazu do PIL Image
            self.img = Image.open(self.img_path)
            # Konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
            self.img = ImageTk.PhotoImage(self.img)
            # Wyświetlanie oryginalnego obrazu
            self.orig_label.configure(image=self.img)
            self.orig_label.image = self.img
            # Segmentacja obrazu
            self.segment_image()

    def segment_image(self):
        if self.img_path:
            # Wczytywanie obrazu jako obiekt typu numpy array
            img = cv2.imread(self.img_path)

            # Zastosowanie binaryzacji z użyciem progu
            ret, bw1 = cv2.threshold(
                img, int(self.threshold * 255), 255, cv2.THRESH_BINARY
            )

            # Konwersja z obiektu typu numpy array do PIL Image
            self.bw_img = Image.fromarray(bw1)
            # Konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
            self.bw_img = ImageTk.PhotoImage(self.bw_img)
            # Wyświetlanie zbinaryzowanego obrazu
            self.bw_label.configure(image=self.bw_img)
            self.bw_label.image = self.bw_img

            # Wykrycie pierwszej tekstury
            texture1_mask = cv2.inRange(img, (0, 0, 0), (50, 50, 50))

            # Wykrycie drugiej tekstury
            texture2_mask = cv2.inRange(img, (200, 200, 200), (255, 255, 255))

            # Utworzenie macierzy etykiet
            label_matrix = np.zeros_like(texture1_mask)
            label_matrix[texture1_mask == 255] = 1
            label_matrix[texture2_mask == 255] = 2

            # Utworzenie dwóch oddzielnych obrazów dla każdej tekstury
            texture1 = cv2.bitwise_and(img, img, mask=texture1_mask)
            texture2 = cv2.bitwise_and(img, img, mask=texture2_mask)

            # Przypisanie kolorów do etykiet
            label_colored = np.zeros_like(img)
            label_colored[label_matrix == 1] = [0, 255, 255]  # Kolor żółty
            label_colored[label_matrix == 2] = [255, 0, 0]  # Kolor niebieski

            # Nałożenie kolorów na obrazy tekstur
            texture1_colored = cv2.addWeighted(texture1, 0.5, label_colored, 0.5, 0)
            texture2_colored = cv2.addWeighted(texture2, 0.5, label_colored, 0.5, 0)

            result = cv2.add(texture1_colored, texture2_colored)
            result2 = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            result_pil = Image.fromarray(result2)
            self.segmented_img = ImageTk.PhotoImage(result_pil)

            # Wyświetlanie segmentowanego obrazu
            self.segmented_label.configure(image=self.segmented_img)
            self.segmented_label.image = self.segmented_img

    def update_threshold(self, value):
        self.threshold = float(value)
        # Segmentacja obrazu po zmianie progu
        self.segment_image()


root = tk.Tk()
app = App(root)
root.mainloop()
