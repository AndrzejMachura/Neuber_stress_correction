"""This module contains class describing isotropic material.
   Class methods are used to generate lists with data required to define stress-strain curve.
   Ramperg-Osgood relation for isotropic materials was used to define non-linearity of the material"""

import math

class Mat:
    def __init__(self, mat_name, Ftu, Fty, elongation, E):
        self.mat_name= mat_name
        self.Ftu = Ftu
        self.Fty = Fty
        self.elongation = elongation
        self.E= E
        self.n= math.log(self.Ftu/self.Fty)/math.log(self.elongation/0.2) 
        # In original form natural logarithm was used. 
        # Common logarithm do not 
        self.H= self.Fty/(0.002**self.n)
   
    def __str__(self):
        _output = f'Material {self.mat_name} mechanical properties:\n   Young Modulus: {self.E}MPa\n   Ultimate strength: {self.Ftu}MPa\n   Yield strength: {self.Fty}MPa\n   Maximum elongation: {self.elongation}%'
        return _output 

    def generate_stress_list(self):
        return [n for n in range(0, int(self.Ftu*1.05), 1)]
    
    def generate_hooke_strain(self):
        return [i/self.E for i in self.generate_stress_list()]

    def generate_r_o_strain (self):
        return [s/self.E + (s/self.H)**(1/self.n) for s in self.generate_stress_list()]

    def generate_true_strain (self):
        return [math.log(1.+(s/self.E + (s/self.H)**(1/self.n))) for s in self.generate_stress_list()]
    
    def generate_true_stress (self):
        return [s*(1+(s/self.E + (s/self.H)**(1/self.n))) for s in self.generate_stress_list()]

if __name__ == "__main__":

    test_material= Mat("2024-T3",440.,340.,6.,70000.)
    print(test_material)
    material_name=str(test_material.mat_name)
    print("\n\n   "+material_name)
    


