# src/trafficSimulator/core/intersection_manager.py
from .vehicle import Vehicle


class IntersectionArm:
    def __init__(self, segment_index, stop_distance=None, clearance_distance=15.0):
        self.segment_index = segment_index
        self.stop_distance = stop_distance          # None -> length - 2.0 (auto)
        self.clearance_distance = clearance_distance  # quanto deve avanzare oltre per "liberare"

    def get_stop_distance(self, segment):
        if self.stop_distance is not None:
            return self.stop_distance
        return max(0.0, segment.get_length() - 2.0)


class Intersection:
    def __init__(self, arms, mode="fcfs"):
        self.arms = {a.segment_index: a for a in arms}
        self.mode = mode
        self.occupant_segment = None
        self.occupant_vehicle_id = None
        self.arrival_times = {}  # vehicle_id -> istante di arrivo alla stop line


class IntersectionManager:
    def __init__(self, simulation):
        self.simulation = simulation
        self.intersections = []

    def add_intersection(self, arms, mode="fcfs"):
        built = [a if isinstance(a, IntersectionArm) else IntersectionArm(**a) for a in arms]
        inter = Intersection(built, mode=mode)
        self.intersections.append(inter)
        return inter

    def update(self):
        for inter in self.intersections:
            self._release_if_cleared(inter)
            self._track_arrivals(inter)
            self._grant_priority(inter)

    def _release_if_cleared(self, inter):
        if inter.occupant_segment is None:
            return
        sim = self.simulation
        veh = sim.vehicles.get(inter.occupant_vehicle_id)
        arm = inter.arms[inter.occupant_segment]
        if veh is None:
            inter.occupant_segment = inter.occupant_vehicle_id = None
            return
        still_on_arm = (
            veh.current_road_index < len(veh.path)
            and veh.path[veh.current_road_index] == arm.segment_index
        )
        if not still_on_arm and veh.x >= arm.clearance_distance:
            inter.occupant_segment = inter.occupant_vehicle_id = None

    def _track_arrivals(self, inter):
        sim = self.simulation
        for seg_idx, arm in inter.arms.items():
            segment = sim.segments[seg_idx]
            if not segment.vehicles:
                continue
            first_id = segment.vehicles[0]
            first_veh = sim.vehicles[first_id]
            if first_veh.x >= arm.get_stop_distance(segment):
                inter.arrival_times.setdefault(first_id, sim.t)
            else:
                inter.arrival_times.pop(first_id, None)

    def _grant_priority(self, inter):
        if inter.occupant_segment is not None:
            return
        sim = self.simulation
        candidates = []
        for seg_idx in inter.arms:
            segment = sim.segments[seg_idx]
            if not segment.vehicles:
                continue
            first_id = segment.vehicles[0]
            if first_id in inter.arrival_times:
                candidates.append((inter.arrival_times[first_id], seg_idx, first_id))
        if candidates:
            candidates.sort(key=lambda c: c[0])  # FCFS
            _, seg_idx, veh_id = candidates[0]
            inter.occupant_segment, inter.occupant_vehicle_id = seg_idx, veh_id

    def get_virtual_lead(self, segment_index):
        """Se questo segmento non ha la precedenza, ritorna un veicolo fermo alla stop-line."""
        for inter in self.intersections:
            arm = inter.arms.get(segment_index)
            if arm and inter.occupant_segment not in (None, segment_index):
                segment = self.simulation.segments[segment_index]
                return Vehicle({'x': arm.get_stop_distance(segment), 'v': 0, 'l': 0})
        return None