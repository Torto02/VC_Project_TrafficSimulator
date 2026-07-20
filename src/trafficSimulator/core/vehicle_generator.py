from .vehicle import Vehicle
from numpy.random import randint

class VehicleGenerator:
    def __init__(self, config={}):
        # Imposta i valori di default e poi applica eventuali sovrascritture dal config.
        self.set_default_config()

        # Copia nella classe gli attributi presenti nella configurazione ricevuta.
        for attr, val in config.items():
            setattr(self, attr, val)

        # Prepara il primo veicolo da inserire nella simulazione.
        self.init_properties()

    def set_default_config(self):
        """Imposta la configurazione base del generatore."""
        # Numero medio di veicoli generati al minuto.
        self.vehicle_rate = 40
        # Lista di possibili veicoli con pesi di estrazione.
        self.vehicles = [
            (1, {})
        ]
        # Tempo dell'ultimo veicolo inserito.
        self.last_added_time = 0

    def init_properties(self):
        # Genera in anticipo il prossimo veicolo da provare a inserire.
        self.upcoming_vehicle = self.generate_vehicle()

    def generate_vehicle(self):
        """Estrae casualmente un veicolo tra quelli configurati, rispettando i pesi."""
        # Somma dei pesi usati per il sorteggio.
        total = sum(pair[0] for pair in self.vehicles)
        # Estrae un valore casuale tra 1 e il totale dei pesi.
        r = randint(1, total+1)
        for (weight, config) in self.vehicles:
            # Scala il valore casuale finché non ricade nel peso del veicolo selezionato.
            r -= weight
            if r <= 0:
                return Vehicle(config)

    def update(self, simulation):
        """Prova ad aggiungere un nuovo veicolo quando è trascorso abbastanza tempo."""
        # Converte il rate configurato in un intervallo temporale tra due inserimenti.
        if simulation.t - self.last_added_time >= 60 / self.vehicle_rate:
            # Verifica che il segmento di ingresso sia libero o abbia spazio sufficiente.
            segment = simulation.segments[self.upcoming_vehicle.path[0]]      
            if len(segment.vehicles) == 0\
               or simulation.vehicles[segment.vehicles[-1]].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.l:
                # Inserisce il veicolo nella simulazione e aggiorna il timestamp.
                simulation.add_vehicle(self.upcoming_vehicle)
                
                self.last_added_time = simulation.t
            # Prepara comunque il prossimo veicolo da tentare di inserire al tick successivo.
            self.upcoming_vehicle = self.generate_vehicle()
