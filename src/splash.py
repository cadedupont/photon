from tkinter import Tk, Label
from PIL import Image, ImageTk

# Create root window
root: Tk = Tk()
root.title("Photon")
root.iconbitmap("res/logo.ico")
root.resizable(False, False)

# Center root window to middle of screen
width: int = 800
height: int = 434
x: int = (root.winfo_screenwidth() // 2) - (width // 2)
y: int = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Load image
splash: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open("res/splash.jpg"))

# Create splash screen
splash_screen: Label = Label(root, image=splash)
splash_screen.pack()

# Run root window main loop for 3 seconds, then destroy
root.after(3000, root.destroy)
root.mainloop()