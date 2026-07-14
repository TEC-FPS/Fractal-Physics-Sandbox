import pygame
import numpy as np
import random
import scipy.ndimage as ndimage
import sys
import time
import math
# =====================================================================
# LAYER 2 ARCHITECTURE - PART 1: THE VECTOR-DRIVEN CELL BLUEPRINT
# =====================================================================
class MacroMolecule:
    def __init__(self, x, y, inherited_fluid, inherited_nodes):
        # 1. OUTSIDE EXTERNAL STATE (Where the vessel floats on Layer 2)
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.radius = 25.0  # Fixed laboratory size standard (No forced scaling)
        
        # 2. INSIDE PRIVATE SANCTUARY (The Replicated Genetic Base)
        # Each cell clones the exact fluid grid and node pool at the moment of inception
        self.fluid_matrix = inherited_fluid.copy()
        self.nodes = [dict(n) for n in inherited_nodes] # Isolated deep copy of the family tree
        
        # Independent surface memory buffers to hold its private spacebar microscopic views
        self.snapshot_surface = pygame.Surface((800, 600))
        self.mini_map_surface = pygame.Surface((200, 150))
        
    def calculate_micro_locomotion(self):
        if len(self.nodes) > 0:
            # Let the true raw velocities add up honestly to break the diagonal lock
            raw_sum_vx = sum(n["vx"] for n in self.nodes)
            raw_sum_vy = sum(n["vy"] for n in self.nodes)
            
            # Use a balanced scaling factor so the heavy macro-cell drifts with mass
            momentum_scale = 0.00002  
            self.vx = raw_sum_vx * momentum_scale
            self.vy = raw_sum_vy * momentum_scale     

        else:
            self.vx = 0.0
            self.vy = 0.0

    def update_macro_physics_and_plow(self, macro_fluid, dt, sliders):
        # =====================================================================
        # LINE-FOR-LINE LAYER 1 SENSOR REPLICATION AT THE MACRO SCALE
        # =====================================================================
        current_speed = math.sqrt(self.vx**2 + self.vy**2) + 1e-5
        dx = self.vx / current_speed
        dy = self.vy / current_speed
        
        # Calculate left and right perpendicular shoulder vectors
        lx, ly = -dy, dx
        rx, ry = dy, -dx
        
        # Scale sensor distance relative to the giant macro-molecule radius
        sensor_dist = self.radius + 5.0
        nx_idx = int(self.x + dx * sensor_dist) % WIDTH
        ny_idx = int(self.y + dy * sensor_dist) % HEIGHT
        
        l_x = int(self.x + lx * (self.radius + 3.0)) % WIDTH
        l_y = int(self.y + ly * (self.radius + 3.0)) % HEIGHT
        r_x = int(self.x + rx * (self.radius + 3.0)) % WIDTH
        r_y = int(self.y + ry * (self.radius + 3.0)) % HEIGHT
        
        # Sniff out the macro-fluid pressures beneath its massive shoulders
        left_pressure = macro_fluid[l_x, l_y]
        right_pressure = macro_fluid[r_x, r_y]
        
        # Identical Shoulder Deflection Torque Steering
        torque = left_pressure - right_pressure
        # Direct link to your live dashboard dashboard knob!
 # Safe fallback gates: Reads raw floats or unwraps list containers seamlessly
        steer_val = sliders["steering"]
        steering_sensitivity = steer_val[0] if isinstance(steer_val, list) else steer_val
                
        # Accumulate steering deflection onto the macro-vectors
        self.vx += (lx * torque * steering_sensitivity * current_speed) * dt
        self.vy += (ly * torque * steering_sensitivity * current_speed) * dt
        
        # =====================================================================
        # KINETIC MASS DISPLACEMENT PLOW (IDENTICAL TO LAYER 1 ENGINE)
        # =====================================================================
        ix = max(0, min(WIDTH - 1, int(self.x)))
        iy = max(0, min(HEIGHT - 1, int(self.y)))
        local_macro_density = macro_fluid[ix, iy]
        
        # Scoop out a vacuum trench from the center core
        consumed_mass = local_macro_density * 0.10
        macro_fluid[ix, iy] = max(0.005, local_macro_density - consumed_mass)
        
        # Forcefully stamp that mass 90 degrees outward onto its massive shoulders
        stamp_idx_l_x = int(self.x + lx * self.radius) % WIDTH
        stamp_idx_l_y = int(self.y + ly * self.radius) % HEIGHT
        stamp_idx_r_x = int(self.x + rx * self.radius) % WIDTH
        stamp_idx_r_y = int(self.y + ry * self.radius) % HEIGHT
        
        half_stamp = consumed_mass * 0.5
        macro_fluid[stamp_idx_l_x, stamp_idx_l_y] += half_stamp
        macro_fluid[stamp_idx_r_x, stamp_idx_r_y] += half_stamp
        
         # Safe fallback gate: Handles raw floats or unwraps list containers smoothly
        ceil_val = sliders["ceiling_max"]
        ceiling_max = ceil_val if isinstance(ceil_val, list) else ceil_val

        if macro_fluid[stamp_idx_l_x, stamp_idx_l_y] > ceiling_max:
            macro_fluid[stamp_idx_l_x, stamp_idx_l_y] = ceiling_max
        if macro_fluid[stamp_idx_r_x, stamp_idx_r_y] > ceiling_max:
            macro_fluid[stamp_idx_r_x, stamp_idx_r_y] = ceiling_max

# FLUID MEDIUM RESISTANCE: Localized fluid thickness acts as an exponential terminal velocity brake
        _local_fluid_density = macro_fluid[ix, iy]
        
        # Calculate a dynamic macro drag coefficient based on the density the atom is standing on
        _macro_drag = 1.0 + (1.0 * _local_fluid_density)
        
        # Apply the fluid resistance directly to the atom's macro-velocity vectors
        # The faster the atom flies or the thicker the fluid, the harder the medium pushes back
        self.vx -= (self.vx * 0.03 * _macro_drag) * dt
        self.vy -= (self.vy * 0.03 * _macro_drag) * dt
        # =====================================================================
# LAYER 3 ARCHITECTURE - THE FRONTAL ELEMENT HULL BLUEPRINT
# =====================================================================
class MacroElement:
    def __init__(self, x, y, inherited_macro_fluid, live_atoms_list):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.radius = 33.3
        self.macro_fluid_matrix = inherited_macro_fluid
        self.atoms = live_atoms_list

    def update_internal_physics(self, dt, WIDTH, HEIGHT):
        """
        Forces the atoms trapped inside this Element to update their positions
        and physics frames while Layer 3 is actively viewed.
        """
        for atom in self.atoms:
            # Let the atom update its own internal Layer 1 nodes natively
            if hasattr(atom, 'update_internal_nodes'): 
                atom.update_internal_nodes(dt)
            
            # Call your atom's existing velocity update logic if it exists
            if hasattr(atom, 'update_physics'):
                atom.update_physics(dt)
                
            # Move the atom inside the element matrix
            atom.x += atom.vx * dt
            atom.y += atom.vy * dt
            
            # Torus wrapping for the internal atoms
            if atom.x < 0: atom.x = WIDTH
            elif atom.x > WIDTH: atom.x = 0
            if atom.y < 0: atom.y = HEIGHT
            elif atom.y > HEIGHT: atom.y = 0

    def calculate_element_locomotion(self):
        if len(self.atoms) > 0:
            raw_sum_vx = sum(atom.vx for atom in self.atoms)
            raw_sum_vy = sum(atom.vy for atom in self.atoms)
            
                        # Massive inertial scale factor to give it heavy macro-momentum
            momentum_scale = 0.005
            self.vx = raw_sum_vx * momentum_scale
            self.vy = raw_sum_vy * momentum_scale
            
            # --- LIVE MACRO-SHOULDER TORQUE STEERING (MIRRORED FROM PAGE 18) ---
            current_speed = math.sqrt(self.vx**2 + self.vy**2) + 1e-5
            heading_angle = math.atan2(self.vy, self.vx + 1e-5)
            
            # Extend the feeler sensors 12 pixels past the outer edge of the element hardshell
            sensor_dist = self.radius + 12.0
            
            # Calculate left and right perpendicular shoulder vectors
            left_sx = int(self.x + math.cos(heading_angle - 0.5) * sensor_dist) % WIDTH
            left_sy = int(self.y + math.sin(heading_angle - 0.5) * sensor_dist) % HEIGHT
            right_sx = int(self.x + math.cos(heading_angle + 0.4) * sensor_dist) % WIDTH
            right_sy = int(self.y + math.sin(heading_angle + 0.4) * sensor_dist) % HEIGHT
            
            # Sniff out the macro-fluid pressures beneath its massive shoulders
            left_density = self.macro_fluid_matrix[left_sx, left_sy]
            right_density = self.macro_fluid_matrix[right_sx, right_sy]
            
            # Hardcoded to your locked-in sweet spot sensitivity value from Page 18
            steering_strength = 7.1
            
                        # Accumulate steering deflection torque directly onto the macro-vectors
            if right_density > left_density:
                self.vx -= (right_density - left_density) * steering_strength * 0.1
            elif left_density > right_density:
                self.vx += (left_density - right_density) * steering_strength * 0.1

            # --- FLUID MEDIUM RESISTANCE FOR MACRO HULLS (MIRRORED FROM PAGE 3) ---
            # Map the exact spatial index coordinates of the Element's center core
            ix = max(0, min(WIDTH - 1, int(self.x)))
            iy = max(0, min(HEIGHT - 1, int(self.y)))
            
            # Sample the local fluid thickness directly beneath its massive hardshell
            _local_fluid_density = self.macro_fluid_matrix[ix, iy]
            
            # Calculate a dynamic macro drag coefficient based on the local density terrain
            _macro_drag = 1.0 + (2.0 * _local_fluid_density)
            
            # Apply the fluid resistance directly to the element's macro-velocity vectors
            # The faster the element flies or the thicker the fluid, the harder the medium pushes back
            self.vx -= (self.vx * 0.03 * _macro_drag) * dt
            self.vy -= (self.vy * 0.03 * _macro_drag) * dt
        else:
            self.vx = 0.0
            self.vy = 0.0

            # --- THE 10% THERMODYNAMIC TRICKLE-DOWN FIELDS ---
            # Capture the element's velocity shifts to calculate external perturbation forces
            if not hasattr(self, 'old_vx'):
                self.old_vx, self.old_vy = self.vx, self.vy
                
            impact_vx = self.vx - self.old_vx
            impact_vy = self.vy - self.old_vy
            
            # Mirror the exact 10% trickle-down ratio from Page 19/20
            trickle_factor = 0.10
            for atom in self.atoms:
                atom.vx += impact_vx * trickle_factor
                atom.vy += impact_vy * trickle_factor
                
            # Cache current velocities for the next frame physics tick
            self.old_vx, self.old_vy = self.vx, self.vy

# =====================================================================
# STEP 1: DIMENSIONS AND VIEWPORT CANVAS
# =====================================================================
WIDTH, HEIGHT = 800, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Thermodynamic Ecosystem - Clean Visual Lab")

# =====================================================================
# PHASE 2 INITIALIZATION: FORENSIC DUAL-WINDOW ARCHITECTURE
# =====================================================================
# 1. Create a completely independent secondary surface canvas for the time-lapse
# We match your master WIDTH and HEIGHT dimensions (800x600) for a 1:1 crisp ratio
snapshot_surface = pygame.Surface((WIDTH, HEIGHT))

# 2. Tell the OS window manager to launch a standalone Secondary Window
# This opens a separate driftable frame that you can drag anywhere on your desktop
# Note: In Pygame 2, this is achieved by opening a second window handle or using a sub-window context
# To guarantee 100% stability across all laptops without crashing Pygame's main event queue,
# we initialize an independent display surface context for the mirror.
pygame.display.set_caption("Universe Evolution Engine - Main Cosmos")

# We create an explicit variable to store the absolute historical tick track
audit_frame_counter_total = 0

# The master toggle switch for the corner time-lapse window (True = Visible, False = Hidden)
show_time_lapse = True

mini_map_surface = pygame.transform.smoothscale(snapshot_surface, (int(WIDTH * 0.25), int(HEIGHT * 0.25)))

pygame.font.init()
FONT = pygame.font.SysFont("Courier", 14)

# =====================================================================
# PHASE 3 INITIALIZATION: FLOATING INTERFACE VARIABLES
# =====================================================================
# Master visibility switch for the dashboard overlay (True = On Screen, False = Hidden)
show_dashboard = False  

# Core data settings for the 6 slider tracks [Current Value, Minimum Limit, Maximum Limit, Text Label]
sliders = {
    "solar_pump":   [0.001,  0.0001, 0.010,  "Solar Regrowth Pump"],
    "steering":     [7.1,    1.0,    15.0,   "Steering Sensitivity"],
    "baseline_tax": [0.05,   0.01,   0.20,   "Metabolic Burn Floor"],
    "ceiling_max":  [5.0,    1.0,    10.0,   "Fluid Density Ceiling"],
    "fission_gate": [0.9,   0.50,   1.00,   "FISSION THRESHOLD"],
    "entropy_clock":[8.0,    0.0,    20.0,   "Entropy Cascade Steps"]
}

# =====================================================================
# LAYER 2 ARCHITECTURE - PART 2: GENERAL ECOSYSTEM SETTINGS
# =====================================================================
# State Switch: 1 = Running Layer 1 Metropolis, 2 = Running Layer 2 Macro-Cosmos
active_simulation_layer = 1  

# The global laboratory container to hold your active macro-cells in memory
macro_population_pool = []

element_population_pool = []
# --- LAYER 3 VOLTAGE CAPACITOR AND TIMING MATRIX ---
layer3_timer_active = False    # Flips to True the exact millisecond the background pool hits 900V
incubation_energy = 0.0        # Dynamically accumulates dt floats during the countdown window
background_voltage_peak = 0.0  # Telemetry tracker to display current background voltage on your HUD

# Tracks which specific molecule your mouse cursor has selected for the microscope
selected_molecule_anchor = None
selected_atom_sub_anchor = None  # <--- DROP THIS EXACT LINE RIGHT HERE

# A secondary fluid matrix dedicated entirely to the Layer 2 macro-environment
# Running on your identical 800x600 grid to preserve scale-free fractal purity
macro_fluid_matrix = np.ones((WIDTH, HEIGHT), dtype=np.float32)

# HYDRODYNAMIC VECTOR ARRAYS: Initialize parallel 2D grids tracking fluid speed/direction
# Set entirely to 0.0 using your exact geography parameters so the puddles start at rest
macro_fluid_vx = np.zeros((WIDTH, HEIGHT), dtype=np.float32)
macro_fluid_vy = np.zeros((WIDTH, HEIGHT), dtype=np.float32)

# Keep a temporary flag to track if the user is actively dragging a slider knob
active_slider = None

# =====================================================================
# STEP 2: EXCAVATING THE NUMPY MATRIX LAYERS
# =====================================================================
fluid_matrix = np.ones((WIDTH, HEIGHT), dtype=np.float32)

# =====================================================================
# STEP 3: INITIALIZING THE FIRST GENERATION POPULATION POOL
# =====================================================================
raw_hardware_time = time.time()

nodes = [
    {
        "x": float((raw_hardware_time * 1000) % WIDTH),
        "y": float((raw_hardware_time * 555) % HEIGHT),
        "vx": float(math.cos(raw_hardware_time) * 130.0),
        "vy": float(math.sin(raw_hardware_time) * 130.0),
        "energy": 0.20,
        "surplus_ticks": 0,
        "flare_L": 0.0,
        "flare_R": 0.0
    },
    {
        "x": float((raw_hardware_time * 8888) % WIDTH),
        "y": float((raw_hardware_time * 333) % HEIGHT),
        "vx": float(math.sin(raw_hardware_time * 1.5) * 130.0),
        "vy": float(math.cos(raw_hardware_time * 1.5) * 130.0),
        "energy": 0.20,
        "surplus_ticks": 0,
        "flare_L": 0.0,
        "flare_R": 0.0
    }
]

# Fully Calibrated Physical System Constants
BASE_ENGINE_FORCE = 180.0
BASELINE_BURN = 0.1         
MOTION_BURN_SCALE = 0.02
MAX_NODE_POPULATION = 2000
audit_frame_counter = 0
# Controls how many times the fluid field diffuses per frame to anchor the CPU clock
DIFFUSION_STEPS = 8        

clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

                       # Unified Input Capture Layer (Processes clicks flawlessly before queue drain)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # --- LEFT-CLICK HOUSING ROUTER (BUTTON 1) ---
            if event.button == 1:
                # Layout metrics matching your original view box configuration on Page 32
                box_width = int(WIDTH * 0.25)
                box_height = int(HEIGHT * 0.25)
                box_x = WIDTH - box_width - 10
                box_y = 10
                
                # Check if the click landed directly inside the active microscope HUD box window
                if active_simulation_layer == 3 and selected_element_anchor and (box_x <= mouse_x <= box_x + box_width) and (box_y <= mouse_y <= box_y + box_height):
                    if selected_atom_sub_anchor is None:
                        # Compute click position relative to the top-left corner of the HUD box
                        box_click_x = mouse_x - box_x
                        box_click_y = mouse_y - box_y
                        
                        # Translate absolute box click back to global canvas scale seamlessly
                        target_mem_x = (box_click_x / box_width) * WIDTH
                        target_mem_y = (box_click_y / box_height) * HEIGHT
                        
                        # Deep-scan internal cells inside the macro hull to select the target atom
                        for atom in selected_element_anchor.atoms:
                            dist = math.sqrt((atom.x - target_mem_x)**2 + (atom.y - target_mem_y)**2)
                            if dist < atom.radius * 3.0: # Padding for comfortable click registration
                                selected_atom_sub_anchor = atom
                                break
                else:
                    # Click landed out in the open field: standard layer selections
                    if active_simulation_layer == 2:
                        for molecule in macro_population_pool:
                            dx_dist = mouse_x - molecule.x
                            dy_dist = mouse_y - molecule.y
                            dist = math.sqrt(dx_dist**2 + dy_dist**2)
                            if dist <= molecule.radius:
                                selected_molecule_anchor = molecule
                                break
                    elif active_simulation_layer == 3:
                        found_match = False
                        for element in element_population_pool:
                            dx_dist = mouse_x - element.x
                            dy_dist = mouse_y - element.y
                            dist = math.sqrt(dx_dist**2 + dy_dist**2)
                            if dist <= element.radius:
                                selected_element_anchor = element
                                selected_atom_sub_anchor = None # Reset deep zoom on focus switch
                                found_match = True
                                break
                        if not found_match:
                            selected_element_anchor = None
                            selected_atom_sub_anchor = None

            # --- RIGHT-CLICK ESCAPE ROUTER (BUTTON 3) ---
            elif event.button == 3:
                if selected_atom_sub_anchor is not None:
                    selected_atom_sub_anchor = None # Step out from Layer 1 nodes to Layer 2 cells
                elif selected_element_anchor is not None:
                    selected_element_anchor = None # Close microscope window completely

                # Unified Keystroke Monitor: All system triggers centralized on a single input node
                # Centralized Keystroke Node
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_time_lapse = not show_time_lapse
                # Instantly clear any old selection flags when toggling views to prevent frame lag
                if not show_time_lapse:
                    selected_molecule_anchor = None
                
            elif event.key == pygame.K_TAB:
                show_dashboard = not show_dashboard
                
            # LAYER 2 TRIGGER: Transition from Layer 1 to Layer 2 Space
            elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and active_simulation_layer == 1:
                active_simulation_layer = 2
                molecule_a = MacroMolecule(WIDTH * 0.35, HEIGHT * 0.50, fluid_matrix, nodes)
                molecule_b = MacroMolecule(WIDTH * 0.65, HEIGHT * 0.50, fluid_matrix, nodes)
                macro_population_pool.extend([molecule_a, molecule_b])
                selected_molecule_anchor = molecule_a
                
            # LAYER 3 TRIGGER: Transition from Layer 2 to Layer 3 Space
            elif (event.key == pygame.K_3 or event.key == pygame.K_KP3) and active_simulation_layer == 2:
                active_simulation_layer = 3
                
                # Native slicing creates independent internal atom trackers
                atoms_for_a = macro_population_pool[:]
                atoms_for_b = macro_population_pool[:]
                
                # Instantiate the elements with their live lists
                element_a = MacroElement(WIDTH * 0.35, HEIGHT * 0.50, macro_fluid_matrix, atoms_for_a)
                element_b = MacroElement(WIDTH * 0.65, HEIGHT * 0.50, macro_fluid_matrix, atoms_for_b)
                
                element_population_pool = [element_a, element_b]
                selected_element_anchor = element_a
                selected_molecule_anchor = None
                
                # Wipe the background macro-pool clean to preserve CPU load
                macro_population_pool = []

    # =================================================================
    # STEP 4: TRACK OVERLAP CONDUCTION PASS (NO TELEPATHIC CHEATS)
    # =================================================================
    num_nodes = len(nodes)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            dx_dist = nodes[i]["x"] - nodes[j]["x"]
            dy_dist = nodes[i]["y"] - nodes[j]["y"]
            dist_sq = (dx_dist ** 2) + (dy_dist ** 2) + 1e-5
           
            # Proximity check bounds their local tracking grid
            if dist_sq < 144.0:
                # 1. Find the coordinate matrix index directly halfway between them
                mid_x = int((nodes[i]["x"] + nodes[j]["x"]) * 0.5) % WIDTH
                mid_y = int((nodes[i]["y"] + nodes[j]["y"]) * 0.5) % HEIGHT
                mid_density = fluid_matrix[mid_x, mid_y]
                
                # 2. Check the insulation value of the terrain beneath their feet
                if mid_density > 0.10:
                    transfer_insulation = 0.01  # Thick terrain breaks the circuit
                else:
                    transfer_insulation = 1.0   # Black path forms an open copper wire
                
                # 3. Calculate the energy current scaled by the true path conduction
                energy_diff = nodes[i]["energy"] - nodes[j]["energy"]
                transfer_rate = 0.1 * math.tanh(1.0 / dist_sq) * transfer_insulation
                nodes[i]["energy"] -= energy_diff * transfer_rate
                nodes[j]["energy"] += energy_diff * transfer_rate

    # =================================================================
    # STEP 5: UN-TIMED ENERGY SATURATION RUPTURE GATE (NO CLOCK CHEATS)
    # =================================================================
    new_nodes = []
    # Lower your starting baseline threshold slightly to comfortably handle the 400-node metropolis
    DYNAMIC_FISSION_THRESHOLD = 0.99  
    
    for n in nodes:
        # The node ruptures strictly when its internal voltage hits saturation
        if n["energy"] >= DYNAMIC_FISSION_THRESHOLD:
            # Split the existing energy pool exactly 50/50 between the twins
            child_energy = n["energy"] * 0.5
            n["energy"] = child_energy
            
            # Spawn the physical twin at the exact same coordinate matrix point
            # Give it a slightly shifted vector heading based on local momentum
            angle = random.uniform(0, 2 * math.pi)
            speed = math.sqrt(n["vx"]**2 + n["vy"]**2) + 0.1
            
            child_node = {
                "x": n["x"],
                "y": n["y"],
                "vx": speed * math.cos(angle),
                "vy": speed * math.sin(angle),
                "energy": child_energy,
                "generation": n["generation"] + 1,
                "current_size": 2 # Keeps our fresh ledger telemetry operational
            }
            new_nodes.append(child_node)
            
    nodes.extend(new_nodes)


    # =================================================================
    # STEP 6: CORE PHYSICAL FILAMENT PROPULSION LOOP
    # =================================================================
    new_births = []  

    for n in nodes:
        n["x"] = n["x"] % WIDTH
        n["y"] = n["y"] % HEIGHT
        
        current_speed = math.sqrt(n["vx"]**2 + n["vy"]**2) + 1e-5
        dx = n["vx"] / current_speed
        dy = n["vy"] / current_speed
        
        lx, ly = -dy, dx
        rx, ry = dy, -dx
        
        sensor_dist = 3.5  
        nx_idx = int(n["x"] + dx * sensor_dist) % WIDTH
        ny_idx = int(n["y"] + dy * sensor_dist) % HEIGHT
        
        l_x = int(n["x"] + lx * 2.5) % WIDTH  
        l_y = int(n["y"] + ly * 2.5) % HEIGHT
        r_x = int(n["x"] + rx * 2.5) % WIDTH
        r_y = int(n["y"] + ry * 2.5) % HEIGHT
        
        front_pressure = fluid_matrix[nx_idx, ny_idx]
        left_pressure = fluid_matrix[l_x, l_y]
        right_pressure = fluid_matrix[r_x, r_y]
        
        # Shoulder Deflection Physics
        torque = left_pressure - right_pressure
        steering_sensitivity = 7.1   # Your locked-in sweet spot sensitivity
        n["vx"] += (lx * torque * steering_sensitivity * current_speed) * dt
        n["vy"] += (ly * torque * steering_sensitivity * current_speed) * dt
        
        n["flare_L"] = max(0.0, torque)   
        n["flare_R"] = max(0.0, -torque)  
        
        ix = max(0, min(WIDTH - 1, int(n["x"])))
        iy = max(0, min(HEIGHT - 1, int(n["y"])))
        local_density = fluid_matrix[ix, iy]
        
        consumed = local_density * 0.15
        n["energy"] += consumed * (1.0 - n["energy"])
        
         # === THE FRICTIONLESS ENERGY HIGHWAY METHOD ===
        burn_density_floor = max(0.05, local_density)
        
        # If sitting on a black path (0.01), motion friction is entirely deleted
        if local_density <= 0.015:
            actual_burn = (BASELINE_BURN * burn_density_floor) * dt
        else:
            actual_burn = ((BASELINE_BURN + (current_speed * MOTION_BURN_SCALE)) * burn_density_floor) * dt
            
        n["energy"] -= actual_burn
        n["energy"] = max(0.0, min(1.0, n["energy"]))

        
        # =============================================================
        # DERIVE THE DYNAMIC THERMODYNAMIC THRESHOLD (Perfect Names Aligned)
        # =============================================================
        engine_throttle = math.tanh(3.0 * n["energy"])
        drag_coefficient = 1.0 + (4.0 * front_pressure)
        
        dynamic_fission_threshold = (BASE_ENGINE_FORCE / (drag_coefficient * 450.0)) * local_density
        
        # Run the Biological Fission Gate with the organic dynamic parameter
        if n["energy"] >= dynamic_fission_threshold and len(nodes) + len(new_births) < MAX_NODE_POPULATION:
            n["surplus_ticks"] += 1
            if n["surplus_ticks"] >= 45:  
                n["surplus_ticks"] = 0
                n["energy"] *= 0.5        
                
                child = {
                    "x": n["x"],
                    "y": n["y"],
                    "vx": -n["vx"], 
                    "vy": -n["vy"],
                    "energy": n["energy"],
                    "surplus_ticks": 0,
                    "flare_L": 0.0,
                    "flare_R": 0.0,
                    "generation": n.get("generation", 0) + 1  # KICKS THE CALENDAR LIVE!                
                }
                new_births.append(child)
        else:
            n["surplus_ticks"] = max(0, n["surplus_ticks"] - 1)
            
        # Set Final Speeds using the variables calculated above
        new_speed = math.sqrt(n["vx"]**2 + n["vy"]**2) + 1e-5
        target_speed = (BASE_ENGINE_FORCE / drag_coefficient) * engine_throttle
        n["vx"] = (n["vx"] / new_speed) * target_speed
        n["vy"] = (n["vy"] / new_speed) * target_speed
        
        n["x"] += n["vx"] * dt
        n["y"] += n["vy"] * dt
        
        # =================================================================
        # RE-CALIBRATED KINETIC MASS DISPLACEMENT OPERATOR
        # =================================================================
        # Define the spatial coordinates of the 6-pixel wide plow zone
        x_start, x_end = max(0, ix-3), min(WIDTH, ix+3)
        y_start, y_end = max(0, iy-3), min(HEIGHT, iy+3)
        
        # 1. Calculate the Total Scooped Field Mass currently sitting in the lane
        total_scooped_mass = float(np.sum(fluid_matrix[x_start:x_end, y_start:y_end]))
        
        # 2. Forcefully clear the center lane down to a zero-resistance vacuum
        fluid_matrix[x_start:x_end, y_start:y_end] = 0.01
        
        # 3. Deduct the exact energy current absorbed by the node's internal battery
        # This prevents us from magically manufacturing matter out of thin air
        energy_flux_absorbed = consumed * dt
        remainder_mass = max(0.0, total_scooped_mass - energy_flux_absorbed)
        
        # 4. Use a 90-degree vector rotation to calculate perpendicular shoulder vectors
        # If forward is (vx, vy), Left is (-vy, vx) and Right is (vy, -vx)
        norm = math.sqrt(n["vx"]**2 + n["vy"]**2) + 1e-6
        lx, ly = -n["vy"] / norm, n["vx"] / norm  # Left shoulder unit vector
        rx, ry = n["vy"] / norm, -n["vx"] / norm   # Right shoulder unit vector
        
        # Calculate the exact pixel center offsets for the shoulder targets (5 pixels out)
        left_ix, left_iy = int(n["x"] + lx * 5), int(n["y"] + ly * 5)
        right_ix, right_iy = int(n["x"] + rx * 5), int(n["y"] + ry * 5)
        
        # Split the leftover mass exactly in half (50/50 allocation)
        displaced_shoulder_mass = remainder_mass * 0.5
        
        # 5. Stamp the mass onto the Left shoulder bank if it sits inside screen borders
        if 3 <= left_ix < WIDTH - 3 and 3 <= left_iy < HEIGHT - 3:
            fluid_matrix[left_ix-1:left_ix+2, left_iy-1:left_iy+2] += displaced_shoulder_mass / 9.0
            
        # 6. Stamp the mass onto the Right shoulder bank if it sits inside screen borders
        if 3 <= right_ix < WIDTH - 3 and 3 <= right_iy < HEIGHT - 3:
            fluid_matrix[right_ix-1:right_ix+2, right_iy-1:right_iy+2] += displaced_shoulder_mass / 9.0
            
        # Enforce a strict physical maximum ceiling so fluid density doesn't overflow to infinity
        fluid_matrix[fluid_matrix > 5.0] = 5.0


    nodes.extend(new_births)
    # Keep a minimum baseline community alive so Layer 1 never completely goes cold in the background
    if len(nodes) > 10:
        nodes = [n for n in nodes if n["energy"] > 0.02]

    # =================================================================
    # STEP 7: ORGANIC CONTINUOUS FLUID DISSIPATION CASCADE (TIME ANCHOR)
    # =================================================================
    # Instead of fake math, the CPU spends its heat diffusing your actual terrain
    for _ in range(DIFFUSION_STEPS):
        fluid_matrix = ndimage.gaussian_filter(fluid_matrix, sigma=0.15)

    # =================================================================
    # STEP 8: AUTOMATIC ENVIRONMENTAL REGROWTH (Recalibrated Scale)
    # =================================================================
    # 1. The Injection Flow: Slowly pump raw, concentrated density back 
    # into the entire grid from beneath to prevent permanent stagnation.
    fluid_matrix += 0.001 * dt
    
    # 2. Narrow the Blur Radius: Drop sigma to 0.30 so the fluid heals 
    # tightly from the borders inward, concentrating food right on the roads.
    fluid_matrix = ndimage.gaussian_filter(fluid_matrix, sigma=0.42)
    
    # Keep the environment strictly bounded between absolute zero and maximum jungle
    fluid_matrix = np.clip(fluid_matrix, 0.0, 1.0)


    # =================================================================
    # STEP 9: CLEAN GRAYSCALE-BLUE VEHICLE DISPLAY
    # =================================================================
    # Smashes density down to clean, beautiful charcoal mapping
    display_matrix = np.clip(fluid_matrix * 255, 0, 255).astype(np.uint8)
    
    # Beautiful, professional lab scheme: Dark charcoal void, deep black trails
    r_chan = (display_matrix // 5).astype(np.uint8)
    g_chan = (display_matrix // 3).astype(np.uint8)
    b_chan = (display_matrix // 2).astype(np.uint8)
    surface_array = np.stack([r_chan, g_chan, b_chan], axis=-1)
    
    # Render active vector telemetry lines and color-changing flares
    for n in nodes:
        nx, ny = int(n["x"]), int(n["y"])
        current_speed = math.sqrt(n["vx"]**2 + n["vy"]**2) + 1e-5
        dx = n["vx"] / current_speed
        dy = n["vy"] / current_speed
        
        if 4 <= nx < WIDTH-4 and 4 <= ny < HEIGHT-4:
            # 1. Paint the Node Body (Pure White Hot dot)            
            
            # === RESTORED ORIGINAL STATIC 4x4 NODE BODY ===
            x_min, x_max = max(0, nx - 2), min(WIDTH, nx + 2)
            y_min, y_max = max(0, ny - 2), min(HEIGHT, ny + 2)
            surface_array[x_min:x_max, y_min:y_max] = 255

            
            # 2. Draw the Laser Trajectory Arrow Line (Soft Green Laser heading)
            for step in range(2, 10):
                lx_pos = int(nx + dx * step)
                ly_pos = int(ny + dy * step)
                if 0 <= lx_pos < WIDTH and 0 <= ly_pos < HEIGHT:
                    surface_array[lx_pos, ly_pos] = [0, 255, 100]
            
            # 3. Left Shoulder Flare (Bright Yellow if slapped by a left wall)
            if n["flare_L"] > 0.01:
                sx = int(nx + (-dy) * 4.0)
                sy = int(ny + (dx) * 4.0)
                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                    surface_array[max(0, sx-2):min(WIDTH, sx+2), max(0, sy-2):min(HEIGHT, sy+2)] = [255, 220, 0]
                    
            # 4. Right Shoulder Flare (Bright Red if slapped by a right wall)
            if n["flare_R"] > 0.01:
                sx = int(nx + (dy) * 4.0)
                sy = int(ny + (-dx) * 4.0)
                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                    surface_array[max(0, sx-2):min(WIDTH, sx+2), max(0, sy-2):min(HEIGHT, sy+2)] = [255, 50, 50]
                    
    # =====================================================================
    # LAYER 2 ARCHITECTURE - PART 4: THE UNIFIED MACRO-COSMOS RENDERER
    # =====================================================================          
      # --- MASTER DISPLAY ROUTER ---
    if active_simulation_layer == 1:
        # --- RUN PRISTINE LAYER 1 GRAPHICS ---
        pygame.surfarray.blit_array(screen, surface_array)
        pop_txt = FONT.render(f"ACTIVE FILAMENTS (POP): {len(nodes)} / {MAX_NODE_POPULATION}", True, (255, 255, 255))
        screen.blit(pop_txt, (20, 20))
       
    elif active_simulation_layer == 2 or active_simulation_layer == 3:
                # --- GLOBAL HYDRODYNAMIC VECTOR PROCESSING PASS ---
        # 1. VISCOUS DISSIPATION: Apply a 4% decay tax so fluid current friction settles naturally over time
        macro_fluid_vx -= (macro_fluid_vx * 0.04) * dt
        macro_fluid_vy -= (macro_fluid_vy * 0.04) * dt
        
        # 2. ADVECTION BLUR CASCADE: Let velocity waves bleed smoothly into neighboring grid squares
        macro_fluid_vx = ndimage.gaussian_filter(macro_fluid_vx, sigma=0.25)
        macro_fluid_vy = ndimage.gaussian_filter(macro_fluid_vy, sigma=0.25)

        # --- RUN VECTOR-DRIVEN LAYER 2 MACRO-COSMOS ---
       
        # STEP 7 REPLICATION: MACRO-FIELD CONTINUOUS DISSIPATION CASCADE
        # Routes the environmental clock directly through the selected molecule's private slider folder
        ui_target = selected_molecule_anchor if selected_molecule_anchor else (macro_population_pool if macro_population_pool else None)
        has_sliders = ui_target is not None and hasattr(ui_target, 'sliders')
        if has_sliders:
            entropy_val = ui_target.sliders["entropy_clock"]
            entropy_steps = int(entropy_val) if isinstance(entropy_val, list) else int(entropy_val)
        else:
            entropy_steps = int(sliders["entropy_clock"][0])
       
        for _ in range(entropy_steps):
            macro_fluid_matrix = ndimage.gaussian_filter(macro_fluid_matrix, sigma=0.15)

        # HIGH CONTRAST FLUID ENGINE RENDERER: Kills the black screen permanently
        macro_surface_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
        blue_map = np.clip((macro_fluid_matrix - 1.0) * 180.0, 0, 255).astype(np.uint8)
        macro_surface_array[..., 0] = blue_map // 6   # Deep indigo/velvet background void
        macro_surface_array[..., 1] = blue_map // 3   # Teal trails
        macro_surface_array[..., 2] = blue_map        # Sharp neon blue fluid walls
        pygame.surfarray.blit_array(screen, macro_surface_array)

 # AUTOMATED THERMODYNAMIC VENT: Bubbles two fresh atoms when Layer 1 reaches 600 nodes
                # --- POTENTIAL FIELD AUTOMATED VENT GATE ---
        # Sums up the live energetic voltage of the community rather than a rigid head count
        _total_l1_volts = sum(float(n["energy"]) for n in nodes)
        
        if _total_l1_volts >= 20.0:

            # Establish the two target spawn center coordinates on the canvas
            _ax, _ay = WIDTH * 0.35, HEIGHT * 0.50
            _bx, _by = WIDTH * 0.65, HEIGHT * 0.50
            
            # Mint the two twin vessels handing each a full fluid copy and the current nodes list
            molecule_a = MacroMolecule(_ax, _ay, fluid_matrix, nodes)
            molecule_b = MacroMolecule(_bx, _by, fluid_matrix, nodes)
            
            # Inject them into the active running simulation pool
            macro_population_pool.extend([molecule_a, molecule_b])
            
            # Set default selection anchor if none exists
            if not selected_molecule_anchor:
                selected_molecule_anchor = molecule_a
       
        # --- MILESTONE 1 REAL-WORLD BUMPER CONSTRAINT PASS ---
        # Enforces physical, impassable barriers across your seamless torus grid edges
        num_mols = len(macro_population_pool)
        for i in range(num_mols):
            for j in range(i + 1, num_mols):
                mol_a = macro_population_pool[i]
                mol_b = macro_population_pool[j]
               
                dx = mol_b.x - mol_a.x
                dy = mol_b.y - mol_a.y
                if dx > WIDTH * 0.5: dx -= WIDTH
                elif dx < -WIDTH * 0.5: dx += WIDTH
                if dy > HEIGHT * 0.5: dy -= HEIGHT
                elif dy < -HEIGHT * 0.5: dy += HEIGHT
               
                dist = math.sqrt(dx**2 + dy**2 + 1e-5)
                min_dist = mol_a.radius + mol_b.radius
               
                if dist < min_dist:
                    overlap = min_dist - dist
                    push_x = (dx / dist) * overlap * 0.5
                    push_y = (dy / dist) * overlap * 0.5
                   
                    mol_a.x -= push_x
                    mol_a.y -= push_y
                    mol_b.x += push_x
                    mol_b.y += push_y
                   
                    # Elastic momentum velocity snap
                    mol_a.vx, mol_b.vx = mol_b.vx * 0.8, mol_a.vx * 0.8
                    mol_a.vy, mol_b.vy = mol_b.vy * 0.8, mol_a.vy * 0.8

 # --- INDIVIDUAL CELL PROCESSING PIPELINE ---
            # --- INDIVIDUAL CELL PROCESSING PIPELINE ---
    if active_simulation_layer == 2:
        for molecule in macro_population_pool:

            # Safely hook private instance memory sliders folder instantly at header
            if not hasattr(molecule, 'sliders'):
                molecule.sliders = {k: float(v[0]) if isinstance(v, list) else float(v) for k, v in sliders.items()}
           
            # IGNITE THE INTERNAL CLOCKS: Forces cell's inner layer to live and herd in background RAM
            for mn in molecule.nodes:
                mn["x"] += mn["vx"] * dt
                mn["y"] += mn["vy"] * dt
                mn["x"] = mn["x"] % WIDTH
                mn["y"] = mn["y"] % HEIGHT
                
                # --- FILAMENT CURRENT VECTOR PASS ---
                # 1. Map the exact integer grid coordinates directly beneath this sub-node
                _n_ix = max(0, min(WIDTH - 1, int(mn["x"])))
                _n_iy = max(0, min(HEIGHT - 1, int(mn["y"])))
                
                # 2. Let the fluid's live current vectors forcefully push and bend the node's heading
                # This organically translates the fluid's rotation straight down into the filaments
                mn["vx"] += macro_fluid_vx[_n_ix, _n_iy] * 0.25 * dt
                mn["vy"] += macro_fluid_vy[_n_ix, _n_iy] * 0.25 * dt

            # BASAL METABOLIC STRUCTURAL LEAK: Stretched dt from hardware lag drains internal batteries
                mn["energy"] -= 0.001 * dt
                    # FLUID METABOLIC INTAKE: Internal nodes organically drink the solar fluid they are plowing through
                mn["energy"] += 0.00099 * macro_fluid_matrix[ix, iy] * dt
           
            # THE RE-PROPORTIONED VECTOR DRIVE: Tuned to give heavy, graceful, floating inertia
            if len(molecule.nodes) > 0:
                raw_sum_vx = sum(mn["vx"] for mn in molecule.nodes)
                raw_sum_vy = sum(mn["vy"] for mn in molecule.nodes)
                
                # NATURALLY PROPORTIONED SPEED GEAR: Adjusted ratio prevents manic missile speeds
                speed_scale = float(molecule.sliders["solar_pump"]) if not isinstance(molecule.sliders["solar_pump"], list) else float(molecule.sliders["solar_pump"])
                momentum_scale = 0.00002 * (speed_scale / 0.001)
                
                molecule.vx = raw_sum_vx * momentum_scale
                molecule.vy = raw_sum_vy * momentum_scale
            else:
                molecule.vx = 0.0
                molecule.vy = 0.0
           
            # --- LIVE MACRO-SHOULDER TORQUE STEERING ---
            heading_angle = math.atan2(molecule.vy, molecule.vx + 1e-5)
            sensor_dist = molecule.radius + 12.0
           
            left_sx = int(molecule.x + math.cos(heading_angle - 0.5) * sensor_dist) % WIDTH
            left_sy = int(molecule.y + math.sin(heading_angle - 0.5) * sensor_dist) % HEIGHT
            right_sx = int(molecule.x + math.cos(heading_angle + 0.4) * sensor_dist) % WIDTH
            right_sy = int(molecule.y + math.sin(heading_angle + 0.4) * sensor_dist) % HEIGHT
           
            left_density = macro_fluid_matrix[left_sx, left_sy]
            right_density = macro_fluid_matrix[right_sx, right_sy]
           
            steer_val = molecule.sliders["steering"]
            steering_strength = float(steer_val[0]) if isinstance(steer_val, list) else float(steer_val)
            
            if right_density > left_density:
                molecule.vx -= (right_density - left_density) * steering_strength * 0.1
            elif left_density > right_density:
                molecule.vx += (left_density - right_density) * steering_strength * 0.1

            # --- ATOM-SCALE VOLTAGE KINETIC PROPULSION ---
            # 1. Sum up the live internal energy voltages of this specific atom's sub-nodes
            _atom_volts = sum(float(mn["energy"]) for mn in molecule.nodes)
            
            # 2. Bracket negative starvation values to guarantee a safe math domain
            _safe_atom_volts = max(0.0, _atom_volts)
            atom_speed_boost = math.log1p(_safe_atom_volts) * 0.05
            
            # 3. Apply the potential-to-kinetic scalar directly to the position steps
            molecule.x += (molecule.vx * atom_speed_boost) * dt
            molecule.y += (molecule.vy * atom_speed_boost) * dt

            # SEAMLESS 3D TORUS BOUNDARY COUPLING
            if molecule.x < -molecule.radius: molecule.x = WIDTH + molecule.radius
            elif molecule.x > WIDTH + molecule.radius: molecule.x = -molecule.radius
            if molecule.y < -molecule.radius: molecule.y = HEIGHT + molecule.radius
            elif molecule.y > HEIGHT + molecule.radius: molecule.y = -molecule.radius

            # Capture old velocities to calculate precise external drag forces
            old_vx, old_vy = molecule.vx, molecule.vy
           
            # EXECUTE THE MACRO-PLOW ENGINE: Fixed to route private local molecule sliders
            molecule.update_macro_physics_and_plow(macro_fluid_matrix, dt, molecule.sliders)
            
            # --- HYDRODYNAMIC KINETIC STIRRING PASS ---
            # 1. Map the exact integer pixel coordinate beneath the atom core
            _fx_idx = max(0, min(WIDTH - 1, int(molecule.x)))
            _fy_idx = max(0, min(HEIGHT - 1, int(molecule.y)))
            
            # 2. Transfer a percentage of the atom's current velocity into the fluid grid
            # This creates a moving localized current wake directly behind the cruising body
            macro_fluid_vx[_fx_idx, _fy_idx] += molecule.vx * 0.15 * dt
            macro_fluid_vy[_fx_idx, _fy_idx] += molecule.vy * 0.15 * dt
            
             # Force high-powered manual fluid plowing directly onto the master macro grid
            px = int(molecule.x + math.cos(heading_angle) * molecule.radius) % WIDTH
            py = int(molecule.y + math.sin(heading_angle) * molecule.radius) % HEIGHT
            macro_fluid_matrix[px, py] = min(8.0, macro_fluid_matrix[px, py] + 1.2)
           
            tx = int(molecule.x - math.cos(heading_angle) * molecule.radius) % WIDTH
            ty = int(molecule.y - math.sin(heading_angle) * molecule.radius) % HEIGHT
            macro_fluid_matrix[tx, ty] = max(0.001, macro_fluid_matrix[tx, ty] - 0.6)
           
            # CALCULATE THE EXTERNAL PERTURBATION FORCE
            impact_vx = molecule.vx - old_vx
            impact_vy = molecule.vy - old_vy
           
            # THE 10% THERMODYNAMIC TRICKLE-DOWN FIELDS
            trickle_factor = 0.10
            for mn in molecule.nodes:
                mn["vx"] += impact_vx * trickle_factor
                mn["vy"] += impact_vy * trickle_factor
                            # --- GLOBAL ATOMIC PURGE ENGINE (UNCOUPLED FROM LAYER SEPARATION) ---
            # Calculates the total combined voltage of the atom. If it hits zero, it dissolves cleanly.
            surviving_atoms_pool = []
            for purge_mol in macro_population_pool:
                # First, drop any individual internal sub-nodes that have completely starved
                purge_mol.nodes = [mn for mn in purge_mol.nodes if mn["energy"] > 0.01]
                
                # Calculate the true overall macro-battery voltage of the entire cell hull
                if len(purge_mol.nodes) > 0:
                    _total_atom_charge = sum(float(mn["energy"]) for mn in purge_mol.nodes)
                    # Strict 0.05 thermodynamic survival boundary (Matches your Layer 3 rule)
                    if _total_atom_charge > 25.00:
                        surviving_atoms_pool.append(purge_mol)
                        
            # Update the master background container with only living, energized cells
            macro_population_pool = surviving_atoms_pool
           
            # Render boundaries and highlights
            is_selected = (molecule == selected_molecule_anchor)
            border_color = (0, 255, 100) if is_selected else (255, 255, 255)
            border_thickness = 2 if is_selected else 1

            # --- REAL-TIME HIGH-CONTRAST CONTINUOUS MICROSCOPE CAMERA LENS ---
            if molecule == selected_molecule_anchor and show_time_lapse:
                # 1. Clear viewport baseline first before drawing updates
                molecule.mini_map_surface.fill((10, 12, 15))
               
                # 2. Fetch live-updating internal fluid matrix (explicitly private to this cell)
                small_grid = molecule.fluid_matrix[::4, ::4]
                color_map = np.clip((small_grid - 1.0) * 180.0, 0, 255).astype(np.uint8)
               
                # 3. Blit the internal glowing fluid maps smoothly
                rgb_array = np.zeros((200, 150, 3), dtype=np.uint8)
                rgb_array[..., 0] = color_map // 6
                rgb_array[..., 1] = color_map // 3
                rgb_array[..., 2] = color_map
                surf = pygame.surfarray.make_surface(rgb_array)
                molecule.mini_map_surface.blit(pygame.transform.scale(surf, (200, 150)), (0, 0))
               
                # 4. Render the live white filament nodes swimming in real-time memory!
                for mn in molecule.nodes:
                    micro_x = int(mn["x"] * 0.25)
                    micro_y = int(mn["y"] * 0.25)
                    pygame.draw.circle(molecule.mini_map_surface, (255, 255, 255), (micro_x, micro_y), 1)

            # Enforce whole integers so Pygame draw doesn't quietly fail
            pygame.draw.circle(screen, border_color, (int(molecule.x), int(molecule.y)), int(molecule.radius), border_thickness)
           
                # Print your clean, professional Layer 2 Laboratory HUD data
        layer2_txt = FONT.render("MACRO-COSMOS LAYER 2 ACTIVE | SYSTEM STABLE", True, (255, 255, 255))
        screen.blit(layer2_txt, (20, 20))
        
        # NEW: LIVE POTENTIAL FIELD TELEMETRY (MATCHES YOUR LAYER 3 SYSTEM BLUEPRINT)
        # Deep-scans the entire active canvas to sum up Layer 1 voltage and display the target gate live
        _l2_hud_l1_volts = sum(float(n["energy"]) for n in nodes)
        l1_volt_txt = FONT.render(f"LAYER 1 VENT FACTORY RECHARGING: {_l2_hud_l1_volts:.2f}V / 70.00V", True, (100, 100, 150))
        screen.blit(l1_volt_txt, (20, 40))
        
        if selected_molecule_anchor:
            # Dynamically recalculate the private node count every single frame tick
            live_nodes_count = len(selected_molecule_anchor.nodes)
            sel_txt = FONT.render(f"SELECTED MOLECULE INTERNAL POP: {live_nodes_count} FILAMENTS", True, (0, 255, 100))
            screen.blit(sel_txt, (20, 60))
           
            # Dynamically sum up the true active internal battery voltages live from memory
            live_macro_battery = sum(float(mn["energy"]) for mn in selected_molecule_anchor.nodes)
            bat_txt = FONT.render(f"SELECTED MOLECULE MACRO-BATTERY: {live_macro_battery:.2f} VOLTS", True, (0, 255, 100))
            screen.blit(bat_txt, (20, 80))
    elif active_simulation_layer == 3:
                # --- INSULATED BACKGROUND FACTORY COMPUTATION LAYER ---
        # Ticks the clocks for the background atoms silently without letting UI code bleed
        for bg_molecule in macro_population_pool:
            # 1. Ignite the internal filament clocks (Mirrored from your native Page 18 loop)
            for mn in bg_molecule.nodes:
                mn["x"] += mn["vx"] * dt
                mn["y"] += mn["vy"] * dt
                mn["x"] = mn["x"] % WIDTH
                mn["y"] = mn["y"] % HEIGHT
                
                # Basal metabolic structural leak
                mn["energy"] -= 0.002 * dt
                
                # Fluid metabolic intake from the background matrix coordinate map
                bg_ix = max(0, min(WIDTH - 1, int(bg_molecule.x)))
                bg_iy = max(0, min(HEIGHT - 1, int(bg_molecule.y)))
                mn["energy"] += 0.00195 * macro_fluid_matrix[bg_ix, bg_iy] * dt
                
            # 2. Recalculate background atom vector drive to update position metrics
            if len(bg_molecule.nodes) > 0:
                raw_sum_vx = sum(mn["vx"] for mn in bg_molecule.nodes)
                raw_sum_vy = sum(mn["vy"] for mn in bg_molecule.nodes)
                momentum_scale = 0.00002
                bg_molecule.vx = raw_sum_vx * momentum_scale
                bg_molecule.vy = raw_sum_vy * momentum_scale
            else:
                bg_molecule.vx = 0.0
                bg_molecule.vy = 0.0
                
            # 3. Update background atom coordinates across the screen glass
            bg_molecule.x += bg_molecule.vx * dt
            bg_molecule.y += bg_molecule.vy * dt
            
            # Torus bounds check for the background floating bodies
            if bg_molecule.x < -bg_molecule.radius: bg_molecule.x = WIDTH + bg_molecule.radius
            elif bg_molecule.x > WIDTH + bg_molecule.radius: bg_molecule.x = -bg_molecule.radius
            if bg_molecule.y < -bg_molecule.radius: bg_molecule.y = HEIGHT + bg_molecule.radius
            elif bg_molecule.y > HEIGHT + bg_molecule.radius: bg_molecule.y = -bg_molecule.radius

                # --- BACKGROUND AUTONOMOUS LAYER 3 LIFE CYCLE ENGINE ---
        # 1. Continuous deep-scan telemetry of the new background atom pool
        background_voltage_peak = 0.0
        for bg_atom in macro_population_pool:
            if hasattr(bg_atom, 'nodes'):
                background_voltage_peak += sum(float(node["energy"]) for node in bg_atom.nodes)
                
                # 2. Check capacitor threshold to initiate the dynamic diversification window
        if background_voltage_peak >= 450.0 and not layer3_timer_active:
            layer3_timer_active = True
            incubation_energy = 0.0  # Clear old ageing data to start incubation fresh
            
        # 3. Process time dilation countdown based entirely on frame calculation rates
        if layer3_timer_active:
            # The lag itself directly accelerates the countdown rate by adding raw dt components
            incubation_energy += 2.0 * dt
            
            if incubation_energy >= 10.0:
                # The incubation window has aged out. Use your native slicing to isolate the organic atoms.
                atoms_for_new_a = macro_population_pool[:]
                atoms_for_new_b = macro_population_pool[:]
                
                # Birth the new twin elements at the default starting coordinates
                new_element_a = MacroElement(WIDTH * 0.35, HEIGHT * 0.50, macro_fluid_matrix, atoms_for_new_a)
                new_element_b = MacroElement(WIDTH * 0.65, HEIGHT * 0.50, macro_fluid_matrix, atoms_for_new_b)
                
                # Append them to your expanding population pool (Supports 2, 20, or 30+ elements smoothly)
                element_population_pool.extend([new_element_a, new_element_b])
                
                # RESET THE CYCLE ENGINE: Wipe the background clean to vent CPU load
                macro_population_pool = []
                layer3_timer_active = False
                layer3_trigger_time = 0

    # --- RUN FRONTAL ELEMENT HULL LAYER 3 ---
    # 1. Clear the screen with your deep charcoal void
        screen.fill((10, 12, 15))
        
        # 2. Loop through your dedicated element pool container
        for element in element_population_pool:
            is_selected = (element == selected_element_anchor)
            border_color = (0, 255, 100) if is_selected else (255, 255, 255)
            border_thickness = 2 if is_selected else 1
            
            # Draw the element hull onto the canvas
            pygame.draw.circle(screen, border_color, (int(element.x), int(element.y)), int(element.radius), border_thickness)
            
        # 3. Print your high-contrast HUD panel data
        layer3_txt = FONT.render("ELEMENT SCALE LAYER 3 ACTIVE | LIVE MOVEMENT CHANNELS", True, (255, 255, 255))
        screen.blit(layer3_txt, (20, 20))
        # Display the live charging status of your background atom factory
        bg_volt_txt = FONT.render(f"BACKGROUND FACTORY RECHARGING: {background_voltage_peak:.2f}V / 450.00V", True, (100, 100, 150))
        screen.blit(bg_volt_txt, (20, 80))
        
        if layer3_timer_active:
            # Graphically count down how much structural window remains before the early cutoff
            remaining_age = max(0.0, 10.0 - incubation_energy)
            timer_txt = FONT.render(f"INCUBATION AGE WINDOW CLOSING: {remaining_age:.2f}s", True, (255, 100, 100))
            screen.blit(timer_txt, (20, 100))
        
        if selected_element_anchor:
            # 1. Display the live count of atoms trapped inside the Element
            live_atoms_count = len(selected_element_anchor.atoms)
            elem_txt = FONT.render(f"SELECTED ELEMENT INTERNAL ATOMS: {live_atoms_count} MOLECULES", True, (0, 255, 100))
            screen.blit(elem_txt, (20, 40))
            
            # 2. Deep-scan all internal atoms and sum up their node voltages live from memory
            # This replicates your exact multi-layered thermodynamic tracking layout
            total_element_volts = 0.0
            for atom in selected_element_anchor.atoms:
                if hasattr(atom, 'nodes'):
                    total_element_volts += sum(float(node["energy"]) for node in atom.nodes)
            
            # 3. Print the live total accumulated voltage to your lab monitor panel
            bat_txt = FONT.render(f"SELECTED ELEMENT MACRO-BATTERY: {total_element_volts:.2f} VOLTS", True, (0, 255, 100))
            screen.blit(bat_txt, (20, 60))
            
                   # 4. --- LIVE TRIPLE-TIER BIOLOGICAL ENGINE ---
        # Activates Layer 1 and Layer 2 physics calculations directly inside your Element pool
        for element in element_population_pool:
            # Gather the total active energy voltage inside the hull to calculate the logarithmic kinetic boost
            _total_element_volts = sum(sum(float(n["energy"]) for n in a.nodes) for a in element.atoms if hasattr(a, 'nodes'))
            speed_boost = math.log1p(max(0.0, _total_element_volts)) * 0.05
            
            # Compute the absolute spatial coordinate steps for this frame pass
            step_x = (element.vx * speed_boost) * dt
            step_y = (element.vy * speed_boost) * dt
            
            # Apply the steps and enforce strict seamless torus wrapping on the macro hull coordinates
            element.x = (element.x + step_x) % WIDTH
            element.y = (element.y + step_y) % HEIGHT
            
            surviving_internal_cells = []
            for atom in element.atoms:
                if hasattr(atom, 'nodes') and len(atom.nodes) > 0:
                    # UNIFIED CELLULAR LOCOMOTION: Anchor internal cells to the element hull step
                    atom.x = (atom.x + step_x) % WIDTH
                    atom.y = (atom.y + step_y) % HEIGHT
                    
                                        # --- UNLOCKED INTERNAL LAYER 1 NODE LIFECYCLES ---
                    surviving_nodes = []
                    new_node_births = []
                    
                                        # --- CROWDING-AWARE INTERNAL LAYER 1 NODE LIFECYCLES ---
                    # Option A: Scales cost of living smoothly based on macro element atom density
                    crowding_factor = 1.0 + (len(element.atoms) * 0.001)
                    
                    for node in atom.nodes:
                        node["x"] = (node["x"] + node["vx"] * dt) % WIDTH
                        node["y"] = (node["y"] + node["vy"] * dt) % HEIGHT
                        
                        # Apply the dynamic crowding factor straight to your basal metabolic tax row
                        node["energy"] -= (0.001 * crowding_factor) * dt
                        
                        n_ix = max(0, min(WIDTH - 1, int(node["x"])))
                        n_iy = max(0, min(HEIGHT - 1, int(node["y"])))
                        node["energy"] += 0.0055 * macro_fluid_matrix[n_ix, n_iy] * dt
                        node["energy"] = max(0.0, min(1.0, node["energy"]))
                        
                        # 3. LIVE FISSION PASS: Split the node pool 50/50 if individual voltage saturates
                        if node["energy"] >= 0.95:
                            node["energy"] *= 0.5
                            angle = random.uniform(0, 2 * math.pi)
                            speed = math.sqrt(node["vx"]**2 + node["vy"]**2) + 0.1
                            child_node = {
                                "x": node["x"], "y": node["y"],
                                "vx": speed * math.cos(angle), "vy": speed * math.sin(angle),
                                "energy": node["energy"], "generation": node.get("generation", 0) + 1,
                                "flare_L": 0.0, "flare_R": 0.0, "surplus_ticks": 0
                            }
                            new_node_births.append(child_node)
                        
                        # 4. MICRO STARVATION FLOOR: Keep the node only if it holds basic charge
                        if node["energy"] > 0.01:
                            surviving_nodes.append(node)
                            
                    # Merge survivors and newborn node divisions back into the atom's matrix
                    surviving_nodes.extend(new_node_births)
                    atom.nodes = surviving_nodes
                        
                    # --- LIVE ATOM-SCALE THERMODYNAMIC CHECK ---
                    _atom_aggregate_volts = sum(float(n["energy"]) for n in atom.nodes)
                    if _atom_aggregate_volts > 10.00:
                        # --- PROVEN MICRO-TO-MACRO DRIVE COUPLING (PAGE 18/19) ---
                        raw_sum_vx = sum(n["vx"] for n in atom.nodes)
                        raw_sum_vy = sum(n["vy"] for n in atom.nodes)
                        atom.vx = raw_sum_vx * 0.0001
                        atom.vy = raw_sum_vy * 0.0001
                        
                        # --- NEW: PROVEN FLUID MEDIUM DRAG RESISTANCE (PAGE 3) ---
                        # Internal atoms now feel physical resistance from the fluid they occupy
                        a_ix = max(0, min(WIDTH - 1, int(atom.x)))
                        a_iy = max(0, min(HEIGHT - 1, int(atom.y)))
                        _local_atom_density = macro_fluid_matrix[a_ix, a_iy]
                        _atom_drag = 1.0 + (1.0 * _local_atom_density)
                        atom.vx -= (atom.vx * 0.01 * _atom_drag) * dt
                        atom.vy -= (atom.vy * 0.01 * _atom_drag) * dt
                        
                        surviving_internal_cells.append(atom)
                        
            element.atoms = surviving_internal_cells

            # --- NEW: INTERNAL CELL-TO-CELL BUMPER CONSTRAINTS (PAGE 17/18) ---
            # Enforces hard physical boundaries between atoms inside the macro hull
            # This generates localized kinetic impact shocks to drive bottom-up cascades
            num_internal_atoms = len(element.atoms)
            for i in range(num_internal_atoms):
                for j in range(i + 1, num_internal_atoms):
                    batom_a = element.atoms[i]
                    batom_b = element.atoms[j]
                    
                    # Torus-aware geometric vector deltas
                    bdx = batom_b.x - batom_a.x
                    bdy = batom_b.y - batom_a.y
                    if bdx > WIDTH * 0.5: bdx -= WIDTH
                    elif bdx < -WIDTH * 0.5: bdx += WIDTH
                    if bdy > HEIGHT * 0.5: bdy -= HEIGHT
                    elif bdy < -HEIGHT * 0.5: bdy += HEIGHT
                    
                    b_dist = math.sqrt(bdx**2 + bdy**2 + 1e-5)
                    b_min_dist = batom_a.radius + batom_b.radius
                    
                    if b_dist < b_min_dist:
                        # 1. Spatial separation push back
                        b_overlap = b_min_dist - b_dist
                        b_push_x = (bdx / b_dist) * b_overlap * 0.5
                        b_push_y = (bdy / b_dist) * b_overlap * 0.5
                        batom_a.x -= b_push_x
                        batom_a.y -= b_push_y
                        batom_b.x += b_push_x
                        batom_b.y += b_push_y
                        
                        # 2. Elastic rebound momentum transfer
                        batom_a.vx, batom_b.vx = batom_b.vx * 0.8, batom_a.vx * 0.8
                        batom_a.vy, batom_b.vy = batom_b.vy * 0.8, batom_a.vy * 0.8

            
            # --- PROVEN LAYER 2 TO LAYER 3 INERTIAL TRANSFER ---
            # Recalculates the element's master velocity vectors straight from its live internal atom pool sums
            if len(element.atoms) > 0:
                raw_elem_vx = sum(a.vx for a in element.atoms)
                raw_elem_vy = sum(a.vy for a in element.atoms)
                element.vx = raw_elem_vx * 0.03
                element.vy = raw_elem_vy * 0.03
                
                # Execute your native sensor steering, shoulder torque, and drag resistance calculations
                element.calculate_element_locomotion()
            else:
                element.vx = 0.0
                element.vy = 0.0
            
            # --- MACRO ELEMENT CELLULAR MITOSIS (RECOVERY REPLICATION) ---
            # 1. Sum up the live remaining aggregate voltage inside this specific macro hull
            _current_element_charge = 0.0
            for atom in element.atoms:
                if hasattr(atom, 'nodes'):
                    _current_element_charge += sum(float(node["energy"]) for node in atom.nodes)
                    
                    # --- PHYSICAL CEILING MITOSIS PASS ---
        # Removed the artificial population cap entirely. 
        # Elements are free to split indefinitely, bound strictly by localized nutrient limits.
            if _current_element_charge >= 500.0:

                # Check the global background pool or master list structure to clone the template nodes
                # We fetch a fresh deep copy of the starting template list configuration
                if len(nodes) > 0:
                    mitosis_nodes_blueprint = [dict(nodes[0])]
                    # Recharge the new twin's starting sub-node to full potential capacity
                    for mn in mitosis_nodes_blueprint:
                        mn["energy"] = 1.0
                        
                    # 3. Spend a tiny metabolic fee from the existing cell battery to fund the birth
                    for atom in element.atoms:
                        if hasattr(atom, 'nodes'):
                            for node in atom.nodes:
                                node["energy"] -= 0.002
                                
                    # 4. Materialize the new cell natively inside the element hull's tracking list
                    new_cellular_twin = MacroMolecule(element.x, element.y, element.macro_fluid_matrix, mitosis_nodes_blueprint)
                    element.atoms.append(new_cellular_twin)
            
            # Calculate heading vector angle to determine plow orientation
            heading_angle = math.atan2(element.vy, element.vx + 1e-5)
            
            # EXECUTE THE MACRO-PLOW ENGINE (Identical to Page 19 logic)
            px = int(element.x + math.cos(heading_angle) * element.radius) % WIDTH
            py = int(element.y + math.sin(heading_angle) * element.radius) % HEIGHT
            macro_fluid_matrix[px, py] = min(8.0, macro_fluid_matrix[px, py] + 0.6)
            
            tx = int(element.x - math.cos(heading_angle) * element.radius) % WIDTH
            ty = int(element.y - math.sin(heading_angle) * element.radius) % HEIGHT
            macro_fluid_matrix[tx, ty] = max(0.001, macro_fluid_matrix[tx, ty] - 0.3)
            
                    # --- VOLTAGE-DRIVEN KINETIC PROPULSION PASS ---
            # 1. Gather the live aggregate voltage of all internal nodes inside this macro hull
            _total_element_volts = 0.0
            for atom in element.atoms:
                if hasattr(atom, 'nodes'):
                    _total_element_volts += sum(float(node["energy"]) for node in atom.nodes)
                    
            # 2. Compute your logarithmic speed booster factor to handle high-voltage scaling safely
            # Protects the math domain by clamping negative starving voltages safely at 0.0
            safe_volts = max(0.0, _total_element_volts)
            speed_boost = math.log1p(safe_volts) * 0.05
            
                    # 3. Cache the element's raw pre-movement velocities to capture external forces
            if not hasattr(element, 'old_vx'):
                element.old_vx, element.old_vy = element.vx, element.vy
                
            # 4. Apply the dynamic potential-to-kinetic multiplier directly to your positional steps
            element.x += (element.vx * speed_boost) * dt
            element.y += (element.vy * speed_boost) * dt
            
            # --- PROVEN TOP-DOWN PERTURBATION CASCADE BLOCK (MIRRORED FROM PAGE 20) ---
            # Computes the net velocity change of the macro hull due to drag, bumps, and thrust
            impact_vx = element.vx - element.old_vx
            impact_vy = element.vy - element.old_vy
            
            # Trickle exactly 10% of that kinetic shockwave down to all hosted internal cells
            trickle_factor = 0.03
            for atom in element.atoms:
                atom.vx += impact_vx * trickle_factor
                atom.vy += impact_vy * trickle_factor
                
            # Cache current velocities for the next frame physics tick
            element.old_vx, element.old_vy = element.vx, element.vy

        # --- THE L3 THERMODYNAMIC RECYCLING PIPELINE ---
        # Scans elements to filter out dead hulls and process nutrient returns
        surviving_elements = []
        for element in element_population_pool:
            # Check its true aggregate voltage state parameters live from memory
            current_volts = 0.0
            for atom in element.atoms:
                if hasattr(atom, 'nodes'):
                    current_volts += sum(float(node["energy"]) for node in atom.nodes)
                    
            # STRUCTURAL INTEGRITY STARVATION BOUNDARY
            if current_volts > 300.00:
                # Element possesses sufficient energy current to hold its bonds
                surviving_elements.append(element)
            else:
                # TOTAL COLLAPSE: Dissolve the macro hull and return its mass to the environment
                ex = max(0, min(WIDTH - 1, int(element.x)))
                ey = max(0, min(HEIGHT - 1, int(element.y)))
                
                # Splash its leftover mass back onto the master landscape grid coordinates
                # This directly re-feeds Layer 3, creating rich nutrient fields for the system
                macro_fluid_matrix[ex, ey] = min(8.0, macro_fluid_matrix[ex, ey] + 4.0)
                
                # Wipe active selection focus if this specific target just dissolved from RAM
                if element == selected_element_anchor:
                    selected_element_anchor = None
                    selected_atom_sub_anchor = None  # Tracks the specific Layer 2 atom selected inside the microscope lens
                    
        # Update population pool exclusively with surviving, non-starved macro hulls
        element_population_pool = surviving_elements

                    # --- PHASE 2 MACRO-BUMPER PASS ENGINE (MIRRORED FROM PAGE 17/18) ---
        # Evaluate spatial collision boundary thresholds between your elements
        for i in range(len(element_population_pool)):
            for j in range(i + 1, len(element_population_pool)):
                elem1 = element_population_pool[i]
                elem2 = element_population_pool[j]
                
                # Calculate raw Euclidean geometric vector distances
                dx = elem2.x - elem1.x
                dy = elem2.y - elem1.y
                distance = math.sqrt(dx**2 + dy**2) + 1e-5
                
                # Check if the combined radii create a hardshell boundary overlap
                min_distance = elem1.radius + elem2.radius
                if distance < min_distance:
                    # 1. PHYSICAL OVERLAP SEPARATION
                    # Calculate the precise distance infraction and normalization vector
                    overlap = min_distance - distance
                    nx = dx / distance
                    ny = dy / distance
                    
                    # Push both heavy hulls apart equally by 50% of the violation to prevent spatial clipping
                    elem1.x -= nx * (overlap * 0.5)
                    elem1.y -= ny * (overlap * 0.5)
                    elem2.x += nx * (overlap * 0.5)
                    elem2.y += ny * (overlap * 0.5)
                    
                    # 2. ELASTIC MOMENTUM KINETIC SNAP
                    # Isolate the relative velocity vector paths
                    kx = elem1.vx - elem2.vx
                    ky = elem1.vy - elem2.vy
                    
                    # Calculate the dot product projection along the contact normal axis
                    dot_product = kx * nx + ky * ny
                    
                    # Only execute the rebound bounce if the elements are actively moving toward each other
                    if dot_product > 0:
                        # Hardcoded to your native 0.95 structural conservation elasticity index from Page 18
                        elastic_rebound_index = 0.95
                        rebound_pulse = (1.0 + elastic_rebound_index) * dot_product / 2.0
                        
                        # Deflect and snap the macro-velocity parameters away from the collision axis
                        elem1.vx -= nx * rebound_pulse
                        elem1.vy -= ny * rebound_pulse
                        elem2.vx += nx * rebound_pulse
                        elem2.vy += ny * rebound_pulse
            
            # SEAMLESS 3D TORUS BOUNDARY COUPLING
            if element.x < -element.radius:
                element.x = WIDTH + element.radius
            elif element.x > WIDTH + element.radius:
                element.x = -element.radius
                
            if element.y < -element.radius:
                element.y = HEIGHT + element.radius
            elif element.y > HEIGHT + element.radius:
                element.y = -element.radius
           
    # =====================================================================
    # EXPANDED DATA OBSERVATORY LEDGER & KEYBOARD TOGGLE
    # =====================================================================
    audit_frame_counter += 1
    audit_frame_counter_total += 1  
    
    if audit_frame_counter >= 200:
        audit_frame_counter = 0  # Reset local data clock
       
        current_pop = len(nodes)
        grid_vacuum_ratio = float(np.sum(fluid_matrix < 0.10) / fluid_matrix.size) * 100.0
       
        if current_pop > 0:
            energies = [n["energy"] for n in nodes]
            energy_variance = float(np.std(energies))
           
            # EXPANDED PHYSICAL METRICS (THE TELESCOPE PIPELINES)
            kinetic_surplus = float(sum(n["energy"] * (n["vx"]**2 + n["vy"]**2) for n in nodes))
            metabolic_efficiency = current_pop / max(0.01, grid_vacuum_ratio)
            biomass_density = float(sum(n["energy"] for n in nodes))
            avg_velocity = float(sum(math.sqrt(n["vx"]**2 + n["vy"]**2) for n in nodes) / current_pop)
            max_generation = int(max(n.get("generation", 0) for n in nodes))
        else:
            energy_variance = 0.0
            kinetic_surplus = 0.0
            metabolic_efficiency = 0.0
            biomass_density = 0.0
            avg_velocity = 0.0
            max_generation = 0
       
        # Write the expanded, un-falsified physical logs honestly to your text file
        with open("universe_audit.txt", "a") as f:
            f.write(f"FRAME: {audit_frame_counter_total:6d} | POP: {current_pop:3d} | "
                    f"SCAR_VAL: {grid_vacuum_ratio:5.2f}% | KINETIC_SURPLUS: {kinetic_surplus:8.2f} | "
                    f"METABOLIC_EFF: {metabolic_efficiency:.2f} | BIOMASS_DEN: {biomass_density:.2f} | "
                    f"TROPHIC_VEL: {avg_velocity:.2f} | MAX_GEN: {max_generation:4d}\n")
                   
        # Capture the current macro-geography canvas cleanly inside RAM memory
        snapshot_surface.blit(screen, (0, 0))

                    # --- THE SINGLE-PASS LENS BLIT ---
        # Direct, real-time pixel rendering pipelines for microscopic viewport feeds
    if show_time_lapse:
        # Layout metrics matching your original view box configuration
        box_width = int(WIDTH * 0.25)
        box_height = int(HEIGHT * 0.25)
        box_x = WIDTH - box_width - 10
        box_y = 10

        if active_simulation_layer == 1:
            screen.blit(mini_map_surface, (box_x, box_y))
            
        elif active_simulation_layer == 2 and selected_molecule_anchor:
            screen.blit(selected_molecule_anchor.mini_map_surface, (box_x, box_y))
            
        elif active_simulation_layer == 3 and selected_element_anchor:
            # 1. Create a fresh canvas for the Layer 3 microscope feed on every frame tick
            layer3_lens_surface = pygame.Surface((box_width, box_height))
            layer3_lens_surface.fill((15, 18, 22))  # Laboratory lens interior shade
            
            # Draw a stark technical border around the view screen glass
            pygame.draw.rect(layer3_lens_surface, (0, 255, 100), (0, 0, box_width, box_height), 1)
            
            box_center_x = box_width // 2
            box_center_y = box_height // 2
                    
                    # --- TORUS-AWARE VIEWPORT PROJECTION SWITCHER ---
            if selected_atom_sub_anchor is None:
                # LAYER 2 CELLULAR OVERVIEW VIEW (Torus Wrapped)
                for atom in selected_element_anchor.atoms:
                    # Project using your original, perfect absolute screen percentages
                    scale_x = atom.x / WIDTH
                    scale_y = atom.y / HEIGHT
                    
                    lens_atom_x = int(scale_x * box_width)
                    lens_atom_y = int(scale_y * box_height)
                    
                    lens_atom_x = max(4, min(lens_atom_x, box_width - 4))
                    lens_atom_y = max(4, min(lens_atom_y, box_height - 4))
                    
                    pygame.draw.circle(layer3_lens_surface, (0, 180, 255), (lens_atom_x, lens_atom_y), 2.5)
                    
                lens_txt = FONT.render("LENS: INTERNAL CELLS (L2)", True, (0, 255, 100))
                layer3_lens_surface.blit(lens_txt, (5, 5))
            else:
                # LAYER 1 DEEP MICROSCOPIC SUB-NODE VIEW (Torus Wrapped)
                for node in selected_atom_sub_anchor.nodes:
                    # 1. Compute torus-aware shortest path coordinate deltas relative to sub-anchor cell
                    ndx = node["x"] - selected_atom_sub_anchor.x
                    ndy = node["y"] - selected_atom_sub_anchor.y
                    if ndx > WIDTH * 0.5: ndx -= WIDTH
                    elif ndx < -WIDTH * 0.5: ndx += WIDTH
                    if ndy > HEIGHT * 0.5: ndy -= HEIGHT
                    elif ndy < -HEIGHT * 0.5: ndy += HEIGHT
                    
                    # 2. Project relative node offsets centered inside panel glass
                    lens_node_x = int((ndx * 0.22) + box_center_x)
                    lens_node_y = int((ndy * 0.22) + box_center_y)
                    lens_node_x = max(4, min(lens_node_x, box_width - 4))
                    lens_node_y = max(4, min(lens_node_y, box_height - 4))
                    
                    volt_hue = int(max(0.0, min(1.0, node["energy"])) * 255)
                    node_color = (0, volt_hue, 255)
                    pygame.draw.circle(layer3_lens_surface, node_color, (lens_node_x, lens_node_y), 2)
                    
                lens_txt = FONT.render("LENS: MICRO FILAMENTS (L1)", True, (0, 255, 100))
                layer3_lens_surface.blit(lens_txt, (5, 5))
                
            # Stuffs your compiled viewport lens straight onto your dashboard display panel
            screen.blit(layer3_lens_surface, (box_x, box_y))

    # =====================================================================
    # PHASE 3 EXECUTION: INTERACTIVE SLIDER OVERLAY LAYER
    # =====================================================================
    # if show_dashboard:
    #     panel_rect = pygame.Rect(30, 80, 320, 260)
    #     pygame.draw.rect(screen, (15, 20, 25), panel_rect)
    #     pygame.draw.rect(screen, (0, 255, 100), panel_rect, 1) # Green laser border
       
    #     mouse_x, mouse_y = pygame.mouse.get_pos()
    #     mouse_click = pygame.mouse.get_pressed()[0] # Left click state
       
    #     start_y = 110
    #     slider_idx = 0
       
    #     # --- THE UI CONTEXT OVERRIDE GATE ---
    #     # Forces the visual sliders to display and alter the ACTIVE SELECTED MOLECULE's memory folder
    #     active_sliders_source = selected_molecule_anchor.sliders if (active_simulation_layer == 2 and selected_molecule_anchor) else sliders
       
    #     for key, current_val in active_sliders_source.items():
    #         # Anchor bounds to global limits definition
    #         min_lim = sliders[key][1]
    #         max_lim = sliders[key][2]
    #         label = sliders[key][3]
            
    #         track_x, track_y = 50, start_y + (slider_idx * 35)
    #         track_w = 180
           
    #         pygame.draw.line(screen, (60, 70, 80), (track_x, track_y), (track_x + track_w, track_y), 2)
           
    #         percent = (current_val - min_lim) / (max_lim - min_lim + 1e-5)
    #         knob_x = int(track_x + (percent * track_w))
           
    #         knob_rect = pygame.Rect(knob_x - 5, track_y - 6, 10, 12)
           
    #         if mouse_click:
    #             if active_slider == key or (active_slider is None and knob_rect.collidepoint(mouse_x, mouse_y)):
    #                 active_slider = key
    #                 new_x = max(track_x, min(mouse_x, track_x + track_w))
    #                 new_percent = (new_x - track_x) / track_w
    #                 current_val = min_lim + (new_percent * (max_lim - min_lim))
                    
    #                 # Write modified numbers directly back into the true active data pocket
    #                 if active_simulation_layer == 2 and selected_molecule_anchor:
    #                     selected_molecule_anchor.sliders[key] = current_val
    #                 else:
    #                     sliders[key][0] = current_val
           
    #         pygame.draw.rect(screen, (255, 255, 255), knob_rect)
           
    #         txt_surface = FONT.render(f"{label}: {current_val:.4f}", True, (255, 255, 255))
    #         screen.blit(txt_surface, (track_x, track_y - 18))
           
    #         slider_idx += 1
           
    #     if not mouse_click:
    #         active_slider = None
           
        # THE DIRECT VARIABLE INFLUX GATES
        if active_simulation_layer == 1:
            fluid_matrix += (sliders["solar_pump"][0] - 0.001) * dt
            steering_sensitivity = sliders["steering"][0]
            BASELINE_BURN = sliders["baseline_tax"][0]
            fluid_matrix[fluid_matrix > sliders["ceiling_max"][0]] = sliders["ceiling_max"][0]
            DYNAMIC_FISSION_THRESHOLD = sliders["fission_gate"][0]
            DIFFUSION_STEPS = int(sliders["entropy_clock"][0])
       
    pygame.display.flip() 