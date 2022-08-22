# Neuber Stress Correction 

    The Neuber method is used to estimate "real" stress based on the linear stress extracted from the FE Model. 
    This method is useful to omit time consuming calculations of non-linear solver with material non-linearity.
    
    Limitations of method:

        1. Can be used only in stress concentration areas like filets or notches.
        2. Mesh should be dense enough to accurately determine stress peak.
        3. Stress field should be mostly linear 



## How to use
    
    Run *Neuber_stress_correction.py* script to convert stress obtained from linear static model to "real" stress.

## Stored files
    
    1. *Neuber_stress_correction.py* - main starting file
    2. *isotropic_material.py* - module contains class describing isotropic material
    3. *instance_tracker* - Decorator used to count number of calls of decorated function or created instances of the class

## License 

    You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
