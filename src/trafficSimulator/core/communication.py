import math
import json

class CommunicationManager:
    def __init__(self, simulation):
        # Riferimento alla simulazione per leggere veicoli, segmenti ed ambiente.
        self.simulation = simulation
        # Ultimo istante in cui sono stati pubblicati i dati telemetrici.
        self.last_send_time = 0
        # Intervallo minimo tra due invii telemetrici consecutivi.
        self.send_interval = 10.0 

    def _get_vehicle_world_pos(self, vehicle):
        """Restituisce la posizione reale del veicolo nel mondo simulato.

        La posizione viene calcolata sul segmento corrente usando il progresso
        del veicolo lungo la strada.
        """
        if vehicle.current_road_index >= len(vehicle.path):
            return None
        seg_idx = vehicle.path[vehicle.current_road_index]
        segment = self.simulation.segments[seg_idx]
        
        # Converte l'avanzamento lineare del veicolo in una frazione del segmento.
        progress = max(0.0, min(1.0, vehicle.x / segment.get_length()))
        return segment.get_point(progress)

    def _get_connected_rsu(self, veh_pos):
        """Trova la prima RSU che copre la posizione del veicolo.

        Se il veicolo è fuori copertura, restituisce `None`.
        """
        if veh_pos is None:
            return None
        
        vx, vy = veh_pos
        # Scorre tutte le RSU presenti nell'ambiente e verifica la distanza.
        for item in self.simulation.environment:
            if item.get("type") == "rsu":
                rx, ry = item.get("x", 0), item.get("y", 0)
                coverage = item.get("coverage", 50)
                dist = math.sqrt((vx - rx)**2 + (vy - ry)**2)
                if dist <= coverage:
                    return item.get("id", "rsu_unknown")
        return None

    def update(self):
        # Ogni ciclo prima aggiorna gli avvisi V2I, poi invia telemetria a intervalli.
        self.process_downlink_warnings()

        if self.simulation.t - self.last_send_time >= self.send_interval:
            self.publish_telemetry()
            self.last_send_time = self.simulation.t

    def process_downlink_warnings(self):
        """Aggiorna il limite di velocità dei veicoli in base alle RSU connesse."""
        for veh_id, veh in self.simulation.vehicles.items():
            # Veicoli speciali come animali e lavori stradali non ricevono questo trattamento.
            if getattr(veh, 'vehicle_class', '') in ['animal', 'roadwork']:
                continue

            # Recupera posizione corrente e RSU eventualmente raggiunta.
            pos = self._get_vehicle_world_pos(veh)
            rsu_id = self._get_connected_rsu(pos)

            if rsu_id and veh.current_road_index < len(veh.path):
                seg_idx = veh.path[veh.current_road_index]
                segment = self.simulation.segments[seg_idx]

                # Se il segmento ha un limite più basso, lo applica al veicolo.
                if hasattr(segment, 'max_speed') and segment.max_speed < veh._v_max:
                    veh.v_max = segment.max_speed
                else:
                    veh.v_max = veh._v_max  

            else:
                # Fuori copertura: ripristina il limite massimo originale.
                veh.v_max = veh._v_max  

    def publish_telemetry(self):
        """Costruisce e stampa il payload telemetrico dei veicoli connessi."""
        payload = []
        for veh_id, veh in self.simulation.vehicles.items():
            # Esclude i veicoli speciali anche dalla telemetria.
            if getattr(veh, 'vehicle_class', '') in ['animal', 'roadwork']:
                continue

            # Include solo i veicoli effettivamente in copertura RSU.
            pos = self._get_vehicle_world_pos(veh)
            rsu_id = self._get_connected_rsu(pos)
            
            if rsu_id:
                # Dati essenziali per l'invio V2I.
                data = {
                    "vehicle_id": str(veh_id)[:8],
                    "class": getattr(veh, 'vehicle_class', 'car'),
                    "connected_rsu": rsu_id,
                    "kinematics": {
                        "speed": round(veh.v, 2),
                        "acceleration": round(veh.a, 2),
                        "world_pos": [round(pos[0], 2), round(pos[1], 2)]
                    }
                }
                if hasattr(veh, 'obu_data'):
                    data["obu"] = veh.obu_data
                payload.append(data)
                
        if payload:
            # Stampa un riepilogo sintetico e il payload completo in JSON.
            print(f"[MQTT/TIS] t={self.simulation.t:.1f}s | Ricevuti {len(payload)} pacchetti V2I tramite RSU attive.")

            print(json.dumps(payload, indent=2))