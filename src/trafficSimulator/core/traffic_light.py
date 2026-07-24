class TrafficLight: # Rappresenta un semaforo con fasi multiple.
    def __init__(self, phases):
        # Sequenza delle fasi del semaforo, ciascuna come (stato, durata).
        self.phases = phases
        # Indice della fase attiva corrente.
        self.current_phase_index = 0
        # Tempo trascorso nella fase corrente.
        self.time_in_phase = 0.0
        # Stato iniziale del semaforo.
        self.state = self.phases[self.current_phase_index][0]

    def update(self, dt):
        """Avanza il tempo del semaforo e cambia fase quando la durata è terminata."""
        # Accumula il tempo trascorso nella fase corrente.
        self.time_in_phase += dt
        # Durata prevista per la fase attualmente attiva.
        current_phase_duration = self.phases[self.current_phase_index][1]
        
        # Quando la durata è finita, passa alla fase successiva in ciclo.
        if self.time_in_phase >= current_phase_duration:
            self.time_in_phase -= current_phase_duration
            self.current_phase_index = (self.current_phase_index + 1) % len(self.phases)
            self.state = self.phases[self.current_phase_index][0]