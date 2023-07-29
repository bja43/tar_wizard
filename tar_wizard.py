# import sys
# import os

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# import numpy as np
import pandas as pd

# import plotly
# import seaborn as sns
# import matplotlib.pyplot as plt

# import jpype as jp
# import jpype.imports

# jp.startJVM(classpath=["Tetrad-gui-current-launch.jar"])

# import edu.cmu.tetrad.search as ts
# import edu.cmu.tetrad.data as td


def open_file():
    fpath = filedialog.askopenfilename()
    df = pd.read_csv(fpath)
    print(df)
    # text.insert(INSERT, df)
    # sns.pairplot(df)
    # plt.show()


root = Tk()
root.geometry("420x420")
root.title("tar wizard 0.0.1")

notebook = ttk.Notebook(root)
tabs = [Frame(notebook) for _ in range(3)]
for i, tab in enumerate(tabs):
    notebook.add(tab, text=f"Tab {i}")
notebook.pack(expand=True, fill="both")

# text = Text(root)
# text.pack()

menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit)

edit_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")

# print(notebook[0])

canvas = Canvas(tabs[0], width=400, height=400)
canvas.pack()

# oval = canvas.create_oval(50, 50, 150, 150)

# global oval = None

def move(event):
    # event.x
    # event.y
    canvas.coords(circle, event.x-50, event.y-50, event.x+50, event.y+50)

canvas.bind("<B1-Motion>", move)

# button = Button(text="open", command=open_file)
# button.pack()

circle = canvas.create_oval(0, 0, 0, 0)

root.mainloop()
