import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

class CrackDetection:
    def rgb_to_grayscale(self, rgb_image):
        return np.dot(rgb_image[..., :3], [0.2989, 0.5870, 0.1140])

    def gaussian_kernel(self, size, sigma=1):
        size = int(size) // 2
        x, y = np.mgrid[-size:size+1, -size:size+1]
        normal = 1 / (2.0 * np.pi * sigma**2)
        g = np.exp(-((x**2 + y**2) / (2.0 * sigma**2))) * normal
        return g

    def sobel_filters(self, img):
        Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
        Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)

        Ix = ndimage.filters.convolve(img, Kx)
        Iy = ndimage.filters.convolve(img, Ky)

        G = np.hypot(Ix, Iy)
        G = G / G.max() * 255
        theta = np.arctan2(Iy, Ix)

        return G, theta

    def non_max_suppression(self, img, D):
        M, N = img.shape
        Z = np.zeros((M, N), dtype=np.int32)
        angle = D * 180. / np.pi
        angle[angle < 0] += 180

        for i in range(1, M - 1):
            for j in range(1, N - 1):
                try:
                    q = 255
                    r = 255

                    # Angle 0
                    if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                        q = img[i, j+1]
                        r = img[i, j-1]
                    # Angle 45
                    elif (22.5 <= angle[i, j] < 67.5):
                        q = img[i+1, j-1]
                        r = img[i-1, j+1]
                    # Angle 90
                    elif (67.5 <= angle[i, j] < 112.5):
                        q = img[i+1, j]
                        r = img[i-1, j]
                    # Angle 135
                    elif (112.5 <= angle[i, j] < 157.5):
                        q = img[i-1, j-1]
                        r = img[i+1, j+1]

                    if (img[i, j] >= q) and (img[i, j] >= r):
                        Z[i, j] = img[i, j]
                    else:
                        Z[i, j] = 0

                except IndexError as e:
                    pass

        return Z

    def threshold(self, img, lowThresholdRatio=0.05, highThresholdRatio=0.09):
        highThreshold = img.max() * highThresholdRatio
        lowThreshold = highThreshold * lowThresholdRatio

        M, N = img.shape
        res = np.zeros((M, N), dtype=np.int32)

        weak = np.int32(25)
        strong = np.int32(255)

        strong_i, strong_j = np.where(img >= highThreshold)
        zeros_i, zeros_j = np.where(img < lowThreshold)

        weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

        res[strong_i, strong_j] = strong
        res[weak_i, weak_j] = weak

        return res, weak, strong

    def hysteresis(self, img, weak, strong=255):
        M, N = img.shape
        for i in range(1, M-1):
            for j in range(1, N-1):
                if (img[i, j] == weak):
                    try:
                        if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                            or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                            or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                            img[i, j] = strong
                        else:
                            img[i, j] = 0
                    except IndexError as e:
                        pass
        return img

    def show_images(self, images):
        root = tk.Tk()
        root.title("Crack Detection")

        for i, (title, img) in enumerate(images):
            image_pil = Image.fromarray(img)
            photo = ImageTk.PhotoImage(image_pil)

            label = tk.Label(root, image=photo)
            label.image = photo
            label.grid(row=0, column=i)

            label_title = tk.Label(root, text=title)
            label_title.grid(row=1, column=i)

        root.mainloop()

    def detect_cracks_on_image(self):
        # Use file dialog to select an image
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        root.destroy()  # Close the hidden main window

        # Check if a file was selected
        if not file_path:
            print("No image selected. Exiting...")
            return

        # Load the RGB image
        rgb_image = plt.imread(file_path)

        # Convert the RGB image to grayscale
        grayscale_image = self.rgb_to_grayscale(rgb_image)

        # Step 1: Noise Reduction
        kernel_size = 5  # You can change this to your desired kernel size
        sigma = 1        # You can change this to your desired sigma value
        gaussian_kernel_matrix = self.gaussian_kernel(kernel_size, sigma)
        filtered_image = np.zeros_like(grayscale_image)

        # Perform the convolution operation
        for i in range(grayscale_image.shape[0] - kernel_size + 1):
            for j in range(grayscale_image.shape[1] - kernel_size + 1):
                region = grayscale_image[i:i+kernel_size, j:j+kernel_size]
                filtered_image[i, j] = np.sum(region * gaussian_kernel_matrix)

        # Step 2: Gradient Calculation
        G, theta = self.sobel_filters(filtered_image)

        # Step 3: Non-Max Suppression
        suppressed_image = self.non_max_suppression(G, theta)

        # Step 4: Threshold
        thresholded_image, weak, strong = self.threshold(suppressed_image)

        # Step 5: Edge Tracking By Hysteresis
        final_image = self.hysteresis(thresholded_image, weak)

        images = [
            ("Filtered Grayscale", filtered_image),
            ("Sobel Magnitude", G),
            ("Sobel Direction", theta),
            ("Non-Maximum Suppressed", suppressed_image),
            ("Thresholded Image", thresholded_image),
            ("Final Image", final_image)
        ]

        self.show_images(images)

if __name__ == "__main__":
    # Create an instance of the CrackDetection class
    app = CrackDetection()

    # Call the detect_cracks_on_image function
    app.detect_cracks_on_image()
