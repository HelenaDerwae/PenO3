from tkinter import *
import Data_tables as dt
import matplotlib
import Klok
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
import Gebruikersscherm
import matplotlib.pyplot as plt
import Optimalisatie

hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
now = Klok.date_now()



devices = ["oven", "afwasmachine", "TV", "multimedia_systeem", "boiler",
        "droogkast", "wasmachine", "lichten_slaapkamer","PC", "vriezer", "koelkast", "kookplaat"]



def data_device(device):
    global usage, on
    usage = Gebruikersscherm.usage(device)
    on = Gebruikersscherm.plot_day_output(device)
    if on is None:
        messagebox.showinfo("info", "Usage is being calculated")
    for i in range(len(on)):
        on[i] = on[i]*usage
    return on


def make_graph(canvas2, device):
    data_device(device)
    f = matplotlib.figure.Figure((4, 4), dpi=100)
    a = f.add_subplot(111)
#    a.plot([0, 1, 2, 3, 4, 5, 6], [0, 0, 0, 1, 1, 0,1])  # vectoren van uren en verbruik, matrix van nullen en enen nog vermenigvuldigen met verbruik
    a.plot(hours, on)
    a.set_xlabel("time (h)")
    a.set_ylabel("usage (kWh)")
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(f, canvas2)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=TRUE)


def make_graph_plus(canvas2):
    f = matplotlib.figure.Figure((4, 4), dpi=100)
    on = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    for i in range(len(on)):
        on[i] = on[i]*525
    a = f.add_subplot(111)
    a.plot(hours, on)
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(f, canvas2)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)
    toolbar = NavigationToolbar2Tk(canvas, canvas2)
    toolbar.update()
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=TRUE)


def make_graph_total():
    global usage, on
    usage = Gebruikersscherm.total_usage()
    price = Optimalisatie.electricity_price()
    fig, ax = plt.subplots()
    if (hours is None) or (usage is None):
        messagebox.showinfo("Info", "Usage is being calculated")
    else:
        ax.plot(hours, usage)
        ax.set_xlabel("time (h)")
        ax.set_ylabel("usage (kWh)")
        plt.title("Total Usage")
        plt.plot(price)
        plt.show()
        graph()


def make_graph_solar_panels(canvas2):
    on = Gebruikersscherm.plot_solar_panels()
    if on is None:
        none_label = Label(canvas2, text="making graph")
        none_label.place()
    else:
        f = matplotlib.figure.Figure((4, 4), dpi=100)
        a = f.add_subplot(111)

        a.plot(hours, on)
        a.set_xlabel("time (h)")
        a.set_ylabel("usage (kWh)")
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(f, canvas2)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=TRUE)


def make_graph_windmill(canvas2):
    on = Gebruikersscherm.plot_windmill()
    if on is None:
        none_label = Label(canvas2, text="making graph")
        none_label.place()
    else:
        f = matplotlib.figure.Figure((4, 4), dpi=100)
        a = f.add_subplot(111)

        a.plot(hours, on)
        a.set_xlabel("time (h)")
        a.set_ylabel("usage (kWh)")
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(f, canvas2)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=TRUE)