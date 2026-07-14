import trafficSimulator as ts

sim = ts.Simulation(config_file="config_image.json")

# --- 1. VIALE PRINCIPALE OVEST -> EST (Corsia Superiore) ---
# Indici 0-4
sim.create_segment((350, 4), (170, 4), identifier="W_In")
sim.create_segment((170, 4), (130, 4), identifier="W_R_Int")
sim.create_segment((130, 4), (-130, 4), identifier="W_Mid")
sim.create_segment((-130, 4), (-170, 4), identifier="W_L_Int")
sim.create_segment((-170, 4), (-350, 4), identifier="W_Out")

# --- 2. VIALE PRINCIPALE EST -> OVEST (Corsia Inferiore) ---
# Indici 5-9
sim.create_segment((-350, -4), (-170, -4), identifier="E_In")
sim.create_segment((-170, -4), (-130, -4), identifier="E_L_Int")
sim.create_segment((-130, -4), (130, -4), identifier="E_Mid")
sim.create_segment((130, -4), (170, -4), identifier="E_R_Int")
sim.create_segment((170, -4), (350, -4), identifier="E_Out")

# --- 3. VIALE VERTICALE SUD ---
# Indici 10-13
sim.create_segment((154, -250), (154, -20), identifier="S_In_UP")
sim.create_quadratic_bezier_curve((154, -20), (154, 4), (130, 4), identifier="Curve_S_to_W")
sim.create_quadratic_bezier_curve((130, -4), (146, -4), (146, -20), identifier="Curve_E_to_S")
sim.create_segment((146, -20), (146, -250), identifier="S_Out_DOWN")

# --- 4. LA STRADA ROSSA (Solo Camion, Sterrato) ---
# Indici 14-17 (Disegnata come sterrato per differenziarla visivamente)
cat_rossa = "dirt"
mat_rossa = "gravel"
sim.create_quadratic_bezier_curve((170, 4), (150, 4), (150, 24), identifier="Red_Curve_In", category=cat_rossa, material=mat_rossa, max_speed=10.0)
sim.create_segment((150, 24), (150, 130), identifier="Red_UP", category=cat_rossa, material=mat_rossa, max_speed=12.0)
sim.create_quadratic_bezier_curve((150, 130), (150, 150), (130, 150), identifier="Red_Curve_Left", category=cat_rossa, material=mat_rossa, max_speed=10.0)
sim.create_segment((130, 150), (-170, 150), identifier="Red_Straight_Left", category=cat_rossa, material=mat_rossa, max_speed=12.0)

# --- 5. IL LOOP BIANCO (Anello Esterno e Taglio Interno) ---
# Indici 18-28 (Anello Esterno)
sim.create_quadratic_bezier_curve((-130, 4), (-150, 4), (-150, 24), identifier="Loop_In")
sim.create_segment((-150, 24), (-150, 70), identifier="Loop_R1_UP")
sim.create_segment((-150, 70), (-150, 90), identifier="Loop_R2_UP")
sim.create_segment((-150, 90), (-150, 130), identifier="Loop_R3_UP")
sim.create_quadratic_bezier_curve((-150, 130), (-150, 150), (-170, 150), identifier="Loop_Top_Right")
sim.create_segment((-170, 150), (-180, 150), identifier="Loop_Top")
sim.create_quadratic_bezier_curve((-180, 150), (-200, 150), (-200, 130), identifier="Loop_Top_Left")
sim.create_segment((-200, 130), (-200, 90), identifier="Loop_L1_DOWN")
sim.create_segment((-200, 90), (-200, 70), identifier="Loop_L2_DOWN")
sim.create_segment((-200, 70), (-200, 24), identifier="Loop_L3_DOWN")
sim.create_quadratic_bezier_curve((-200, 24), (-200, -4), (-170, -4), identifier="Loop_Out")

# Indici 29-31 (Taglio Interno per creare il circuito circolare locale)
sim.create_quadratic_bezier_curve((-200, 90), (-200, 80), (-190, 80), identifier="Inner_Curve_1")
sim.create_segment((-190, 80), (-160, 80), identifier="Inner_Straight")
sim.create_quadratic_bezier_curve((-160, 80), (-150, 80), (-150, 90), identifier="Inner_Curve_2")


# ==========================================
# --- GENERATORI DI TRAFFICO E PERCORSI ---
# ==========================================

# FLUSSO 1: Strada Rossa (ESCLUSIVAMENTE CAMION)
# Entrano da Destra, prendono la strada sterrata a Nord, passano per il loop ed escono a Destra.
sim.create_vehicle_generator(
    vehicle_rate=1.5,
    vehicles=[
        (1, {'path': [0, 14, 15, 16, 17, 23, 24, 25, 26, 27, 28, 6, 7, 8, 9], 'vehicle_class': 'truck'})
    ]
)

# FLUSSO 2: Ingresso da Destra (Misto, escludendo la strada rossa)
sim.create_vehicle_generator(
    vehicle_rate=5,
    vehicles=[
        # Vanno dritti fino all'uscita sinistra
        (6, {'path': [0, 1, 2, 3, 4], 'vehicle_class': 'car'}),
        
        # Entrano nel Loop Bianco (giro largo) e tornano indietro
        (2, {'path': [0, 1, 2, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 6, 7, 8, 9], 'vehicle_class': 'electric'}),
        
        # Entrano nel Loop Bianco, prendono il TAGLIO INTERNO per fare un giro doppio
        (1, {'path': [0, 1, 2, 18, 19, 20, 21, 22, 23, 24, 25, 29, 30, 31, 21, 22, 23, 24, 25, 26, 27, 28, 6, 7, 8, 9], 'vehicle_class': 'car'})
    ]
)

# FLUSSO 3: Ingresso da Sinistra
sim.create_vehicle_generator(
    vehicle_rate=5,
    vehicles=[
        # Vanno dritti fino all'uscita destra
        (7, {'path': [5, 6, 7, 8, 9], 'vehicle_class': 'car'}),
        
        # Girano a destra verso l'uscita Sud
        (2, {'path': [5, 6, 7, 12, 13], 'vehicle_class': 'bus'})
    ]
)

# FLUSSO 4: Ingresso da Sud
sim.create_vehicle_generator(
    vehicle_rate=3,
    vehicles=[
        # Salgono e si immettono nel traffico verso Ovest
        (1, {'path': [10, 11, 2, 3, 4], 'vehicle_class': 'car'})
    ]
)

# --- RENDERIZZAZIONE ---
win = ts.Window(sim)
win.zoom = 2.2
win.offset = (0, 30) # Centriamo la mappa sullo schermo
win.show()