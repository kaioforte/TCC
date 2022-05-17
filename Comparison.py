from Uncoordinated_Charging_TOU import optimization_uc_tou
from Coordinated_Charging_FT import optimization_ft
from Coordinated_Charging_TOU import optimization_tou
import py_dss_interface
from OpenDSS_function import base_case
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('.\matplot_tcc.mplstyle')
import csv

def number_deviations(voltages):
    k = 0
    for n in range(0,150,3):
        if ((np.any(voltages[n]<0.92)) | (np.any(voltages[n+1]<0.92)) | (np.any(voltages[n+2]<0.92))):
            #print(f"({n}, {n+1}, {n+2})")

            # print(buses[int(n/3)])
            k = k + 1
    return k

# with open(r"C:\Users\kaioh\Documents\TCC\Python\Input\LoadShape48h_DemMed.csv", newline='') as f:
#     reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
#     pow_houses = list(reader)
# f.close()
# # pow_base = np.sum(np.array(pow_houses), axis = 0)

# dss = py_dss_interface.DSSDLL()
# pow_base, bus_base, voltages_base = base_case(dss, pow_houses)

# tempo = np.arange(288)

# penetration = {0:0, 4:5, 9:10, 13:15, 18:20, 22:25, 26:30, 31:35, 35:40, 40:45, 44:50, 48:55, 53:60}
# penetration = {9:10, 31:35, 44:50}
penetration = {9:10, 31:35, 44:50, 53:60}

deviations_uc = np.zeros(4)
deviations_ft = np.zeros(4)
deviations_tou = np.zeros(4)

for keys, it in zip(penetration, range(len(penetration))):
    total_power_uc_tou, voltages_uc_tou, buses_uc_tou = optimization_uc_tou(keys)
    total_power_ft, ev_power_ft, soc_ft, voltages_ft, buses_ft = optimization_ft(keys)
    total_power_tou, ev_power_tou, soc_tou, voltages_tou, buses_tou = optimization_tou(keys)
    
    deviations_uc[it] = number_deviations(voltages_uc_tou)
    deviations_ft[it] = number_deviations(voltages_ft)
    deviations_tou[it] = number_deviations(voltages_tou)

br1 = np.arange(4)
br2 = br1 + 0.25
br3 = br1 + 0.50
z = np.polyfit(br1, deviations_uc, 1)
p = np.poly1d(z)

plt.figure(figsize = (10, 5.5), dpi = 300)
plt.bar(br1, deviations_uc, color ='tab:blue', width = 0.25, label='Carregamento\nDescoordenado')
plt.bar(br2, deviations_ft, color ='tab:orange', width = 0.25, label='Carreg. Coordenado\nTarifa Convencional')
plt.bar(br3, deviations_tou, color ='tab:green', width = 0.25, label='Carreg. Coordenado\nTarifa Branca')
plt.plot(br1,p(br1),"black", marker = 'o')
# plt.plot(br1, deviations_uc,"black", marker = 'o')
# plt.figure(figsize = (10,5), dpi = 300)
# plt.plot(penetration.values(), deviations_uc,label='Carregamento\nDescoordenado')
# plt.plot(penetration.values(), deviations_ft,label='Carreg. Coordenado\nTarifa Convencional')
# plt.plot(penetration.values(), deviations_tou,label='Carreg. Coordenado\nTarifa Branca')
plt.ylabel('Número de desvios de Tensão')
# plt.xticks(np.arange(0, 65, 5), ('0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'))
plt.xticks(np.arange(0.25, 4.25, 1), ('10', '35', '50', '60'))
plt.xlabel('Penetração (%)')
plt.legend(loc='upper left', framealpha=1)
plt.margins(x=0, y=0)
plt.ylim(0, 35)
plt.grid(True)
plt.tight_layout()
plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Desvios_Artigo4.png")
plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Desvios_Artigo4.svg")
plt.close()

# # print(deviations_uc)
# # print(deviations_ft)
# # print(deviations_tou)

# penetration = {9:'10%', 18:'20%', 31:'35%', 35:'40%', 44:'50%', 53:'60%'}

# for key in penetration:
#     total_power_10_uc_tou, voltages_10_uc_tou, buses_10_uc_tou = optimization_uc_tou(key)
#     total_power_10_ft, ev_power_10_ft, soc_10_ft, voltages_10_ft, buses_10_ft = optimization_ft(key)
#     total_power_10_tou, ev_power_10_tou, soc_10_tou, voltages_10_tou, buses_10_tou = optimization_tou(key)

#     plt.figure(figsize = (10,5), dpi = 300)
#     # plt.axvspan(0, 105, facecolor='limegreen', alpha=0.1, label='Horário fora de ponta')
#     # plt.axvspan(105, 111, facecolor='yellow', alpha=0.2, label='Horário intermediário')
#     # plt.axvspan(111, 129, facecolor='red', alpha=0.1, label='Horário de ponta')
#     # plt.axvspan(129, 135, facecolor='yellow', alpha=0.2)
#     # plt.axvspan(135, 288, facecolor='limegreen', alpha=0.1)
#     plt.axvspan(0, 105, facecolor='limegreen', alpha=0.1)
#     plt.axvspan(105, 111, facecolor='yellow', alpha=0.2)
#     plt.axvspan(111, 129, facecolor='red', alpha=0.1)
#     plt.axvspan(129, 135, facecolor='yellow', alpha=0.2)
#     plt.axvspan(135, 288, facecolor='limegreen', alpha=0.1)

#     plt.plot(tempo, total_power_10_uc_tou, 'tab:green', linestyle='-', label='Carregamento\nDescoordenado')
#     plt.plot(tempo, total_power_10_ft, 'tab:orange', linestyle='-', label='Carreg. Coord.\nTarifa Conven.')
#     plt.plot(tempo, total_power_10_tou, 'tab:red', linestyle=(0, (2, 1)), label='Carreg. Coord.\nTarifa Branca')
#     plt.plot(tempo, pow_base, 'tab:blue', linestyle='--', label='Caso Base')
#     plt.ylabel('Potência (kVA)')
#     plt.xlabel('Tempo (h)')
#     plt.axhline(112.5, color="black", linestyle="--")
#     plt.text(3, 125, 'capacidade nominal', fontsize=22, va='center', ha='left')
#     #plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
#     plt.xticks(np.arange(0, 289, 12), ('0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24'))
#     plt.xlim(0, 288)
#     plt.legend(loc='upper right', framealpha=1, ncol = 1)
#     plt.ylim(0, 200)
#     plt.margins(x=0)
#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Curva_de_Carga_Artigo_{penetration[key]}.svg")
#     plt.close()

# total_power_uc_tou, voltages_uc_tou, buses_uc_tou = optimization_uc_tou(44)
# total_power_ft, ev_power_ft, soc_ft, voltages_ft, buses_ft = optimization_ft(44)
# total_power_tou, ev_power_tou, soc_tou, voltages_tou, buses_tou = optimization_tou(44)

# print('##################################################')
# print('Base Case')
# number_deviations(voltages_base, bus_base)
# print('##################################################')
# print('Uncoordinated')
# number_deviations(voltages_uc_tou, buses_uc_tou)
# print('##################################################')
# print('Coordinated Flat Tariff')
# number_deviations(voltages_ft, buses_ft)
# print('##################################################')
# print('Coordinated Time of Use')
# number_deviations(voltages_tou, buses_tou)

# print(buses_ft[22])

# plt.figure(figsize = (10, 5.5), dpi = 300)
# plt.plot(tempo, voltages_uc_tou[105], label='Carreg. Descoordenado')
# plt.plot(tempo, voltages_ft[105], linestyle='-', label='Carreg. Coordenado\nTarifa Convencional')
# plt.plot(tempo, voltages_tou[105], linestyle='-', label='Carreg. Coordenado\nTarifa Branca')
# plt.axhline(1.05, color="black", linestyle="--")
# plt.axhline(0.92, color="black", linestyle="--")
# plt.ylabel('Tensão (PU)')
# plt.xlabel('Tempo (h)')
# plt.xticks(np.arange(0, 289, 12), ('0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24'))
# plt.xlim(0, 288)
# plt.text(3, 0.93, 'Limite Mínimo', fontsize=22, va='center', ha='left')
# plt.text(3, 1.04, 'Limite Máximo', fontsize=22, va='center', ha='left')
# plt.ylim(0.86, 1.06)
# plt.legend(loc='lower right', framealpha=1)
# plt.margins(x=0)
# plt.grid(True)
# plt.tight_layout()
# plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Curva_de_Tensão_50%_barra27.png")
# plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Curva_de_Tensão_50%_barra27.svg")
# plt.close()



# for j in range(0, 150, 3):
#     plt.figure(figsize = (11, 14), dpi = 300)
#     plt.subplot(3, 1, 1)
    
#     plt.title(f'Fase 1 {buses_ft[int(j/3)]} - 35% Penetração', fontsize=14)
#     plt.plot(tempo, voltages_uc_tou[j], label='Carreg. Descoordenado')
#     plt.plot(tempo, voltages_ft[j], linestyle='-', label='Carreg. Coordenado\n(Tarifa Convencional)')
#     plt.plot(tempo, voltages_tou[j], linestyle='--', label='Carreg. Coordenado\n(Tarifa Branca)')
#     plt.axhline(1.05, color="black", linestyle="--")
#     plt.axhline(0.92, color="black", linestyle="--")
#     plt.ylabel('Tensão [PU]')
#     plt.xlabel('Tempo')
#     plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
#     plt.ylim(0.86, 1.06)
#     plt.legend(loc='lower right',title="Tipo de Carregamento", prop={'size': 12}, framealpha=1)
#     plt.margins(x=0)
#     plt.grid(True)

#     plt.subplot(3, 1, 2)
#     plt.title(f'Fase 2 {buses_ft[int(j/3)]} - 35% Penetração', fontsize=14)
#     plt.plot(tempo, voltages_uc_tou[j+1], label='Carreg. Descoordenado')
#     plt.plot(tempo, voltages_ft[j+1], linestyle='-', label='Carreg. Coordenado\n(Tarifa Convencional)')
#     plt.plot(tempo, voltages_tou[j+1], linestyle='--', label='Carreg. Coordenado\n(Tarifa Branca)')
#     plt.axhline(1.05, color="black", linestyle="--")
#     plt.axhline(0.92, color="black", linestyle="--")
#     plt.ylabel('Tensão [PU]')
#     plt.xlabel('Tempo')
#     plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
#     plt.ylim(0.86, 1.06)
#     plt.legend(loc='lower right',title="Tipo de Carregamento", prop={'size': 12}, framealpha=1)
#     plt.margins(x=0)
#     plt.grid(True)

#     plt.subplot(3, 1, 3)
#     plt.title(f'Fase 3 {buses_ft[int(j/3)]} - 35% Penetração', fontsize=14)
#     plt.plot(tempo, voltages_uc_tou[j+2], label='Carreg. Descoordenado')
#     plt.plot(tempo, voltages_ft[j+2], linestyle='-', label='Carreg. Coordenado\n(Tarifa Convencional)')
#     plt.plot(tempo, voltages_tou[j+2], linestyle='--', label='Carreg. Coordenado\n(Tarifa Branca)')
#     plt.axhline(1.05, color="black", linestyle="--")
#     plt.axhline(0.92, color="black", linestyle="--")
#     plt.ylabel('Tensão [PU]')
#     plt.xlabel('Tempo')
#     plt.xticks(np.arange(0, 289, 12), ('0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h', '12h', '14h','16h', '18h', '20h', '22h', '24h'))
#     plt.ylim(0.86, 1.06)
#     plt.legend(loc='lower right',title="Tipo de Carregamento", prop={'size': 12}, framealpha=1)
#     plt.margins(x=0)
#     plt.grid(True)

#     plt.tight_layout()
#     plt.savefig(rf"C:\Users\kaioh\Documents\TCC\Python\Comparison\Voltages_35\Curva_de_Tensão_{buses_ft[int(j/3)]}")
#     plt.close()
