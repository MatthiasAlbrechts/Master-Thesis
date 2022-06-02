# Master-Thesis
This repository contains the necessary scripts to calculate free energy perturbation (FEP) corrections to a free energy surface obtained from a Metadynamics simulation (MetaD) along a collective variable (CV). By means of kernel density estimation (KDE), a weighted histogram is constructed that accounts for the potential energy difference between two reference potentials. 

HOWTO

1) Run a MetaD simulation using a low-level potential (U_LL), e.g. semiepirical or DFTB and reach convergence
 
   write out a colvar file with the following columns
   ________________________________________
   Time       CV      metad.rbias      U_LL    
   ...
   ...
   ________________________________________
   
   write out an xyz file containing the configurations used in the colvar file 
   
2) Calculate the energies of a subset of configurations at a different (high-level) potential by running the "high-level energies.py" script. The high-level energies are    automatically added to the colvar data of this subset under the name "FEP_dataX.txt", where X is the random seed used in the selection of the configurations, and        serves as index of the subset. By default, a subset of 500 configurations is calculated. The user can choose the number of subsets to be calculated, depending on        the size of the system and the desired precision. Move the "FEP_dataX.txt" files to the KDE folder.
   
3) Calculate the energy only of these configurations using a high-level potential (U_HL)

6) Run metaFEP_histo_rew.py

7) This will produce the file MetaFEP.dat containing the FEP free energy along 
   the CV smoothed using a moving average filter and relative 95% confidence 
   lower and upper bounds. Raw FEP data also available in last column (noisy)
