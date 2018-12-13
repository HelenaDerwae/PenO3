from tkinter import *
import Gebruikersscherm
import Data_tables as dt
#import datetime


def donothing():
    return


def set_false_schedule():
    global daily_schedule_bool
    schedule_home.destroy()
    daily_schedule_bool = False


def daily_schedule():

    global schedule_home, weekday_schedule, entry_kitchenh, entry_washing_machine_untilh, entry_washing_machineh, \
        entry_tumble_dryer_untilh, entry_tumble_dryerh, entry_pc_untilh, entry_pch, entry_livingroom_untilh, \
        entry_livingroomh, entry_kitchen_untilh, entry_boiler_untilh, \
        entry_boilerh, entry_battery_untilh, entry_batteryh, hours_list, last_label, plus_button, daily_schedule_bool

    schedule_home = Tk()
    schedule_home.title("Daily Schedule")
    schedule_home.geometry("750x650+400+100")

    schedule_bool = True

    ask_label = Label(schedule_home, text="When would you like to use following machines?")
    kitchen_label = Label(schedule_home, text="Kitchen")
    washing_machine_label = Label(schedule_home, text="washing machine")
    livingroom_label = Label(schedule_home, text="tv")
    boiler_label = Label(schedule_home, text="boiler")
    pc_label = Label(schedule_home, text="pc")
    battery_label = Label(schedule_home, text="battery")
    tumble_dryer_label = Label(schedule_home, text="tumble dryer")

    entry_kitchenh = Entry(schedule_home, width=5)
    entry_washing_machineh = Entry(schedule_home, width=5)
    entry_livingroomh = Entry(schedule_home, width=5)
    entry_boilerh = Entry(schedule_home, width=5)
    entry_pch = Entry(schedule_home, width=5)
    entry_batteryh = Entry(schedule_home, width=5)
    entry_tumble_dryerh = Entry(schedule_home, width=5)

    entry_kitchenm = Entry(schedule_home, width=5)
    entry_washing_machinem = Entry(schedule_home, width=5)
    entry_livingroomm = Entry(schedule_home, width=5)
    entry_boilerm = Entry(schedule_home, width=5)
    entry_pcm = Entry(schedule_home, width=5)
    entry_batterym = Entry(schedule_home, width=5)
    entry_tumble_dryerm = Entry(schedule_home, width=5)

    entry_kitchen_untilh = Entry(schedule_home, width=5)
    entry_washing_machine_untilh = Entry(schedule_home, width=5)
    entry_livingroom_untilh = Entry(schedule_home, width=5)
    entry_boiler_untilh= Entry(schedule_home, width=5)
    entry_pc_untilh = Entry(schedule_home, width=5)
    entry_battery_untilh = Entry(schedule_home, width=5)
    entry_tumble_dryer_untilh = Entry(schedule_home, width=5)

    entry_kitchen_untilm = Entry(schedule_home, width=5)
    entry_washing_machine_untilm = Entry(schedule_home, width=5)
    entry_livingroom_untilm = Entry(schedule_home, width=5)
    entry_boiler_untilm = Entry(schedule_home, width=5)
    entry_pc_untilm = Entry(schedule_home, width=5)
    entry_battery_untilm = Entry(schedule_home, width=5)
    entry_tumble_dryer_untilm = Entry(schedule_home, width=5)

    ask_label.config(font=('Courier', 10))
    kitchen_label.config(font=('Courier', 10))
    washing_machine_label.config(font=('Courier', 10))
    livingroom_label.config(font=('Courier', 10))
    boiler_label.config(font=('Courier', 10))
    pc_label.config(font=('Courier', 10))
    battery_label.config(font=('Courier', 10))
    tumble_dryer_label.config(font=('Courier', 10))

    ask_label.place(x=40, y=20)
    kitchen_label.place(x=40, y= 100)
    washing_machine_label.place(x=40, y=130)
    livingroom_label.place(x=40, y=160)
    boiler_label.place(x=40, y=190)
    pc_label.place(x=40, y=220)
    battery_label.place(x=40, y=250)
    tumble_dryer_label.place(x=40, y=280)
    last_label = 280

    entry_kitchenh.place(x=200, y=100)
    entry_washing_machineh.place(x=200, y=130)
    entry_livingroomh.place(x=200, y=160)
    entry_boilerh.place(x=200, y=190)
    entry_pch.place(x=200, y=220)
    entry_batteryh.place(x=200, y=250)
    entry_tumble_dryerh.place(x=200, y=280)

    entry_kitchenm.place(x=260, y=100)
    entry_washing_machinem.place(x=260, y=130)
    entry_livingroomm.place(x=260, y=160)
    entry_boilerm.place(x=260, y=190)
    entry_pcm.place(x=260, y=220)
    entry_batterym.place(x=260, y=250)
    entry_tumble_dryerm.place(x=260, y=280)

    entry_kitchen_untilh.place(x=340, y=100)
    entry_washing_machine_untilh.place(x=340, y=130)
    entry_livingroom_untilh.place(x=340, y=160)
    entry_boiler_untilh.place(x=340, y=190)
    entry_pc_untilh.place(x=340, y=220)
    entry_battery_untilh.place(x=340, y=250)
    entry_tumble_dryer_untilh.place(x=340, y=280)

    entry_kitchen_untilm.place(x=400, y=100)
    entry_washing_machine_untilm.place(x=400, y=130)
    entry_livingroom_untilm.place(x=400, y=160)
    entry_boiler_untilm.place(x=400, y=190)
    entry_pc_untilm.place(x=400, y=220)
    entry_battery_untilm.place(x=400, y=250)
    entry_tumble_dryer_untilm.place(x=400, y=280)

    from_label = Label(schedule_home, text="From")
    to_label = Label(schedule_home, text="To")
    hours1_label = Label(schedule_home, text="hours")
    minutes1_label = Label(schedule_home, text="minutes")
    hours2_label = Label(schedule_home, text="hours")
    minutes2_label = Label(schedule_home, text="minutes")

    from_label.place(x=230, y=50)
    to_label.place(x=380, y=50)
    hours1_label.place(x=200, y=70)
    minutes1_label.place(x=260, y=70)
    hours2_label.place(x=340, y=70)
    minutes2_label.place(x=400, y=70)

    enter_button = Button(schedule_home, text="Enter for tomorrow", command=getManual, width=20, height=2)
    enter_button.config(relief=RAISED, font=('Courier', 10))
    enter_button.place(x=500, y=70)

    weekday_button = Button(schedule_home, text="Set as default weekday", command=getWeek, width=30, height=2)
    weekday_button.config(relief=RAISED, font=('Courier', 10))
    weekday_button.place(x=490, y=160)

    weekend_button = Button(schedule_home, text="Set as default weekendday",command=getWeekend, width=30, height=2)
    weekend_button.config(relief=RAISED, font=('Courier', 10))
    weekend_button.place(x=490, y=250)

    plus_button = Button(schedule_home, text="+", command=lambda: plus_button_get_name(last_label, plus_button), width=3, height=1)
    plus_button.config(relief=RAISED, font=('Courier', 10))
    plus_button.place(x=40, y=last_label+50)
    last_label += 30

    schedule_home.protocol('WM_DELETE_WINDOW', set_false_schedule)


def plus_button_get_name(y, button):
    global device_entry, entry_box
    entry_box = Toplevel()
    entry_box.title("Add device")
    entry_box.geometry("200x100+400+300")

    device_label = Label(entry_box, text="What is the name of your device?")
    device_label.grid(row=0, column=1)
    device_entry = Entry(entry_box)
    device_entry.grid(row=1, column=1)

    ok_button = Button(entry_box, text="Ok", command=lambda: plus(y, button))
    ok_button.grid(row=2, column=1)


def plus(y, button):
    global new_device_name, plus_entryh, plus_entry_untilh
    new_device_name = device_entry.get()
    entry_box.destroy()
    button.destroy()

    plus_label = Label(schedule_home, text=str(new_device_name))
    plus_label.config(font=('Courier', 10))
    plus_label.place(x=40, y=y)

    plus_entryh = Entry(schedule_home, width=5)
    plus_entrym = Entry(schedule_home, width=5)
    plus_entry_untilh = Entry(schedule_home, width=5)
    plus_entry_untilm = Entry(schedule_home, width=5)

    plus_entryh.place(x=200, y=y)
    plus_entrym.place(x=260, y=y)
    plus_entry_untilh.place(x=340, y=y)
    plus_entry_untilm.place(x=400, y=y)

    add_manual_button = Button(schedule_home, text="add manual", command=lambda:add_manual("plus"), width=10, height=1)
    add_manual_button.place(x=460, y=y)

    add_week_button = Button(schedule_home, text="add week", command=lambda: add_week("plus"), width=10, height=1)
    add_week_button.place(x=550, y=y)

    add_weekend_button = Button(schedule_home, text="add weekend", command=lambda: add_weekend("plus"), width=10,
                                height=1)
    add_weekend_button.place(x=640, y=y)

    y += 30

    if y < 600:
        new_button = Button(schedule_home, text="+", command=lambda: plus_button_get_name(y, new_button), width=3,
                            height=1)
        new_button.config(relief=RAISED, font=('Courier', 10))
        new_button.place(x=40, y=y)


def getschedule():
    global weekday_schedule, hours_list
    wrong_number = False
    hours_list = [entry_kitchenh.get(), entry_washing_machine_untilh.get(), entry_washing_machineh.get(),
        entry_tumble_dryer_untilh.get(), entry_tumble_dryerh.get(), entry_pc_untilh.get(), entry_pch.get(),
        entry_livingroom_untilh.get(), entry_livingroomh.get(),
        entry_kitchen_untilh.get(), entry_boiler_untilh.get(), entry_boilerh.get(), entry_battery_untilh.get(),
                  entry_batteryh.get()]
    for i in hours_list:
        if not i.replace(".", "").isdigit():
            messagebox.showerror("Error", "Please enter a valid number.")
            wrong_number = True
            break
        elif i == '':
            messagebox.showerror("Error", "Please fill in for every machine.")
            wrong_number = True
            break
        elif int(i) > 23 or int(i) < 00:
            messagebox.showerror("Error", "Please enter a number between 00 and 23.")
            wrong_number = True
            break
    if ((entry_kitchenh.get() == entry_kitchen_untilh.get())
        or (entry_livingroomh.get() == entry_livingroom_untilh.get()) or (
                entry_boilerh.get() == entry_boiler_untilh.get())
        or (entry_boilerh.get() == entry_boiler_untilh.get()) or (entry_pch.get() == entry_pc_untilh.get())
        or (entry_tumble_dryerh.get() == entry_tumble_dryer_untilh.get()) or (
                entry_washing_machineh.get() == entry_washing_machine_untilh.get())
        or (entry_batteryh.get() == entry_battery_untilh.get())):
        messagebox.showerror("Error", "Start hour can not be the same as end hour.")
    if ((entry_kitchenh.get() < entry_kitchen_untilh.get())
        or (entry_livingroomh.get() < entry_livingroom_untilh.get()) or (
                entry_boilerh.get() < entry_boiler_untilh.get())
        or (entry_boilerh.get() < entry_boiler_untilh.get()) or (entry_pch.get() == entry_pc_untilh.get())
        or (entry_tumble_dryerh.get() < entry_tumble_dryer_untilh.get()) or (
                entry_washing_machineh.get() < entry_washing_machine_untilh.get())
        or (entry_batteryh.get() < entry_battery_untilh.get())):
        messagebox.showerror("Error", "Start hour can not be a higher number than the end hour.")
    elif wrong_number != True:
        weekday_schedule = []
        weekday_schedule.append(["kitchen", int(entry_kitchenh.get()) + 1, int(entry_kitchen_untilh.get()) + 1])
        weekday_schedule.append(["livingroom", int(entry_livingroomh.get()) + 1, int(entry_livingroom_untilh.get()) + 1])
        weekday_schedule.append(["boiler", int(entry_boilerh.get()) + 1, int(entry_boiler_untilh.get()) + 1])
        weekday_schedule.append(["pc", int(entry_pch.get()) + 1, int(entry_pc_untilh.get()) + 1])
        weekday_schedule.append(
            ["tumble_dryer", int(entry_tumble_dryerh.get()) + 1, int(entry_tumble_dryer_untilh.get()) + 1])
        weekday_schedule.append(["washing_machine", int(entry_washing_machineh.get()) + 1,
                                 int(entry_washing_machine_untilh.get()) + 1])
        weekday_schedule.append(["battery", int(entry_batteryh.get()) + 1, int(entry_battery_untilh.get()) + 1])
        return weekday_schedule



def check_entry(button):
    if(plus_entryh.get() == '') or (plus_entry_untilh.get() == ''):
        if button == "plus":
            messagebox.showerror("Error", "Please fill in every field.")
        else:
            messagebox.showerror("Error", "Please fill in for every machine.")
        return False
    elif int(plus_entryh.get()) < 0 or int(plus_entryh.get()) > 23 or int(plus_entry_untilh.get()) < 0 or \
            int(plus_entry_untilh.get()) > 23:
        messagebox.showerror("Error", "Please enter a number between 00 and 23.")
        return False
    elif plus_entryh.get() == plus_entry_untilh.get():
        messagebox.showerror("Error", "Start hour can not be the same as end hour.")
    else:
        return True


def add_manual(button):
    if check_entry(button):
        new_schedule = [[str(new_device_name), int(plus_entryh.get()) + 1, int(plus_entry_untilh.get()) + 1]]
        Gebruikersscherm.change_machines_manual(new_schedule)
        Gebruikersscherm.set_manual_date_machines()


def add_week(button):
    if check_entry(button):
        new_schedule = [[str(new_device_name), int(plus_entryh.get()) + 1, int(plus_entry_untilh.get()) + 1]]
        Gebruikersscherm.change_machines_week(new_schedule)


def add_weekend(button):
    if check_entry(button):
        new_schedule = [[str(new_device_name), int(plus_entryh.get()) + 1, int(plus_entry_untilh.get()) + 1]]
        Gebruikersscherm.change_machines_weekend(new_schedule)


def getManual():
    if getschedule() is None:
        return
    else:
        Gebruikersscherm.change_machines_manual(getschedule())
        Gebruikersscherm.set_manual_date_machines()


def getWeek():
    if getschedule() is None:
        return
    else:
        Gebruikersscherm.change_machines_week(getschedule())


def getWeekend():
    if getschedule() is None:
        return
    else:
        Gebruikersscherm.change_machines_weekend(getschedule())