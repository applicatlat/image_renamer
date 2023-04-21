import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image
import PIL
from tkinter import ttk

reverse_list = []
"""
This code aims to change an image file's name by adding_width_height_kb values of the respected image. The purpose of
this action is to help the content creator to categorize images accordingly within his/her projects. The code that
stores the names, getting the width, height and size values of the images and undoing the action codes were written
by Levent Alahan Tekinalp. The UI is created with the help of chatgpt. Within the code I will mention my initials
where I contributed and mention as well the ChatGPT's.
"""


def update_progress(progress_bar, value):
    """
    ChatGPT
    This function updates the value of progress bar
    :param progress_bar: the progress bar widget
    :param value: the current value of the progress bar
    :return:
    """
    progress_bar["value"] = value
    progress_bar.update()


def my_function(my_list):
    """
    Chat GPT
    this function creates the progressbar and updates based on the list of images
    :param my_list: the list to be taken as the basis of the measurement
    :return:
    """
    my_list = list(range(100))
    progress_bar = ttk.Progressbar(canvas, orient="horizontal", length=200, mode="determinate", maximum=100)
    canvas.create_window(200, 180, window=progress_bar, width=200)
    for i, item in enumerate(my_list):
        # perform some task
        update_progress(progress_bar, (i + 1) * 100 / len(my_list))


def reverse_process():
    """
    LAT & ChatGPT
    reverses the name change operation made either by select files or select folders operation. It must be called
    after the name change operation has done
    :return:
    """

    try:
        entries = os.listdir(reverse_list[0])
        print(reverse_list[0])
    except IndexError:
        return
    x = 0
    for item in reverse_list[1:]:
        print(item)
        if entries[x].find(item):
            try:
                my_function(reverse_list[1:])
                print(reverse_list[0] + "/" + entries[x])
                os.rename(reverse_list[0] + "/" + entries[x], reverse_list[0] + "/" + item)
            except PIL.UnidentifiedImageError:
                print("pass")
                pass
        x += 1

    reverse_list.clear()


def convert_units(byte_size, unit):
    """
    LAT
    This function converts byte to KB for readability
    :param byte_size: byte size of the image
    :param unit: created for multiple implementation in the future currently there is only KB option
    :return:
    """
    if unit == "KB":
        return round(byte_size / 1024)


def select_files():
    """
    ChatGPT & LAT - Uses tkinter module to crate file picker. Multiple files can be picked.
    :return:
    """
    try:
        files = filedialog.askopenfilenames(multiple=True)
        folder = files[0].rsplit('/', 1)[0]
        reverse_list.append(folder)

    except FileNotFoundError:
        return
    except IndexError:
        return
    for file in files:
        old_name = file
        file_name = file.rsplit('/', 1)[-1]

        try:
            reverse_list.append(str(file_name))
            img = Image.open(old_name)
            new_file_raw = str("_" + str(img.size[0]) + "w" + "_" + str(img.size[1]) + "h" + "_" + str(
                convert_units(byte_size=os.stat(folder + "/" + file_name).st_size, unit="KB")) + "kb")
            new_full_file = folder + "/" + str(os.path.splitext(file_name)[0]) + new_file_raw + ".jpg"
            img.close()
            os.rename(old_name, new_full_file)
            my_function(files)

        except PIL.UnidentifiedImageError:
            print("pass")
            pass


def select_folders():
    """
    Chat-gpt & LAT - picks multiple files
    :return:
    """
    try:
        folders = filedialog.askdirectory()

        entries = os.listdir(folders)
        reverse_list.append(folders)
        my_function(my_list=folders)
    except FileNotFoundError:
        return
    for entry in entries:
        old_name = folders + "/" + entry
        try:
            reverse_list.append(str(entry))
            img = Image.open(old_name)
            new_file_raw = str("_" + str(img.size[0]) + "w" + "_" + str(img.size[1]) + "h" + "_" + str(
                convert_units(byte_size=os.stat(folders + "/" + entry).st_size, unit="KB")) + "kb")
            new_full_file = folders + "/" + str(os.path.splitext(entry)[0]) + new_file_raw + ".jpg"
            img.close()
            os.rename(old_name, new_full_file)
        except PIL.UnidentifiedImageError:
            print("pass")
            pass


class ElegantButton(tk.Button):
    """
    CHATGPT
    Class that creates blue colored stylish button
    """
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.config(relief=tk.FLAT, bd=0, bg='#0F4D92', fg='white',
                    activebackground='#00A5E5', activeforeground='white',
                    font=('Helvetica', 12), padx=10, pady=5)
        self.bind('<Enter>', lambda e: self.config(bg='#00A5E5'))
        self.bind('<Leave>', lambda e: self.config(bg='#0F4D92'))


root = tk.Tk()
root.title('File name changer')

root.geometry("400x300")
root.resizable(False, False)

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

start_color = "#73C2FB"
end_color = "#0F4C81"

for i in range(300):
    r = int(start_color[1:3], 16) + (int(end_color[1:3], 16) - int(start_color[1:3], 16)) * i // 300
    g = int(start_color[3:5], 16) + (int(end_color[3:5], 16) - int(start_color[3:5], 16)) * i // 300
    b = int(start_color[5:7], 16) + (int(end_color[5:7], 16) - int(start_color[5:7], 16)) * i // 300
    color = f"#{r:02x}{g:02x}{b:02x}"

    canvas.create_rectangle(0, i, 400, i + 1, fill=color, outline="")

folder_button = ElegantButton(root, text="Select Folder", command=select_folders)
file_button = ElegantButton(root, text="Select File", command=select_files)
reverse_button = ElegantButton(root, text="Reverse", command=reverse_process)

canvas.create_window(200, 25, window=folder_button, width=100)
canvas.create_window(200, 75, window=file_button, width=100)
canvas.create_window(200, 125, window=reverse_button, width=100)

root.mainloop()
