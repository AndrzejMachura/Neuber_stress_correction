from unittest.mock import call
import pylab
from os import system
from isotropic_material import Mat
from instance_tracker import InstanceTracker

class MatNameError (Exception):
    pass
class NegativeValue (Exception):
    pass
class ModulusError (Exception):
    pass
class UltStrError (Exception):
    pass
class ElongationError (Exception):
    pass

@InstanceTracker
class PeakStressMat(Mat):
    
    def __init__(self, peak, *arguments):
        Mat.__init__(self, *arguments)
        self.peak_stress= peak 
    
    def generate_hooke_stress(self):
        return [n for n in range(0, int(self.peak_stress*1.05), 1)]
    
    def generate_hooke_strain(self):
        return [i/self.E for i in self.generate_hooke_stress()]


#class Results(PeakStressMat): 
#    pass #pamiętaj by uzupelnic


def generate_chart(Y=Mat("2024-T72", 470, 300, 11, 71000)):

    ultimate_elongation = [0., 1.1*max(Y.generate_r_o_strain())]
    ultimate_stress = [Y.Ftu, Y.Ftu]
    peak_strain = peak_stress/Y.E


    pylab.title("Stress-Strain")
    pylab.plot(Y.generate_r_o_strain(),Y.generate_stress_list(),'y')
    pylab.plot(Y.generate_hooke_strain(),Y.generate_hooke_stress(),'b')
    pylab.plot(ultimate_elongation,ultimate_stress,'r')
    pylab.plot(peak_strain, peak_stress, 'g', marker=".", markersize=10)
    pylab.legend(['Engineering Stress-Strain','True Stress-Strain','Ultimate Stregnth','Peak Stress Point'], loc='lower right', shadow=True, fontsize='medium', title='Legend')
    pylab.ylim(0., 1.1*max(Y.generate_hooke_stress()))
    pylab.ylabel("Stress [MPa]")
    pylab.xlim(0., 1.1*max(Y.generate_r_o_strain()))
    pylab.xlabel("Strain [-]") 
    pylab.grid(True)  
    pylab.savefig(str(Y.mat_name)+".jpg", dpi = 720) 
    pylab.show()

def generate_text_file(X=Mat("2024-T72", 470, 300, 11, 71000)):
    file = open(X.mat_name+".txt","w")
    file.write(str(X)+"\n")
    file.write("Row Number\tEngineering Strain\tEngineering Stress\tTrue Strain\tTrue Stress \n")
    i=0
    while i < len(X.generate_stress_list()):
        e_strain = "{:.3e}".format(X.generate_r_o_strain()[i])
        e_stress = "{:.3e}".format(X.generate_stress_list()[i])
        tr_strain = "{:.3e}".format(X.generate_true_strain()[i])
        tr_stress = "{:.3e}".format(X.generate_true_stress()[i])
        file.write(str(i+1)+"\t"+str(e_strain)+"\t"+str(e_stress)+"\t"+str(tr_strain)+"\t"+str(tr_stress)+"\n")
        i+=1
    
    file.close()

print("Required units are given in brackets \n")

Results_list =[] #list of results declared for further usege in output file generation

while True:
    print("\nMenu:\n")
    print("1. Generate new material curve")
    print("2. Calculate reduced stress")
    print("3. Generate output file")
    print("4. Exit\n") 
    try: 
        i= int(input("Print number to choose option:\n"))
    except ValueError:
        print("Menu option must be given")
        system("PAUSE")
        print("\n")
        continue

    match i:
        case 1:      
            try:
                mat_name= input("Give material name: ")
                if mat_name =="": raise MatNameError
                E = float (input("Give Younga modulus (MPa): "))
                Ftu = float (input("Give Ultimate Tensile Strength (MPa): "))
                Fty = float (input("Give Yield Tensile Strength (MPa): ")) 
                u = float (input("Give maximum elongation (%): "))
                material = Mat(mat_name, Ftu, Fty, u, E)
                
                if E<0 or Ftu<0 or Fty<0 or u<0: raise NegativeValue
                if E<Ftu: raise ModulusError
                if Ftu<Fty: raise UltStrError
                if u/100.<= 0.002: raise ElongationError

            except MatNameError:
                print("\n") 
                print("Material should be named.\n")               
                system("PAUSE")
                print("\n")              
                continue

            except ValueError:
                print("\n") 
                print("All marterial physical properties should be given.\n")               
                system("PAUSE")
                print("\n")              
                continue

            except NegativeValue:
                print("\n") 
                print("All marterial physical properties should be positive numbers.\n")
                system("PAUSE")
                print("\n")                 
                continue

            except ModulusError:
                print("\n")                 
                print("Young Modulus should be greater than Ultimate Tensile Strength.\n")
                system("PAUSE")
                print("\n")                  
                continue

            except UltStrError:
                print("\n")                
                print("Ultimate Tensile Strength should be greater than Yield Tensile Strength.\n")
                system("PAUSE")
                print("\n")                
                continue

            except ElongationError:
                print("\n")                
                print('Maximum Elongation should be greater than 0.2%.\n')
                system("PAUSE")
                print("\n")                
                continue                
        case 2:    
            
            while True:
                try:
                    peak_stress = float (input("Give linear peak stress (MPa): "))
                    mat_wp= PeakStressMat(peak_stress, "2024", 440., 340., 8., 70000. )
                    print(f"case no.: {PeakStressMat.counter} ")
                    generate_chart (mat_wp)
                    break
                except ValueError:
                    print ("ValueError: Invalid Value.\nTry once again.\n")
                    system("PAUSE")
                    continue
                except NameError:
                    print ("Invalid Stress-Strain curve.\nPlease define material curve\n")
                    system("PAUSE")
                    break
            
        case 3:
            try:
                generate_text_file(material)
            except NameError:
                generate_text_file()
        case 4:
            break