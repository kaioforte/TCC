
import numpy as np
import pandas as pd
import os


def arrival_48h_rand(number_ev, t_initial, t_final):
    t_initial = t_initial/(1/6)
    t_final = t_final/(1/6)
    rng = np.random.default_rng(12345)
    t_arr = rng.integers(low=t_initial, high=t_final+1, size=number_ev)

    return t_arr

def arrival(number_ev):
    rng = np.random.default_rng(123)
    rand = rng.integers(low=1, high=64574, size=number_ev)
    t_arr = pd.read_excel(r"C:\Users\kaioh\Documents\Universidade\TCC\Python\Input\weekday_time_of_arrival.xlsx", header=None)[0][rand]
    print(t_arr)
    t_arr = round(t_arr/(1/6)).astype(int)
    return t_arr

def departure_48h_rand(number_ev, t_initial, t_final):
    t_initial = (t_initial + 24)/(1/6)
    t_final = (t_final+24)/(1/6)
    rng = np.random.default_rng(12346)
    t_dep = rng.integers(low=t_initial, high=t_final+1, size=number_ev)
    t_dep = [x-1 for x in t_dep]

    return t_dep


def ev_48h_profile(number_ev, t_arr, t_dep):

    array = [[] for i in range(288)]
    for i in range(number_ev):
        for t in range(t_arr[i], t_dep[i]+1, 1):
            array[t].append(i)

    return array


def tariff_48h(t1, t2, t3, t4, c1, c2, c3):
    t1, t2, t3, t4 = int(t1/(1/6)), int(t2/(1/6)), int(t3/(1/6)), int(t4/(1/6))
    array = np.zeros(288)
    for i in range(0, t1):
        array[i] = c1
    for i in range(t1, t2):
        array[i] = c2
    for i in range(t2, t3):
        array[i] = c3
    for i in range(t3, t4):
        array[i] = c2
    for i in range(t4, 288):
        array[i] = c1

    return array

def ev_loadshape_optimized(number_ev, pow_EV_var, tempo):
    ev = []
    for i in range(number_ev):
        ev.append([])
        for t in tempo:
            if (t,i) in pow_EV_var and pow_EV_var[(t,i)].varValue != 0.0:
                ev[i].append(round(pow_EV_var[(t, i)].varValue*-1/7.7, 2))
            else:
                ev[i].append(0.0)
    return ev

def ev_loadshape(t_arr, number_ev, tempo):
    loadshape = np.zeros((number_ev, len(tempo)), dtype = float)
    
    for i in range(number_ev):
        loadshape[i, t_arr[i]] = -5.27895/7.7
        loadshape[i, t_arr[i]+1:t_arr[i]+20] = -1
    
    return loadshape

def save_figure(number_ev, tempo, ev_loadshape_nonoptimized, pow_base, pow_opendss, t_dep, plt, ev, ev_power, path):

    pot_charge = np.zeros(288)
    # pow_opendss = np.zeros(288)
    soc = np.zeros((number_ev, 288))
    soc[ : : ] = np.nan
    pot_per_car = np.zeros((number_ev, 288))

    for t in tempo:
        for i in range(number_ev):
            if ev_loadshape_nonoptimized[i,t] != 0:
                pot_charge[t] += ev_loadshape_nonoptimized[i,t]*-7.7

    # pow_opendss = np.genfromtxt(r"C:\Users\kaioh\Documents\TCC\Python\OpenDSS\Circuito_exemplo\DI_yr_0\DI_SystemMeter_1.CSV", delimiter=',', dtype=float, skip_header=1,usecols=1)

    for t in tempo:
        for i in range(number_ev):
            if ev_loadshape_nonoptimized[i,t] != 0:
                pot_per_car[i, t] = ev_loadshape_nonoptimized[i,t]*-7.7

    for t in tempo:
        for i in range(number_ev):
            if 7.7 > pot_per_car[i, t] > 0:    
                soc[i, t] = 20
            elif pot_per_car[i, t] == 7.7:    
                soc[i, t] = soc[i, t-1] + pot_per_car[i, t-1]*(95*(1/6)/40)
            elif soc[i, t-1] > 76 and t < t_dep[i]:
                soc[i, t] = 80

    plt.figure(figsize = (13,4.5), dpi = 300)
    plt.suptitle('Non Optimized - ' + str(number_ev) + ' EVs', fontsize=16)
    plt.axvspan(0, 105, facecolor='limegreen', alpha=0.1, label='Horário fora de ponta')
    plt.axvspan(105, 111, facecolor='yellow', alpha=0.2, label='Horário intermediário')
    plt.axvspan(111, 129, facecolor='red', alpha=0.1, label='Horário de ponta')
    plt.axvspan(129, 135, facecolor='yellow', alpha=0.2)
    plt.axvspan(135, 288, facecolor='limegreen', alpha=0.1)

    plt.plot(tempo, pow_opendss, 'y',label='Pot Total (kVA)')
    plt.plot(tempo, ev, "b",label='Pot dos Veículos (kW)')
    plt.plot(tempo, pow_base, 'green', linestyle='--',label='Pot das Cargas Residenciais (kVA)')
    plt.axhline(112.5, color="black", linestyle="--")
    plt.title('Curva de Carga')
    plt.ylabel('Potência em kW')
    plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
    plt.ylim(0, 200)
    plt.legend(loc='upper right', prop={'size': 10}, framealpha=1)
    plt.margins(x=0)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(rf"{path}\Curva_de_Carga_Non_Optimized.jpg")
    plt.close()

    for i in range(number_ev):
        plt.figure(figsize = (13,6), dpi = 300)
        plt.subplot(2, 1, 1)
        plt.title(f'Potência de Carregamento do Carro {i+1} - Non Optimized', fontsize=14)
        plt.plot(tempo, ev_power[i],label=f'Carro {i}')
        plt.ylabel('Potência em kW')
        plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
        plt.ylim(0, 8.5)
        plt.margins(x=0)
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.title(f'SOC do Carro {i+1} - Non Optimized', fontsize=14)
        plt.plot(tempo, soc[i],label=f'Carro {i}')
        plt.ylabel('%')
        plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
        plt.ylim(10, 90)
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(rf"{path}\Charging_Power_SOC_Non_Optimized_Car"+ f"{i}.jpg")
        plt.close()

def save_figure_optimized(number_ev, tempo, pow_base, pow_opendss, plt, pow_tot_var, ev_profile, pow_EV_var, state_of_charge_var, ev, ev_power, path):
    
    soc = np.zeros((number_ev, 288))
    soc[ : : ] = np.nan
    for t in tempo:
        for i in ev_profile[t]:    
            soc[i, t] = state_of_charge_var[(t, i)].varValue
    
            
    
    plt.figure(figsize = (13,4.5), dpi = 300)
    plt.suptitle('Optimized - ' + str(number_ev) + ' EVs', fontsize=16)

    plt.axvspan(0, 105, facecolor='limegreen', alpha=0.1, label='Horário fora de ponta')
    plt.axvspan(105, 111, facecolor='yellow', alpha=0.2, label='Horário intermediário')
    plt.axvspan(111, 129, facecolor='red', alpha=0.1, label='Horário de ponta')
    plt.axvspan(129, 135, facecolor='yellow', alpha=0.2)
    plt.axvspan(135, 288, facecolor='limegreen', alpha=0.1)
    plt.plot(tempo, pow_opendss, 'y',label='Pot Total (kVA)')
    # plt.plot(tempo, pot_tot, 'r', label='Pot Calculada')
    plt.plot(tempo, ev, "b", label='Pot dos Veículos (kW)')
    plt.plot(tempo, pow_base, 'green', linestyle='--',label='Pot das Cargas Residenciais (kVA)')
    plt.axhline(112.5, color="black", linestyle="--")
    plt.title('Curva de Carga')
    plt.ylabel('Potência em kW')
    plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
    plt.ylim(0, 200)
    plt.legend(loc='upper right', prop={'size': 10}, framealpha=1)
    plt.margins(x=0)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(rf"{path}\Curva_de_Carga_Optimized.jpg")
    plt.close()
    
    for i in range(number_ev):
        plt.figure(figsize = (13,6), dpi = 300)
        
        plt.subplot(2, 1, 1)
        plt.title(f'Potência de Carregamento do Carro {i+1} - Optimized', fontsize=14)
        plt.plot(tempo, ev_power[i],label=f'Carro {i}')
        plt.ylabel('Potência em kW')
        plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
        plt.ylim(0, 8.5)
        plt.margins(x=0)
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.title(f'SOC do Carro {i+1} - Optimized', fontsize=14)
        plt.plot(tempo, soc[i],label=f'Carro {i}')
        plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
        plt.ylabel('%')
        plt.ylim(10, 90)
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(rf"{path}\Charging_Power_SOC_Optimized_Car"+ f"{i}.jpg")
        plt.close()

def voltage_figure(all_voltages_per_node, bus_names, tempo, plt, y, number_ev, path):
    for j in range(0, 150, 3):
        plt.figure(figsize = (13.8,7), dpi = 150)
        plt.title(y + " - " + bus_names[int(j/3)])
        plt.plot(tempo, all_voltages_per_node[j], 'k',label='V1')
        plt.plot(tempo, all_voltages_per_node[j+1], 'b',label='V2')
        plt.plot(tempo, all_voltages_per_node[j+2], 'r',label='V3')
        plt.axhline(1.05, color="black", linestyle="--")
        plt.axhline(0.95, color="black", linestyle="--")
        plt.ylabel('Tensão(V)')
        plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
        plt.ylim(0.86, 1.06)
        plt.legend(loc='upper right', prop={'size': 10})
        plt.grid(True)
        plt.savefig(rf"{path}\Voltage"+f"_{y}_{bus_names[int(j/4)]}.jpg")
        plt.close()