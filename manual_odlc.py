from tkinter import *
from proto.classes import *
from PIL import ImageTk,Image
import os
import json


class image_list:
    def __init__(self,
                 img_index: int,
                 img_dir: str,
                 os_list: list,
                 ):
        self.img_index = img_index
        self.img_dir = img_dir
        self.os_list = os_list

    def make_filename(self):
        return os.path.join(self.img_dir, self.os_list[self.img_index])

    def get_img_name(self):
        return self.os_list[self.img_index][:-4]

    def change_index(self, increment):
        self.img_index = (self.img_index + increment) % len(self.os_list)

    def update_os_list(self):
        self.os_list = os.listdir(self.img_dir)

    def remove_curr_img(self):
        self.os_list.remove(self.os_list[self.img_index])


img_list = image_list(0, './cropped_images', os.listdir('./cropped_images'))
# creates main window
window = Tk()
window.title("Tkinter Window")
window.geometry("400x300")
window.configure(bg="#1e2233")

# initialize a left and right column
left_frame = Frame(window)
left_frame.pack(side=LEFT)
left_frame.columnconfigure((0, 1), weight=1)
left_frame.configure(bg="#1e2233")

right_frame = Frame(window)
right_frame.pack(side=RIGHT, anchor = W)

filename = StringVar()
filename.set('Current image: ' + img_list.get_img_name())
filename_label = Label(left_frame, textvariable=filename, bg='#1e2233', fg='white', font='none 10 bold').grid(row=0, column=0)

shape_label = Label(left_frame, text="Shape", bg="#1e2233", fg="white", font="none 10 bold").grid(row=3, column=0)
shape = StringVar()
shape_entry = OptionMenu(left_frame, shape, "Circle", "Semicircle", "Quarter_Circle", "Triangle", "Square", "Rectangle",
                         "Trapezoid", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Star", "Cross")
shape_entry.configure(anchor=N)
shape_entry.grid(row=3, column=1, sticky="ew")


shape_color_label = Label(left_frame, text="Shape Color", bg="#1e2233", fg="white", font="none 10 bold").grid(row=4, column=0)

shape_color = StringVar()
shape_color_entry = OptionMenu(left_frame, shape_color, "White", "Black", "Gray", "Red", "Blue", "Green", "Yellow",
                               "Purple", "Brown", "Orange")
shape_color_entry.grid(row=4, column=1, sticky="ew")


alphanum_label = Label(left_frame, text="Alphanum", bg="#1e2233", fg="white", font="none 10 bold").grid(row=5, column=0)
alphanum = StringVar()
alphanum_entry = OptionMenu(left_frame, alphanum, *Alphanum)
alphanum_entry.grid(row=5, column=1, sticky="ew")


alpha_color_label = Label(left_frame, text="Alphanum Color", bg="#1e2233", fg="white", font="none 10 bold").grid(row=6, column=0)

alphanum_color = StringVar()
alphanum_color_entry = OptionMenu(left_frame, alphanum_color, "White", "Black", "Gray", "Red", "Blue", "Green", "Yellow",
                                  "Purple", "Brown", "Orange")
alphanum_color_entry.grid(row=6, column=1, sticky="ew")


rotation_label = Label(left_frame, text="Rotation", bg="#1e2233", fg="white", font="none 10 bold").grid(row=7, column=0)
rotation = StringVar()
rotation_entry = OptionMenu(left_frame, rotation, "N", "NE", "E", "SE", "S", "SW", "W", "NW")
rotation_entry.grid(row=7, column=1, sticky="ew")


# CHANGE IMG_0602.JPG to whatever images are needed to be opened

img = ImageTk.PhotoImage(Image.open(img_list.make_filename()))

panel = Label(right_frame, image=img)
panel.pack(side="left", fill="both", expand="yes")

# canvas = Canvas(leftframe, width = 500, height = 500)
# canvas.configure(bg = "black")
# canvas.pack(fill = BOTH)
# canvas.create_image(0, 0, anchor = NW, image=img)


# click function updates target_json.json when SUBMIT button is pressed.
def submit_click(img_list, panel):

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
    json_file = open('cropped_images_data/' + img_list.get_img_name() + '.json', 'w')
    json_file.write(json_string)
    json_file.close()

    # Label (window, text = data, bg = "black", fg = "white", font = "none 10 bold").grid(row = 5, column = 0)
    shape.set('')
    shape_color.set('')
    alphanum.set('')
    alphanum_color.set('')
    rotation.set('')
    img_list.remove_curr_img()
    change_img(img_list, panel, 1)



def change_img(img_list, panel, increment):
    img_list.change_index(increment)
    filename.set('Current image: ' + img_list.get_img_name())
    img = ImageTk.PhotoImage(Image.open(img_list.make_filename()))
    panel.configure(image=img)
    panel.image = img
    panel.pack(side="left", fill="both", expand="yes")


Button(left_frame, text="Submit", width=5, command=lambda *args: submit_click(img_list, panel), bg='#1e2233', fg='white').grid(row=8, column=1)

Button(left_frame, text="Left", width=5, command=lambda *args: change_img(img_list, panel, -1), bg='#1e2233', fg='white').grid(row=8, column=0)

Button(left_frame, text="Right", width=5, command=lambda *args: change_img(img_list, panel, 1), bg='#1e2233', fg='white').grid(row=8, column=2)


if __name__ == "__main__":
    if not os.path.exists('cropped_images_data'):
        os.makedirs('cropped_images_data')
    window.mainloop()
