def lighting():
    global lights_canvas, lights_root, text_list, room_list_database

    lights_root = Toplevel()
    lights_root.title("Lighting")
    lights_root.geometry("900x500")

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


def update_lights(i):
    lights_canvas.itemconfigure(text_list[i], text=Gebruikersscherm.light(room_list_database[i]))