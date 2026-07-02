import trafficSimulator as ts

sim = ts.Simulation(config_file="config_open.json")

# --- TOPOLOGIA APERTA ---

# 1. Autostrada Principale (Nasce a Ovest, Muore a Est)
sim.create_segment((-400, 0), (-100, 0), identifier="Hwy_Ingresso", max_speed=25.0)
sim.create_segment((-100, 0), (100, 0), identifier="Hwy_Centro", max_speed=25.0)
sim.create_segment((100, 0), (400, 0), identifier="Hwy_Uscita", max_speed=25.0)

# 2. Rampa di Immissione (Nasce a Sud, si unisce in Centro)
sim.create_segment((-150, 300), (-150, 100), identifier="Rampa_In_Sud", max_speed=13.8)
sim.create_quadratic_bezier_curve((-150, 100), (-150, 0), (-100, 0), identifier="Curva_Immissione", max_speed=10.0)

# 3. Rampa di Uscita (Si stacca in Centro, Muore a Nord)
sim.create_quadratic_bezier_curve((100, 0), (150, 0), (150, -100), identifier="Curva_Uscita", max_speed=10.0)
sim.create_segment((150, -100), (150, -300), identifier="Rampa_Out_Nord", max_speed=13.8)


# --- GENERATORI DI TRAFFICO (Con Flussi Infiniti) ---

# Flusso 1: Viaggiatori autostradali (Da Ovest a Est: 0 -> 1 -> 2)
sim.create_vehicle_generator(
    vehicle_rate=6,
    vehicles=[
        (8, {'path': [0, 1, 2], 'vehicle_class': 'car'}),
        (3, {'path': [0, 1, 2], 'vehicle_class': 'truck'})
    ]
)

# Flusso 2: Pendolari che entrano in autostrada da Sud (Da Sud a Est: 3 -> 4 -> 1 -> 2)
sim.create_vehicle_generator(
    vehicle_rate=4,
    vehicles=[
        (5, {'path': [3, 4, 1, 2], 'vehicle_class': 'car'}),
        (1, {'path': [3, 4, 1, 2], 'vehicle_class': 'bus'})
    ]
)

# Flusso 3: Veicoli che escono dall'autostrada verso Nord
# Alcuni arrivano da Ovest (0 -> 1 -> 5 -> 6), altri entrano da Sud ed escono a Nord (3 -> 4 -> 1 -> 5 -> 6)
sim.create_vehicle_generator(
    vehicle_rate=5,
    vehicles=[
        (4, {'path': [0, 1, 5, 6], 'vehicle_class': 'electric'}),
        (2, {'path': [3, 4, 1, 5, 6], 'vehicle_class': 'car'})
    ]
)

# --- RENDERIZZAZIONE ---
win = ts.Window(sim)
win.zoom = 1.5
win.offset = (0, 0)
win.show()