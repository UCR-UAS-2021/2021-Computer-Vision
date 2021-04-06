from tkinter import *
from proto.classes import *
from PIL import ImageTk,Image 
import json

#creates main window
window = Tk()
window.title("Tkinter Window")
window.configure(bg = "black")

#initialize a left and right column
leftframe = Frame(window)
leftframe.pack(side = LEFT)
leftframe.configure(bg = "black")

rightframe = Frame(window)
rightframe.pack(side = RIGHT, anchor = W)




Label (leftframe, text = "Enter the shape:", bg = "black", fg = "white", font = "none 10 bold").pack()
shape = StringVar()
shape_entry = OptionMenu( rightframe, shape, "Circle", "Semicircle", "Quarter_Circle", "Triangle", "Square", "Rectangle","Trapezoid", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Star", "Cross"
)
shape_entry.configure(anchor = N) 
shape_entry.pack()


Label (leftframe, text = "Enter the shape color:", bg = "black", fg = "white", font = "none 10 bold").pack()

shape_color = StringVar()
shape_color_entry = OptionMenu(rightframe, shape_color, "White", "Black", "Gray", "Red", "Blue", "Green", "Yellow", "Purple", "Brown", "Orange"
)
shape_color_entry.pack()


Label (leftframe, text = "Enter the character:", bg = "black", fg = "white", font = "none 10 bold").pack()
alphanum = StringVar()
alphanum_entry = OptionMenu(rightframe, alphanum, *Alphanum
)
alphanum_entry.pack()


Label (leftframe, text = "Enter the character color:", bg = "black", fg = "white", font = "none 10 bold").pack()

alphanum_color = StringVar()
alphanum_color_entry = OptionMenu(rightframe, alphanum_color, "White", "Black", "Gray", "Red", "Blue", "Green", "Yellow", "Purple", "Brown", "Orange"
)
alphanum_color_entry.pack()


Label (leftframe, text = "Enter the rotation in degrees", bg = "black", fg = "white", font = "none 10 bold").pack()

rotation_entry = Entry(rightframe, width = 5, bg = "white")
rotation_entry.pack()


#CHANGE IMG_0602.JPG to whatever images are needed to be opened
img = ImageTk.PhotoImage(Image.open("IMG_0602.JPG"))

canvas = Canvas(leftframe, width = 500, height = 500)
canvas.configure(bg = "black")
canvas.pack(fill = BOTH)
canvas.create_image(0, 0, anchor = NW, image=img)


#click function updates target_json.json when SUBMIT button is pressed.
def click():

    shape_choice = Shape[shape.get()]

    shape_color_choice = Color[shape_color.get()]

    alphanum_color_choice = Color[alphanum_color.get()]

    rotation = rotation_entry.get()
    
    my_target = Target(alphanumeric=alphanum.get(),
                  shape=shape_choice,
                  alphanumeric_color=alphanum_color_choice,
                  shape_color=shape_color_choice,
                  posx=0,
                  posy=0,
                  rotation=rotation,
                  height=0,
                  width=0)

    #data = my_target.make_target_only_json()
    json_string = my_target.make_target_only_json()

    #Our json file takes the name 'target_json.json
    json_file = open('target_json.json', 'w')
    json_file.write(json_string)
    json_file.close()
    #Label (window, text = data, bg = "black", fg = "white", font = "none 10 bold").grid(row = 5, column = 0)
    
    
    

#creates submit button
Button(rightframe, text = "Submit", width = 5, command = click) .pack()

if __name__ == "__main__":
    window.mainloop()

