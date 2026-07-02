import trafficSimulator as ts

# Carichiamo la nuova configurazione specifica
sim = ts.Simulation(config_file="config_twoway.json")

# --- TOPOLOGIA: VIALE A DOPPIO SENSO ---
# Distanza dal centro (spartitraffico)
LANE_OFFSET = 4.0

# CARREGGIATA EST (Andata: da sinistra verso destra)
# Indice 0: Primo tratto
sim.create_segment((-250, -LANE_OFFSET), (0, -LANE_OFFSET), identifier="Viale_Est_1", max_speed=13.8)
# Indice 1: Secondo tratto (corsia preferenziale per diversificare)
sim.create_segment((0, -LANE_OFFSET), (250, -LANE_OFFSET), identifier="Viale_Est_2", max_speed=13.8, category="bus_lane")
# Indice 2: Svincolo / Inversione a U Est
sim.create_quadratic_bezier_curve((250, -LANE_OFFSET), (280, 0), (250, LANE_OFFSET), identifier="Inversione_Est", max_speed=8.0)

# CARREGGIATA OVEST (Ritorno: da destra verso sinistra)
# Indice 3: Primo tratto
sim.create_segment((250, LANE_OFFSET), (0, LANE_OFFSET), identifier="Viale_Ovest_1", max_speed=13.8)
# Indice 4: Secondo tratto
sim.create_segment((0, LANE_OFFSET), (-250, LANE_OFFSET), identifier="Viale_Ovest_2", max_speed=13.8)
# Indice 5: Svincolo / Inversione a U Ovest
sim.create_quadratic_bezier_curve((-250, LANE_OFFSET), (-280, 0), (-250, -LANE_OFFSET), identifier="Inversione_Ovest", max_speed=8.0)


# --- GENERAZIONE DEL TRAFFICO INDIPENDENTE ---

# 1. Flusso Est (Percorso: 0 -> 1 -> 2 -> 3 -> 4 -> 5)
sim.create_vehicle_generator(
    vehicle_rate=6,
    vehicles=[
        (10, {'path': [0, 1, 2, 3, 4, 5], 'vehicle_class': 'car'}),
        (3,  {'path': [0, 1, 2, 3, 4, 5], 'vehicle_class': 'truck'})
    ]
)

# 2. Flusso Ovest (Percorso partendo dal lato opposto: 3 -> 4 -> 5 -> 0 -> 1 -> 2)
# Generiamo i veicoli sfalsati in modo da vederli sfrecciare nei due sensi
sim.create_vehicle_generator(
    vehicle_rate=6,
    vehicles=[
        (8, {'path': [3, 4, 5, 0, 1, 2], 'vehicle_class': 'electric'}),
        (4, {'path': [3, 4, 5, 0, 1, 2], 'vehicle_class': 'bus'})
    ]
)

# --- RENDERIZZAZIONE ---
win = ts.Window(sim)
win.zoom = 2.5
win.offset = (0, 0)
win.show()