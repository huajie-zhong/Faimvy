import os
import shutil
import send2trash

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD
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


def open_folder():
    global image_files, folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        image_files = [f for f in os.listdir(
            folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            messagebox.showinfo(
                "No Image Files", "No image files found in the selected folder.")
        else:
            show_image(current_index)
    else:
        print("No folder selected.")


def open_image(image_path=None):
    global image_files, current_index, folder_path
    if image_path is None:
        image_path = filedialog.askopenfilename(
            filetypes=[('Image Files', '.jpg .jpeg .png')])
    if image_path:
        folder_path = os.path.dirname(image_path)
        image_files = [f for f in os.listdir(
            folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            messagebox.showinfo(
                "No Image Files", "No image files found in the selected folder.")
        else:
            current_index = image_files.index(os.path.basename(image_path))
            show_image(current_index)
    else:
        print("No image selected.")


def on_drop(event):
    image_paths = event.data.strip('{}').split()
    image_path = ' '.join(image_paths)
    open_image(image_path)


def show_image(index):
    global scale_factor, original_image, canvas_image, tk_image
    image_path = os.path.join(folder_path, image_files[index])
    image = Image.open(image_path)
    # Resize the image to fit the window
    max_size = (root.winfo_width(), root.winfo_height())
    image.thumbnail(max_size, Image.LANCZOS)
    # Store the original image
    original_image = image.copy()
    # Apply the scale factor
    new_size = (int(image.width * scale_factor),
                int(image.height * scale_factor))
    image = image.resize(new_size, Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(image)

    # Update the canvas with the new image
    canvas.delete("all")
    canvas_image = canvas.create_image(
        root.winfo_width() // 2, root.winfo_height() // 2, image=tk_image)


def next_image(event=None):
    global current_index, scale_factor
    current_index += 1
    if current_index >= len(image_files):
        current_index = 0
    scale_factor = 1.0
    show_image(current_index)


def previous_image(event=None):
    global current_index, scale_factor
    current_index -= 1
    if current_index < 0:
        current_index = len(image_files) - 1
    scale_factor = 1.0
    show_image(current_index)


def zoom(event):
    global scale_factor, original_image, canvas_image, tk_image

    # Increase or decrease the scale factor depending on the direction of the mouse scroll
    if event.delta > 0:
        # Don't allow zooming in beyond a certain scale factor
        if scale_factor < 10.0:
            scale_factor *= 1.1
    else:
        # Don't allow zooming out beyond a certain scale factor
        if scale_factor > 0.1:
            scale_factor /= 1.1

    # Resize the original image
    new_size = (int(original_image.width * scale_factor),
                int(original_image.height * scale_factor))
    image = original_image.resize(new_size, Image.LANCZOS)

    # Get the current position of the image
    coords = canvas.coords(canvas_image)
    new_x = coords[0]
    new_y = coords[1]

    tk_image = ImageTk.PhotoImage(image)

    # Update the canvas with the new image
    canvas.delete("all")
    canvas_image = canvas.create_image(
        new_x, new_y, image=tk_image, anchor='center')


def start_drag(event):
    '''Begin drag of an object'''
    # record the item and its location
    drag_data["item"] = canvas_image
    drag_data["x"] = event.x
    drag_data["y"] = event.y


def stop_drag(event):
    '''End drag of an object'''
    # reset the drag information
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0


def do_drag(event):
    '''Handle dragging of an object'''
    # compute how much the mouse has moved
    delta_x = event.x - drag_data["x"]
    delta_y = event.y - drag_data["y"]
    # move the object the appropriate amount
    canvas.move(drag_data["item"], delta_x, delta_y)
    # record the new position
    drag_data["x"] = event.x
    drag_data["y"] = event.y


def favorite_image(event):
    global image_files, current_index, folder_path
    # Get the current image file
    image_file = image_files[current_index]
    # Construct the source and destination paths
    src_path = os.path.join(folder_path, image_file)
    dst_path = os.path.join(folder_path, favorite_folder, image_file)
    # Move the image file
    shutil.move(src_path, dst_path)
    # Update the image_files array
    image_files = [f for f in os.listdir(
        folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    # If the current index is not valid anymore, reset it to 0
    if current_index >= len(image_files):
        current_index = 0
    # Show the next image
    show_image(current_index)


def delete_image(event):
    global image_files, current_index, folder_path
    # Get the current image file
    image_file = image_files[current_index]
    # Construct the source and destination paths
    src_path = os.path.join(folder_path, image_file)
    # Move the image file
    send2trash(src_path)
    # Update the image_files array
    image_files = [f for f in os.listdir(
        folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    # If the current index is not valid anymore, reset it to 0
    if current_index >= len(image_files):
        current_index = 0
    # Show the next image
    show_image(current_index)


root = TkinterDnD.Tk()
root.title("Image Viewer")


button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, fill=tk.X)

open_button = tk.Button(button_frame, text="Open Folder", command=open_folder)
open_button.pack(side=tk.LEFT)
open_image_button = tk.Button(
    button_frame, text="Open Image", command=open_image)
open_image_button.pack(side=tk.LEFT)

canvas_height = root.winfo_screenheight() - button_frame.winfo_reqheight()
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=canvas_height)
canvas.pack(fill=tk.BOTH, expand=True)


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
root.bind('d', delete_image)

root.drop_target_register('DND_Files')
root.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
