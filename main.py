import tkinter as tk
from tkinter import filedialog
from skimage.filters import threshold_otsu
import numpy as np
from PIL import ImageTk, Image
import cv2


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Segmentacja tekstury")
        self.img_path = ""
        self.img = None
        self.bw_img = None
        self.segmented_img = None
        self.threshold = 0.5

        # Ustawienie tła na czarne
        self.master.configure(bg="black")

        # Tytuł
        self.title_label = tk.Label(
            self.master, text="Segmentacja tekstury", bg="black", fg="white", font=("Arial", 16, "bold")
        )
        self.title_label.pack(padx=10, pady=10)

        # Ramka dla przycisku wyboru pliku
        self.select_frame = tk.Frame(self.master, bg="black")
        self.select_frame.pack(anchor="nw", padx=10, pady=10)

        # Przycisk do wyboru pliku
        self.select_button = tk.Button(
            self.select_frame, text="Wybierz obraz", command=self.select_image
        )
        self.select_button.pack(side="left")

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

        # Ramka dla obrazów
        self.image_frame = tk.Frame(self.master, bg="black")
        self.image_frame.pack()

        # Etykieta do wyświetlenia oryginalnego obrazu
        self.orig_label = tk.Label(self.image_frame, bg="black")
        self.orig_label.pack(side="left", padx=10)

        # Etykieta do wyświetlenia zbinaryzowanego obrazu
        self.bw_label = tk.Label(self.image_frame, bg="black")
        self.bw_label.pack(side="left", padx=10)

        # Etykieta do wyświetlenia segmentowanego obrazu
        self.segmented_label = tk.Label(self.master, bg="black")
        self.segmented_label.pack(padx=10, pady=10)

        # Przycisk do zapisu segmentowanego obrazu
        self.save_segmented_button = tk.Button(
            self.master, text="Zapisz segmentowany obraz", command=self.save_segmented_image
        )
        self.save_segmented_button.pack(padx=10, pady=5)

        # Przycisk do zapisu obrazu z maską
        self.save_masked_button = tk.Button(
            self.master, text="Zapisz obraz z maską", command=self.save_masked_image
        )
        self.save_masked_button.pack(padx=10, pady=5)

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

            # Konwersja obrazu do skali szarości
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Zastosowanie binaryzacji z użyciem progu
            ret, bw = cv2.threshold(
                gray_img, int(self.threshold * 255), 255, cv2.THRESH_BINARY
            )

            # Konwersja z obiektu typu numpy array do PIL Image
            self.bw_img = Image.fromarray(bw)
            # Konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
            self.bw_img = ImageTk.PhotoImage(self.bw_img)
            # Wyświetlanie zbinaryzowanego obrazu
            self.bw_label.configure(image=self.bw_img)
            self.bw_label.image = self.bw_img

            # Tworzenie maski trzeciego obrazu
            mask = cv2.inRange(bw, 0, 50)

            # Zastosowanie maski na trzecim obrazie
            masked_img = self.apply_mask(img, mask)

            # Konwersja obrazu do formatu RGB
            masked_img_rgb = cv2.cvtColor(masked_img, cv2.COLOR_BGR2RGB)

            # Tworzenie obiektu PIL Image
            masked_img_pil = Image.fromarray(masked_img_rgb)

            # Konwersja PIL Image do formatu, który może być wyświetlony w Tkinter
            masked_img_tk = ImageTk.PhotoImage(masked_img_pil)

            # Wyświetlanie segmentowanego obrazu
            self.segmented_label.configure(image=masked_img_tk)
            self.segmented_label.image = masked_img_tk

    def apply_mask(self, image, mask):
        # Utworzenie obrazu o rozmiarze maski
        mask_image = np.zeros_like(image)

        # Ustawienie koloru maski na żółty (255, 255, 0)
        mask_color = (255, 255, 0)

        # Kopiowanie wartości pikseli z obrazu oryginalnego na obraz maski tylko dla wartości niezerowych w masce
        mask_image[mask > 0] = mask_color

        # Dodanie maski do obrazu oryginalnego
        masked_image = cv2.addWeighted(image, 0.7, mask_image, 0.3, 0)

        return masked_image

    def update_threshold(self, value):
        self.threshold = float(value)
        # Segmentacja obrazu po zmianie progu
        self.segment_image()

    def save_segmented_image(self):
        if self.segmented_img:
            # Wybieranie miejsca zapisu segmentowanego obrazu
            save_path = filedialog.asksaveasfilename(
                title="Zapisz segmentowany obraz",
                defaultextension=".png",
                filetypes=(("PNG files", "*.png"), ("All files", "*.*")),
            )
            if save_path:
                # Konwersja PhotoImage do Image
                image_pil = self.segmented_img
                image_pil = image_pil._PhotoImage__photo
                image_pil = ImageTk.getimage(image_pil)

                # Zapisywanie segmentowanego obrazu
                image_pil.save(save_path)

    def save_masked_image(self):
        if self.img_path:
            # Wczytywanie obrazu jako obiekt typu numpy array
            img = cv2.imread(self.img_path)

            # Wykrycie pierwszej tekstury
            texture1_mask = cv2.inRange(img, (0, 0, 0), (50, 50, 50))

            # Wykrycie drugiej tekstury
            texture2_mask = cv2.inRange(img, (200, 200, 200), (255, 255, 255))

            # Utworzenie macierzy etykiet
            label_matrix = np.zeros_like(texture1_mask)
            label_matrix[texture1_mask == 255] = 1
            label_matrix[texture2_mask == 255] = 2

            # Przypisanie kolorów do etykiet
            label_colored = np.zeros_like(img)
            label_colored[label_matrix == 1] = [0, 255, 255]  # Kolor żółty
            label_colored[label_matrix == 2] = [255, 0, 0]  # Kolor niebieski

            # Nałożenie kolorów na obrazy tekstur
            texture1_colored = cv2.addWeighted(img, 0.5, label_colored, 0.5, 0)
            texture2_colored = cv2.addWeighted(img, 0.5, label_colored, 0.5, 0)

            result = cv2.add(texture1_colored, texture2_colored)
            result2 = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

            # Konwersja obrazu do formatu PIL Image
            result_pil = Image.fromarray(result2)

            # Wybieranie miejsca zapisu obrazu z maską
            save_path = filedialog.asksaveasfilename(
                title="Zapisz obraz z maską",
                defaultextension=".png",
                filetypes=(("PNG files", "*.png"), ("All files", "*.*")),
            )
            if save_path:
                # Zapisywanie obrazu z maską
                result_pil.save(save_path)

root = tk.Tk()
app = App(root)
root.mainloop()
