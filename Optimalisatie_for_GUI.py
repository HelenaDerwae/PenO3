from Continous_running_file import solution
import Optimalisatie2 as db
from SetUp2 import *
import Klok

oplossing, bat_inhoud, total_usage, bat_opladen, bat_afladen, total, T_binnen, Q_pomp, price = solution[0],solution[1],solution[2],solution[3],solution[4],solution[5],solution[6],solution[7], solution[8]

def optimization_random_on():
    time2 = Klok.time_now()[0:2]
    # time2 = 1
    print(time2)

    prijzen = db.electricity_price()

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
    bat_max_opladen = db.charging_speed_bat()
    bat_max_afladen = db.discharging_speed_bat()
    bat_max_inhoud = db.capacity_bat()
    bat_prev_inhoud = db.battery_storage_yesterday()
    T_buiten = db.outside_temperatures()
    T_gewenst = db.desired_inside_temperatures()
    T_begin = 20
    ### machines:
    # print(sum(opbrengst))

    machines_db = db.machines()
    machines = list()
    car = db.car()
    print('car',car)

    for i in machines_db:
        machines.append(Machine(i[0], int(i[1]), float(i[2]), int(i[3]), int(i[4])))
    # machines.append(Machine(car[0], int(car[1]), float(car[2]), int(car[3]), int(car[4])))
    machines.append(Machine(car[0], int(car[1]), int(car[2]), int(car[3]), int(car[4])))

    machines_updated = list()
    for i in machines_db:
        machines_updated.append(
            UpdatedMachine(i[0], int(i[1]), float(i[2]), int(i[3]), int(i[4]), int(time2), oplossing))
    machines_updated.append(Machine(car[0], int(car[1]), int(car[2]), int(car[3]), int(car[4])))

    func_plot(total_usage,opbrengst,prijzen,bat_inhoud,total,time2)

    opl = optimalisatie(prijzen, machines_updated, opbrengst, T_begin,T_buiten,T_gewenst, bat_max_opladen, bat_max_afladen,
              bat_max_inhoud, bat_prev_inhoud,time2,bat_opladen,bat_afladen, T_binnen, Q_pomp)

    db.optimization_output(opl[0])
    db.battery_storage_output(opl[1][1:25])
    db.inside_temperature_output(opl[6])
    db.battery_output(opl[3])
    db.usage_output(opl[5])

    easy_print(opl[0],time2)
#self.testButton = Button(self, text=" test", command=lambda:[funct1(), updated_optimization(schedule, "apparaat")])
optimization_random_on()

