import os
import shutil

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from dotenv import load_dotenv

load_dotenv()

favorite_folder = os.getenv("FAVORITE_FOLDER")


image_files = []
current_index = 0  # Index of the current image being displayed
folder_path = ""

scale_factor = 1.0
original_image = None
canvas_image = None

drag_data = {"x": 0, "y": 0, "item": None}


root = tk.Tk()
root.title("Image Viewer")


canvas = tk.Canvas(root, width=root.winfo_screenwidth(),
                   height=root.winfo_screenheight())
canvas.pack()

open_button = tk.Button(root, text="Open Folder", command=open_folder)
open_button.place(relx=0.0, rely=0.0, anchor='nw')

root.geometry("854x480")

root.bind("<Right>", next_image)
root.bind("r", next_image)

root.bind("<Left>", previous_image)
root.bind("e", previous_image)

root.bind("<MouseWheel>", zoom)

root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", do_drag)
root.bind("<ButtonRelease-1>", stop_drag)

root.bind('f', favorite_image)

root.mainloop()
