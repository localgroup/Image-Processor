import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
from scipy import stats
import imageio.v2 as imageio


class ImageProcessing:
    def __init__(self):
        self.file_path = None

    def open_file(self):
        """
        Opens the file-dialog.
        :return:
        """
        root = tk.Tk()
        root.withdraw()

        self.file_path = filedialog.askopenfilename()  # Uses tkinter filedialog to open a window.
        if not self.file_path:
            print("No file selected.")
            return None
        if not os.path.exists(self.file_path):
            print(f"The file {self.file_path} does not exist.")
            return None
        print(f"The file {self.file_path} exists.")
        return self.file_path

    def top_n_colors(self, img, n):
        """
        Processes the image to determine the top ten colors.
        :param img:
        :param n:
        :return:
        """
        # Reshapes the numpy array
        pixels = img.reshape(-1, img.shape[-1])  # img.shape[-1] retrieves the size of the last dimension of the
        # img array, which corresponds to the number of color channels in each pixel!

        unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)  # Returns unique colors and their counts.
        top_indices = np.argpartition(a=counts, kth=-n)[-n:]  # Sorts the array counts by -n. Then slice the array.

        top_n_colors = unique_colors[top_indices]  # Returns the top n colors
        top_n_counts = counts[top_indices]  # Returns their top n counts

        most_common_color = stats.mode(pixels, axis=0)  # Gives the modal value of the pixels.
        print(f"The most common colors are: {list(most_common_color[0])}; not rgb value.")  # The colors returned are in
        # not in rgb values, but rather their individual appearance in the picture. Refer to the docs...

        return top_n_colors, top_n_counts

    def detect_color(self, file_location):
        """
        Detects the colors
        :param file_location:
        :return:
        """
        if not file_location:
            print("No file selected.")
            return

        if not os.path.exists(file_location):
            print(f"The file {file_location} does not exist.")
            return

        img = imageio.imread(file_location)  # Return a numpy array of the image!
        top_colors, top_counts = self.top_n_colors(img, 20)  # Change the value of n to load more colors! Takes more
        # time to process the image.
        rgb_values = []
        for color in top_colors:
            for _ in color:
                rgb_val = color[0], color[1], color[2]  # Creates a tuple for the rgb values.
                rgb_values.append(rgb_val)
                break
        return rgb_values


processor = ImageProcessing()

if __name__ == "__main__":
    file_path = processor.open_file()
    if file_path:
        processor.detect_color(file_path)
