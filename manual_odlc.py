from tkinter import *
from proto.classes import *
from PIL import ImageTk,Image
import os
import json


# creates main window
window = Tk()
window.title("Tkinter Window")
window.geometry("400x300")
window.configure(bg="gray")

# initialize a left and right column
left_frame = Frame(window)
left_frame.pack(side=LEFT)
left_frame.columnconfigure((0, 1), weight=1)
left_frame.configure(bg="gray")

right_frame = Frame(window)
right_frame.pack(side=RIGHT, anchor = W)


shape_label = Label(left_frame, text="Shape", bg="gray", fg="white", font="none 10 bold").grid(row=3, column=0)
shape = StringVar()
shape_entry = OptionMenu(left_frame, shape, "Circle", "Semicircle", "Quarter_Circle", "Triangle", "Square", "Rectangle",
                         "Trapezoid", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Star", "Cross")
shape_entry.configure(anchor=N)
shape_entry.grid(row=3, column=1, sticky="ew")


shape_color_label = Label(left_frame, text="Shape Color", bg="gray", fg="white", font="none 10 bold").grid(row=4, column=0)

shape_color = StringVar()
shape_color_entry = OptionMenu(left_frame, shape_color, "White", "Black", "Gray", "Red", "Blue", "Green", "Yellow",
                               "Purple", "Brown", "Orange")
shape_color_entry.grid(row=4, column=1, sticky="ew")


alphanum_label = Label(left_frame, text="Alphanum", bg="gray", fg="white", font="none 10 bold").grid(row=5, column=0)
alphanum = StringVar()
alphanum_entry = OptionMenu(left_frame, alphanum, *Alphanum)
alphanum_entry.grid(row=5, column=1, sticky="ew")


alpha_color_label = Label(left_frame, text="Alphanum Color", bg="gray", fg="white", font="none 10 bold").grid(row=6, column=0)

alphanum_color = StringVar()
alphanum_color_entry = OptionMenu(left_frame, alphanum_color, "White", "Black", "Gray", "Red", "Blue", "Green", "Yellow",
                                  "Purple", "Brown", "Orange")
alphanum_color_entry.grid(row=6, column=1, sticky="ew")


rotation_label = Label(left_frame, text="Rotation", bg="gray", fg="white", font="none 10 bold").grid(row=7, column=0)
rotation = StringVar()
rotation_entry = OptionMenu(left_frame, rotation, "N", "NE", "E", "SE", "S", "SW", "W", "NW")
rotation_entry.grid(row=7, column=1, sticky="ew")


# CHANGE IMG_0602.JPG to whatever images are needed to be opened

img_index = 0
img_dir = "./cropped_images"
os_list = os.listdir(img_dir)
img = ImageTk.PhotoImage(Image.open(os.path.join(img_dir, os_list[img_index])))

panel = Label(right_frame, image=img)
panel.pack(side="left", fill="both", expand="yes")

# canvas = Canvas(leftframe, width = 500, height = 500)
# canvas.configure(bg = "black")
# canvas.pack(fill = BOTH)
# canvas.create_image(0, 0, anchor = NW, image=img)


# click function updates target_json.json when SUBMIT button is pressed.
def submit_click(index, directory, panel):

    shape_choice = Shape[shape.get()]

    shape_color_choice = Color[shape_color.get()]

    alphanum_color_choice = Color[alphanum_color.get()]
    
    my_target = Target(alphanumeric=alphanum.get(),
                       shape=shape_choice,
                       alphanumeric_color=alphanum_color_choice,
                       shape_color=shape_color_choice,
                       posx=0,
                       posy=0,
                       rotation=rotation.get(),
                       height=0,
                       width=0)

    json_string = my_target.make_target_only_json()

    # Our json file takes the name 'target_json.json
    json_file = open('cropped_images_data/' + os.listdir(directory)[index][:-4] + '.json', 'w')
    json_file.write(json_string)
    json_file.close()

    # Label (window, text = data, bg = "black", fg = "white", font = "none 10 bold").grid(row = 5, column = 0)
    shape.set('')
    shape_color.set('')
    alphanum.set('')
    alphanum_color.set('')
    rotation.set('')
    change_img(img_index, img_dir, panel, 1)



def change_img(index, directory, panel, increment):
    global img_index
    index += increment
    file_list = os.listdir(directory)
    img_index = index % len(file_list)
    img = ImageTk.PhotoImage(Image.open(os.path.join(directory, file_list[img_index])))
    panel.configure(image=img)
    panel.image = img
    panel.pack(side="left", fill="both", expand="yes")


# TODO: Figure out passing in parameters here
Button(left_frame, text="Submit", width=5, command=lambda *args: submit_click(img_index, img_dir, panel)).grid(row=8, column=1)

Button(left_frame, text="Left", width=5, command=lambda *args: change_img(img_index, img_dir, panel, -1)).grid(row=8, column=0)

Button(left_frame, text="Right", width=5, command=lambda *args: change_img(img_index, img_dir, panel, 1)).grid(row=8, column=2)


if __name__ == "__main__":
    if not os.path.exists('cropped_images_data'):
        os.makedirs('cropped_images_data')
    window.mainloop()
