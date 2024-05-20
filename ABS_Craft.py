# Bottom Shell
# Side Shell
# Strenght Deck and other Decks
# Superstructure and Deckhouses – Front, Sides, Ends, and Tops
# Tank Bulkheads
# Watertight Bulkheads
# Water Jet Tunnels


import math
import numpy as np
from validations import val_data


class Craft:


    MATERIALS = ('Acero', 'Aluminio', 'Fibra laminada', 'Fibra en sandwich')
    ZONES = ('Vagra Maestra', 'Fondo', 'Costado', 'Cubiertas', 'Superestructura y Casetas', 'Mamparos Estancos y de Tanques')

    def __init__(self):
        print("\nEscantillonados ABS Highspeed Craft --- ABS Highspeed Craft Scantlings\n")
        self.L = val_data("Ingrese la eslora de escantillón (metros): ")
        self.LW = val_data("Ingrese la eslora de la línea de flotación (metros): ")
        self.B = val_data("Ingrese la manga de su embarcación (metros): ")
        self.BW = val_data("Ingrese la manga de la línea de flotación (metros): ")
        self.D = val_data("Ingrese el puntal de su embarcacion (metros): ")
        self.d = val_data("Ingrese el calado de la embarcación (metros): ")
        self.V = val_data("Ingrese la velocidad (nudos): ")
        self.W = val_data("Ingrese el desplazamiento de la embarcación (kg): ")
        self.Bcg = val_data("Ingrese la astilla muerta fondo en LCG (°grados): ")
        self.material = self.select_material()
        self.context = self.select_context()
        self.zone = self.select_zone()
        self.sigma_u = val_data("Ingrese el esfuerzo ultimo a la tracción (MPa): ")
        self.sigma_y = val_data("Ingrese el limite elastico por tracción (MPa): ")
        self.resistencia = self.determine_resistencia()
        self.sigma_ap = self.dstress_plating(self.zone)
        self.sigma_ai = self.dstress_internals(self.zone)


    #Función para mostrar el menú en consola
    def display_menu(self, items) -> None:
        """Muestra un menú basado en una lista de items."""
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

    def select_material(self) -> int:
        print("\nLista de materiales disponibles")
        self.display_menu(self.MATERIALS)
        opcion = val_data("Seleccione un material (Ingrese el número correspondiente): ", False, True, -1, 1, len(self.MATERIALS))
        return opcion

    #Revisar esta función
    def select_context(self) -> int:
        print("\n1. Chapado \
               \n2. Refuerzos")
        opcion = val_data("\nIngrese el número correspondiente al analisis: ", False, True, -1, 1, len(self.ZONES))
        return opcion

    def determine_resistencia(self) -> str:
        if self.material == 'Acero':
            if 200 < self.sigma_y < 300:
                return 'Ordinaria'
            elif 300 <= self.sigma_y:
                return 'Alta'
            else:
                return 'Baja'
        else:
            return 'Ordinaria'

    def select_zone(self) -> int:
        print("\nSeleccione la zona que desea escantillonar")
        self.display_menu(self.ZONES)
        choice = val_data("Ingrese el número correspondiente: ", False, True, -1, 1, len(self.ZONES))
        return choice

    

    def dstress_internals(self, zone) -> tuple:  #Corregir
        """Calcula el esfuerzo de diseño basado en la zona seleccionada."""
        zones = {
            'Fondo': {
                'Bottom Longitudinals Slamming Pressure': 0.65 * self.sigma_y,
                'Bottom Transverse and Girders Slamming pressure': 0.80 * self.sigma_y,
                'Bottom Longitudinals Sea Pressure': 0.50 * self.sigma_y,
                'Bottom Transverses and Girders Sea pressure': 0.60 * self.sigma_y
            },
            'Costado': {
                'Side Longitudinals Slamming Pressure': 0.60 * self.sigma_y,
                'Side Transverses and Girders Slamming Pressure': 0.80 * self.sigma_y,
                'Side Longitudinals Sea Pressure': 0.50 * self.sigma_y,
                'Side Transverses and Girders Sea Pressure': 0.60 * self.sigma_y,
            },
            'Cubiertas, Mamparos y Superestructura': {
                'Deck Longitudinals - Strength Decks': 0.33 * self.sigma_y,
                'Deck Longitudinals - Other Decks': 0.40 * self.sigma_y,
                'Deck Transverses and Girders Strength Decks': 0.75 * self.sigma_y,
                'Deck Transverses and Girders Other Decks': 0.75 * self.sigma_y, 
                'Wet Deck Longitudinals': 0.75 * self.sigma_y,
                'Wet Deck Transverses and Girders': 0.75 * self.sigma_y,
                'Watertight Bulkheads': 0.85 * self.sigma_y,
                'Tank Bulkheads': 0.60 * self.sigma_y,
                'Superstructure and Deckhouse': 0.70 * self.sigma_y
            },
        }
        if zone == 'Cuaderna Maestra':
            zone = 'Fondo'
        selected_zone = zones[zone]
        stress_values = tuple(selected_zone.values())
        return stress_values 



class Pressures:


    def __init__(self, craft: Craft):
        self.craft = craft
        #   Atributos internos para almacenar valores
        self.N1 = 0.1
        self.N2 = 0.0078
        self.N3 = 9.8
        self.tau = val_data("\nÁngulo de trimado a máxima velocidad (grados): ", True, True, -1, 3)
        # self.lp = val_data("\nDigite el borde más largo del panel de la placa, en cm: ")
        # self.sp = val_data("Digite el borde más corto del panel de la placa, en cm: ")
        # self.l = val_data("\nIngrese la longitud sin apoyo del refuerzo en cm: ")
        # self.s = val_data("Ingrese la separación de los longitudinales o rigidizadores del fondo, en cm: ")
        # self.h13 = self.calculate_h13()
        self.ncg = self.calculate_ncg()
        # self.FDp, self.FDs = self.calculate_FD()
        # self.FV = self.calculate_FV()
        
    
    #Juntar estas 2 funciones en el opcion
    def calculate_h13(self) -> float:
        print("\nSeleccione el tipo de embarcacón de diseño:\n1: High-Speed Craft \n2: Coastal Craft \n3: Riverine Craft")
        select = val_data("Ingrese el número correspondiente: ", False, True, 0, 1, 3)
        if select == 1:
           return max(4, (self.craft.L / 12))
        elif select == 2:
            return max(2.5, (self.craft.L / 12))
        else:
            return max(0.5, (self.craft.L / 12)) 
    
    def calculate_ncg(self) -> float:
        kn = 0.256
        ncg_limit = 1.39 + kn * (self.craft.V / math.sqrt(self.craft.L))
        _ncg = self.N2 * (((12 * self.h13) / self.craft.BW) + 1) * self.tau * (50 - self.craft.Bcg) * ((pow(self.craft.V, 2) * pow(self.craft.BW, 2)) / self.craft.W)
        ncg = min(ncg_limit, _ncg)
        if self.craft.V > (18 * math.sqrt(self.craft.L)):
            opcion = val_data("\nIngrese 1 si su embarcación es regular o 2 si es de búsqueda y rescate\n")
            if opcion == 1: #embarcación regular
                ncg = 6
            else:   #embarcación de búsqueda y rescate
                ncg = 7
        if self.craft.L < 24 and ncg < 1:
            ncg = 1
        return ncg
     
    def calculate_FD(self):
        ADp = min(self.lp * self.sp, 2.5 * pow(self.s, 2))
        ADs = max(self.l * self.s, 0.33 * pow(self.l, 2))
        # Calculo de AR
        AR = 6.95 * self.craft.W / self.craft.d
        # Valores de AD/AR
        ADRp = ADp / AR
        ADRs = ADs / AR
        # Puntos conocidos y sus valores correspondientes
        x_known = [0.001, 0.005, 0.010, 0.05, 0.100, 0.500, 1]
        y_known = [1, 0.86, 0.76, 0.47, 0.37, 0.235, 0.2]
        
        # Interpolación manual para ADRp
        FDp = 0.2  # Valor por defecto
        for i in range(len(x_known) - 1):
            if x_known[i] <= ADRp <= x_known[i + 1]:
                FDp = y_known[i] + (y_known[i + 1] - y_known[i]) * (ADRp - x_known[i]) / (x_known[i + 1] - x_known[i])
                break
        # Asegurar que FDp esté dentro [0.4, 1.0]
        FDp = min(max(FDp, 0.4), 1.0)
        
        # Interpolación manual para ADRs
        FDs = 0.2  # Valor por defecto
        for i in range(len(x_known) - 1):
            if x_known[i] <= ADRs <= x_known[i + 1]:
                FDs = y_known[i] + (y_known[i + 1] - y_known[i]) * (ADRs - x_known[i]) / (x_known[i + 1] - x_known[i])
                break
        # Asegurar que FDs esté dentro [0.4, 1.0]
        FDs = min(max(FDs, 0.4), 1.0)
        
        return FDp, FDs

    def calculate_FV(self) -> float:
        print("\n*Nota: Pulse Enter si desea tomar el valor mayor de FV")
        Lx = val_data("Ingrese la distancia a popa donde se esta realizando los calculos (metros): ", True, True, 0)
        Fx = Lx / self.craft.L
        # Puntos conocidos y sus valores correspondientes
        x_known = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.445, 0.4, 0.3, 0.2, 0.1, 0]
        y_known = [0.25, 0.39, 0.52, 0.66, 0.8, 0.92, 1, 1, 1, 1, 1, 0.5]
        # Si Fx es exactamente 0 o 1, retornar los valores correspondientes
        if Fx == 0:
            return 1
        if Fx == 1:
            return 0.25
        # Interpolación manual
        FV = 1  # Valor por defecto
        for i in range(len(x_known) - 1):
            if x_known[i] >= Fx >= x_known[i + 1]:
                FV = y_known[i] + (y_known[i + 1] - y_known[i]) * (Fx - x_known[i]) / (x_known[i + 1] - x_known[i])
                break
        # Asegurar que FV esté dentro [0.25, 1.0]
        FV = min(max(FV, 0.25), 1.0)      
        return FV
    
    

    def bottom_pressure(self):
        slamming_pressure_less61 = (((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + self.ncg) * self.FDp * self.FV)
        hidrostatic_pressure = self.N3 * (0.64 * self.h13 + self.craft.d)
        return max (slamming_pressure_less61, hidrostatic_pressure)

    def side_transom_pressure(self):
        slamming_pressure = ((self.N1 * self.craft.W) / (self.craft.LW * self.craft.BW)) * (1 + self.nxx) * ((70 - self.Bsx) / (70 - self.Bcg)) * self.FD
        hidrostatic_pressure = self.N3 * (self.Hs - y)
        # where L is generally not to be taken less than 30 m page 71
        fore_end = 0.28 * Fa * Cp * N3 * (0.22 + 0.15 * math.tan(alfa)) * ((0.4 * self.craft.V * math.cos(beta) + 0.6 * self.craft.L ** 0.5) ** 2)
        return max(slamming_pressure, hidrostatic_pressure) if self.craft.L < 30 else max(slamming_pressure, hidrostatic_pressure), fore_end
    
    
    #revisar de aqui para abajo
    def wet_deck_pressure(self):
        deck_pressure = 30 * self.N1 * self.FD * self.F1 * self.craft.V * self.v1 * (1 - 0.85 * self.ha / self.h13)
        return deck_pressure
    
    def decks_pressures(self):
        pass
    
    def superstructures_pressures(self):
        pass
    
    def bulkheads_pressures(self):
        pass



class Plating_acero_aluminio:
    
    
    def __init__(self, craft: Craft, pressure: Pressures):
        self.craft = craft
        self.pressure = pressure
        self.k = self.calculate_k_k1()[0] if self.craft.material in ['Acero', 'Aluminio'] else self.calculate_k_k1()[1]


    def calculate_k_k1(self) -> tuple:
        # Definir las listas en orden creciente
        ls_known = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        k_known = [0.308, 0.348, 0.383, 0.412, 0.436, 0.454, 0.468, 0.479, 0.487, 0.493, 0.500]
        k1_known = [0.014, 0.017, 0.019, 0.021, 0.024, 0.024, 0.025, 0.026, 0.027, 0.027, 0.028]
        
        ls = self.l / self.s

        if ls > 2.0:
            k = 0.500
            k1 = 0.028
        elif ls < 1.0:
            k = 0.308
            k1 = 0.014
        else:
            # Realiza la interpolación
            k = np.interp(ls, ls_known, k_known)
            k1 = np.interp(ls, ls_known, k1_known)

        return k, k1
    
    #Voy por aqui
    def dstress_plating(self, zone) -> tuple:  
        """Calcula el esfuerzo de diseño 'sigma_a' basado en la zona seleccionada."""
        if self.craft.zone == 1:#Corregir
            zones = {
                'Fondo': {
                    'Bottom Shell Slamming Pressure': 0.90 * self.sigma_y,
                    'Bottom Shell Hydrostatic Pressure': 0.55 * self.sigma_y,
                },
                'Costado': {
                    'Side Shell Slamming Pressure': 0.90 * self.sigma_y,
                    'Side Shell Hydrostatic Pressure': 0.55 * self.sigma_y,
                },
                'Cubiertas, Mamparos y Superestructura': {
                    'Deck Plating Strength Deck': 0.60 * self.sigma_y,
                    'Deck Plating Lower Decks/Other Decks': 0.60 * self.sigma_y,
                    'Deck Plating Wet Decks': 0.90 * self.sigma_y,
                    'Bulkheads Deep Tank': 0.60 * self.sigma_y,
                    'Bulkheads Watertight': 0.95 * self.sigma_y
                }
            }
            if zone == 'Cuaderna Maestra':
                zone = 'Fondo'
            selected_zone = zones[zone]
            stress_values = tuple(selected_zone.values())
        return stress_values
    
    #The thickness of the shell, deck or bulkhead plating
    def lateral_loading(self) -> float:
        t1 = self.s * 10 * math.sqrt((self.pressure * self.k)/(1000*self.d_stressp))
        return t1
        
    def secondary_stiffening(self) -> float:
        if self.craft.material == "Acero":
            return 0.01 * self.s
        else:
            return 0.012 * self.s
        
    def minimun_thickness(self) -> float:
        if self.craft.zone == 1:    #Fondo
            if self.craft.material == "Acero":
                return max(0.44 * math.sqrt(self.craft.L * self.qs) + 2, 3.5)
            else:
                return max(0.70 * math.sqrt(self.craft.L * self.qa) + 1, 4.0)
        elif self.craft.zone == 2:  #Costados y Espejo
            if self.craft.material == "Acero":
                return max(0.40 * math.sqrt(self.craft.L * self.qs) + 2, 3.0)
            else:
                return max(0.62 * math.sqrt(self.craft.L * self.qa) + 1, 3.5)
        elif self.craft.zone == 3:  #Cubierta principal
            if self.craft.material == "Acero":
                return max(0.40 * math.sqrt(self.craft.L * self.qs) + 1, 3.0)
            else:
                return max(0.62 * math.sqrt(self.craft.L * self.qa) + 1, 3.5)
        elif self.craft.zone == 4:  #Lower Decks, W.T. Bulkheads, Deep Tank Bulkheads
            if self.craft.material == "Acero":
                return max(0.35 * math.sqrt(self.craft.L * self.qs) + 1, 3.0)
            else:
                return max(0.52 * math.sqrt(self.craft.L * self.qa) + 1, 3.5)
      
    #Water Jet Tunnels
    t = self.s * math.sqrt(pressure * self.k / (1000 * self.d_stressp))
    
    #Transverse Thruster Tubes
    t = 0.008 *self.d * math.sqrt(Q) + 3.0
    
    #Decks Provided for the Operation or Stowage of Vehicles
    t = math.sqrt((self.beta * self.W *(1 + 0.5 * self.nxx)) / self.sigma_a)
    
    