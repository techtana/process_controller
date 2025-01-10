import numpy as np

class Soil:
    """Water evaporation from soil follows 2 main stages:
        1. Atmosphere-controlled stage
            Evaporation is largely independent of soil 
            moisture content and evaporation occurs near 
            the free-water rate.
        2. Soil-controlled stage
            Evaporation rate is determined by the rate
            at which water can be conducted to the surface
            rather than by atmospheric conditions.
    """
    def __init__(self,):
        self.moisture = 30
        self.area = 1
    
    def intake(self, w):
        absorb = w/self.moisture if self.moisture < 100 else 0
        self.moisture = self.moisture + absorb
        return absorb
    
    def evaporate_mock(self, F, H, dt):
        """Mock equation, inspired by the equation below. Not exactly the same.
        
        src: https://www.engineeringtoolbox.com/evaporation-water-surface-d_690.html
        
        Parameter
        ---------
        F: float
            air flow (m/s^2)
        H: float
            Atmostpheric humudity (kg/m^3)
        M: float
            Soil humidity (kg/m^3)
        dt: float
            period of time
        
        Return
        ------
        float
            kilograms of water evaporated
        """
        x = np.log(self.moisture/H)
        # x = (self.moisture - H)/H
        evap = (3+F*0.277)*x*dt
        self.moisture = self.moisture - evap/self.moisture
        return evap
    
    @staticmethod
    def evaporate_rate__free_water(m, R_n, rho_a, c_p, delta_e, g_a, lambda_v, gamma):
        """Penman equation
        
        src: https://en.wikipedia.org/wiki/Penman_equation
        
        Parameter
        ---------
        m: float
            Slope of the saturation vapor pressure curve (Pa K^-1)
        R_n: float
            Net irradiance (W m^-2)
        rho_a: float
            density of air (kg m^-3)
        c_p: float
            heat capacity of air (J kg^-1 K^-1)
        delta_e: float
            vapor pressure deficit (Pa)
        g_a: float
            momentum surface aerodynamic conductance (m s^-1)
        lambda_v: float
            latent heat of vaporization (J kg^-1)
        gamma: float
            psychrometric constant (Pa K^-1)
        
        Return
        ------
        float
            units of kg/(m2·s) -- kilograms of water evaporated
            every second for each square meter of area.
        """
        
        return (m*R_n+rho_a*c_p*delta_e*g_a)/(lambda_v*(m+gamma))
    
    @staticmethod
    def stage_1_evaporate(t1):
        E_1 = evaporate_rate__free_water(m, R_n, rho_a, c_p, delta_e, g_a, lambda_v, gamma)
        F_1 = E_1*t1
        return E_1, F_1
    
    @staticmethod
    def stage_2_evaporate(t, t1, F1, E1):
        E_t = (8/np.sqrt(np.pi))*E1*t1/t
        F_t = F1*(1+(8/np.sqrt(np.pi)*np.log(t/t1)))
        return E_t, F_t