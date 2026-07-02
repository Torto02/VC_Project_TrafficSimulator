from collections import deque # Aggiungi questa riga

from .config import Config
from .event_manager import EventManager
from .communication import CommunicationManager
from .vehicle_generator import VehicleGenerator
from .geometry.quadratic_curve import QuadraticCurve
from .geometry.cubic_curve import CubicCurve
from .geometry.segment import Segment
from .vehicle import Vehicle

class Simulation:
    # ... resto del codice ...
    def __init__(self, config_file="config.json"):
        self.config = Config(config_file)
        self.segments = []
        self.vehicles = {}
        self.vehicle_generator = []
        self.t = 0.0
        self.frame_count = 0
        self.dt = 1 / self.config.get("simulation.fps", 60)
        self.environment = self.config.get("environment", [])
        
        # --- FASE 4: Inizializzazione Managers ---
        self.event_manager = EventManager(self)
        self.communication_manager = CommunicationManager(self)

    def add_vehicle(self, veh):
        self.vehicles[veh.id] = veh
        if len(veh.path) > 0:
            self.segments[veh.path[0]].add_vehicle(veh)

    def add_segment(self, seg):
        self.segments.append(seg)

    def add_vehicle_generator(self, gen):
        self.vehicle_generator.append(gen)

    def create_vehicle(self, **kwargs):
        veh = Vehicle(kwargs)
        self.add_vehicle(veh)


    def create_segment(self, *args, identifier="", max_speed=16.6, category="general", material="asphalt"):
        seg = Segment(args, identifier=identifier, max_speed=max_speed, category=category, material=material)
        self.add_segment(seg)

    def create_quadratic_bezier_curve(self, start, control, end, identifier="", max_speed=16.6, category="general", material="asphalt"):
        cur = QuadraticCurve(start, control, end, identifier=identifier, max_speed=max_speed, category=category, material=material)
        self.add_segment(cur)

    def create_cubic_bezier_curve(self, start, control_1, control_2, end, identifier="", max_speed=16.6, category="general", material="asphalt"):
        cur = CubicCurve(start, control_1, control_2, end, identifier=identifier, max_speed=max_speed, category=category, material=material)
        self.add_segment(cur)

    def create_vehicle_generator(self, **kwargs):
        gen = VehicleGenerator(kwargs)
        self.add_vehicle_generator(gen)

    def run(self, steps):
        for _ in range(steps):
            self.update()

    def update(self):
        # Update vehicles
        for segment in self.segments:
            # FIX: Ordina l'array a ogni frame basandosi sulla coordinata x. 
            # Garantisce che chi sta fisicamente davanti sia sempre al primo posto nella logica.
            segment.vehicles = deque(sorted(segment.vehicles, key=lambda v_id: self.vehicles[v_id].x, reverse=True))
            
            if len(segment.vehicles) != 0:
                self.vehicles[segment.vehicles[0]].update(None, self.dt)
            for i in range(1, len(segment.vehicles)):
                self.vehicles[segment.vehicles[i]].update(self.vehicles[segment.vehicles[i-1]], self.dt)

        # Check roads for out of bounds vehicle
        for segment in self.segments:
            while len(segment.vehicles) > 0:
                vehicle_id = segment.vehicles[0]
                vehicle = self.vehicles[vehicle_id]
                
                # Se il veicolo supera la fine della strada
                if vehicle.x >= segment.get_length():
                    # Se c'è una strada successiva nel suo percorso
                    if vehicle.current_road_index + 1 < len(vehicle.path):
                        vehicle.current_road_index += 1
                        next_road_index = vehicle.path[vehicle.current_road_index]
                        self.segments[next_road_index].vehicles.append(vehicle_id)
                        vehicle.x = 0
                        segment.vehicles.popleft()
                    else:
                        # --- FIX TOPOLOGIA APERTA ---
                        # Il veicolo ha terminato il suo viaggio e scompare nel nulla.
                        segment.vehicles.popleft()       # Rimuovi dalla strada visiva
                        del self.vehicles[vehicle_id]    # Elimina l'oggetto dalla RAM
                else:
                    break

        # Update vehicle generators
        for gen in self.vehicle_generator:
            gen.update(self)

        # Update managers
        if hasattr(self, 'event_manager'):
            self.event_manager.update()
        if hasattr(self, 'communication_manager'):
            self.communication_manager.update()

        # Increment time
        self.t += self.dt
        self.frame_count += 1