import time
from SetUp2 import *
import Optimalisatie2 as db
import datetime
import Klok as kl

### Daily update

# date2 = str(kl.date_now())
# time2 = date2[11:13]
time2 = 1
# time2 = kl.time_now()[0:2]
time2 = int(time2)
def new_optimization(t):

    print("i am working", t)

    ### Gegevens database

    ## Energie

    straal = db.blade_length()
    efficientie = db.efficiency_windmill()
    windsnelheden = db.wind_speed()

    direct = db.radiation_direct_horizontal()
    diffuse = db.radiation_diffuse_horizontal()
    oppervlakte = db.surface_solar_panels()
    rendement = db.efficiency_solar_panels()

    opbrengst = vector_sum(windenergie(straal, windsnelheden, efficientie),
                           zonne_energie(direct, diffuse, oppervlakte, rendement))
    # print(opbrengst)
    # print(zonne_energie(direct,diffuse,oppervlakte,rendement))
    ## Verwarming
    T_begin = 20
    # T_begin = db.inside_temperature_yesterday()
    T_buiten = db.outside_temperatures()
    T_gewenst = db.desired_inside_temperatures()

    ## Machines

    machines_db = db.machines()
    machines = list()

    for i in machines_db:
        machines.append(Machine(i[0], int(i[1]), int(i[2]), int(i[3]), int(i[4])))


    ## Optimalisatie

    prijzen = db.electricity_price()
    bat_max_opladen = db.charging_speed_bat()
    bat_max_afladen = db.discharging_speed_bat()
    bat_max_inhoud = db.capacity_bat()
    prev_battery_inhoud = db.battery_storage_yesterday()

    oplossing, bat_inhoud, total_usage, bat_opladen, bat_afladen, total, T_binnen, Q_pomp, price = optimalisatie(prijzen, machines, opbrengst,T_begin,T_buiten,T_gewenst, bat_max_opladen, bat_max_afladen, bat_max_inhoud, prev_battery_inhoud)
    easy_print(oplossing,int(time2))
    db.optimization_output(oplossing)

    func_plot(total_usage,opbrengst,prijzen,bat_inhoud,total,time2)
    print("Completed optimalization")

    return oplossing, unpack(bat_inhoud), unpack(total_usage), unpack(bat_opladen), unpack(bat_afladen), unpack(total), unpack(T_binnen), unpack(Q_pomp), price

solution = new_optimization("00,00")
# print(solution)
# print(solve[0])

#
# while True:

# if kl.time_now() == '00:00':
#
#     solution = new_optimization("00:00")



time.sleep(1.0)  # wait one minute

while time2 != 0:
    print(time2)
    time.sleep(1.0)
    time2 += 1
    if time2 == 24:
        time2 = 0
else:
    solution = new_optimization("00:00")
    time2 = 0



# schedule.every().day.at("00:00").do(new_optimization, 'It is 00:00')
