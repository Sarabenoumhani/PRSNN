This repository outlines the key steps for running the PRSNN technique, including data collection,
ensuring data quality, and the deep learning phase. It utilizes summary statistics data from the
Psychiatric Genomics Consortium (PGC) and genotypes data from Opensnp. In the supplementary
material, we present one of the three datasets used in our study, derived from PGC. Specifically,
this dataset focuses on depression disease.


• The Data library includes essential functions for collecting individual genotypes from Opensnp, preprocessing PGC data, and handling the data. Its main purpose is to prepare datasets.

• The Daraengineering library contains functions such as encode functionthat performs label
encoding and PCA on the input data.

• The PRS library contains functions for calculating the polygenic risk scores.
