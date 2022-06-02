from ase.io import read
from ase.calculators.gaussian import Gaussian
from ase.units import kJ,mol
import numpy as np
from sklearn.model_selection import train_test_split

# read colvar file
# discard first half of metaD configurations
n_skip_config = 100000
plumed_all = np.loadtxt("colvar", skiprows=1+n_skip_config, usecols=(0,3,4,5))
# count number of configurations
n_configurations = len(plumed_all[:,0])

# assign index to each configuration
index_config = np.empty((n_configurations))
for i in range(n_configurations):
    index_config[i] = i

# select random subset of configurations
size = 500
seed = 0
configs_train, configs_test = train_test_split(index_config, random_state=seed, shuffle=True, test_size=size)
indexes = np.array(configs_test).astype(int)
# select configurations from colvar file
plumed_subset = np.empty((size,4))
configs = []
for i in range(size):
    plumed_subset[i, :] = plumed_all[indexes[i], :]
    # read coordinates of selected configs
    config_subset = read("sn2-pos-1.xyz", index=indexes[i] + n_skip_config, format="xyz")
    configs.append(config_subset)

# set up PBE0/def2-SVP(P) calc with Gaussian
energies_dum = []
calc = Gaussian(label='calc/gaussian',
                method='pbe1pbe',
                basis='Def2SVPP',
                charge=-1)

# re-evaluate all read configurations
for atoms in configs:
    atoms.calc = calc
    energies_dum.append(atoms.get_potential_energy())

# convert to kJ/mol (standard PLUMED unit)
energies_high = np.array(energies_dum)
energies_high = energies_high / (kJ / mol)

# shift energies to similar levels
plumed_subset[:, 3] = plumed_subset[:, 3] - np.mean(plumed_subset[:, 3])
energies_high = energies_high - np.mean(energies_high)
# add high-level energies to file with CV-values, bias and low-level energies
filename = "FEP_data" + str(seed) + ".txt"
np.savetxt(filename, np.vstack((plumed_subset.T, energies_high.T)).T, fmt='%12.3f %12.3f %12.3f %12.3f %12.3f')

