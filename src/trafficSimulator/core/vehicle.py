import uuid
import numpy as np

class Vehicle:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):
        self.id = uuid.uuid4()
        self.l = 4
        self.s0 = 4
        self.T = 1
        self.v_max = 16.6
        self.a_max = 1.44
        self.b_max = 4.61
        self.path = []
        self.current_road_index = 0
        self.x = 0
        self.v = 0
        self.a = 0
        self.stopped = False
        

        self.vehicle_class = "car" # 'car', 'truck', 'bus', 'electric'
        self.engine_type = "combustion" # 'combustion', 'electric', 'hybrid'
        

        self.obu_data = {
            "co2_emissions": 0.0,
            "engine_rpm": 800,
            "ac_temp": 22.0,
            "ambient_light": "high",
            "fog_lights": False,
            "rain_sensor": False
        }

    # funzione per inizializzare le proprietà derivate dalla configurazione
    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max
        
        # Modifica automatica della fisica base a seconda della classe
        if self.vehicle_class == "truck":
            self.l = 8          # Veicolo più lungo
            self.v_max = 12.0   # Meno veloce
            self.a_max = 0.9    # Accelerazione ridotta
        elif self.vehicle_class == "bus":
            self.l = 10
            self.v_max = 10.0
        elif self.vehicle_class == "electric":
            self.engine_type = "electric"
            self.a_max = 2.0    # Accelerazione bruciante tipica degli EV

    # Funzione per aggiornare lo stato del veicolo in base al veicolo che lo precede e al delta time (ovvero il tempo trascorso dall'ultimo aggiornamento, 
    # usato per calcolare la nuova posizione e velocità)
    def update(self, lead, dt):
        # Aggiorna la posizione e la velocità
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
                 
        # Aggiorna l'accelazione
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v
            
            # Se la distanza dal veicolo che precede è troppo piccola, forza un'accelerazione negativa molto forte per evitare collisioni
            if delta_x <= 0.1:
                alpha = 50 
            else:
                alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x
                
        #  Aggiorna l'accelerazione del veicolo in base alla velocità attuale, alla velocità massima e al parametro alpha calcolato sopra
        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -self.b_max*self.v/self.v_max
            
            
        # Aggiorna i dati simulati dell'OBU (On-Board Unit) se la funzione update_telemetry è stata definita 
        if hasattr(self, 'update_telemetry'):
            self.update_telemetry()

    # Funzione per aggiornare i dati simulati dell'OBU (On-Board Unit) del veicolo, come giri del motore e emissioni di CO2, basandosi sulla fisica attuale del veicolo
    def update_telemetry(self):
        """Calcola e aggiorna i valori simulati dell'OBU basandosi sulla fisica attuale"""
        speed_factor = max(0, min(1, self.v / self.v_max)) # 0.0 -> 1.0
        
        # RPM del Motore
        if self.engine_type == "combustion":
            base_rpm = 800
            # Aumenta i giri con la velocità e li fa schizzare con l'accelerazione
            calculated_rpm = base_rpm + int(speed_factor * 2500) + int(self.a * 200)
            self.obu_data["engine_rpm"] = max(base_rpm, calculated_rpm)
            
            # Emissioni di CO2 (approssimazione g/s)
            idle_emission = 0.5
            accel_penalty = max(0, self.a) * 2.5 # Emette molto in accelerazione
            speed_penalty = speed_factor * 1.5   # Consuma di più ad alte velocità
            self.obu_data["co2_emissions"] = idle_emission + accel_penalty + speed_penalty
            
        elif self.engine_type == "electric":
            # I motori elettrici ruotano a regimi molto più elevati
            self.obu_data["engine_rpm"] = int(speed_factor * 12000)
            self.obu_data["co2_emissions"] = 0.0 # Zero emissioni dirette

    def update(self, lead, dt):
        # Update position and velocity
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -self.b_max*self.v/self.v_max
        