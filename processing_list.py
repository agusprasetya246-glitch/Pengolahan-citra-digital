from PIL import Image, ImageOps

def get_display_image(img_pil, max_size=(400, 400)):
    if img_pil is None: return None
    img_temp = img_pil.copy()
    img_temp.thumbnail(max_size)

    temp_path = "temp_gui_preview.png"
    img_temp.save(temp_path)
    return temp_path

def ImgNegative(img_input,coldepth):
    #solusi 1
    #img_output=ImageOps.invert(img_input)

    #solusi 2
    if coldepth!=24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i,j] = (255-r, 255-g, 255-b)

    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgRotate(img_input,coldepth,deg,direction):
    #solusi 1
    #img_output=img_input.rotate(deg)

    #solusi 2
    if coldepth!=24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB',(img_input.size[1],img_input.size[0]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            if direction=="C":
                r, g, b = img_input.getpixel((j,img_output.size[0]-i-1))
            else:
                r, g, b = img_input.getpixel((img_input.size[1]-j-1,i))
            pixels[i,j] = (r, g, b)

    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgGrayscale(img_input, coldepth):
    # Konversi ke RGB jika perlu untuk memproses pixel
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    # Buat kanvas baru dengan ukuran yang sama
    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()

    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))

            gray = int((r + g + b) / 3)
            pixels[i, j] = (gray, gray, gray)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output