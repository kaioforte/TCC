import pulp as pl
import numpy as np
import py_dss_interface
import csv
from EV_Description_OpenDSS import ev_buses
from OpenDSS_function import circuit_solver, base_case
from EV_profile import arrival, departure_48h_rand, ev_48h_profile, tariff_48h, ev_loadshape_optimized, ev_loadshape, save_figure, voltage_figure, save_figure_optimized
import matplotlib.pyplot as plt
plt.style.use('.\matplot_tcc.mplstyle')

def optimization_ft(number_ev):
    ### SETS ###
    tempo = np.arange(288)

    ### PARAMETERS ###
    charg_eff = 0.95
    delta_t = 10/60
    bat_cap = 40

    # t_arr = arrival_48h_rand(number_ev, 17, 20)
    t_arr = arrival(number_ev).tolist()
    t_dep = departure_48h_rand(number_ev, 5, 6)

    # Tarifa Convencional e Tarifa Branca - CPFL Ijuí/RS
    c = np.full(288, 0.35850)
    

    ev_profile = ev_48h_profile(number_ev, t_arr, t_dep)
    print(ev_profile)

    # pow_houses = pd.read_csv(r"C:\Users\kaioh\Documents\TCC\Python\Input\LoadShape48h_DemMed.csv", sep=';', header=None)
    with open(r"C:\Users\kaioh\Documents\TCC\Python\Input\LoadShape48h_DemMed.csv", newline='') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        pow_houses = list(reader)
    f.close()
    # pow_base = pow_houses.sum(axis = 0)
    pow_base = np.sum(np.array(pow_houses), axis = 0)

    reactive_power = np.sin(np.arccos(0.9)) * pow_base


    ### PROBLEM TYPE ###
    prob = pl.LpProblem("ChargingScheduling", pl.LpMinimize)


    ### DECISION VARIABLES ###
    ## Potência Total
    pow_tot_var = pl.LpVariable.dicts("TotalPower", tempo, 0)

    ## Potência de Carregamento do EV
    pow_EV_var = pl.LpVariable.dicts("EVChargingPower", [(t, i) for t in tempo 
                                                            for i in ev_profile[t]],
                                                    0, 7.7)

    pow_EV_var_t = pl.LpVariable.dicts("EVChargingPower_t", tempo, 0, number_ev*7.7)

    ## SOC das Baterias
    state_of_charge_var = pl.LpVariable.dicts("StateOfCharge", [(t, i) for t in tempo 
                                                                    for i in ev_profile[t]],
                                                            20, 100)


    ### optimization_ft PROBLEM ###
    ## Função Objetivo - Somatório da Potência Total x tarifa no tempo
    prob += pl.lpSum(pow_tot_var[t] * (1/6) * c[t] for t in tempo)


    ### CONSTRAINTS ###

    for t in tempo:
        prob += pow_tot_var[t] <= np.sqrt((0.91*112.5)**2 - reactive_power[t]**2)

    ## Potência Total = Potência Base + Somatório das Potências de Carregamento
    for t in tempo:
        prob += pow_tot_var[t] == pow_base[t] + pl.lpSum(pow_EV_var[(t, i)] for i in ev_profile[t])

    ## SoC(atual) = SoC(passado) + Energia de Carregamento em DeltaT
    for t in tempo:
        for i in ev_profile[t]:
            ## Este if serve para garantir que o SoC(passado) de um EV que acabou de chegar seja igual a 20%
            if t == t_arr[i]:
                prob += state_of_charge_var[(t, i)] == 20
                continue
            prob += state_of_charge_var[(t, i)] == state_of_charge_var[(t-1, i)] + ((100*charg_eff*delta_t/bat_cap)*pow_EV_var[(t, i)])

    ## SoC(departure) = 100%
    for t in tempo:
        for i in ev_profile[t]:
            if t == t_dep[i]:
                prob += state_of_charge_var[(t, i)] >= 80

    for t in tempo:
        prob += pow_EV_var_t[t] == pl.lpSum(pow_EV_var[(t, i)] for i in ev_profile[t])


    ### SOLVER - GLPK ###
    prob.solve(solver=pl.GLPK_CMD(msg=False))
    print("Status: ", pl.LpStatus[prob.status])
    dss = py_dss_interface.DSSDLL()
    
    ev_bus = ev_buses(number_ev).tolist()
    
    total_power, buses, voltages, total_active_power, ev, ev_power = circuit_solver(dss, pow_houses, number_ev, ev_loadshape_optimized(number_ev, pow_EV_var, tempo), ev_bus)
    
    path_custo = rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Coordinated_Charging_FT\custo_{number_ev}.txt"     
    with open(path_custo, 'w') as f:
        f.write(f'{number_ev} carros:\n')        
        f.write(f'Fator de Carga para 48h = {np.sum(total_active_power*(1/6))/(48*max(total_active_power))}\n\n')
        f.write(f'Fator de Carga para 6h - 6h = {np.sum(total_active_power[36:181]*(1/6))/(24*max(total_active_power[36:181]))}\n\n')
        f.write(f'Custo de Carregamento dos Veículos = {np.sum(c*ev)}\n')
        f.write(f'Custo de Energia = {np.sum(total_active_power * c)}\n')
    f.close()

    if not all(power <= 112.5 for power in total_power):
        print("não conseguiu otimizar somente com 1 run")
    
    soc = np.zeros((number_ev, 288))
    soc[ : : ] = np.nan
    for t in tempo:
        for i in ev_profile[t]:    
            soc[i, t] = state_of_charge_var[(t, i)].varValue

    return total_power, ev_power, soc, voltages, buses

# with open(r"C:\Users\kaioh\Documents\TCC\Python\Input\LoadShape48h_DemMed.csv", newline='') as f:
#     reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
#     pow_houses = list(reader)
# f.close()

# dss = py_dss_interface.DSSDLL()
# pow_base, bus_base, voltages_base = base_case(dss, pow_houses)

# total_power_9, ev_power9, soc9, voltages_9, buses_9 = optimization_ft(9)
# total_power_27, ev_power27, soc27, voltages_27, buses_27 = optimization_ft(31)
total_power_44, ev_power44, soc44, voltages_44, buses_44 = optimization_ft(44)

# tempo=np.arange(288)

# plt.figure(figsize = (10,5), dpi = 300)
# plt.plot(tempo, total_power_9, label='10%')
# plt.plot(tempo, total_power_27, linestyle='-', label='35%')
# plt.plot(tempo, total_power_44, linestyle='-', label='50%')
# plt.plot(tempo, pow_base, 'tab:red', linestyle='--', label='Caso Base')
# plt.ylabel('Potência (kVA)')
# plt.xlabel('Tempo (h)')
# plt.axhline(112.5, color="black", linestyle="--")
# plt.text(3, 125, 'capacidade nominal', fontsize=22, va='center', ha='left')
# #plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
# plt.xticks(np.arange(0, 289, 12), ('0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24'))
# plt.xlim(0, 288)
# plt.legend(loc='upper right', framealpha=1)
# plt.ylim(0, 200)
# plt.margins(x=0)
# plt.grid(True)
# plt.tight_layout()
# plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Coordinated_Charging_FT\Curva_de_Carga_Artigo.svg")
# plt.close()

# ### Barras dos carro 0-8 --->'barra24.1', 'barra14.2', 'barra49.1', 'barra47.3', 'barra6.1', 'barra11.2', 'barra12.1', 'barra11.1', 'barra22.1'
# indices = [(np.where(buses_9 =='barra24')[0][0] * 3), (np.where(buses_9 =='barra14')[0][0] * 3) + 1, (np.where(buses_9 =='barra49')[0][0] * 3), (np.where(buses_9 =='barra47')[0][0] * 3) + 2, (np.where(buses_9 =='barra6')[0][0] * 3), (np.where(buses_9 =='barra11')[0][0] * 3) + 1, (np.where(buses_9 =='barra12')[0][0] * 3), (np.where(buses_9 =='barra11')[0][0] * 3), (np.where(buses_9 =='barra22')[0][0] * 3)]
# barras = ['barra24-1', 'barra14-2', 'barra49-1', 'barra47-3', 'barra6-1', 'barra11-2', 'barra12-1', 'barra11-1', 'barra22-1']

# for iter, barra in zip(indices, barras):
    
#     plt.figure(figsize = (13, 6), dpi = 300)
#     plt.plot(tempo, voltages_9[iter], label='10%')
#     plt.plot(tempo, voltages_27[iter], linestyle='-', label='35%')
#     plt.plot(tempo, voltages_44[iter], linestyle='-', label='50%')
#     plt.axhline(1.05, color="black", linestyle="--")
#     plt.axhline(0.95, color="black", linestyle="--")
#     plt.ylabel('Tensão [PU]')
#     plt.xlabel('Tempo')
#     plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
#     plt.ylim(0.86, 1.06)
#     plt.legend(loc='upper right',title="Penetração de VE", prop={'size': 12}, framealpha=1)
#     plt.margins(x=0)
#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Coordinated_Charging_FT\Curva_de_Tensão_{barra}")
#     plt.close()

# for i in range(9):
#     plt.figure(figsize = (10,7), dpi = 300)
#     plt.subplot(2, 1, 1)
#     plt.title(f'(a)', fontsize=22)
#     plt.plot(tempo, ev_power9[i], linestyle='-', label='10%')
#     plt.plot(tempo, ev_power27[i], linestyle='-', label='35%')
#     plt.plot(tempo, ev_power44[i], linestyle='-', label='50%')
#     plt.ylabel('Potência (kW)')
#     # plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
#     plt.xticks(np.arange(0, 289, 12), ('0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24'))
#     plt.yticks(np.arange(0, 11, 2.5), ('0', '2.5', '5', '7.5', '10'))
#     plt.xlim(0, 288)
#     plt.ylim(0, 10)
#     plt.legend(loc='upper right', framealpha=1)
#     plt.margins(x=0)
#     plt.grid(True)

#     plt.subplot(2, 1, 2)
#     plt.title(f'(b)', fontsize=22)
#     plt.plot(tempo, soc9[i], linestyle='-', label='10%')
#     plt.plot(tempo, soc27[i], linestyle='-', label='35%')
#     plt.plot(tempo, soc44[i], linestyle='-', label='50%')
#     plt.xticks(np.arange(0, 289, 12), ('0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24'))
#     plt.xlim(0, 288)
#     plt.margins(x=0)
#     plt.ylabel('SOC (%)')
#     plt.xlabel('Tempo (h)')
#     plt.ylim(0, 100)
#     plt.yticks(np.arange(0, 101, 20), ('0', '20', '40', '60', '80', '100'))
#     plt.grid(True)

#     plt.tight_layout()
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Coordinated_Charging_FT\Charging_Power_SOC_Optimized_Car_Artigo"+ f"{i+1}.png")
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Coordinated_Charging_FT\Charging_Power_SOC_Optimized_Car_Artigo"+ f"{i+1}.svg")
#     plt.close()

# for j in range(0, 150, 3):
#     plt.figure(figsize = (10, 5.5), dpi = 300)
#     plt.plot(tempo, voltages_9[j], label='10%')
#     plt.plot(tempo, voltages_27[j], linestyle='-', label='35%')
#     plt.plot(tempo, voltages_44[j], linestyle='-', label='50%')
#     plt.plot(tempo, voltages_base[j], 'tab:red', linestyle='--', label='Caso Base')
#     plt.axhline(1.05, color="black", linestyle="--")
#     plt.axhline(0.92, color="black", linestyle="--")
#     plt.ylabel('Tensão (PU)')
#     plt.xlabel('Tempo (h)')
#     plt.xticks(np.arange(0, 289, 12), ('0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24'))
#     plt.xlim(0, 288)
#     plt.text(3, 0.93, 'Limite Mínimo', fontsize=22, va='center', ha='left')
#     plt.text(3, 1.04, 'Limite Máximo', fontsize=22, va='center', ha='left')
#     plt.ylim(0.86, 1.06)
#     plt.legend(loc='lower right', framealpha=1)
#     plt.margins(x=0)
#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Coordinated_Charging_FT\Voltages\Perfil_de_Tensão_{buses_9[int(j/3)]}.png")
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Coordinated_Charging_FT\Voltages\Perfil_de_Tensão_{buses_9[int(j/3)]}.svg")
#     plt.close()



