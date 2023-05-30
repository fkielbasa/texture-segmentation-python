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

        # przycisk do wyboru obrazka
        self.select_button = tk.Button(self.master, text="Wybierz obraz", command=self.select_image)
        self.select_button.pack()
        # przycisk do segmentacji obrazka
        self.segment_button = tk.Button(self.master, text="Segmentuj", command=self.segment_image)
        self.segment_button.pack()

        # etykieta do wyświetlenia oryginalnego obrazka
        self.orig_title = tk.Label(self.master, text="")
        self.orig_title.pack(side="left")
        self.orig_label = tk.Label(self.master,text="")
        self.orig_label.pack(side="left")


        # etykieta do wyświetlenia zbinaryzowanego obrazka
        self.bw_label = tk.Label(self.master)
        self.bw_label.pack(side="left")

        # etykieta do wyświetlenia segmentowanego obrazka
        self.segmented_label = tk.Label(self.master)
        self.segmented_label.pack(side="left")






    def select_image(self):
        # wybieranie pliku z obrazem
        self.img_path = filedialog.askopenfilename(title="Wybierz obraz")
        if self.img_path:
            # ładowanie obrazu do PIL Image
            self.img = Image.open(self.img_path)
            # konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
            self.img = ImageTk.PhotoImage(self.img)
            # wyświetlanie oryginalnego obrazu
            self.orig_label.config(image=self.img)

    def segment_image(self):
        if self.img_path:
            # wczytywanie obrazu jako obiekt typu numpy array
            img = cv2.imread(self.img_path)

            # zastosowanie binaryzacji z użyciem progu 0.5
            ret, bw1 = cv2.threshold(img, 0.5 * 255, 255, cv2.THRESH_BINARY)

            # konwersja z obiektu typu numpy array do PIL Image
            self.bw_img = Image.fromarray(bw1)

            # konwersja do grayscale
            bw_gray = self.bw_img.convert('L')

            # konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
            self.bw_img = ImageTk.PhotoImage(bw_gray)

            # wyświetlanie zbinaryzowanego obrazu
            self.bw_label.config(image=self.bw_img)



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
            label_colored[label_matrix == 1] = [0, 255, 255]  # kolor żółty
            label_colored[label_matrix == 2] = [255, 0, 0]  # kolor niebieski

            # Nałożenie kolorów na obrazy tekstur
            texture1_colored = cv2.addWeighted(texture1, 0.5, label_colored, 0.5, 0)
            texture2_colored = cv2.addWeighted(texture2, 0.5, label_colored, 0.5, 0)


            result = cv2.add(texture1_colored, texture2_colored)
            result2 = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            result_pil = Image.fromarray(result2)
            self.result_tk = ImageTk.PhotoImage(result_pil)

            self.segmented_label.config(image=self.result_tk)


root = tk.Tk()
app = App(root)
root.geometry("1920x1080")
root.mainloop()
