from tkinter import *
import Gebruikersscherm
from tkinter import messagebox
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
import Klok

day_type = Klok.day_type()
number_of_entries = 3

def get_temperature_scheme(day_type):

    global temperature_list
    temperature_list = []
    key_positions = []
    result = []

    if day_type == 'week':

        temperature_list = Gebruikersscherm.temperature_week()

    elif day_type == 'weekend':

        temperature_list = Gebruikersscherm.temperature_weekend()

    for i in range(1,len(temperature_list)):
        if temperature_list[i] != temperature_list[i-1]:
            key_positions.append(i)
    length = len(key_positions)

    for i in range(number_of_entries-length):
        key_positions.append(None)

    return key_positions

def add_entries(button):

    global number_of_entries
    number_of_entries += 1
    button.destroy()
    show_entries()

def show_entries():

    global from_list, to_list, degrees_list

    from_list = []
    to_list = []
    degrees_list = []
    day_type = Klok.day_type()
    key_positions = get_temperature_scheme(day_type)

    for i in range(number_of_entries):

        i_entry = Entry(temp_schedule_root, width = 5)
        i_entry.place(x=530, y=170 + i*45)
        from_list.append(i_entry)
        if i == 0:
            i_entry.insert(0,"0")

        else:
            if key_positions[i-1] is not None:
                i_entry.insert(0,str(key_positions[i-1]))

    for j in range(number_of_entries):

        j_entry = Entry(temp_schedule_root, width =5)
        j_entry.place(x=630, y = 170 + j*45)
        to_list.append(j_entry)
        if j == number_of_entries-1:
            j_entry.insert(0, "0")

        else:
            if key_positions[j] is not None:
                j_entry.insert(0,str(key_positions[j]))

    for k in range(number_of_entries):

        k_entry = Entry(temp_schedule_root, width=5)
        k_entry.place(x=730 ,y= 170 + k*45)
        degrees_list.append(k_entry)

        if k == 0:
            k_entry.insert(0,str(temperature_list[0]))

        else:
            if key_positions[k-1] is not None:
                k_entry.insert(0,str(temperature_list[key_positions[k-1]]))

    plus_button = Button(temp_schedule_root, text = "+", command = lambda: add_entries(plus_button), width = 5, height = 1)
    plus_button.place(x=800, y=200 + (number_of_entries-1)*45)

def temperature_schedule():

    global from_list, to_list, degrees_list, temp_schedule_root

    temp_schedule_root = Tk()
    temp_schedule_root.title("Temperature schedule")
    temp_schedule_root.geometry("900x600+400+100")

    canvas = Canvas(temp_schedule_root, width = 400, height = 300, highlightthickness = 0)
    canvas.place(x=20, y=120)

    title_label = Label(temp_schedule_root, text= "Adjust the daily temperature schedule")
    title_label.config(font=('Courier', 20))
    title_label.place(x=10, y=10)

    current_schedule_label = Label(temp_schedule_root, text= "Current temperature schedule:")
    current_schedule_label.config(font=('Courier', 15))
    current_schedule_label.place(x=10, y=80)

    adjust_schedule_label = Label(temp_schedule_root, text= "Adjust temperature schedule:")
    adjust_schedule_label.config(font=('Courier', 15))
    adjust_schedule_label.place(x=480, y=80)

    from_label = Label(temp_schedule_root, text = "from (h)")
    from_label.config(font=('Courier',15))
    from_label.place(x=530, y=130)

    to_label = Label(temp_schedule_root, text="to (h)")
    to_label.config(font=('Courier', 15))
    to_label.place(x=630, y=130)

    degrees_label= Label(temp_schedule_root, text="°C")
    degrees_label.config(font=('Courier',15))
    degrees_label.place(x=730, y=130)

    show_entries()

    enter_week_button = Button(temp_schedule_root, text="Enter for week", command= lambda: [get_entries(from_list, to_list, degrees_list, "week"),temperature_graph()], width = 15, height = 3)
    enter_week_button.place(x=520, y= 450)

    enter_weekend_button = Button(temp_schedule_root, text="Enter for weekend",
                               command=lambda: [get_entries(from_list, to_list, degrees_list, "weekend"), temperature_graph()], width=15,
                               height=3)
    enter_weekend_button.place(x=660, y=450)
    temperature_graph()

def get_entries(from_list, to_list, degrees_list, day_type):
    result = []

    for i in range(len(from_list)):
        for j in range(i+1,len(from_list)):
            if from_list[i].get() == from_list[j].get() or from_list[i].get() == to_list[i].get():
                messagebox.showerror("Error", "Not possible, try again.")
                return

            elif from_list[i].get() == '' and to_list[i].get() != '':
                messagebox.showerror("Error", "Not possible, try again.")
                return

            elif from_list[i].get() == '' and degrees_list[i].get() != '':
                messagebox.showerror("Error", "Not possible, try again.")
                return

    if int(from_list[0].get()) != 0 or int(to_list[len(from_list)-1].get()) != 0:
        messagebox.showerror("Error", "Make sure every hour has a temperature")
        return

    for i in range(len(from_list)-1):
        for j in range(int(to_list[i].get())-int(from_list[i].get())):
            result.append(degrees_list[i].get())

    for i in range(24-int(from_list[len(from_list)-1].get())):
        result.append(degrees_list[len(from_list)-1].get())

    messagebox.showinfo("Confirmed","Succesfully saved")

    if day_type == 'week':
        Gebruikersscherm.change_temperature_week(result)

    if day_type == 'weekend':
        Gebruikersscherm.change_temperature_weekend(result)

def temperature_graph():

    canvas = Canvas(temp_schedule_root, width=400, height=300, highlightthickness=0)
    canvas.place(x=20, y=120)

    day_type = Klok.day_type()

    if day_type == 'week':
        temperatures = Gebruikersscherm.temperature_week()
    elif day_type == 'weekend':
        temperatures = Gebruikersscherm.temperature_weekend()

    hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    f = matplotlib.figure.Figure((4, 4), dpi=100)
    a = f.add_subplot(111)
    a.plot(hours, temperatures)

    canvas2 = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(f, canvas)
    canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)
    canvas2._tkcanvas.pack(side=TOP, fill=BOTH, expand=TRUE)

    a.set_xlabel("Time (h)")
    a.set_ylabel("Temperature (°C)")
    a.set_xticks(hours, minor=True)


