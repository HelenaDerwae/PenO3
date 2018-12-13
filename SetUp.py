import cvxpy
import numpy
import datetime
import math
import matplotlib.pyplot as plt
# from cvxpy import *
# import GLPK_MI
# from cvxpy import GLPK_MI
# from cvxpy.problems.solvers.glpk_mi_intf import GLPK_MI
# import



### hulpfuncties:
def get_daily_battery_quota(prices_today, opbrangst_today, prices_tomorrow, opbrensgt_tomorrow, max_battery, prev_battery):
    mid_pr_today = prices_today.mid()
    mid_opbr_tod = opbrangst_today.mid()

    mid_pr_tom = prices_tomorrow.mid()
    mid_opbr_tom = opbrensgt_tomorrow.mid()

    factor = (mid_pr_today/mid_pr_tom)*(mid_opbr_tod/mid_opbr_tom)

    quota = factor*prev_battery

    if prev_battery > max_battery:
        quota = max_battery

    return quota

def get_daily_winnings(prices,total):
    opt_prijs = get_random_on_price(prices,total)
    mid_total = sum(total)/len(total)
    prijs = 0
    for i in range(len(prices)):
        prijs += prices[i]*mid_total

    print('Zonder optimalisatie zou u ', round(prijs,4),' moeten betalen. Maar door de optimalisatie betaalt u maar ',round(opt_prijs,4),', dit is een verschil van ', round(prijs-opt_prijs,4), '.')


def get_random_on_price(prices,updated_total):

    prijs = 0

    for i in range(len(prices)):
        prijs += prices[i]*updated_total[i]

    return prijs


def already_worked_schedule(schedule,time):
    already_worked_schedule = dict()
    for i in schedule.keys():
        already_worked_schedule[i] = schedule[i][:int(time)]
    return already_worked_schedule

def vector_sum(vector1,vector2):
    for i in range(len(vector1)):
        vector1[i] += vector2[i]

    return vector1

def only_get_prev_schedule(schedule,time):
    for elem in schedule.keys():
        schedule[elem] = schedule[elem][0:time]

    return schedule






def easy_print(schedule,time):
    print("{:<18} {:<70}".format('Name', 'Schedule'))
    time_list =[0]*24
    time_list[int(time)] = 1
    print("{:<18} {:<70}".format('Time', str(time_list)))
    for name in schedule.keys():
        schedule_app = schedule[name]
        print("{:<18} {:<70}".format(name, str(schedule_app)))

def total_price(totaal_verbruik,prijzen):
    total_price = 0
    for i in range(len(prijzen)):
        total_price += totaal_verbruik[i]*prijzen[i]

    return total_price

def sum_matrix(matrix):
    sum = 0
    for elem in matrix:
        sum += elem
    return sum

def variable_in_matrix(variable,matrix):
    # Gewone 'in' command lijkt niet te werken.

    for elem in matrix:
        if elem == variable:
            return True
    return False

def cumulatieve_som(i, array):

    sum = 0
    for j in range(0,i+1):
        sum += array[i]

    return sum

def get_values_others(other):
    values = []
    for i in other.value:
        values.append(float(i))
    return values

def get_values(machine,was_working, was_finished):
    new_matrix = []

    if was_working or was_finished:
        # print('get_values',machine.name,machine.matrix)
        return list(machine.matrix)
    else:
        for elem in machine.matrix:
            if isinstance(elem, int) or isinstance(elem,numpy.int32):
                new_matrix.append(elem)
            else:
                if isinstance(elem.value, type(None)):
                    print('NONE',machine.name, elem.value)
                # print(machine.name,elem.value)
                new_matrix.append(round(float(elem.value)))
        return new_matrix

def partial_sum(vector, startwaarde, eindwaarde):

    sum = 0

    for i in range(startwaarde, eindwaarde+1):
        sum += vector[i]

    return sum

def is_weekday():
    day = datetime.datetime.today().weekday()

    if day in range(0,5):
        return "week"
    else:
        return "weekend"

def windenergie(straal, windsnelheden, efficientie, luchtdichtheid = 1.29):

    output = []
    oppervlakte = math.pi * straal ** 2

    for i in windsnelheden:
        windvermogen = (0.5 * luchtdichtheid * i ** 3)
        werkelijkwindvermogen = efficientie * windvermogen
        generatorvermogen = oppervlakte * werkelijkwindvermogen

        output.append(round(generatorvermogen, 3)/1000)

    return output


def list_info(total_usage, opbrengst, prices, bat_inhoud, total, time=0):
    time = int(time)
    if isinstance(total_usage[0],float):
        list_tot_usage = total_usage
        list_bat = bat_inhoud
        list_tot = total
    else:
        list_bat = [bat_inhoud[0]] + [0] * (24 - time)
        list_tot_usage = [0] * (24 - time)
        list_tot = [0] * (24 - time)
        for i in range(0, 24 - time):
            list_bat[i + 1] += bat_inhoud[i + 1].value
            list_tot_usage[i] += total_usage[i].value
            list_tot[i] += total[i].value

    return list_tot_usage, opbrengst, prices, list_bat, list_tot


def func_plot(total_usage, opbrengst, prices, bat_inhoud, total, time=0):

    list_tot_usage, opbrengst, prices, list_bat, list_tot = list_info(total_usage, opbrengst, prices, bat_inhoud, total,time)

    prices_relative = [i for i in prices]
    prices_relative = numpy.array(prices_relative)
    prices_relative = (prices_relative - prices_relative.min()) / (prices_relative.max() - prices_relative.min()) *8
    prices_relative = list(prices_relative)
    # prices_total = [i * prices[time+i] for i in list_tot]


    plt.plot(list_tot_usage)
    plt.plot(opbrengst)
    plt.plot(prices_relative)
    plt.plot(list_bat)
    plt.plot(list_tot)
    # plt.plot(prices_total)
    # plt.legend(handles=)
    plt.show()




def auto(kilometer, max_batterij_inhoud, max_range):

    """
    https://www.egear.be/tesla-model-3/
    """

    return kilometer/max_range*max_batterij_inhoud

def zonne_energie(direct, diffuse, oppervlakte,rendement):

    output = []
    totale_radiatie = vector_sum(direct, diffuse)

    for i in totale_radiatie:
        vermogen = rendement * i * oppervlakte / 1000000000

        output.append(vermogen)

    return output

def verbruik_verwarming(duration, Tbui, Tbeg, Tend, start, end,elem=24):
    a = 105.84
    rho_l = 1.293
    Cp = 1005
    V = 360
    winst = 2.5
    for t in range(len(Tbui)):
        Tbui[t]+=273
    Tbeg+=273
    Tend+=273
    matrix = [0] * elem


    for t in range(start, start + duration):
        T_mom = Tbeg + (Tend - Tbeg) / duration * (t - start + 1)
        dQ = V * rho_l * Cp * (T_mom - Tbeg) / (3600 * (t - start + 1))
        Q_verlies = a * (T_mom - Tbui[t])

        W = (dQ + Q_verlies) / winst

        matrix[t] = W*10**(-3)

    for t in range(start + duration, end):
        W = a * (Tend - Tbui[t]) / winst
        matrix[t] = W*10**(-3)

    return matrix


def get_prev_workinghours(apparaat, prev_schedule, time=0):

    if not isinstance(time, int):
        time = int(time)

    schedule_apparaat = prev_schedule[apparaat]

    return sum(schedule_apparaat[:int(time)])


def was_working(apparaat, prev_schedule_full, random, time=0):

    time = int(time)
    if prev_schedule_full[apparaat][int(time)] == 1 or random[-1] == 1:
        return True
    else:
        return False

def was_finished_random(apparaat_name,apparaat_duration,prev_schedule,random,time):

    if sum(prev_schedule[apparaat_name][:int(time)]) == apparaat_duration and random[apparaat_name][-1] == 1:
        return True
    else:
        return False

def was_not_finished_random(apparaat_name,apparaat_duration,prev_schedule,random,time):

    if sum(prev_schedule[apparaat_name][:int(time)]) != apparaat_duration and random[apparaat_name][-1] == 1:
        print(apparaat_name,random[apparaat_name][-1])
        return True
    else:
        return False


    #### Nog eens goednakijken

### Optimalisatie

class Machine:
    def __init__(self, name, duration, usage, start, end):
        self.variable1 = cvxpy.Variable(boolean=True)
        self.variable2 = cvxpy.Variable(boolean=True)
        self.variable3 = cvxpy.Variable(boolean=True)
        self.variable4 = cvxpy.Variable(boolean=True)
        self.variable5 = cvxpy.Variable(boolean=True)
        self.variable6 = cvxpy.Variable(boolean=True)
        self.variable7 = cvxpy.Variable(boolean=True)
        self.variable8 = cvxpy.Variable(boolean=True)
        self.variable9 = cvxpy.Variable(boolean=True)
        self.variable10 = cvxpy.Variable(boolean=True)
        self.variable11 = cvxpy.Variable(boolean=True)
        self.variable12 = cvxpy.Variable(boolean=True)
        self.variable13 = cvxpy.Variable(boolean=True)
        self.variable14 = cvxpy.Variable(boolean=True)
        self.variable15 = cvxpy.Variable(boolean=True)
        self.variable16 = cvxpy.Variable(boolean=True)
        self.variable17 = cvxpy.Variable(boolean=True)
        self.variable18 = cvxpy.Variable(boolean=True)
        self.variable19 = cvxpy.Variable(boolean=True)
        self.variable20 = cvxpy.Variable(boolean=True)
        self.variable21 = cvxpy.Variable(boolean=True)
        self.variable22 = cvxpy.Variable(boolean=True)
        self.variable23 = cvxpy.Variable(boolean=True)
        self.variable24 = cvxpy.Variable(boolean=True)

        self.list = [self.variable1,self.variable2,self.variable3,self.variable4,self.variable5,\
                                   self.variable6,self.variable7,self.variable8,self.variable9,self.variable10,\
                                   self.variable11,self.variable12,self.variable13,self.variable14,self.variable15,\
                                   self.variable16,self.variable17,self.variable18,self.variable19,self.variable20,\
                                   self.variable21,self.variable22,self.variable23,self.variable24]

        self.name = name
        self.duration = duration
        self.usage = usage
        self.start = start
        self.end = end
        # if status == 'ON':
        if end > start:
            array = [0] * start
            for i in range(0, end - start):
                array.append(self.list[i])
            for i in range(0, 24-end):
                array.append(0)
        elif end < start:
            array = []
            for i in range(0, end):
                array.append(self.list[i])
            for i in range(0, start-end):
                array.append(0)
            for i in range(0, 24-start):
                array.append(self.list[end+i-1])
        else:
            array = [0] * 24

        self.matrix = numpy.array(array)
        self.variable_list = list(self.matrix)

        self.constraint = sum_matrix(self.matrix) == self.duration


def optimalisatie(prijzen, apparaten, opbrengst, bat_max_opladen=0, bat_max_afladen=0,
              bat_max_inhoud=0, prev_battery_inhoud=0, bettery_quota=0):

    ###Variabelen:


    bat_opladen = cvxpy.Variable(24)
    bat_afladen = cvxpy.Variable(24)
    bat_inhoud = [prev_battery_inhoud] + [0]*24

    ### hoofdconstraints

    constraints = []

    total = [0]*24
    total_usage = [0]*24
    for i in range(0, 24):
        for j in apparaten:
            if isinstance(j.usage,list) and len(j.usage) == 24:
                total_usage[i] += j.usage[i]*j.matrix[i]
            else:
                total_usage[i] += j.usage*j.matrix[i]
        bat_inhoud[i+1] = bat_inhoud[i] - bat_afladen[i] + bat_opladen[i]
        total[i] = total_usage[i] - opbrengst[i] - bat_afladen[i] + bat_opladen[i]

    for i in range(len(prijzen)):
        constraints.append(bat_inhoud[i+1] >= 0)
        constraints.append(bat_inhoud[i+1] <= bat_max_inhoud)
        constraints.append(total_usage[i] <= 10)
        constraints.append(0 <= bat_afladen[i])
        constraints.append(bat_afladen[i] <= bat_max_afladen)
        constraints.append(0 <= bat_opladen[i])
        constraints.append(bat_opladen[i] <= bat_max_opladen)

        constraints.append(total[i] >= 0)
        constraints.append(total[i] <= 12)
    constraints.append(bat_inhoud[-1] == bettery_quota)
    ### constraint apparaten

    for i in apparaten:
        constraints.append(i.constraint)
    for i in apparaten:
        if i.start < i.end:
            # print(i.name,"i.start < i.end:" )
            for j in range(i.start + 1, i.end):
                if i.duration != 0:
                    constraints.append(i.matrix[j] >= i.matrix[j - 1] - 1 / i.duration * partial_sum(i.matrix,
                                                                                             max(i.start,
                                                                                                 j - i.duration),
                                                                                             j - 1))
        else:
            # print(i.name,"i.start >= i.end:")
            for j in range(1, 24):
                if i.duration != 0:
                    constraints.append(i.matrix[j] >= i.matrix[j - 1] - 1 / i.duration * partial_sum(i.matrix,
                                                                                                 max(i.end,
                                                                                                     j - i.duration),
                                                                                                 j - 1))
    ### Objectieffunctie

    Prijs = 0

    for i in range(len(prijzen)):
        Prijs += prijzen[i] * (total[i])


    ### Optimalisatie
    print(constraints)

    obj = cvxpy.Minimize(Prijs)

    while constraints.count(True) > 0:
        constraints.remove(True)
    while constraints.count(False) > 0:
        constraints.remove(False)

    problem = cvxpy.Problem(obj, constraints)
    # problem = GLPK_MI.solve('GLPK_MI', obj,constraints,dict(),True,True,dict())
    # problem.solve(solver=cvxpy.GLPK_MI)
    problem.solve()

    print(problem.value)


    oplossing = dict()
    for i in apparaten:
        oplossing[i.name] = get_values(i,False,False)

    return oplossing, bat_inhoud, total_usage, bat_opladen,bat_afladen, total



class UpdatedMachine:
    def __init__(self, name, duration, usage, start, end, time=0, prev_schedule = None, randomon = {}):

        time = int(time)

        self.variable1 = cvxpy.Variable(boolean=True)
        self.variable2 = cvxpy.Variable(boolean=True)
        self.variable3 = cvxpy.Variable(boolean=True)
        self.variable4 = cvxpy.Variable(boolean=True)
        self.variable5 = cvxpy.Variable(boolean=True)
        self.variable6 = cvxpy.Variable(boolean=True)
        self.variable7 = cvxpy.Variable(boolean=True)
        self.variable8 = cvxpy.Variable(boolean=True)
        self.variable9 = cvxpy.Variable(boolean=True)
        self.variable10 = cvxpy.Variable(boolean=True)
        self.variable11 = cvxpy.Variable(boolean=True)
        self.variable12 = cvxpy.Variable(boolean=True)
        self.variable13 = cvxpy.Variable(boolean=True)
        self.variable14 = cvxpy.Variable(boolean=True)
        self.variable15 = cvxpy.Variable(boolean=True)
        self.variable16 = cvxpy.Variable(boolean=True)
        self.variable17 = cvxpy.Variable(boolean=True)
        self.variable18 = cvxpy.Variable(boolean=True)
        self.variable19 = cvxpy.Variable(boolean=True)
        self.variable20 = cvxpy.Variable(boolean=True)
        self.variable21 = cvxpy.Variable(boolean=True)
        self.variable22 = cvxpy.Variable(boolean=True)
        self.variable23 = cvxpy.Variable(boolean=True)
        self.variable24 = cvxpy.Variable(boolean=True)

        self.list = [self.variable1,self.variable2,self.variable3,self.variable4,self.variable5,\
                                   self.variable6,self.variable7,self.variable8,self.variable9,self.variable10,\
                                   self.variable11,self.variable12,self.variable13,self.variable14,self.variable15,\
                                   self.variable16,self.variable17,self.variable18,self.variable19,self.variable20,\
                                   self.variable21,self.variable22,self.variable23,self.variable24]

        self.name = name
        # print('prev_working hours',name,get_prev_workinghours(name, prev_schedule, time))
        self.duration = int(duration) - get_prev_workinghours(name, prev_schedule, time)
        self.duration2 = int(duration)
        # print(name,self.duration2,self.duration,usage)
        self.usage = usage
        self.start = int(start)
        self.end = int(end)
        self.time = int(time)
        # self.status = status
        #
        # if randomon == name:
        #     self.status = 'ON'

        # ### Als vaatwas eerst off staat maar dan random on, en dan ander apparaat random on, vaatwas niet meer on

        # if status == 'ON':
        # random_on_sum = sum(randomon[name])
        if was_finished_random(name, duration, prev_schedule, randomon, time):
            if self.duration2 + time > 24:
                duration_random = 24-time
                self.unworkedhours = self.duration2 - duration_random
                # print(name,self.unworkedhours)
                array = [1] * int(duration_random) + [0] * (
                            24 - time - duration_random)
                # print(self.name,random_on_sum)
            else:
                self.unworkedhours = 0
                # print(self.name,random_on_sum)
                # array = [1] * int((self.duration2 / (1 + random_on_sum))) + [0] * (
                #             24 - time - int((self.duration2 / (1 + random_on_sum))))
                array = [1] * int(self.duration2) + [0] * (
                            24 - time - int(self.duration2))

            # print('was_finished',name,array)
            # print(name,self.duration2)

        elif was_working(name, prev_schedule, randomon[name], time):

            array = [1]*self.duration + [0]*(24-time-self.duration)
            # print(name, 'was working',array)
        # elif self.duration == 0:
        #     print(name,'0')
        #     array = [0]*(24-time)

        elif was_not_finished_random(name, duration, prev_schedule, randomon, time):
            # array = [1] * int((self.duration2 / (1 + random_on_sum))) + [0] * (
            #         24 - time - int((self.duration2 / (1 + random_on_sum))))
            array = [1] * int(self.duration2) + [0] * (
                    24 - time - int(self.duration2))
            ### als het apparaat nog ingepland staat maar al vroeg opzet, moet de inplanning dan nog opnieuw gebeuren na de random on actie? of is het voldoende als het zo gewoon opstaat
        else:
            # print(name,'rest')
            if end > start:
                array = []
                if time > end:
                    for i in range(time, 24):
                        array.append(self.list[i])
                elif time >= start:
                    for i in range(time, end):
                        array.append(self.list[i])
                    for i in range(end, 24):
                        array.append(0)
                elif time < start:
                    for i in range(time, start):
                        array.append(0)
                    for i in range(start, end):
                        array.append(self.list[i])
                    for i in range(end, 24):
                        array.append(0)
                    # print('time>start',name,array)

            elif end < start:
                array = []
                if time > start:
                    for i in range(time, 24):
                        array.append(self.list[i])
                elif time < end:
                    for i in range(time, end):
                        array.append(self.list[i])
                    for i in range(end, start):
                        array.append(0)
                    for i in range(start, 24):
                        array.append(self.list[i])
                elif end < time <= start:
                    for i in range(time, start):
                        array.append(0)
                    for i in range(start, 24):
                        array.append(self.list[i])
            else:
                array = [0] * (24-time)

        # print(self.name,array,self.duration2)

        self.matrix = numpy.array(array)
        # print(name,self.matrix)
        self.variable_list = list(self.matrix)
        self.constraint = sum_matrix(self.matrix) == self.duration

class Variables:
    def __init__(self,time):
        self.variable1 = cvxpy.Variable(integer=True)
        self.variable2 = cvxpy.Variable(integer=True)
        self.variable3 = cvxpy.Variable(integer=True)
        self.variable4 = cvxpy.Variable(integer=True)
        self.variable5 = cvxpy.Variable(integer=True)
        self.variable6 = cvxpy.Variable(integer=True)
        self.variable7 = cvxpy.Variable(integer=True)
        self.variable8 = cvxpy.Variable(integer=True)
        self.variable9 = cvxpy.Variable(integer=True)
        self.variable10 = cvxpy.Variable(integer=True)
        self.variable11 = cvxpy.Variable(integer=True)
        self.variable12 = cvxpy.Variable(integer=True)
        self.variable13 = cvxpy.Variable(integer=True)
        self.variable14 = cvxpy.Variable(integer=True)
        self.variable15 = cvxpy.Variable(integer=True)
        self.variable16 = cvxpy.Variable(integer=True)
        self.variable17 = cvxpy.Variable(integer=True)
        self.variable18 = cvxpy.Variable(integer=True)
        self.variable19 = cvxpy.Variable(integer=True)
        self.variable20 = cvxpy.Variable(integer=True)
        self.variable21 = cvxpy.Variable(integer=True)
        self.variable22 = cvxpy.Variable(integer=True)
        self.variable23 = cvxpy.Variable(integer=True)
        self.variable24 = cvxpy.Variable(integer=True)

        self.list = [self.variable1, self.variable2, self.variable3, self.variable4, self.variable5, \
                     self.variable6, self.variable7, self.variable8, self.variable9, self.variable10, \
                     self.variable11, self.variable12, self.variable13, self.variable14, self.variable15, \
                     self.variable16, self.variable17, self.variable18, self.variable19, self.variable20, \
                     self.variable21, self.variable22, self.variable23, self.variable24]
        self.matrix = self.list[time:]
        self.array = numpy.array(self.matrix)


def optimalisatierandomon2(prijzen, opbrengst, apparaten, prev_schedule_full, random,bat_max_opladen = 0, bat_max_inhoud = 0,bat_max_afladen=0, time = 0, prev_battery_inhoud = 0):

    time = int(time)


    ###Variabelen:

    bat_opladen = Variables(int(time))
    bat_afladen = Variables(int(time))
    bat_inhoud = [prev_battery_inhoud] + [0]*(24-time)

    ### hoofdconstraints

    constraints = []

    total = [0]*(24-time)
    total_usage = [0]*(24-time)

    for i in range(0, 24-time):
        for j in apparaten:
            if isinstance(j.usage,list) and len(j.usage) == 24:
                total_usage[i] += j.usage[i]*j.matrix[i]
            else:
                total_usage[i] += j.usage*j.matrix[i]
        bat_inhoud[i+1] = bat_inhoud[i] - bat_afladen.matrix[i] + bat_opladen.matrix[i]
        total[i] = total_usage[i] - opbrengst[time + i] - bat_afladen.matrix[i] + bat_opladen.matrix[i]


    for i in range(0,24-time):
        constraints.append(bat_inhoud[i+1] >= 0)
        constraints.append(bat_inhoud[i+1] <= bat_max_inhoud)
        constraints.append(total_usage[i] <= 10)
        constraints.append(0 <= bat_afladen.matrix[i])
        constraints.append(bat_afladen.matrix[i] <= bat_max_afladen)
        constraints.append(0 <= bat_opladen.matrix[i])
        constraints.append(bat_opladen.matrix[i] <= bat_max_opladen)

        constraints.append(total[i] >= 0)

    ### constraint apparaten

    for i in apparaten:
        was_finished2 = was_finished_random(i.name,i.duration2,prev_schedule_full,random,time)
        was_working2 = was_working(i.name,prev_schedule_full,random[i.name],time)

        if was_finished2 == False and was_working2 == False:
            constraints.append(i.constraint)
        print(i.name,i.constraint)

    for i in apparaten:
        if i.start < i.end:
            for j in range(1, 24-time):
                if i.duration != 0:
                    constraints.append(i.matrix[j] >= i.matrix[j - 1] - 1 / i.duration2 * partial_sum(i.matrix,
                                                                                                     max(
                                                                                                         i.start,
                                                                                                         j - i.duration2),
                                                                                                     j - 1))
        else:
            print(i.name, "i.start >= i.end:")
            for j in range(1, 24-time):
                if i.duration != 0:
                    constraints.append(i.matrix[j] >= i.matrix[j - 1] - 1 / i.duration2 * partial_sum(i.matrix,
                                                                                                     max(i.end,
                                                                                                         j - i.duration2),
                                                                                                     j - 1))
                    print(i.name, "i.start >= i.end:",i.matrix[j] >= i.matrix[j - 1] - 1 / i.duration2 * partial_sum(i.matrix,
                                                                                                     max(i.end,
                                                                                                         j - i.duration2),
                                                                                                     j - 1))

    ### Objectieffunctie

    Prijs = 0

    for i in range(0,24-time):
        Prijs += prijzen[time + i] * total[i]

    ### Optimalisatie
    print('Prijs',Prijs)
    obj = cvxpy.Minimize(Prijs)
    # print('dcp obj',obj.is_dcp())
    while constraints.count(True) > 0:
        constraints.remove(True)
    while constraints.count(False) > 0:
        constraints.remove(False)

    # for i in constraints:
    #     print(i,i.is_dcp())

    problem = cvxpy.Problem(obj, constraints)

    # problem.solve(solver='glpk_mi')
    problem.solve()
    print(problem.get_data())
    price = problem.value
    print(price)
    print(problem.status)

    ### Aangepast naar dict
    oplossing = dict()
    for i in apparaten:
        was_finished2 = was_finished_random(i.name,i.duration2,prev_schedule_full,random,time)
        was_working2 = was_working(i.name,prev_schedule_full,random[i.name],time)
        oplossing[i.name] = get_values(i, was_working2,was_finished2)

    return oplossing, bat_inhoud, total_usage, bat_opladen,bat_afladen, total
