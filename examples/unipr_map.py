# import trafficSimulator as ts
# sim = ts.Simulation(config_file="unipr.json")

# sim.create_segment((-4, 200), (-4, 110), identifier="Cubi_N_S_Up", category="general")
# sim.create_segment((0, 110), (0, 200), identifier="Cubi_S_N_Up", category="general")

# sim.create_segment((-4, 100), (-4, 0), identifier="Cubi_N_S_Down", category="general")
# sim.create_segment((0, 0), (0, 100), identifier="Cubi_S_N_Down", category="general")

# #----
# sim.create_segment((3, 103), (60, 103), identifier="parcheggio_cubi_dx_dx", category="general")
# sim.create_segment((60, 107), (3, 107), identifier="parcheggio_cubi_dx_sx", category="general")

# sim.create_segment((-7, 107), (-64, 107), identifier="parcheggio_cubi_sx_sx", category="general")
# sim.create_segment((-64, 103), (-7, 103), identifier="parcheggio_cubi_sx_dx", category="general")
# #---
# sim.create_segment((30,210),(4,210), identifier="viale_usberti_dx_sx", category="general")
# sim.create_segment((4,206),(30, 206), identifier="viale_usberti_dx_dx", category="general")

# sim.create_segment((105,210), (45,210), identifier="viale_usberti_dx_sx_Dx", category="general")
# sim.create_segment((45,206),(105, 206), identifier="viale_usberti_dx_dx_Dx", category="general")

# sim.create_segment((-158,206),(-10, 206), identifier="viale_usberti_sx_dx", category="general")
# sim.create_segment((-10,210), (-158,210), identifier="viale_usberti_sx_sx", category="bus_lane")

# sim.create_segment((-230,206),(-164, 206), identifier="viale_usberti_sx_dx_Sx", category="general")
# sim.create_segment((-164,210), (-230,210), identifier="viale_usberti_sx_sx_Sx", category="bus_lane")

# sim.create_segment((0,212),(0, 245), identifier="cantiere_S_N", category="dirt")
# sim.create_segment((-4,245), (-4,212), identifier="cantiere_N_S", category="dirt")

# sim.create_segment((-10,290),(-40, 361), identifier="cantiere_E_W", category="dirt")
# sim.create_segment((-44,360), (-14,288), identifier="cantiere_W_E", category="dirt")

# sim.create_segment("viale_usberti_dx_sx", "viale_usberti_sx_sx", identifier="viale_usberti_dx_sx_to_viale_usberti_sx_sx", category="general")
# sim.create_segment("viale_usberti_sx_dx", "viale_usberti_dx_dx", identifier="viale_usberti_sx_dx_to_viale_usberti_dx_dx", category="general")

# # parcheggi cubi
# sim.create_segment("Cubi_S_N_Down", "Cubi_S_N_Up", identifier="Cubi_S_N_Down_to_Cubi_S_N_Up", category="general")
# sim.create_segment("Cubi_N_S_Up", "Cubi_N_S_Down", identifier="Cubi_N_S_Up_to_Cubi_N_S_Down", category="general")

# sim.create_quadratic_bezier_curve("Cubi_S_N_Down", "parcheggio_cubi_dx_dx", identifier="Cubi_S_N_Down_to_parcheggio_cubi_dx_dx")
# sim.create_quadratic_bezier_curve("Cubi_S_N_Down", "parcheggio_cubi_sx_sx", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")

# sim.create_quadratic_bezier_curve("Cubi_N_S_Up", "parcheggio_cubi_dx_dx", identifier="Cubi_N_S_Up_to_parcheggio_cubi_dx_dx")
# sim.create_quadratic_bezier_curve("Cubi_N_S_Up", "parcheggio_cubi_sx_sx", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")

# sim.create_quadratic_bezier_curve("parcheggio_cubi_dx_sx", "Cubi_S_N_Up", identifier="Cubi_S_N_Down_to_parcheggio_cubi_dx_dx")
# sim.create_quadratic_bezier_curve("parcheggio_cubi_sx_dx", "Cubi_S_N_Up", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")

# sim.create_quadratic_bezier_curve("parcheggio_cubi_dx_sx", "Cubi_N_S_Down", identifier="Cubi_N_S_Up_to_parcheggio_cubi_dx_dx")
# sim.create_quadratic_bezier_curve("parcheggio_cubi_sx_dx", "Cubi_N_S_Down", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")

# sim.create_quadratic_bezier_curve("cantiere_S_N", "cantiere_E_W", identifier="cantiere_S_N_to_cantiere_E_W", category="dirt")
# sim.create_quadratic_bezier_curve("cantiere_W_E", "cantiere_N_S", identifier="cantiere_W_E_to_cantiere_N_S", category="dirt")

# sim.create_quadratic_bezier_curve("Cubi_S_N_Up", "viale_usberti_dx_dx", identifier="Cubi_S_N_Up_to_viale_usberti_dx_dx")
# sim.create_quadratic_bezier_curve("viale_usberti_dx_sx", "Cubi_N_S_Up", identifier="viale_usberti_dx_sx_to_Cubi_N_S_Up")
# sim.create_quadratic_bezier_curve("Cubi_S_N_Up", "viale_usberti_sx_sx", identifier="Cubi_S_N_Up_to_viale_usberti_sx_sx")
# sim.create_quadratic_bezier_curve("viale_usberti_sx_dx", "Cubi_N_S_Up", identifier="viale_usberti_sx_dx_to_Cubi_N_S_Up")
# sim.create_quadratic_bezier_curve("Cubi_S_N_Up", "cantiere_S_N", identifier="Cubi_S_N_Up_to_cantiere_S_N")
# sim.create_quadratic_bezier_curve("cantiere_N_S", "Cubi_N_S_Up", identifier="cantiere_N_S_to_Cubi_N_S_Up")
# sim.create_quadratic_bezier_curve("viale_usberti_dx_sx", "cantiere_S_N", identifier="viale_usberti_dx_sx_to_cantiere_S_N")
# sim.create_quadratic_bezier_curve("viale_usberti_sx_dx", "cantiere_S_N", identifier="viale_usberti_sx_dx_to_cantiere_S_N")
# sim.create_quadratic_bezier_curve("cantiere_N_S", "viale_usberti_dx_dx", identifier="cantiere_N_S_to_viale_usberti_dx_dx")

# sim.create_segment((128,307),(114,450), identifier="viale_usberti_dx_S_N", category="general")
# sim.create_segment((110,450),(124,307), identifier="viale_usberti_dx_N_S", category="general")

# sim.create_segment((134,245),(130,298), identifier="viale_usberti_dx_S_N_down", category="general")
# sim.create_segment((126,298),(130,245), identifier="viale_usberti_dx_N_S_down", category="general")

# sim.create_quadratic_bezier_curve("viale_usberti_dx_dx_Dx", "viale_usberti_dx_S_N_down", identifier="viale_usberti_dx_dx_to_viale_usberti_dx_S_N")
# sim.create_quadratic_bezier_curve("viale_usberti_dx_N_S_down", "viale_usberti_dx_sx_Dx", identifier="viale_usberti_dx_N_S_to_viale_usberti_dx_sx")

# sim.create_segment("viale_usberti_dx_S_N_down", "viale_usberti_dx_S_N", identifier="viale_usberti_dx_S_N_down_to_viale_usberti_dx_S_N", category="general")
# sim.create_segment("viale_usberti_dx_N_S", "viale_usberti_dx_N_S_down", identifier="viale_usberti_dx_N_S_to_viale_usberti_dx_N_S_down", category="general")

# sim.create_segment((-258,480),(80,480), identifier="viale_superiore_dx_W_E", category="general")
# sim.create_segment((80,484),(-258,484), identifier="viale_superiore_dx_E_W", category="general")

# sim.create_segment((-266,484),(-400,484), identifier="viale_superiore_sx_E_W", category="general")
# sim.create_segment((-400,480),(-266,480), identifier="viale_superiore_sx_W_E", category="general")

# sim.create_segment((-260,402),(-260,478), identifier="viale_usberti_sx_S_N_UP", category="bus_lane")
# sim.create_segment((-264,478),(-264,402), identifier="viale_usberti_sx_N_S_UP", category="general")

# sim.create_segment((-260,370),(-260,392), identifier="viale_usberti_sx_S_N_Mid", category="bus_lane")
# sim.create_segment((-264,392),(-264,370), identifier="viale_usberti_sx_N_S_Mid", category="general")

# sim.create_segment((-290,394),(-270,394), identifier="parc_scienze_dx", category="general")
# sim.create_segment((-270,398),(-290,398), identifier="parc_scienze_sx", category="general")

# sim.create_segment("viale_usberti_sx_S_N_Mid", "viale_usberti_sx_S_N_UP", identifier="viale_usberti_sx_S_N_Mid_to_viale_usberti_sx_S_N_UP", category="bus_lane")
# sim.create_segment("viale_usberti_sx_N_S_UP", "viale_usberti_sx_N_S_Mid", identifier="viale_usberti_sx_N_S_UP_to_viale_usberti_sx_N_S_Mid", category="general")

# sim.create_quadratic_bezier_curve("viale_usberti_dx_S_N", "viale_superiore_dx_E_W", identifier="viale_usberti_dx_S_N_to_viale_superiore_dx_E_W")
# sim.create_quadratic_bezier_curve("viale_superiore_dx_W_E", "viale_usberti_dx_N_S", identifier="viale_superiore_dx_W_E_to_viale_usberti_dx_N_S")

# sim.create_quadratic_bezier_curve("parc_scienze_dx", "viale_usberti_sx_N_S_Mid", identifier="parc_scienze_dx_to_viale_usberti_sx_N_S_Mid")
# sim.create_quadratic_bezier_curve("viale_usberti_sx_N_S_UP", "parc_scienze_sx", identifier="viale_usberti_sx_N_S_UP_to_viale_scienze_sx")





# sim.create_segment("viale_superiore_sx_W_E", "viale_superiore_dx_W_E", identifier="viale_superiore_sx_W_E_to_viale_superiore_dx_W_E", category="general")
# sim.create_segment("viale_superiore_dx_E_W", "viale_superiore_sx_E_W", identifier="viale_superiore_dx_E_W_to_viale_superiore_sx_E_W", category="general")

# sim.create_quadratic_bezier_curve("viale_superiore_sx_W_E", "viale_superiore_dx_W_E", identifier="viale_superiore_sx_W_E_to_viale_superiore_dx_W_E")
# sim.create_quadratic_bezier_curve("viale_superiore_dx_E_W", "viale_superiore_sx_E_W", identifier="viale_superiore_dx_E_W_to_viale_superiore_sx_E_W")

# sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N_UP", "viale_superiore_dx_W_E", identifier="viale_usberti_sx_S_N_UP_to_viale_superiore_dx_W_E")
# sim.create_quadratic_bezier_curve("viale_superiore_dx_E_W", "viale_usberti_sx_N_S_UP", identifier="viale_superiore_dx_E_W_to_viale_usberti_sx_N_S_UP")

# sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N_UP", "viale_superiore_sx_E_W", identifier="viale_usberti_sx_S_N_UP_to_viale_superiore_sx_E_W")
# sim.create_quadratic_bezier_curve("viale_superiore_sx_W_E", "viale_usberti_sx_N_S_UP", identifier="viale_superiore_sx_W_E_to_viale_usberti_sx_N_S_UP")

# sim.create_segment((120,304),(50,284), identifier="viale_mensa_E_W", category="general")
# sim.create_segment((50,280),(120,300), identifier="viale_mensa_W_E", category="general")

# sim.create_segment((39,213),(39,260), identifier="viale_mensa_S_N", category="general")
# sim.create_segment((35,260),(35,213), identifier="viale_mensa_N_S", category="general")

# sim.create_quadratic_bezier_curve("viale_usberti_dx_N_S", "viale_mensa_E_W", identifier="viale_usberti_dx_N_S_to_viale_mensa_E_W")
# sim.create_quadratic_bezier_curve("viale_mensa_W_E", "viale_usberti_dx_S_N", identifier="viale_mensa_W_E_to_viale_usberti_dx_S_N")
# sim.create_quadratic_bezier_curve("viale_usberti_dx_S_N_down", "viale_mensa_E_W", identifier="viale_usberti_dx_S_N_down_to_viale_mensa_E_W")
# sim.create_quadratic_bezier_curve("viale_mensa_W_E", "viale_usberti_dx_N_S_down", identifier="viale_mensa_W_E_to_viale_usberti_dx_N_S_down")

# sim.create_quadratic_bezier_curve("viale_usberti_dx_sx_Dx", "viale_mensa_S_N", identifier="viale_mensa_S_N_to_viale_mensa_W_E")
# sim.create_quadratic_bezier_curve("viale_usberti_dx_dx", "viale_mensa_S_N", identifier="viale_mensa_E_W_to_viale_mensa_N_S")
# sim.create_quadratic_bezier_curve("viale_mensa_N_S", "viale_usberti_dx_sx", identifier="viale_mensa_S_N_to_viale_mensa_W_E")
# sim.create_quadratic_bezier_curve("viale_mensa_N_S", "viale_usberti_dx_dx_Dx", identifier="viale_mensa_E_W_to_viale_mensa_N_S")
# sim.create_quadratic_bezier_curve("viale_usberti_dx_dx", "viale_usberti_dx_dx_Dx", identifier="viale_mensa_S_N_to_viale_mensa_W_E")
# sim.create_quadratic_bezier_curve("viale_usberti_dx_sx_Dx", "viale_usberti_dx_sx", identifier="viale_mensa_E_W_to_viale_mensa_N_S")

# sim.create_quadratic_bezier_curve("viale_mensa_S_N", "viale_mensa_W_E", identifier="viale_mensa_S_N_to_viale_mensa_W_E")
# sim.create_quadratic_bezier_curve("viale_mensa_E_W", "viale_mensa_N_S", identifier="viale_mensa_E_W_to_viale_mensa_N_S")

# sim.create_segment((-260,230),(-260,290), identifier="viale_usberti_sx_S_N", category="bus_lane")
# sim.create_segment((-264,290),(-264,230), identifier="viale_usberti_sx_N_S", category="general")


# sim.create_quadratic_bezier_curve("viale_usberti_sx_N_S", "viale_usberti_sx_dx_Sx", identifier="viale_usberti_sx_N_S_to_viale_usberti_sx_dx")
# sim.create_quadratic_bezier_curve("viale_usberti_sx_sx_Sx", "viale_usberti_sx_S_N", identifier="viale_usberti_sx_sx_to_viale_usberti_sx_S_N",category="bus_lane")

# sim.create_segment((-262,320),(-262,350), identifier="viale_usberti_lavori_S_N", category="work_zone")
# sim.create_segment((-262,350),(-262,320), identifier="viale_usberti_lavori_N_S", category="work_zone")

# sim.create_quadratic_bezier_curve("viale_usberti_lavori_N_S", "viale_usberti_sx_N_S", identifier="viale_usberti_lavori_N_S_to_viale_usberti_sx_N_S")
# sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N", "viale_usberti_lavori_S_N", identifier="viale_usberti_sx_S_N_to_viale_usberti_lavori_S_N", category="bus_lane")

# sim.create_quadratic_bezier_curve("viale_usberti_sx_N_S_Mid", "viale_usberti_lavori_N_S", identifier="viale_usberti_lavori_N_S_to_viale_usberti_sx_N_S")
# sim.create_quadratic_bezier_curve("viale_usberti_lavori_S_N", "viale_usberti_sx_S_N_Mid", identifier="viale_usberti_sx_S_N_to_viale_usberti_lavori_S_N", category="bus_lane")

# sim.create_quadratic_bezier_curve("viale_usberti_lavori_N_S", "viale_usberti_sx_N_S", identifier="viale_usberti_lavori_N_S_to_viale_usberti_sx_N_S")
# sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N", "viale_usberti_lavori_S_N", identifier="viale_usberti_sx_S_N_to_viale_usberti_lavori_S_N", category="bus_lane")

# sim.create_segment((-160,215),(-160,230), identifier="usberti_parcheggio")
# sim.create_segment((-164,230),(-164,215), identifier="parcheggio_usberti")


# sim.create_segment("viale_usberti_sx_sx", "viale_usberti_sx_sx_Sx", identifier="viale_usberti_sx_sx_to_viale_usberti_sx_sx_Sx", category="bus_lane")
# sim.create_segment("viale_usberti_sx_dx_Sx", "viale_usberti_sx_dx", identifier="viale_usberti_sx_dx_Sx_to_viale_usberti_sx_dx")


# sim.create_quadratic_bezier_curve("viale_usberti_sx_dx_Sx", "usberti_parcheggio", identifier="viale_usberti_sx_dx_Sx_to_usberti_parcheggio")
# sim.create_quadratic_bezier_curve("parcheggio_usberti", "viale_usberti_sx_dx", identifier="parcheggio_usberti_to_viale_usberti_sx_dx")


# #-----


# sim.create_vehicle_generator(
# 	vehicle_rate=40,
# 	vehicles=[
# 		(6, {"path": [0, 8, 3], "vehicle_class": "car"}),
# 		(2, {"path": [0, 10, 5], "vehicle_class": "electric"})
# 	]
# )

# # sim.create_vehicle_generator(
# # 	vehicle_rate=40,
# # 	vehicles=[
# # 		(5, {"path": [2, 6, 5], "vehicle_class": "car"}),
# # 		(2, {"path": [2, 9, 1], "vehicle_class": "truck"})
# # 	]
# # )

# # sim.create_vehicle_generator(
# # 	vehicle_rate=40,
# # 	vehicles=[
# # 		(5, {"path": [4, 11, 1], "vehicle_class": "car"}),
# # 		(1, {"path": [4, 7, 3], "vehicle_class": "bus"})
# # 	]
# # )

# # sim.create_intersection([
# #     {"segment_index": 2, "clearance_distance": 50.0},
# #     {"segment_index": 3, "clearance_distance": 50.0},
# #     {"segment_index": 5, "clearance_distance": 50.0},
# # ])

# win = ts.Window(sim)
# win.show()



import trafficSimulator as ts

sim = ts.Simulation(config_file="unipr.json")

# Cubi - segmenti base
sim.create_segment((-4, 200), (-4, 110), identifier="Cubi_N_S_Up", category="general")  #1
sim.create_segment((0, 110), (0, 200), identifier="Cubi_S_N_Up", category="general")  #2
sim.create_segment((-4, 100), (-4, 0), identifier="Cubi_N_S_Down", category="general")  #3
sim.create_segment((0, 0), (0, 100), identifier="Cubi_S_N_Down", category="general")  #4

# Parcheggio Cubi
sim.create_segment((3, 103), (60, 103), identifier="parcheggio_cubi_dx_dx", category="general")  #5
sim.create_segment((60, 107), (3, 107), identifier="parcheggio_cubi_dx_sx", category="general")  #6
sim.create_segment((-7, 107), (-64, 107), identifier="parcheggio_cubi_sx_sx", category="general")  #7
sim.create_segment((-64, 103), (-7, 103), identifier="parcheggio_cubi_sx_dx", category="general")  #8

# Viale Usberti - tratto principale a destra
sim.create_segment((30, 210), (4, 210), identifier="viale_usberti_dx_sx", category="general")  #9
sim.create_segment((4, 206), (30, 206), identifier="viale_usberti_dx_dx", category="general")  #10
sim.create_segment((105, 210), (45, 210), identifier="viale_usberti_dx_sx_Dx", category="general")  #11
sim.create_segment((45, 206), (105, 206), identifier="viale_usberti_dx_dx_Dx", category="general")  #12

# Viale Usberti - tratto principale a sinistra
sim.create_segment((-158, 206), (-10, 206), identifier="viale_usberti_sx_dx", category="general")  #13
sim.create_segment((-10, 210), (-158, 210), identifier="viale_usberti_sx_sx", category="bus_lane")  #14
sim.create_segment((-230, 206), (-164, 206), identifier="viale_usberti_sx_dx_Sx", category="general")  #15
sim.create_segment((-164, 210), (-230, 210), identifier="viale_usberti_sx_sx_Sx", category="bus_lane")  #16

# Cantiere
sim.create_segment((0, 212), (0, 245), identifier="cantiere_S_N", category="dirt")  #17
sim.create_segment((-4, 245), (-4, 212), identifier="cantiere_N_S", category="dirt")  #18
sim.create_segment((-10, 290), (-40, 361), identifier="cantiere_E_W", category="dirt")  #19
sim.create_segment((-44, 360), (-14, 288), identifier="cantiere_W_E", category="dirt")  #20

# Collegamenti tra i due tratti centrali
sim.create_segment("viale_usberti_dx_sx", "viale_usberti_sx_sx", identifier="viale_usberti_dx_sx_to_viale_usberti_sx_sx", category="general")  #21
sim.create_segment("viale_usberti_sx_dx", "viale_usberti_dx_dx", identifier="viale_usberti_sx_dx_to_viale_usberti_dx_dx", category="general")  #22

# Collegamenti Cubi - parcheggi
sim.create_segment("Cubi_S_N_Down", "Cubi_S_N_Up", identifier="Cubi_S_N_Down_to_Cubi_S_N_Up", category="general")  #23
sim.create_segment("Cubi_N_S_Up", "Cubi_N_S_Down", identifier="Cubi_N_S_Up_to_Cubi_N_S_Down", category="general")  #24

# Curve parcheggio Cubi
sim.create_quadratic_bezier_curve("Cubi_S_N_Down", "parcheggio_cubi_dx_dx", identifier="Cubi_S_N_Down_to_parcheggio_cubi_dx_dx")  #25
sim.create_quadratic_bezier_curve("Cubi_S_N_Down", "parcheggio_cubi_sx_sx", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")  #26
sim.create_quadratic_bezier_curve("Cubi_N_S_Up", "parcheggio_cubi_dx_dx", identifier="Cubi_N_S_Up_to_parcheggio_cubi_dx_dx")  #27
sim.create_quadratic_bezier_curve("Cubi_N_S_Up", "parcheggio_cubi_sx_sx", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")  #28
sim.create_quadratic_bezier_curve("parcheggio_cubi_dx_sx", "Cubi_S_N_Up", identifier="Cubi_S_N_Down_to_parcheggio_cubi_dx_dx")  #29
sim.create_quadratic_bezier_curve("parcheggio_cubi_sx_dx", "Cubi_S_N_Up", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")  #30
sim.create_quadratic_bezier_curve("parcheggio_cubi_dx_sx", "Cubi_N_S_Down", identifier="Cubi_N_S_Up_to_parcheggio_cubi_dx_dx")  #31
sim.create_quadratic_bezier_curve("parcheggio_cubi_sx_dx", "Cubi_N_S_Down", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")  #32

# Curve cantiere
sim.create_quadratic_bezier_curve("cantiere_S_N", "cantiere_E_W", identifier="cantiere_S_N_to_cantiere_E_W", category="dirt")  #33
sim.create_quadratic_bezier_curve("cantiere_W_E", "cantiere_N_S", identifier="cantiere_W_E_to_cantiere_N_S", category="dirt")  #34

# Cubi - Viale Usberti / Cantiere
sim.create_quadratic_bezier_curve("Cubi_S_N_Up", "viale_usberti_dx_dx", identifier="Cubi_S_N_Up_to_viale_usberti_dx_dx")  #35
sim.create_quadratic_bezier_curve("viale_usberti_dx_sx", "Cubi_N_S_Up", identifier="viale_usberti_dx_sx_to_Cubi_N_S_Up")  #36
sim.create_quadratic_bezier_curve("Cubi_S_N_Up", "viale_usberti_sx_sx", identifier="Cubi_S_N_Up_to_viale_usberti_sx_sx")  #37
sim.create_quadratic_bezier_curve("viale_usberti_sx_dx", "Cubi_N_S_Up", identifier="viale_usberti_sx_dx_to_Cubi_N_S_Up")  #38
sim.create_quadratic_bezier_curve("Cubi_S_N_Up", "cantiere_S_N", identifier="Cubi_S_N_Up_to_cantiere_S_N")  #39
sim.create_quadratic_bezier_curve("cantiere_N_S", "Cubi_N_S_Up", identifier="cantiere_N_S_to_Cubi_N_S_Up")  #40
sim.create_quadratic_bezier_curve("viale_usberti_dx_sx", "cantiere_S_N", identifier="viale_usberti_dx_sx_to_cantiere_S_N")  #41
sim.create_quadratic_bezier_curve("viale_usberti_sx_dx", "cantiere_S_N", identifier="viale_usberti_sx_dx_to_cantiere_S_N")  #42
sim.create_quadratic_bezier_curve("cantiere_N_S", "viale_usberti_dx_dx", identifier="cantiere_N_S_to_viale_usberti_dx_dx")  #43


# Viale Usberti - tratto verticale destra
sim.create_segment((128, 307), (114, 450), identifier="viale_usberti_dx_S_N", category="general")  #44
sim.create_segment((110, 450), (124, 307), identifier="viale_usberti_dx_N_S", category="general")  #45
sim.create_segment((134, 245), (130, 298), identifier="viale_usberti_dx_S_N_down", category="general")  #46
sim.create_segment((126, 298), (130, 245), identifier="viale_usberti_dx_N_S_down", category="general")  #47

# Curve tratto verticale destra
sim.create_quadratic_bezier_curve("viale_usberti_dx_dx_Dx", "viale_usberti_dx_S_N_down", identifier="viale_usberti_dx_dx_to_viale_usberti_dx_S_N")  #48
sim.create_quadratic_bezier_curve("viale_usberti_dx_N_S_down", "viale_usberti_dx_sx_Dx", identifier="viale_usberti_dx_N_S_to_viale_usberti_dx_sx")  #49

# Collegamenti interni tratto verticale destra
sim.create_segment("viale_usberti_dx_S_N_down", "viale_usberti_dx_S_N", identifier="viale_usberti_dx_S_N_down_to_viale_usberti_dx_S_N", category="general")  #50
sim.create_segment("viale_usberti_dx_N_S", "viale_usberti_dx_N_S_down", identifier="viale_usberti_dx_N_S_to_viale_usberti_dx_N_S_down", category="general")  #51

# Viale Superiore e Viale Usberti alto
sim.create_segment((-258, 480), (80, 480), identifier="viale_superiore_dx_W_E", category="general")  #52
sim.create_segment((80, 484), (-258, 484), identifier="viale_superiore_dx_E_W", category="general")  #53
sim.create_segment((-266, 484), (-400, 484), identifier="viale_superiore_sx_E_W", category="general")  #54
sim.create_segment((-400, 480), (-266, 480), identifier="viale_superiore_sx_W_E", category="general")  #55
sim.create_segment((-260, 402), (-260, 478), identifier="viale_usberti_sx_S_N_UP", category="bus_lane")  #56
sim.create_segment((-264, 478), (-264, 402), identifier="viale_usberti_sx_N_S_UP", category="general")  #57
sim.create_segment((-260, 370), (-260, 392), identifier="viale_usberti_sx_S_N_Mid", category="bus_lane")  #58
sim.create_segment((-264, 392), (-264, 370), identifier="viale_usberti_sx_N_S_Mid", category="general")  #59
sim.create_segment((-290, 394), (-270, 394), identifier="parc_scienze_dx", category="general")  #60
sim.create_segment((-270, 398), (-290, 398), identifier="parc_scienze_sx", category="general")  #61

sim.create_segment("viale_usberti_sx_S_N_Mid", "viale_usberti_sx_S_N_UP", identifier="viale_usberti_sx_S_N_Mid_to_viale_usberti_sx_S_N_UP", category="bus_lane")  #62
sim.create_segment("viale_usberti_sx_N_S_UP", "viale_usberti_sx_N_S_Mid", identifier="viale_usberti_sx_N_S_UP_to_viale_usberti_sx_N_S_Mid", category="general")  #63

# Curve tratto alto
sim.create_quadratic_bezier_curve("viale_usberti_dx_S_N", "viale_superiore_dx_E_W", identifier="viale_usberti_dx_S_N_to_viale_superiore_dx_E_W")  #64
sim.create_quadratic_bezier_curve("viale_superiore_dx_W_E", "viale_usberti_dx_N_S", identifier="viale_superiore_dx_W_E_to_viale_usberti_dx_N_S")  #65
sim.create_quadratic_bezier_curve("parc_scienze_dx", "viale_usberti_sx_N_S_Mid", identifier="parc_scienze_dx_to_viale_usberti_sx_N_S_Mid")  #66
sim.create_quadratic_bezier_curve("viale_usberti_sx_N_S_UP", "parc_scienze_sx", identifier="viale_usberti_sx_N_S_UP_to_viale_scienze_sx")  #67

# Collegamenti Viale Superiore
sim.create_segment("viale_superiore_sx_W_E", "viale_superiore_dx_W_E", identifier="viale_superiore_sx_W_E_to_viale_superiore_dx_W_E", category="general")  #68
sim.create_segment("viale_superiore_dx_E_W", "viale_superiore_sx_E_W", identifier="viale_superiore_dx_E_W_to_viale_superiore_sx_E_W", category="general")  #69

# Curve Viale Superiore
sim.create_quadratic_bezier_curve("viale_superiore_sx_W_E", "viale_superiore_dx_W_E", identifier="viale_superiore_sx_W_E_to_viale_superiore_dx_W_E")  #70
sim.create_quadratic_bezier_curve("viale_superiore_dx_E_W", "viale_superiore_sx_E_W", identifier="viale_superiore_dx_E_W_to_viale_superiore_sx_E_W")  #71
sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N_UP", "viale_superiore_dx_W_E", identifier="viale_usberti_sx_S_N_UP_to_viale_superiore_dx_W_E")  #72
sim.create_quadratic_bezier_curve("viale_superiore_dx_E_W", "viale_usberti_sx_N_S_UP", identifier="viale_superiore_dx_E_W_to_viale_usberti_sx_N_S_UP")  #73
sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N_UP", "viale_superiore_sx_E_W", identifier="viale_usberti_sx_S_N_UP_to_viale_superiore_sx_E_W")  #74
sim.create_quadratic_bezier_curve("viale_superiore_sx_W_E", "viale_usberti_sx_N_S_UP", identifier="viale_superiore_sx_W_E_to_viale_usberti_sx_N_S_UP")  #75

# Viale Mensa
sim.create_segment((120, 304), (50, 284), identifier="viale_mensa_E_W", category="general")  #76
sim.create_segment((50, 280), (120, 300), identifier="viale_mensa_W_E", category="general")  #77
sim.create_segment((39, 213), (39, 260), identifier="viale_mensa_S_N", category="general")  #78
sim.create_segment((35, 260), (35, 213), identifier="viale_mensa_N_S", category="general")  #79

# Curve Viale Mensa
sim.create_quadratic_bezier_curve("viale_usberti_dx_N_S", "viale_mensa_E_W", identifier="viale_usberti_dx_N_S_to_viale_mensa_E_W")  #80
sim.create_quadratic_bezier_curve("viale_mensa_W_E", "viale_usberti_dx_S_N", identifier="viale_mensa_W_E_to_viale_usberti_dx_S_N")  #81
sim.create_quadratic_bezier_curve("viale_usberti_dx_S_N_down", "viale_mensa_E_W", identifier="viale_usberti_dx_S_N_down_to_viale_mensa_E_W")  #82
sim.create_quadratic_bezier_curve("viale_mensa_W_E", "viale_usberti_dx_N_S_down", identifier="viale_mensa_W_E_to_viale_usberti_dx_N_S_down")  #83
sim.create_quadratic_bezier_curve("viale_usberti_dx_sx_Dx", "viale_mensa_S_N", identifier="viale_mensa_S_N_to_viale_mensa_W_E")  #84
sim.create_quadratic_bezier_curve("viale_usberti_dx_dx", "viale_mensa_S_N", identifier="viale_mensa_E_W_to_viale_mensa_N_S")  #85
sim.create_quadratic_bezier_curve("viale_mensa_N_S", "viale_usberti_dx_sx", identifier="viale_mensa_S_N_to_viale_mensa_W_E")  #86
sim.create_quadratic_bezier_curve("viale_mensa_N_S", "viale_usberti_dx_dx_Dx", identifier="viale_mensa_E_W_to_viale_mensa_N_S")  #87
sim.create_quadratic_bezier_curve("viale_usberti_dx_dx", "viale_usberti_dx_dx_Dx", identifier="viale_mensa_S_N_to_viale_mensa_W_E")  #88
sim.create_quadratic_bezier_curve("viale_usberti_dx_sx_Dx", "viale_usberti_dx_sx", identifier="viale_mensa_E_W_to_viale_mensa_N_S")  #89
sim.create_quadratic_bezier_curve("viale_mensa_S_N", "viale_mensa_W_E", identifier="viale_mensa_S_N_to_viale_mensa_W_E")  #90
sim.create_quadratic_bezier_curve("viale_mensa_E_W", "viale_mensa_N_S", identifier="viale_mensa_E_W_to_viale_mensa_N_S")  #91

# Viale Usberti sinistra - tratto basso
sim.create_segment((-260, 230), (-260, 290), identifier="viale_usberti_sx_S_N", category="bus_lane")  #92
sim.create_segment((-264, 290), (-264, 230), identifier="viale_usberti_sx_N_S", category="general")  #93

# Curve tratto basso sinistro
sim.create_quadratic_bezier_curve("viale_usberti_sx_N_S", "viale_usberti_sx_dx_Sx", identifier="viale_usberti_sx_N_S_to_viale_usberti_sx_dx")  #94
sim.create_quadratic_bezier_curve("viale_usberti_sx_sx_Sx", "viale_usberti_sx_S_N", identifier="viale_usberti_sx_sx_to_viale_usberti_sx_S_N", category="bus_lane")  #95

# Viale Usberti lavori
sim.create_segment((-262, 320), (-262, 350), identifier="viale_usberti_lavori_S_N", category="work_zone")  #96
sim.create_segment((-262, 350), (-262, 320), identifier="viale_usberti_lavori_N_S", category="work_zone")  #97

# Curve lavori
sim.create_quadratic_bezier_curve("viale_usberti_lavori_N_S", "viale_usberti_sx_N_S", identifier="viale_usberti_lavori_N_S_to_viale_usberti_sx_N_S")  #98
sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N", "viale_usberti_lavori_S_N", identifier="viale_usberti_sx_S_N_to_viale_usberti_lavori_S_N", category="bus_lane")  #99
sim.create_quadratic_bezier_curve("viale_usberti_sx_N_S_Mid", "viale_usberti_lavori_N_S", identifier="viale_usberti_lavori_N_S_to_viale_usberti_sx_N_S")  #100
sim.create_quadratic_bezier_curve("viale_usberti_lavori_S_N", "viale_usberti_sx_S_N_Mid", identifier="viale_usberti_sx_S_N_to_viale_usberti_lavori_S_N", category="bus_lane")  #101
sim.create_quadratic_bezier_curve("viale_usberti_lavori_N_S", "viale_usberti_sx_N_S", identifier="viale_usberti_lavori_N_S_to_viale_usberti_sx_N_S")  #102
sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N", "viale_usberti_lavori_S_N", identifier="viale_usberti_sx_S_N_to_viale_usberti_lavori_S_N", category="bus_lane")  #103

# Parcheggio lato usberti
sim.create_segment((-160, 215), (-160, 230), identifier="usberti_parcheggio")  #104
sim.create_segment((-164, 230), (-164, 215), identifier="parcheggio_usberti")  #105

sim.create_segment("viale_usberti_sx_sx", "viale_usberti_sx_sx_Sx", identifier="viale_usberti_sx_sx_to_viale_usberti_sx_sx_Sx", category="bus_lane")  #106
sim.create_segment("viale_usberti_sx_dx_Sx", "viale_usberti_sx_dx", identifier="viale_usberti_sx_dx_Sx_to_viale_usberti_sx_dx")  #107

# Curve parcheggio usberti
sim.create_quadratic_bezier_curve("viale_usberti_sx_dx_Sx", "usberti_parcheggio", identifier="viale_usberti_sx_dx_Sx_to_usberti_parcheggio")  #108
sim.create_quadratic_bezier_curve("parcheggio_usberti", "viale_usberti_sx_dx", identifier="parcheggio_usberti_to_viale_usberti_sx_dx")  #109

#-----

sim.create_vehicle_generator(
    vehicle_rate=40,
    vehicles=[
        (6, {"path": [0, 8, 3], "vehicle_class": "car"}),
        (2, {"path": [0, 10, 5], "vehicle_class": "electric"})
    ]
)

# sim.create_vehicle_generator(
#     vehicle_rate=40,
#     vehicles=[
#         (5, {"path": [2, 6, 5], "vehicle_class": "car"}),
#         (2, {"path": [2, 9, 1], "vehicle_class": "truck"})
#     ]
# )

# sim.create_vehicle_generator(
#     vehicle_rate=40,
#     vehicles=[
#         (5, {"path": [4, 11, 1], "vehicle_class": "car"}),
#         (1, {"path": [4, 7, 3], "vehicle_class": "bus"})
#     ]
# )

# sim.create_intersection([
#     {"segment_index": 2, "clearance_distance": 50.0},
#     {"segment_index": 3, "clearance_distance": 50.0},
#     {"segment_index": 5, "clearance_distance": 50.0},
# ])

win = ts.Window(sim)
win.show()