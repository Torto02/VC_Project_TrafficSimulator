from collections import deque # Aggiungi questa riga
import math

from .config import Config
from .event_manager import EventManager
from .communication import CommunicationManager
from .vehicle_generator import VehicleGenerator
from .geometry.quadratic_curve import QuadraticCurve
from .geometry.cubic_curve import CubicCurve
from .geometry.segment import Segment
from .vehicle import Vehicle
from .intersection_manager import IntersectionManager


class Simulation:
    def __init__(self, config_file="config.json"):
        self.config = Config(config_file)
        self.segments = []
        self.vehicles = {}
        self.vehicle_generator = []
        self.t = 0.0
        self.frame_count = 0
        self.dt = 1 / self.config.get("simulation.fps", 60)
        self.environment = self.config.get("environment", [])
        self.intersection_manager = IntersectionManager(self)
        
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

    def update(self):
        # 1. Update Semafori
        for segment in self.segments:
            if getattr(segment, 'traffic_light', None):
                segment.traffic_light.update(self.dt)

        # 2. Update Veicoli e Logica Ostacoli
        for idx, segment in enumerate(self.segments):
            segment.vehicles = deque(sorted(segment.vehicles, key=lambda v_id: self.vehicles[v_id].x, reverse=True))
            
            if len(segment.vehicles) != 0:
                first_veh = self.vehicles[segment.vehicles[0]]
                virtual_lead = None
                
                # --- Semafori ---
                if getattr(segment, 'traffic_light', None) and segment.traffic_light.state in ["red", "yellow"]:
                    stop_line = segment.get_length() - 2.0
                    if first_veh.x < stop_line:
                        virtual_lead = Vehicle({'x': stop_line, 'v': 0, 'l': 0})
                
                # --- Intersection Manager (Incroci configurati manualmente) ---
                inter_lead = self.intersection_manager.get_virtual_lead(idx)
                if inter_lead and (virtual_lead is None or inter_lead.x < virtual_lead.x):
                    virtual_lead = inter_lead

                # --- FIX FISICO: Code spillback e MERGE CONCORRENTE ---
                if first_veh.current_road_index + 1 < len(first_veh.path):
                    next_road_index = first_veh.path[first_veh.current_road_index + 1]
                    next_segment = self.segments[next_road_index]
                    
                    # CASO A: Il segmento successivo è già occupato (code)
                    if len(next_segment.vehicles) > 0:
                        last_veh_next = self.vehicles[next_segment.vehicles[-1]]
                        projected_x = segment.get_length() + last_veh_next.x
                        
                        next_seg_lead = Vehicle({
                            'x': projected_x,
                            'v': last_veh_next.v,
                            'l': last_veh_next.l
                        })
                        if virtual_lead is None or next_seg_lead.x < virtual_lead.x:
                            virtual_lead = next_seg_lead
                    
                    # CASO B: Gestione precedenze sui bivi multipli
                    # Cerchiamo se c'è un altro veicolo su una strada diversa che vuole entrare nel nostro stesso next_segment
                    for other_idx, other_seg in enumerate(self.segments):
                        if other_idx == idx or len(other_seg.vehicles) == 0:
                            continue
                            
                        other_first = self.vehicles[other_seg.vehicles[0]]
                        
                        if other_first.current_road_index + 1 < len(other_first.path) and \
                           other_first.path[other_first.current_road_index + 1] == next_road_index:
                            
                            dist_self = segment.get_length() - first_veh.x
                            dist_other = other_seg.get_length() - other_first.x
                            
                            # Chi è più vicino al bivio ha la precedenza. A parità di distanza, diamo precedenza per ID di strada.
                            if dist_other < dist_self or (dist_other == dist_self and other_idx < idx):
                                stop_line_merge = segment.get_length() - 2.0
                                
                                # Frena solo se non ha già superato la linea di stop
                                if first_veh.x < stop_line_merge:
                                    merge_yield_lead = Vehicle({'x': stop_line_merge, 'v': 0, 'l': 0})
                                    if virtual_lead is None or merge_yield_lead.x < virtual_lead.x:
                                        virtual_lead = merge_yield_lead

                first_veh.update(virtual_lead, self.dt)
                
            for i in range(1, len(segment.vehicles)):
                self.vehicles[segment.vehicles[i]].update(self.vehicles[segment.vehicles[i-1]], self.dt)
                
        # 3. Check uscita confini e rimozione
        for segment in self.segments:
            while len(segment.vehicles) > 0:
                vehicle_id = segment.vehicles[0]
                vehicle = self.vehicles[vehicle_id]
                
                if vehicle.x >= segment.get_length():
                    if vehicle.current_road_index + 1 < len(vehicle.path):
                        next_road_index = vehicle.path[vehicle.current_road_index + 1]
                        next_segment = self.segments[next_road_index]
                        
                        # Controlla se c'è fisicamente spazio nel nuovo segmento
                        can_enter = (
                            len(next_segment.vehicles) == 0 
                            or self.vehicles[next_segment.vehicles[-1]].x > vehicle.s0 + vehicle.l
                        )
                        
                        if can_enter:
                            vehicle.current_road_index += 1
                            next_segment.vehicles.append(vehicle_id)
                            vehicle.x = 0
                            segment.vehicles.popleft()
                        else:
                            # FIX SICUREZZA MATH:
                            # Se non può entrare, lo inchiodiamo sul limite del segmento per evitare l'overlapping IDM negativo.
                            vehicle.x = segment.get_length()
                            vehicle.v = 0
                            break
                    else:
                        segment.vehicles.popleft()
                        del self.vehicles[vehicle_id]
                else:
                    break

        # Aggiornamenti componenti secondari
        for gen in self.vehicle_generator:
            gen.update(self)
            
        if hasattr(self, 'event_manager'): self.event_manager.update()
        if hasattr(self, 'intersection_manager'): self.intersection_manager.update()
        if hasattr(self, 'communication_manager'): self.communication_manager.update()
        
        self.t += self.dt
        self.frame_count += 1

    

    def create_intersection(self, arms, mode="fcfs"):
        return self.intersection_manager.add_intersection(arms, mode=mode)