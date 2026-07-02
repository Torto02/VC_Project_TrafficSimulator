import trafficSimulator as ts
import time

sim = ts.Simulation()

# Creazione di un percorso misto: 
# Usiamo i nuovi parametri 'category' e 'material'
sim.create_segment((0, 3), (150, 3), identifier="Via_Asfalto", category="general", material="asphalt")
sim.create_segment((150, 3), (250, 3), identifier="Via_Sterrato", category="dirt", material="gravel", max_speed=5.0)

# Generatore che sputa diverse classi di veicoli
sim.create_vehicle_generator(
    vehicle_rate=5,
    vehicles=[
        # (Peso probabilità, Parametri del veicolo)
        (5, {'path': [0, 1], 'vehicle_class': 'car'}),
        (5, {'path': [0, 1], 'vehicle_class': 'truck'}),
        (3, {'path': [0, 1], 'vehicle_class': 'electric'})
    ]
)

win = ts.Window(sim)

# --- DEBUG SATELLITARE CORRETTO ---
def print_telemetry_hook(sim):
    # Aggiorniamo ogni 60 frame (circa 1 secondo) per leggibilità
    if sim.frame_count % 60 == 0 and len(sim.vehicles) > 0:
        
        # 1. Prova visiva della corretta generazione: contiamo la flotta
        counts = {}
        for v in sim.vehicles.values():
            counts[v.vehicle_class] = counts.get(v.vehicle_class, 0) + 1
            
        # 2. Leggiamo l'ULTIMO veicolo spawnato (indice -1)
        veh_id = list(sim.vehicles.keys())[-1]
        veh = sim.vehicles[veh_id]
        
        print(f"\n[RECAP FLOTTA] {counts}")
        print(f"[ULTIMO OBU {str(veh.id)[:8]}] "
              f"Classe: {veh.vehicle_class.upper()} | "
              f"Vel: {veh.v:.1f}m/s | "
              f"Accel: {veh.a:.1f}m/s² | "
              f"RPM: {veh.obu_data['engine_rpm']} | "
              f"CO2: {veh.obu_data['co2_emissions']:.2f} g/s")

original_update = sim.update
def hooked_update():
    original_update()
    print_telemetry_hook(sim)

sim.update = hooked_update

win.show()