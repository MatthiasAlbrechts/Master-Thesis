from sklearn.neighbors import KernelDensity
import numpy as np
import scipy.stats

kb = 1.381E-23
T = 300
Na = 6.022E23
beta = 1000 / (Na * kb * T)
# thermal energy in kj/mol
Ethermal = (Na * kb * T) / 1000

# read metaD FES
metaD_fes = np.loadtxt("fes_PM6", skiprows=6, usecols=(0, 1))
metaD_fes_CV = metaD_fes[:, 0]
metaD_fes_E = metaD_fes[:, 1]

# create list to collect reweighted FESs of different subsets
FES_list = []

# calculate high-level FES for every subset
n_subsets = 20
for seed in range(n_subsets):
    # read FEP data
    input = "FEP_data" + str(seed) + ".txt"
    FEP_data = np.loadtxt(input, usecols=(1, 2, 3, 4))

    cv = FEP_data[:, 0]
    bias = FEP_data[:, 1]
    E1 = FEP_data[:, 2]
    E2 = FEP_data[:, 3]
    nconf = len(cv)

    # center bias to avoid numerical problems
    bias_mean = np.mean(bias[:])
    bias_shifted = bias - bias_mean

    # low-level: metaD weights
    w_low = np.exp(beta * bias_shifted)
    # high-level: metaD weights * perturbative weights
    w_high = w_low * np.exp(beta * (E1 - E2))
    # build low-level histogram by fitting Kernal Density model to the subset CV values using low-level weights
    kdelow = KernelDensity(kernel='gaussian', bandwidth=0.05, leaf_size=1000).fit(cv.reshape(-1, 1),
                                                                      sample_weight=w_low)
    # build high-level histogram by fitting Kernal Density model to the subset CV values using high-level weights
    kdehigh = KernelDensity(kernel='gaussian', bandwidth=0.05, leaf_size=1000).fit(cv.reshape(-1, 1),
                                                                       sample_weight=w_high)
 
    # calculate FES from probability distribution of subset
    subset_low_level_FES = - kdelow.score_samples(metaD_fes_CV.reshape(-1, 1)) / beta
    subset_high_level_FES = - kdehigh.score_samples(metaD_fes_CV.reshape(-1, 1)) / beta
    # calculate FEP term
    delta_FEP = subset_high_level_FES - subset_low_level_FES
    # calculate final high-level FES for respective subset
    high_level_FES = metaD_fes_E + delta_FEP
    FES_list.append(high_level_FES)

# find T critical value (95% confidence interval)
tcrit = scipy.stats.t.ppf(q=.025, df=n_subsets - 1)

# calculate arithmetic mean with respective error bars
high_level_FESs = np.stack(FES_list)
mean_high_level_FES = np.mean(high_level_FESs, axis=0)
lower_boundary = mean_high_level_FES - tcrit * np.std(high_level_FESs, axis=0) / np.sqrt(n_subsets)
upper_boundary = mean_high_level_FES + tcrit * np.std(high_level_FESs, axis=0) / np.sqrt(n_subsets)

filename = "high-level FES.txt"
np.savetxt(filename, np.vstack((metaD_fes_CV.T, mean_high_level_FES.T, lower_boundary.T,upper_boundary.T)).T, fmt='%12.3f %12.3f %12.3f %12.3f')
