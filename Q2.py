import numpy as np
from Polymer import macroMolecule

def main(): #inputs
    try:
        n_input = input("degree of polymerization (1000)?:")
        N=int(n_input) if n_input else 1000

        m_input = input("How many molecules (50)?:")
        M = int(m_input) if m_input else 50
    except ValueError:
        print("Invalid input. Using default values: N=1000, M=50.")
        N, M = 1000, 50

    coms_x, coms_y, coms_z = [], [], [] #Array storage
    e2e_dists = []
    rg_dists = []
    m_weights = []

    for _ in range(M): #Running the simulation 'M' times
        poly = macroMolecule(degreeOfPolymerization = N)
        poly.freelyJointedChainModel()
        #meters-->nanometers
        coms_x.append(poly.centerOfMass.x*1e9)
        coms_y.append(poly.centerOfMass.y*1e9)
        coms_z.append(poly.centerOfMass.z*1e9)
        #meters-->micrometers
        e2e_dists.append(poly.endToEndDistance*1e6)
        rg_dists.append(poly.radiusOfGyration*1e6)
        m_weights.append(poly.MW)

    avg_com_x=np.mean(coms_x)
    avg_com_y=np.mean(coms_y)
    avg_com_z=np.mean(coms_z)

    avg_e2e=np.mean(e2e_dists)
    std_e2e=np.std(e2e_dists, ddof=1)
    avg_rg=np.mean(rg_dists)
    std_rg=np.std(rg_dists, ddof=1)

    m_weights = np.array(m_weights)
    Mn=np.mean(m_weights)
    Mw=np.sum(m_weights**2)/np.sum(m_weights)
    pdi=Mw/Mn

    print(f"\nMetrics for {M} molecules of degree of polymerization = {N}")
    print(f"Avg center of mass (nm) = {avg_com_x:.3f}, {avg_com_y:.3f}, {avg_com_z:.3f}")
    print("End to end distance (um):")
    print(f" Average = {avg_e2e:.3f}")
    print(f" Std. Dev. = {std_e2e:.3f}")
    print("Radius of gyration (um):")
    print(f" Average = {avg_rg:.3f}")
    print (f" Std. Dev. = {std_rg:.3f}")
    print(f"PDI {pdi:.2f}")

if __name__ == "__main__":
    main()
