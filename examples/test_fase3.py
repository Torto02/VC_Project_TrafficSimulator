import trafficSimulator as ts

sim = ts.Simulation()

# Creazione delle strade (interagiscono con l'ambiente definito in config.json)
sim.create_segment((0, 3), (100, 3), identifier="Via_A", category="general")
sim.create_segment((100, 3), (200, 3), identifier="Via_B", category="dirt", material="gravel")
sim.create_quadratic_bezier_curve((200, 3), (220, 0), (200, -3), identifier="Curva")
sim.create_segment((200, -3), (0, -3), identifier="Ritorno", category="bus_lane")

# Generatore di veicoli misto
sim.create_vehicle_generator(
    vehicle_rate=3,
    vehicles=[
        (6, {'path': [0, 1, 2, 3], 'vehicle_class': 'car'}),
        (2, {'path': [0, 1, 2, 3], 'vehicle_class': 'truck'}),
        (2, {'path': [0, 1, 2, 3], 'vehicle_class': 'electric'})
    ]
)

win = ts.Window(sim)
win.show()