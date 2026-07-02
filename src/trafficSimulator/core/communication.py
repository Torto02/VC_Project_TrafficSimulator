import json

class CommunicationManager:
    def __init__(self, simulation):
        self.simulation = simulation
        self.last_send_time = 0
        self.send_interval = 2.0  # Frequenza di invio dei dati al TIS (es. ogni 2 secondi)

    def update(self):
        if self.simulation.t - self.last_send_time >= self.send_interval:
            self.publish_telemetry()
            self.last_send_time = self.simulation.t

    def publish_telemetry(self):
        payload = []
        for veh_id, veh in self.simulation.vehicles.items():
            # Escludiamo gli ostacoli fittizi dalla telemetria
            if getattr(veh, 'vehicle_class', '') in ['animal', 'roadwork']:
                continue
            
            # Formattazione del pacchetto dati
            data = {
                "vehicle_id": str(veh_id)[:8],
                "class": getattr(veh, 'vehicle_class', 'car'),
                "kinematics": {
                    "speed": round(veh.v, 2),
                    "acceleration": round(veh.a, 2),
                    "position_x": round(veh.x, 2)
                }
            }
            # Integrazione dei dati OBU (Sensori, Motore, Emissioni)
            if hasattr(veh, 'obu_data'):
                data["obu"] = veh.obu_data
                
            payload.append(data)
        
        if payload:
            print(f"\n[MQTT/TIS] 📡 Pubblicazione telemetria per {len(payload)} veicoli aggregati via RSU...")
            # Scommenta la riga seguente per visualizzare l'effettivo JSON formattato nel terminale
            # print(json.dumps(payload, indent=2))