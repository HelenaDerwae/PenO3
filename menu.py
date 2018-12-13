from tkinter import *

def add_commands(room_menu, window):

    room_menu.add_command(label="Home", command= window.destroy )
    room_menu.add_command(label="Kitchen", command=kitchen_window)
    room_menu.add_command(label="Living Room", command=livingroom_window)
    room_menu.add_command(label="Bathroom", command=bathroom_window)
    room_menu.add_command(label="Bedroom", command=bedroom_window)
    room_menu.add_command(label="Garage", command=garage_window)
    room_menu.add_command(label="Energy Supply", command=supply_window)