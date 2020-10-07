import tkinter.filedialog
import tkinter.messagebox
import tkinter as tk

import cv2
from PIL import Image, ImageTk

import os
import socket

global panelA

def get_image():
    # Server IP or Hostname
    HOST = ''

    # Make sure it's 1000+
    PORT = 65432

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST, PORT))
    s.listen()

    print('Waiting for messages')
    (conn, addr) = s.accept()
    print('Got connection from', addr)

    while True:
        f = open('image.png', 'wb')
        conn.send(b'Send the Image')

        data = conn.recv(1024)
        while (data):
            print('Downloading file...')
            f.write(data)
            data = conn.recv(1024)
        f.close()
        print('Finished')
        conn.close()

    conn.close() # Close connections

    image = cv2.imread("image.png")

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

window = tk.Tk()
panelA = None

get_image_button = tk.Button(window, text="Get image", command=get_image)
get_image_button.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

window.mainloop()