from tkinter import *
from PIL import Image, ImageTk

root = Tk()

#setting up a tkinter canvas with scrollbars
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

canvas = Canvas(frame, bd=0)
canvas.grid(row=0, column=0, sticky=N+S+E+W)

frame.pack(fill=BOTH,expand=1)

open_file = Image.open("explain_dog.jpeg")
img = ImageTk.PhotoImage(open_file)

canvas.create_image(0, 0, image = img, anchor = "nw")

def printcoords(event):
	print(event.x, event.y)

canvas.bind("<Button 1>", printcoords)

root.mainloop()