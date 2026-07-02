import trafficSimulator as ts

sim = ts.Simulation(config_file="config_bifurcation.json")

# --- TOPOLOGIA: RACCORDO MULTIMODALE ---

# 1. SUPERSTRADA EST (Andata, da Ovest verso Est, y = -4)
sim.create_segment((-300, -4), (-100, -4), identifier="Hwy_Est_1", max_speed=25.0)
sim.create_segment((-100, -4), (300, -4), identifier="Hwy_Est_2", max_speed=25.0, category="bus_lane") # Corsia preferenziale dopo il bivio

# 2. BIFORCAZIONE NORD (Strada sterrata lenta che devia dalla Superstrada)
# Rampa d'uscita (Curva verso Nord)
sim.create_quadratic_bezier_curve((-100, -4), (-50, -4), (-50, -100), identifier="Rampa_Uscita", max_speed=10.0, category="dirt", material="gravel")
# Tratto rettilineo verso Nord
sim.create_segment((-50, -100), (-50, -300), identifier="Via_Foresta_Andata", max_speed=8.0, category="dirt", material="gravel")

# 3. RITORNO DALLA BIFORCAZIONE NORD
# Tratto rettilineo verso Sud (sfalsato di 8 metri sull'asse x per il doppio senso)
sim.create_segment((-42, -300), (-42, -100), identifier="Via_Foresta_Ritorno", max_speed=8.0, category="dirt", material="gravel")
# Rampa di immissione (Curva che si ricollega alla Superstrada Ovest)
sim.create_quadratic_bezier_curve((-42, -100), (-42, 4), (-100, 4), identifier="Rampa_Immissione", max_speed=13.8)

# 4. SUPERSTRADA OVEST (Ritorno, da Est verso Ovest, y = 4)
sim.create_segment((300, 4), (-100, 4), identifier="Hwy_Ovest_1", max_speed=25.0)
sim.create_segment((-100, 4), (-300, 4), identifier="Hwy_Ovest_2", max_speed=25.0)

# 5. RACCORDI INVISIBILI (U-Turns) PER FLUSSO CONTINUO
sim.create_quadratic_bezier_curve((300, -4), (330, 0), (300, 4), identifier="U-Turn_Est", max_speed=15.0)
sim.create_quadratic_bezier_curve((-300, 4), (-330, 0), (-300, -4), identifier="U-Turn_Ovest", max_speed=15.0)
sim.create_quadratic_bezier_curve((-50, -300), (-46, -330), (-42, -300), identifier="U-Turn_Nord", max_speed=5.0)


# --- GENERAZIONE DEL TRAFFICO E SCELTA DEI PERCORSI ---

# Percorso 1 (Dritto sulla superstrada, fa il giro)
path_straight = [0, 1, 8, 6, 7, 9] 
# Percorso 2 (Prende la biforcazione, esplora lo sterrato e torna indietro)
path_bifurcation = [0, 2, 3, 10, 4, 5, 7, 9] 

sim.create_vehicle_generator(
    vehicle_rate=7,
    vehicles=[
        # La maggior parte delle auto e dei camion va dritto ad alta velocità
        (10, {'path': path_straight, 'vehicle_class': 'car'}),
        (4,  {'path': path_straight, 'vehicle_class': 'truck'}),
        (3,  {'path': path_straight, 'vehicle_class': 'bus'}),
        
        # Una percentuale di veicoli elettrici e auto sceglie la via secondaria
        (4,  {'path': path_bifurcation, 'vehicle_class': 'electric'}),
        (3,  {'path': path_bifurcation, 'vehicle_class': 'car'})
    ]
)

# Immettiamo anche traffico che nasce dal lato opposto (Est) per popolare subito la carreggiata di ritorno
sim.create_vehicle_generator(
    vehicle_rate=5,
    vehicles=[
        (6, {'path': [6, 7, 9, 0, 1, 8], 'vehicle_class': 'car'}),
        (3, {'path': [6, 7, 9, 0, 2, 3, 10, 4, 5], 'vehicle_class': 'truck'})
    ]
)

# --- RENDERIZZAZIONE ---
win = ts.Window(sim)
win.zoom = 1.6
win.offset = (0, 70) # Sposta l'inquadratura per centrare la diramazione a Nord
win.show()