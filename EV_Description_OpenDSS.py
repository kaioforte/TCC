import numpy as np
#Esse Description não é usado na otimização, será usado mais tarde no OpenDSS

def ev_buses(number_ev):
    ev_bus = np.array(['bus1 = barra3.1' ,
    'bus1 = barra3.2' ,
    'bus1 = barra3.3' ,
    'bus1 = barra4.1' ,
    'bus1 = barra4.2' ,
    'bus1 = barra4.3' ,
    'bus1 = barra5.1' ,
    'bus1 = barra5.2' ,
    'bus1 = barra5.3' ,
    'bus1 = barra6.1' ,
    'bus1 = barra6.2' ,
    'bus1 = barra6.3' ,
    'bus1 = barra7.1' ,
    'bus1 = barra7.2' ,
    'bus1 = barra7.3' ,
    'bus1 = barra7a.1' ,
    'bus1 = barra7a.2' ,
    'bus1 = barra7a.3' ,
    'bus1 = barra8.1' ,
    'bus1 = barra8.2' ,
    'bus1 = barra8.3' ,
    'bus1 = barra9.1' ,
    'bus1 = barra9.2' ,
    'bus1 = barra9.3' ,
    'bus1 = barra10.2' ,
    'bus1 = barra11.1' ,
    'bus1 = barra11.2' ,
    'bus1 = barra11.3' ,
    'bus1 = barra12.1' ,
    'bus1 = barra12.2' ,
    'bus1 = barra12.3' ,
    'bus1 = barra13.1' ,
    'bus1 = barra13.2' ,
    'bus1 = barra13.3' ,
    'bus1 = barra14.1' ,
    'bus1 = barra14.2' ,
    'bus1 = barra14.3' ,
    'bus1 = barra15.1' ,
    'bus1 = barra15.2' ,
    'bus1 = barra15.3' ,
    'bus1 = barra16.1' ,
    'bus1 = barra16.2' ,
    'bus1 = barra16.3' ,
    'bus1 = barra17.1' ,
    'bus1 = barra17.2' ,
    'bus1 = barra17.3' ,
    'bus1 = barra18.1' ,
    'bus1 = barra18.2' ,
    'bus1 = barra18.3' ,
    'bus1 = barra38.1' ,
    'bus1 = barra38.2' ,
    'bus1 = barra38.3' ,
    'bus1 = barra39.1' ,
    'bus1 = barra39.2' ,
    'bus1 = barra39.3' ,
    'bus1 = barra40.1' ,
    'bus1 = barra40.2' ,
    'bus1 = barra40.3' ,
    'bus1 = barra41.1' ,
    'bus1 = barra41.2' ,
    'bus1 = barra41.3' ,
    'bus1 = barra42.1' ,
    'bus1 = barra42.2' ,
    'bus1 = barra42.3' ,
    'bus1 = barra43.1' ,
    'bus1 = barra43.2' ,
    'bus1 = barra43.3' ,
    'bus1 = barra44.1' ,
    'bus1 = barra44.2' ,
    'bus1 = barra44.3' ,
    'bus1 = barra45.1' ,
    'bus1 = barra45.2' ,
    'bus1 = barra45.3' ,
    'bus1 = barra19.1' ,
    'bus1 = barra19.2' ,
    'bus1 = barra19.3' ,
    'bus1 = barra20.1' ,
    'bus1 = barra20.2' ,
    'bus1 = barra20.3' ,
    'bus1 = barra21.1' ,
    'bus1 = barra21.2' ,
    'bus1 = barra21.3' ,
    'bus1 = barra22.1' ,
    'bus1 = barra22.2' ,
    'bus1 = barra22.3' ,
    'bus1 = barra23.1' ,
    'bus1 = barra23.2' ,
    'bus1 = barra24.1' ,
    'bus1 = barra24.2' ,
    'bus1 = barra24.3' ,
    'bus1 = barra25.1' ,
    'bus1 = barra25.2' ,
    'bus1 = barra26.1' ,
    'bus1 = barra26.2' ,
    'bus1 = barra26.3' ,
    'bus1 = barra27.1' ,
    'bus1 = barra27.2' ,
    'bus1 = barra27.3' ,
    'bus1 = barra28.1' ,
    'bus1 = barra28.2' ,
    'bus1 = barra28.3' ,
    'bus1 = barra29.2' ,
    'bus1 = barra30.1' ,
    'bus1 = barra30.2' ,
    'bus1 = barra30.3' ,
    'bus1 = barra31.1' ,
    'bus1 = barra31.2' ,
    'bus1 = barra31.3' ,
    'bus1 = barra32.1' ,
    'bus1 = barra32.2' ,
    'bus1 = barra32.3' ,
    'bus1 = barra33.1' ,
    'bus1 = barra33.2' ,
    'bus1 = barra33.3' ,
    'bus1 = barra34.1' ,
    'bus1 = barra34.2' ,
    'bus1 = barra34.3' ,
    'bus1 = barra47a.1' ,
    'bus1 = barra47a.2' ,
    'bus1 = barra47a.3' ,
    'bus1 = barra35.1' ,
    'bus1 = barra35.2' ,
    'bus1 = barra35.3' ,
    'bus1 = barra36.1' ,
    'bus1 = barra36.2' ,
    'bus1 = barra36.3' ,
    'bus1 = barra37.1' ,
    'bus1 = barra37.2' ,
    'bus1 = barra37.3' ,
    'bus1 = barra46.1' ,
    'bus1 = barra46.2' ,
    'bus1 = barra46.3' ,
    'bus1 = barra47.1' ,
    'bus1 = barra47.2' ,
    'bus1 = barra47.3' ,
    'bus1 = barra48.1' ,
    'bus1 = barra48.2' ,
    'bus1 = barra48.3' ,
    'bus1 = barra49.1' ,
    'bus1 = barra49.2' ,
    'bus1 = barra49.3' ])

    rng = np.random.default_rng(12)
    idx = rng.integers(low=0, high=len(ev_bus)+1, size=number_ev)
    buses = ev_bus[idx]
    return buses

ev_buses(44) 
ev_bus0 = ['bus1=barra21.1.0',
            'bus1=barra22.1.0',
            'bus1=barra23.2.0',
            'bus1=barra24.3.0',
            'bus1=barra25.2.0',
            'bus1=barra32.1.0',
            'bus1=barra33.1.0',
            'bus1=barra35.3.0',
            'bus1=barra36.1.0',
            'bus1=barra37.1.0',
            'bus1=barra48.2.0',
            'bus1=barra32.1.0',
            'bus1=barra33.2.0',
            'bus1=barra34.2.0',
            'bus1=barra35.1.0',
            'bus1=barra36.1.0',
            'bus1=barra37.1.0',
            'bus1=barra47.3.0',
            'bus1=barra48.2.0',
            'bus1=barra49.3.0',
            'bus1=barra33.1.0',
            'bus1=barra35.2.0',
            'bus1=barra37.3.0',
            'bus1=barra39.1.0',
            'bus1=barra41.2.0',
            'bus1=barra43.1.0',
            'bus1=barra45.1.0']





