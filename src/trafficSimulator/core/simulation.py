from collections import deque 
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
        # Carica la configurazione del progetto e inizializza lo stato globale della simulazione.
        self.config = Config(config_file)
        # Segmenti stradali presenti nel modello.
        self.segments = []
        # Dizionario di tutti i veicoli attivi, indicizzati per id.
        self.vehicles = {}
        # Generatori di veicoli che inseriscono nuovi mezzi nel tempo.
        self.vehicle_generator = []
        # Tempo simulato corrente.
        self.t = 0.0
        # Numero di frame già elaborati.
        self.frame_count = 0
        # Passo temporale della simulazione, derivato dal frame rate.
        self.dt = 1 / self.config.get("simulation.fps", 60)
        # Oggetti ambientali statici, come RSU o altri elementi infrastrutturali.
        self.environment = self.config.get("environment", [])
        # Gestore delle intersezioni.
        self.intersection_manager = IntersectionManager(self)
        
        
        # Gestori secondari che aggiornano eventi e comunicazioni V2I.
        self.event_manager = EventManager(self)
        self.communication_manager = CommunicationManager(self)

    def add_vehicle(self, veh):
        """Registra un veicolo nella simulazione e lo inserisce nel primo segmento del suo percorso."""
        self.vehicles[veh.id] = veh
        if len(veh.path) > 0:
            self.segments[veh.path[0]].add_vehicle(veh)

    def add_segment(self, seg):
        """Aggiunge un nuovo segmento stradale al grafo della simulazione."""
        self.segments.append(seg)

    def add_vehicle_generator(self, gen):
        """Registra un generatore che creerà nuovi veicoli durante l'esecuzione."""
        self.vehicle_generator.append(gen)

    def create_vehicle(self, **kwargs):
        """Crea un veicolo a partire dai parametri forniti e lo inserisce nella simulazione."""
        veh = Vehicle(kwargs)
       
        self.add_vehicle(veh)



    def get_segment_by_id(self, identifier):
        """Trova un segmento stradale usando il suo identificatore logico."""
        for seg in self.segments:
            if seg.identifier == identifier:
                return seg
        raise ValueError(f"[Errore] Segmento '{identifier}' non trovato. Assicurati di crearlo prima di collegarlo.")

    def _get_intersection(self, p1, p2, p3, p4):
        """Calcola il punto di intersezione tra due rette.

        Viene usato per stimare un buon punto di controllo nelle curve di Bezier.
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4

        # Se le rette sono parallele, usa un punto medio di fallback.
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            
            return ((x2 + x3) / 2, (y2 + y3) / 2)

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
        return (px, py)


    
    def create_segment(self, *args, identifier="", max_speed=16.6, category="general", material="asphalt"):
        """Crea un segmento lineare oppure collega due segmenti esistenti."""
        if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
            # Se riceve due id di segmenti, crea il collegamento usando i punti estremi.
            start_seg = self.get_segment_by_id(args[0])
            end_seg = self.get_segment_by_id(args[1])
            points = (start_seg.points[-1], end_seg.points[0]) 
        else:
            # Altrimenti usa direttamente i punti passati in input.
            points = args
            
        seg = Segment(points, identifier=identifier, max_speed=max_speed, category=category, material=material)
        self.add_segment(seg)
        return seg

    def create_quadratic_bezier_curve(self, pt1, pt2, pt3=None, identifier="", max_speed=16.6, category="general", material="asphalt"):
        """Crea una curva di Bezier quadratica tra due elementi o tre punti espliciti."""
        if isinstance(pt1, str) and isinstance(pt2, str):
            # Quando riceve due segmenti, calcola automaticamente il controllo.
            start_seg = self.get_segment_by_id(pt1)
            end_seg = self.get_segment_by_id(pt2)
            
            actual_start = start_seg.points[-1]
            actual_end = end_seg.points[0]
            
            
            # Usa i punti vicini ai segmenti per stimare una curva fluida.
            p1 = start_seg.points[-2] if len(start_seg.points) > 1 else start_seg.points[0]
            p2 = actual_start
            p3 = actual_end
            p4 = end_seg.points[1] if len(end_seg.points) > 1 else end_seg.points[-1]
            
            actual_control = self._get_intersection(p1, p2, p3, p4)
        else:
            # In alternativa usa i tre punti espliciti forniti dal chiamante.
            actual_start = pt1
            actual_control = pt2
            actual_end = pt3
            
        cur = QuadraticCurve(actual_start, actual_control, actual_end, identifier=identifier, max_speed=max_speed, category=category, material=material)
        self.add_segment(cur)
        return cur

    def create_cubic_bezier_curve(self, pt1, pt2, pt3=None, pt4=None, identifier="", max_speed=16.6, category="general", material="asphalt"):
        """Crea una curva di Bezier cubica e la aggiunge alla rete stradale."""
        cur = CubicCurve(pt1, pt2, pt3, pt4, identifier=identifier, max_speed=max_speed, category=category, material=material)
        self.add_segment(cur)
        return cur

    def create_vehicle_generator(self, **kwargs):
        """Crea e registra un generatore di veicoli."""
        gen = VehicleGenerator(kwargs)
        self.add_vehicle_generator(gen)

    def run(self, steps):
        """Esegue la simulazione per un numero dato di passi temporali."""
        for _ in range(steps):
            self.update()

    def update(self):
        """Avanza di un frame la simulazione aggiornando tutti i sottosistemi."""
        # Prima aggiorna i semafori, così il resto del ciclo usa lo stato corrente.
        for segment in self.segments:
            if getattr(segment, 'traffic_light', None):
                segment.traffic_light.update(self.dt)

        # Aggiorna i veicoli segmento per segmento, in ordine di avanzamento.
        for idx, segment in enumerate(self.segments):
            segment.vehicles = deque(sorted(segment.vehicles, key=lambda v_id: self.vehicles[v_id].x, reverse=True))
            
            if len(segment.vehicles) != 0:
                # Il primo veicolo del segmento è quello che influenza tutti gli altri.
                first_veh = self.vehicles[segment.vehicles[0]]
                virtual_lead = None
                
                
                # Se il semaforo è rosso o giallo, crea un leader virtuale sulla stop-line.
                if getattr(segment, 'traffic_light', None) and segment.traffic_light.state in ["red", "yellow"]:
                    stop_line = segment.get_length() - 2.0
                    if first_veh.x < stop_line:
                        virtual_lead = Vehicle({'x': stop_line, 'v': 0, 'l': 0})
                
                
                # Le intersezioni possono imporre un ulteriore vincolo di precedenza.
                inter_lead = self.intersection_manager.get_virtual_lead(idx)
                if inter_lead and (virtual_lead is None or inter_lead.x < virtual_lead.x):
                    virtual_lead = inter_lead

                
                # Gestisce anche il caso in cui il veicolo stia per entrare nel segmento successivo.
                if first_veh.current_road_index + 1 < len(first_veh.path):
                    next_road_index = first_veh.path[first_veh.current_road_index + 1]
                    next_segment = self.segments[next_road_index]
                    
                    
                    # Se il segmento successivo è già occupato, crea un leader virtuale proiettato.
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
                    
                    
                    
                    # Gestisce anche i conflitti di merge fra segmenti che convergono sullo stesso ramo.
                    for other_idx, other_seg in enumerate(self.segments):
                        if other_idx == idx or len(other_seg.vehicles) == 0:
                            continue
                            
                        other_first = self.vehicles[other_seg.vehicles[0]]
                        
                        if other_first.current_road_index + 1 < len(other_first.path) and \
                           other_first.path[other_first.current_road_index + 1] == next_road_index:
                            
                            dist_self = segment.get_length() - first_veh.x
                            dist_other = other_seg.get_length() - other_first.x
                            
                            
                            # Chi arriva prima al punto di merge ha la precedenza.
                            if dist_other < dist_self or (dist_other == dist_self and other_idx < idx):
                                stop_line_merge = segment.get_length() - 2.0
                                
                                
                                if first_veh.x < stop_line_merge:
                                    merge_yield_lead = Vehicle({'x': stop_line_merge, 'v': 0, 'l': 0})
                                    if virtual_lead is None or merge_yield_lead.x < virtual_lead.x:
                                        virtual_lead = merge_yield_lead

                # Aggiorna il veicolo di testa con eventuali vincoli virtuali.
                first_veh.update(virtual_lead, self.dt)
                
            # Aggiorna i veicoli seguenti usando come leader il veicolo davanti nello stesso segmento.
            for i in range(1, len(segment.vehicles)):
                self.vehicles[segment.vehicles[i]].update(self.vehicles[segment.vehicles[i-1]], self.dt)
                
        
        # Gestisce i passaggi da un segmento al successivo o la rimozione dei veicoli arrivati a destinazione.
        for segment in self.segments:
            while len(segment.vehicles) > 0:
                vehicle_id = segment.vehicles[0]
                vehicle = self.vehicles[vehicle_id]
                
                if vehicle.x >= segment.get_length():
                    if vehicle.current_road_index + 1 < len(vehicle.path):
                        # Prova a far entrare il veicolo nel segmento successivo solo se c'è spazio sufficiente.
                        next_road_index = vehicle.path[vehicle.current_road_index + 1]
                        next_segment = self.segments[next_road_index]
                        
                        
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
                            # Se non può entrare, si ferma esattamente alla fine del segmento.
                            vehicle.x = segment.get_length()
                            vehicle.v = 0
                            break
                    else:
                        # Se il percorso è finito, elimina il veicolo dalla simulazione.
                        segment.vehicles.popleft()
                        del self.vehicles[vehicle_id]
                else:
                    break

        # Aggiorna i generatori che possono introdurre nuovi veicoli.
        for gen in self.vehicle_generator:
            gen.update(self)
            
        # Aggiorna i sistemi ausiliari nell'ordine in cui dipendono dal tempo simulato.
        if hasattr(self, 'event_manager'): self.event_manager.update()
        if hasattr(self, 'intersection_manager'): self.intersection_manager.update()
        if hasattr(self, 'communication_manager'): self.communication_manager.update()
        
        # Avanza il tempo globale di simulazione.
        self.t += self.dt
        self.frame_count += 1

    

    def create_intersection(self, arms, mode="fcfs"):
        """Crea una nuova intersezione gestita da IntersectionManager."""
        return self.intersection_manager.add_intersection(arms, mode=mode)