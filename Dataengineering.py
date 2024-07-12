import pandas as pd 
import numpy as np
from prince import CA
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score,accuracy_score
from scipy.stats import pearsonr
from sklearn.ensemble import RandomForestRegressor

def encode(df):
 label_encoder = LabelEncoder()
 df['genotype_encoded'] = label_encoder.fit_transform(df['genotype'])
 df['rsid_encoded'] = label_encoder.fit_transform(df['rsid'])

# Perform PCA on the encod ed genotypes
 X = df[['genotype_encoded', 'rsid_encoded']]
 pca = PCA(n_components=2)
 pca_result = pca.fit_transform(X)

# Add PCA result back to the original data
 df['pca_encoded_genotype_1'] = pca_result[:, 0]  # First PCA component
 df['pca_encoded_genotype_2'] = pca_result[:, 1]  # Second PCA component

 df.to_csv('Despression summ.csv', index=False)

 return df

def feature_selection(X_train, y_train):
 rf = RandomForestRegressor()
 rf.fit(X_train, y_train)
 Feature=rf.feature_importances_
 return Feature