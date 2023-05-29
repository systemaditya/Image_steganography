from tkinter import *
from tkinter import messagebox as mb
from PIL import Image

def generate_data(pixels, data):
    data_in_binary = []

    for c in data:
        binary_data = format(ord(c), '08b')
        data_in_binary.append(binary_data)

    length_of_data = len(data_in_binary)
    image_data = iter(pixels)

    for a in range(length_of_data):
        pixels = [val for val in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]

        for b in range(8):
            if (data_in_binary[a][b] == '1') and (pixels[b] % 2 != 0):
                pixels[b] -= 1
            elif (data_in_binary[a][b] == '0') and (pixels[b] % 2 == 0):
                if pixels[b] == 0:
                    pixels[b] += 1
                pixels[b] -= 1

        if (length_of_data-1) == a:
            if pixels[-1] % 2 == 0:
                if pixels[-1] == 0:
                    pixels[-1] += 1
                else:
                    pixels[-1] -= 1

        pixels = tuple(pixels)

        yield pixels[:3]
        yield pixels[3:6]
        yield pixels[6:9]


def encryption(img, data):
    # This method will encode data to the new image that will be created
    size = img.size[0]
    (a, b) = (0, 0)

    for pixel in generate_data(img.getdata(), data):
        img.putpixel((a, b), pixel)
        if size-1 == a:
            a = 0; b += 1
        else:
            a += 1


def main_encryption(img, text, new_image_name):
    # This function will take the arguments, create a new image, encode it and save it to the same directory
    image = Image.open(img, 'r')

    if (len(text) == 0) or (len(img) == 0) or (len(new_image_name) == 0):
        mb.showerror("Error", 'You have not put a value! Please put all values before pressing the button')

    new_image = image.copy()
    encryption(new_image, text)

    new_image_name += '.png'

    new_image.save(new_image_name, 'png')


def main_decryption(img, strvar):
    # This function will decode the image given to it and extract the hidden message from it
    image = Image.open(img, 'r')

    data = ''
    image_data = iter(image.getdata())

    decoding = True

    while decoding:
        pixels = [value for value in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]

        # string of binary data
        binary_string = ''

        for c in pixels[:8]:
            if c % 2 == 0:
                binary_string += '0'
            else:
                binary_string += '1'

        data += chr(int(binary_string, 2))
        if pixels[-1] % 2 != 0:
            strvar.set(data)


# Creating the button functions
def encode_image():
    encode_wn = Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('600x220')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='AntiqueWhite')
    Label(encode_wn, text='Encode an Image', font=("Comic Sans MS", 15), bg='AntiqueWhite').place(a=220, rely=0)

    Label(encode_wn, text='Enter the path to the image(with extension):', font=("Times New Roman", 13),
          bg='AntiqueWhite').place(a=10, b=50)
    Label(encode_wn, text='Enter the data to be encoded:', font=("Times New Roman", 13), bg='AntiqueWhite').place(
        a=10, b=90)
    Label(encode_wn, text='Enter the output file name (without extension):', font=("Times New Roman", 13),
          bg='AntiqueWhite').place(a=10, b=130)

    img_path = Entry(encode_wn, width=35)
    img_path.place(a=350, b=50)

    text_to_be_encoded = Entry(encode_wn, width=35)
    text_to_be_encoded.place(a=350, b=90)

    after_save_path = Entry(encode_wn, width=35)
    after_save_path.place(a=350, b=130)

    Button(encode_wn, text='Encode the Image', font=('Helvetica', 12), bg='PaleTurquoise', command=lambda:
    main_encryption(img_path.get(), text_to_be_encoded.get(), after_save_path.get())).place(a=220, b=175)


def decode_image():
    decode_wn = Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('600x300')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='Bisque')

    Label(decode_wn, text='Decode an Image', font=("Comic Sans MS", 15), bg='Bisque').place(a=220, rely=0)

    Label(decode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 12),
          bg='Bisque').place(a=10, b=50)

    img_entry = Entry(decode_wn, width=35)
    img_entry.place(a=350, b=50)

    text_strvar = StringVar()

    Button(decode_wn, text='Decode the Image', font=('Helvetica', 12), bg='PaleTurquoise', command=lambda:
    main_decryption(img_entry.get(), text_strvar)).place(a=220, b=90)

    Label(decode_wn, text='Text that has been encoded in the image:', font=("Times New Roman", 12), bg='Bisque').place(
        a=180, b=130)

    text_entry = Entry(decode_wn, width=94, text=text_strvar, state='disabled')
    text_entry.place(a=15, b=160, height=100)


# Initializing the window
root = Tk()
root.title('Bits Pilani Project by\nAditya Varma')
root.geometry('300x200')
root.resizable(0, 0)
root.config(bg='Moccasin')

Label(root, text='Bits Pilani Project by\nAditya Varma', font=('Aldhabi', 15), bg='Moccasin',
      wraplength=500).place(x=65, y=10)

Button(root, text='Encode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=encode_image).place(
    x=30, y=80)

Button(root, text='Decode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=decode_image).place(
    x=30, y=130)

# Finalizing the window
root.update()
root.mainloop()