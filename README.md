# Master-Thesis
This repository contains the necessary scripts to calculate free energy perturbation (FEP) corrections to a free energy surface obtained from a Metadynamics simulation (MetaD) along a collective variable (CV). By means of kernel density estimation (KDE), a weighted histogram is constructed that accounts for the potential energy difference between two reference Hamiltonians, i.e., a low- and high-level potential. By recalculating different subsets of randomly sampled metaD configurations at high-level theory, different high-level FESs are obtained. The arithmetic mean of these FESs is chosen as the estimate of the true high-level FES. 

HOWTO

1) Run a MetaD simulation using a low-level potential (U_LL), e.g. semiepirical or DFTB and reach convergence
 
   write out a colvar file with the following columns

   Time       CV      metad.rbias      U_LL    
   
   write out an xyz file containing the configurations used in the colvar file 
   
2) Recalculate the energies of a subset of configurations at high-level potential by running the "high-level energies.py" script. The high-level energies are                automatically added to the colvar data of this subset under the name "FEP_dataX.txt", where X is the random seed used in the selection of the configurations.            By default, a subset of 500 configurations is calculated. Choose the number of subsets, depending on the size of the system and the desired precision.          
   Move the "FEP_dataX.txt" files to the "KDE" folder.
   
3) Run the "KDE reweighting.py" script in the "KDE" folder. The estimate of the true high-level FES is calculated as the arithmetic mean of the high-level FESs that are    calculated from the different subsets. Error bars are calculated at the 95% confidence interval. The high-level FES with respective error bars is written out in the      "high-level FES.txt" file.


