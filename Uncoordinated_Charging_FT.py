import numpy as np
import py_dss_interface
import csv
from EV_Description_OpenDSS import ev_buses
from OpenDSS_function import circuit_solver, base_case
from EV_profile import arrival, tariff_48h, departure_48h_rand, ev_loadshape
import matplotlib.pyplot as plt
plt.style.use('.\matplot_tcc.mplstyle')

def optimization_uc_ft(number_ev):
    ### SETS ###
    tempo = np.arange(288)

    # t_arr = arrival_48h_rand(number_ev, 17, 20)
    t_arr = arrival(number_ev).tolist()
    t_dep = departure_48h_rand(number_ev, 5, 6)

    # Tarifa Convencional e Tarifa Branca - CPFL Ijuí/RS
    c = np.full(288, 0.35850)
    # c = tariff_48h(17.5, 18.5, 21.5, 22.5, 0.23604, 0.48095, 0.72587)

    # pow_houses = pd.read_csv(r"C:\Users\kaioh\Documents\TCC\Python\Input\LoadShape48h_DemMed.csv", sep=';', header=None)
    with open(r"C:\Users\kaioh\Documents\TCC\Python\Input\LoadShape48h_DemMed.csv", newline='') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        pow_houses = list(reader)
    f.close()

    dss = py_dss_interface.DSSDLL()
    
    ev_bus = ev_buses(number_ev).tolist()
    
    # Caso Base sem otimização
    ev_loadshape_nonoptimized = ev_loadshape(t_arr, number_ev, tempo)
    total_power, buses, voltages, total_active_power, ev, ev_power = circuit_solver(dss, pow_houses, number_ev, ev_loadshape_nonoptimized.tolist(), ev_bus)
    
    path_custo = rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_FT\custo_ft_{number_ev}.txt"     
    with open(path_custo, 'w') as f:
        f.write(f'{number_ev} carros:\n')               
        f.write(f'Fator de Carga para 48h = {np.sum(total_active_power*(1/6))/(48*max(total_active_power))}\n\n')
        f.write(f'Fator de Carga para 6h - 6h = {np.sum(total_active_power[36:181]*(1/6))/(24*max(total_active_power[36:181]))}\n\n')
        f.write(f'Custo de Carregamento dos Veículos = {np.sum(c*ev)}\n')
        f.write(f'Custo de Energia = {np.sum(total_active_power * c)}\n')
    f.close()

    soc = np.zeros((number_ev, 288))
    soc[ : : ] = np.nan
    for t in tempo:
        for i in range(number_ev):
            if t == t_arr[i]-1:
                soc[i][t] = 20
            elif 7.71 > ev_power[i][t] > 5.15:    
                soc[i][t] = soc[i][t-1] + ev_power[i][t]*(95*(1/6)/40)
            elif soc[i][t-1] > 79 and t < t_dep[i]:
                soc[i][t] = 80

    return total_power, ev_power, soc, voltages, buses

# with open(r"C:\Users\kaioh\Documents\TCC\Python\Input\LoadShape48h_DemMed.csv", newline='') as f:
#     reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
#     pow_houses = list(reader)
# f.close()
# # pow_base = np.sum(np.array(pow_houses), axis = 0)

# dss = py_dss_interface.DSSDLL()
# pow_base, bus_base, voltages_base = base_case(dss, pow_houses)

# total_power_9, ev_power, soc, voltages_9, buses_9 = optimization_uc_ft(9)
total_power_27, ev_power, soc, voltages_27, buses_27 = optimization_uc_ft(31)
# total_power_44, ev_power, soc, voltages_44, buses_44 = optimization_uc_ft(44)

tempo=np.arange(288)

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
# plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_FT\Curva_de_Carga_Artigo.png")
# plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_FT\Curva_de_Carga_Artigo.svg")
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
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_FT\Curva_de_Tensão_{barra}")
#     plt.close()

plt.figure(figsize = (10,7), dpi = 300)
plt.subplot(2, 1, 1)
for i in range(31):
    plt.plot(tempo, ev_power[i], linestyle='-')
plt.title(f'(a)', fontsize=22)
plt.ylabel('Potência (kW)')
# plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
plt.xticks(np.arange(0, 289, 12), ('0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24'))
plt.yticks(np.arange(0, 11, 2.5), ('0', '2.5', '5', '7.5', '10'))
plt.xlim(0, 288)
plt.ylim(0, 10)
# plt.legend(loc='upper right',title="Penetração de VE", prop={'size': 12}, framealpha=1)
plt.margins(x=0)
plt.grid(True)

plt.subplot(2, 1, 2)
for i in range(31):
    plt.plot(tempo, soc[i], linestyle='-')
plt.title(f'(b)', fontsize=22)
# plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
plt.xticks(np.arange(0, 289, 12), ('0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24'))
plt.xlim(0, 288)
plt.margins(x=0)
plt.ylabel('SOC (%)')
plt.xlabel('Tempo (h)')
plt.ylim(0, 100)
plt.yticks(np.arange(0, 101, 20), ('0', '20', '40', '60', '80', '100'))
plt.grid(True)

plt.tight_layout()
plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_FT\SOC_Artigo.png")
plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_FT\SOC_Artigo.svg")
plt.close()

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
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_FT\Voltages\Perfil_de_Tensão_{buses_9[int(j/3)]}.png")
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_FT\Voltages\Perfil_de_Tensão_{buses_9[int(j/3)]}.svg")
#     plt.close()