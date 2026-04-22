from PIL import Image, ImageOps
import math

def get_display_image(img_pil, max_size=(390, 693)):
    if img_pil is None: return None
    img_temp = img_pil.copy()
    img_temp.thumbnail(max_size)
    temp_path = "temp_gui_preview.png"
    img_temp.save(temp_path)
    return temp_path

def SaveImage(img_pil, path):
    try:
        img_pil.save(path)
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False
    
#aritmatika
def ImgNegative(img_input,coldepth):

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
    else:
        img_output = img_output.convert("RGB")
    
    return img_output

def log(img_input, coldepth):
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
    else:
        img_output = img_output.convert("RGB")
    
    return img_output

def ImgBlend(img1, img2, alpha_value):
    # Alpha_value dari slider (0-100) diubah menjadi rentang 0.0 - 1.0 (C)
    c = alpha_value / 100.0
    
    # Pastikan kedua gambar dalam mode RGB
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    
    # Resize gambar kedua agar sama dengan gambar pertama
    if img1.size != img2.size:
        img2 = img2.resize(img1.size)
        
    img_output = Image.new('RGB', (img1.size[0], img1.size[1]))
    pixels = img_output.load()
    
    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            r1, g1, b1 = img1.getpixel((i, j)) # Gambar A
            r2, g2, b2 = img2.getpixel((i, j)) # Gambar B
            
            # Rumus: Pnew = C*A + (1-C)*B
            new_r = int(c * r1 + (1 - c) * r2)
            new_g = int(c * g1 + (1 - c) * g2)
            new_b = int(c * b1 + (1 - c) * b2)
            
            # Clipping if Pnew > 255
            if new_r > 255: new_r = 255
            if new_g > 255: new_g = 255
            if new_b > 255: new_b = 255
            
            pixels[i, j] = (new_r, new_g, new_b)
            
    return img_output

#geometri
def ImgRotate(img_input,coldepth,deg,direction):
    
    if coldepth!=24:
        img_input = img_input.convert('RGB')
    
    if direction == "180":
        img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    else: # Untuk 90 CW atau 90 CCW
        img_output = Image.new('RGB', (img_input.size[1], img_input.size[0]))

    
    pixels = img_output.load()
    width_in, height_in = img_input.size
    
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            if direction == "C": # 90 Degree CW
                r, g, b = img_input.getpixel((j, height_in - 1 - i))
            elif direction == "CC": # 90 Degree CCW
                r, g, b = img_input.getpixel((width_in - 1 - j, i))
            elif direction == "180": # 180 Degree
                r, g, b = img_input.getpixel((width_in - 1 - i, height_in - 1 - j))
            pixels[i,j] = (r, g, b)

    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgFlip(img_input, coldepth, mode):
    # Pastikan dalam mode RGB untuk pemrosesan piksel
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    # Dimensi tetap sama, tidak berubah seperti rotasi
    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels = img_output.load()
    
    for i in range(width):
        for j in range(height):
            if mode == "H":
                r, g, b = img_input.getpixel((i, height - 1 - j))
            elif mode == "V":
                r, g, b = img_input.getpixel((width - 1 - i, j))
            
            pixels[i, j] = (r, g, b)

    # Kembalikan ke Color Depth asli sesuai variabel coldepth yang kamu miliki
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output