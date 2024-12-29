# And may you never let it outshine your own. Love, Sean.

import os
import time
import tkinter as tk
from PIL import Image, ImageTk

class GifDisplayApp:
    def __init__(self, root, gif_folder_1, gif_folder_2, image_folder_1, image_folder_2, signal_file):
        self.root = root
        self.gif_folder_1 = gif_folder_1
        self.gif_folder_2 = gif_folder_2
        self.image_folder_1 = image_folder_1
        self.image_folder_2 = image_folder_2
        self.signal_file = signal_file

        self.frames_1 = []
        self.frames_2 = []
        self.current_frame_1 = 0
        self.current_frame_2 = 0
        self.latest_gif_path_1 = None
        self.latest_gif_path_2 = None
        self.last_signal_check = 0
        self.signal_last_modified = 0
        self.last_image_1 = "Unknown"
        self.last_image_2 = "Unknown"

        self.root.attributes("-fullscreen", True)
        self.root.config(bg="black")

        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        self.frame_1 = tk.Frame(self.main_frame, bg="black", width=400)
        self.frame_1.pack(side="left", fill="both", expand=True, padx=0)

        self.title_1 = tk.Label(self.frame_1, text="Aurora Borealis (Northern Hemisphere)",
                                font=("Helvetica", 12, "bold"), fg="white", bg="black")
        self.title_1.pack(anchor="center", pady=10)

        self.label_1 = tk.Label(self.frame_1, bg="black")
        self.label_1.pack(fill="both", expand=True)

        self.last_updated_1 = tk.Label(self.frame_1, text=f"Latest Forecast: {self.last_image_1[:-4]} UTC",
                                       font=("Helvetica", 10), fg="white", bg="black")
        self.last_updated_1.pack(anchor="center", pady=5)

        self.frame_2 = tk.Frame(self.main_frame, bg="black", width=400)
        self.frame_2.pack(side="right", fill="both", expand=True, padx=0)

        self.title_2 = tk.Label(self.frame_2, text="Aurora Australis (Southern Hemisphere)",
                                font=("Helvetica", 12, "bold"), fg="white", bg="black")
        self.title_2.pack(anchor="center", pady=10)

        self.label_2 = tk.Label(self.frame_2, bg="black")
        self.label_2.pack(fill="both", expand=True)

        self.last_updated_2 = tk.Label(self.frame_2, text=f"Latest Forecast: {self.last_image_2[:-4]} UTC",
                                       font=("Helvetica", 10), fg="white", bg="black")
        self.last_updated_2.pack(anchor="center", pady=5)

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

    def check_signal_file(self):
        """Check if the signal file has been updated."""
        try:
            modified_time = os.path.getmtime(self.signal_file)
            if modified_time != self.signal_last_modified:
                self.signal_last_modified = modified_time
                print("Signal file updated. Reloading GIFs...")
                self.reload_gifs()
        except FileNotFoundError:
            print("Signal file not found.")

    def reload_gifs(self):
        """Terminate current GIFs and reload them."""
        self.frames_1 = []
        self.frames_2 = []
        self.current_frame_1 = 0
        self.current_frame_2 = 0
        self.latest_gif_path_1 = None
        self.latest_gif_path_2 = None
        self.last_image_1 = "Unknown"
        self.last_image_2 = "Unknown"

        self.check_for_new_gif()

    def check_for_new_gif(self):
        for i, (gif_folder, frames, latest_path, last_image_label, image_folder) in enumerate([
            (self.gif_folder_1, self.frames_1, self.latest_gif_path_1, self.last_updated_1, self.image_folder_1),
            (self.gif_folder_2, self.frames_2, self.latest_gif_path_2, self.last_updated_2, self.image_folder_2)
        ]):
            # Check the most recent GIF
            gifs = [f for f in os.listdir(gif_folder) if f.endswith(".gif")]
            if gifs:
                newest_gif_path = max(
                    (os.path.join(gif_folder, f) for f in gifs),
                    key=os.path.getmtime,
                )
                if newest_gif_path != latest_path:
                    print(f"New GIF detected in folder {i + 1}: {newest_gif_path}")
                    frames[:] = self.load_frames(newest_gif_path)
                    if i == 0:
                        self.latest_gif_path_1 = newest_gif_path
                    else:
                        self.latest_gif_path_2 = newest_gif_path

            # Check the most recent image
            images = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
            if images:
                newest_image_name = max(
                    images,
                    key=lambda f: os.path.getmtime(os.path.join(image_folder, f)),
                )
                print(f"Last updated image in folder {i + 1}: {newest_image_name}")
                last_image_label.config(text=f"Latest Forecast: {newest_image_name[:-4]} UTC")

    def update_gifs(self):
        # Check the signal file for updates periodically
        if time.time() - self.last_signal_check > 5:  # Check every 5 seconds
            self.check_signal_file()
            self.last_signal_check = time.time()

        if self.frames_1:
            self.label_1.config(image=self.frames_1[self.current_frame_1])
            self.current_frame_1 = (self.current_frame_1 + 1) % len(self.frames_1)

        if self.frames_2:
            self.label_2.config(image=self.frames_2[self.current_frame_2])
            self.current_frame_2 = (self.current_frame_2 + 1) % len(self.frames_2)

        self.root.after(115, self.update_gifs)


def run_display_app(gif_folder_1, gif_folder_2, image_folder_1, image_folder_2, signal_file):
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.config(bg="black")

    app = GifDisplayApp(root, gif_folder_1, gif_folder_2, image_folder_1, image_folder_2, signal_file)

    root.mainloop()


if __name__ == "__main__":
    run_display_app(
        "/home/wskwok1999/Documents/Python_Scripts/aurora_north_gif_display",
        "/home/wskwok1999/Documents/Python_Scripts/aurora_south_gif_display",
        "/home/wskwok1999/Documents/Python_Scripts/aurora_north_images",
        "/home/wskwok1999/Documents/Python_Scripts/aurora_south_images",
        "/home/wskwok1999/Documents/Python_Scripts/signal.txt"
    )
