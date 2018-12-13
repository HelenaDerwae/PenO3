import Database as db


# TABLES
weather_conditions = db.Table('Smart_home','Weather_conditions','datetime KEY, outside_temperature INTEGER, wind_speed INTEGER, radiation_direct_horizontal INTEGER, radiation_diffuse_horizontal INTEGER', 'Weather_conditions.xlsx')
machines = db.Table('Smart_home', 'Machines', 'machine KEY, room TEXT, duration INTEGER, usage INTEGER, start_time_week INTEGER, stop_time_week INTEGER, start_time_weekend INTEGER, stop_time_weekend INTEGER, start_time_manual INTEGER, stop_time_manual INTEGER, start_button_begin TEXT, start_button_end TEXT, stop_button TEXT')
vectors = db.Table('Smart_home', 'Vectors', 'date KEY, auto BLOB, koelkast BLOB, vriezer BLOB, oven BLOB, kookplaat BLOB, wasmachine BLOB, afwasmachine BLOB, droogkast BLOB, boiler BLOB, TV BLOB', 'Vectors.xlsx')
energy = db.Table('Smart_home', 'Energy', 'datetime KEY, inside_temperature INTEGER, usage_heating_system INTEGER, yield_solar_panels INTEGER, yield_windmill INTEGER, electricity_price INTEGER, storage_battery INTEGER, discharging_battery INTEGER, charging_battery INTEGER, total_usage INTEGER', 'Energy.xlsx')
energy_details = db.Table('Smart_home', 'Energy_details', 'surface_solar_panels INTEGER, efficiency_solar_panels INTEGER, blade_length INTEGER, efficiency_windmill INTEGER, charging_speed_battery INTEGER, discharging_speed_battery INTEGER, capacity_battery INTEGER')
user = db.Table('Smart_home', 'User', 'family KEY, login TEXT, password TEXT')
temperature = db.Table('Smart_home', 'Temperature', 'time KEY, weekend INTEGER, week INTEGER, manual INTEGER')
car = db.Table('Smart_home', 'Car', 'name_car KEY, range_car INTEGER, capacity_car INTEGER, duration_car INTEGER, updated TEXT, distance_car INTEGER, start_time_week INTEGER, stop_time_week INTEGER, start_time_weekend INTEGER, stop_time_weekend INTEGER, start_time_manual INTEGER, stop_time_manual INTEGER')
manual = db.Table('Smart_home', 'Manual', 'temperature_schedule TEXT, machines_schedule TEXT, car_schedule TEXT')
datetime = db.Table('Smart_home', 'Datetime', 'datetime')
lights = db.Table('Smart_home', 'Lights', 'room KEY, status TEXT')


def init_smart_home():
    """
    Initialisation of the database 'Smart_home'.
    Before using init_smart_home be sure to clear the database with clear_smart_home
    or delete the file (gives reduction in MB).
    """
    smart_home = db.Database('Smart_home')

    assert smart_home.add_table(temperature) == True
    assert smart_home.add_table(weather_conditions) == True
    assert smart_home.add_table(machines) == True
    assert smart_home.add_table(energy) == True
    assert smart_home.add_table(energy_details) == True
    assert smart_home.add_table(user) == True
    assert smart_home.add_table(car) == True
    assert smart_home.add_table(manual) == True
    assert smart_home.add_table(vectors) == True
    assert smart_home.add_table(datetime) == True
    assert smart_home.add_table(lights) == True
    assert smart_home.get_tables() == [temperature, weather_conditions, machines, energy, energy_details, user, car,
                                     manual, vectors, datetime, lights]

    # -------------WEATHER-CONDITIONS-----------------
    weather_conditions.create_index('datetime')

    # ------------------MACHINES-----------------------
    machines.create_index('machine')
    data = [('oven','kitchen', '0','0.79','0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0'),('koelkast','kitchen','24','116','0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0'), ('vriezer','kitchen','24','220','0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0'), ('kookplaat','kitchen','0','2.78','0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0'), ('afwasmachine','kitchen','0','0.84','0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0'), ('boiler','storage space','0','0','0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0'), ('TV','living room','0','0','0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0'), ('wasmachine','storage space','0','2.50','0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0'), ('droogkast','storage space','0','2.50','0','0','0','0','0','0','2018-01-01 00:00','2018-01-01 00:00','0')]
    machines.add_data(data)

    # -----------------VECTORS------------------------
    vectors.create_index('date')

    # -------------------ENERGY-----------------------
    energy.create_index('datetime')

    # ---------------ENERGY-DETAILS-------------------
    data = [('19.62','0.8','1.85','0.8','5','7','13.5')]
    energy_details.add_data(data)

    # -------------------USER------------------------
    user.create_index('family')
    data = [('Peeters', 'Peeters', 'X')]
    user.add_data(data)

    # ----------------TEMPERATURE---------------------
    temperature.create_index('time')
    data = [ ('00:00','20','20','20'), ('01:00','20','20','20'), ('02:00','20','20','20'), ('03:00','20','20','20'), ('04:00','20','20','20'), ('05:00','20','20','20'),
             ('06:00','20','20','20'),('07:00','20','20','20'), ('08:00','20','20','20'), ('09:00','20','20','20'), ('10:00','20','20','20'), ('11:00','20','20','20'),
             ('12:00','20','20','20'), ('13:00','20','20','20'), ('14:00','20','20','20'), ('15:00','20','20','20'), ('16:00','20','20','20'), ('17:00','20','20','20'),
             ('18:00','20','20','20'), ('19:00','20','20','20'), ('20:00','20','20','20'), ('21:00','20','20','20'), ('22:00','20','20','20'), ('23:00','20','20','20')]
    temperature.add_data(data)

    # -------------------CAR--------------------------
    data = [('0','0','0','0','0','0','0','0','0','0','0','0')]
    car.add_data(data)

    # ------------------MANUAL------------------------
    data = [('0', '0', '0')]
    manual.add_data(data)

    # -----------------DATETIME-----------------------
    data = [('0')]
    datetime.add_data(data)
    datetime.update_variable('datetime', '2018-01-01 00:00')

    # -----------------LIGHTS-----------------------
    data = [('berging', 'off'), ('living', 'off'), ('keuken', 'off'), ('slaapkamer', 'off'), ('badkamer', 'off')]
    lights.add_data(data)


def clear_smart_home():
    """
    Delete all the tables in database 'Smart_home'.
    """
    smart_home = db.Database('Smart_home')

    assert smart_home.add_table(temperature) == True
    assert smart_home.add_table(weather_conditions) == True
    assert smart_home.add_table(machines) == True
    assert smart_home.add_table(energy) == True
    assert smart_home.add_table(energy_details) == True
    assert smart_home.add_table(user) == True
    assert smart_home.add_table(car) == True
    assert smart_home.add_table(manual) == True
    assert smart_home.add_table(vectors) == True
    assert smart_home.add_table(datetime) == True
    assert smart_home.add_table(lights) == True
    assert smart_home.get_tables() == [temperature, weather_conditions, machines, energy, energy_details, user, car,
                                       manual, vectors, datetime, lights]

    smart_home.remove_all_tables()
    assert smart_home.get_tables() == []


if __name__ == '__main__':
    # clear_smart_home()
    init_smart_home()
