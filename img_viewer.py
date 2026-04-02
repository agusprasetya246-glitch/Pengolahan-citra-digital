import FreeSimpleGUI as sg
import os.path
from PIL import Image, ImageOps
from processing_list import *

sg.theme("LightBlue2")

# Kolom Area No 1: Area open folder and select image
file_list_column = [
    [sg.Text("Open Image Folder :"),],
    [sg.In(size=(20, 1), enable_events=True, key="ImgFolder"),sg.FolderBrowse(),],        
    [sg.Text("Choose an image from list :"),],
    [sg.Listbox(values=[], enable_events=True, size=(18, 10), key="ImgList")],
]

# Kolom Area No 2: Area viewer image input
image_viewer_column = [
    [sg.Text("Image Input :")],
    [sg.Text(size=(40, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
]

# Kolom Area No 3: Area Image info dan Tombol list of processing
list_processing = [
    [sg.Text("Image Information:"),],
    [sg.Text(size=(20, 1), key="ImgSize"),],
    [sg.Text(size=(20, 1), key="ImgColorDepth"),],
    [sg.Text("List of Processing:"),],
    [sg.Button("Image Negative", size=(20, 1), key="ImgNegative"),],
    [sg.Button("Image Rotate", size=(20, 1), key="ImgRotate"),],
    [sg.Button("Image Grayscale", size=(20, 1), key="ImgGrayscale"),],
    [sg.Text("Brightness Value:"), sg.Input(size=(5, 1), key="BrightVal", default_text="30")],
    [sg.Button("Adjust Brightness", size=(20, 1), key="ImgBrightness"),],
    [sg.HSeparator()],
    [sg.Button("Save Image", size=(20, 1), button_color=("white", "green"), key="ImgSave"),]
]

# Kolom Area No 4: Area viewer image output
image_viewer_column2 = [
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(40, 1), key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer")],
]

# Gabung Full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.VSeperator(),
        sg.Column(list_processing),
        sg.VSeperator(),
        sg.Column(image_viewer_column2),
    ]
]
window = sg.Window("Mini Image Editor", layout)

#nama image file temporary setiap kali processing output
filename_out = "out.png" 

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Folder name was filled in, make a list of files in the folder
    if event == "ImgFolder":
        folder = values["ImgFolder"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["ImgList"].update(fnames)
    elif event == "ImgList": # A file was chosen from the listbox
        try:
            filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
            img_original = Image.open(filename)
            img_input = Image.open(filename)
            display_path = get_display_image(img_input)

            window["FilepathImgInput"].update(filename)
            window["ImgProcessingType"].update(filename)
            window["ImgInputViewer"].update(filename=display_path)
            window["ImgOutputViewer"].update(filename=display_path)

            img_width, img_height = img_input.size
            window["ImgSize"].update(f"Image Size : {img_width} x {img_height}")

            #img_input.show()

            #Size
            img_width, img_height = img_input.size
            window["ImgSize"].update("Image Size : "+str(img_width)+" x "+str(img_height))

            #Color depth
            mode_to_coldepth = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32, "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32}
            coldepth = mode_to_coldepth[img_input.mode]
            window["ImgColorDepth"].update("Color Depth : "+str(coldepth))
        except Exception as e:
            print(f"Error: {e}")

    elif event == "ImgNegative":
        try:
            window["ImgProcessingType"].update("Image Negative")
            img_output=ImgNegative(img_input,coldepth)
            img_input=img_output
            
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except:
            pass

    elif event == "ImgRotate":
        try:
            window["ImgProcessingType"].update("Image Rotate")
            img_output=ImgRotate(img_input,coldepth,90,"C")
            img_input = img_output
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except:
            pass
    
    elif event == "ImgGrayscale":
        try:
            window["ImgProcessingType"].update("Image Grayscale")
            img_output=ImgGrayscale(img_input,coldepth)
            img_input = img_output 
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except:
            pass
    
    elif event == "ImgBrightness":
        try:
            nilai = int(values["BrightVal"])
            window["ImgProcessingType"].update(f"Brightness ({nilai})")
            img_output=ImgBrightness(img_original, coldepth, nilai)
            img_input = img_output 
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except:
            pass
    
    elif event == "ImgSave":
        try:
            save_path = sg.popup_get_file(
                    "Save Image As", 
                    save_as=True, 
                    no_window=True, 
                    default_extension=".png",
                    file_types=(("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*"))
                )
            if save_path:
                success = SaveImage(img_input, save_path)
                if success:
                    sg.popup("Berhasil menyimpan!")
                else:
                        sg.popup_error("Gagal menyimpan gambar. Periksa konsol untuk detailnya.")
        except Exception as e:
            print(f"Error pada GUI Save: {e}")
                
window.close() 