import trafficSimulator as ts

# Carichiamo la configurazione avanzata
sim = ts.Simulation(config_file="config_smartcity.json")

# --- TOPOLOGIA: DISTRETTO SMART CITY ---

# Indice 0: Tangenziale Sud (Molto veloce: ~90 km/h)
sim.create_segment((-300, -200), (300, -200), identifier="Tangenziale_Sud", max_speed=25.0, category="general")

# Indice 1: Svincolo Est (Media velocità, curva ampia)
sim.create_quadratic_bezier_curve((300, -200), (450, 0), (300, 200), identifier="Svincolo_Est", max_speed=13.8)

# Indice 2: Viale Nord cittadino (Corsia preferenziale: ~50 km/h)
sim.create_segment((300, 200), (-100, 200), identifier="Viale_Nord", max_speed=13.8, category="bus_lane")

# Indice 3: Ingresso Campus Ingegneria (Curva stretta, rallentamento: ~30 km/h)
sim.create_quadratic_bezier_curve((-100, 200), (-250, 100), (-100, 0), identifier="Ingresso_Campus", max_speed=8.3)

# Indice 4: Viale Interno Sterrato (Zona di test sensori/sospensioni, molto lento: ~18 km/h)
sim.create_segment((-100, 0), (100, 0), identifier="Area_Test_Sterrato", max_speed=5.0, category="dirt", material="gravel")

# Indice 5: Curva complessa di raccordo (Bézier Cubica)
sim.create_cubic_bezier_curve((100, 0), (150, 0), (0, -50), (0, -100), identifier="Curva_Laboratori", max_speed=8.3)

# Indice 6: Immissione in Tangenziale
sim.create_quadratic_bezier_curve((0, -100), (0, -200), (-300, -200), identifier="Raccordo_Uscita", max_speed=13.8)


# --- GENERAZIONE DEL TRAFFICO ---
# Flusso continuo ad alta intensità che percorre l'intero anello (0 -> 6)
sim.create_vehicle_generator(
    vehicle_rate=5,
    vehicles=[
        (12, {'path': [0, 1, 2, 3, 4, 5, 6], 'vehicle_class': 'car'}),
        (3,  {'path': [0, 1, 2, 3, 4, 5, 6], 'vehicle_class': 'bus'}),
        (2,  {'path': [0, 1, 2, 3, 4, 5, 6], 'vehicle_class': 'truck'}),
        (5,  {'path': [0, 1, 2, 3, 4, 5, 6], 'vehicle_class': 'electric'})
    ]
)

# Aggiungiamo un secondo generatore "ritardato" per immettere veicoli 
# direttamente dal viale Nord (indice 2) e creare interazioni di flusso
sim.create_vehicle_generator(
    vehicle_rate=3,
    vehicles=[
        (5, {'path': [2, 3, 4, 5, 6, 0, 1], 'vehicle_class': 'car'}),
        (2, {'path': [2, 3, 4, 5, 6, 0, 1], 'vehicle_class': 'truck'})
    ]
)

# --- RENDERIZZAZIONE ---
win = ts.Window(sim)
# Uno zoom più ampio per godere dell'intera mappa
win.zoom = 1.8
win.offset = (0, 0)
win.show()