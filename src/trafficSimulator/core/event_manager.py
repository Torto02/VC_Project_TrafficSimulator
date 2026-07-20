from collections import deque
from .vehicle import Vehicle

class EventManager:
    def __init__(self, simulation):
        # Riferimento alla simulazione per leggere tempo, segmenti e veicoli.
        self.simulation = simulation
        # Lista degli eventi caricati dalla configurazione.
        self.events = simulation.config.get("events", [])
        # Ostacoli/eventi attivi che devono essere rimossi allo scadere.
        self.active_obstacles = []
        # Tiene traccia degli eventi singoli già attivati.
        self.triggered_events = set()

    def update(self):
        """Controlla se qualche evento deve essere attivato o rimosso."""
        t = self.simulation.t

        # Scorre tutti gli eventi configurati e valuta se devono partire.
        for i, event in enumerate(self.events):
            is_periodic = "period" in event
            
            if is_periodic:
                # Gli eventi periodici si ripetono ogni `period` secondi.
                period = event["period"]
                trigger_time = event.get("trigger_time", 0)
            
                # Se non esiste ancora, usa un tempo iniziale compatibile con il periodo.
                last_trigger = event.get("last_trigger_time", trigger_time - period)

                # Attiva solo quando è scaduto il tempo minimo tra due attivazioni.
                if t >= trigger_time and t >= last_trigger + period:
                    self.trigger_event(event)
                    event["last_trigger_time"] = t
            else:
                # Gli eventi singoli vengono attivati una sola volta.
                if i not in self.triggered_events and t >= event.get("trigger_time", 0):
                    self.trigger_event(event)
                    self.triggered_events.add(i)

        # Rimuove gli ostacoli scaduti.
        for obs_data in self.active_obstacles[:]:
            if t >= obs_data['expire_time']:
                self.remove_event(obs_data)
                self.active_obstacles.remove(obs_data)

    def trigger_event(self, event):
        """Crea e inserisce nella simulazione un ostacolo/evento temporaneo."""
        event_type = event.get("type", "obstacle")
        segment_idx = event.get("segment", 0)
        pos_x = event.get("position", 50)
        duration = event.get("duration", 15.0)
        
        # Dimensione semplificata dell'ostacolo in base al tipo di evento.
        length = 2.0 if event_type == "animal" else 8.0
        

        # L'evento viene modellato come un veicolo fermo sul segmento indicato.
        obstacle = Vehicle({
            "path": [segment_idx],
            "x": pos_x,
            "v": 0,
            "a": 0,
            "vehicle_class": event_type,
            "l": length
        })
        
        # Impedisce che l'ostacolo venga mosso dalla logica normale dei veicoli.
        obstacle.update = lambda lead, dt: None 
        
        if segment_idx < len(self.simulation.segments):
            segment = self.simulation.segments[segment_idx]
            # Registra l'ostacolo nel segmento e nella lista globale dei veicoli.
            segment.vehicles.append(obstacle.id)
            self.simulation.vehicles[obstacle.id] = obstacle
            


            # Riordina i veicoli del segmento per mantenere coerente la gestione delle distanze.
            segment.vehicles = deque(sorted(segment.vehicles, key=lambda v_id: self.simulation.vehicles[v_id].x, reverse=True))
            
            # Memorizza quando l'evento dovrà essere rimosso.
            self.active_obstacles.append({
                'obstacle_id': obstacle.id,
                'segment_idx': segment_idx,
                'expire_time': self.simulation.t + duration
            })
            print(f"[Event Manager] ⚠️ Evento attivato: {event_type.upper()} su segmento {segment_idx} (Dura {duration}s)")

    def remove_event(self, obs_data):
        """Rimuove un ostacolo temporaneo dalla simulazione e dal segmento."""
        obs_id = obs_data['obstacle_id']
        seg_idx = obs_data['segment_idx']
        

        # Elimina il veicolo-ostacolo dal segmento se è ancora presente.
        if seg_idx < len(self.simulation.segments):
            segment = self.simulation.segments[seg_idx]
            if obs_id in segment.vehicles:
                segment.vehicles.remove(obs_id)
                
        # Rimuove l'istanza del veicolo dalla simulazione.
        if obs_id in self.simulation.vehicles:
            del self.simulation.vehicles[obs_id]
            

        # Messaggio di log per indicare che il traffico è tornato libero.
        print(f"[Event Manager] ✅ Evento {str(obs_id)[:4]}... risolto sul segmento {seg_idx}. Traffico in sblocco.")