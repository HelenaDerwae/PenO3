from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.backend_bases import key_press_handler
from daily_schedule import *
import Data_tables as dt
import Gebruikersscherm
import pandas as pd
import matplotlib
import grafieken
import Temperature_schedule
import Database
import Klok
import matplotlib.pyplot as plt
import Optimalisatie
#import Optimalisatie_for_GUI


now = Klok.datetime_now()

root = Tk()
root.title("Login")
root.geometry("750x500+400+100")

kitchen_bool = False
living_bool = False
bedroom_bool = False
bathroom_bool = False
storage_bool = False
supply_bool = False
settings_bool = False
car_bool = False
daily_schedule_bool = False
temperature_bool = False
lighting_bool = False


def set_false_kitchen():
    global kitchen_bool
    kitchen_home.destroy()
    kitchen_bool = False


def set_false_living():
    global living_bool
    living_home.destroy()
    living_bool = False


def set_false_bedroom():
    global bedroom_bool
    bedroom_home.destroy()
    bedroom_bool = False


def set_false_bathroom():
    global bathroom_bool
    bathroom_home.destroy()
    bathroom_bool = False


def set_false_storage():
    global storage_bool
    storage_home.destroy()
    storage_bool = False


def set_false_car():
    global car_bool
    car_home.destroy()
    car_bool = False


def set_false_supply():
    global supply_bool
    supply_home.destroy()
    supply_bool = False


def set_false_settings():
    global settings_bool
    settings_home.destroy()
    settings_bool = False


def set_false_lighting():
    global lighting_bool
    lights_root.destroy()
    lighting_bool = False


def lighting():
    global lights_canvas, lights_root, text_list, room_list_database, lighting_bool

    lights_root = Toplevel()
    lights_root.title("Lighting")
    lights_root.geometry("900x500")

    lighting_bool = True

    room_list = ["Kitchen", "Living Room", "Bedroom", "Bathroom", "Storage space"]
    room_list_database = ["keuken", "living", "slaapkamer", "badkamer", "berging"]
    text_list = []

    title = Label(lights_root, text="Turn the lights around the house on and off")
    title.config(font=('Courier', 23))
    title.place(x=10, y=10)

    room = Label(lights_root, text="Room:")
    room.config(font=('Courier', 23))
    room.place(x=50, y=75)

    status = Label(lights_root, text="Status:")
    status.config(font=('Courier', 23))
    status.place(x=300, y=75)

    lights_canvas = Canvas(lights_root, highlightthickness=0)
    lights_canvas.place(x=350, y=155)

    for i in range(len(room_list)):
        i_label1 = Label(lights_root, text=room_list[i])
        i_label1.config(font=('Courier', 20))
        i_label1.place(x=50, y=150 + 45 * i)

        i_text = lights_canvas.create_text(20, 20 + i * 45, fill="black", font=('Courier', 15),
                                           text=Gebruikersscherm.light(room_list_database[i]))
        text_list.append(i_text)

        i_on_button = Button(lights_root, text="On",
                             command=lambda i=i: [Gebruikersscherm.set_light_on(room_list_database[i]),
                                                  update_lights(i)])
        i_on_button.config(font=('Courier', 15))
        i_on_button.place(x=450, y=150 + 45 * i)

        i_off_button = Button(lights_root, text="Off",
                              command=lambda i=i: [Gebruikersscherm.set_light_off(room_list_database[i]),
                                                   update_lights(i)])
        i_off_button.config(font=('Courier', 15))
        i_off_button.place(x=500, y=150 + 45 * i)

    lights_root.protocol('WM_DELETE_WINDOW', set_false_lighting)


def update_lights(i):
    lights_canvas.itemconfigure(text_list[i], text=Gebruikersscherm.light(room_list_database[i]))


def driving_time_today():
    global entry_box_driving, today, driving_entry
    today = Klok.date_now()[8:10]
    if not Gebruikersscherm.updated_distance():
        entry_box_driving = Toplevel()
        entry_box_driving.title("Driving time")
        entry_box_driving.geometry("300x100+800+300")

        driving_label = Label(entry_box_driving, text="What distance did you  travel today?")
        driving_label.grid(row=0, column=0)
        driving_entry = Entry(entry_box_driving)
        driving_entry.grid(row=1, column=0)
        hours_label = Label(entry_box_driving, text="km")
        hours_label.grid(row=1, column=1)

        ok_button = Button(entry_box_driving, text="Ok", command=ok_driving)
        ok_button.grid(row=2, column=0)

        entry_box_driving.protocol('WM_DELETE_WINDOW', donothing)


def ok_driving():
    driving_time = driving_entry.get()
    if driving_time.replace(".", "").isdigit():
        entry_box_driving.destroy()
        Gebruikersscherm.set_distance(driving_time)
        home_root.deiconify()
    else:
        messagebox.showerror("Error", "Please fill in a number")


def buttons(canvas, machine):
    on_button = Button(canvas, text="On", command=lambda: start(machine), width=10, height=3)
    on_button.grid(row=3, column=0)

    undo_button = Button(canvas, text="Undo", command=lambda: undo(machine), width=10, height=3)
    undo_button.grid(row=3, column=2)

    off_button = Button(canvas, text="Off", command=lambda: stop(machine), width=10, height=3)
    off_button.grid(row=3, column=4)

    delete_button = Button(canvas, text="delete", command=lambda: delete(machine), width=10, height=3)
    delete_button.grid(row=3, column=6)


def start(machine):
    Gebruikersscherm.start_button(machine)
 #   Optimalisatie_for_GUI.optimization_random_on()


def stop(machine):
    Gebruikersscherm.stop_button(machine)


def undo(machine):
    Gebruikersscherm.undo_button(machine)


def delete(machine):
    global warning_screen
    warning_screen = Toplevel()
    warning_screen.title("Add device")
    warning_screen.geometry("300x100+800+300")

    warning_label = Label(warning_screen, text="Are you sure you want to delete this device?")
    warning_label.place(x=25, y=15)

    yes_delete = Button(warning_screen, text="Yes", command=lambda: delete_ok(machine), width=5, height=1)
    yes_delete.place(x=100, y=50)

    no_delete = Button(warning_screen, text="No", command=delete_no, width=5, height=1)
    no_delete.place(x=160, y=50)


def delete_ok(machine):
    Gebruikersscherm.delete_machine(machine)
#    Optimalisatie_for_GUI.optimization_random_on()
    warning_screen.destroy()


def delete_no():
    warning_screen.destroy()


def hide_canvas():
    i = 0
    while i < 29:
        try:
            all_canvasses = [stove_canvas, stove_canvas2, oven_canvas, oven_canvas2, dishwasher_canvas,
                             dishwasher_canvas2, tv_canvas, tv_canvas2, boiler_canvas, boiler_canvas2,
                             electric_car_canvas, electric_car_canvas2, tumble_dryer_canvas, tumble_dryer_canvas2,
                             washing_machine_canvas, washing_machine_canvas2, pc_canvas, pc_canvas2,
                             solar_panels_canvas, solar_panels_canvas2, windmill_canvas, windmill_canvas2,
                             battery_canvas, baterry_canvas2, plus_canvas]
            all_canvasses[i].pack_forget()
            i += 1
        except NameError:
            i += 1


def center(win, y):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def donothing():
    return


def close_all():
    if kitchen_bool:
        kitchen_home.destroy()
    if living_bool:
        living_home.destroy()
    if bedroom_bool:
        bedroom_home.destroy()
    if bathroom_bool:
        bathroom_home.destroy()
    if storage_bool:
        storage_home.destroy()
    if supply_bool:
        supply_home.destroy()
    if settings_bool:
        settings_home.destroy()
    if car_bool:
        car_home.destroy()
    if lighting_bool:
        lights_root.destroy()
    if temperature_bool:
        temp_schedule_root.destroy()
    if daily_schedule_bool:
        schedule_home.destroy()
    home_root.destroy()


def show_window(home):
    frame_list = {kitchen_home, living_home, bedroom_home, bathroom_home, storage_home, supply_home, settings_home,
                  car_home}
    for i in frame_list:
        if i == home:
            home.deiconify()
        else:
            i.iconify()


def hide_window(home):
    frame_list = {kitchen_home, living_home, bedroom_home, bathroom_home, storage_home, supply_home, settings_home,
                  car_home}
    for i in frame_list:
        if i == home:
            home.iconify()
        else:
            i.iconify()


def click_next_2():
    if str(entry_name.get()) == login and str(entry_pass.get()) == password:
        logout_home.destroy()
        home()
    else:
        messagebox.showerror("Error", "Wrong combination, try again!")


def close_logout():
    logout_home.destroy()


def logout():
    global logout_home

    close_all()
    logout_home = Toplevel()
    logout_home.title("Login")
    logout_home.geometry("750x500+400+100")

    frame_1 = Frame(logout_home, width=500, height=400, bd=10, relief=GROOVE)
    frame_1.place(x=125, y=50)

    label_name = Label(frame_1, text="Name")
    label_pass = Label(frame_1, text="Password")
    entry_name = Entry(frame_1, width=40)
    entry_pass = Entry(frame_1, width=40)

    label_name.config(font=('Courier', 20))
    label_pass.config(font=('Courier', 20))

    label_name.place(x=100, y=100)
    label_pass.place(x=40, y=150)
    entry_name.place(x=200, y=110)
    entry_pass.place(x=200, y=160)

    next_button = Button(frame_1, text="Next", command=click_next_2, width=10, height=2)
    next_button.config(relief=RAISED, font=('Courier', 10))
    next_button.place(x=195, y=230)

    logout_home.protocol('WM_DELETE_WINDOW', close_logout)


#******************************
def add_commands(room_menu, window):
    if room_menu == home_menu:
        room_menu.add_command(label="Home", command= donothing)

    else:
        room_menu.add_command(label="Home", command= window.iconify)
    room_menu.add_command(label="Kitchen", command=lambda: kitchen_window())
    room_menu.add_command(label="Living Room", command=lambda: livingroom_window())
    room_menu.add_command(label="Bathroom", command=lambda: bathroom_window())
    room_menu.add_command(label="Bedroom", command=lambda: bedroom_window())
    room_menu.add_command(label="Storage space", command=lambda: storage_window())
    room_menu.add_command(label="Energy Supply", command=lambda: supply_window())
    room_menu.add_command(label="Car", command=lambda: car_window())
    room_menu.add_command(label="Settings", command=lambda: settings_window())


def get_device_name(window, row, column, room):

    global entry_box, device_entry, device_row, device_window, device_column, duration_entry,\
        usage_entry
    device_window = window
    device_row = row
    device_column = column

    blank_canvas = Canvas(window, width=1000, height=1000, highlightthickness=0)
    blank_canvas.place(x=325, y=0)

    entry_box = Toplevel()
    entry_box.title("Add device")
    entry_box.geometry("300x170+800+300")

    device_label = Label(entry_box, text="What is the name of your device?")
    device_label.grid(row=0, column=1)
    device_entry = Entry(entry_box)
    device_entry.grid(row=1, column=1)

    duration_label = Label(entry_box, text="What is the uptime of your device?")
    duration_label.grid(row=2, column=1)
    time = Label(entry_box, text="hours")
    time.grid(row=3, column=2)
    duration_entry = Entry(entry_box)
    duration_entry.grid(row=3, column=1)

    usage_label = Label(entry_box, text="What is the usage of your device?")
    usage_label.grid(row=4, column=1)
    usage = Label(entry_box, text="kWh")
    usage.grid(row=5, column=2)
    usage_entry = Entry(entry_box)
    usage_entry.grid(row=5, column=1)

    ok_button = Button(entry_box, text="Ok", command=lambda: add_device(device_window, device_row, device_column, room))
    ok_button.grid(row=6, column=1)


def add_device(window, row, column, room):
    device_name = str(device_entry.get())
    device_duration = duration_entry.get()
    device_usage = usage_entry.get()
    entry_box.destroy()
    if (not device_usage.replace(".", "").isdigit()) and (not device_duration.replace(".", "").isdigit()):
        messagebox.showerror("Error", "The usage of your machine should be a number.")
        messagebox.showerror("Error", "The duration of your machine should be a number.")
        get_device_name(window, row, column, room)
    elif not device_usage.replace(".", "").isdigit():
        messagebox.showerror("Error", "The usage of your machine should be a number.")
        get_device_name(window, row, column, room)
    elif not device_duration.replace(".", "").isdigit():
        messagebox.showerror("Error", "The duration of your machine should be a number.")
        get_device_name(window, row, column, room)
    else:
        device_button = Button(window, text=device_name, command=lambda: plus_button_func(window, device_name), width=20, height=5)
        device_button.grid(row=row, column=column)
        Gebruikersscherm.add_machine(device_name, float(device_duration), float(device_usage), str(room))
        grafieken.devices.append(str(device_name))

        if column == 0:
            new_row = row
            new_column = column + 1
            new_button = Button(window, text="+", command=lambda: get_device_name(window, new_row, new_column, room), width=20,
                                height=5)
            new_button.grid(row=new_row, column=new_column)

        elif column == 1:
            if row != 4:
                new_row = row + 1
                new_column = 0
                new_button = Button(window, text="+", command=lambda: get_device_name(window, new_row, new_column, room),
                                    width=20, height=5)
                new_button.grid(row=new_row, column=new_column)

            else:
                messagebox.showwarning("Warning", "Maximum number of devices reached!")


#*********temperature***********


def read_inside_temperature():
    return Gebruikersscherm.inside_temperature()


def temp_plus(event):

    Gebruikersscherm.set_manual_date_temperature()

    new_temperature = int(read_inside_temperature()) + 1

    Gebruikersscherm.change_temperature(str(new_temperature))

 #   Optimalisatie_for_GUI.optimization_random_on()


def temp_minus(event):

    Gebruikersscherm.set_manual_date_temperature()

    new_temperature = int(read_inside_temperature()) - 1

    Gebruikersscherm.change_temperature( str(new_temperature))

#    Optimalisatie_for_GUI.optimization_random_on()


def update_temp():
    home_canvas.itemconfigure(temp_text, text = str(read_inside_temperature()))
    home_canvas.itemconfigure(date, text=Klok.full_datetime_now())
    home_root.after(500, update_temp)


#*******plus*********
def plus_button_func(home, device):
    global plus_canvas
    hide_canvas()
    plus_canvas = Canvas(home, width=500, height=500, highlightthickness=0)
    plus_canvas.place(x=325, y=5)
    plus_canvas2 = Canvas(home, width=400, height=400, highlightthickness=0)
    plus_canvas2.place(x=375, y=425)

    buttons(plus_canvas2, str(device))
    grafieken.make_graph(plus_canvas, device)


#******************** Car ******************
def car_window():
    global car_home, current_car, from_entry, to_entry, car_bool
    car_home = Toplevel()
    car_home.title("Car")
    car_home.geometry("750x500+400+100")

    car_bool = True

    car_menu = Menu(car_home)
    car_home.config(menu=car_menu)

    add_commands(car_menu, car_home)

    existing_car = Gebruikersscherm.existing_car()
    text = "current car: " + str(existing_car)
    current_car = Label(car_home, text=text)
    current_car.config(font=('Courier', 10))
    current_car.place(x=300, y=50)

    set_car_button = Button(car_home, text="Set car", command=set_car, width=15, height=3)
    set_car_button.place(x=75, y=100)

    change_car_button = Button(car_home, text="Change car", command=set_car, width=15, height=3)
    change_car_button.place(x=325, y=100)

    delete_car_button = Button(car_home, text="Delete car", command=delete_car, width=15, height=3)
    delete_car_button.place(x=600, y=100)

    ask_label = Label(car_home, text="Between what hours do you want the car to reload?")
    to_label = Label(car_home, text="To")
    hours1_label = Label(car_home, text="h")
    hours2_label = Label(car_home, text="h")

    from_entry = Entry(car_home, width=5)
    to_entry = Entry(car_home, width=5)

    ask_label.config(font=('Courier', 10))
    to_label.config(font=('Courier', 10))
    hours1_label.config(font=('Courier', 10))
    hours2_label.config(font=('Courier', 10))

    ask_label.place(x=200, y=200)
    to_label.place(x=380, y=250)
    hours1_label.place(x=340, y=250)
    hours2_label.place(x=465, y=250)

    from_entry.place(x=300, y=250)
    to_entry.place(x=425, y=250)

    weekday_button = Button(car_home, text="Set as standard for weekdays", command=set_car_week, width=25, height=3)
    weekend_button = Button(car_home, text="Set as standard for weekends", command=set_car_weekend, width=25, height=3)
    manual_button = Button(car_home, text="Set for tomorrow", command=set_car_manual, width=20, height=3)
    weekday_button.place(x=50, y=300)
    weekend_button.place(x=300, y=300)
    manual_button.place(x=580, y=300)

 #   car_home.iconify()
    car_home.protocol('WM_DELETE_WINDOW', set_false_car)


def set_car_week():
    start_time = from_entry.get()
    stop_time = to_entry.get()
    if (start_time.isdigit() and stop_time.isdigit()) or (start_time.replace(".", "").isdigit() and
                                                          stop_time.replace(".", "").isdigit()):
        if start_time == stop_time:
            messagebox.showerror("Error", "Start time and stop time may not be the same.")
        if start_time > stop_time:
            messagebox.showerror("Error", "Start time can not be a higher number than stop time.")
        else:
            schedule_car = [start_time, stop_time]
            Gebruikersscherm.change_car_week(schedule_car)
    else:
        messagebox.showerror("Error", "Please enter valid numbers.")
#    Optimalisatie_for_GUI.optimization_random_on()


def set_car_weekend():
    start_time = from_entry.get()
    stop_time = to_entry.get()
    if (start_time.isdigit() and stop_time.isdigit()) or (start_time.replace(".", "").isdigit() and
                                                          stop_time.replace(".", "").isdigit()):
        if start_time == stop_time:
            messagebox.showerror("Error", "Start time and stop time may not be the same.")
        if start_time > stop_time:
            messagebox.showerror("Error", "Start time can not be a higher number than stop time.")
        else:
            schedule_car = [start_time, stop_time]
            Gebruikersscherm.change_car_weekend(schedule_car)
    else:
        messagebox.showerror("Error", "Please enter valid numbers.")
#        Optimalisatie_for_GUI.optimization_random_on()


def set_car_manual():
    start_time = from_entry.get()
    stop_time = to_entry.get()
    if (start_time.isdigit() and stop_time.isdigit()) or (start_time.replace(".", "").isdigit() and
                                                          stop_time.replace(".", "").isdigit()):
        if start_time == stop_time:
            messagebox.showerror("Error", "Start time and stop time may not be the same.")
        if start_time > stop_time:
            messagebox.showerror("Error", "Start time can not be a higher number than stop time.")
        else:
            schedule_car = [start_time, stop_time]
            Gebruikersscherm.change_car_manual(schedule_car)
    else:
        messagebox.showerror("Error", "Please enter valid numbers.")
 #   Optimalisatie_for_GUI.optimization_random_on()


def set_car():
    global device_entry, range_entry, duration_entry, capacity_entry, entry_box_car
    entry_box_car = Toplevel()
    entry_box_car.title("New car")
    entry_box_car.geometry("300x200+800+300")

    device_label = Label(entry_box_car, text="What is the name of this car?")
    device_label.grid(row=0, column=1)
    #    device_name = StringVar()
    device_entry = Entry(entry_box_car)
    device_entry.grid(row=1, column=1)

    range_label = Label(entry_box_car, text="What is the range of this car?")
    range_label.grid(row=2, column=1)
    range = Label(entry_box_car, text="km")
    range.grid(row=3, column=2)
    range_entry = Entry(entry_box_car)
    range_entry.grid(row=3, column=1)

    duration_label = Label(entry_box_car, text="What is the charging duration of this car?")
    duration_label.grid(row=4, column=1)
    time = Label(entry_box_car, text="hours")
    time.grid(row=5, column=2)
    duration_entry = Entry(entry_box_car)
    duration_entry.grid(row=5, column=1)

    capacity_label = Label(entry_box_car, text="What is the capacity of the battery of this car?")
    capacity_label.grid(row=6, column=1)
    capacity = Label(entry_box_car, text="F")
    capacity.grid(row=7, column=2)
    capacity_entry = Entry(entry_box_car)
    capacity_entry.grid(row=7, column=1)

    ok_button = Button(entry_box_car, text="Ok", command=set_car_ok)
    ok_button.grid(row=8, column=1)


def set_car_ok():
    car_name = device_entry.get()
    car_range = range_entry.get()
    car_capacity = capacity_entry.get()
    car_duration = duration_entry.get()
    if car_duration.replace(".", "").isdigit() and car_capacity.replace(".", "").isdigit() and \
            car_range.replace(".", "").isdigit():
        if float(car_duration) > 0 and float(car_capacity) > 0 and float(car_range) > 0:
            Gebruikersscherm.set_car(str(car_name),  str(car_range), str(car_capacity), str(car_duration))
            entry_box_car.destroy()
            current_car.config(text="current car: " + str(car_name))
    else:
        messagebox.showerror("Error", "Please enter a valid number for the duration, range and capacity")
#    Optimalisatie_for_GUI.optimization_random_on()


def delete_car():
    Gebruikersscherm.delete_car()
    current_car.config(text="current car: ")
#    Optimalisatie_for_GUI.optimization_random_on()

# *****************************KITCHEN***************************
def kitchen_window():

    global kitchen_home, kitchen_bool

    kitchen_home = Toplevel()
    kitchen_home.title("Kitchen")
    kitchen_home.geometry("750x500+400+100")

    kitchen_bool = True

    kitchen_menu = Menu(kitchen_home)
    kitchen_home.config(menu=kitchen_menu)

    add_commands(kitchen_menu, kitchen_home)

    i = 0
    j = 0
    for device in Gebruikersscherm.machines_room("kitchen"):
        if device == "oven":
            device_name = "Oven"
            device = oven
            device_button = Button(kitchen_home, text=device_name, command=device, width=20, height=5)
            device_button.grid(row=i, column=j)
        elif device == "kookplaat":
            device_name = "Stove"
            device = stove
            device_button = Button(kitchen_home, text=device_name, command=device, width=20, height=5)
            device_button.grid(row=i, column=j)
        elif device == "koelkast":
            device_name = "Refrigerator"
            device = fridge
            device_button = Button(kitchen_home, text=device_name, command=device, width=20, height=5)
            device_button.grid(row=i, column=j)
        elif device == "vriezer":
            device_name = "Freezer"
            device = freezer
            device_button = Button(kitchen_home, text=device_name, command=device, width=20, height=5)
            device_button.grid(row=i, column=j)
        elif device == "afwasmachine":
            device_name = "Dishwasher"
            device = dishwasher
            device_button = Button(kitchen_home, text=device_name, command=device, width=20, height=5)
            device_button.grid(row=i, column=j)
        elif device != "oven" and device != "kookplaat" and device != "koelkast" and device != "vriezer" and device != "afwasmachine":
            device_name = str(device)
            device_button = Button(kitchen_home, text=device_name, command=lambda: plus_button_func(kitchen_home, device), width=20, height=5)
            device_button.grid(row=i, column=j)

        if j == 0:
            j += 1
        else:
            j = 0
            i += 1
        if i == 4 and j == 1:
            messagebox.showwarning("warning", "You have reached the maximum number of devices for this room")

    plus_button = Button(kitchen_home, text="+", command= lambda: get_device_name(kitchen_home, i, j, "kitchen"), width=20,
                         height=5)

    plus_button.grid(row=i, column=j)

    kitchen_home.protocol('WM_DELETE_WINDOW', set_false_kitchen)


#****************** Kitchen machines **************
def fridge():
    hide_canvas()
    blank_canvas = Canvas(kitchen_home, width=1000, height=1000, highlightthickness=0)
    blank_canvas.place(x=325, y=0)
    messagebox.showinfo("consumption refrigerator", "The annual consumption of the refrigerator is 116 kWh.")


def freezer():
    hide_canvas()
    blank_canvas = Canvas(kitchen_home, width=1000, height=1000, highlightthickness=0)
    blank_canvas.place(x=325, y=0)
    messagebox.showinfo("consumption freezer", "The annual consumption of the freezer is 220 kWh.")


def oven():
    global oven_canvas, oven_canvas2
    hide_canvas()
    oven_canvas = Canvas(kitchen_home, width=600, height=600, highlightthickness=0)
    oven_canvas.place(x=325, y=5)
    oven_canvas2 = Canvas(kitchen_home, width=400, height=400, highlightthickness=0)
    oven_canvas2.place(x=375, y=425)

    buttons(oven_canvas2, "oven")
    grafieken.make_graph(oven_canvas, "oven")


def stove():
    global stove_canvas, stove_canvas2
    hide_canvas()
    stove_canvas = Canvas(kitchen_home, width=500, height=500, highlightthickness=0)
    stove_canvas.place(x=325, y=5)
    stove_canvas2 = Canvas(kitchen_home, width=400, height=400, highlightthickness=0)
    stove_canvas2.place(x=375, y=425)

    buttons(stove_canvas2, "kookplaat")
    grafieken.make_graph(stove_canvas, "kookplaat")


def dishwasher():
    global dishwasher_canvas, dishwasher_canvas2
    hide_canvas()
    dishwasher_canvas = Canvas(kitchen_home, width=500, height=500, highlightthickness=0)
    dishwasher_canvas.place(x=325, y=5)
    dishwasher_canvas2 = Canvas(kitchen_home, width=400, height=400, highlightthickness=0)
    dishwasher_canvas2.place(x=375, y=425)

    buttons(dishwasher_canvas2, "afwasmachine")
    grafieken.make_graph(dishwasher_canvas, "afwasmachine")


#****************** Living Room **************
def livingroom_window():

    global living_home, living_bool

    living_home = Toplevel()
    living_home.title("Living Room")
    living_home.geometry("750x500+400+100")

    living_bool = True

    living_menu = Menu(living_home)
    living_home.config(menu=living_menu)

    i = 0
    j = 0
    for device in Gebruikersscherm.machines_room("living room"):
        if device == "TV":
            device_name = "TV"
            device = tv
            device_button = Button(living_home, text=device_name, command=device, width=20, height=5)
            device_button.grid(row=i, column=j)
        elif device != "TV":
            device_name = str(device)
            device_button = Button(living_home, text=device_name, command=lambda: plus_button_func(living_home, device), width=20, height=5)
            device_button.grid(row=i, column=j)
        if j == 0:
            j += 1
        else:
            j = 0
            i += 1
        if i == 4 and j == 1:
            messagebox.showwarning("warning", "You have reached the maximum number of devices for this room")

    add_commands(living_menu, living_home)
    plus_button = Button(living_home, text="+", command=lambda: get_device_name(living_home, i, j, "living room"), width=20, height=5)

    plus_button.grid(row=i, column=j)

    living_home.protocol('WM_DELETE_WINDOW', set_false_living)


#****************** livingroom machines **************
def tv():
    global tv_canvas, tv_canvas2
    hide_canvas()
    tv_canvas = Canvas(living_home, width=500, height=500, highlightthickness=0)
    tv_canvas.place(x=325, y=5)
    tv_canvas2 = Canvas(living_home, width=400, height=400, highlightthickness=0)
    tv_canvas2.place(x=375, y=425)

    buttons(tv_canvas2, "TV")
    grafieken.make_graph(tv_canvas, "TV")


# ****************** Bathroom **************
def bathroom_window():

    global bathroom_home, bathroom_bool

    bathroom_home = Toplevel()
    bathroom_home.title("Bathroom")
    bathroom_home.geometry("750x500+400+100")

    bathroom_bool = True

    bathroom_menu = Menu(bathroom_home)
    bathroom_home.config(menu=bathroom_menu)

    add_commands(bathroom_menu, bathroom_home)

    i = 0
    j = 0
    for device in Gebruikersscherm.machines_room("bathroom"):
        device_name = str(device)
        device_button = Button(bathroom_home, text=device_name, command=lambda: plus_button_func(bathroom_home, device),
                               width=20, height=5)
        device_button.grid(row=i, column=j)
        if j == 0:
            j += 1
        else:
            j = 0
            i += 1
        if i == 4 and j == 1:
            messagebox.showwarning("warning", "You have reached the maximum number of devices for this room")

    plus_button = Button(bathroom_home, text="+", command=lambda: get_device_name(bathroom_home, i, j, "bathroom"), width=20, height=5)
    plus_button.grid(row=i, column=j)

    blank_canvas = Canvas(bathroom_home, width=500, height=500, highlightthickness=0)
    blank_canvas.place(x=325, y=5)
    blank_canvas2 = Canvas(bathroom_home, width=400, height=400, highlightthickness=0)
    blank_canvas2.place(x=450, y=425)

    bathroom_home.protocol('WM_DELETE_WINDOW', set_false_bathroom)

# ****************** bathroom machines **************


# ****************** Storage **************
def storage_window():

    global storage_home, storage_bool

    storage_home = Toplevel()
    storage_home.title("Storage")
    storage_home.geometry("750x500+400+100")

    storage_bool = True

    storage_menu = Menu(storage_home)
    storage_home.config(menu=storage_menu)

    add_commands(storage_menu, storage_home)

    i = 0
    j = 0
    for device in Gebruikersscherm.machines_room("storage space"):
        if device == "boiler":
            device_name = "Boiler"
            device = boiler
            device_button = Button(storage_home, text=device_name, command=device, width=20, height=5)
            device_button.grid(row=i, column=j)
        elif device == "droogkast":
            device_name = "Tumble Dryer"
            device = tumble_dryer
            device_button = Button(storage_home, text=device_name, command=device, width=20, height=5)
            device_button.grid(row=i, column=j)
        elif device == "wasmachine":
            device_name = "Washing Machine"
            device = washing_machine
            device_button = Button(storage_home, text=device_name, command=device, width=20, height=5)
            device_button.grid(row=i, column=j)
        elif device != "droogkast" and device != "boiler" and device != "wasmachine":
            device_name = str(device)
            device_button = Button(storage_home, text=device_name, command=lambda: plus_button_func(storage_home, device), width=20, height=5)
            device_button.grid(row=i, column=j)

        if j == 0:
            j += 1
        else:
            j = 0
            i += 1
        if i == 4 and j == 1:
            messagebox.showwarning("warning", "You have reached the maximum number of devices for this room")

    plus_button = Button(storage_home, text="+", command=lambda: get_device_name(storage_home, i, j, "storage space"), width=20, height=5)

    plus_button.grid(row=i, column=j)

    storage_home.protocol('WM_DELETE_WINDOW', set_false_storage)


#****************** storage machines **************

def boiler():
    global boiler_canvas, boiler_canvas2
    hide_canvas()
    boiler_canvas = Canvas(storage_home, width=500, height=500, highlightthickness=0)
    boiler_canvas.place(x=325, y=5)
    boiler_canvas2 = Canvas(storage_home, width=400, height=400, highlightthickness=0)
    boiler_canvas2.place(x=375, y=425)

    buttons(boiler_canvas2, "boiler")
    grafieken.make_graph(boiler_canvas, "boiler")


def tumble_dryer():
    global tumble_dryer_canvas, tumble_dryer_canvas2
    hide_canvas()
    tumble_dryer_canvas = Canvas(storage_home, width=500, height=500, highlightthickness=0)
    tumble_dryer_canvas.place(x=325, y=5)
    tumble_dryer_canvas2 = Canvas(storage_home, width=400, height=400, highlightthickness=0)
    tumble_dryer_canvas2.place(x=375, y=425)

    buttons(tumble_dryer_canvas2, "droogkast")
    grafieken.make_graph(tumble_dryer_canvas, "droogkast")


def washing_machine():
    global washing_machine_canvas,washing_machine_canvas2
    hide_canvas()
    washing_machine_canvas = Canvas(storage_home, width=500, height=500, highlightthickness=0)
    washing_machine_canvas.place(x=325, y=5)
    washing_machine_canvas2 = Canvas(storage_home, width=400, height=400, highlightthickness=0)
    washing_machine_canvas2.place(x=375, y=425)

    buttons(washing_machine_canvas2, "wasmachine")
    grafieken.make_graph(washing_machine_canvas, "wasmachine")


# ****************** Bedroom **************
def bedroom_window():
    global bedroom_home, bedroom_bool

    bedroom_home = Toplevel()
    bedroom_home.title("Bedroom")
    bedroom_home.geometry("750x500+400+100")

    bedroom_bool = True

    bedroom_menu = Menu(bedroom_home)
    bedroom_home.config(menu=bedroom_menu)

    add_commands(bedroom_menu, bedroom_home)

    i = 0
    j = 0
    for device in Gebruikersscherm.machines_room("bedroom"):
        device_name = str(device)
        device_button = Button(bedroom_home, text=device_name, command=lambda: plus_button_func(bedroom_home, device), width=20, height=5)
        device_button.grid(row=i, column=j)
        if j == 0:
            j += 1
        else:
            j = 0
            i += 1
        if i == 4 and j == 1:
            messagebox.showwarning("warning", "You have reached the maximum number of devices for this room")


    plus_button = Button(bedroom_home, text="+", command= lambda: get_device_name(bedroom_home, i, j, "bedroom"), width=20, height=5)

    plus_button.grid(row=i, column=j)

    bedroom_home.protocol('WM_DELETE_WINDOW', set_false_bedroom)


# ****************** bedroom machines **************
def pc():
    global pc_canvas,pc_canvas2
    hide_canvas()
    pc_canvas = Canvas(bedroom_home, width=500, height=500, highlightthickness=0)
    pc_canvas.place(x=325, y=5)
    pc_canvas2 = Canvas(bedroom_home, width=400, height=400, highlightthickness=0)
    pc_canvas2.place(x=375, y=425)

    buttons(pc_canvas2, "PC")
    grafieken.make_graph(pc_canvas, "PC")


# ****************** Energy Supply **************

def supply_window():
    global supply_home, supply_bool

    supply_home = Toplevel()
    supply_home.title("Supply")
    supply_home.geometry("750x500+400+100")

    supply_bool = True

    supply_menu = Menu(supply_home)
    supply_home.config(menu=supply_menu)

    add_commands(supply_menu, supply_home)

    # i = 0
    # j = 0
    # for device in Gebruikersscherm.machines_room("supply"):
    #     if device == "zonnepanelen":
    #         device_name = "Solar Panels"
    #         device = solar_panels
    #     if device == "windmolen":
    #         device_name = "Windmill"
    #         device = windmill
    #     if device == "batterij":
    #         device_name = "Battery"
    #         device = battery
    #
    #     device_button = Button(supply_home, text=device_name, command=device, width=20, height=5)
    #     device_button.grid(row=i, column=j)
    #     if j == 0:
    #         j += 1
    #     else:
    #         j = 0
    #         i += 1
    #     if i == 4 and j == 1:
    #         messagebox.showwarning("warning", "You have reached the maximum number of devices for this room")

    solarpanel_button = Button(supply_home, text="Solar panels", command=solar_panels, width=20, height=5)
    windmill_button = Button(supply_home, text="Windmill", command=windmill, width=20, height=5)
    battery_button = Button(supply_home, text="Battery", command=battery, width=20, height=5)
#    plus_button = Button(supply_home, text="+", command= lambda: get_device_name(supply_home, 1, 1, "supply home"), width=20, height=5)

    solarpanel_button.grid(row=0)
    windmill_button.grid(row=0,column=1)
    battery_button.grid(row=1,column=0)
#   plus_button.grid(row=1, column=1)

#  supply_home.iconify()
    supply_home.protocol('WM_DELETE_WINDOW', set_false_supply)


# ****************** supply machines **************
def solar_panels():
    global solar_panels_canvas, solar_panels_canvas2
    hide_canvas()
    solar_panels_canvas = Canvas(supply_home, width=500, height=500, highlightthickness=0)
    solar_panels_canvas.place(x=325, y=5)
    solar_panels_canvas2 = Canvas(supply_home, width=400, height=400, highlightthickness=0)
    solar_panels_canvas2.place(x=375, y=425)

#    buttons(solar_panels_canvas2, "zonnepanelen")
    grafieken.make_graph_solar_panels(solar_panels_canvas)


def battery():
    global battery_canvas, battery_canvas2
    hide_canvas()
    battery_canvas = Canvas(supply_home, width=500, height=500, highlightthickness=0)
    battery_canvas.place(x=325, y=5)
    battery_canvas2 = Canvas(supply_home, width=400, height=400, highlightthickness=0)
    battery_canvas2.place(x=375, y=425)


def windmill():
    global windmill_canvas, windmill_canvas2
    hide_canvas()
    windmill_canvas = Canvas(supply_home, width=500, height=500, highlightthickness=0)
    windmill_canvas.place(x=325, y=5)
    windmill_canvas2 = Canvas(supply_home, width=400, height=400, highlightthickness=0)
    windmill_canvas2.place(x=375, y=425)

    grafieken.make_graph_windmill(windmill_canvas)


# ********************** Homescreen**************
def home():

    global home_root, time2, mFrame, watch, home_menu, home_canvas, temp_text, name_text_update, date
    home_root = Toplevel()
    home_root.title("Home")
    home_root.geometry("1100x650+200+0")

    home_canvas = Canvas(home_root, width=1220, height=770, highlightthickness=0)
    home_canvas.place(x=0, y=0)
    home_menu = Menu(home_root)
    home_root.config(menu=home_menu)

    photo = PhotoImage(file=r"C:\Users\Helena\Pictures\x.gif")
    home_canvas.image = photo
    home_canvas.create_image(0,0, image = photo)
    name_text = str(login) + ' family'
    home_canvas.create_text(200, 220, fill="white", font='Courier, 50', text="Welcome,")
    name_text_update = home_canvas.create_text(200, 300, fill="white", font='Courier, 30', text=name_text)
    date = home_canvas.create_text(1010, 650, fill="white", font='Courier, 20', text=Klok.full_datetime_now())
    circle = home_canvas.create_oval(700, 150, 950, 400, outline="white", width=5)

    plus_canvas = Canvas(home_root, width=70, height=70, highlightthickness=0)
    plus_canvas.place(x=650, y=360)
    plus_canvas.create_image(0,0, image=photo)
    plus_square = plus_canvas.create_rectangle(2.5, 2.5, 67.5, 67.5, outline="white", width =5)
    plus_text= plus_canvas.create_text(35, 35, fill="white", font='Courier, 30', text="+")
    plus_canvas.bind("<Button-1>", temp_plus)

    minus_canvas = Canvas(home_root, width=70, height=70, highlightthickness=0)
    minus_canvas.place(x=930, y=360)
    minus_canvas.create_image(0,0, image = photo)
    minus_square = minus_canvas.create_rectangle(2.5,2.5,67.5,67.5, outline="white", width =5)
    minus_text= minus_canvas.create_text(35,35, fill="white", font=('Courier, 40'), text= "-")
    minus_canvas.bind("<Button-1>", temp_minus)

    lighting_button = Button(home_root, text="Lighting", command=lighting, width=20, height=3)
    lighting_button.config(bg="white")
    lighting_button.place(x=50, y=440)

    logout_button = Button(home_root, text="Logout", command=logout, width=20, height=3)
    logout_button.config(bg="white")
    logout_button.place(x=50, y=560)

    daily_schedule_button = Button(home_root, text="Daily Schedule", command=daily_schedule, width=20, height=3)
    daily_schedule_button.config(bg="white")
    daily_schedule_button.place(x=50, y=500)

    total_usage_button = Button(home_root, text="Total usage", command=grafieken.make_graph_total, width=20, height=3)
    total_usage_button.config(bg="white")
    total_usage_button.place(x=50, y=380)

    adjust_temperature_button = Button(home_root, text="Temperature schedule",
                                       command=Temperature_schedule.temperature_schedule, width=25, height=3)
    adjust_temperature_button.place(x=733, y=420)

    temp_text = home_canvas.create_text(790, 275, fill="white", font='Courier, 50', text=read_inside_temperature)
    home_canvas.create_text(865, 275, fill="white", font='Courier, 50', text="°C")
    add_commands(home_menu, home_root)
    update_temp()

    home_root.protocol('WM_DELETE_WINDOW', close_all)


# ******************************SETTINGS****************************
def settings_window():

    global settings_home, new_name_entry, password_entry1, password_entry2, new_pass_entry, settings_bool

    settings_home = Toplevel()
    settings_home.title("Settings")
    settings_home.geometry("1000x600+150+100")

    settings_bool = True

    settings_menu = Menu(settings_home)
    settings_home.config(menu=settings_menu)

    add_commands(settings_menu, settings_home)

    profile_label = Label(settings_home, text="Profile settings:")
    profile_label.config(font=('Courier', 25))
    profile_label.place(x=10, y=10)

    house_label = Label(settings_home, text="House settings:")
    house_label.config(font=('Courier', 25))
    house_label.place(x=450, y=10)

    # ************** Change name ******************

    change_name_label = Label(settings_home, text="Change name:")
    change_name_label.config(font=('Courier', 23))
    change_name_label.place(x=60, y=60)

    new_name_label = Label(settings_home, text="New name?")
    new_name_label.config(font=('Courier', 15))
    new_name_label.place(x=130, y=100)

    new_name_entry = Entry(settings_home, width=40)
    new_name_entry.place(x=110, y=130)

    password_label1 = Label(settings_home, text="Password?")
    password_label1.config(font=('Courier', 15))
    password_label1.place(x=130, y=150)

    password_entry1 = Entry(settings_home, show='*', width=40)
    password_entry1.place(x=110, y=180)

    save_name_button = Button(settings_home, text="Save",
                              command=lambda: change_name(new_name_entry.get(), password_entry1.get()), width=6,
                              height=2)
    save_name_button.place(x=130, y=210)

    # ************************change pass**************

    change_pass_label = Label(settings_home, text="Change password:")
    change_pass_label.config(font=('Courier', 23))
    change_pass_label.place(x=60, y=250)

    new_pass_label = Label(settings_home, text="New password?")
    new_pass_label.config(font=('Courier', 15))
    new_pass_label.place(x=130, y=290)

    new_pass_entry = Entry(settings_home, width=40)
    new_pass_entry.place(x=110, y=320)

    password_label2 = Label(settings_home, text="Old password?")
    password_label2.config(font=('Courier', 15))
    password_label2.place(x=130, y=340)

    password_entry2 = Entry(settings_home, show='*', width=40)
    password_entry2.place(x=110, y=370)

    save_pass_button = Button(settings_home, text="Save",
                              command=lambda: change_pass(new_pass_entry.get(), password_entry2.get()), width=6,
                              height=2)
    save_pass_button.place(x=130, y=400)

    # ******************************** House settings ************************

    solar_area_label1 = Label(settings_home, text="What is the total surface area")
    solar_area_label2 = Label(settings_home, text="of the solar panels?:")
    solar_area_label3 = Label(settings_home, text="m²")

    solar_area_label1.config(font=('Courier', 15))
    solar_area_label1.place(x=500, y=60)
    solar_area_label2.config(font=('Courier', 15))
    solar_area_label2.place(x=500, y=90)
    solar_area_label3.config(font=('Courier', 15))
    solar_area_label3.place(x=660, y=120)

    solar_area_entry = Entry(settings_home, width=20)
    solar_area_entry.insert(0, Gebruikersscherm.surface_solar_panels())
    solar_area_entry.place(x=520, y=125)

    save_solar_area_button = Button(settings_home, text="✓",
                                    command=lambda: [
                                        Gebruikersscherm.set_surface_solar_panels(solar_area_entry.get()),
                                        show_message(solar_area_entry.get())], width=3,
                                    height=1)
    save_solar_area_button.place(x=710, y=120)

    solar_eff_label = Label(settings_home, text="What is their efficiency?")
    solar_eff_label.config(font=('Courier', 15))
    solar_eff_label.place(x=500, y=150)

    solar_eff_label2 = Label(settings_home, text="%")
    solar_eff_label2.config(font=('Courier', 15))
    solar_eff_label2.place(x=660, y=180)

    solar_eff_entry = Entry(settings_home, width=20)
    solar_eff_entry.insert(0, Gebruikersscherm.efficiency_solar_panels())
    solar_eff_entry.place(x=520, y=185)

    save_solar_area_button = Button(settings_home, text="✓",
                                    command=lambda: [
                                        Gebruikersscherm.set_efficiency_solar_panels(solar_eff_entry.get()),
                                        show_message(solar_eff_entry.get())],
                                    width=3,
                                    height=1)
    save_solar_area_button.place(x=710, y=180)

    blade_length_label = Label(settings_home, text="How long are the windmill's blades?")
    blade_length_label.config(font=('Courier', 15))
    blade_length_label.place(x=500, y=210)

    blade_length_label2 = Label(settings_home, text="m")
    blade_length_label2.config(font=('Courier', 15))
    blade_length_label2.place(x=660, y=240)

    blade_length_entry = Entry(settings_home, width=20)
    blade_length_entry.insert(0, Gebruikersscherm.blade_length())
    blade_length_entry.place(x=520, y=245)

    save_blade_length_button = Button(settings_home, text="✓",
                                      command=lambda: [Gebruikersscherm.set_blade_length(blade_length_entry.get()),
                                                       show_message(blade_length_entry.get())],
                                      width=3,
                                      height=1)
    save_blade_length_button.place(x=710, y=240)

    wind_eff_label = Label(settings_home, text="What is the efficiency of the windmill?")
    wind_eff_label.config(font=('Courier', 15))
    wind_eff_label.place(x=500, y=270)

    wind_eff_label2 = Label(settings_home, text="%")
    wind_eff_label2.config(font=('Courier', 15))
    wind_eff_label2.place(x=660, y=300)

    wind_eff_entry = Entry(settings_home, width=20)
    wind_eff_entry.insert(0, Gebruikersscherm.efficiency_windmill())
    wind_eff_entry.place(x=520, y=305)

    save_wind_eff_button = Button(settings_home, text="✓",
                                  command=lambda: [Gebruikersscherm.set_efficiency_windmill(wind_eff_entry.get()),
                                                   show_message(wind_eff_entry.get())],
                                  width=3,
                                  height=1)
    save_wind_eff_button.place(x=710, y=300)

    charge_speed_label = Label(settings_home, text="What is the battery charge speed?")
    charge_speed_label.config(font=('Courier', 15))
    charge_speed_label.place(x=500, y=330)

    charge_speed_label2 = Label(settings_home, text="kWh")
    charge_speed_label2.config(font=('Courier', 15))
    charge_speed_label2.place(x=660, y=360)

    charge_speed_entry = Entry(settings_home, width=20)
    charge_speed_entry.insert(0, Gebruikersscherm.charging_speed_bat())
    charge_speed_entry.place(x=520, y=365)

    save_charge_speed_button = Button(settings_home, text="✓",
                                      command=lambda: [
                                          Gebruikersscherm.set_charging_speed_bat(charge_speed_entry.get()),
                                          show_message(charge_speed_entry.get())],
                                      width=3,
                                      height=1)
    save_charge_speed_button.place(x=710, y=360)

    discharge_speed_label = Label(settings_home, text="What is the battery discharge speed?")
    discharge_speed_label.config(font=('Courier', 15))
    discharge_speed_label.place(x=500, y=390)

    discharge_speed_label2 = Label(settings_home, text="kWh")
    discharge_speed_label2.config(font=('Courier', 15))
    discharge_speed_label2.place(x=660, y=420)

    discharge_speed_entry = Entry(settings_home, width=20)
    discharge_speed_entry.insert(0, Gebruikersscherm.discharging_speed_bat())
    discharge_speed_entry.place(x=520, y=425)

    save_discharge_speed_button = Button(settings_home, text="✓",
                                         command=lambda: [Gebruikersscherm.set_discharging_speed_bat(
                                             discharge_speed_entry.get()),
                                                          show_message(discharge_speed_entry.get())],
                                         width=3,
                                         height=1)
    save_discharge_speed_button.place(x=710, y=420)

    batt_capacity_label = Label(settings_home, text="What is the battery capacity?")
    batt_capacity_label.config(font=('Courier', 15))
    batt_capacity_label.place(x=500, y=450)

    batt_capacity_label2 = Label(settings_home, text="kWA")
    batt_capacity_label2.config(font=('Courier', 15))
    batt_capacity_label2.place(x=660, y=480)

    batt_capacity_entry = Entry(settings_home, width=20)
    batt_capacity_entry.insert(0, Gebruikersscherm.capacity_bat())
    batt_capacity_entry.place(x=520, y=485)

    save_batt_capacity_button = Button(settings_home, text="✓",
                                       command=lambda: [Gebruikersscherm.set_capacity_bat(
                                           batt_capacity_entry.get()), show_message(batt_capacity_entry.get())],
                                       width=3,
                                       height=1)
    save_batt_capacity_button.place(x=710, y=480)


def change_name(new_name, given_password):

    family_name = Gebruikersscherm.family_name()

    if str(given_password) == str(password):
        Gebruikersscherm.change_family(family_name, new_name, password)
        dt.user.print_table()
        messagebox.showinfo("Confirmation", "New name succesfully saved!")
        new_name_entry.delete(0, 'end')
        password_entry1.delete(0, 'end')
        home_canvas.itemconfig(name_text_update, text = new_name + " family")

    else:
        messagebox.showerror("Error", "Wrong password, try again!")
        new_name_entry.delete(0, 'end')
        password_entry1.delete(0, 'end')


def change_pass(new_password, old_password):

    family_name = Gebruikersscherm.family_name()
    login_name = Gebruikersscherm.family()[0]
    password = Gebruikersscherm.family()[1]

    if str(old_password) == str(password):
        Gebruikersscherm.change_family(family_name, login_name, new_password)
        dt.user.print_table()
        messagebox.showinfo("Confirmation", "New password succesfully saved!")

    else:
        messagebox.showerror("Error", "Wrong password, try again!")

    new_pass_entry.delete(0, 'end')
    password_entry2.delete(0, 'end')


def show_message(input):

    if input.replace(".", "").isdigit():
        messagebox.showinfo("Confirmation", "Succesfully saved!")

    else:
        messagebox.showerror("Error", "Given input is not a number")


# ******************* Login Screen *********************
def click_next():
    global login, password
    login, password = 0, 0
    login, password = Gebruikersscherm.family()
    if str(entry_name.get()) == login and str(entry_pass.get()) == password:
        driving_time_today()
        home()
        root.withdraw()

    else:
        messagebox.showerror("Error", "Wrong combination, try again!")


frame_1 = Frame(root, width=500, height=400, bd=10, relief=GROOVE)
frame_1.place(x=125, y=50)

label_name = Label(frame_1, text="Name")
label_pass = Label(frame_1, text="Password")
entry_name = Entry(frame_1, width=40)
entry_pass = Entry(frame_1, show='*', width=40)

label_name.config(font=('Courier', 20))
label_pass.config(font=('Courier', 20))

label_name.place(x=100, y=100)
label_pass.place(x=40, y=150)
entry_name.place(x=200, y=110)
entry_pass.place(x=200, y=160)

next_button = Button(frame_1, text="Next", command=click_next, width=10, height=2)
next_button.config(relief=RAISED, font=('Courier', 10))
next_button.place(x=195, y=230)

center(root, 100)

root.mainloop()