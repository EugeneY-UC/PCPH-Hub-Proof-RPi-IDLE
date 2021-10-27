# -*- coding: utf-8 -*-
#!/usr/bin/python3

import tkinter as tk
from tkinter import font as tkfont
from pathlib import Path
import csv
import time


PIN_LENGTH = 4
PASSWORD_LENGTH = 6

CSV_FOLDER = Path("CSV")


class Node:

    def __init__(self, num=0):
        self.__num = num
        self.__power_applied = False

    def get_num(self):
        return self.__num

    def get_power_applied(self):
        return self.__power_applied

    def set_power_applied(self, power):
        self.__power_applied = power


class User:
    
    def __init__(self, num=0):
        self.__num = num
        self.__pin = None
        self.__node_num = 0

    def get_num(self):
        return self.__num

    def get_pin(self):
        return self.__pin

    def set_pin(self, pin):
        self.__pin = str(pin).zfill(PIN_LENGTH)

    def get_node_num(self):
        return self.__node_num

    def set_node_num(self, node_num):
        self.__node_num = node_num

    def pin_ok(self, pin):
        if self.__pin == None:
            return False
        else:
            return self.__pin == pin

class Users:
    def __init__(self, path=CSV_FOLDER / "user_test.csv"):
        self.__users = self.__read_csv(path)

    def get_users(self):
        return self.__users

    def set_users(self, users):
        self.__users = users

    def get_user_by_pin(self, pin):
        for user in self.__users:
            if user.get_pin() == pin:
                return user
        return None

    @staticmethod
    def __read_csv(path):
        read_users = list()
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_count = 0
            for row in csv_reader:
                column_count = 0
                for column in row:
                    if row_count > 0:
                        if column_count == 0:
                            new_user = User(int(column))
                        elif column_count == 1:
                            new_user.set_pin(column)
                        elif column_count == 2:
                            new_user.set_node_num(int(column))
                        read_users.append(new_user)
                    column_count += 1
                row_count += 1
        return read_users


frame_num = 0

cur_user = None
cur_pin = -1       
node_num = -1

users = Users()


def switch_to_fullscreen(event):
    root.attributes("-fullscreen", True)

def switch_from_fullscreen(event):
    root.attributes("-fullscreen", False)


def time_event_gen():
    global frame_num
    if frame_num == 4:
        frame_4.event_generate('<<time_event>>', when='tail')

def to_fourthscreen(event):
    global frame_num
    frame_num = 4
    frame_3.pack_forget()
    frame_4.pack(fill="both", expand=True)
    frame_4.focus_set()
    frame_4.after(5000, time_event_gen)

def to_thirdscreen(event):
    global frame_num
    frame_num = 3
    frame_2.pack_forget()
    label_3_0.configure(text="Charger #" + str(node_num) + " selected")
    frame_3.pack(fill="both", expand=True)
    frame_3.focus_set()

def to_secondscreen(event):
    global frame_num
    frame_num = 2
    frame_1.pack_forget()
    frame_3.pack_forget()
    frame_2.pack(fill="both", expand=True)
    name_node_num.set(node_num)
    entry_2_1_2.focus()
    entry_2_1_2.select_range(0, tk.END)

def to_firstscreen(event):
    global frame_num
    frame_num = 1
    frame_0.pack_forget()
    frame_1.pack(fill="both", expand=True)
    entry_1.focus_set()

def to_zeroscreen(event):
    global frame_num
    frame_num = 0
    frame_1.pack_forget()
    frame_2.pack_forget()
    frame_3.pack_forget()
    frame_4.pack_forget()
    name_pin.set('')
    frame_0.pack(fill="both", expand=True)
    frame_0.focus_set()


root = tk.Tk()

root.wm_title("PCPH  HUB")
root.geometry("800x600")
root.minsize(800, 600)
root.configure(bg="#3838B8")
root.attributes("-fullscreen", True)

name_pin = tk.StringVar()
name_node_num = tk.StringVar(root, value=node_num)

color_front = "white"
color_back = "#3838B8"
color_entry_back = "#B8B8F8"

font_1 = tkfont.Font(family="Helvetica", size=128)
font_2 = tkfont.Font(family="Helvetica", size=24)
font_3 = tkfont.Font(family="Helvetica", size=32)
font_4 = tkfont.Font(family="Helvetica", size=48)
font_5 = tkfont.Font(family="Helvetica", size=64)


frame_0 = tk.Frame(root, bg=color_back)

def key_press(event):
    if event.char == event.keysym or len(event.char) == 1:
        to_firstscreen(event)

frame_0.bind("<Key>", key_press)
frame_0.pack(fill="both", expand=True)
frame_0.focus_set()

label_0_1 = tk.Label(frame_0,
                     text="--------    PCPH    --------",
                     font=font_1,
                     fg=color_front,
                     bg=color_back)
label_0_1.place(relx=0.5, rely=0.45, anchor='n')

label_0_2 = tk.Label(frame_0,
                     text="Press any key to activate",
                     font=font_2,
                     fg=color_front,
                     bg=color_back)
label_0_2.place(relx=0.5, rely=0.85, anchor='n')


frame_1 = tk.Frame(root, bg=color_back)

font_1_1 = tkfont.Font(family="Verdana", size=48)
font_1_2 = tkfont.Font(family="Arial", size=64, weight="bold")

label_1 = tk.Label(frame_1, text="Enter " + str(PIN_LENGTH) + "-digit PIN",
                font=font_1_1,
                fg=color_front,
                bg=color_back)
label_1.place(relx=0.5, rely=0.3, anchor="c")


def get_entry_1(event):
    global node_num
    global cur_pin
    global cur_user
    if len(name_pin.get()) == PIN_LENGTH:
        try:
            cur_pin = int(name_pin.get())
        except:
            name_pin.set('')
            return
        cur_user = users.get_user_by_pin(str(cur_pin).zfill(PIN_LENGTH))
        if cur_user is None:
           name_pin.set('')
           return
        user_num = cur_user.get_num()
        node_num = cur_user.get_node_num()
        to_secondscreen(event)
    else:
        name_pin.set('')

entry_1 = tk.Entry(frame_1,
                textvariable=name_pin,
                font=font_1_2,
                width=PIN_LENGTH,
                bg=color_entry_back)
entry_1.bind("<Return>", get_entry_1)
entry_1.bind("<Escape>", to_zeroscreen)
entry_1.place(relx=0.5, rely=0.5, anchor="c")
entry_1.focus_set()

label_2 = tk.Label(frame_1, text="Press Cancel to return",
                font=font_2,
                fg=color_front,
                bg=color_back)
label_2.place(relx=0.5, rely=0.85, anchor="n")


frame_2 = tk.Frame(root, bg='white')

def clear_entry(event):
    entry_2_1_2.delete(0, tk.END)

frame_2_1 = tk.Frame(frame_2, bg='white')
frame_2_1.place(relwidth=1, relheight=0.8)

frame_2_2 = tk.Frame(frame_2, bg=color_back)
frame_2_2.place(rely=0.8, relwidth=1, relheight=0.2)

label_2_1_1 = tk.Label(frame_2_1,
                       text="Current rate per hour:",
                       font=font_3)
label_2_1_1.place(relx=0.35, rely=0.3, anchor= 'c')

label_2_1_2 = tk.Label(frame_2_1,
                       text="Please enter your \n charger number:",
                       font=font_3)
label_2_1_2.place(relx=0.35, rely=0.7, anchor='c')

button_2_1_1 = tk.Button(frame_2_1,
                         text="$0.183",
                         font=font_3)
button_2_1_1.place(relx=0.75, rely=0.3, anchor='c')

def get_entry(event):
    global node_num
    try:
        node_num = int(name_node_num.get())
        to_thirdscreen(event)
    except:
        name_node_num.set('')

entry_2_1_2 = tk.Entry(frame_2_1,
                       textvariable=name_node_num,
                       width=3,
                       font=font_3)
entry_2_1_2.bind('<Escape>', clear_entry)
entry_2_1_2.bind('<Return>', get_entry)
entry_2_1_2.place(relx=0.75, rely=0.7, anchor='c')

label_2_2 = tk.Label(frame_2_2,
                  text="Press Enter to select",
                  font=font_2,
                  bg=color_back,
                  fg='white')
label_2_2.place(relx=0.5, rely=0.5, anchor='c')


frame_3 = tk.Frame(root, bg=color_back)

frame_3.bind("<Escape>", to_secondscreen)
frame_3.bind("<Return>", to_fourthscreen)
frame_3.focus_set()

label_3_0 = tk.Label(frame_3,
                     font=font_4,
                     fg=color_front,
                     bg=color_back)
label_3_0.place(relx=0.5, rely=0.4, anchor='n')

label_3_1 = tk.Label(frame_3, text="Press Enter to confirm and start charging",
                font=font_2,
                fg=color_front,
                bg=color_back)
label_3_1.place(relx=0.5, rely=0.8, anchor="n")

label_3_2 = tk.Label(frame_3, text="Press Cancel to return",
                font=font_2,
                fg=color_front,
                bg=color_back)
label_3_2.place(relx=0.5, rely=0.9, anchor="n")

frame_4 = tk.Frame(root, bg=color_back)

frame_4.bind("<Escape>", to_zeroscreen)
frame_4.bind("<<time_event>>", to_zeroscreen)

label_4_1 = tk.Label(frame_4,
                     text="Charging Started",
                     font=font_5,
                     fg=color_front,
                     bg=color_back)
label_4_1.place(relx=0.5, rely=0.45, anchor='n')
                   
label_4_2 = tk.Label(frame_4, text="Press Cancel to return",
                font=font_2,
                fg=color_front,
                bg=color_back)
label_4_2.place(relx=0.5, rely=0.85, anchor="n")


root.bind("<Shift-Up>", switch_to_fullscreen)
root.bind("<Shift-Down>", switch_from_fullscreen)
root.bind("<Shift-Escape>", to_zeroscreen)

root.mainloop()
