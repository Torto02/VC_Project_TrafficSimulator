# Traffic Simulator - Relazione di Progetto

## 1. Topologie Avanzate e Incroci

**Richiesta: Definire nuove topologie con segmenti multipli e intersezioni (es. Campus Scienze UNIPR, piccolo distretto, ecc.).**

**Implementazione**: Il simulatore di base è stato esteso per supportare la creazione di mappe urbane complesse, nello specifico è stata mappata una versione semplificata del Campus dell'Università di Parma (file ``unipr_map.py``)

Per gestire gli svincoli complessi e le intersezioni senza semafori, è stata sviluppata una classe dedicata `IntersectionManager`. Questa controlla il diritto di precedenza utilizzando una logica First-Come, First-Served (FCFS), calcolando il tempo di arrivo dei veicoli alla linea di stop e inserendo virtualmente un veicolo (ostacolo) invisibile per costringere gli altri a cedere la precedenza, azzerando le collisioni.

**Esempio di utilizzo:**

```python
# Creazione di strade e rami dell'incrocio
sim.create_segment((30, 210), (4, 210), identifier="viale_usberti_dx_sx")
sim.create_segment((-158, 206), (-10, 206), identifier="viale_usberti_sx_dx")

# Gestione di un incrocio definendo la distanza di arresto per ogni ramo
sim.create_intersection([
    {"segment_index": 1, "clearance_distance": 5.0},
    {"segment_index": 12, "clearance_distance": 5.0},
    {"segment_index": 17, "clearance_distance": 5.0}
], mode="fcfs")
```

## 2. Categorie e Materiali Stradali

**Richiesta: Disegnare i segmenti stradali con colori e spessori diversi in base a categoria (corsia generale, corsia bus, taxi) e materiale (asfalto, ghiaia, sterrato).**

**Implementazione:** Il costruttore della classe astratta `Segment` (e di  `QuadraticCurve`  e  `CubicCurve`) è stato modificato per accettare i parametri  `category` (default: "general") e `material` (default: "asphalt"). All'interno del motore di rendering grafico (classe  `Window` in `window.py`), il metodo `draw_segments` decodifica questi attributi per modificare dinamicamente lo stile visivo del tracciato. Il rendering standard disegna asfalto in grigio chiaro; se la strada è di categoria `bus_lane`, viene renderizzata in rosato; se è categorizzata come `work_zone`, viene disegnata in arancione; infine, se la categoria è `dirt` o il materiale è `gravel`, il tracciato assume un colore marrone per simulare lo sterrato.

**Esempio di utilizzo:**

```python
# Corsia standard in asfalto (default)
sim.create_segment((110, 450), (124, 307), identifier="viale_usberti_dx_N_S")

# Corsia preferenziale riservata agli autobus
sim.create_segment((-10, 210), (-158, 210), identifier="viale_usberti_sx_sx", category="bus_lane")

# Strada sterrata per cantieri
sim.create_segment((0, 212), (0, 245), identifier="cantiere_S_N", category="dirt", material="gravel")

# Zona lavori stradali
sim.create_segment((-262, 320), (-262, 350), identifier="viale_usberti_lavori_S_N", category="work_zone")
```

## 3. Limite di Velocità e Segnaletica Intelligente V2I

**Richiesta: Includere una proprietà per la velocità massima nei segmenti stradali, predisponendola per la gestione di warning inviati da elementi su strada (es. sistemi di controllo della velocità) verso i veicoli.**

**Implementazione**: Nel costruttore delle geometrie stradali è stato aggiunto l'attributo `max_speed` (con un valore di default di 16.6 m/s, circa 60 km/h) ed è stata integrata nel modulo CommunicationManager. Quando un veicolo attraversa il raggio di coperturadi una RSU, viene simulata una comunicazione *Vehicle-to-Infrastructure* (V2I): l'RSU invia una notifica all'OBU del veicolo per aggiornare dinamicamente la sua velocità massima consentita (v_max) se il limite stradale locale è più restrittivo di quello preimpostato dalla classe del veicolo.

**Esempio di utilizzo:**

```python
# Creazione di un segmento stradale con limite di velocità
sim.create_segment((-262, 320), (-262, 350), identifier="viale_usberti_lavori_S_N", max_speed=40.0)

# il CommunicationManager gestisce il cambio di velocità:
if rsu_id and segment.max_speed < veh._v_max:
   veh.v_max = segment.max_speed  # Il veicolo frena per rispettare il nuovo limite
```

## 4. Frecce Direzionali di Marcia

**Richiesta: Disegnare una freccia all'interno di ogni carreggiata stradale per evidenziare la corretta direzione del viaggio.**

```python
# Le frecce direzionali vengono generate automaticamente per ogni strada definita nel simulatore.
# Non è necessario alcun comando manuale, è sufficiente creare il tracciato:

sim.create_segment((110, 450), (124, 307), identifier="viale_usberti_dx_N_S")
# Genererà automaticamente una freccia orientata verso il basso (Nord -> Sud) al centro del segmento.
```

## 5. Identificatori Mnemonici e Costruzione Dinamica

**Richiesta: Aggiungere la possibilità di assegnare un identificatore "mnemonico" (una stringa) ai segmenti stradali, per semplificare la loro gestione e il loro utilizzo durante la creazione della topologia.**

**Implementazione:** Ogni segmento è stato arricchito con l'attributo `identifier`. Per sfruttarl la classe `Simulation` è stata modificata con la funzione `get_segment_by_id(identifier)`, che permette di ricercare un tratto stradale semplicemente dal suo nome.

Le funzioni costruttrici (create_segment e create_quadratic_bezier_curve) ora accettano sia le classiche coordinate matematiche, sia direttamente gli identificatori in formato stringa. 

**Esempio di utilizzo:**

```python
# 1. Si creano i segmenti assegnando un identificatore mnemonico
sim.create_segment((30, 210), (4, 210), identifier="viale_usberti_dx")
sim.create_segment((-158, 206), (-10, 206), identifier="viale_usberti_sx")

# 2. Si collegano automaticamente richiamandoli per nome (il simulatore estrarrà i punti di inizio/fine in autonomia)
sim.create_segment("viale_usberti_dx", "viale_usberti_sx", identifier="collegamento_dritto")

# 3. Creazione di una curva automatica: il simulatore calcola da solo il vertice di tangenza per la curva di Bézier!
sim.create_quadratic_bezier_curve("viale_usberti_dx", "viale_usberti_sx", identifier="curva_morbida_usberti")
```

## 6. Classi Veicolari Differenziate

**Richiesta: Introdurre la possibilità di definire una "classe" per i veicoli, disegnandoli con colori e/o forme diverse in base a questa proprietà aggiuntiva (es. auto, camion, bus, veicolo elettrico, ecc.).**

**Implementazione:** Alla classe `Vehicle` è stato aggiunto l'attributo `vehicle_class`: nel metodo di inizializzazione (`init_properties`), la fisica del veicolo muta in base alla classe. I camion (`truck`) e i bus (`bus`) subiscono un aumento di lunghezza (rispettivamente 8 e 10 metri) e una limitazione sull'accelerazione. I veicoli elettrici (`electric`), invece, ottengono una risposta in accelerazione (`a_max`) molto più rapida, simulando l'erogazione di coppia immediata dei motori a batteria. Nel motore grafico (`window.py`), il renderer differenzia visivamente il traffico:

- **Car (Auto):** Blu standard
- **Electric (Elettrica):** Verde acceso
- **Truck (Camion):** Marrone (spessore maggiorato)
- **Bus (Autobus):** Arancione (spessore maggiorato)

**Esempio di utilizzo:**

```python
# Generazione di flussi di traffico misto basato sulle classi veicolari
sim.create_vehicle_generator(
    vehicle_rate=40,
    vehicles=[
        # Alta probabilità (peso 6) di generare un'auto
        (6, {"path": [3, 22, 1, 34], "vehicle_class": "car"}),

        # Probabilità inferiore (peso 2) di generare un mezzo elettrico scattante
        (2, {"path": [3, 22, 1, 34], "vehicle_class": "electric"}),

        # Probabilità rara (peso 1) di generare un mezzo pesante e lento
        (1, {"path": [92, 89, 96], "vehicle_class": "truck"})
    ]
)
```

## 7. On-Board Unit (OBU) e Telemetria

**Richiesta: Includere informazioni aggiuntive gestite dalle OBU a bordo dei veicoli (es. emissioni CO2, tipo di motore, RPM, temperatura AC, sensori, ecc.).**

**Implementazione:** La classe `Vehicle` è stata arricchita con il dizionario di stato `obu_data`. Invece di limitarsi a valori statici, è stata implementata una funzione di calcolo dinamico (`update_telemetry`) che viene richiamata a ogni step della simulazione. 

La telemetria è direttamente accoppiata al motore del veicolo:

- **Motori a combustione**: I giri del motore (RPM) e le emissioni di CO2 variano in funzione dello `speed_factor` e subiscono un forte aumento durante l'accelerazione
- **Motori elettrici**:Generano zero emissioni di CO2 e operano a regimi RPM calcolati in modo differenziato.
- I valori di base per AC e sensori luce/pioggia possono essere preimpostati dal file JSON.

## 8. Configurazione JSON (GUI e Simulazione)

**Richiesta: Definire un file di configurazione (es. in formato JSON) per impostare la GUI (colori, dimensioni) e parametri della simulazione.**

**Implementazione**: È stata creata la classe `Config` per il parsing di file esterni (es. `unipr.json`). Questo permette al JSON di gestire in modo centralizzato i dati:

- Le impostazioni della finestra (risoluzione, titolo, colore di sfondo).
- I flussi di traffico
- Il posizionamento degli elementi infrastrutturali (Ambiente).
- La programmazione temporale degli eventi.

**Esempio di utilizzo**

```python
{
  "gui": {
    "window_title": "Traffic Simulator - Campus UNIPR",
    "width": 1280,
    "height": 720,
    "bg_color": [245, 245, 250]
  },
  "simulation": {
    "fps": 60
  }
}

#Nel main della simulazione:
sim = ts.Simulation(config_file="unipr.json") # Inizializza tutto dal JSON
```

## 9. Ambiente eRSU

**Richiesta: Aggiungere componenti ambientali (alberi, edifici, RSU, ecc.)**

**Implementazione**: Il sistema di rendering grafico è stato dotato di una funzioni che legge dal JSON e disegna edifici (building), alberi (tree) e parcheggi e altri elementi.

Per le comunicazioni, è stata integrata la Road-Side Unit (RSU). Tramite il `CommunicationManager`,  a intervalli regolari viene calcolata la distanza euclidea tra i veicoli e le RSU.  Se un veicolo entra nel raggio di copertura:

1. Aggrega i dati  (velocità, posizione) e la telemetria OBU del veicolo in un payload JSON formattato e lo "pubblica" a terminale, simulando la trasmissione verso un controllore remoto 
2. L'RSU invia eventuali limiti di velocità locali all'OBU, che adatta la fisica di guida del mezzo in tempo reale.

**Esempio di utilizzo:**

```python
// Configurazione nel file JSON per ambiente e RSU
"environment": [
  { "type": "building", "x": 70, "y": 250, "width": 40, "height": 20, "id": "mensa" },
  { "type": "tree", "x": -130, "y": 185, "radius": 10, "id": "albero1" },
  { "type": "rsu", "x": -260, "y": 380, "coverage": 130, "id": "rsu_usberti_polo_scienze" }
]
```

## 10. Gestione Eventi (Lavori, Animali)

**Richiesta: Implementare eventi accidentali (es. cantieri, attraversamento di animali) programmati nel tempo che generino congestione.**

**Implementazione:** Il modulo `EventManager` legge gli eventi dal file JSON e li inietta nella simulazione allo scadere del tempo (`trigger_time`).  L'evento crea un veicolo fittizio sul tracciato stradale con velocità fissa a zero e gli viene assegnata una classe (es: animal o work_zone). In questo modo, le auto in arrivo rilevano l'animale come se fosse l'auto che le precede, e applicano nativamente l'algoritmo di car-following per frenare e accodarsi. Alla fine della durata dell'evento, il veicolo fittizio viene eliminato e il traffico riprende naturalmente.

L'EventManager supporta anche eventi periodici tramite il parametro period.

```python
"events": [
  {
    "type": "animal",       // Tipo di evento (animal, work_zone)
    "segment": 1,           // Indice della strada interessata
    "position": 30,         // Posizione spaziale sul tratto
    "trigger_time": 10.0,   // Inizio evento al secondo 10
    "duration": 50.0,       // Durata del blocco in secondi prima dello sblocco
    "period": 45            // Opzionale: ripete l'evento ciclicamente
  }
]
```