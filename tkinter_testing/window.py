import tkinter.filedialog
import tkinter.messagebox
import tkinter as tk

import cv2
from PIL import Image, ImageTk

import os
import socket

def select_image():
 global panelA
 global image_path

 path = tk.filedialog.askopenfilename()
 image_path = path

 if len(path) > 0:
    image = cv2.imread(path)

    if image.shape[1] >= 1120:
        scale_percent = 1120 / image.shape[1] * 100
    else:
        scale_percent = 100
    height = int(image.shape[0] * scale_percent / 100)
    width = int(image.shape[1] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    if panelA is None:
        panelA = tk.Label(image=image)
        panelA.image = image
        panelA.pack(side="left", padx=10, pady=10)
    else:
        panelA.configure(image=image)
        panelA.image = image

def send_image():
    if panelA is not None:
        HOST = '192.168.1.5' # Server IP or Hostname
        PORT = 65432 #1000+ recoommended
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST,PORT))

        while True:
            f = open(image_path, 'rb')
            data = f.read(1024)

            while (data):
                print('Sending Image...')
                sock.send(data)
                data = f.read(1024)
            f.close()
            print('Image sent!')
            sock.close()
            break
        sock.close()
    else:
        tk.messagebox.showwarning("Error", "Please add an image before sending to the Raspberry Pi.")

window = tk.Tk()
panelA = None

select_image_button = tk.Button(window, text="Select an image", command=select_image)
select_image_button.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

send_button = tk.Button(window, text="Send image", command=send_image)
send_button.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

window.mainloop()