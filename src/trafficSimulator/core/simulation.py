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


# --- NUOVI METODI HELPER PER IL COLLEGAMENTO SMART ---
    def get_segment_by_id(self, identifier):
        """Trova un segmento stradale usando il suo nome mnemonico"""
        for seg in self.segments:
            if seg.identifier == identifier:
                return seg
        raise ValueError(f"[Errore] Segmento '{identifier}' non trovato. Assicurati di crearlo prima di collegarlo.")

    def _get_intersection(self, p1, p2, p3, p4):
        """Calcola l'intersezione di due rette (necessario per calcolare il punto di controllo perfetto delle curve)"""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            # Linee parallele (nessuna intersezione netta): usiamo il punto medio
            return ((x2 + x3) / 2, (y2 + y3) / 2)

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
        return (px, py)


    # --- MODIFICA METODI DI CREAZIONE ---
    def create_segment(self, *args, identifier="", max_speed=16.6, category="general", material="asphalt"):
        # Se l'utente passa due stringhe (es: "Strada_A", "Strada_B")
        if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
            start_seg = self.get_segment_by_id(args[0])
            end_seg = self.get_segment_by_id(args[1])
            points = (start_seg.points[-1], end_seg.points[0]) # Collega la fine della prima all'inizio della seconda
        else:
            # Comportamento classico a coordinate
            points = args
            
        seg = Segment(points, identifier=identifier, max_speed=max_speed, category=category, material=material)
        self.add_segment(seg)
        return seg

    def create_quadratic_bezier_curve(self, pt1, pt2, pt3=None, identifier="", max_speed=16.6, category="general", material="asphalt"):
        # Se l'utente passa due stringhe per collegare due strade
        if isinstance(pt1, str) and isinstance(pt2, str):
            start_seg = self.get_segment_by_id(pt1)
            end_seg = self.get_segment_by_id(pt2)
            
            actual_start = start_seg.points[-1]
            actual_end = end_seg.points[0]
            
            # Calcolo automatico del punto di controllo (Tangenza perfetta)
            p1 = start_seg.points[-2] if len(start_seg.points) > 1 else start_seg.points[0]
            p2 = actual_start
            p3 = actual_end
            p4 = end_seg.points[1] if len(end_seg.points) > 1 else end_seg.points[-1]
            
            actual_control = self._get_intersection(p1, p2, p3, p4)
        else:
            # Comportamento classico
            actual_start = pt1
            actual_control = pt2
            actual_end = pt3
            
        cur = QuadraticCurve(actual_start, actual_control, actual_end, identifier=identifier, max_speed=max_speed, category=category, material=material)
        self.add_segment(cur)
        return cur

    def create_cubic_bezier_curve(self, pt1, pt2, pt3=None, pt4=None, identifier="", max_speed=16.6, category="general", material="asphalt"):
        # Le curve cubiche richiedono ancora coordinate esplicite dato che hanno due punti di controllo liberi.
        cur = CubicCurve(pt1, pt2, pt3, pt4, identifier=identifier, max_speed=max_speed, category=category, material=material)
        self.add_segment(cur)
        return cur

    def create_vehicle_generator(self, **kwargs):
        gen = VehicleGenerator(kwargs)
        self.add_vehicle_generator(gen)

    def run(self, steps):
        for _ in range(steps):
            self.update()

    # MODIFICA METODO UPDATE (Da sostituire interamente la sezione dei veicoli)
    def update(self):
        # 1. Update Semafori
        for segment in self.segments:
            if getattr(segment, 'traffic_light', None):
                segment.traffic_light.update(self.dt)

        # 2. Update Veicoli e Logica Ostacoli
        for segment in self.segments:
            segment.vehicles = deque(sorted(segment.vehicles, key=lambda v_id: self.vehicles[v_id].x, reverse=True))

            if len(segment.vehicles) != 0:
                first_veh = self.vehicles[segment.vehicles[0]]
                tl_lead = None
                
                # LOGICA SEMAFORO: Se è rosso/giallo, crea un blocco virtuale 2 metri prima della fine
                if getattr(segment, 'traffic_light', None) and segment.traffic_light.state in ["red", "yellow"]:
                    stop_line = segment.get_length() - 2.0
                    # Applica il blocco SOLO se il veicolo non ha già superato la linea di arresto
                    if first_veh.x < stop_line:
                        tl_lead = Vehicle({'x': stop_line, 'v': 0, 'l': 0})
                
                first_veh.update(tl_lead, self.dt)

            for i in range(1, len(segment.vehicles)):
                self.vehicles[segment.vehicles[i]].update(self.vehicles[segment.vehicles[i-1]], self.dt)

        # 3. Check uscita confini e rimozione (Invariato dall'ultimo fix topologia aperta)
        for segment in self.segments:
            while len(segment.vehicles) > 0:
                vehicle_id = segment.vehicles[0]
                vehicle = self.vehicles[vehicle_id]
                
                if vehicle.x >= segment.get_length():
                    if vehicle.current_road_index + 1 < len(vehicle.path):
                        vehicle.current_road_index += 1
                        next_road_index = vehicle.path[vehicle.current_road_index]
                        self.segments[next_road_index].vehicles.append(vehicle_id)
                        vehicle.x = 0
                        segment.vehicles.popleft()
                    else:
                        segment.vehicles.popleft()
                        del self.vehicles[vehicle_id]
                else:
                    break

        for gen in self.vehicle_generator:
            gen.update(self)

        if hasattr(self, 'event_manager'): self.event_manager.update()
        if hasattr(self, 'communication_manager'): self.communication_manager.update()

        self.t += self.dt
        self.frame_count += 1