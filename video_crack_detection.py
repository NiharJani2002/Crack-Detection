import tkinter as tk
from tkinter import filedialog
import numpy as np
from skimage import color, filters, feature, io
from skimage.metrics import structural_similarity as ssim

class CrackDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crack Detection App")
        self.video_path = None

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.file_label = tk.Label(self.main_frame, text="Selected Video:")
        self.file_label.pack()

        self.select_button = tk.Button(self.main_frame, text="Select Video", command=self.select_video)
        self.select_button.pack()

        self.detect_button = tk.Button(self.main_frame, text="Detect Cracks", command=self.detect_cracks)
        self.detect_button.pack()

        self.output_label = tk.Label(self.main_frame, text="")
        self.output_label.pack()

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if self.video_path:
            self.file_label.config(text=f"Selected Video: {self.video_path}")
        else:
            self.file_label.config(text="No video selected.")

    def detect_cracks(self):
        if self.video_path:
            self.detect_cracks_in_video(self.video_path)
            self.output_label.config(text="Crack detection completed. Output saved as 'output_crack_detection.mp4'")
        else:
            self.output_label.config(text="Please select a valid video file.")

    def detect_cracks_in_video(self, video_path):
        def gaussian_kernel(size, sigma=1):
            size = int(size) // 2
            x, y = np.mgrid[-size:size+1, -size:size+1]
            normal = 1 / (2.0 * np.pi * sigma**2)
            g = np.exp(-((x**2 + y**2) / (2.0 * sigma**2))) * normal
            return g

        def non_max_suppression(img, D):
            return filters.non_maximum_suppression(img, D)

        def hysteresis(img, low_threshold=0.05, high_threshold=0.09):
            return filters.apply_hysteresis_threshold(img, low_threshold, high_threshold)

        video_reader = io.get_reader(video_path)
        fps = video_reader.get_meta_data()['fps']

        output_video_path = 'output_crack_detection.mp4'
        video_writer = io.get_writer(output_video_path, fps=fps)

        prev_frame = None
        frame_counter = 0
        non_repetitive_frame_counter = 0

        for frame in video_reader:
            gray_frame = color.rgb2gray(frame)
            edges = filters.sobel(gray_frame)
            edges_after_suppression = non_max_suppression(edges, angle=np.arctan2(edges, edges))
            edges_after_threshold = hysteresis(edges_after_suppression)

            if prev_frame is not None:
                ssim_index = ssim(edges_after_threshold, prev_frame)
                if ssim_index > 0.84:
                    continue

            frame_counter += 1
            non_repetitive_frame_counter += 1

            side_by_side_frames = np.hstack((frame, np.stack((edges_after_threshold,) * 3, axis=-1)))

            video_writer.append_data(edges_after_threshold)

            prev_frame = edges_after_threshold

        video_reader.close()
        video_writer.close()

        print("Total frames in the original video:", frame_counter)
        print("Total non-repetitive frames:", non_repetitive_frame_counter)

if __name__ == '__main__':
    root = tk.Tk()
    app = CrackDetectionApp(root)
    root.mainloop()
