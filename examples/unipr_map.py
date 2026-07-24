import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


import trafficSimulator as ts

sim = ts.Simulation(config_file="unipr.json")

# Cubi - segmenti base
sim.create_segment((-4, 200), (-4, 110), identifier="Cubi_N_S_Up", category="general")  #0
sim.create_segment((0, 110), (0, 200), identifier="Cubi_S_N_Up", category="general")  #11
sim.create_segment((-4, 100), (-4, 0), identifier="Cubi_N_S_Down", category="general")  #2
sim.create_segment((0, 0), (0, 100), identifier="Cubi_S_N_Down", category="general")  #3

# Parcheggio Cubi
sim.create_segment((3, 103), (60, 103), identifier="parcheggio_cubi_dx_dx", category="general")  #4
sim.create_segment((60, 107), (3, 107), identifier="parcheggio_cubi_dx_sx", category="general")  #5
sim.create_segment((-7, 107), (-64, 107), identifier="parcheggio_cubi_sx_sx", category="general")  #6
sim.create_segment((-64, 103), (-7, 103), identifier="parcheggio_cubi_sx_dx", category="general")  #7

# Viale Usberti - tratto principale a destra
sim.create_segment((30, 210), (4, 210), identifier="viale_usberti_dx_sx", category="general")  #8
sim.create_segment((4, 206), (30, 206), identifier="viale_usberti_dx_dx", category="general")  #9
sim.create_segment((105, 210), (45, 210), identifier="viale_usberti_dx_sx_Dx", category="general")  #10
sim.create_segment((45, 206), (105, 206), identifier="viale_usberti_dx_dx_Dx", category="general")  #11

# Viale Usberti - tratto principale a sinistra
sim.create_segment((-158, 206), (-10, 206), identifier="viale_usberti_sx_dx", category="general")  #12
sim.create_segment((-10, 210), (-158, 210), identifier="viale_usberti_sx_sx", category="bus_lane")  #13
sim.create_segment((-230, 206), (-164, 206), identifier="viale_usberti_sx_dx_Sx", category="general")  #14
sim.create_segment((-164, 210), (-230, 210), identifier="viale_usberti_sx_sx_Sx", category="bus_lane")  #15

# Cantiere
sim.create_segment((0, 212), (0, 245), identifier="cantiere_S_N", category="dirt", material="grvel")  #16
sim.create_segment((-4, 245), (-4, 212), identifier="cantiere_N_S", category="dirt", material="grvel")  #17
sim.create_segment((-10, 290), (-40, 361), identifier="cantiere_E_W", category="dirt", material="grvel")  #18
sim.create_segment((-44, 360), (-14, 288), identifier="cantiere_W_E", category="dirt", material="grvel")  #19

# Collegamenti tra i due tratti centrali
sim.create_segment("viale_usberti_dx_sx", "viale_usberti_sx_sx", identifier="viale_usberti_dx_sx_to_viale_usberti_sx_sx", category="general")  #20
sim.create_segment("viale_usberti_sx_dx", "viale_usberti_dx_dx", identifier="viale_usberti_sx_dx_to_viale_usberti_dx_dx", category="general")  #21

# Collegamenti Cubi - parcheggi
sim.create_segment("Cubi_S_N_Down", "Cubi_S_N_Up", identifier="Cubi_S_N_Down_to_Cubi_S_N_Up", category="general")  #22
sim.create_segment("Cubi_N_S_Up", "Cubi_N_S_Down", identifier="Cubi_N_S_Up_to_Cubi_N_S_Down", category="general")  #23

# Curve parcheggio Cubi
sim.create_quadratic_bezier_curve("Cubi_S_N_Down", "parcheggio_cubi_dx_dx", identifier="Cubi_S_N_Down_to_parcheggio_cubi_dx_dx")  #24
sim.create_quadratic_bezier_curve("Cubi_S_N_Down", "parcheggio_cubi_sx_sx", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")  #25
sim.create_quadratic_bezier_curve("Cubi_N_S_Up", "parcheggio_cubi_dx_dx", identifier="Cubi_N_S_Up_to_parcheggio_cubi_dx_dx")  #26
sim.create_quadratic_bezier_curve("Cubi_N_S_Up", "parcheggio_cubi_sx_sx", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")  #27
sim.create_quadratic_bezier_curve("parcheggio_cubi_dx_sx", "Cubi_S_N_Up", identifier="Cubi_S_N_Down_to_parcheggio_cubi_dx_dx")  #28
sim.create_quadratic_bezier_curve("parcheggio_cubi_sx_dx", "Cubi_S_N_Up", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")  #29
sim.create_quadratic_bezier_curve("parcheggio_cubi_dx_sx", "Cubi_N_S_Down", identifier="Cubi_N_S_Up_to_parcheggio_cubi_dx_dx")  #30
sim.create_quadratic_bezier_curve("parcheggio_cubi_sx_dx", "Cubi_N_S_Down", identifier="Cubi_S_N_Down_to_parcheggio_cubi_sx_sx")  #31

# Curve cantiere
sim.create_quadratic_bezier_curve("cantiere_S_N", "cantiere_E_W", identifier="cantiere_S_N_to_cantiere_E_W", category="dirt")  #32
sim.create_quadratic_bezier_curve("cantiere_W_E", "cantiere_N_S", identifier="cantiere_W_E_to_cantiere_N_S", category="dirt")  #33

# Cubi - Viale Usberti / Cantiere
sim.create_quadratic_bezier_curve("Cubi_S_N_Up", "viale_usberti_dx_dx", identifier="Cubi_S_N_Up_to_viale_usberti_dx_dx")  #34
sim.create_quadratic_bezier_curve("viale_usberti_dx_sx", "Cubi_N_S_Up", identifier="viale_usberti_dx_sx_to_Cubi_N_S_Up")  #35
sim.create_quadratic_bezier_curve("Cubi_S_N_Up", "viale_usberti_sx_sx", identifier="Cubi_S_N_Up_to_viale_usberti_sx_sx")  #36
sim.create_quadratic_bezier_curve("viale_usberti_sx_dx", "Cubi_N_S_Up", identifier="viale_usberti_sx_dx_to_Cubi_N_S_Up")  #37
sim.create_quadratic_bezier_curve("Cubi_S_N_Up", "cantiere_S_N", identifier="Cubi_S_N_Up_to_cantiere_S_N")  #38
sim.create_quadratic_bezier_curve("cantiere_N_S", "Cubi_N_S_Up", identifier="cantiere_N_S_to_Cubi_N_S_Up")  #39
sim.create_quadratic_bezier_curve("viale_usberti_dx_sx", "cantiere_S_N", identifier="viale_usberti_dx_sx_to_cantiere_S_N")  #40
sim.create_quadratic_bezier_curve("viale_usberti_sx_dx", "cantiere_S_N", identifier="viale_usberti_sx_dx_to_cantiere_S_N")  #41
sim.create_quadratic_bezier_curve("cantiere_N_S", "viale_usberti_dx_dx", identifier="cantiere_N_S_to_viale_usberti_dx_dx")  #42

# Viale Usberti - tratto verticale destra
sim.create_segment((128, 307), (114, 450), identifier="viale_usberti_dx_S_N", category="general")  #43
sim.create_segment((110, 450), (124, 307), identifier="viale_usberti_dx_N_S", category="general")  #44
sim.create_segment((134, 245), (130, 298), identifier="viale_usberti_dx_S_N_down", category="general")  #45
sim.create_segment((126, 298), (130, 245), identifier="viale_usberti_dx_N_S_down", category="general")  #46

# Curve tratto verticale destra
sim.create_quadratic_bezier_curve("viale_usberti_dx_dx_Dx", "viale_usberti_dx_S_N_down", identifier="viale_usberti_dx_dx_to_viale_usberti_dx_S_N")  #47
sim.create_quadratic_bezier_curve("viale_usberti_dx_N_S_down", "viale_usberti_dx_sx_Dx", identifier="viale_usberti_dx_N_S_to_viale_usberti_dx_sx")  #48

# Collegamenti interni tratto verticale destra
sim.create_segment("viale_usberti_dx_S_N_down", "viale_usberti_dx_S_N", identifier="viale_usberti_dx_S_N_down_to_viale_usberti_dx_S_N", category="general")  #49
sim.create_segment("viale_usberti_dx_N_S", "viale_usberti_dx_N_S_down", identifier="viale_usberti_dx_N_S_to_viale_usberti_dx_N_S_down", category="general")  #50

# Viale Superiore e Viale Usberti alto
sim.create_segment((-258, 480), (80, 480), identifier="viale_superiore_dx_W_E", category="general")  #51
sim.create_segment((80, 484), (-258, 484), identifier="viale_superiore_dx_E_W", category="general")  #52
sim.create_segment((-266, 484), (-400, 484), identifier="viale_superiore_sx_E_W", category="general")  #53
sim.create_segment((-400, 480), (-266, 480), identifier="viale_superiore_sx_W_E", category="general")  #54
sim.create_segment((-260, 402), (-260, 478), identifier="viale_usberti_sx_S_N_UP", category="bus_lane")  #55
sim.create_segment((-264, 478), (-264, 402), identifier="viale_usberti_sx_N_S_UP", category="general")  #56
sim.create_segment((-260, 370), (-260, 392), identifier="viale_usberti_sx_S_N_Mid", category="bus_lane")  #57
sim.create_segment((-264, 392), (-264, 370), identifier="viale_usberti_sx_N_S_Mid", category="general")  #58
sim.create_segment((-290, 394), (-270, 394), identifier="parc_scienze_dx", category="general")  #59
sim.create_segment((-270, 398), (-290, 398), identifier="parc_scienze_sx", category="general")  #60

sim.create_segment("viale_usberti_sx_S_N_Mid", "viale_usberti_sx_S_N_UP", identifier="viale_usberti_sx_S_N_Mid_to_viale_usberti_sx_S_N_UP", category="bus_lane")  #61
sim.create_segment("viale_usberti_sx_N_S_UP", "viale_usberti_sx_N_S_Mid", identifier="viale_usberti_sx_N_S_UP_to_viale_usberti_sx_N_S_Mid", category="general")  #62

# Curve tratto alto
sim.create_quadratic_bezier_curve("viale_usberti_dx_S_N", "viale_superiore_dx_E_W", identifier="viale_usberti_dx_S_N_to_viale_superiore_dx_E_W")  #63
sim.create_quadratic_bezier_curve("viale_superiore_dx_W_E", "viale_usberti_dx_N_S", identifier="viale_superiore_dx_W_E_to_viale_usberti_dx_N_S")  #64
sim.create_quadratic_bezier_curve("parc_scienze_dx", "viale_usberti_sx_N_S_Mid", identifier="parc_scienze_dx_to_viale_usberti_sx_N_S_Mid")  #65
sim.create_quadratic_bezier_curve("viale_usberti_sx_N_S_UP", "parc_scienze_sx", identifier="viale_usberti_sx_N_S_UP_to_viale_scienze_sx")  #66

# Collegamenti Viale Superiore
sim.create_segment("viale_superiore_sx_W_E", "viale_superiore_dx_W_E", identifier="viale_superiore_sx_W_E_to_viale_superiore_dx_W_E", category="general")  #67
sim.create_segment("viale_superiore_dx_E_W", "viale_superiore_sx_E_W", identifier="viale_superiore_dx_E_W_to_viale_superiore_sx_E_W", category="general")  #68

# Curve Viale Superiore
sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N_UP", "viale_superiore_dx_W_E", identifier="viale_usberti_sx_S_N_UP_to_viale_superiore_dx_W_E")  #69
sim.create_quadratic_bezier_curve("viale_superiore_dx_E_W", "viale_usberti_sx_N_S_UP", identifier="viale_superiore_dx_E_W_to_viale_usberti_sx_N_S_UP")  #70
sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N_UP", "viale_superiore_sx_E_W", identifier="viale_usberti_sx_S_N_UP_to_viale_superiore_sx_E_W")  #71
sim.create_quadratic_bezier_curve("viale_superiore_sx_W_E", "viale_usberti_sx_N_S_UP", identifier="viale_superiore_sx_W_E_to_viale_usberti_sx_N_S_UP")  #72

# Viale Mensa
sim.create_segment((120, 304), (50, 284), identifier="viale_mensa_E_W", category="general", max_speed=5)  #73
sim.create_segment((50, 280), (120, 300), identifier="viale_mensa_W_E", category="general", max_speed=5)  #74
sim.create_segment((39, 213), (39, 260), identifier="viale_mensa_S_N", category="general", max_speed=5)  #75
sim.create_segment((35, 260), (35, 213), identifier="viale_mensa_N_S", category="general", max_speed=5)  #76

# Curve Viale Mensa
sim.create_quadratic_bezier_curve("viale_usberti_dx_N_S", "viale_mensa_E_W", identifier="viale_usberti_dx_N_S_to_viale_mensa_E_W")  #77
sim.create_quadratic_bezier_curve("viale_mensa_W_E", "viale_usberti_dx_S_N", identifier="viale_mensa_W_E_to_viale_usberti_dx_S_N")  #78
sim.create_quadratic_bezier_curve("viale_usberti_dx_S_N_down", "viale_mensa_E_W", identifier="viale_usberti_dx_S_N_down_to_viale_mensa_E_W")  #79
sim.create_quadratic_bezier_curve("viale_mensa_W_E", "viale_usberti_dx_N_S_down", identifier="viale_mensa_W_E_to_viale_usberti_dx_N_S_down")  #80
sim.create_quadratic_bezier_curve("viale_usberti_dx_sx_Dx", "viale_mensa_S_N", identifier="viale_usberti_dx_sx_Dx_to_viale_mensa_S_N")  #81
sim.create_quadratic_bezier_curve("viale_usberti_dx_dx", "viale_mensa_S_N", identifier="viale_usberti_dx_dx_to_viale_mensa_S_N")  #82
sim.create_quadratic_bezier_curve("viale_mensa_N_S", "viale_usberti_dx_sx", identifier="viale_mensa_N_S_to_viale_usberti_dx_sx")  #83
sim.create_quadratic_bezier_curve("viale_mensa_N_S", "viale_usberti_dx_dx_Dx", identifier="viale_mensa_N_S_to_viale_usberti_dx_dx_Dx")  #84
sim.create_quadratic_bezier_curve("viale_usberti_dx_dx", "viale_usberti_dx_dx_Dx", identifier="viale_usberti_dx_dx_to_viale_usberti_dx_dx_Dx")  #85
sim.create_quadratic_bezier_curve("viale_usberti_dx_sx_Dx", "viale_usberti_dx_sx", identifier="viale_usberti_dx_sx_Dx_to_viale_usberti_dx_sx")  #86
sim.create_quadratic_bezier_curve("viale_mensa_S_N", "viale_mensa_W_E", identifier="viale_mensa_S_N_to_viale_mensa_W_E", )  #87
sim.create_quadratic_bezier_curve("viale_mensa_E_W", "viale_mensa_N_S", identifier="viale_mensa_E_W_to_viale_mensa_N_S")  #88

# Viale Usberti sinistra - tratto basso
sim.create_segment((-260, 230), (-260, 290), identifier="viale_usberti_sx_S_N", category="bus_lane")  #89
sim.create_segment((-264, 290), (-264, 230), identifier="viale_usberti_sx_N_S", category="general")  #90

# Curve tratto basso sinistro
sim.create_quadratic_bezier_curve("viale_usberti_sx_N_S", "viale_usberti_sx_dx_Sx", identifier="viale_usberti_sx_N_S_to_viale_usberti_sx_dx")  #91
sim.create_quadratic_bezier_curve("viale_usberti_sx_sx_Sx", "viale_usberti_sx_S_N", identifier="viale_usberti_sx_sx_to_viale_usberti_sx_S_N", category="bus_lane")  #92

# Viale Usberti lavori
sim.create_segment((-262, 320), (-262, 350), identifier="viale_usberti_lavori_S_N", category="work_zone")  #93
sim.create_segment((-262, 350), (-262, 320), identifier="viale_usberti_lavori_N_S", category="work_zone")  #94

# Curve lavori
sim.create_quadratic_bezier_curve("viale_usberti_lavori_N_S", "viale_usberti_sx_N_S", identifier="viale_usberti_lavori_N_S_to_viale_usberti_sx_N_S")  #95
sim.create_quadratic_bezier_curve("viale_usberti_sx_S_N", "viale_usberti_lavori_S_N", identifier="viale_usberti_sx_S_N_to_viale_usberti_lavori_S_N", category="bus_lane")  #96
sim.create_quadratic_bezier_curve("viale_usberti_sx_N_S_Mid", "viale_usberti_lavori_N_S", identifier="viale_usberti_lavori_N_S_to_viale_usberti_sx_N_S")  #97
sim.create_quadratic_bezier_curve("viale_usberti_lavori_S_N", "viale_usberti_sx_S_N_Mid", identifier="viale_usberti_lavori_S_N_to_viale_usberti_sx_S_N_Mid", category="bus_lane")  #98

# Parcheggio lato usberti
sim.create_segment((-160, 215), (-160, 230), identifier="usberti_parcheggio")  #99
sim.create_segment((-164, 230), (-164, 215), identifier="parcheggio_usberti")  #100

sim.create_segment("viale_usberti_sx_sx", "viale_usberti_sx_sx_Sx", identifier="viale_usberti_sx_sx_to_viale_usberti_sx_sx_Sx", category="bus_lane")  #101
sim.create_segment("viale_usberti_sx_dx_Sx", "viale_usberti_sx_dx", identifier="viale_usberti_sx_dx_Sx_to_viale_usberti_sx_dx")  #102

# Curve parcheggio usberti
sim.create_quadratic_bezier_curve("viale_usberti_sx_dx_Sx", "usberti_parcheggio", identifier="viale_usberti_sx_dx_Sx_to_usberti_parcheggio")  #103
sim.create_quadratic_bezier_curve("parcheggio_usberti", "viale_usberti_sx_dx", identifier="parcheggio_usberti_to_viale_usberti_sx_dx")  #104



sim.create_intersection([
    {"segment_index": 1, "clearance_distance": 5.0, },
    {"segment_index": 12, "clearance_distance": 5.0, },
    {"segment_index": 17, "clearance_distance": 5.0, },
    {"segment_index": 8, "clearance_distance": 5.0, },
])

sim.create_intersection([
    {"segment_index": 3, "clearance_distance": 5.0, },
    {"segment_index": 7, "clearance_distance": 5.0, },
    {"segment_index": 5, "clearance_distance": 5.0, },
    {"segment_index": 0, "clearance_distance": 5.0, },
])

sim.create_intersection([
    {"segment_index": 9, "clearance_distance": 5.0, },
    {"segment_index": 76, "clearance_distance": 5.0, },
    {"segment_index": 10, "clearance_distance": 5.0, }
])

sim.create_intersection([
    {"segment_index": 45, "clearance_distance": 5.0, },
    {"segment_index": 44, "clearance_distance": 5.0, },
    {"segment_index": 74, "clearance_distance": 5.0, },
])

sim.create_intersection([
    {"segment_index": 52, "clearance_distance": 5.0, },
    {"segment_index": 54, "clearance_distance": 5.0, },
    {"segment_index": 55, "clearance_distance": 5.0, },
])

sim.create_intersection([
    {"segment_index": 56, "clearance_distance": 5.0, },
    {"segment_index": 59, "clearance_distance": 5.0, },
    {"segment_index": 57, "clearance_distance": 5.0, },
])

sim.create_intersection([
    {"segment_index": 14, "clearance_distance": 5.0, },
    {"segment_index": 100, "clearance_distance": 5.0, },
    {"segment_index": 13, "clearance_distance": 5.0, },
])


seg_lavori_SN = sim.get_segment_by_id("viale_usberti_sx_S_N")
seg_lavori_NS = sim.get_segment_by_id("viale_usberti_sx_N_S_Mid")

seg_lavori_SN.add_traffic_light([
    ("green", 20),
    ("red", 30)
])

seg_lavori_NS.add_traffic_light([
    ("red", 20),
    ("green", 30)
])


sim.create_vehicle_generator(
    vehicle_rate=4,
    vehicles=[
        (1, {
            "path": [3,22,1,34,9,85,11,47,45,49,43,63,52,68,53], 
            "vehicle_class": "car", 
            "engine_type": "combustion"
        })
    ]
)

sim.create_vehicle_generator(
    vehicle_rate=4,
    vehicles=[
        (1, {
            "path": [3,22,1,34,9,82,75,87,74,78,43,63,52,68,53], 
            "vehicle_class": "car", 
            "engine_type": "combustion"
        })
    ]
)


sim.create_vehicle_generator(
    vehicle_rate=4,
    vehicles=[
        (1, {
            "path": [54,72,56,62,58,97,94,95,90,91,14,102,12,37,0,26,4], 
            "vehicle_class": "car", 
            "engine_type": "electric"
        })
    ]
)

sim.create_vehicle_generator(
    vehicle_rate=4,
    vehicles=[
        (1, {
            "path": [100,104,12,21,9,82,75,87,74,78,43,63,52,68,53], 
            "vehicle_class": "car", 
            "engine_type": "electric"
        })
    ]
)


sim.create_vehicle_generator(
    vehicle_rate=1,
    vehicles=[
        (1, {
            "path": [3,22,1,34,9,85,11,47,45,49,43,63,52,68,53], 
            "vehicle_class": "car", 
            "engine_type": "combustion"
        })
    ]
)

sim.create_vehicle_generator(
    vehicle_rate=1,
    vehicles=[
        (1, {
            "path": [3,22,1,38,16,32,18], 
            "vehicle_class": "truck", 
            "engine_type": "combustion"
        })
    ]
)

sim.create_vehicle_generator(
    vehicle_rate=1,
    vehicles=[
        (1, {
            "path": [3,22,1,36,13,101,15,92,89,96,93,98,57,61,55,71,53], 
            "vehicle_class": "bus", 
            "engine_type": "combustion",
            "v_max": 5.5
        })
    ]
)

win = ts.Window(sim)
win.show()