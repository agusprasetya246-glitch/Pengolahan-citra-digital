import FreeSimpleGUI as sg
import os.path
from PIL import Image, ImageOps
from processing_list import *

sg.theme("LightBlue2")

file_list_column = [
    [sg.Text("Open Image Folder :"),],
    [sg.In(size=(20, 1), enable_events=True, key="ImgFolder"),sg.FolderBrowse(),],        
    [sg.Text("Choose an image from list :"),],
    [sg.Listbox(values=[], enable_events=True, size=(18, 10), key="ImgList")],
    [sg.Text("Image Information:"),],
    [sg.Text(size=(20, 1), key="ImgSize"),],
    [sg.Text(size=(20, 1), key="ImgColorDepth"),],
]

image_viewer_column = [
    [sg.Text("Image Input :")],
    [sg.Text(size=(40, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
]

image_viewer_column2 = [
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(40, 1), key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer")],
]

image_viewer_column_2nd = [
    [sg.pin(sg.Column([
        [sg.Text("Image Input 2 (Blend):"),sg.Button("Select 2nd Image", key="ImgSelect2")],
        [sg.Image(key="ImgInputViewer2")],
        [sg.Text("Opacity (%):")],
        [sg.Slider(range=(0, 100), orientation='h', default_value=50, key="BlendAlpha", enable_events=True)]
    ], key="ColBlend", visible=False))]
]

list_processing = [
    [sg.Text("List of Processing:")],
    [sg.Button("Image Negative", size=(20, 1), key="ImgNegative"),
     sg.Button("Image Grayscale", size=(20, 1), key="ImgGrayscale"),
     sg.Button("Logaritmik", size=(20,1), key="Log"),
     sg.Button("blend mode",size=(20,1), key="ModeBlend"),
     sg.Button("Save Image", size=(20, 1), button_color=("white", "green"), key="ImgSave"),
     sg.Text("Brightness Value:"),
     sg.Slider(range=(-255, 255), orientation='h', size=(15, 15), default_value=0, key="BrightVal", enable_events=True),sg.Button("reset", size=(5,1), key="Default")
     ],
     [sg.Button("Image Rotate 90C", size=(20, 1), key="ImgRotate"),
      sg.Button("Image Rotate 90CCW", size=(20, 1), key="ImgRotateCCW"),
      sg.Button("Image Rotate 180", size=(20, 1), key="ImgRotate180"),
      sg.Button("Flip(V)", size=(20, 1), key="flipv"),
      sg.Button("Flip(H)", size=(20, 1), key="fliph"),]
]

layout = [
    [sg.Column(list_processing, expand_x=True)],
    [sg.HSeparator()],
    [
        sg.Column(file_list_column, vertical_alignment='top'),
        sg.VSeperator(),
        sg.Column(image_viewer_column, expand_x=True, expand_y=True, vertical_alignment='top'),
        sg.VSeperator(),
        sg.Column(image_viewer_column_2nd, vertical_alignment='top'),
        sg.VSeperator(),
        sg.Column(image_viewer_column2, expand_x=True, expand_y=True, vertical_alignment='top'),
    ]
]

window = sg.Window("Mini Image Editor", layout, resizable=True).finalize()
window.maximize()

filename_out = "out.png" 

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

#ARITMATIKA
    elif event == "ImgNegative":
        try:
            window["ImgProcessingType"].update("Image Negative")
            img_output=ImgNegative(img_input,coldepth)
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except:
            pass

    elif event == "ImgGrayscale":
        try:
            window["ImgProcessingType"].update("Image Grayscale")
            img_output=ImgGrayscale(img_input,coldepth)
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except Exception as e:
            print(f"Error Gryscale: {e}")

    elif event == "Log":
        try:
            window["ImgProcessingType"].update("Logarithmic")
            img_output = log(img_input, coldepth)
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except Exception as e:
            print(f"Error Auto Tone: {e}")
    
    elif event == "BrightVal":
        try:
            nilai = int(values["BrightVal"])
            window["ImgProcessingType"].update(f"Brightness ({nilai})")
            img_output=ImgBrightness(img_original, coldepth, nilai)
            img_output.save(filename_out) 
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except Exception as e:
            print(f"Error Live Brightness: {e}")

    elif event == "ModeBlend":
        # Toggle visibilitas kolom blend
        is_visible = window["ColBlend"].visible
        window["ColBlend"].update(visible=not is_visible)
    
    elif event == "ImgSelect2":
        filename2 = sg.popup_get_file("Pilih Gambar Kedua", no_window=True)
        if filename2:
            img_input2 = Image.open(filename2)
            display_path2 = get_display_image(img_input2)
            window["ImgInputViewer2"].update(filename=display_path2)

    elif event == "BlendAlpha":
        try:
            # Pastikan img_input2 sudah ada
            img_output = ImgBlend(img_original, img_input2, values["BlendAlpha"])
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except Exception as e:
            print(f"Pilih gambar kedua dulu: {e}")

#GEOMETRI
    elif event == "ImgRotate":
        try:
            window["ImgProcessingType"].update("Image Rotate")
            img_output=ImgRotate(img_input,coldepth,90,"C")
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except:
            pass

    elif event == "ImgRotateCCW":
        try:
            window["ImgProcessingType"].update("Image Rotate")
            img_output=ImgRotate(img_input,coldepth,-90,"CC")
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except:
            pass

    elif event == "ImgRotate180":
        try:
            window["ImgProcessingType"].update("Image Rotate")
            img_output=ImgRotate(img_input,coldepth,180,"180")
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except:
            pass
    
    elif event == "fliph":
        try:
            window["ImgProcessingType"].update("Flip Horizontal")
            img_output = ImgFlip(img_input, coldepth, "H")
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except Exception as e:
            print(f"Error Flip H: {e}")

    elif event == "flipv":
        try:
            window["ImgProcessingType"].update("Flip Vertical")
            img_output = ImgFlip(img_input, coldepth, "V")
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except Exception as e:
            print(f"Error Flip V: {e}")

    elif event == "Default":
        try:
            window["BrightVal"].update(0)
            window["BlendAlpha"].update(50)
            window["ImgProcessingType"].update("Brightness (0) - Reset")
            img_output.save(filename_out)
            display_out = get_display_image(img_input)
            window["ImgOutputViewer"].update(filename=display_out)
        except Exception as e:
            print(f"Error Reset: {e}")

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