import dearpygui.dearpygui as dpg
import math

class Window:
    """Gestisce la finestra grafica, i controlli e il rendering della simulazione."""

    def __init__(self, simulation):
        self.simulation = simulation
        self.config = simulation.config  
        
        
        self.window_width = self.config.get("gui.width", 1280)
        self.window_height = self.config.get("gui.height", 720)
        self.window_title = self.config.get("gui.window_title", "TrafficSimulator")
        self.bg_color = tuple(self.config.get("gui.bg_color", [250, 250, 250]))

        self.zoom = 1
        self.offset = (0, 0)
        self.speed = 1

        self.is_running = False

        self.is_dragging = False
        self.old_offset = (0, 0)
        self.zoom_speed = 1

        self.setup()
        self.setup_themes()
        self.create_windows()
        self.create_handlers()
        self.resize_windows()

    def setup(self):
        """Crea il contesto Dear PyGui e prepara il viewport principale."""
        dpg.create_context()
        
        dpg.create_viewport(title=self.window_title, width=self.window_width, height=self.window_height)
        dpg.setup_dearpygui()

    def setup_themes(self):
        """Definisce i temi grafici usati dall'interfaccia e dai pulsanti."""
        with dpg.theme() as global_theme:

            with dpg.theme_component(dpg.mvAll):
                # Stile comune per tutti gli elementi GUI.
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
                
                dpg.add_theme_color(dpg.mvThemeCol_Button, (90, 90, 95))
                dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 91, 140))
            with dpg.theme_component(dpg.mvInputInt):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (90, 90, 95), category=dpg.mvThemeCat_Core)
            

        dpg.bind_theme(global_theme)

        

        with dpg.theme(tag="RunButtonTheme"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (5, 150, 18))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (12, 207, 23))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (2, 120, 10))

        with dpg.theme(tag="StopButtonTheme"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (150, 5, 18))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (207, 12, 23))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (120, 2, 10))

    def create_windows(self):
        """Costruisce la finestra di simulazione e il pannello comandi."""
        dpg.add_window(
            tag="MainWindow",
            label="Simulation",
            no_close=True,
            no_collapse=True,
            no_resize=True,
            no_move=True
        )
        
        dpg.add_draw_node(tag="OverlayCanvas", parent="MainWindow")
        dpg.add_draw_node(tag="Canvas", parent="MainWindow")

        with dpg.window(
            tag="ControlsWindow",
            label="Controls",
            no_close=True,
            no_collapse=True,
            no_resize=True,
            no_move=True
        ):
            with dpg.collapsing_header(label="Simulation Control", default_open=True):

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Run", tag="RunStopButton", callback=self.toggle)
                    dpg.add_button(label="Next frame", callback=self.simulation.update)

                dpg.add_slider_int(tag="SpeedInput", label="Speed", min_value=1, max_value=100,default_value=1, callback=self.set_speed)
            
            with dpg.collapsing_header(label="Simulation Status", default_open=True):

                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    
                    with dpg.table_row():
                        dpg.add_text("Status:")
                        dpg.add_text("_", tag="StatusText")

                    with dpg.table_row():
                        dpg.add_text("Time:")
                        dpg.add_text("_s", tag="TimeStatus")

                    with dpg.table_row():
                        dpg.add_text("Frame:")
                        dpg.add_text("_", tag="FrameStatus")
            
            
            with dpg.collapsing_header(label="Camera Control", default_open=True):
    
                dpg.add_slider_float(tag="ZoomSlider", label="Zoom", min_value=0.1, max_value=100, default_value=self.zoom,callback=self.set_offset_zoom)            
                with dpg.group():
                    dpg.add_slider_float(tag="OffsetXSlider", label="X Offset", min_value=-100, max_value=100, default_value=self.offset[0], callback=self.set_offset_zoom)
                    dpg.add_slider_float(tag="OffsetYSlider", label="Y Offset", min_value=-100, max_value=100, default_value=self.offset[1], callback=self.set_offset_zoom)

    def resize_windows(self):
        """Adatta le dimensioni delle finestre alla viewport corrente."""
        width = dpg.get_viewport_width()
        height = dpg.get_viewport_height()

        # Il pannello controlli resta a sinistra, la scena occupa il resto.
        dpg.set_item_width("ControlsWindow", 300)
        dpg.set_item_height("ControlsWindow", height-38)
        dpg.set_item_pos("ControlsWindow", (0, 0))

        dpg.set_item_width("MainWindow", width-315)
        dpg.set_item_height("MainWindow", height-38)
        dpg.set_item_pos("MainWindow", (300, 0))

    def create_handlers(self):
        """Registra gli handler per mouse e ridimensionamento del viewport."""
        with dpg.handler_registry():
            dpg.add_mouse_down_handler(callback=self.mouse_down)
            dpg.add_mouse_drag_handler(callback=self.mouse_drag)
            dpg.add_mouse_release_handler(callback=self.mouse_release)
            dpg.add_mouse_wheel_handler(callback=self.mouse_wheel)
        dpg.set_viewport_resize_callback(self.resize_windows)

    def update_panels(self):
        """Aggiorna i testi di stato mostrati nel pannello laterale."""
        if self.is_running:
            dpg.set_value("StatusText", "Running")
            dpg.configure_item("StatusText", color=(0, 255, 0))
        else:
            dpg.set_value("StatusText", "Stopped")
            dpg.configure_item("StatusText", color=(255, 0, 0))
        
        
        dpg.set_value("TimeStatus", f"{self.simulation.t:.2f}s")
        dpg.set_value("FrameStatus", self.simulation.frame_count)

    def mouse_down(self):
        """Avvia il trascinamento della camera quando si clicca sulla scena."""
        if not self.is_dragging:
            if dpg.is_item_hovered("MainWindow"):
                self.is_dragging = True
                self.old_offset = self.offset
        
    def mouse_drag(self, sender, app_data):
        """Sposta la camera mentre il mouse viene trascinato."""
        if self.is_dragging:
            self.offset = (
                self.old_offset[0] + app_data[1]/self.zoom,
                self.old_offset[1] - app_data[2]/self.zoom 
            )

    def mouse_release(self):
        """Ferma il trascinamento della camera."""
        self.is_dragging = False

    def mouse_wheel(self, sender, app_data):
        """Imposta uno zoom graduale quando la rotellina e sopra la scena."""
        if dpg.is_item_hovered("MainWindow"):
            self.zoom_speed = 1 + 0.01*app_data

    def update_inertial_zoom(self, clip=0.005):
        """Applica uno zoom inerziale che si avvicina progressivamente a 1."""
        if self.zoom_speed != 1:
            self.zoom *= self.zoom_speed
            self.zoom_speed = 1 + (self.zoom_speed - 1) / 1.05
        if abs(self.zoom_speed - 1) < clip:
            self.zoom_speed = 1

    def update_offset_zoom_slider(self):
        """Allinea i widget della camera ai valori correnti della vista."""
        dpg.set_value("ZoomSlider", self.zoom)
        dpg.set_value("OffsetXSlider", self.offset[0])
        dpg.set_value("OffsetYSlider", self.offset[1])

    def set_offset_zoom(self):
        """Legge i valori dei slider e aggiorna zoom e offset."""
        self.zoom = dpg.get_value("ZoomSlider")
        self.offset = (dpg.get_value("OffsetXSlider"), dpg.get_value("OffsetYSlider"))

    def set_speed(self):
        """Legge lo slider e aggiorna la velocita di simulazione."""
        self.speed = dpg.get_value("SpeedInput")

    def to_screen(self, x, y):
        """Converte coordinate mondo in coordinate schermo."""
        return (
            self.canvas_width/2 + (x + self.offset[0] ) * self.zoom,
            self.canvas_height/2 - (y + self.offset[1]) * self.zoom 
        )

    def to_world(self, x, y):
        """Converte coordinate schermo in coordinate mondo."""
        return (
            (x - self.canvas_width/2) / self.zoom - self.offset[0],
            -(y - self.canvas_height/2) / self.zoom - self.offset[1] 
        )
    
    @property
    def canvas_width(self):
        """Larghezza disponibile per il canvas della simulazione."""
        return dpg.get_item_width("MainWindow")

    @property
    def canvas_height(self):
        """Altezza disponibile per il canvas della simulazione."""
        return dpg.get_item_height("MainWindow")

    def draw_bg(self, color=None):
        """Disegna lo sfondo della scena."""
        if color is None:
            color = self.bg_color 
        dpg.draw_rectangle(
            (-10, -10),
            (self.canvas_width+10, self.canvas_height+10), 
            thickness=0,
            fill=color,
            parent="OverlayCanvas"
        )

    def draw_axes(self, opacity=80):
        """Disegna gli assi cartesiani come riferimento visivo."""
        x_center, y_center = self.to_screen(0, 0)
        
        dpg.draw_line(
            (-10, y_center),
            (self.canvas_width+10, y_center),
            thickness=2, 
            color=(0, 0, 0, opacity),
            parent="OverlayCanvas"
        )
        dpg.draw_line(
            (x_center, -10),
            (x_center, self.canvas_height+10),
            thickness=2,
            color=(0, 0, 0, opacity),
            parent="OverlayCanvas"
        )

    def draw_grid(self, unit=10, opacity=50):
        """Disegna una griglia di riferimento con passo configurabile."""
        x_start, y_start = self.to_world(0, 0)
        x_end, y_end = self.to_world(self.canvas_width, self.canvas_height)
        
        
        n_x = int(min(x_start, x_end) / unit)
        m_x = int(max(x_start, x_end) / unit) + 1
        n_y = int(min(y_start, y_end) / unit)
        m_y = int(max(y_start, y_end) / unit) + 1

        for i in range(n_x, m_x):
            dpg.draw_line(
                self.to_screen(unit*i, min(y_start, y_end) - 10/self.zoom),
                self.to_screen(unit*i, max(y_start, y_end) + 10/self.zoom),
                thickness=1,
                color=(0, 0, 0, opacity),
                parent="OverlayCanvas"
            )

        for i in range(n_y, m_y):
            dpg.draw_line(
                self.to_screen(min(x_start, x_end) - 10/self.zoom, unit*i),
                self.to_screen(max(x_start, x_end) + 10/self.zoom, unit*i),
                thickness=1,
                color=(0, 0, 0, opacity),
                parent="OverlayCanvas"
            )

    def draw_segments(self):
        """Disegna i segmenti stradali e le luci semaforiche associate."""
        for segment in self.simulation.segments:
            # Colore base del tratto stradale.
            color = (180, 180, 220) 
            thickness = 3.5 * self.zoom
                         
            if hasattr(segment, 'material'):
                if segment.material == "gravel" or segment.category == "dirt":
                    color = (160, 140, 100) 
                elif segment.category == "bus_lane":
                    color = (200, 150, 150) 
                elif segment.category == "work_zone":
                    color = (244, 164, 96) 
                         
            dpg.draw_polyline(segment.points, color=color, thickness=thickness, parent="Canvas")
                         
            
            MIN_LENGTH_FOR_ARROW = 15.0  
            
            if segment.get_length() > MIN_LENGTH_FOR_ARROW:
                
                # La freccia indica il verso di percorrenza del segmento.
                center_pos = segment.get_point(0.5)
                heading = segment.get_heading(0.5)
                                 
                
                arrow_len = 2.0
                dx = math.cos(heading) * arrow_len
                dy = math.sin(heading) * arrow_len
                                 
                p1 = (center_pos[0] + dx, center_pos[1] + dy) 
                p2 = (center_pos[0] - dx, center_pos[1] - dy) 
                                 
                dpg.draw_arrow(p1, p2, thickness=0, size=3.0, color=(0, 0, 0, 80), parent="Canvas")

        
        for segment in self.simulation.segments:
            if getattr(segment, 'traffic_light', None):
                # Disegna il semaforo sulla fine del segmento.
                pos = segment.points[-1]
                state = segment.traffic_light.state
                
                if state == "green":
                    light_color = (0, 255, 0)
                elif state == "yellow":
                    light_color = (255, 200, 0)
                else:
                    light_color = (255, 0, 0)
                
                dpg.draw_circle(
                    center=pos, 
                    radius=4.5 * self.zoom, 
                    color=(50, 50, 50), 
                    fill=light_color, 
                    parent="Canvas"
                )

    def draw_vehicles(self):
        for segment in self.simulation.segments:
            for vehicle_id in segment.vehicles:
                vehicle = self.simulation.vehicles[vehicle_id]
                progress = vehicle.x / segment.get_length()
                position = segment.get_point(progress)
                heading = segment.get_heading(progress)
                node = dpg.add_draw_node(parent="Canvas")
                
                
                veh_color = (0, 0, 255) 
                veh_thickness = 1.76 * self.zoom
                
                if hasattr(vehicle, 'vehicle_class'):
                    if vehicle.vehicle_class == "truck":
                        veh_color = (139, 69, 19)   
                        veh_thickness = 2.5 * self.zoom
                    elif vehicle.vehicle_class == "bus":
                        veh_color = (255, 140, 0)   
                        veh_thickness = 2.5 * self.zoom
                    elif vehicle.vehicle_class == "electric":
                        veh_color = (0, 210, 0)     
                    elif vehicle.vehicle_class == "obstacle":
                        veh_color = (255, 0, 0)      
                        veh_thickness = 3.5 * self.zoom
                    elif vehicle.vehicle_class == "animal":
                        veh_color = (255, 255, 0)    
                        veh_thickness = 2.0 * self.zoom    

                dpg.draw_line(
                    (0, 0),
                    (vehicle.l, 0),
                    thickness=veh_thickness,
                    color=veh_color,
                    parent=node
                )
                translate = dpg.create_translation_matrix(position)
                rotate = dpg.create_rotation_matrix(heading, [0, 0, 1])
                dpg.apply_transform(node, translate*rotate)

    def apply_transformation(self):
        screen_center = dpg.create_translation_matrix([self.canvas_width/2, self.canvas_height/2, -0.01])
        translate = dpg.create_translation_matrix(self.offset)
        
        scale = dpg.create_scale_matrix([self.zoom, -self.zoom]) 
        dpg.apply_transform("Canvas", screen_center*scale*translate)

    def render_loop(self):
        
        self.update_inertial_zoom()
        self.update_offset_zoom_slider()

        
        dpg.delete_item("OverlayCanvas", children_only=True)
        dpg.delete_item("Canvas", children_only=True)
        
        
        self.draw_bg()
        self.draw_axes()
        self.draw_grid(unit=10)
        self.draw_grid(unit=50)
        self.draw_segments()
        self.draw_vehicles()

        
        self.apply_transformation()

        
        self.update_panels()

        
        if self.is_running:
            self.simulation.run(self.speed)

    def show(self):
        """Mostra la viewport e avvia il ciclo principale dell'interfaccia."""
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            self.render_loop()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

    def run(self):
        """Avvia la simulazione e aggiorna il pulsante Run/Stop."""
        self.is_running = True
        dpg.set_item_label("RunStopButton", "Stop")
        dpg.bind_item_theme("RunStopButton", "StopButtonTheme")

    def stop(self):
        """Ferma la simulazione e ripristina il pulsante Run/Stop."""
        self.is_running = False
        dpg.set_item_label("RunStopButton", "Run")
        dpg.bind_item_theme("RunStopButton", "RunButtonTheme")

    def toggle(self):
        """Alterna lo stato della simulazione tra avvio e pausa."""
        if self.is_running: self.stop()
        else: self.run()

    def draw_environment(self):
        """Renderizza elementi decorativi o infrastrutturali sulla scena."""
        for item in self.simulation.environment:
            item_type = item.get("type")
            x = item.get("x", 0)
            y = item.get("y", 0)
            
            if item_type == "tree":
                # Alberi come cerchi verdi.
                radius = item.get("radius", 3) * self.zoom
                dpg.draw_circle(center=(x, y), radius=radius, color=(34, 139, 34), fill=(34, 139, 34, 200), parent="Canvas")
                
            elif item_type == "building":
                # Edifici come rettangoli semplici.
                w = item.get("width", 10)
                h = item.get("height", 10)
                dpg.draw_rectangle(pmin=(x, y), pmax=(x+w, y+h), color=(100, 100, 100), fill=(220, 220, 220), parent="Canvas")
                
            elif item_type == "rsu":
                # Le RSU mostrano area di copertura e antenna centrale.
                coverage = item.get("coverage", 50) * self.zoom
                antenna_radius = 1.5 * self.zoom
                
                dpg.draw_circle(center=(x, y), radius=coverage, color=(0, 200, 255, 100), fill=(0, 200, 255, 15), parent="Canvas")
                
                dpg.draw_circle(center=(x, y), radius=antenna_radius, color=(0, 0, 0), fill=(0, 200, 255), parent="Canvas")
            
            elif item_type == "parking":
                # Parcheggio con stalli disegnati a griglia.
                w = item.get("width", 80)
                h = item.get("height", 30)

                target_spot_w = 5
                target_spot_h = h/3

                cols = max(1, int(w // target_spot_w))
                spot_w = w / cols

                dpg.draw_rectangle(
                    pmin=(x, y),
                    pmax=(x + w, y + h),
                    color=(112, 128, 144),
                    fill=(112, 128, 144),
                    parent="Canvas"
                )

                for i in range(cols + 1):
                    line_x = x + i * spot_w
                    dpg.draw_line((line_x, y), (line_x, y + h), color=(255, 255, 255, 200), thickness=2, parent="Canvas")

                dpg.draw_line((x, y + h / 2), (x + w, y + h / 2), color=(255, 255, 255, 220), thickness=2, parent="Canvas")
            
            elif item_type == "other":
                # Placeholder generico per oggetti non classificati.
                w = item.get("width", 80)
                h = item.get("height", 30)
                dpg.draw_rectangle(pmin=(x, y), pmax=(x+w, y+h), color=(189, 183, 107), fill=(189, 183, 107), parent="Canvas")
                
    
    def draw_vehicles(self):
        """Disegna tutti i veicoli presenti sulla rete."""
        for segment in self.simulation.segments:
            for vehicle_id in segment.vehicles:
                vehicle = self.simulation.vehicles[vehicle_id]
                
                
                # Normalizza la posizione sul segmento per evitare valori fuori range.
                progress = vehicle.x / segment.get_length()
                progress = max(0.0, min(1.0, progress)) 
                
                
                position = segment.get_point(progress)
                heading = segment.get_heading(progress)
                node = dpg.add_draw_node(parent="Canvas")
                
                veh_color = (0, 0, 255) 
                veh_thickness = 1.76 * self.zoom
                
                if hasattr(vehicle, 'vehicle_class'):
                    if vehicle.vehicle_class == "truck":
                        veh_color = (139, 69, 19)   
                        veh_thickness = 2.5 * self.zoom
                    elif vehicle.vehicle_class == "bus":
                        veh_color = (255, 140, 0)   
                        veh_thickness = 2.5 * self.zoom
                    elif vehicle.vehicle_class == "electric":
                        veh_color = (0, 210, 0)     
                    elif vehicle.vehicle_class == "animal":
                        veh_color = (160, 82, 45)   
                        veh_thickness = 3.5 * self.zoom 
                    elif vehicle.vehicle_class == "roadwork":
                        veh_color = (220, 20, 60)   
                        veh_thickness = 4.0 * self.zoom

                # Il veicolo viene rappresentato come una linea orientata lungo la corsia.
                dpg.draw_line(
                    (0, 0),
                    (vehicle.l, 0),
                    thickness=veh_thickness,
                    color=veh_color,
                    parent=node
                )
                translate = dpg.create_translation_matrix(position)
                rotate = dpg.create_rotation_matrix(heading, [0, 0, 1])
                dpg.apply_transform(node, translate*rotate)

    
    def render_loop(self):
        """Esegue un singolo frame di rendering e aggiorna la simulazione."""
        self.update_inertial_zoom()
        self.update_offset_zoom_slider()
        
        
        dpg.delete_item("OverlayCanvas", children_only=True)
        dpg.delete_item("Canvas", children_only=True)
                 
        
        # Disegna prima sfondo e overlay, poi contenuti dinamici.
        self.draw_bg()
        self.draw_axes()
        self.draw_grid(unit=10)
        self.draw_grid(unit=50)
        
        
        self.draw_environment() 
        self.draw_segments()
        self.draw_vehicles()
        
        
        self.apply_transformation()
        
        
        self.update_panels()
        
        
        if self.is_running:
            self.simulation.run(self.speed)