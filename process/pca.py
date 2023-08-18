from pandas import merge as pandas_merge
from sklearn.decomposition import PCA

def pca(ww_all):

    proc_df = ww_all.pivot(columns='region', values='data').fillna(0.0)
    proc_df.columns = proc_df.columns.rename(None)

    proc_df = proc_df.drop(columns="nation")

    # Standardize the data
    proc_df_standardized = (proc_df - proc_df.mean()) / proc_df.std()
    proc_df_standardized = proc_df_standardized.fillna(0.0)

    # Perform PCA
    pca = PCA(n_components=4)
    _ = pca.fit_transform(proc_df)
    coefficients = pca.components_

    _ = pca.fit_transform(proc_df_standardized)
    coefficients_std = pca.components_

    return {"coeff": coefficients, "coeff_std": coefficients_std, "region": list(proc_df.columns)}

