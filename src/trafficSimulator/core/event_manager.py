from collections import deque
from .vehicle import Vehicle

class EventManager:
    def __init__(self, simulation):
        self.simulation = simulation
        self.events = simulation.config.get("events", [])
        self.active_obstacles = [] # Traccia gli ostacoli attivi per rimuoverli
        self.triggered_events = set()

    def update(self):
        t = self.simulation.t
        
        # 1. Attivazione nuovi eventi (con supporto alla periodicità)
        for i, event in enumerate(self.events):
            is_periodic = "period" in event
            
            if is_periodic:
                period = event["period"]
                trigger_time = event.get("trigger_time", 0)
                # Imposta l'ultimo trigger a un valore fittizio per farlo scattare la prima volta
                last_trigger = event.get("last_trigger_time", trigger_time - period)
                
                # Se abbiamo superato il trigger_time iniziale e il periodo è trascorso
                if t >= trigger_time and t >= last_trigger + period:
                    self.trigger_event(event)
                    event["last_trigger_time"] = t
            else:
                # Evento singolo classico
                if i not in self.triggered_events and t >= event.get("trigger_time", 0):
                    self.trigger_event(event)
                    self.triggered_events.add(i)
                
        # 2. Rimozione eventi scaduti
        for obs_data in self.active_obstacles[:]:
            if t >= obs_data['expire_time']:
                self.remove_event(obs_data)
                self.active_obstacles.remove(obs_data)

    def trigger_event(self, event):
        event_type = event.get("type", "obstacle")
        segment_idx = event.get("segment", 0)
        pos_x = event.get("position", 50)
        duration = event.get("duration", 15.0) # Durata di default
        
        length = 2.0 if event_type == "animal" else 8.0
        
        # Creazione ostacolo
        obstacle = Vehicle({
            "path": [segment_idx],
            "x": pos_x,
            "v": 0,
            "a": 0,
            "vehicle_class": event_type,
            "l": length
        })
        
        obstacle.update = lambda lead, dt: None 
        
        if segment_idx < len(self.simulation.segments):
            segment = self.simulation.segments[segment_idx]
            segment.vehicles.append(obstacle.id)
            self.simulation.vehicles[obstacle.id] = obstacle
            
            # FIX CRUCIALE: Riordiniamo i veicoli sul segmento per posizione (x decrescente)
            # In questo modo il car-following rispetta sempre l'ordine spaziale fisico
            segment.vehicles = deque(sorted(segment.vehicles, key=lambda v_id: self.simulation.vehicles[v_id].x, reverse=True))
            
            self.active_obstacles.append({
                'obstacle_id': obstacle.id,
                'segment_idx': segment_idx,
                'expire_time': self.simulation.t + duration
            })
            print(f"[Event Manager] ⚠️ Evento attivato: {event_type.upper()} su segmento {segment_idx} (Dura {duration}s)")

    def remove_event(self, obs_data):
        obs_id = obs_data['obstacle_id']
        seg_idx = obs_data['segment_idx']
        
        # Rimuoviamo l'ostacolo dal segmento e dalla memoria centrale
        if seg_idx < len(self.simulation.segments):
            segment = self.simulation.segments[seg_idx]
            if obs_id in segment.vehicles:
                segment.vehicles.remove(obs_id)
                
        if obs_id in self.simulation.vehicles:
            del self.simulation.vehicles[obs_id]
            
        # FIX: Convertito obs_id in stringa prima di fare lo slicing [:4]
        print(f"[Event Manager] ✅ Evento {str(obs_id)[:4]}... risolto sul segmento {seg_idx}. Traffico in sblocco.")