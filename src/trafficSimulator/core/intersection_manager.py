
from .vehicle import Vehicle


class IntersectionArm:
    def __init__(self, segment_index, stop_distance=None, clearance_distance=15.0):
        # Segmento che confluisce nell'intersezione.
        self.segment_index = segment_index
        # Distanza dalla quale il veicolo deve fermarsi se non è specificata altrove.
        self.stop_distance = stop_distance          
        # Distanza minima oltre la quale l'incrocio si considera liberato.
        self.clearance_distance = clearance_distance  

    def get_stop_distance(self, segment):
        # Se è stata configurata una stop-line esplicita, usa quella.
        if self.stop_distance is not None:
            return self.stop_distance
        # Altrimenti posiziona la stop-line quasi alla fine del segmento.
        return max(0.0, segment.get_length() - 2.0)


class Intersection:
    def __init__(self, arms, mode="fcfs"):
        # Mappa segmento -> braccio dell'intersezione.
        self.arms = {a.segment_index: a for a in arms}
        # Modalità di gestione della precedenza, di default first-come first-served.
        self.mode = mode
        # Segmento attualmente occupato dal veicolo con precedenza.
        self.occupant_segment = None
        # ID del veicolo che ha ottenuto la precedenza.
        self.occupant_vehicle_id = None
        # Tempi di arrivo dei veicoli alla stop-line.
        self.arrival_times = {}  


class IntersectionManager:
    def __init__(self, simulation):
        # Accesso alla simulazione per leggere segmenti, veicoli e tempo.
        self.simulation = simulation
        # Elenco delle intersezioni gestite.
        self.intersections = []

    def add_intersection(self, arms, mode="fcfs"):
        """Crea una nuova intersezione a partire dai bracci configurati."""
        built = [a if isinstance(a, IntersectionArm) else IntersectionArm(**a) for a in arms]
        inter = Intersection(built, mode=mode)
        self.intersections.append(inter)
        return inter

    def update(self):
        # Ogni intersezione viene aggiornata in tre fasi: rilascio, tracking, assegnazione.
        for inter in self.intersections:
            self._release_if_cleared(inter)
            self._track_arrivals(inter)
            self._grant_priority(inter)

    def _release_if_cleared(self, inter):
        """Libera l'intersezione quando il veicolo che l'occupa l'ha oltrepassata."""
        if inter.occupant_segment is None:
            return
        sim = self.simulation
        veh = sim.vehicles.get(inter.occupant_vehicle_id)
        arm = inter.arms[inter.occupant_segment]
        # Se il veicolo non esiste più, azzera lo stato di occupazione.
        if veh is None:
            inter.occupant_segment = inter.occupant_vehicle_id = None
            return
        # Il veicolo è ancora sul braccio se il suo segmento corrente coincide con quello dell'intersezione.
        still_on_arm = (
            veh.current_road_index < len(veh.path)
            and veh.path[veh.current_road_index] == arm.segment_index
        )
        # Se ha superato la clearance distance, l'intersezione torna libera.
        if not still_on_arm and veh.x >= arm.clearance_distance:
            inter.occupant_segment = inter.occupant_vehicle_id = None

    def _track_arrivals(self, inter):
        """Memorizza l'istante in cui il primo veicolo di un braccio raggiunge la stop-line."""
        sim = self.simulation
        for seg_idx, arm in inter.arms.items():
            segment = sim.segments[seg_idx]
            if not segment.vehicles:
                continue
            # Considera solo il primo veicolo della coda del segmento.
            first_id = segment.vehicles[0]
            first_veh = sim.vehicles[first_id]
            # Una volta arrivato alla stop-line, registra il tempo di arrivo.
            if first_veh.x >= arm.get_stop_distance(segment):
                inter.arrival_times.setdefault(first_id, sim.t)
            else:
                # Se arretra rispetto alla stop-line, rimuove la candidatura.
                inter.arrival_times.pop(first_id, None)

    def _grant_priority(self, inter):
        """Assegna la precedenza al veicolo arrivato prima tra i candidati."""
        if inter.occupant_segment is not None:
            return
        sim = self.simulation
        candidates = []
        for seg_idx in inter.arms:
            segment = sim.segments[seg_idx]
            if not segment.vehicles:
                continue
            # Un candidato è il primo veicolo del braccio che ha già raggiunto la stop-line.
            first_id = segment.vehicles[0]
            if first_id in inter.arrival_times:
                candidates.append((inter.arrival_times[first_id], seg_idx, first_id))
        if candidates:
            # FCFS: vince chi è arrivato prima.
            candidates.sort(key=lambda c: c[0])  
            _, seg_idx, veh_id = candidates[0]
            inter.occupant_segment, inter.occupant_vehicle_id = seg_idx, veh_id

    def get_virtual_lead(self, segment_index):
        """Restituisce un veicolo virtuale fermo alla stop-line se il braccio è bloccato.

        Serve come vincolo artificiale per impedire al veicolo reale di superare
        l'intersezione quando non ha la precedenza.
        """
        for inter in self.intersections:
            arm = inter.arms.get(segment_index)
            if arm and inter.occupant_segment not in (None, segment_index):
                # Crea un leader virtuale fermo nel punto di arresto del braccio.
                segment = self.simulation.segments[segment_index]
                return Vehicle({'x': arm.get_stop_distance(segment), 'v': 0, 'l': 0})
        return None