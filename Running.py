from SetUp import *
from time import sleep
import Optimalisatie as db



date2 = str(datetime.datetime.now())
date_tom2 = str(datetime.datetime.today() + datetime.timedelta(days=1))
date_yest2 = str(datetime.datetime.today() + datetime.timedelta(days=-1))
# print(date2)
date = "2018-" + str(date2[5:7]) + "-" + str(date2[8:10])
tomorrow = "2018-" + str(date_tom2[5:7]) + "-" + str(date_tom2[8:10])
yesterday = "2018-" + str(date_yest2[5:7]) + "-" + str(date_yest2[8:10])
print(yesterday,date,tomorrow)
# print(date)
weekday = is_weekday()
time = date2[11:13]
# time = 11
prijzen = db.electricity_price()
prijzen_tom = db.electricity_price()
# print(prijzen)
# print(len(prijzen))
# prijzen.append([16])

### opbrengst:

straal = db.blade_length()
efficientie = db.efficiency_windmill()
windsnelheden = db.wind_speed()
windsnelheden_tom = db.wind_speed()

direct = db.radiation_direct_horizontal()
direct_tom = db.radiation_direct_horizontal()
# print(direct)
diffuse = db.radiation_diffuse_horizontal()
diffuse_tom = db.radiation_diffuse_horizontal()
# print(diffuse)
oppervlakte = db.surface_solar_panels()
rendement = db.efficiency_solar_panels()

opbrengst = vector_sum(windenergie(straal, windsnelheden, efficientie),zonne_energie(direct, diffuse, oppervlakte, rendement))
# opbrengst_tom = vector_sum(windenergie(straal, windsnelheden_tom, efficientie),zonne_energie(direct_tom, diffuse_tom, oppervlakte, rendement))
# print(opbrengst)
# print(len(opbrengst))

### machines:

machines_db = db.machines()
machines = list()
random_on = dict()

for i in machines_db:
    machines.append(Machine(i[0], int(i[1]), float(i[2]), int(i[3]), int(i[4])))
    random_on[i[0]] = []

### optimalisatie:

prijzen = db.electricity_price()
print(prijzen)
bat_max_opladen = db.charging_speed_bat()
bat_max_afladen = db.discharging_speed_bat()
bat_max_inhoud = db.capacity_bat()
# bat_prev_inhoud = db.battery_storage(yesterday)
# print(bat_prev_inhoud)
bat_prev_inhoud = 5

# battery_quota = get_daily_battery_quota(prijzen,opbrengst,prijzen_tom,opbrengst_tom,bat_max_inhoud,bat_prev_inhoud)
battery_quota = 3
print(battery_quota)

schedule, bat_inhoud, total_usage, bat_opladen, bat_afladen, total = optimalisatie(prijzen, machines, opbrengst, bat_max_opladen, bat_max_afladen, bat_max_inhoud,bat_prev_inhoud,battery_quota)
list_tot_usage, opbrengst, prices, list_bat, list_tot = list_info(total_usage, opbrengst, prijzen, bat_inhoud, total)
all_info = (schedule, list_tot_usage, opbrengst, prices, list_bat, list_tot)

func_plot(total_usage,opbrengst,prijzen,bat_inhoud,total)
get_daily_winnings(prices,list_tot)
print(list_tot)
def running(all_info,first_time=0):

    if first_time == 0:
        easy_print(all_info[0], int(time))
        first_time = 1
    name = str(input('Welk apparaat staat er plotseling aan? '))
    random_on[name].append(1)
    for i in machines_db:
        if i[0] != name:
            random_on[i[0]].append(0)

    # print('random_on',random_on)

    #### Nog opslagen in database

    if str(date[11:18]) != "00:00:00":

        machines_updated = list()
        already_done = already_worked_schedule(all_info[0], time)

        for i in machines_db:
            machines_updated.append(UpdatedMachine(i[0], int(i[1]), float(i[2]), int(i[3]), int(i[4]), int(time), schedule ,random_on))
            # print('name',i[0],'duration',int(i[1])+ sum(random_on[i[0]])*int(i[1]))
        print(machines_updated)
        schedule_updated, bat_inhoud, total_usage, bat_opladen, bat_afladen, total = optimalisatierandomon2(all_info[3], all_info[2], machines_updated,all_info[0],random_on,bat_max_opladen,bat_max_afladen,bat_max_inhoud,int(time),all_info[4][int(time) - 1])

        list_tot_usage_upd, opbrengst, prices, list_bat_upd, list_tot_upd = list_info(total_usage, all_info[2], all_info[3], bat_inhoud, total,int(time))

        # easy_print(schedule_updated,time)
        for i in already_done.keys():
            schedule_updated[i] = already_done[i] + schedule_updated[i]

        list_tot_usage_upd = all_info[1][:int(time)] + list_tot_usage_upd
        list_bat_upd = all_info[4][:int(time)] + list_bat_upd[1:]
        list_tot_upd = all_info[5][:int(time)] + list_tot_upd

        all_info_upd = (schedule_updated, list_tot_usage_upd, opbrengst, prices, list_bat_upd, list_tot_upd, int(time))

        # schedule_updated = already_done
        easy_print(schedule_updated, int(time))
        func_plot(list_tot_usage_upd, opbrengst, prijzen, list_bat_upd, list_tot_upd,time)
        print(list_tot_upd)
        print(get_random_on_price(prices,list_tot_upd))
        get_daily_winnings(prices,list_tot_upd)
        running(all_info_upd,first_time)

    running(schedule,first_time)


running(all_info)
