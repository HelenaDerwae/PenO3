import Data_tables as dt
import Gebruikersscherm as gb
import Klok as kl


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


def standard_machines():
    """
    Returns the standard machines in a list.
    """
    return ['windmolen', 'auto', 'verwarming', 'batterij', 'koelkast', 'vriezer', 'oven', 'kookplaat', 'wasmachine', 'afwasmachine',
    'droogkast', 'boiler', 'TV']


def windmill(date):
    """
    Returns in a list the wind speed of every hour of one day.
    There are five different states: 0, 1, 2, 3, 4 and 5 (Beaufort scale).
    """
    vector = dt.weather_conditions.select_data_of_date('wind_speed', date)
    i = []

    for wind_speed in vector:
        if float(wind_speed) <= 0.5:
            i.append(0)
        elif 0.5 < float(wind_speed) <= 1.5:
            i.append(1)
        elif 1.5 < float(wind_speed) <= 3.3:
            i.append(2)
        elif 3.3 < float(wind_speed) <= 5.5:
            i.append(3)
        elif 5.5 < float(wind_speed) <= 7.9:
            i.append(4)
        elif 7.9 < float(wind_speed):
            i.append(5)
    return i


def heating_system(date):
    """
    Returns in a list the wind speed of every hour of one day.
    There are 100 different states between 0 and 1.
    """
    vector = list_converter(dt.vectors.select_data('verwarming', 'date', date))
    i = []

    for usage in vector:
        value = round(float(usage)/3000, 2)
        if value == 0:
            i.append(0)
        if 0 < value <= 0.25:
            i.append(0.25)
        elif 0.25 < value <= 0.5:
            i.append(0.50)
        elif 0.5 < value <= 0.75:
            i.append(0.75)
        elif 0.75 < value <= 1:
            i.append(1)
    return i


def machines():
    """
    Returns in a dictionary the vectors of the standard machines used in the mini house.
    The key is the name of the machine in string form followed by the vector in string form as value.

    The standard machines in order: 'windmolen', 'auto', 'verwarming', 'batterij', 'koelkast', 'vriezer', 'oven', 'kookplaat', 'wasmachine', 'afwasmachine',
    'droogkast', 'boiler', 'TV'.
    """
    i = dict()
    i['uur'] = kl.datetime_now()
    date_1 = kl.date_now()
    date_2 = date_1 + ' 00:00:00'
    machines = ['auto', 'batterij', 'koelkast', 'vriezer', 'oven', 'kookplaat', 'wasmachine', 'afwasmachine',
    'droogkast', 'boiler', 'TV']
    existing_machines = dt.machines.read_variable('machine')

    i['licht_berging'] = dt.lights.select_data('status', 'room', 'berging')
    i['licht_living'] = dt.lights.select_data('status', 'room', 'living')
    i['licht_keuken'] = dt.lights.select_data('status', 'room', 'keuken')
    i['licht_slaapkamer'] = dt.lights.select_data('status', 'room', 'slaapkamer')
    i['licht_badkamer'] = dt.lights.select_data('status', 'room', 'badkamer')
    i['verwarming'] = heating_system(date_2)
    i['windmolen'] = windmill(date_1)

    for machine in machines:
        if machine in existing_machines:
            vector = list_converter(dt.vectors.select_data(machine, 'date', date_2))
            i[machine] = vector
        elif machine is 'batterij':
            vector = list_converter(dt.vectors.select_data('batterij', 'date', date_2))
            i[machine] = vector
        elif machine is 'auto' and gb.existing_car() is not None:
            vector = list_converter(dt.vectors.select_data(machine, 'date', date_2))
            i[machine] = vector
        else:
            vector = 24*[0]
            i[machine] = vector
    return i

machines()