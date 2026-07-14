import trafficSimulator as ts

sim = ts.Simulation()

# Fasi Semaforiche Incrociate (Ciclo totale 28 secondi)
# NS riceve il verde per primo
phases_NS = [("green", 12), ("yellow", 3), ("red", 13)]
# EW aspetta col rosso per i primi 15 secondi, poi tocca a lui
phases_EW = [("red", 15), ("green", 10), ("yellow", 3)]

# --- ASSE NORD-SUD ---
# Segmento 0: Da Nord fino all'incrocio. Aggiungiamo il semaforo alla fine di questo segmento.
sim.create_segment((0, -200), (0, -10), identifier="NS_In").add_traffic_light(phases_NS)
# Segmento 1: Attraversamento incrocio e uscita verso Sud
sim.create_segment((0, -10), (0, 200), identifier="NS_Out")

# --- ASSE EST-OVEST ---
# Segmento 2: Da Ovest fino all'incrocio. Aggiungiamo il semaforo EW.
sim.create_segment((-200, 0), (-10, 0), identifier="EW_In").add_traffic_light(phases_EW)
# Segmento 3: Attraversamento incrocio e uscita verso Est
sim.create_segment((-10, 0), (200, 0), identifier="EW_Out")

# Generatori di traffico indipendenti
sim.create_vehicle_generator(
    vehicle_rate=3,
    vehicles=[(1, {'path': [0, 1], 'vehicle_class': 'car'})]
)
sim.create_vehicle_generator(
    vehicle_rate=4,
    vehicles=[(1, {'path': [2, 3], 'vehicle_class': 'truck'})]
)

# Rendering
win = ts.Window(sim)
win.zoom = 2.0
win.offset = (0, 0)
win.show()