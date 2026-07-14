import trafficSimulator as ts
sim = ts.Simulation(config_file="config_image.json")

sim.create_segment((0, 0), (0, 200), identifier="Cubi_S_N", category="general")
sim.create_segment((-5, 200), (-5, 0), identifier="Cubi_N_S", category="general")



sim.create_segment((205,210), (5,210), identifier="cubi_right_sx", category="general")
sim.create_segment((5,205),(205, 205), identifier="cubi_right_dx", category="general")

sim.create_segment((-260,205),(-10, 205), identifier="cubi_left_dx", category="general")
sim.create_segment((-10,210), (-260,210), identifier="cubi_left_sx", category="general")


sim.create_segment("cubi_right_sx", "cubi_left_sx", identifier="cubi_right_sx_to_cubi_left_sx", category="general")
sim.create_segment("cubi_left_dx", "cubi_right_dx", identifier="cubi_left_dx_to_cubi_right_dx", category="general")



sim.create_quadratic_bezier_curve("Cubi_S_N", "cubi_right_dx", identifier="Cubi_S_N_to_cubi_right_dx")
sim.create_quadratic_bezier_curve("cubi_right_sx", "Cubi_N_S", identifier="cubi_right_sx_to_Cubi_N_S")

sim.create_quadratic_bezier_curve("Cubi_S_N", "cubi_left_sx", identifier="Cubi_S_N_to_cubi_left_sx")
sim.create_quadratic_bezier_curve("cubi_left_dx", "Cubi_N_S", identifier="cubi_left_dx_to_Cubi_N_S")


sim.create_vehicle_generator(
	vehicle_rate=4,
	vehicles=[
		(6, {"path": [0, 8, 3], "vehicle_class": "car"}),
		(2, {"path": [0, 10, 5], "vehicle_class": "electric"})
	]
)

sim.create_vehicle_generator(
	vehicle_rate=3,
	vehicles=[
		(5, {"path": [2, 6, 5], "vehicle_class": "car"}),
		(2, {"path": [2, 9, 1], "vehicle_class": "truck"})
	]
)

sim.create_vehicle_generator(
	vehicle_rate=3,
	vehicles=[
		(5, {"path": [4, 11, 1], "vehicle_class": "car"}),
		(1, {"path": [4, 7, 3], "vehicle_class": "bus"})
	]
)


win = ts.Window(sim)
win.show()