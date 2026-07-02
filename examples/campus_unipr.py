import trafficSimulator as ts

# Inizializzazione che carica in automatico config.json
sim = ts.Simulation()

# --- TOPOLOGIA: PARCO AREA DELLE SCIENZE (UNIPR) ---
# Indice 0: Viale G. P. Usberti (Ingresso Sud)
sim.create_segment((-200, -100), (-100, 0), identifier="Viale_Usberti_Ingresso", max_speed=8.3, category="general")

# Indice 1: Curva verso il Plesso di Ingegneria
sim.create_quadratic_bezier_curve((-100, 0), (-50, 50), (0, 50), identifier="Curva_Ingegneria", max_speed=8.3)

# Indice 2: Rettilineo Sede Didattica / Scientifica Ingegneria
sim.create_segment((0, 50), (100, 50), identifier="Sede_Ingegneria", max_speed=8.3)

# Indice 3: Curva e discesa verso la zona CUS
sim.create_cubic_bezier_curve((100, 50), (150, 50), (150, 150), (100, 150), identifier="Curva_CUS", max_speed=8.3)

# Indice 4: Viale di uscita
sim.create_segment((100, 150), (-200, 150), identifier="Viale_Uscita", max_speed=8.3)

# Indice 5: Raccordo ad anello per mantenere il traffico continuo (simula la rotonda di uscita)
sim.create_cubic_bezier_curve((-200, 150), (-250, 150), (-250, -100), (-200, -100), identifier="Rotonda_Raccordo", max_speed=8.3)


# --- GENERAZIONE DEL TRAFFICO ---
# Creiamo un flusso misto: auto degli studenti, autobus TEP (linee 7/14/21) e mezzi elettrici
sim.create_vehicle_generator(
    vehicle_rate=4, # Frequenza di immissione
    vehicles=[
        (15, {'path': [0, 1, 2, 3, 4, 5], 'vehicle_class': 'car'}),       # Studenti/Docenti
        (3,  {'path': [0, 1, 2, 3, 4, 5], 'vehicle_class': 'bus'}),       # Autobus TEP
        (2,  {'path': [0, 1, 2, 3, 4, 5], 'vehicle_class': 'truck'}),     # Furgoni consegne/manutenzione
        (4,  {'path': [0, 1, 2, 3, 4, 5], 'vehicle_class': 'electric'})   # Veicoli EV
    ]
)


# --- RENDERIZZAZIONE ---
win = ts.Window(sim)

# Offset e Zoom iniziali per inquadrare bene la mappa del campus
win.zoom = 3.0
win.offset = (50, -20)

win.show()