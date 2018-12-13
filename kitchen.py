from tkinter import *

from menu import add_commands
# *****************************KITCHEN***************************
def kitchen_window():

    global kitchen_home

    kitchen_home = Toplevel()
    kitchen_home.title("Kitchen")
    kitchen_home.geometry("750x500+400+100")
    #window(kitchen_home)

    kitchen_menu = Menu(kitchen_home)
    kitchen_home.config(menu=kitchen_menu)

    add_commands(kitchen_menu, kitchen_home)

    oven_button = Button(kitchen_home, text="Oven", command=donothing, width=20, height=5)
    fridge_button = Button(kitchen_home, text="Refrigerator", command=donothing, width=20, height=5)
    freezer_button = Button(kitchen_home, text="Freezer", command=donothing, width=20, height=5)
    stove_button = Button(kitchen_home, text="Stove", command=donothing, width=20, height=5)
    dishwasher_button = Button(kitchen_home, text="Dishwasher", command=donothing, width=20, height=5)
    plus_button = Button(kitchen_home, text="+", command= lambda: get_device_name(kitchen_home, 2, 1), width=20, height=5)

    oven_button.grid( row=0)
    fridge_button.grid( row=1)
    freezer_button.grid( row=2)
    stove_button.grid( row=0, column=1)
    dishwasher_button.grid( row=1, column=1)
    plus_button.grid( row=2, column=1)
