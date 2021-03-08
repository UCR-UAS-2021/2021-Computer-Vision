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
    
    if(shape.get() == "Circle"):
        shape_choice = Shape(1)
    elif(shape.get() == "Semicircle"):
        shape_choice = Shape(2)
    elif(shape.get() == "Quarter_Circle"):
        shape_choice = Shape(3)
    elif(shape.get() == "Triangle"):
        shape_choice = Shape(4)
    elif(shape.get() == "Square"):
        shape_choice = Shape(5)
    elif(shape.get() == "Rectangle"):
        shape_choice = Shape(6)
    elif(shape.get() == "Trapezoid"):
        shape_choice = Shape(7)
    elif(shape.get() == "Pentagon"):
        shape_choice = Shape(8)
    elif(shape.get() == "Hexagon"):
        shape_choice = Shape(9)
    elif(shape.get() == "Heptagon"):
        shape_choice = Shape(10)
    elif(shape.get() == "Octagon"):
        shape_choice = Shape(11)
    elif(shape.get() == "Star"):
        shape_choice = Shape(12)
    elif(shape.get() == "Cross"):
        shape_choice = Shape(13)

    
    if(shape_color.get() == "White"):
        shape_color_choice = Color(1)
    elif(shape_color.get() == "Black"):
        shape_color_choice = Color(2)
    elif(shape_color.get() == "Gray"):
        shape_color_choice = Color(3)
    elif(shape_color.get() == "Red"):
        shape_color_choice = Color(4)
    elif(shape_color.get() == "Blue"):
        shape_color_choice = Color(5)
    elif(shape_color.get() == "Green"):
        shape_color_choice = Color(6)
    elif(shape_color.get() == "Yellow"):
        shape_color_choice = Color(7)
    elif(shape_color.get() == "Purple"):
        shape_color_choice = Color(8)
    elif(shape_color.get() == "Brown"):
        shape_color_choice = Color(9)
    elif(shape_color.get() == "Orange"):
        shape_color_choice = Color(10)
    
    
    if(alphanum_color.get() == "White"):
        alphanum_color_choice = Color(1)
    elif(alphanum_color.get() == "Black"):
        alphanum_color_choice = Color(2)
    elif(alphanum_color.get() == "Gray"):
        alphanum_color_choice = Color(3)
    elif(alphanum_color.get() == "Red"):
        alphanum_color_choice = Color(4)
    elif(alphanum_color.get() == "Blue"):
        alphanum_color_choice = Color(5)
    elif(alphanum_color.get() == "Green"):
        alphanum_color_choice = Color(6)
    elif(alphanum_color.get() == "Yellow"):
        alphanum_color_choice = Color(7)
    elif(alphanum_color.get() == "Purple"):
        alphanum_color_choice = Color(8)
    elif(alphanum_color.get() == "Brown"):
        alphanum_color_choice = Color(9)
    elif(alphanum_color.get() == "Orange"):
        alphanum_color_choice = Color(10)
    
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


window.mainloop()

