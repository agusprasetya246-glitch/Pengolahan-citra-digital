from PIL import Image, ImageOps
import math

def get_display_image(img_pil, max_size=(600, 600)):
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

def SaveImage(img_pil, path):
    try:
        img_pil.save(path)
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False

def ImgBrightness(img_input, coldepth, nilai):
    # Pastikan dalam mode RGB untuk pemrosesan piksel
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()
    
    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))
            
            new_r = int(r) + nilai
            new_g = int(g) + nilai
            new_b = int(b) + nilai

            if new_r > 255: new_r = 255
            if new_r < 0: new_r = 0
            
            if new_g > 255: new_g = 255
            if new_g < 0: new_g = 0
            
            if new_b > 255: new_b = 255
            if new_b < 0: new_b = 0
            
            pixels[i, j] = (new_r, new_g, new_b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output

def ImgAutoTone(img_input, coldepth):
    # Pastikan dalam mode RGB untuk pemrosesan piksel
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()

    c = 255 / math.log(1 + 255) 
    
    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))
            
            new_r = int(c * math.log(1 + r))
            new_g = int(c * math.log(1 + g))
            new_b = int(c * math.log(1 + b))
            
            pixels[i, j] = (new_r, new_g, new_b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output