from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import subprocess
import os

class CrackDetectionApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Button for Crack Detection Image
        self.button_image = Button(text='Crack Detection Image')
        self.button_image.bind(on_press=self.detect_crack_image)
        self.layout.add_widget(self.button_image)
        
        # Button for Crack Detection Video
        self.button_video = Button(text='Crack Detection Video')
        self.button_video.bind(on_press=self.detect_crack_video)
        self.layout.add_widget(self.button_video)
        
        return self.layout
    
    def detect_crack_image(self, instance):
        # Get the absolute path to the image_crack_detection.py file
        script_path = os.path.abspath('image_crack_detection.py')
        # Call the image crack detection script using subprocess
        subprocess.run(['python', script_path])
    
    def detect_crack_video(self, instance):
        # Get the absolute path to the video_crack_detection.py file
        script_path = os.path.abspath('video_crack_detection.py')
        # Call the video crack detection script using subprocess
        subprocess.run(['python', script_path])

if __name__ == '__main__':
    CrackDetectionApp().run()
