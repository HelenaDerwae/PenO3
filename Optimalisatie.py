import Data_tables as dt
import datetime
import Klok as kl


# -------------OPTIMIZATION-----------------
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


def electricity_price():
    """
    Returns the electricity price in a list of the day of execution.
    It must be executed on the day of optimization.
    Variable date must be in the string form '2018-02-25'.
    """
    date = kl.date_now()
    prices = dt.energy.select_data_of_date('electricity_price', date)
    return prices


def charging_speed_bat():
    """
    Reads the batteries charging speed.
    """
    charging_speed = dt.energy_details.read_variable('charging_speed_battery')
    return charging_speed


def discharging_speed_bat():
    """
    Reads the batteries discharging speed.
    """
    discharging_speed = dt.energy_details.read_variable('discharging_speed_battery')
    return discharging_speed


def capacity_bat():
    """
    Reads the maximum capacity of the battery.
    """
    capacity = dt.energy_details.read_variable('capacity_battery')
    return capacity


def manual_date_machines():
    """
    Returns the date when de user has set a manual machine schedule.
    """
    date = dt.manual.read_variable('machines_schedule')
    return date


def manual_date_car():
    """
    Returns the date when de user has set a manual machine schedule.
    """
    date = dt.manual.read_variable('car_schedule')
    return date


def machines():
    """
    Reads all machines and gives a list of lists with each list the name, duration, usage, start_time, end_time of an individual machine.
    Takes the machines of the day of execution.
    """
    date_now = kl.date_now()
    datetime_now = kl.datetime_now()
    day_type = kl.day_type()
    machines = dt.machines.read_variable('machine')
    list_of_machines = []

    for machine in machines:
        start_datetime = dt.machines.select_data('start_button_begin', 'machine', machine)
        stop_datetime = dt.machines.select_data('start_button_end', 'machine', machine)
        machine = dt.machines.select_data('machine', 'machine', machine)
        duration = dt.machines.select_data('duration', 'machine', machine)
        usage = dt.machines.select_data('usage', 'machine', machine)

        if dt.machines.select_data('stop_button', 'machine', machine) is '1':
            start_time = 0
            stop_time = 0

        elif datetime.datetime(int(start_datetime[0:4]), int(start_datetime[5:7]), int(start_datetime[8:10]), int(start_datetime[11:13])) <= datetime.datetime(int(datetime_now[0:4]), int(datetime_now[5:7]), int(datetime_now[8:10]), int(datetime_now[11:13])) < datetime.datetime(int(stop_datetime[0:4]), int(stop_datetime[5:7]), int(stop_datetime[8:10]), int(stop_datetime[11:13])):
            if int(start_datetime[8:10]) == int(stop_datetime[8:10]):
                start_time = dt.machines.select_data('start_button_begin', 'machine', machine)[11:13]
                stop_time = dt.machines.select_data('start_button_end', 'machine', machine)[11:13]
            else:
                if start_datetime[8:10] == datetime_now[8:10]:
                    start_time = dt.machines.select_data('start_button_begin', 'machine', machine)[11:13]
                    stop_time = 23
                elif stop_datetime[8:10] == datetime_now[8:10]:
                    start_time = 0
                    stop_time = dt.machines.select_data('start_button_end', 'machine', machine)[11:13]

        else:
            if date_now == manual_date_machines():
                start_time = dt.machines.select_data('start_time_manual', 'machine', machine)
                stop_time = dt.machines.select_data('stop_time_manual', 'machine', machine)
            else:
                start_time = dt.machines.select_data('start_time_' + str(day_type), 'machine', machine)
                stop_time = dt.machines.select_data('stop_time_' + str(day_type), 'machine', machine)

        data_of_machine = [machine, int(duration), int(usage), int(start_time), int(stop_time)]
        list_of_machines.append(data_of_machine)
    return list_of_machines


def optimization_output(optimization, date=None):
    """
    Given the dictionarie 'optimization' with the first element the
    name of the machine and second the status vector.
    The vector is saved in the database.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    for machine in optimization:
        vector = optimization[machine]
        key = "date='" + str(date) + " 00:00:00'"
        dt.vectors.update_data(machine, vector, key)


# ------------ENERGY-CALCULATION---------------
def blade_length():
    """
    Reads the maximum capacity of the battery.
    """
    length = dt.energy_details.read_variable('blade_length')
    return length


def surface_solar_panels():
    """
    Reads the surface of the solar panels.
    """
    surface = dt.energy_details.read_variable('surface_solar_panels')
    return surface


def efficiency_windmill():
    """
    Reads the efficiency of the windmill.
    """
    efficiency = dt.energy_details.read_variable('efficiency_windmill')
    return efficiency


def efficiency_solar_panels():
    """
    Reads the efficiency of the windmill.
    """
    efficiency = dt.energy_details.read_variable('efficiency_solar_panels')
    return efficiency


def wind_speed(date=None):
    """
    Returns the wind speed in a list from the day of execution.
    """
    if date is None:
        date = kl.date_now()

    wind_speed = dt.weather_conditions.select_data_of_date('wind_speed', date)
    return wind_speed


def wind_energy_output(wind_energy, date=None):
    """
    Inserts the yield wind energy in the database.
    The variable wind_energy_output must be a list of 24 integers representing every hour of a day.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    for hour in range(len(wind_energy)):
        if hour <= 9:
            key = "datetime='" + str(date) + " 0" + str(hour) + ":00'"
            dt.energy.update_data('yield_windmill', wind_energy[hour], key)
        else:
            key = "datetime='" + str(date) + " " + str(hour) + ":00'"
            dt.energy.update_data('yield_windmill', wind_energy[hour], key)


def solar_energy_output(solar_energy, date=None):
    """
    Inserts the yield energy of the solar panels in the database.
    The variable solar_energy_output must be a list of 24 integers representing every hour of a day.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    for hour in range(len(solar_energy)):
        if hour <= 9:
            key = "datetime='" + str(date) + " 0" + str(hour) + ":00'"
            dt.energy.update_data('yield_solar_panels', solar_energy[hour], key)
        else:
            key = "datetime='" + str(date) + " " + str(hour) + ":00'"
            dt.energy.update_data('yield_solar_panels', solar_energy[hour], key)


def radiation_direct_horizontal(date=None):
    """
    Returns the direct horizontal radiation in a list from the date of execution.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    radiation_direct = dt.weather_conditions.select_data_of_date('radiation_direct_horizontal', date)
    return radiation_direct


def radiation_diffuse_horizontal(date=None):
    """
    Returns the diffuse horizontal radiation in a list from the date of execution.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    radiation_diffuse = dt.weather_conditions.select_data_of_date('radiation_diffuse_horizontal', date)
    return radiation_diffuse


def storage_battery_output(storage_battery,date=None):
    """
    Inserts the battery storage on every hour of the given date.
    Storage_battery must be a list of 24 variables.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    time = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    for i in range(len(storage_battery)):
        key = "datetime='" + str(date) + ' ' + time[i] + "'"
        dt.energy.update_data('storage_battery', storage_battery[i], key)


def storage_battery_yesterday():
    """
    Reads the battery storage from yesterday (last hour).
    It's executed on the day of optimization.
    Variable date must be in the string form '2018-02-25'.
    """
    date = kl.date_now()
    previous_date = kl.previous_date()
    if date == '2018-01-01':
        return 0
    else:
        storage = dt.energy.select_data_last_hour('storage_battery', previous_date)
        if storage is None:
            return 0
        else:
            return storage


# -------------CAR-----------------
def range_car():
    """
    Reads the range of the car.
    """
    range = dt.car.read_variable('range_car')
    return range


def capacity_car():
    """
    Reads the range of the car.
    """
    capacity = dt.car.read_variable('capacity_car')
    return capacity


def distance_car():
    """
    Reads the distance of the car.
    """
    distance = dt.car.read_variable('distance_car')
    return distance


def duration_car():
    """
    Reads the duration of the car.
    """
    duration = dt.car.read_variable('duration_car')
    return duration


def car():
    """
    Reads the car variables and gives a list with car, duration, distance_car, start_time, end_time.
    It must be executed on the day of optimization.
    """
    date = kl.date_now()
    day_type = kl.day_type()
    if not dt.car.read_variable('name_car') is 0:
        if date == manual_date_car():
            columns = ['duration', 'distance_car', 'start_time_manual', 'stop_time_manual']
        else:
            columns = ['duration', 'distance_car', 'start_time_' + str(day_type), 'stop_time_' + str(day_type)]

        list = ['auto']
        for column in columns:
            data = dt.car.read_variable(column)
            list.append(data)
        return list
    else:
        return None


# -------------TEMPERATURE----------------
def manual_date_temperature():
    """
    Returns the date when de user has set a manual machine schedule.
    """
    date = dt.manual.read_variable('temperature_schedule')
    return date


def outside_temperatures(date=None):
    """
    Reads the outside temperatures for a whole day.
    The variable date is in form of '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    temperature = dt.weather_conditions.select_data_of_date('outside_temperature', date)
    return temperature


def desired_inside_temperatures():
    """
    Reads the desired inside temperatures for a whole day.
    It depends on the type of the day and if the user wants a manual schedule.
    """
    date = kl.date_now()
    day_type = kl.day_type()
    if date == manual_date_temperature():
        temperature = dt.temperature.read_variable('manual')
        return temperature
    else:
        temperature = dt.temperature.read_variable(day_type)
        return temperature


def inside_temperature_yesterday():
    """
    Reads the inside temperature from yesterday (last hour).
    It's executed on the day of optimization.
    Variable date must be in the string form '2018-02-25'.
    """
    date = kl.date_now()
    previous_date = kl.previous_date()
    if date == '2018-01-01':
        return 0
    else:
        temperature = dt.energy.select_data_last_hour('inside_temperature', previous_date)
        return temperature


def inside_temperature_output(inside_temperatures, date=None):
    """
    Inserts the inside temperature of every hour of the given date.
    inside_temperatures must be a list of 24 variables.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    time = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00',
            '11:00',
            '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00',
            '23:00']
    for i in range(len(inside_temperatures)):
        key = "datetime='" + str(date) + ' ' + time[i] + "'"
        dt.energy.update_data('inside_temperature', inside_temperatures[i], key)


def inside_temperatures(date=None):
    """
    Reads the inside temperatures for a whole day.
    The variable date is in form of '2018-02-25' or can be the moment of execution.
    """
    if date is None:
        date = kl.date_now()

    temperature = dt.energy.select_data_of_date('inside_temperature', date)
    return temperature


# -------------SIEBE----------------
def current_vectors(date=None):
    """
    Returns in a dictionary the vectors of all the machines (incl. car) on the date of execution or on the given date.
    The key is the name of the machine in string form followed by the vector in string form as value.
    The variable date is in form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()
    date = date + ' 00:00:00'
    i = {}
    machines = dt.machines.read_variable('machine') + ['auto']

    for machine in machines:
        vector = list_converter(dt.vectors.select_data(machine, 'date', date))
        print('machine ' + str(machine))
        print('vector ' + str(vector))
        i[machine] = vector
    return i


def discharging_battery_output(vector, date=None):
    """
    Inserts the discharging battery vector in the database on the given day or moment of execution.
    The variable vector must be a list of 24 integers representing every hour of a day.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    for hour in range(len(vector)):
        if hour <= 9:
            key = "datetime='" + str(date) + " 0" + str(hour) + ":00'"
            dt.energy.update_data('discharging_battery', vector[hour], key)
        else:
            key = "datetime='" + str(date) + " " + str(hour) + ":00'"
            dt.energy.update_data('discharging_battery', vector[hour], key)


def discharging_battery(date=None):
    """
    Returns the discharging battery vector of the given day or moment of execution.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    discharging = dt.energy.select_data_of_date('discharging_battery', date)
    return discharging


def charging_battery_output(vector, date=None):
    """
    Inserts the charging battery vector in the database on the given day or moment of execution.
    The variable vector must be a list of 24 integers representing every hour of a day.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    for hour in range(len(vector)):
        if hour <= 9:
            key = "datetime='" + str(date) + " 0" + str(hour) + ":00'"
            dt.energy.update_data('charging_battery', vector[hour], key)
        else:
            key = "datetime='" + str(date) + " " + str(hour) + ":00'"
            dt.energy.update_data('charging_battery', vector[hour], key)


def charging_battery(date=None):
    """
    Returns the charging battery vector of the given day or moment of execution.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    charging = dt.energy.select_data_of_date('charging_battery', date)
    return charging


def storage_battery(date=None):
    """
    Returns the storage in the battery on the given day or moment of execution.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    storage = dt.energy.select_data_of_date('storage_battery', date)
    return storage


def total_usage_output(vector, date=None):
    """
    Inserts the total usage vector in the database on the given day or moment of execution.
    The variable vector must be a list of 24 integers representing every hour of a day.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    for hour in range(len(vector)):
        if hour <= 9:
            key = "datetime='" + str(date) + " 0" + str(hour) + ":00'"
            dt.energy.update_data('total_usage', vector[hour], key)
        else:
            key = "datetime='" + str(date) + " " + str(hour) + ":00'"
            dt.energy.update_data('total_usage', vector[hour], key)


def total_usage(date=None):
    """
    Returns the usage vector of all machines on the given day or moment of execution.
    Variable date must be in the string form '2018-02-25'.
    """
    if date is None:
        date = kl.date_now()

    usages = dt.energy.select_data_of_date('total_usage', date)
    return usages


def usage_heating_system_output(vector, date=None):
    """
    Inserts the vector of the heating system on the given day or moment of execution.
    Usage must be a list of length 24.
    Date must be in string form '2018-01-25' .
    """
    if date is None:
        date = kl.date_now()

    for hour in range(len(vector)):
        if hour <= 9:
            key = "datetime='" + str(date) + " 0" + str(hour) + ":00'"
            dt.energy.update_data('usage_heating_system', vector[hour], key)
        else:
            key = "datetime='" + str(date) + " " + str(hour) + ":00'"
            dt.energy.update_data('usage_heating_system', vector[hour], key)


def usage_heating_system(date=None):
    """
    Returns the vector of the heating system.
    Date must be in string form '2018-01-25' or can be the moment of execution.
    """
    if date is None:
        date = kl.date_now()

    usages = dt.energy.select_data_of_date('usage_heating_system', date)
    return usages
