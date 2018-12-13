import Data_tables as dt
import datetime
import Klok as kl


# -------------CAR-----------------
def set_manual_date_car(date):
    """
    Sets the date when the user wants a manual car schedule to manual.
    """
    dt.manual.update_variable('car_schedule', date)


def manual_date_car():
    """
    Returns the date when de user has set a manual machine schedule.
    """
    date = dt.manual.read_variable('car_schedule')
    return date


def set_car(name, range, capacity, duration):
    """
    Creates a new car. There is place for only one car.
    Variable range gives the range of the car and capacity is the battery capacity of the car.
    """
    dt.car.update_variable('name_car', name)
    dt.car.update_variable('range_car', range)
    dt.car.update_variable('capacity_car', capacity)
    dt.car.update_variable('duration_car', duration)
    dt.car.update_variable('updated', '0')
    dt.car.update_variable('distance_car', '0')
    dt.car.update_variable('start_time_week', '0')
    dt.car.update_variable('stop_time_week', '0')
    dt.car.update_variable('start_time_weekend', '0')
    dt.car.update_variable('stop_time_weekend', '0')
    dt.car.update_variable('start_time_manual', '0')
    dt.car.update_variable('stop_time_manual', '0')


def delete_car():
    """
    Deletes the existing car.
    """
    dt.car.update_variable('name_car', '0')
    dt.car.update_variable('range_car', '0')
    dt.car.update_variable('capacity_car', '0')
    dt.car.update_variable('duration_car', '0')
    dt.car.update_variable('updated', '0')
    dt.car.update_variable('distance_car', '0')
    dt.car.update_variable('start_time_week', '0')
    dt.car.update_variable('stop_time_week', '0')
    dt.car.update_variable('start_time_weekend', '0')
    dt.car.update_variable('stop_time_weekend', '0')
    dt.car.update_variable('start_time_manual', '0')
    dt.car.update_variable('stop_time_manual', '0')


def change_car_week(car):
    """
    Changes the standard schedule of the car in a week day.
    Car must be a list: start_time and stop_time.
    """
    start_time = car[0]
    stop_time = car[1]
    dt.car.update_variable('start_time_week', start_time)
    dt.car.update_variable('stop_time_week', stop_time)


def change_car_weekend(car):
    """
    Changes the standard schedule of the car in a weekend day.
    Car must be a list: start_time and stop_time.
    """
    start_time = car[0]
    stop_time = car[1]
    dt.car.update_variable('start_time_weekend', start_time)
    dt.car.update_variable('stop_time_weekend', stop_time)


def change_car_manual(car):
    """
    Changes the manual standard schedule of the car.
    Car must be a list: start_time and stop_time.
    """
    start_time = car[0]
    stop_time = car[1]
    dt.car.update_variable('start_time_manual', start_time)
    dt.car.update_variable('stop_time_manual', stop_time)


def existing_car():
    """
    Returns the name of the car. If there is no car, returns None.
    """
    if dt.car.read_variable('name_car') == 0:
        return None
    else:
        return dt.car.read_variable('name_car')


def set_distance(distance):
    """
    Sets the distance of the car. The distance must be updated every day.
    """
    date = kl.date_now()
    if isinstance(distance, int) or distance.replace('.','').isdigit() is True:
        dt.car.update_variable('updated', date)
        dt.car.update_variable('distance_car', distance)


def updated_distance():
    """
    Returns True if distance is updated for the given day.
    False if it isn't been inserted.
    """
    date = kl.date_now()
    updated = dt.car.read_variable('updated')

    if updated == date:
        return True
    else:
        return False


# -------------USER-----------------
def family_name():
    """
    Returns the family name.
    """
    name = dt.user.read_variable('family')
    return name


def change_family(name, login, password):
    """
    Creates a new user.
    """
    dt.user.update_variable('family', name)
    dt.user.update_variable('login', login)
    dt.user.update_variable('password', password)


def family():
    """
    Gives login and password from the user.
    Returns first login, second password.
    """
    login = dt.user.read_variable('login')
    password = dt.user.read_variable('password')
    return login, password


# -------------TEMPERATURE-----------------
def set_manual_date_temperature():
    """
    Sets the date when the user wants a manual temperature schedule to manual.
    """
    date = kl.date_now()
    dt.manual.update_variable('temperature_schedule', date)


def manual_date_temperature():
    """
    Returns the date when de user has set a manual temperature schedule.
    Variable date is given in a string form '2018-12-25'
    """
    date = dt.manual.read_variable('temperature_schedule')
    return date


def change_temperature(temperature):
    """
    Changes the temperature of the time of execution and the following hours of that day.
    """
    time = kl.time_now()
    day_type = kl.day_type()
    dt.temperature.copy_column1_to_column2(day_type, 'manual')
    start_hour = int(time[0] + time[1])

    for hour in range(start_hour, 24):
        if hour <= 9:
            key = "time='0" + str(hour) + ":00'"
            dt.temperature.update_data('manual', temperature, key)
        else:
            key = "time='" + str(hour) + ":00'"
            dt.temperature.update_data('manual', temperature, key)


def change_temperature_week(temperatures):
    """
    Changes the standard temperature schedule of a week day.
    Temperatures must be a list of all temperature values started with '00:00' and ended with '23:00'.
    """
    for hour in range(len(temperatures)):
        if hour <= 9:
            key = "time='0" + str(hour) + ":00'"
            dt.temperature.update_data('week', temperatures[hour], key)
        else:
            key = "time='" + str(hour) + ":00'"
            dt.temperature.update_data('week', temperatures[hour], key)


def temperature_week():
    """
    Returns the temperature schedule of a weekday.
    """
    temperatures = dt.temperature.read_variable('week')
    return temperatures


def change_temperature_weekend(temperatures):
    """
    Changes the standard temperature schedule of a weekend day.
    Temperatures must be a list of all temperature values started with '00:00' and ended with 23:00.
    """
    for hour in range(len(temperatures)):
        if hour <= 9:
            key = "time='0" + str(hour) + ":00'"
            dt.temperature.update_data('weekend', temperatures[hour], key)
        else:
            key = "time='" + str(hour) + ":00'"
            dt.temperature.update_data('weekend', temperatures[hour], key)


def temperature_weekend():
    """
    Returns the temperature schedule of a weekend day.
    """
    temperatures = dt.temperature.read_variable('weekend')
    return temperatures


def inside_temperature():
    """
    Reads the inside temperature.
    """
    time = kl.time_now()
    date = kl.date_now()
    day_type = kl.day_type()

    if date == manual_date_temperature():
        temperature = dt.temperature.select_data('manual', 'time', time)
        return temperature
    else:
        temperature = dt.temperature.select_data(day_type, 'time', time)
        return temperature


# -------------MACHINES-----------------
def list_converter(vector):
    """
    Converts the vector from a string to a list.
    """
    i = []
    vector = vector[1:len(vector)-1].replace(',','')
    length = len(vector)
    current_elements = ''

    for index in range(length):
        element = vector[index]
        if element is ' ' or index+1 == length:
            if index+1 == length:
                current_elements += str(element)
            if current_elements.isdigit() == True:
                i.append(int(current_elements))
                current_elements = ''
            else:
                i.append(float(current_elements))
                current_elements = ''
        else:
            current_elements += str(element)
    return i


def existing_machines():
    """
    Returns all machines in the database.
    """
    machines = dt.machines.read_variable('machine')
    return machines


def usage(machine):
    """
    Returns the usage of a given machine.
    """
    usage = dt.machines.select_data('usage', 'machine', machine)
    return usage


def add_machine(name, duration, usage, room):
    """
    Adds a new machine in the database with the given details.
    """
    data = [(str(name), str(room), str(duration), str(usage),'0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0')]
    dt.machines.add_data(data)
    dt.vectors.add_column(name, 'TEXT')


def machines_room(room):
    """
    Returns the machines in the given room.
    """
    machines = dt.machines.select_data('machine', 'room', room)

    if isinstance(machines, list) == False:
        return [machines]
    else:
        return machines


def delete_machine(name):
    """
    Deletes the given machine in the database.
    """
    dt.machines.delete_data('machine', name)
    key = "date >= '2018-01-01' and date <= '2018-12-31'"
    dt.vectors.update_data(name, 0, key)


def set_manual_date_machines():
    """
    Sets the date when the user wants a manual machine schedule to manual.
    It takes the next day to be manual.
    """
    date = kl.next_date()
    dt.manual.update_variable('machines_schedule', date)


def manual_date_machines():
    """
    Returns the date when de user has set a manual machine schedule.
    Variable date is given in a string form '2018-12-25'
    """
    date = dt.manual.read_variable('machines_schedule')
    return date


def change_machines_week(machines):
    """
    Changes the standard schedule of all machines in a week day.
    Machines must be a list of lists with each list: name, start_time and stop_time.
    """
    for machine in machines:
        name = machine[0]
        start_time = machine[1]
        stop_time = machine[2]
        key = "machine='" + str(name) + "'"
        dt.machines.update_data('start_time_week', start_time, key)
        dt.machines.update_data('stop_time_week', stop_time, key)


def change_machines_weekend(machines):
    """
    Changes the standard schedule of all machines in a weekend day.
    machines must be a list of lists with each list: name, start_time and stop_time.
    """
    for machine in machines:
        name = machine[0]
        start_time = machine[1]
        stop_time = machine[2]
        key = "machine='" + str(name) + "'"
        dt.machines.update_data('start_time_weekend', start_time, key)
        dt.machines.update_data('stop_time_weekend', stop_time, key)


def change_machines_manual(machines):
    """
    Changes the manual standard schedule of all machines.
    Machines must be a list of lists with each list: name, start_time and stop_time.
    """
    for machine in machines:
        name = machine[0]
        start_time = machine[1]
        stop_time = machine[2]
        key = "machine='" + str(name) + "'"
        dt.machines.update_data('start_time_manual', start_time, key)
        dt.machines.update_data('stop_time_manual', stop_time, key)


def plot_day_output(machine):
    """
    Returns the vector of the given machine of the day of execution.
    """
    date = kl.date_now() + ' 00:00:00'
    vector = list_converter(dt.vectors.select_data(machine, 'date', date))
    if vector is not None:
        return vector
    else:
        return None


def plot_windmill():
    """
    Returns the day vector of the yield of the windmill in a list.
    """
    date = kl.date_now()
    vector = dt.energy.select_data_of_date('yield_windmill', date)
    if not None in vector:
        return vector
    else:
        return None


def plot_solar_panels():
    """
    Returns the day vector of the yield of the solar panels in a list.
    """
    date = kl.date_now()
    vector = dt.energy.select_data_of_date('yield_solar_panels', date)
    if not None in vector:
        return vector
    else:
        return None


def usage_car(distance, capacity, range, duration):
    """
    Returns the usage of the car.
    So the usage of every hour in kWh.
    """
    return (distance/range*capacity)/duration


def total_usage():
    """
    Returns the total usage of every hour in a list.
    """
    date = kl.date_now()
    usages = dt.energy.select_data_of_date('total_usage', date)
    if not None in usages:
        return usages
    else:
        return None


def start_button(machine):
    """
    Turns the given machine on.
    The machine will work from its duration from the moment of the start button is been activated.
    """
    start_time = kl.datetime_now()
    duration = dt.machines.select_data('duration', 'machine', machine)
    new_time = datetime.datetime(int(start_time[0:4]), int(start_time[5:7]), int(start_time[8:10]), int(start_time[11:13])) + datetime.timedelta(hours=float(duration))
    stop_time = new_time.strftime("2018-%m-%d %H:%M")

    key = "machine='" + str(machine) + "'"
    dt.machines.update_data('stop_button', '0', key)
    dt.machines.update_data('start_button_begin', start_time, key)
    dt.machines.update_data('start_button_end', stop_time, key)


def undo_button(machine):
    """
    Erases the modification due to the start or stop button.
    """
    key = "machine='" + str(machine) + "'"
    dt.machines.update_data('start_button_begin', '2018-01-01 00:00', key)
    dt.machines.update_data('start_button_end', '2018-01-01 00:00', key)
    dt.machines.update_data('stop_button', '0', key)


def stop_button(machine):
    """
    Turns the given machine off.
    The machine will stop working.
    """
    key = "machine='" + str(machine) + "'"
    dt.machines.update_data('stop_button', '1', key)
    dt.machines.update_data('start_button_begin', '2018-01-01 00:00', key)
    dt.machines.update_data('start_button_end', '2018-01-01 00:00', key)


# -------------VARIABLES-----------------
def charging_speed_bat():
    """
    Reads the batteries charging speed.
    """
    charging_speed = dt.energy_details.read_variable('charging_speed_battery')
    return charging_speed


def set_charging_speed_bat(charging_speed):
    """
    Sets the charging speed of the battery to a given value.
    """
    if isinstance(charging_speed, int) or charging_speed.replace('.','').isdigit() is True:
        dt.energy_details.update_variable('charging_speed_batttery', charging_speed)


def discharging_speed_bat():
    """
    Reads the batteries discharging speed.
    """
    discharging_speed = dt.energy_details.read_variable('discharging_speed_battery')
    return discharging_speed


def set_discharging_speed_bat(discharging_speed):
    """
    Sets the discharging speed of the battery to a given value.
    """
    if isinstance(discharging_speed, int) or discharging_speed.replace('.','').isdigit() is True:
        dt.energy_details.update_variable('discharging_speed_battery', discharging_speed)


def capacity_bat():
    """
    Reads the maximum capacity of the battery.
    """
    capacity = dt.energy_details.read_variable('capacity_battery')
    return capacity


def set_capacity_bat(capacity):
    """
    Sets the capacity of the battery to a given value.
    """
    if isinstance(capacity, int) or capacity.replace('.','').isdigit() is True:
        dt.energy_details.update_variable('capacity_battery', capacity)


def blade_length():
    """
    Reads the maximum capacity of the battery.
    """
    length = dt.energy_details.read_variable('blade_length')
    return length


def set_blade_length(length):
    """
    Sets the blade length of the windmill to a given value.
    """
    if isinstance(length, int) or length.replace('.','').isdigit() is True:
        dt.energy_details.update_variable('blade_length', length)


def surface_solar_panels():
    """
    Reads the surface of the solar panels.
    """
    surface = dt.energy_details.read_variable('surface_solar_panels')
    return surface


def set_surface_solar_panels(surface):
    """
    Sets the surface of the solar panels to a given value.
    """
    if isinstance(surface, int) or surface.replace('.','').isdigit() is True:
        dt.energy_details.update_variable('surface_solar_panels', surface)


def efficiency_windmill():
    """
    Reads the efficiency of the windmill.
    """
    efficiency = dt.energy_details.read_variable('efficiency_windmill')
    return efficiency


def set_efficiency_windmill(efficiency):
    """
    Sets the efficiency of the windmill to a given value.
    """
    if isinstance(efficiency, int) or efficiency.replace('.','').isdigit() is True:
        dt.energy_details.update_variable('efficiency_windmill', efficiency)


def efficiency_solar_panels():
    """
    Reads the efficiency of the windmill.
    """
    efficiency = dt.energy_details.read_variable('efficiency_solar_panels')
    return efficiency


def set_efficiency_solar_panels(efficiency):
    """
    Sets the efficiency of the windmill to a given value.
    """
    if isinstance(efficiency, int) or efficiency.replace('.','').isdigit() is True:
        dt.energy_details.update_variable('efficiency_solar_panels', efficiency)


# -------------LIGHTS-----------------
def set_light_on(room):
    """
    Turns the light in the given room on.
    """
    key = "room=" + "'" + str(room) + "'"
    dt.lights.update_data('status', 'on', key)


def set_light_off(room):
    """
    Turns the light in the given room off.
    """
    key = "room=" + "'" + str(room) + "'"
    dt.lights.update_data('status', 'off', key)


def light(room):
    """
    Returns on if the light in the given room is on, else returns off.
    """
    status = dt.lights.select_data('status', 'room', room)
    return status
