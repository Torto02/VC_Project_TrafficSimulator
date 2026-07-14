class TrafficLight:
    def __init__(self, phases):
        # phases è una lista di tuple, es: [("green", 10), ("yellow", 3), ("red", 15)]
        self.phases = phases
        self.current_phase_index = 0
        self.time_in_phase = 0.0
        self.state = self.phases[self.current_phase_index][0]

    def update(self, dt):
        self.time_in_phase += dt
        current_phase_duration = self.phases[self.current_phase_index][1]
        
        if self.time_in_phase >= current_phase_duration:
            self.time_in_phase -= current_phase_duration
            self.current_phase_index = (self.current_phase_index + 1) % len(self.phases)
            self.state = self.phases[self.current_phase_index][0]