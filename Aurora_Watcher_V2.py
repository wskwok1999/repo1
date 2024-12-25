# And may you never let it outshine your own. Love, Sean.

import os
import time
import tkinter as tk
from PIL import Image, ImageTk

class GifDisplayApp:
    def __init__(self, root, gif_folder_1, gif_folder_2):
        self.root = root
        self.gif_folder_1 = gif_folder_1
        self.gif_folder_2 = gif_folder_2

        # Debug folder checks
        #print("GIF folder 1 exists:", os.path.exists(self.gif_folder_1))
        #print("GIF folder 2 exists:", os.path.exists(self.gif_folder_2))

        # Create UI
        self.label_1 = tk.Label(root)
        self.label_1.grid(row=0, column=0)
        self.label_2 = tk.Label(root)
        self.label_2.grid(row=0, column=1)

        self.frames_1 = []
        self.frames_2 = []
        self.current_frame_1 = 0
        self.current_frame_2 = 0
        self.latest_gif_path_1 = None
        self.latest_gif_path_2 = None

        self.check_interval = 30000  # Check every 5 seconds
        self.last_checked = 0

        self.root.attributes("-fullscreen",True)
        self.root.config(bg="black")

        self.update_gifs()

    def load_frames(self, gif_path):
        print(f"Loading frames from: {gif_path}")
        img = Image.open(gif_path)
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(img.copy()))
                img.seek(img.tell() + 1)
        except EOFError:
            print(f"Loaded {len(frames)} frames from {gif_path}")
        return frames

    def check_for_new_gif(self):
        for i, (folder, frames, latest_path) in enumerate([
            (self.gif_folder_1, self.frames_1, self.latest_gif_path_1),
            (self.gif_folder_2, self.frames_2, self.latest_gif_path_2)
        ]):
            gifs = [f for f in os.listdir(folder) if f.endswith(".gif")]
            if gifs:
                newest_gif_path = max(
                    (os.path.join(folder, f) for f in gifs),
                    key=os.path.getmtime,
                )
                if newest_gif_path != latest_path:
                    print(f"New GIF detected in folder {i + 1}: {newest_gif_path}")
                    if i == 0:
                        self.frames_1 = self.load_frames(newest_gif_path)
                        self.latest_gif_path_1 = newest_gif_path
                    else:
                        self.frames_2 = self.load_frames(newest_gif_path)
                        self.latest_gif_path_2 = newest_gif_path

    def update_gifs(self):
        if time.time() - self.last_checked > self.check_interval / 1000:
            self.check_for_new_gif()
            self.last_checked = time.time()

        if self.frames_1:
            self.label_1.config(image=self.frames_1[self.current_frame_1])
            self.current_frame_1 = (self.current_frame_1 + 1) % len(self.frames_1)

        if self.frames_2:
            self.label_2.config(image=self.frames_2[self.current_frame_2])
            self.current_frame_2 = (self.current_frame_2 + 1) % len(self.frames_2)

        self.root.after(115, self.update_gifs)

def run_display_app(gif_folder_1, gif_folder_2):
    root = tk.Tk()
    root.title("Aurora Borealis (Northern Hemisphere)                                  Aurora Australis (Southern Hemisphere)")
    root.geometry("800x400")
    root.attributes("-fullscreen",True)
    root.config(bg="black")

    app = GifDisplayApp(root, gif_folder_1, gif_folder_2)

    root.mainloop()

if __name__ == "__main__":
    run_display_app("/home/wskwok1999/Documents/Python_Scripts/aurora_north_gif_display","/home/wskwok1999/Documents/Python_Scripts/aurora_south_gif_display")
