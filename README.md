# Faimvy
Fast image viewer

## Introduction

The Image Viewer allows users to view images, open folders, and pick a favorite folder for storing images. It also supports features such as zooming, dragging images, and managing favorite images.

## Requirements

- Python
- Tkinter
- Pillow (PIL)
- TkinterDnD

## Usage

1. **Open Folder**: Opens a folder containing images.
2. **Open Image**: Opens a specific image file.
3. **Pick Favorite Folder**: Sets a folder as the favorite destination for storing images.
4. **Navigation**:
   - Use **Right Arrow** or **'r'** key to view the next image.
   - Use **Left Arrow** or **'e'** key to view the previous image.
5. **Zooming**: Scroll the mouse wheel to zoom in or out on the image.
6. **Dragging**: Click and drag an image to move it within the window.
7. **Favorite Image**: Press **'f'** key to move the current image to the favorite folder.
8. **Delete Image**: Press **Shift + D** to delete the current image.
9. **Reading Metadata/EXIF Data**: Metadata/EXIF data is displayed alongside the image.
10. **Drag and Drop**: You can drag and drop image files directly onto the window to open them.

## Installation

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the script using `python app.py`.

## Configuration

The application saves the favorite folder selection in a file named `favorite_folder.pkl`.

## License

This project is licensed under the [GPL-3.0 license](LICENSE).

