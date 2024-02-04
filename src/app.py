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
