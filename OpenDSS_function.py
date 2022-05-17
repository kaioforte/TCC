import numpy as np

def circuit_solver(dss, pow_houses, number_ev, ev_loadshape, ev_bus):

    dss.text(r"Compile C:\Users\kaioh\Documents\Universidade\TCC\Python\OpenDSS\Master_RS2.dss")

    dss.loads_first()
    for c in range(88):
        dss.text(f"New Loadshape.demanda{c} npts=288 minterval=10 mult={pow_houses[c]}")
        dss.loads_write_daily(f"demanda{c}")
        dss.loads_next()

    for i in range(number_ev):
        dss.text(f"New Loadshape.recarga{i} npts=288 minterval=10 mult={ev_loadshape[i]}")
        dss.text(f"New Storage.VE{i} phases=1 {ev_bus[i]} kV=0.220 kWrated=7.7 kWhRated=40 %stored=20 %EffCharge=100 state=idling dispmode=follow model=1 daily=recarga{i} kvar=0")

    dss.text("Set mode=daily")
    dss.text("Set number=1")
    dss.text("Set stepsize=10m")
    
    # Arrays vazios para serem preenchidos depois
    total_power = np.zeros(288)
    total_active_power = np.zeros(288)
    total_reactive_power = np.zeros(288)
    all_voltages_per_node = np.zeros((150,288))
    a_losses = np.zeros(288)
    r_losses = np.zeros(288)
    ev_power = np.zeros((number_ev,288))

    for i in range(288):
        # SOlve do opendss
        dss.solution_solve()
        # Potência total do sistema
        total_power[i] = np.sqrt((np.array(dss.circuit_total_power()[0])**2) + (np.array(dss.circuit_total_power()[1])**2))
        # Potência ativa total do sistema
        total_active_power[i] = -1 * np.array(dss.circuit_total_power()[0])
        # Potência reativa total do sistema
        total_reactive_power[i] = -1 * np.array(dss.circuit_total_power()[1])
        # Perdas ativas totais do sistema
        a_losses[i] = dss.circuit_losses()[0]/1000
        # Perdas reativas totais do sistema
        r_losses[i] = dss.circuit_losses()[1]/1000
        # Tensão de cada nó do sistema (ex: tensão 1,2,3 e 4 do bus5)
        # Como algumas barras não tem o nó .4 adiciona np.nan nas posições onde seria a barraX.4, mas que não existem.
        # Assim conseguimos criar um array com 200 tensões (ao invés de 193) de cada fase da barra (.1 .2 .3 .4)
        # para que a relação com o bus_names (que tem 50 buses) faça sentido.  
        temp = np.insert(np.array(dss.circuit_all_bus_vmag_pu()), [3, 35, 36, 119, 126, 139, 140], np.nan)
        # Remove os nós .4 que não serviam para o objetivo do trabalho
        temp = np.delete(temp, np.arange(3,200,4))
        for j in range(150):
            all_voltages_per_node[j][i] = temp[j]
        # Potência de cada EV em cada instante de tempo
        for j in range(number_ev):
            dss.circuit_set_active_element(f"Storage.VE{j}")
            ev_power[j][i] = dss.cktelement_powers()[0]
    
    # Nome de todos os buses do sistema
    bus_names = np.array(dss.circuit_all_bus_names()) 
    # Soma a potência de cada instante de tempo de cada carro
    ev = np.sum(ev_power, axis = 0)


    return total_power, bus_names, all_voltages_per_node, total_active_power, ev, ev_power


def base_case(dss, pow_houses):
    dss.text(r"Compile C:\Users\kaioh\Documents\Universidade\TCC\Python\OpenDSS\Master_RS2.dss")

    dss.loads_first()
    for c in range(88):
        dss.text(f"New Loadshape.demanda{c} npts=288 minterval=10 mult={pow_houses[c]}")
        dss.loads_write_daily(f"demanda{c}")
        dss.loads_next()

    dss.text("Set mode=daily")
    dss.text("Set number=1")
    dss.text("Set stepsize=10m")
    
    # dss.text("DemandInterval = True")
    # dss.solution_solve()

    total_power = np.zeros(288)
    all_voltages_per_node = np.zeros((150,288))
    bus_names = np.array(dss.circuit_all_bus_names())

    for i in range(288):

        dss.solution_solve()

        total_power[i] = np.sqrt((np.array(dss.circuit_total_power()[0])**2) + (np.array(dss.circuit_total_power()[1])**2))

        temp = np.insert(np.array(dss.circuit_all_bus_vmag_pu()), [3, 35, 36, 119, 126, 139, 140], np.nan)
        temp = np.delete(temp, np.arange(3,200,4))
        for j in range(150):
            all_voltages_per_node[j][i] = temp[j]

    return total_power, bus_names, all_voltages_per_node



def circuit_solver2(t, dss, pow_houses, number_ev, ev_loadshape, ev_bus):

    dss.text(r"Compile C:\Users\kaioh\Documents\TCC\Python\OpenDSS\Master_RS2.dss")

    dss.loads_first()
    for c in range(88):
        dss.text(f"New Loadshape.demanda{c} npts=288 minterval=10 mult={pow_houses[c]}")
        dss.loads_write_daily(f"demanda{c}")
        dss.loads_next()

    for i in range(number_ev):
        dss.text(f"New Loadshape.recarga{i} npts=288 minterval=10 mult={ev_loadshape[i]}")
        dss.text(f"New Storage.VE{i} phases=1 {ev_bus[i]} kV=0.220 kWrated=7.7 kWhRated=40 %stored=20 %EffCharge=100 state=idling dispmode=follow model=1 daily=recarga{i} kvar=0")

    dss.text("Set mode=daily")
    dss.text("Set number=1")
    dss.text("Set stepsize=10m")
    
    # Arrays vazios para serem preenchidos depois
    total_power = np.zeros(288-t)
    total_active_power = np.zeros(288-t)
    total_reactive_power = np.zeros(288-t)
    all_voltages_per_node = np.zeros((150,288-t))
    a_losses = np.zeros(288-t)
    r_losses = np.zeros(288-t)
    ev_power = np.zeros((number_ev,288-t))
    
    
    for i in range(288-t):
        # SOlve do opendss
        dss.solution_solve()
        # Potência total do sistema
        total_power[i] = np.sqrt((np.array(dss.circuit_total_power()[0])**2) + (np.array(dss.circuit_total_power()[1])**2))
        # Potência ativa total do sistema
        total_active_power[i] = -1 * np.array(dss.circuit_total_power()[0])
        # Potência reativa total do sistema
        total_reactive_power[i] = -1 * np.array(dss.circuit_total_power()[1])
        # Perdas ativas totais do sistema
        a_losses[i] = dss.circuit_losses()[0]/1000
        # Perdas reativas totais do sistema
        r_losses[i] = dss.circuit_losses()[1]/1000
        # Tensão de cada nó do sistema (ex: tensão 1,2,3 e 4 do bus5)
        # Como algumas barras não tem o nó .4 adiciona np.nan nas posições onde seria a barraX.4, mas que não existem.
        # Assim conseguimos criar um array com 200 tensões (ao invés de 193) de cada fase da barra (.1 .2 .3 .4)
        # para que a relação com o bus_names (que tem 50 buses) faça sentido.  
        temp = np.insert(np.array(dss.circuit_all_bus_vmag_pu()), [3, 35, 36, 119, 126, 139, 140], np.nan)
        # Remove os nós .4 que não serviam para o objetivo do trabalho
        temp = np.delete(temp, np.arange(3,200,4))
        for j in range(150):
            all_voltages_per_node[j][i] = temp[j]
        # Potência de cada EV em cada instante de tempo
        for j in range(number_ev):
            dss.circuit_set_active_element(f"Storage.VE{j}")
            ev_power[j][i] = dss.cktelement_powers()[0]
    
    # Nome de todos os buses do sistema
    bus_names = np.array(dss.circuit_all_bus_names()) 
    # Soma a potência de cada instante de tempo de cada carro
    ev = np.sum(ev_power, axis = 0)


    return total_power, bus_names, all_voltages_per_node, total_active_power, ev, ev_power