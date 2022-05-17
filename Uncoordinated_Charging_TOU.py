import numpy as np
import py_dss_interface
import csv
from EV_Description_OpenDSS import ev_buses
from OpenDSS_function import circuit_solver, base_case
from EV_profile import arrival, tariff_48h, departure_48h_rand, ev_loadshape
import matplotlib.pyplot as plt
plt.style.use('.\matplot_tcc.mplstyle')

def optimization_uc_tou(number_ev):
    ### SETS ###
    tempo = np.arange(288)

    # t_arr = arrival_48h_rand(number_ev, 17, 20)
    t_arr = arrival(number_ev).tolist()

    # Tarifa Convencional e Tarifa Branca - CPFL Ijuí/RS
    # c = np.full(288, 0.35850)
    c = tariff_48h(17.5, 18.5, 21.5, 22.5, 0.23604, 0.48095, 0.72587)

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

    path_custo = rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_TOU\custo_tou_{number_ev}.txt"     
    with open(path_custo, 'w') as f:
        f.write(f'{number_ev} carros:\n')
        f.write(f'Custo de Energia = {np.sum(total_active_power * c)}\n')
        f.write(f'Custo de Carregamento dos Veículos = {np.sum(c*ev)}\n')
        f.write(f'Fator de Carga para 48h = {np.sum(total_active_power*(1/6))/(48*max(total_active_power))}\n\n')
    f.close()

    return total_power, voltages, buses

# total_power_9, voltages_9, buses_9 = optimization_uc_tou(9)
# total_power_27, voltages_27, buses_27 = optimization_uc_tou(31)
# total_power_44, voltages_44, buses_44 = optimization_uc_tou(44)

# with open(r"C:\Users\kaioh\Documents\TCC\Python\Input\LoadShape48h_DemMed.csv", newline='') as f:
#     reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
#     pow_houses = list(reader)
# f.close()

# dss = py_dss_interface.DSSDLL()
# pow_base = base_case(dss, pow_houses)

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
# plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_TOU\Curva_de_Carga_UC_TOU_Artigo")
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
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Uncoordinated_Charging_TOU\Curva_de_Tensão_{barra}")
#     plt.close()