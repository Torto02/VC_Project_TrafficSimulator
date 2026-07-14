import trafficSimulator as ts

sim = ts.Simulation(config_file="config_bifurcation.json")

# --- TOPOLOGIA: RACCORDO MULTIMODALE ---

# 1. SUPERSTRADA EST (Andata, da Ovest verso Est, y = -4)
sim.create_segment((-300, -4), (-100, -4), identifier="Hwy_Est_1", max_speed=25.0)
sim.create_segment((-100, -4), (300, -4), identifier="Hwy_Est_2", max_speed=25.0, category="bus_lane") # Corsia preferenziale dopo il bivio
